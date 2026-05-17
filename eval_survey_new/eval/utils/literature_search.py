"""文献搜索工具 - 基于 AutoSurvey 自建论文库

替换原 Semantic Scholar 搜索，使用 agentscope-survey/AutoSurvey 的
FAISS 向量索引 + TinyDB 元数据库进行论文检索。

接口与原 literature_search.py 完全兼容：
  search_sync(query, limit) -> List[Dict]
  返回格式: {title, authors, year, venue, abstract, arxiv_id, doi, citation_count, source}
"""

import json
import hashlib
import logging
import re
import asyncio
import numpy as np
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# AutoSurvey DB 默认路径（相对于 paper_gen/）
_PAPER_GEN_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_DEFAULT_DB_PATH = _PAPER_GEN_ROOT / "agentscope-survey" / "AutoSurvey" / "database"
_DEFAULT_EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1"

# 延迟加载的全局单例（避免重复加载 FAISS + embedding model）
_DB_INSTANCE = None


def _get_db_instance(db_path: Path = None, embedding_model: str = None):
    """延迟加载 AutoSurvey DB 单例"""
    global _DB_INSTANCE
    if _DB_INSTANCE is not None:
        return _DB_INSTANCE

    db_path = db_path or _DEFAULT_DB_PATH
    embedding_model = embedding_model or _DEFAULT_EMBEDDING_MODEL

    logger.info(f"[AutoSurveyDB] 正在加载论文库: {db_path}")

    import faiss
    from tinydb import TinyDB, Query
    from sentence_transformers import SentenceTransformer

    # TinyDB
    db = TinyDB(str(db_path / "arxiv_paper_db.json"))
    table = db.table("cs_paper_info")
    logger.info(f"[AutoSurveyDB] TinyDB 加载完成: {len(table)} 篇论文")

    # FAISS abstract index
    abs_index = faiss.read_index(str(db_path / "faiss_paper_abs_embeddings.bin"))
    logger.info(f"[AutoSurveyDB] FAISS abstract 索引加载完成: {abs_index.ntotal} 向量")

    # ID mapping
    with open(db_path / "arxivid_to_index_abs.json", "r") as f:
        id_to_index = json.loads(f.read())
    id_to_index = {aid: int(idx) for aid, idx in id_to_index.items()}
    index_to_id = {idx: aid for aid, idx in id_to_index.items()}

    # Embedding model
    model = SentenceTransformer(embedding_model, trust_remote_code=True)
    logger.info(f"[AutoSurveyDB] Embedding 模型加载完成: {embedding_model}")

    _DB_INSTANCE = {
        "db": db,
        "table": table,
        "abs_index": abs_index,
        "id_to_index": id_to_index,
        "index_to_id": index_to_id,
        "embedding_model": model,
        "query_cls": Query,
    }
    return _DB_INSTANCE


def _embed_query(model, text: str) -> np.ndarray:
    """编码查询文本"""
    prefixed = "search_query: " + text
    embedding = model.encode([prefixed])[0]
    return embedding.astype("float32")


def _paper_to_result(paper: dict) -> dict:
    """将 AutoSurvey 论文记录转换为标准搜索结果格式"""
    arxiv_id = paper.get("id", "")
    # 去掉版本号后缀 (e.g., "2401.12345v1" -> "2401.12345")
    clean_id = re.sub(r"v\d+$", "", arxiv_id)

    authors = paper.get("authors", [])
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(",")]

    venue = ""
    pub_info = paper.get("publication_venue_info", {})
    if isinstance(pub_info, dict):
        venue = pub_info.get("name", "")
    if not venue:
        venue = paper.get("best_citation_venue", "")

    return {
        "title": paper.get("title", ""),
        "authors": authors,
        "year": str(paper.get("date", ""))[:4],
        "venue": venue,
        "abstract": paper.get("abs", ""),
        "arxiv_id": clean_id,
        "doi": paper.get("doi", ""),
        "citation_count": 0,
        "source": "autosurvey_db",
    }


@dataclass
class PaperInfo:
    """论文信息（兼容原接口）"""
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
    """基于 AutoSurvey 论文库的文献搜索器

    使用 FAISS 向量索引进行语义检索，替代 Semantic Scholar API。
    对于 agentscope-survey 生成的引用（来源于该论文库），命中率极高。
    """

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        db_path: Optional[Path] = None,
        embedding_model: Optional[str] = None,
    ):
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / "cache" / "search"
        self._cache_dir = cache_dir
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._db_path = db_path
        self._embedding_model = embedding_model

    def _get_db(self):
        return _get_db_instance(self._db_path, self._embedding_model)

    # ----------------------------------------------------------- cache

    def _cache_key(self, query: str) -> str:
        return hashlib.md5(query.lower().strip().encode()).hexdigest()

    def _load_cache(self, query: str) -> Optional[List[Dict]]:
        path = self._cache_dir / f"{self._cache_key(query)}.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                logger.debug(f"  [缓存命中] {query[:40]}")
                return data
            except Exception:
                pass
        return None

    def _save_cache(self, query: str, results: List[Dict]):
        path = self._cache_dir / f"{self._cache_key(query)}.json"
        try:
            path.write_text(
                json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception as e:
            logger.warning(f"缓存写入失败: {e}")

    # ----------------------------------------------------------- title match

    def _titles_match(self, title1: str, title2: str, threshold: float = 0.7) -> bool:
        def normalize(s):
            return re.sub(r"[^\w\s]", "", s.lower()).strip()
        t1, t2 = normalize(title1), normalize(title2)
        if t1 == t2:
            return True
        words1, words2 = set(t1.split()), set(t2.split())
        if not words1 or not words2:
            return False
        similarity = len(words1 & words2) / max(len(words1), len(words2))
        return similarity > threshold

    # ----------------------------------------------------------- search

    def _search_autosurvey_db(self, query: str, limit: int = 10) -> List[Dict]:
        """在 AutoSurvey 论文库中搜索"""
        db = self._get_db()
        embedding = _embed_query(db["embedding_model"], query)
        query_vector = np.array([embedding]).astype("float32")

        # 检索更多候选以提高召回
        candidate_num = min(limit * 3, db["abs_index"].ntotal)
        distances, indices = db["abs_index"].search(query_vector, candidate_num)

        candidate_ids = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx in db["index_to_id"]:
                candidate_ids.append(db["index_to_id"][idx])

        if not candidate_ids:
            return []

        # 从 TinyDB 获取论文元数据
        Q = db["query_cls"]()
        papers = db["table"].search(Q.id.one_of(candidate_ids))

        # 按 FAISS 距离排序（candidate_ids 已按距离排序）
        paper_map = {p["id"]: p for p in papers}
        results = []
        for aid in candidate_ids[:limit]:
            if aid in paper_map:
                results.append(_paper_to_result(paper_map[aid]))

        return results

    # ----------------------------------------------------------- public API

    async def search(self, query: str, limit: int = 5) -> Optional[List[Dict]]:
        """搜索文献（兼容异步接口）"""
        cached = self._load_cache(query)
        if cached is not None:
            return cached

        results = self._search_autosurvey_db(query, limit)
        if results:
            logger.info(f"[AutoSurveyDB] 检索成功: {len(results)} 篇 (query: {query[:50]})")
        else:
            logger.info(f"[AutoSurveyDB] 无结果: {query[:50]}")

        self._save_cache(query, results or [])
        return results if results else None

    def search_sync(self, query: str, limit: int = 5) -> Optional[List[Dict]]:
        """同步版本：搜索文献"""
        cached = self._load_cache(query)
        if cached is not None:
            return cached

        results = self._search_autosurvey_db(query, limit)
        if results:
            logger.info(f"[AutoSurveyDB] 检索成功: {len(results)} 篇 (query: {query[:50]})")
        else:
            logger.info(f"[AutoSurveyDB] 无结果: {query[:50]}")

        self._save_cache(query, results or [])
        return results if results else None

    async def verify_paper_exists(
        self, title: str, authors: List[str] = None, year: str = None
    ) -> PaperInfo:
        """验证论文是否存在"""
        query = f"{authors[0]} {title}" if authors else title
        papers = await self.search(query, limit=5)

        if not papers:
            return PaperInfo(
                title=title, authors=authors or [], year=year or "",
                exists=False, source="not_found",
            )

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
                    exists=True,
                )

        return PaperInfo(
            title=title, authors=authors or [], year=year or "",
            exists=False, source="title_mismatch",
        )

    def verify_paper_exists_sync(
        self, title: str, authors: List[str] = None, year: str = None
    ) -> PaperInfo:
        """同步版本"""
        return asyncio.run(self.verify_paper_exists(title, authors, year))
