"""维度1: 文献内容准确性评测

评估 related_works.tex 中对每篇引用的描述是否与原文一致。
检测幻觉类型：内容描述与实际不符、夸大贡献等。

- 有 arXiv ID（bib 自带或 S2 消歧得到）→ 下载 PDF，用全文 + LLM 按 0–3 档打分。
- 无 arXiv ID → Semantic Scholar 多候选检索 + LLM 消歧：无匹配则 0；有匹配且无 arXiv 则固定 2；有 arXiv 则转入全文流程。

客观评测，输出 1-10 分。支持随机抽样：从 tex 实际引用的**全部**条目中统一抽取若干条（不区分是否有 arXiv）；维度 2 与维度 1 同批引用对齐时需由评测器传入相同 key 顺序。

accuracy_level（0-3）含义（有全文时由 LLM 判定）：
  3 = 描述基本无误
  2 = 与原论文有轻微偏差或错误，但不影响读者对上下文的理解
  1 = 方法/贡献有实质性错误
  0 = 内容完全捏造，或与论文完全无关
"""

import random
import logging
import asyncio
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, replace

from ..utils.bib_parser import parse_bib_file, extract_citations_from_tex, BibEntry
from ..utils.llm_client import LLMClient
from ..utils.paper_fetcher import PaperFetcher
from ..utils.literature_search import LiteratureSearch

logger = logging.getLogger(__name__)

# 无 arXiv：S2 多候选 + LLM 判断哪一篇对应 bib（并抽取 arXiv）
S2_DISAMBIGUATION_PROMPT = """你是学术文献匹配助手。下面是一条 BibTeX 所描述的论文，以及 Semantic Scholar 返回的若干候选（按序号 0 起）。

## Bib 条目（待匹配）
- 标题: {paper_title}
- 作者: {paper_authors}
- 年份: {paper_year}

## S2 候选列表（序号从 0 开始）
{candidates_block}

## 任务
1. 判断候选中**是否有一条**与 Bib 条目指向**同一篇论文**（允许标题轻微差异、预印本与正式版等）。
2. 若**没有**合理匹配：match_index 必须为 null，并在 reason 中简要说明。
3. 若**有**匹配：给出 match_index（0 到 N-1），并在 arxiv_id 字段填写该候选自带的 ArXiv ID（纯 id，如 2401.12345；若无则填 null）。
4. 不要猜测不存在的 arXiv ID。

请以 JSON 输出：
{{
  "match_index": null 或整数,
  "arxiv_id": null 或字符串,
  "reason": "简短说明"
}}"""


# 有全文时使用（arXiv 论文）
ACCURACY_PROMPT_FULLTEXT = """你是一位学术诚信审查员。请判断 Related Works 中对论文的描述是否准确。

## 重要说明：多文献联合引用
若描述中该引用与多篇文献同时出现（如 \\cite{{a, b, c}}），则描述可能是对整组文献的综合概括。此时只需判断：**该论文是否支持该描述中的某个合理部分**？若描述中的某部分可由同组其他文献支持，则不应因该论文未涉及该部分而判定为错误。例如，若描述称「多种架构包括 LLM 上优于 Adam」，而当前论文只做了 grokking 实验，但同组另一篇论文做了 LLM 实验，则当前论文不应因此被判为严重错误。

## 原始论文信息
- 标题: {paper_title}
- 作者: {paper_authors}
- 年份: {paper_year}
- 论文内容摘录（前 3000 字符）:
{paper_content}

## Related Works 中的描述
{description}

## 任务
请检查描述是否与论文实际内容一致，重点关注：
1. 论文的主要方法/贡献是否被准确描述
2. 是否有夸大、歪曲或明显错误的描述
3. 关键数据/结论是否有错
4. 若为多文献联合引用，仅判断该论文是否支持描述的某合理部分

请以 JSON 格式输出：
{{
    "accuracy_level": 0/1/2/3,
    "hallucination_type": null/"misrepresentation"/"exaggeration"/"wrong_metadata",
    "details": "具体问题说明（如准确则填 null）"
}}

accuracy_level（必须严格区分，只输出 0–3）：
  3 = 描述基本无误：与论文内容一致，无明显事实性错误
  2 = 与原论文有轻微偏差或错误，但不影响读者对上下文的理解
  1 = 方法或贡献有实质性错误：会误导读者对论文工作的理解
  0 = 内容完全捏造，或与该论文完全无关"""


S2_MATCH_CANDIDATE_LIMIT = 10


def _normalize_accuracy_level(level: int) -> int:
    """统一为 0–3；兼容历史输出中的 4。"""
    if level >= 4:
        return 3
    return max(0, min(3, level))


def _strip_arxiv_id(raw: Optional[str]) -> str:
    if not raw:
        return ""
    s = str(raw).strip()
    s = re.sub(r"^arxiv:\s*", "", s, flags=re.I)
    s = re.sub(r"v\d+$", "", s, flags=re.I)
    m = re.search(r"(\d{4}\.\d{4,5})", s)
    return m.group(1) if m else s


def _format_s2_candidates_block(papers: List[Dict]) -> str:
    lines = []
    for i, p in enumerate(papers):
        ext = (p.get("arxiv_id") or "").strip() or "（无）"
        auth = ", ".join(p.get("authors") or [])
        ab = (p.get("abstract") or "")[:400]
        lines.append(
            f"[{i}] 标题: {p.get('title', '')}\n"
            f"    作者: {auth}\n"
            f"    年份: {p.get('year', '')}\n"
            f"    ArXiv: {ext}\n"
            f"    摘要摘录: {ab}..."
        )
    return "\n\n".join(lines)


@dataclass
class CitationAccuracyResult:
    """单篇引用的准确性结果"""
    citation_key: str
    title: str
    arxiv_id: str
    verified: bool              # 是否成功验证
    accuracy_level: int         # 0-3，见模块文档
    hallucination_type: Optional[str]
    details: str
    verification_mode: str      # "fulltext" | "semantic_scholar" | "failed"

    # 兼容旧字段
    @property
    def accurate(self) -> bool:
        return self.accuracy_level >= 3

    @property
    def severity(self) -> int:
        """兼容旧字段：将 accuracy_level 反转为 severity(0-2)"""
        if self.accuracy_level >= 3:
            return 0
        if self.accuracy_level == 2:
            return 1
        return 2

    # accuracy_level（0-3）→ 归一化分数，再映射到总分 1–10
    _LEVEL_SCORE = {3: 1.0, 2: 0.65, 1: 0.15, 0: 0.0}

    @property
    def score(self) -> float:
        """计算分数 (0-1)"""
        if not self.verified:
            return 0.35     # 验证失败给偏低分，无法验证的引用可信度有限
        return self._LEVEL_SCORE.get(self.accuracy_level, 0.5)


@dataclass
class ContentAccuracyEvalResult:
    """内容准确性评测总结果"""
    article_name: str
    total_citations: int
    verified_citations: int
    citation_results: List[CitationAccuracyResult] = field(default_factory=list)

    @property
    def score(self) -> float:
        """计算总分 (1-10)，只计入成功验证的条目"""
        verified = [r for r in self.citation_results if r.verified]
        if not verified:
            return 5.0
        avg = sum(r.score for r in verified) / len(verified)
        return round(avg * 9 + 1, 2)

    @property
    def hallucination_count(self) -> int:
        return sum(1 for r in self.citation_results if r.hallucination_type is not None)

    @property
    def fulltext_count(self) -> int:
        return sum(1 for r in self.citation_results if r.verification_mode == "fulltext")

    @property
    def semantic_scholar_count(self) -> int:
        return sum(1 for r in self.citation_results if r.verification_mode == "semantic_scholar")

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.citation_results if r.verification_mode == "failed")

    def get_hallucinations(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": r.citation_key,
                "title": r.title,
                "arxiv_id": r.arxiv_id,
                "accuracy_level": r.accuracy_level,
                "type": r.hallucination_type,
                "mode": r.verification_mode,
                "details": r.details
            }
            for r in self.citation_results
            if r.accuracy_level < 3 and r.verified
        ]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "article_name": self.article_name,
            "score": self.score,
            "total_citations": self.total_citations,
            "verified_citations": self.verified_citations,
            "fulltext_verified": self.fulltext_count,
            "semantic_scholar_verified": self.semantic_scholar_count,
            "failed_count": self.failed_count,
            "hallucination_count": self.hallucination_count,
            "hallucinations": self.get_hallucinations(),
            "details": [
                {
                    "key": r.citation_key,
                    "title": r.title,
                    "arxiv_id": r.arxiv_id,
                    "accuracy_level": r.accuracy_level,
                    "accurate": r.accurate,
                    "hallucination_type": r.hallucination_type,
                    "mode": r.verification_mode,
                    "details": r.details
                }
                for r in self.citation_results
            ]
        }


class ContentAccuracyEvaluator:
    """内容准确性评测器

    - 有 arXiv ID：拉取全文，LLM 按 0–3 档评分
    - 无 arXiv ID：S2 多候选 + LLM 消歧；无匹配→0；有 arXiv→转全文；否则固定 2
    """

    def __init__(
        self,
        llm_client: LLMClient,
        paper_fetcher: Optional[PaperFetcher] = None,
        literature_search: Optional[LiteratureSearch] = None,
        max_papers_to_verify: int = 20
    ):
        self.llm = llm_client
        self.paper_fetcher = paper_fetcher or PaperFetcher()
        self.literature_search = literature_search or LiteratureSearch()
        self.max_papers_to_verify = max_papers_to_verify

    @staticmethod
    def _is_multi_cite_context(contexts: List[str]) -> bool:
        """判断上下文是否属于多文献并引（如 \\cite{a,b,c} / \\citep{a,b}）。"""
        joined = "\n".join(contexts or [])
        return bool(
            re.search(
                r'\\cite\w*\{[^{}]*,[^{}]*\}',
                joined
            )
        )

    @staticmethod
    def _looks_hard_error(details: str) -> bool:
        """粗略识别“明显硬错误”描述，避免多文献并引保护把 L1/L0 抬高。"""
        text = (details or "").lower()
        hard_signals = [
            "完全无关",
            "论文不存在",
            "not found",
            "根本不存在",
            "实质性错误",
            "明显错误",
            "major",
            "severe",
        ]
        return any(s in text for s in hard_signals)

    def _verify_single_citation(
        self,
        entry: BibEntry,
        contexts: List[str],
        valid_non_academic: Optional[set] = None
    ) -> CitationAccuracyResult:
        """验证单篇引用的准确性（调用前已确保 entry.arxiv_id 非空）"""
        description = "\n\n".join(contexts[:3]) if contexts else "无上下文"
        valid_non_academic = valid_non_academic or set()

        full_text, http_status = self.paper_fetcher.get_paper_content(arxiv_id=entry.arxiv_id)
        if not full_text:
            if http_status == 404:
                if entry.key in valid_non_academic:
                    logger.info(f"  ✓(L3) [白名单] [{entry.key}] {entry.title[:50]} (blog/技术报告等，无法学术库验证)")
                    return CitationAccuracyResult(
                        citation_key=entry.key,
                        title=entry.title,
                        arxiv_id=entry.arxiv_id,
                        verified=True,
                        accuracy_level=3,
                        hallucination_type=None,
                        details="已知有效引用（blog/技术报告等），无法通过学术库验证",
                        verification_mode="fulltext"
                    )
                logger.info(f"  ✗✗(L0) [arXiv 404 虚假] [{entry.key}] {entry.title[:50]}")
                return CitationAccuracyResult(
                    citation_key=entry.key,
                    title=entry.title,
                    arxiv_id=entry.arxiv_id,
                    verified=True,
                    accuracy_level=0,
                    hallucination_type="not_found",
                    details="arXiv 404，论文不存在（虚假引用）",
                    verification_mode="fulltext"
                )
            logger.warning(f"  PDF 下载失败，跳过: {entry.key} (arXiv:{entry.arxiv_id})")
            return CitationAccuracyResult(
                citation_key=entry.key,
                title=entry.title,
                arxiv_id=entry.arxiv_id,
                verified=False,
                accuracy_level=3,
                hallucination_type=None,
                details="PDF 下载失败",
                verification_mode="failed"
            )

        prompt = ACCURACY_PROMPT_FULLTEXT.format(
            paper_title=entry.title,
            paper_authors=entry.author_string,
            paper_year=entry.year,
            paper_content=full_text[:3000],
            description=description[:2000]
        )
        result = self.llm.chat_json(prompt)
        if result is None:
            logger.warning(f"  LLM 评估失败: {entry.key}")
            return CitationAccuracyResult(
                citation_key=entry.key,
                title=entry.title,
                arxiv_id=entry.arxiv_id,
                verified=False,
                accuracy_level=3,
                hallucination_type=None,
                details="LLM 评估失败",
                verification_mode="failed"
            )

        # 优先读 accuracy_level；兼容旧格式（accurate + severity）
        if "accuracy_level" in result:
            accuracy_level = _normalize_accuracy_level(int(result.get("accuracy_level", 3)))
        else:
            accurate = result.get("accurate", True)
            severity = int(result.get("severity", 0))
            if accurate:
                raw = {0: 3, 1: 3, 2: 2}.get(severity, 3)
            else:
                raw = {0: 2, 1: 1, 2: 0}.get(severity, 1)
            accuracy_level = _normalize_accuracy_level(raw)

        h_type = result.get("hallucination_type")
        details = result.get("details") or ""

        # 多文献并引保护：除非明显硬错误，否则不把 L2/L1 轻易打成更差档
        if (
            accuracy_level == 2
            and self._is_multi_cite_context(contexts)
            and not self._looks_hard_error(details)
        ):
            accuracy_level = 3
            if not h_type:
                h_type = "misrepresentation"
            details = f"[multi-cite保护] {details}"
        if (
            accuracy_level == 1
            and self._is_multi_cite_context(contexts)
            and not self._looks_hard_error(details)
        ):
            accuracy_level = 2
            if not h_type:
                h_type = "misrepresentation"
            details = f"[multi-cite保护] {details}"

        level_labels = {3: "✓ 基本无误", 2: "~ 轻微偏差", 1: "✗ 实质性错误", 0: "✗✗ 捏造/无关"}
        logger.info(f"  {level_labels.get(accuracy_level, '?')}(L{accuracy_level})  [{entry.key}] {entry.title[:50]}")
        if accuracy_level < 3:
            logger.info(f"    └─ {details[:120]}")

        return CitationAccuracyResult(
            citation_key=entry.key,
            title=entry.title,
            arxiv_id=entry.arxiv_id,
            verified=True,
            accuracy_level=accuracy_level,
            hallucination_type=h_type,
            details=details,
            verification_mode="fulltext"
        )

    def _s2_query_for_entry(self, entry: BibEntry, title_override: Optional[str] = None) -> str:
        t = (title_override or entry.title or "").strip()
        if entry.authors:
            return f"{entry.authors[0]} {t}".strip()
        return t

    def _verify_single_citation_s2_meta(
        self,
        entry: BibEntry,
        contexts: List[str],
        valid_non_academic: Optional[set] = None
    ) -> CitationAccuracyResult:
        """无 arXiv：S2 多候选检索 + LLM 消歧；无匹配→0；有 arXiv→全文；否则固定 2。"""
        valid_non_academic = valid_non_academic or set()
        level_labels = {3: "✓ 基本无误", 2: "~ 固定轻微档(S2)", 1: "✗ 实质性错误", 0: "✗✗ 捏造/无关"}

        def _fetch_candidates() -> List[Dict]:
            q = self._s2_query_for_entry(entry)
            papers = self.literature_search.search_sync(q, limit=S2_MATCH_CANDIDATE_LIMIT) or []
            if papers:
                return papers
            short_title = re.split(r'[:\-–—]', entry.title, maxsplit=1)[0].strip()
            if (
                short_title
                and len(short_title) >= 12
                and short_title != entry.title.strip()
            ):
                papers = self.literature_search.search_sync(
                    self._s2_query_for_entry(entry, title_override=short_title),
                    limit=S2_MATCH_CANDIDATE_LIMIT,
                ) or []
            return papers

        papers = _fetch_candidates()

        if not papers:
            if entry.key in valid_non_academic:
                logger.info(f"  ✓(L3) [白名单] [S2] [{entry.key}] {entry.title[:50]} (无候选，非学术白名单)")
                return CitationAccuracyResult(
                    citation_key=entry.key,
                    title=entry.title,
                    arxiv_id="",
                    verified=True,
                    accuracy_level=3,
                    hallucination_type=None,
                    details="已知有效引用（blog/技术报告等），S2 无候选",
                    verification_mode="semantic_scholar",
                )
            logger.info(f"  ✗✗(L0) [S2 无候选] [{entry.key}] {entry.title[:50]}")
            return CitationAccuracyResult(
                citation_key=entry.key,
                title=entry.title,
                arxiv_id="",
                verified=True,
                accuracy_level=0,
                hallucination_type="not_found",
                details="Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）",
                verification_mode="semantic_scholar",
            )

        candidates_block = _format_s2_candidates_block(papers)
        disamb_prompt = S2_DISAMBIGUATION_PROMPT.format(
            paper_title=entry.title,
            paper_authors=entry.author_string,
            paper_year=entry.year,
            candidates_block=candidates_block,
        )
        result = self.llm.chat_json(disamb_prompt)
        if result is None:
            logger.warning(f"  S2 消歧 LLM 失败: {entry.key}")
            return CitationAccuracyResult(
                citation_key=entry.key,
                title=entry.title,
                arxiv_id="",
                verified=False,
                accuracy_level=3,
                hallucination_type=None,
                details="S2 多候选消歧：LLM 调用失败",
                verification_mode="failed",
            )

        raw_idx = result.get("match_index")
        reason = (result.get("reason") or "").strip() or "（无说明）"
        idx: Optional[int] = None
        if raw_idx is not None and raw_idx != "":
            try:
                idx = int(raw_idx)
            except (TypeError, ValueError):
                idx = None

        if idx is None or idx < 0 or idx >= len(papers):
            if entry.key in valid_non_academic:
                logger.info(f"  ✓(L3) [白名单] [S2消歧无匹配] [{entry.key}] {entry.title[:50]}")
                return CitationAccuracyResult(
                    citation_key=entry.key,
                    title=entry.title,
                    arxiv_id="",
                    verified=True,
                    accuracy_level=3,
                    hallucination_type=None,
                    details=f"白名单引用；S2 消歧无匹配。LLM: {reason}",
                    verification_mode="semantic_scholar",
                )
            logger.info(f"  ✗✗(L0) [S2消歧无匹配] [{entry.key}] {entry.title[:50]}")
            return CitationAccuracyResult(
                citation_key=entry.key,
                title=entry.title,
                arxiv_id="",
                verified=True,
                accuracy_level=0,
                hallucination_type="fabricated",
                details=f"候选共 {len(papers)} 条，LLM 判定无与 Bib 对应的论文。理由: {reason}",
                verification_mode="semantic_scholar",
            )

        matched = papers[idx]
        aid = _strip_arxiv_id(result.get("arxiv_id"))
        if not aid:
            aid = _strip_arxiv_id(matched.get("arxiv_id"))

        if aid:
            logger.info(
                f"  [S2→全文] [{entry.key}] 消歧命中 #{idx}，arXiv={aid} | {reason[:80]}"
            )
            new_entry = replace(entry, arxiv_id=aid)
            return self._verify_single_citation(new_entry, contexts, valid_non_academic)

        mt = matched.get("title", "")
        details = (
            f"S2 消歧命中候选 #{idx}（无 arXiv，未做全文核对），固定 accuracy_level=2。"
            f" 匹配题: {mt}。LLM: {reason}"
        )
        logger.info(f"  {level_labels[2]}(L2) [S2] [{entry.key}] {entry.title[:50]}")
        logger.info(f"    └─ {details[:160]}")
        return CitationAccuracyResult(
            citation_key=entry.key,
            title=entry.title,
            arxiv_id="",
            verified=True,
            accuracy_level=2,
            hallucination_type=None,
            details=details,
            verification_mode="semantic_scholar",
        )

    def evaluate(
        self,
        tex_path: Path,
        bib_path: Path,
        article_name: str = "",
        sample_size: Optional[int] = None,
        seed: int = 42,
        valid_non_academic_citations: Optional[set] = None
    ) -> ContentAccuracyEvalResult:
        """评估内容准确性（见模块顶 accuracy_level 与流程说明）。

        sample_size：从全部 tex 实际引用中随机抽若干条做内容准确性验证；
        为 None 时全量。抽样在「有/无 arXiv」合并池上进行，不再只对 arXiv 子集抽样。
        """
        entries = parse_bib_file(bib_path)
        citations_context = extract_citations_from_tex(tex_path)

        entry_map = {e.key: e for e in entries}

        all_cited = [
            (entry_map[key], contexts)
            for key, contexts in citations_context.items()
            if key in entry_map
        ]
        total_cited = len(all_cited)
        n_arxiv = sum(1 for e, _ in all_cited if e.arxiv_id)
        logger.info(
            f"  tex 引用 {total_cited} 条，有 arXiv {n_arxiv} 条，无 arXiv {total_cited - n_arxiv} 条"
        )

        if sample_size is not None and total_cited > sample_size:
            random.seed(seed)
            to_verify = random.sample(all_cited, sample_size)
            logger.info(
                f"  统一抽样: 从 {total_cited} 条中抽取 {sample_size} 条做维度1 内容准确性"
            )
        else:
            to_verify = all_cited

        n_full = sum(1 for e, _ in to_verify if e.arxiv_id)
        logger.info(
            f"开始评估内容准确性: {article_name}, "
            f"本批 {len(to_verify)} 条（全文 {n_full} | S2 {len(to_verify) - n_full}）"
        )

        results = []
        for i, (entry, contexts) in enumerate(to_verify):
            mode_hint = "arXiv" if entry.arxiv_id else "S2"
            logger.info(f"  [{i+1}/{len(to_verify)}] [{mode_hint}] {entry.key} ({entry.year})")
            valid_non_academic = valid_non_academic_citations or set()
            try:
                if entry.arxiv_id:
                    result = self._verify_single_citation(entry, contexts, valid_non_academic)
                else:
                    result = self._verify_single_citation_s2_meta(entry, contexts, valid_non_academic)
                results.append(result)
            except Exception as e:
                logger.warning(f"  验证失败 {entry.key}: {e}")
                results.append(CitationAccuracyResult(
                    citation_key=entry.key,
                    title=entry.title,
                    arxiv_id=entry.arxiv_id or "",
                    verified=False,
                    accuracy_level=3,
                    hallucination_type=None,
                    details=f"验证异常: {e}",
                    verification_mode="failed"
                ))

        eval_result = ContentAccuracyEvalResult(
            article_name=article_name,
            total_citations=total_cited,
            verified_citations=len(results),
            citation_results=results
        )

        logger.info(
            f"  ──────────────────────────────────────────────────\n"
            f"  小结 [{article_name}]  总分 {eval_result.score}/10\n"
            f"  全文验证 {eval_result.fulltext_count} 篇 | "
            f"S2+LLM 验证 {eval_result.semantic_scholar_count} 篇 | "
            f"失败跳过 {eval_result.failed_count} 篇 | "
            f"幻觉 {eval_result.hallucination_count} 篇"
        )
        return eval_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    eval_dir = Path(__file__).parent.parent
    sources_dir = eval_dir.parent / "sources"

    llm = LLMClient()
    evaluator = ContentAccuracyEvaluator(llm, max_papers_to_verify=5)

    result = evaluator.evaluate(
        tex_path=sources_dir / "ours" / "related_works.tex",
        bib_path=sources_dir / "ours" / "references.bib",
        article_name="ours"
    )

    print(f"评测结果: {result.score}/10")
    print(f"幻觉数量: {result.hallucination_count}")
