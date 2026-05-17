#!/usr/bin/env python3
"""Related Works 评测系统主入口

整合四个评测维度：
1. 内容准确性（客观，1-10分，先跑）
2. 引用相关性（客观，1-10分）
3. 指令遵循（AB对称评测）
4. 写作质量（AB对称评测）

Usage:
    python evaluator.py                    # 默认只做客观评测（维度1+2）
    python evaluator.py --dim 1 2 3 4      # 完整评测（含主观维度3+4）
    python evaluator.py --quick            # 快速评测（跳过内容准确性）
    python evaluator.py --dim 3 4          # 只评测主观维度3和4
"""

from pathlib import Path
try:
    from dotenv import load_dotenv
    _eval_survey_root = Path(__file__).resolve().parent.parent
    _paper_gen_root = _eval_survey_root.parent
    load_dotenv(_eval_survey_root / ".env")
    # batch_run/.env 后加载且覆盖，便于在批量实验目录统一改密钥
    load_dotenv(_paper_gen_root / "batch_run" / ".env", override=True)
except ImportError:
    pass

import json
import logging
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml

from .utils.llm_client import LLMClient
from .utils.paper_fetcher import PaperFetcher
from .utils.literature_search import LiteratureSearch
from .metrics.citation_relevance import CitationRelevanceEvaluator
from .metrics.content_accuracy import ContentAccuracyEvaluator
from .metrics.instruction_following import InstructionFollowingEvaluator
from .metrics.writing_quality import WritingQualityEvaluator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RelatedWorksEvaluator:
    """Related Works 评测系统"""

    def __init__(
        self,
        config_path: Optional[Path] = None,
        task: Optional[str] = None,
        eval_model: Optional[str] = None,
    ):
        """初始化评测系统

        Args:
            config_path: 配置文件路径
            task: 任务名称，对应 sources/{task}/ 目录（如 sudamuon、sfedavg）
            eval_model: 打分用 LLM 模型（覆盖 config，用于消融：dpsk、gpt4o、sonnet4.6）
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"

        self.config = self._load_config(config_path)
        self.eval_dir = Path(__file__).parent
        self.sources_dir = self.eval_dir.parent / "sources"
        self.results_dir = self.eval_dir / "results"
        self.results_dir.mkdir(exist_ok=True)
        self.eval_model = eval_model

        # 确定当前任务目录
        if task is not None:
            self.task = task
            self.task_dir = self.sources_dir / task
        else:
            # 自动发现：取 sources/ 下第一个含 survey_plan.md 的目录
            candidates = sorted(
                d for d in self.sources_dir.iterdir()
                if d.is_dir() and (d / "survey_plan.md").exists()
            )
            if not candidates:
                raise FileNotFoundError(
                    "sources/ 下未找到含 survey_plan.md 的任务目录，请用 --task 指定"
                )
            self.task = candidates[0].name
            self.task_dir = candidates[0]
            logger.info(f"自动选择任务: {self.task}")
        
        # 消融模型别名 → 实际 API model_id
        # 注意：在部分 OpenAI 兼容代理上 gpt-4o 可能不可用，可用 gpt-5.1 代替做对照
        EVAL_MODEL_MAP = {
            "dpsk": "deepseek-v3.2",
            "gpt4o": "gpt-4o",
            "gpt51": "gpt-5.1",
            "gpt54": "gpt-5.4",
            "sonnet4.6": "claude-sonnet-4-6",
        }
        model_override = EVAL_MODEL_MAP.get(eval_model, eval_model) if eval_model else None
        if eval_model:
            logger.info(f"打分模型消融: {eval_model} -> {model_override or eval_model}")
        self.llm = LLMClient(config_path, model_override=model_override)
        self.paper_fetcher = PaperFetcher(
            cache_dir=self.eval_dir / "cache",
            max_chars=self.config.get('paper_fetcher', {}).get('max_chars', 50000)
        )

        self.citation_evaluator = CitationRelevanceEvaluator(self.llm)
        lit_search = LiteratureSearch(cache_dir=self.eval_dir / "cache" / "search")
        self.content_evaluator = ContentAccuracyEvaluator(
            self.llm,
            self.paper_fetcher,
            literature_search=lit_search,
            max_papers_to_verify=self.config.get('evaluation', {})
                .get('objective', {})
                .get('content_accuracy', {})
                .get('max_papers_to_verify', 20)
        )
        self.instruction_evaluator = InstructionFollowingEvaluator(self.llm)
        self.writing_evaluator = WritingQualityEvaluator(self.llm)
    
    def _load_config(self, config_path: Path) -> dict:
        """加载配置文件"""
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def _load_task_eval_config(self) -> dict:
        """加载任务级评测配置（sources/{task}/eval_config.yaml）"""
        cfg_path = self.task_dir / "eval_config.yaml"
        if cfg_path.exists():
            with open(cfg_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def _discover_articles(self) -> List[str]:
        """发现当前任务下所有待评测的 agent 文章（sources/{task}/{agent}/）"""
        articles = []
        for item in self.task_dir.iterdir():
            if item.is_dir() and (item / "related_works.tex").exists():
                articles.append(item.name)
        return sorted(articles)
    
    def evaluate(
        self,
        dimensions: Optional[List[int]] = None,
        quick: bool = False,
        sample_size: Optional[int] = None,
        seed: int = 42
    ) -> Dict[str, Any]:
        """运行评测
        
        Args:
            dimensions: 要评测的维度列表（1-4），None 表示全部
            quick: 快速模式，跳过耗时的内容准确性评测
            sample_size: 从每篇文章全部 tex 引用中统一抽取的数量，用于维度1；
                若同时评测维度2，维度2 的质量分仅针对该批 key（Key References 覆盖仍全量）。
                None 表示两维均对引用全量（维度2 质量分侧仍排除捏造 key 后全量）。
            seed: 随机种子
            
        Returns:
            评测结果字典
        """
        if dimensions is None:
            dimensions = [1, 2]  # 默认只做客观评测（内容准确性、引用相关性）
        
        if quick and 1 in dimensions:
            logger.info("快速模式：跳过内容准确性评测（维度1）")
            dimensions = [d for d in dimensions if d != 1]
        
        # 任务级配置：no_sample、valid_non_academic_citations
        task_cfg = self._load_task_eval_config()
        if task_cfg.get("no_sample"):
            sample_size = None
            logger.info(f"任务 {self.task}：禁用抽样，全量评估")
        elif sample_size is None:
            # 未指定 --sample 时使用 config 默认
            sample_size = self.config.get('evaluation', {}).get('objective', {}).get('sample_size')
        if sample_size is not None:
            logger.info(
                f"抽样模式：每篇文章从全部 tex 引用中统一抽 {sample_size} 条；"
                f"维度1 仅验证该批；与维度2 同批时相关性质量分仅评该批（Key Ref 覆盖仍全量）"
            )
        
        valid_non_academic = set(task_cfg.get("valid_non_academic_citations") or [])
        if valid_non_academic:
            logger.info(f"任务 {self.task}：白名单引用（blog/技术报告等）{valid_non_academic}")
        
        articles = self._discover_articles()
        logger.info(f"任务: {self.task}，发现 {len(articles)} 篇待评测文章: {articles}")

        plan_path = self.task_dir / "survey_plan.md"
        if not plan_path.exists():
            raise FileNotFoundError(f"未找到 survey_plan.md: {plan_path}")

        results = {
            "evaluation_time": datetime.now().isoformat(),
            "task": self.task,
            "eval_model": self.eval_model or self.config.get("llm", {}).get("model", "default"),
            "articles": articles,
            "dimensions_evaluated": dimensions,
            "objective_scores": {},
            "comparative_results": {}
        }

        # fabricated_keys_by_article: 存储各文章由内容准确性检测出的完全捏造 cite key，供引用相关性联动
        fabricated_keys_by_article: Dict[str, set] = {a: set() for a in articles}
        # 维度1 实际验证的 cite key 顺序，供维度2 质量分与维度1 同批对齐
        content_accuracy_key_order_by_article: Dict[str, List[str]] = {}

        # ── 维度1 内容准确性先跑，给维度2 引用相关性提供完全捏造的 key 集合 ─────
        if 1 in dimensions:
            logger.info("=" * 50)
            logger.info("维度1: 内容准确性评测（先跑，以便联动）")
            logger.info("=" * 50)
            for article in articles:
                tex_path = self.task_dir / article / "related_works.tex"
                bib_path = self.task_dir / article / "references.bib"
                if tex_path.exists() and bib_path.exists():
                    result = self.content_evaluator.evaluate(
                        tex_path=tex_path,
                        bib_path=bib_path,
                        article_name=article,
                        sample_size=sample_size,
                        seed=seed,
                        valid_non_academic_citations=valid_non_academic
                    )
                    if article not in results["objective_scores"]:
                        results["objective_scores"][article] = {}
                    results["objective_scores"][article]["content_accuracy"] = result.to_dict()
                    content_accuracy_key_order_by_article[article] = [
                        r.citation_key for r in result.citation_results
                    ]
                    logger.info(f"  {article}: {result.score}/10 (幻觉: {result.hallucination_count})")

                    # 收集完全捏造（accuracy_level==0）的 cite key
                    fab_keys = {
                        r.citation_key
                        for r in result.citation_results
                        if r.verified and r.accuracy_level == 0
                    }
                    if fab_keys:
                        fabricated_keys_by_article[article] = fab_keys
                        logger.info(f"  [联动] {article} 发现 {len(fab_keys)} 条完全捏造论文，"
                                    f"将传入引用相关性: {fab_keys}")

        if 2 in dimensions:
            logger.info("=" * 50)
            logger.info("维度2: 引用相关性评测")
            logger.info("=" * 50)
            for article in articles:
                bib_path = self.task_dir / article / "references.bib"
                if bib_path.exists():
                    use_aligned = 1 in dimensions and article in content_accuracy_key_order_by_article
                    result = self.citation_evaluator.evaluate(
                        bib_path=bib_path,
                        plan_path=plan_path,
                        tex_path=self.task_dir / article / "related_works.tex",
                        article_name=article,
                        sample_size=None if use_aligned else sample_size,
                        seed=seed,
                        fabricated_keys=fabricated_keys_by_article.get(article),
                        quality_key_order=(
                            content_accuracy_key_order_by_article[article] if use_aligned else None
                        ),
                    )
                    if article not in results["objective_scores"]:
                        results["objective_scores"][article] = {}
                    results["objective_scores"][article]["citation_relevance"] = result.to_dict()
                    logger.info(f"  {article}: {result.score}/10"
                                + (f" (联动排除捏造: {result.fabricated_count}篇)"
                                   if result.fabricated_count else ""))

        if len(articles) >= 2 and (3 in dimensions or 4 in dimensions):
            for i, article_a in enumerate(articles):
                for article_b in articles[i+1:]:
                    pair_key = f"{article_a}_vs_{article_b}"
                    results["comparative_results"][pair_key] = {}

                    tex_a = self.task_dir / article_a / "related_works.tex"
                    tex_b = self.task_dir / article_b / "related_works.tex"
                    
                    if 3 in dimensions:
                        logger.info("=" * 50)
                        logger.info(f"维度3: 指令遵循评测 ({article_a} vs {article_b})")
                        logger.info("=" * 50)
                        result = self.instruction_evaluator.evaluate(
                            tex_path_a=tex_a,
                            tex_path_b=tex_b,
                            plan_path=plan_path,
                            article_a=article_a,
                            article_b=article_b
                        )
                        results["comparative_results"][pair_key]["instruction_following"] = result.to_dict()
                        logger.info(f"  胜者: {result.final_winner}")
                    
                    if 4 in dimensions:
                        logger.info("=" * 50)
                        logger.info(f"维度4: 写作质量评测 ({article_a} vs {article_b})")
                        logger.info("=" * 50)
                        result = self.writing_evaluator.evaluate(
                            tex_path_a=tex_a,
                            tex_path_b=tex_b,
                            article_a=article_a,
                            article_b=article_b
                        )
                        results["comparative_results"][pair_key]["writing_quality"] = result.to_dict()
                        logger.info(f"  胜者: {result.final_winner}")
        
        results["summary"] = self._generate_summary(results)
        sm = results["summary"]
        results["aggregate"] = {
            "run_mean_total": sm.get("run_mean_total"),
            "per_article_max_total": sm.get("per_article_max_total"),
            "per_article_total_scores": sm.get("per_article_total_scores", {}),
            "run_mean_content_accuracy": sm.get("run_mean_content_accuracy"),
            "run_mean_citation_relevance": sm.get("run_mean_citation_relevance"),
        }

        self._save_results(results)
        
        return results
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成评测摘要，包含各维度排名和总分汇总"""
        articles = results.get("articles", [])
        summary = {
            "objective_rankings": {},
            "comparative_results": {},
            "total_scores": {}
        }

        # ── 客观维度排名（先内容准确性，再引用相关性）────────────────────────────
        for metric in ["content_accuracy", "citation_relevance"]:
            scores = []
            for article, data in results.get("objective_scores", {}).items():
                if metric in data:
                    scores.append((article, data[metric].get("score", 0)))
            scores.sort(key=lambda x: x[1], reverse=True)
            summary["objective_rankings"][metric] = scores

        # ── 多配置批量：每篇「总分」= 维度1 + 维度2（各 0–10，合计 0–20）；本组总分 = 跨篇均值 ──
        per_article_total: Dict[str, float] = {}
        ca_vals: list[float] = []
        cr_vals: list[float] = []
        for article in articles:
            obj = results.get("objective_scores", {}).get(article, {})
            ca = obj.get("content_accuracy", {}).get("score")
            cr = obj.get("citation_relevance", {}).get("score")
            if ca is None and cr is None:
                continue
            ca_f = float(ca if ca is not None else 0)
            cr_f = float(cr if cr is not None else 0)
            per_article_total[article] = round(ca_f + cr_f, 2)
            if ca is not None:
                ca_vals.append(ca_f)
            if cr is not None:
                cr_vals.append(cr_f)
        if per_article_total:
            totals = list(per_article_total.values())
            summary["per_article_total_scores"] = per_article_total
            summary["run_mean_total"] = round(sum(totals) / len(totals), 3)
            summary["run_max_article_total"] = round(max(totals), 2)
            summary["run_min_article_total"] = round(min(totals), 2)
            summary["per_article_max_total"] = 20.0
            if ca_vals:
                summary["run_mean_content_accuracy"] = round(sum(ca_vals) / len(ca_vals), 3)
            if cr_vals:
                summary["run_mean_citation_relevance"] = round(sum(cr_vals) / len(cr_vals), 3)

        # ── 主观维度相对分 ────────────────────────────────────────────────────
        for pair_key, data in results.get("comparative_results", {}).items():
            summary["comparative_results"][pair_key] = {}
            for metric in ["instruction_following", "writing_quality"]:
                if metric in data:
                    summary["comparative_results"][pair_key][metric] = {
                        "final_winner": data[metric].get("final_winner", "unknown"),
                        "relative_score": data[metric].get("relative_score", 0.0)
                    }

        # ── 总分汇总（仅两篇文章时有意义）─────────────────────────────────────
        # 总分 = 内容准确性(1-10) + 引用相关性(1-10) + dim3(-5~+5) + dim4(同)
        # 主观维度转换：relative_score > 0 则 A 得 relative_score，B 得 0（相对优势分）
        if len(articles) == 2:
            a, b = articles[0], articles[1]
            pair_key = f"{a}_vs_{b}"
            total = {a: 0.0, b: 0.0}

            obj = results.get("objective_scores", {})
            for article in [a, b]:
                if "citation_relevance" in obj.get(article, {}):
                    total[article] += obj[article]["citation_relevance"].get("score", 0)
                if "content_accuracy" in obj.get(article, {}):
                    total[article] += obj[article]["content_accuracy"].get("score", 0)

            comp = results.get("comparative_results", {}).get(pair_key, {})
            for metric in ["instruction_following", "writing_quality"]:
                if metric in comp:
                    rel = comp[metric].get("relative_score", 0.0)
                    if rel > 0:
                        total[a] += rel
                    elif rel < 0:
                        total[b] += abs(rel)

            summary["total_scores"] = {
                art: round(total[art], 2) for art in [a, b]
            }

        return summary
    
    def _save_results(self, results: Dict[str, Any]):
        """保存评测结果（文件名带任务名、打分模型和时间戳）"""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        eval_model = self.eval_model or "default"
        stem = f"{self.task}_{eval_model}_{ts}"

        json_path = self.results_dir / f"eval_result_{stem}.json"
        clean_json = json.dumps(results, indent=2, ensure_ascii=False)
        clean_json = self._strip_ansi(clean_json)
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(clean_json)
        logger.info(f"JSON 结果已保存: {json_path}")

        md_path = self.results_dir / f"eval_report_{stem}.md"
        self._generate_markdown_report(results, md_path)
        logger.info(f"Markdown 报告已保存: {md_path}")

        self._json_path = json_path
        self._md_path = md_path
    
    @staticmethod
    def _strip_ansi(text: str) -> str:
        """移除 ANSI 终端转义码"""
        return re.sub(r'\x1b\[[0-9;]*m', '', text)

    def _generate_markdown_report(self, results: Dict[str, Any], output_path: Path):
        """生成 Markdown 格式的评测报告"""
        eval_model = results.get("eval_model", "default")
        lines = [
            "# Related Works 评测报告",
            "",
            f"**评测时间**: {results.get('evaluation_time', 'N/A')}",
            f"**打分模型**: {eval_model}",
            f"**评测文章**: {', '.join(results.get('articles', []))}",
            f"**评测维度**: {results.get('dimensions_evaluated', [])}",
            "",
            "---",
            "",
            "## 执行摘要",
            "",
        ]
        
        summary = results.get("summary", {})

        for metric, rankings in summary.get("objective_rankings", {}).items():
            metric_name = "引用相关性" if metric == "citation_relevance" else "内容准确性"
            lines.append(f"### {metric_name}排名（1-10分）")
            for i, (article, score) in enumerate(rankings, 1):
                lines.append(f"{i}. **{article}**: {score}/10")
            lines.append("")

        if summary.get("run_mean_total") is not None:
            lines.append("### 本组客观总分（多配置汇总）")
            lines.append(
                "- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。"
            )
            lines.append(
                f"- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = "
                f"**{summary['run_mean_total']}** / 20"
            )
            if summary.get("run_mean_content_accuracy") is not None:
                lines.append(
                    f"- 跨配置平均 · 内容准确性: **{summary['run_mean_content_accuracy']}** / 10"
                )
            if summary.get("run_mean_citation_relevance") is not None:
                lines.append(
                    f"- 跨配置平均 · 引用相关性: **{summary['run_mean_citation_relevance']}** / 10"
                )
            pat = summary.get("per_article_total_scores") or {}
            if pat:
                lines.append("- 各配置总分（CA+CR）:")
                for art in sorted(pat.keys(), key=lambda x: pat[x], reverse=True):
                    lines.append(f"  - **{art}**: {pat[art]} / 20")
            lines.append("")

        for pair_key, metrics in summary.get("comparative_results", {}).items():
            lines.append(f"### 对比评测: {pair_key}")
            for metric, info in metrics.items():
                metric_name = "指令遵循" if metric == "instruction_following" else "写作质量"
                rel = info.get("relative_score", 0.0)
                winner = info.get("final_winner", "N/A")
                sign = "+" if rel >= 0 else ""
                lines.append(f"- {metric_name}: 胜者 **{winner}**，相对分 {sign}{rel:.2f} / 5.0")
            lines.append("")

        total_scores = summary.get("total_scores", {})
        if total_scores:
            dims = results.get("dimensions_evaluated", [])
            has_subjective = 3 in dims or 4 in dims
            max_score = 30 if has_subjective else 20
            formula = "内容准确性(1-10) + 引用相关性(1-10)" + (
                " + dim3相对优势分(0~5) + dim4相对优势分(0~5)" if has_subjective else ""
            )
            lines.append("### 综合总分")
            lines.append(f"> 总分 = {formula}，满分{max_score}分")
            sorted_total = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
            for i, (article, score) in enumerate(sorted_total, 1):
                lines.append(f"{i}. **{article}**: {score:.2f} / {max_score}")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## 详细评测结果",
            "",
        ])
        
        if results.get("objective_scores"):
            lines.append("### 客观评测（维度1-2）")
            lines.append("")
            
            for article, data in results["objective_scores"].items():
                lines.append(f"#### {article}")
                lines.append("")
                
                # 先内容准确性，再引用相关性
                if "content_accuracy" in data:
                    ca = data["content_accuracy"]
                    lines.extend([
                        f"**内容准确性**: {ca.get('score', 'N/A')}/10",
                        f"- 验证引用数: {ca.get('verified_citations', 0)}",
                        f"- 幻觉数量: {ca.get('hallucination_count', 0)}",
                        f"- 下载失败跳过: {ca.get('failed_count', 0)}",
                        ""
                    ])
                    
                    hallucinations = ca.get("hallucinations", [])
                    if hallucinations:
                        lines.append("**发现的幻觉:**")
                        for h in hallucinations[:5]:
                            lines.append(f"- `{h.get('key')}`: {h.get('type')} - {h.get('details', '')[:100]}")
                        lines.append("")
                
                if "citation_relevance" in data:
                    cr = data["citation_relevance"]
                    covered = cr.get('key_refs_covered', 'N/A')
                    total_kr = cr.get('key_refs_total', 'N/A')
                    cov_rate = cr.get('coverage_rate', 0)
                    fab_count = cr.get('fabricated_count', 0)
                    fab_note = f"（其中 {fab_count} 条为内容准确性检测的完全捏造，已直接计为不相关）" if fab_count else ""
                    lines.extend([
                        f"**引用相关性**: {cr.get('score', 'N/A')}/10",
                        f"- Key References 覆盖: {covered}/{total_kr} ({cov_rate:.0%})",
                        f"- 总引用数: {cr.get('total_citations', 0)}（评估 {cr.get('evaluated_citations', 0)} 条{fab_note}）",
                        f"- 强相关: {cr.get('highly_relevant', 0)}",
                        f"- 弱相关: {cr.get('weakly_relevant', 0)}",
                        f"- 不相关: {cr.get('irrelevant', 0)}",
                        ""
                    ])
                    key_coverage = cr.get("key_coverage", [])
                    if key_coverage:
                        lines.append("**Key References 覆盖详情:**")
                        for kc in key_coverage:
                            mark = "✓" if kc.get("covered") else "✗"
                            matched = f" → `{kc['matched_cite_key']}`" if kc.get("matched_cite_key") else ""
                            lines.append(f"- {mark} {kc.get('key_ref', '')}{matched}")
                        lines.append("")
        
        if results.get("comparative_results"):
            lines.append("### 对比评测（维度3-4）")
            lines.append("")
            
            for pair_key, data in results["comparative_results"].items():
                lines.append(f"#### {pair_key}")
                lines.append("")
                
                if "instruction_following" in data:
                    inf = data["instruction_following"]
                    rel = inf.get("relative_score", 0.0)
                    sign = "+" if rel >= 0 else ""
                    lines.extend([
                        f"**指令遵循（计划遵循度）**: 相对分 {sign}{rel:.2f} / 5.0，胜者 **{inf.get('final_winner', 'N/A')}**",
                        ""
                    ])
                    dim_scores = inf.get("dimension_scores", {})
                    if dim_scores:
                        inf_dim_names = {
                            "topic_coverage": "主题覆盖",
                            "narrative_arc": "叙事脉络",
                            "task_fulfillment": "任务完成",
                            "content_richness": "内容丰富度",
                            "professional_depth": "专业程度"
                        }
                        lines.append("**各子维度相对分（正=第一篇好，负=第二篇好）:**")
                        for dim, score in dim_scores.items():
                            sign_d = "+" if score >= 0 else ""
                            lines.append(f"- {inf_dim_names.get(dim, dim)}: {sign_d}{score:.2f}")
                        lines.append("")

                if "writing_quality" in data:
                    wq = data["writing_quality"]
                    rel = wq.get("relative_score", 0.0)
                    sign = "+" if rel >= 0 else ""
                    lines.extend([
                        f"**写作质量**: 相对分 {sign}{rel:.2f} / 5.0，胜者 **{wq.get('final_winner', 'N/A')}**",
                        ""
                    ])
                    dim_scores = wq.get("dimension_scores", {})
                    if dim_scores:
                        wq_dim_names = {
                            "density": "信息密度",
                            "depth": "技术深度",
                            "synthesis": "批判性综合",
                            "motivation": "动机涌现"
                        }
                        lines.append("**各子维度相对分（正=第一篇好，负=第二篇好）:**")
                        for dim, score in dim_scores.items():
                            sign_d = "+" if score >= 0 else ""
                            lines.append(f"- {wq_dim_names.get(dim, dim)}: {sign_d}{score:.2f}")
                        lines.append("")
        
        content = self._strip_ansi("\n".join(lines))
        output_path.write_text(content, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(
        description="Related Works 评测系统",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--dim",
        type=int,
        nargs="+",
        choices=[1, 2, 3, 4],
        help="要评测的维度（1=内容准确性, 2=引用相关性, 3=指令遵循, 4=写作质量）"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="快速模式：跳过内容准确性（维度1）"
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        metavar="N",
        help="内容准确性/引用相关性的抽样数量（默认评估全部，推荐值：15-20）"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="随机种子，保证抽样可复现（默认 42）"
    )
    parser.add_argument(
        "--task",
        type=str,
        default=None,
        help="任务名称，对应 sources/{task}/ 目录（如 sudamuon、sfedavg）。不指定则自动选择"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="配置文件路径"
    )
    parser.add_argument(
        "--eval-model",
        type=str,
        default=None,
        help="打分用 LLM 模型（消融：dpsk、gpt4o、sonnet4.6）"
    )

    args = parser.parse_args()

    evaluator = RelatedWorksEvaluator(
        args.config,
        task=args.task,
        eval_model=args.eval_model,
    )
    results = evaluator.evaluate(
        dimensions=args.dim,
        quick=args.quick,
        sample_size=args.sample,
        seed=args.seed
    )

    print("\n" + "=" * 50)
    print("评测完成！")
    print("=" * 50)
    print(f"JSON 结果: {evaluator._json_path}")
    print(f"Markdown 报告: {evaluator._md_path}")


if __name__ == "__main__":
    main()
