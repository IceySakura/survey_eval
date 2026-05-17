"""文献搜索工具 - 用于验证论文存在性

复用自 literature_tools.py 的逻辑，使用 Google Scholar 和 Semantic Scholar。
支持磁盘缓存，避免重复请求。
"""

import os
import re
import json
import time
import random
import hashlib
import logging
import asyncio
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
import aiohttp

logger = logging.getLogger(__name__)

SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1"
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")

# 有 API key 时限制更宽松（1 req/s），无 key 时保守设置
S2_RATE_LIMIT_INTERVAL = 1.5 if SEMANTIC_SCHOLAR_API_KEY else 5.0
S2_MAX_RETRIES = 3
S2_BASE_RETRY_DELAY = 10.0  # 遇限流时的基础等待时间（秒）

# Google Scholar 因 CAPTCHA 在自动化场景下不可用，已禁用
SCHOLARLY_AVAILABLE = False


@dataclass
class PaperInfo:
    """论文信息"""
    title: str
    authors: List[str]
    year: str
    venue: str = ""
    abstract: str = ""
    citation_count: int = 0
    arxiv_id: str = ""
    doi: str = ""
    source: str = ""
    exists: bool = True


class LiteratureSearch:
    """文献搜索器（带磁盘缓存）"""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Args:
            cache_dir: 搜索结果缓存目录，默认 eval/cache/search
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / "cache" / "search"
        self._cache_dir = cache_dir
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        self._last_s2_request_time = 0.0
        self._s2_headers = {}

        if SEMANTIC_SCHOLAR_API_KEY:
            self._s2_headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY
            logger.info("Semantic Scholar: 使用 API Key（更宽松的限流）")


    # ------------------------------------------------------------------ cache

    def _cache_key(self, query: str) -> str:
        """生成缓存键（用 query 的 md5）"""
        return hashlib.md5(query.lower().strip().encode()).hexdigest()

    def _load_cache(self, query: str) -> Optional[List[Dict]]:
        """从磁盘读取缓存"""
        path = self._cache_dir / f"{self._cache_key(query)}.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
                logger.debug(f"  [缓存命中] {query[:40]}")
                return data
            except Exception:
                pass
        return None

    def _save_cache(self, query: str, results: List[Dict]):
        """将结果写入磁盘缓存"""
        path = self._cache_dir / f"{self._cache_key(query)}.json"
        try:
            path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception as e:
            logger.warning(f"缓存写入失败: {e}")

    # -------------------------------------------------------------- title match

    def _titles_match(self, title1: str, title2: str, threshold: float = 0.7) -> bool:
        def normalize(s):
            return re.sub(r'[^\w\s]', '', s.lower()).strip()
        t1, t2 = normalize(title1), normalize(title2)
        if t1 == t2:
            return True
        words1, words2 = set(t1.split()), set(t2.split())
        if not words1 or not words2:
            return False
        similarity = len(words1 & words2) / max(len(words1), len(words2))
        return similarity > threshold

    # ----------------------------------------------- Semantic Scholar (async)

    async def _s2_request(
        self, session: aiohttp.ClientSession, url: str, params: dict
    ) -> Optional[aiohttp.ClientResponse]:
        """带限流和指数退避的 S2 请求"""
        for attempt in range(S2_MAX_RETRIES):
            now = time.time()
            elapsed = now - self._last_s2_request_time
            if elapsed < S2_RATE_LIMIT_INTERVAL:
                await asyncio.sleep(S2_RATE_LIMIT_INTERVAL - elapsed)
            self._last_s2_request_time = time.time()

            response = await session.get(url, params=params, headers=self._s2_headers)

            if response.status == 429:
                # 指数退避 + 随机抖动，避免集体重试
                wait = S2_BASE_RETRY_DELAY * (2 ** attempt) + random.uniform(0, 2)
                logger.warning(f"Semantic Scholar 限流，等待 {wait:.1f}s（第{attempt+1}次重试）")
                await asyncio.sleep(wait)
                continue

            return response

        logger.error("Semantic Scholar 多次限流，放弃本次请求")
        return None

    async def _search_semantic_scholar(self, query: str, limit: int = 5) -> Optional[List[Dict]]:
        params = {
            "query": query,
            "limit": limit,
            "fields": "paperId,title,authors,year,abstract,citationCount,externalIds,venue"
        }
        url = f"{SEMANTIC_SCHOLAR_API_URL}/paper/search"

        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await self._s2_request(session, url, params)
            if response is None:
                return None
            if response.status != 200:
                logger.warning(f"Semantic Scholar 搜索失败 ({response.status})")
                return None
            data = await response.json()

        papers = data.get("data", [])
        if not papers:
            return None

        result = []
        for paper in papers:
            authors = [a.get("name", "") for a in paper.get("authors", [])]
            external_ids = paper.get("externalIds", {})
            result.append({
                "title": paper.get("title", ""),
                "authors": authors,
                "year": str(paper.get("year", "")),
                "venue": paper.get("venue", ""),
                "abstract": paper.get("abstract", ""),
                "citation_count": paper.get("citationCount", 0),
                "arxiv_id": external_ids.get("ArXiv", ""),
                "doi": external_ids.get("DOI", ""),
                "source": "semantic_scholar"
            })
        return result

    # ------------------------------------------------------------ public API

    async def search(self, query: str, limit: int = 5) -> Optional[List[Dict]]:
        """搜索文献（优先读缓存，命中则直接返回）

        仅使用 Semantic Scholar。Google Scholar 因 CAPTCHA 在自动化场景下不可用，
        已禁用以避免长时间挂起。

        Args:
            query: 搜索关键词
            limit: 返回结果数量
        """
        # 1. 读缓存
        cached = self._load_cache(query)
        if cached is not None:
            return cached

        papers = None

        # 2. Semantic Scholar
        for attempt in range(S2_MAX_RETRIES):
            try:
                s2_papers = await self._search_semantic_scholar(query, limit)
                if s2_papers:
                    papers = s2_papers
                    logger.info(f"Semantic Scholar 搜索成功: {len(papers)} 篇")
                    break
            except Exception as e:
                logger.warning(f"Semantic Scholar 搜索失败: {e}")
            if attempt < S2_MAX_RETRIES - 1:
                await asyncio.sleep(S2_BASE_RETRY_DELAY * (attempt + 1))

        # 3. 写缓存（None 保存为空列表，防止反复重试同一个失败查询）
        self._save_cache(query, papers or [])
        return papers

    async def verify_paper_exists(
        self,
        title: str,
        authors: List[str] = None,
        year: str = None
    ) -> PaperInfo:
        """验证论文是否存在"""
        query = f"{authors[0]} {title}" if authors else title

        papers = await self.search(query, limit=5)

        if not papers:
            return PaperInfo(title=title, authors=authors or [], year=year or "",
                             exists=False, source="not_found")

        for paper in papers:
            if self._titles_match(title, paper.get("title", "")):
                return PaperInfo(
                    title=paper.get("title", title),
                    authors=paper.get("authors", authors or []),
                    year=str(paper.get("year", year or "")),
                    venue=paper.get("venue", ""),
                    abstract=paper.get("abstract", ""),
                    citation_count=paper.get("citation_count", 0),
                    arxiv_id=paper.get("arxiv_id", ""),
                    doi=paper.get("doi", ""),
                    source=paper.get("source", ""),
                    exists=True
                )

        return PaperInfo(title=title, authors=authors or [], year=year or "",
                         exists=False, source="title_mismatch")

    def verify_paper_exists_sync(
        self, title: str, authors: List[str] = None, year: str = None
    ) -> PaperInfo:
        """同步版本"""
        return asyncio.run(self.verify_paper_exists(title, authors, year))

    def search_sync(self, query: str, limit: int = 5) -> Optional[List[Dict]]:
        """同步版本：搜索文献"""
        return asyncio.run(self.search(query, limit))
