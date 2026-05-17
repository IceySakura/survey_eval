"""维度2: 引用文献相关性评测

评分分两步：
1. Key References 覆盖检查（全量，一次 LLM 调用）：Plan 中列出的关键文献是否被引用
2. 逐篇相关性质量分：默认从引用中抽样；若传入与维度1 对齐的 key 顺序，则只评该批（0=不相关 / 1=弱相关 / 2=强相关）

最终分数 = 覆盖分（主体）+ 质量加分 + 引用丰富度(0-3) - 偏题惩罚，映射到 1-10。
"""

import random
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field

from ..utils.bib_parser import parse_bib_file, extract_citations_from_tex, BibEntry
from ..utils.llm_client import LLMClient

logger = logging.getLogger(__name__)

# 引用条数丰富度加分：线性增至上限，total_citations == CITATION_COUNT_FULL_AT 时拿满
CITATION_COUNT_BONUS_CAP = 3.0
CITATION_COUNT_FULL_AT = 40

# 偏题惩罚：不相关率超过阈值后线性增加，100% 不相关时扣满 OFF_TOPIC_PENALTY_MAX
OFF_TOPIC_IRRELEVANT_THRESHOLD = 0.2
OFF_TOPIC_PENALTY_MAX = 2.0


def _citation_count_bonus(total_citations: int) -> float:
    if CITATION_COUNT_FULL_AT <= 0:
        return 0.0
    return min(CITATION_COUNT_BONUS_CAP, (total_citations / CITATION_COUNT_FULL_AT) * CITATION_COUNT_BONUS_CAP)


def _off_topic_penalty(irrelevant_rate: float) -> float:
    excess = max(0.0, irrelevant_rate - OFF_TOPIC_IRRELEVANT_THRESHOLD)
    denom = 1.0 - OFF_TOPIC_IRRELEVANT_THRESHOLD
    if denom <= 0:
        return 0.0
    return min(OFF_TOPIC_PENALTY_MAX, excess * (OFF_TOPIC_PENALTY_MAX / denom))


# ─── Prompt 1：逐篇相关性打分（复用，用于质量加分 / 偏题惩罚）───────────────
RELEVANCE_PROMPT = """你是一位学术论文审稿人，正在评估一篇 Related Works 段落中某条引用的相关性。

## 写作任务说明（完整 Plan）
{plan}

## 待评估的引用论文
- 标题: {title}
- 作者: {authors}
- 年份: {year}
- 发表于: {venue}

## 评分标准（0-2）

请严格依据上方 Plan 的内容来判断相关性：

**2 = 强相关**，满足以下任一条件：
- 是 Plan 的 "Key References" 中明确列出的文献
- 是 Plan 各 Section 描述的核心研究方向的直接代表性工作
- 是直接激发本研究动机的背景工作（如同类方法的局限性、已有的初步尝试），Plan 中有明确提及或高度契合

**1 = 弱相关**，满足以下任一条件：
- 是 Plan 核心方向的相邻技术，与主题有交叉但并非核心
- 是研究背景的更广泛上下文，在 Related Works 中提及合理但 Plan 并未强调

**0 = 不相关**：
- 论文与 Plan 描述的所有核心方向均无明显关联
- 引用明显属于其他研究方向，难以找到与 Plan 主题的合理联系

请以 JSON 格式输出：
{{"relevance": <0-2>, "reason": "简短解释，说明为何判定为该分数"}}"""


# ─── Prompt 2：Key References 覆盖检查（一次调用，全量）───────────────────────
KEY_COVERAGE_PROMPT = """你是一位学术审稿人，请检查一篇 Related Works 的引用列表是否覆盖了写作计划中要求的关键文献。

## 写作计划（Survey Plan）
{plan}

## 该文章实际引用的所有论文（cite key → 标题）
{cited_list}

## 任务
对 Plan 中 "Key References" 一节列出的每条关键文献，判断：
- **covered**：引用列表中有该论文，或有内容高度相同的等价替代（例如同一论文的不同版本/会议版与 arXiv 版）
- **missing**：引用列表中找不到该论文或等价替代

请以 JSON 格式输出，key 为关键文献的简短描述（与 Plan 中的描述一致），value 为对象：
{{
  "<key_ref_description>": {{
    "covered": true/false,
    "matched_cite_key": "<匹配的 cite key，若未覆盖则为 null>",
    "note": "简短说明"
  }},
  ...
}}"""


# ─── 数据结构 ──────────────────────────────────────────────────────────────────

@dataclass
class CitationRelevanceResult:
    """单篇引用的相关性结果"""
    citation_key: str
    title: str
    authors: str
    year: str
    relevance_score: int  # 0-2
    reason: str

    @property
    def normalized_score(self) -> float:
        return self.relevance_score / 2.0


@dataclass
class KeyCoverageResult:
    """Key References 覆盖检查结果"""
    key_ref: str          # Plan 中的关键文献描述
    covered: bool
    matched_cite_key: Optional[str]
    note: str


@dataclass
class CitationRelevanceEvalResult:
    """引用相关性评测总结果"""
    article_name: str
    total_citations: int
    evaluated_citations: int       # 抽样评估的数量（含捏造论文）
    citation_results: List[CitationRelevanceResult] = field(default_factory=list)
    key_coverage: List[KeyCoverageResult] = field(default_factory=list)
    total_key_refs: int = 0        # Plan Key References 总数
    fabricated_count: int = 0      # 维度1 内容准确性检测出的完全捏造论文数（直接计为不相关）

    # ── 覆盖分相关 ──────────────────────────────────────────────────────────
    @property
    def covered_count(self) -> int:
        return sum(1 for r in self.key_coverage if r.covered)

    @property
    def coverage_rate(self) -> float:
        if self.total_key_refs == 0:
            return 1.0
        return self.covered_count / self.total_key_refs

    # ── 抽样质量相关 ─────────────────────────────────────────────────────────
    @property
    def highly_relevant_count(self) -> int:
        return sum(1 for r in self.citation_results if r.relevance_score == 2)

    @property
    def irrelevant_count(self) -> int:
        return sum(1 for r in self.citation_results if r.relevance_score == 0)

    @property
    def irrelevant_rate(self) -> float:
        if not self.citation_results:
            return 0.0
        return self.irrelevant_count / len(self.citation_results)

    # ── 最终分数（1-10）────────────────────────────────────────────────────
    @property
    def score(self) -> float:
        """
        计分公式：
          覆盖分  = coverage_rate * 7          （主体，0-7）
          质量加分 = highly_relevant_rate * 2  （0-2，抽样中强相关比例）
          丰富度加分 = min(3, total/40*3)      （0-3，40 条 tex 实际引用即拿满）
          偏题惩罚 = max(0, rate-0.2) / 0.8 * 2  （超过 20% 不相关才线性扣，全不相关扣满 2）
          raw = 覆盖分 + 质量加分 + 丰富度加分 - 偏题惩罚  （理论最高约 12）
          final = clamp(raw, 0, 10) → 映射到 1-10
        """
        if self.total_key_refs == 0 and not self.citation_results:
            return 5.0

        coverage_score = self.coverage_rate * 7.0

        if self.citation_results:
            hr_rate = self.highly_relevant_count / len(self.citation_results)
            quality_bonus = hr_rate * 2.0
            penalty = _off_topic_penalty(self.irrelevant_rate)
        else:
            quality_bonus = 0.0
            penalty = 0.0

        citation_count_bonus = _citation_count_bonus(self.total_citations)

        raw = coverage_score + quality_bonus + citation_count_bonus - penalty
        raw = max(0.0, min(10.0, raw))
        # 映射到 1-10（保留至少 1 分）
        return round(max(1.0, raw), 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "article_name": self.article_name,
            "score": self.score,
            "total_citations": self.total_citations,
            "evaluated_citations": self.evaluated_citations,
            "fabricated_count": self.fabricated_count,
            # 覆盖检查
            "key_refs_total": self.total_key_refs,
            "key_refs_covered": self.covered_count,
            "coverage_rate": round(self.coverage_rate, 3),
            "citation_count_bonus": round(_citation_count_bonus(self.total_citations), 3),
            "key_coverage": [
                {
                    "key_ref": r.key_ref,
                    "covered": r.covered,
                    "matched_cite_key": r.matched_cite_key,
                    "note": r.note
                }
                for r in self.key_coverage
            ],
            # 抽样质量
            "highly_relevant": self.highly_relevant_count,
            "weakly_relevant": (
                self.evaluated_citations
                - self.highly_relevant_count
                - self.irrelevant_count
            ),
            "irrelevant": self.irrelevant_count,
            "details": [
                {
                    "key": r.citation_key,
                    "title": r.title,
                    "relevance": r.relevance_score,
                    "reason": r.reason
                }
                for r in self.citation_results
            ]
        }


# ─── 评测器 ────────────────────────────────────────────────────────────────────

class CitationRelevanceEvaluator:
    """引用相关性评测器（两步：覆盖检查 + 抽样质量打分）"""

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def _evaluate_single_citation(
        self,
        entry: BibEntry,
        plan_content: str
    ) -> CitationRelevanceResult:
        """对单篇引用进行相关性打分"""
        prompt = RELEVANCE_PROMPT.format(
            plan=plan_content,
            title=entry.title,
            authors=entry.author_string,
            year=entry.year,
            venue=entry.venue or "N/A"
        )
        result = self.llm.chat_json(prompt)

        if result is None:
            logger.warning(f"  [评估失败] {entry.key} -> 默认弱相关")
            return CitationRelevanceResult(
                citation_key=entry.key,
                title=entry.title,
                authors=entry.author_string,
                year=entry.year,
                relevance_score=1,
                reason="评估失败，默认弱相关"
            )

        score = result.get("relevance", 1)
        reason = result.get("reason", "")
        score_label = {0: "✗ 不相关", 1: "~ 弱相关", 2: "✓ 强相关"}.get(score, "?")
        logger.info(f"  {score_label}  [{entry.key}] {entry.title[:55]}")
        logger.info(f"    └─ {reason[:120]}")

        return CitationRelevanceResult(
            citation_key=entry.key,
            title=entry.title,
            authors=entry.author_string,
            year=entry.year,
            relevance_score=score,
            reason=reason
        )

    def _check_key_coverage(
        self,
        entries: List[BibEntry],
        plan_content: str
    ) -> List[KeyCoverageResult]:
        """
        一次 LLM 调用，对照 Plan Key References 检查覆盖情况。
        entries 为全量已引用条目（不抽样）。
        """
        cited_list_str = "\n".join(
            f"- {e.key}: {e.title} ({e.year})"
            for e in entries
        )
        prompt = KEY_COVERAGE_PROMPT.format(
            plan=plan_content,
            cited_list=cited_list_str
        )
        result = self.llm.chat_json(prompt)

        if result is None or not isinstance(result, dict):
            logger.warning("  Key References 覆盖检查失败，跳过")
            return []

        coverage = []
        for key_ref, info in result.items():
            if not isinstance(info, dict):
                continue
            covered = bool(info.get("covered", False))
            matched = info.get("matched_cite_key") or None
            note = info.get("note", "")
            mark = "✓" if covered else "✗"
            logger.info(f"  {mark} Key Ref: {key_ref[:60]}"
                        + (f" → {matched}" if matched else ""))
            coverage.append(KeyCoverageResult(
                key_ref=key_ref,
                covered=covered,
                matched_cite_key=matched,
                note=note
            ))
        return coverage

    def evaluate(
        self,
        bib_path: Path,
        plan_path: Path,
        tex_path: Optional[Path] = None,
        article_name: str = "",
        sample_size: Optional[int] = None,
        seed: int = 42,
        fabricated_keys: Optional[set] = None,
        quality_key_order: Optional[List[str]] = None
    ) -> CitationRelevanceEvalResult:
        """
        评估引用相关性（两步）：

        步骤1 — Key References 覆盖检查（全量，1次 LLM 调用）
          对照 Plan 中的 Key References，检查每条是否被引用或有等价替代。

        步骤2 — 质量打分
          - 若提供 quality_key_order：仅对该列表中的 cite key 逐篇打 0/1/2 分（与维度1 同批引用对齐），
            此时忽略 sample_size。
          - 否则：从实际引用中按 sample_size 随机抽样（None 表示全量）；捏造 key 仍先固定 0 分且不进入 LLM。

        fabricated_keys: 由维度1 内容准确性检测出的完全捏造论文（accuracy_level==0）的 cite key 集合。
          这些论文在质量打分时直接计为不相关（score=0）；
          在步骤1 Key References 覆盖检查中也会从「实际引用列表」里剔除，避免虚假引用冒充覆盖。

        最终分数 = 覆盖分(0-7) + 质量加分(0-2) + 丰富度(0-3) - 偏题惩罚(0~2)，再截断到 1-10。
        """
        all_entries = parse_bib_file(bib_path)
        plan_content = plan_path.read_text(encoding='utf-8')
        fabricated_keys = fabricated_keys or set()

        # 过滤：只保留 tex 中实际被引用的条目
        if tex_path is not None and tex_path.exists():
            cited_keys = set(extract_citations_from_tex(tex_path).keys())
            entries = [e for e in all_entries if e.key in cited_keys]
            skipped = len(all_entries) - len(entries)
            if skipped:
                logger.info(f"  bib 共 {len(all_entries)} 条，tex 实际引用 {len(entries)} 条"
                            f"（跳过未引用的 {skipped} 条）")
        else:
            entries = all_entries

        # Key Ref 与丰富度：剔除维度1 认定的捏造引用，不当作有效「全量引用」
        entries_for_coverage = [e for e in entries if e.key not in fabricated_keys]
        if fabricated_keys:
            n_drop = len(entries) - len(entries_for_coverage)
            if n_drop > 0:
                dropped = [e.key for e in entries if e.key in fabricated_keys]
                logger.info(
                    f"  [维度1 联动] Key Ref / 引用计数：从 tex 引用中剔除 {n_drop} 条捏造文献 "
                    f"({', '.join(dropped)})"
                )
        total = len(entries_for_coverage)

        # ── 步骤1：Key References 覆盖检查（全量，不抽样；列表已不含捏造）───
        logger.info(f"  [步骤1] Key References 覆盖检查: {article_name} ({total} 条有效引用)")
        key_coverage = self._check_key_coverage(entries_for_coverage, plan_content)
        total_key_refs = len(key_coverage)
        covered = sum(1 for r in key_coverage if r.covered)
        logger.info(f"  覆盖 {covered}/{total_key_refs} 条 Key References")

        # ── 步骤2：质量打分 ────────────────────────────────────────────
        entry_by_key = {e.key: e for e in entries}

        def _fabricated_result(e: BibEntry) -> CitationRelevanceResult:
            return CitationRelevanceResult(
                citation_key=e.key,
                title=e.title,
                authors=e.author_string,
                year=e.year,
                relevance_score=0,
                reason="维度1 内容准确性检测：完全捏造论文（accuracy_level=0），直接计为不相关"
            )

        quality_results: List[CitationRelevanceResult] = []
        fab_in_batch = 0

        if quality_key_order is not None:
            if fabricated_keys:
                logger.info(f"  [维度1 联动] 捏造 key 集合: " + ", ".join(sorted(fabricated_keys)))
            logger.info(
                f"  [步骤2] 与维度1 对齐的质量打分: {article_name}，共 {len(quality_key_order)} 条 cite key"
            )
            for i, key in enumerate(quality_key_order):
                e = entry_by_key.get(key)
                if e is None:
                    logger.warning(f"  quality_key_order 中的 key 不在当前 tex/bib 引用列表中，跳过: {key}")
                    continue
                logger.info(f"  [{i+1}/{len(quality_key_order)}] {e.key} ({e.year})")
                if key in fabricated_keys:
                    quality_results.append(_fabricated_result(e))
                    fab_in_batch += 1
                else:
                    quality_results.append(self._evaluate_single_citation(e, plan_content))
        else:
            # 完全捏造的条目直接记为不相关；排除捏造后再按 sample_size 抽样
            fabricated_results: List[CitationRelevanceResult] = []
            if fabricated_keys:
                fab_entries = [e for e in entries if e.key in fabricated_keys]
                if fab_entries:
                    logger.info(f"  [维度1 联动] 将 {len(fab_entries)} 条完全捏造论文直接计为不相关: "
                                + ", ".join(e.key for e in fab_entries))
                for e in fab_entries:
                    fabricated_results.append(_fabricated_result(e))

            sample_pool = [e for e in entries if e.key not in fabricated_keys]
            sample_entries = sample_pool
            if sample_size is not None and len(sample_pool) > sample_size:
                random.seed(seed)
                sample_entries = random.sample(sample_pool, sample_size)
                logger.info(f"  [步骤2] 抽样质量打分: {article_name}，"
                            f"抽样 {len(sample_entries)}/{len(sample_pool)} 条（已排除 {len(fabricated_results)} 条捏造）")
            else:
                logger.info(f"  [步骤2] 质量打分: {article_name}，共 {len(sample_entries)} 条"
                            + (f"（已排除 {len(fabricated_results)} 条捏造）" if fabricated_results else ""))

            quality_results = list(fabricated_results)
            fab_in_batch = len(fabricated_results)
            for i, entry in enumerate(sample_entries):
                logger.info(f"  [{i+1}/{len(sample_entries)}] {entry.key} ({entry.year})")
                quality_results.append(self._evaluate_single_citation(entry, plan_content))

        eval_result = CitationRelevanceEvalResult(
            article_name=article_name,
            total_citations=total,
            evaluated_citations=len(quality_results),
            citation_results=quality_results,
            key_coverage=key_coverage,
            total_key_refs=total_key_refs,
            fabricated_count=fab_in_batch
        )

        logger.info(f"  {'─'*50}")
        logger.info(f"  小结 [{article_name}]  总分 {eval_result.score}/10")
        logger.info(f"  Key Ref 覆盖 {covered}/{total_key_refs} ({eval_result.coverage_rate:.0%})")
        logger.info(f"  强相关 {eval_result.highly_relevant_count} 篇 | "
                    f"弱相关 {eval_result.evaluated_citations - eval_result.highly_relevant_count - eval_result.irrelevant_count} 篇 | "
                    f"不相关 {eval_result.irrelevant_count} 篇")
        return eval_result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    eval_dir = Path(__file__).parent.parent
    sources_dir = eval_dir.parent / "sources"

    llm = LLMClient()
    evaluator = CitationRelevanceEvaluator(llm)

    result = evaluator.evaluate(
        bib_path=sources_dir / "ours" / "references.bib",
        plan_path=sources_dir / "survey_plan.md",
        article_name="ours"
    )

    print(f"评测结果: {result.score}/10")
    print(f"Key Ref 覆盖: {result.covered_count}/{result.total_key_refs}")
    print(f"强相关: {result.highly_relevant_count}")
    print(f"不相关: {result.irrelevant_count}")
