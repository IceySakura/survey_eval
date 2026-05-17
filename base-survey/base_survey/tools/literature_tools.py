"""文献搜索工具 - 仅 Semantic Scholar

base-survey 版本：只使用 Semantic Scholar API，无 Google Scholar。
"""

import os
import asyncio
import time
from typing import List, Callable
import aiohttp

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1"
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")

S2_RATE_LIMIT_INTERVAL = 3.5
S2_MAX_RETRIES = 3
S2_RETRY_DELAY = 5.0

_last_s2_request_time = 0.0


def create_literature_tools() -> List[Callable]:
    """创建文献搜索工具函数列表（仅 Semantic Scholar）"""

    s2_headers = {}
    if SEMANTIC_SCHOLAR_API_KEY:
        s2_headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY

    def _normalize_paper_id(paper_id: str) -> str:
        """规范化论文 ID"""
        paper_id = paper_id.strip()
        if paper_id.lower().startswith("arxiv:"):
            return paper_id
        elif paper_id.replace(".", "").replace("v", "").isdigit() or (
            len(paper_id.split(".")) == 2 and paper_id.split(".")[0].isdigit()
        ):
            return f"arXiv:{paper_id}"
        elif paper_id.startswith("10."):
            return f"DOI:{paper_id}"
        return paper_id

    async def _s2_rate_limited_request(
        session: aiohttp.ClientSession, url: str, params: dict
    ) -> aiohttp.ClientResponse:
        """Semantic Scholar 带速率限制和重试的请求"""
        global _last_s2_request_time

        for attempt in range(S2_MAX_RETRIES):
            now = time.time()
            elapsed = now - _last_s2_request_time
            if elapsed < S2_RATE_LIMIT_INTERVAL:
                wait_time = S2_RATE_LIMIT_INTERVAL - elapsed
                await asyncio.sleep(wait_time)

            _last_s2_request_time = time.time()
            response = await session.get(url, params=params, headers=s2_headers)

            if response.status == 429:
                retry_after = S2_RETRY_DELAY * (attempt + 1)
                logger.warning(
                    f"Semantic Scholar 速率限制，{retry_after}秒后重试 "
                    f"({attempt + 1}/{S2_MAX_RETRIES})"
                )
                await asyncio.sleep(retry_after)
                continue

            return response

        return response

    async def _search_semantic_scholar(
        query: str, limit: int, year_range: str, fields_of_study: str
    ) -> List[dict]:
        """使用 Semantic Scholar 搜索"""
        params = {
            "query": query,
            "limit": limit,
            "fields": "paperId,title,authors,year,abstract,citationCount,url,externalIds,venue,publicationDate",
        }
        if year_range:
            params["year"] = year_range
        if fields_of_study:
            params["fieldsOfStudy"] = fields_of_study

        url = f"{SEMANTIC_SCHOLAR_API_URL}/paper/search"

        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await _s2_rate_limited_request(session, url, params)
            if response.status != 200:
                error_text = await response.text()
                logger.warning(
                    f"Semantic Scholar 搜索失败 ({response.status}): {error_text[:200]}"
                )
                return []

            data = await response.json()

        papers = data.get("data", [])
        result = []
        for paper in papers:
            authors = [a.get("name", "") for a in paper.get("authors", [])]
            external_ids = paper.get("externalIds", {})
            result.append({
                "paperId": paper.get("paperId", ""),
                "title": paper.get("title", ""),
                "authors": authors,
                "year": paper.get("year", ""),
                "venue": paper.get("venue", ""),
                "abstract": paper.get("abstract", ""),
                "citationCount": paper.get("citationCount", 0),
                "url": paper.get("url", ""),
                "arxiv_id": external_ids.get("ArXiv", ""),
                "doi": external_ids.get("DOI", ""),
            })

        return result

    async def literature_search(
        query: str,
        limit: int = 10,
        year_range: str = "",
        fields_of_study: str = "",
    ) -> str:
        """搜索学术文献（Semantic Scholar）

        Args:
            query: 搜索关键词
            limit: 返回结果数量，默认 10，最大 100
            year_range: 年份范围，如 "2020-2024" 或 "2023-"
            fields_of_study: 研究领域，如 "Computer Science"

        Returns:
            搜索结果
        """
        if not query:
            raise ValueError("搜索查询不能为空")

        limit = min(max(1, limit), 100)
        papers = []

        for attempt in range(S2_MAX_RETRIES):
            logger.info(
                f"Semantic Scholar 搜索 (第 {attempt + 1}/{S2_MAX_RETRIES} 次)..."
            )
            try:
                papers = await _search_semantic_scholar(
                    query, limit, year_range, fields_of_study
                )
                if papers:
                    break
            except Exception as e:
                logger.warning(f"Semantic Scholar 搜索失败 (第 {attempt + 1} 次): {e}")

            if attempt < S2_MAX_RETRIES - 1:
                await asyncio.sleep(S2_RETRY_DELAY * (attempt + 1))
        else:
            return f"未找到与 '{query}' 相关的论文。"

        result_lines = [
            f"## 搜索结果: '{query}' (Semantic Scholar，显示 {len(papers)} 条)\n"
        ]

        for i, paper in enumerate(papers, 1):
            title = paper.get("title", "无标题")
            authors = paper.get("authors", [])
            author_names = ", ".join(authors[:5]) if authors else "未知"
            if len(authors) > 5:
                author_names += " et al."

            year = paper.get("year", "N/A")
            citations = paper.get("citationCount", 0)
            abstract = paper.get("abstract", "")
            venue = paper.get("venue", "")
            arxiv_id = paper.get("arxiv_id", "")
            doi = paper.get("doi", "")
            paper_id = paper.get("paperId", "")

            result_lines.append(f"### {i}. {title}")
            result_lines.append(f"- **作者**: {author_names}")
            result_lines.append(f"- **年份**: {year}")
            if venue:
                result_lines.append(f"- **发表于**: {venue}")
            result_lines.append(f"- **引用数**: {citations}")
            if arxiv_id:
                result_lines.append(f"- **arXiv ID**: {arxiv_id}")
            if doi:
                result_lines.append(f"- **DOI**: {doi}")
            if paper_id:
                result_lines.append(f"- **Semantic Scholar ID**: {paper_id}")
            if abstract:
                if len(abstract) > 300:
                    abstract = abstract[:300] + "..."
                result_lines.append(f"- **摘要**: {abstract}")
            result_lines.append("")

        return "\n".join(result_lines)

    async def literature_get_citations(paper_id: str, limit: int = 10) -> str:
        """获取引用该论文的论文列表"""
        if not paper_id:
            raise ValueError("论文 ID 不能为空")

        paper_id = _normalize_paper_id(paper_id)
        limit = min(max(1, limit), 100)

        url = f"{SEMANTIC_SCHOLAR_API_URL}/paper/{paper_id}/citations"
        params = {
            "limit": limit,
            "fields": "paperId,title,authors,year,citationCount",
        }

        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await _s2_rate_limited_request(session, url, params)
            if response.status == 404:
                return f"未找到论文: {paper_id}"
            if response.status != 200:
                error_text = await response.text()
                raise Exception(
                    f"API 请求失败 (状态码 {response.status}): {error_text}"
                )

            data = await response.json()

        citations = data.get("data", [])
        if not citations:
            return f"论文 {paper_id} 暂无引用记录。"

        result_lines = [f"## 引用 {paper_id} 的论文 (显示 {len(citations)} 条)\n"]
        for i, item in enumerate(citations, 1):
            citing_paper = item.get("citingPaper", {})
            title = citing_paper.get("title", "无标题")
            authors = citing_paper.get("authors", [])
            author_names = ", ".join(
                [a.get("name", "") for a in authors[:3]]
            )
            if len(authors) > 3:
                author_names += " et al."
            year = citing_paper.get("year", "N/A")
            cit_count = citing_paper.get("citationCount", 0)

            result_lines.append(f"{i}. **{title}** ({year})")
            result_lines.append(f"   - 作者: {author_names}")
            result_lines.append(f"   - 引用数: {cit_count}")
            result_lines.append("")

        return "\n".join(result_lines)

    async def literature_get_references(paper_id: str, limit: int = 10) -> str:
        """获取论文的参考文献列表"""
        if not paper_id:
            raise ValueError("论文 ID 不能为空")

        paper_id = _normalize_paper_id(paper_id)
        limit = min(max(1, limit), 100)

        url = f"{SEMANTIC_SCHOLAR_API_URL}/paper/{paper_id}/references"
        params = {
            "limit": limit,
            "fields": "paperId,title,authors,year,citationCount",
        }

        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await _s2_rate_limited_request(session, url, params)
            if response.status == 404:
                return f"未找到论文: {paper_id}"
            if response.status != 200:
                error_text = await response.text()
                raise Exception(
                    f"API 请求失败 (状态码 {response.status}): {error_text}"
                )

            data = await response.json()

        references = data.get("data", [])
        if not references:
            return f"论文 {paper_id} 暂无参考文献记录。"

        result_lines = [f"## {paper_id} 的参考文献 (显示 {len(references)} 条)\n"]
        for i, item in enumerate(references, 1):
            cited_paper = item.get("citedPaper", {})
            title = cited_paper.get("title", "无标题")
            authors = cited_paper.get("authors", [])
            author_names = ", ".join(
                [a.get("name", "") for a in authors[:3]]
            )
            if len(authors) > 3:
                author_names += " et al."
            year = cited_paper.get("year", "N/A")
            cit_count = cited_paper.get("citationCount", 0)

            result_lines.append(f"{i}. **{title}** ({year})")
            result_lines.append(f"   - 作者: {author_names}")
            result_lines.append(f"   - 引用数: {cit_count}")
            result_lines.append("")

        return "\n".join(result_lines)

    return [
        literature_search,
        literature_get_citations,
        literature_get_references,
    ]
