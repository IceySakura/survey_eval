#!/usr/bin/env python3
"""从 eval-survey/eval/results/eval_result_*.json 汇总表格、消融与评测一致性分析。

输出：
  - batch_run/results/eval_analysis.md
  - batch_run/results/eval_leaderboard.csv（按任务内排名：生成配置 × 三评测均分）
  - batch_run/results/eval_matrix_by_task.csv（与 leaderboard 同构的长表）
  - batch_run/results/eval_citation_stats.csv（各生成配置：引用条数、关键覆盖、CR 分等）

用法：
  python batch_run/summarize_eval_analysis.py
  python batch_run/summarize_eval_analysis.py --results-dir eval-survey/eval/results
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RESULTS = ROOT / "eval-survey" / "eval" / "results"
OUT_DIR = ROOT / "batch_run" / "results"

EVAL_MODELS_ORDER = ["gpt51", "sonnet4.6", "dpsk"]


def _per_article_totals(data: dict) -> Dict[str, float]:
    ag = data.get("aggregate") or {}
    sm = data.get("summary") or {}
    pt = ag.get("per_article_total_scores") or sm.get("per_article_total_scores")
    if isinstance(pt, dict) and pt:
        return {k: float(v) for k, v in pt.items()}
    out: Dict[str, float] = {}
    for art, o in (data.get("objective_scores") or {}).items():
        ca = (o.get("content_accuracy") or {}).get("score")
        cr = (o.get("citation_relevance") or {}).get("score")
        if ca is None and cr is None:
            continue
        out[art] = float(ca or 0) + float(cr or 0)
    return out


def parse_variant(article: str) -> Tuple[str, str]:
    """(agent, backbone) 如 base, gpt51"""
    if article.startswith("base_"):
        return "base", article[5:]
    if article.startswith("reasflow_"):
        return "reasflow", article[9:]
    return "other", article


def discover_latest(
    results_dir: Path,
    tasks: Optional[List[str]] = None,
) -> Dict[Tuple[str, str], Path]:
    """(task, eval_model) -> 最新 json 路径。"""
    by_key: Dict[Tuple[str, str], List[Path]] = defaultdict(list)
    for p in results_dir.glob("eval_result_*.json"):
        # eval_result_{task}_{eval_model}_{YYYYMMDD_HHMMSS}.json
        # 从 JSON 内容读取 task/eval_model 字段（不硬编码任务名）
        m = re.match(r"^eval_result_(.+)_(\d{8}_\d{6})\.json$", p.name)
        if not m:
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        task = data.get("task")
        em = data.get("eval_model")
        if not task or not em:
            continue
        if tasks and task not in tasks:
            continue
        by_key[(task, em)].append(p)
    out: Dict[Tuple[str, str], Path] = {}
    for k, paths in by_key.items():
        out[k] = max(paths, key=lambda x: x.stat().st_mtime)
    return out


def load_combo(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _first_eval_path_for_task(
    latest: Dict[Tuple[str, str], Path], task: str
) -> Optional[Path]:
    for em in EVAL_MODELS_ORDER:
        p = latest.get((task, em))
        if p:
            return p
    return None


def build_citation_stats_rows(
    latest: Dict[Tuple[str, str], Path],
    tasks_seen: List[str],
    json_cache: Dict[Path, dict],
) -> List[dict]:
    """各生成配置的引用条数与维度2子指标；条数类字段取该任务首个可用评测 JSON（与评测模型无关）。"""

    def getd(p: Path) -> dict:
        if p not in json_cache:
            json_cache[p] = load_combo(p)
        return json_cache[p]

    rows: List[dict] = []
    for task in tasks_seen:
        canon_p = _first_eval_path_for_task(latest, task)
        if not canon_p:
            continue
        d0 = getd(canon_p)
        for art in sorted((d0.get("objective_scores") or {}).keys()):
            cr0 = (
                (d0.get("objective_scores") or {})
                .get(art, {})
                .get("citation_relevance")
            )
            if not cr0:
                continue
            agent, backbone = parse_variant(art)
            cov = cr0.get("coverage_rate")
            cov_s = f"{float(cov) * 100:.1f}%" if cov is not None else ""
            row: dict = {
                "task": task,
                "variant": art,
                "agent": agent,
                "backbone": backbone,
                "total_citations": cr0.get("total_citations", ""),
                "evaluated_citations": cr0.get("evaluated_citations", ""),
                "key_refs_covered": cr0.get("key_refs_covered", ""),
                "key_refs_total": cr0.get("key_refs_total", ""),
                "coverage_rate": cov_s,
                "fabricated_count": cr0.get("fabricated_count", ""),
            }
            for em in EVAL_MODELS_ORDER:
                p = latest.get((task, em))
                if not p:
                    row[f"cr_{em}"] = ""
                    continue
                cr = (
                    getd(p)
                    .get("objective_scores", {})
                    .get(art, {})
                    .get("citation_relevance", {})
                )
                sc = cr.get("score")
                row[f"cr_{em}"] = round(float(sc), 2) if sc is not None else ""
            rows.append(row)
    rows.sort(key=lambda r: (r["task"], r["variant"]))
    return rows


def md_table(headers: List[str], rows: List[List[object]]) -> str:
    lines = [
        "| " + " | ".join(str(h) for h in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    ap.add_argument(
        "--tasks",
        nargs="*",
        default=None,
        help="仅这些 task；默认从文件名推断全部",
    )
    args = ap.parse_args()
    results_dir = args.results_dir
    if not results_dir.is_dir():
        print(f"目录不存在: {results_dir}")
        return 1

    latest = discover_latest(results_dir, tasks=args.tasks)
    if not latest:
        print("未找到 eval_result_*.json")
        return 1

    tasks_seen = sorted({k[0] for k in latest})

    json_cache: Dict[Path, dict] = {}
    citation_stats_rows = build_citation_stats_rows(latest, tasks_seen, json_cache)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUT_DIR / "eval_leaderboard.csv"
    citation_csv = OUT_DIR / "eval_citation_stats.csv"
    if citation_stats_rows:
        cf = [
            "task",
            "variant",
            "agent",
            "backbone",
            "total_citations",
            "evaluated_citations",
            "key_refs_covered",
            "key_refs_total",
            "coverage_rate",
            "fabricated_count",
        ] + [f"cr_{em}" for em in EVAL_MODELS_ORDER]
        with open(citation_csv, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cf, extrasaction="ignore")
            w.writeheader()
            w.writerows(citation_stats_rows)

    # —— 按任务的矩阵：生成配置 × 评测模型 ——
    matrix_rows: List[dict] = []
    for task in tasks_seen:
        pt_by_em: Dict[str, Dict[str, float]] = {}
        for em in EVAL_MODELS_ORDER:
            p = latest.get((task, em))
            if not p:
                continue
            pt_by_em[em] = _per_article_totals(load_combo(p))
        all_arts = set()
        for pt in pt_by_em.values():
            all_arts |= set(pt.keys())
        for art in sorted(all_arts):
            agent, backbone = parse_variant(art)
            row: dict = {
                "task": task,
                "variant": art,
                "agent": agent,
                "backbone": backbone,
            }
            scores = []
            for em in EVAL_MODELS_ORDER:
                v = pt_by_em.get(em, {}).get(art)
                row[f"total_{em}"] = round(v, 2) if v is not None else ""
                if v is not None:
                    scores.append(v)
            row["mean_eval_models"] = round(sum(scores) / len(scores), 3) if scores else ""
            matrix_rows.append(row)
        matrix_rows.sort(
            key=lambda r: (
                r["task"],
                -(float(r["mean_eval_models"]) if r["mean_eval_models"] != "" else -1),
                r["variant"],
            ),
        )

    matrix_csv = OUT_DIR / "eval_matrix_by_task.csv"
    if matrix_rows:
        fields = [
            "task",
            "variant",
            "agent",
            "backbone",
            "total_gpt51",
            "total_sonnet4.6",
            "total_dpsk",
            "mean_eval_models",
        ]
        with open(matrix_csv, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(matrix_rows)

    # —— 以生成配置为核心：任务内按「三评测均分」排名（leaderboard CSV）——
    rows_variant: List[dict] = []
    for task in tasks_seen:
        msub = [r for r in matrix_rows if r["task"] == task]
        msub.sort(
            key=lambda r: (
                -(float(r["mean_eval_models"]) if r["mean_eval_models"] != "" else -1),
                r["variant"],
            ),
        )
        rank = 0
        for r in msub:
            rank += 1
            mu = r["mean_eval_models"]
            rows_variant.append(
                {
                    "task": task,
                    "rank_in_task": rank,
                    "variant": r["variant"],
                    "agent": r["agent"],
                    "backbone": r["backbone"],
                    "mean_across_eval_models": mu,
                    "total_gpt51": r.get("total_gpt51", ""),
                    "total_sonnet4.6": r.get("total_sonnet4.6", ""),
                    "total_dpsk": r.get("total_dpsk", ""),
                }
            )
    if rows_variant:
        vf = [
            "task",
            "rank_in_task",
            "variant",
            "agent",
            "backbone",
            "mean_across_eval_models",
            "total_gpt51",
            "total_sonnet4.6",
            "total_dpsk",
        ]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=vf, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows_variant)

    # —— 消融：agent ——
    ab_agent: List[dict] = []
    for task in tasks_seen:
        for em in EVAL_MODELS_ORDER:
            p = latest.get((task, em))
            if not p:
                continue
            pt = _per_article_totals(load_combo(p))
            b = [s for a, s in pt.items() if parse_variant(a)[0] == "base"]
            r = [s for a, s in pt.items() if parse_variant(a)[0] == "reasflow"]
            ab_agent.append(
                {
                    "task": task,
                    "eval_model": em,
                    "mean_base": round(sum(b) / len(b), 3) if b else "",
                    "mean_reasflow": round(sum(r) / len(r), 3) if r else "",
                    "delta_rf_minus_base": (
                        round(sum(r) / len(r) - sum(b) / len(b), 3)
                        if b and r
                        else ""
                    ),
                }
            )

    # —— 消融：backbone（同一 backbone 下 base vs reasflow 配对差）——
    ab_backbone: List[dict] = []
    backbones = sorted(
        {parse_variant(a)[1] for row in matrix_rows for a in [row["variant"]]}
    )
    for task in tasks_seen:
        for bb in backbones:
            for em in EVAL_MODELS_ORDER:
                p = latest.get((task, em))
                if not p:
                    continue
                pt = _per_article_totals(load_combo(p))
                tb = pt.get(f"base_{bb}")
                tr = pt.get(f"reasflow_{bb}")
                if tb is None and tr is None:
                    continue
                ab_backbone.append(
                    {
                        "task": task,
                        "backbone": bb,
                        "eval_model": em,
                        "base_total": round(tb, 2) if tb is not None else "",
                        "reasflow_total": round(tr, 2) if tr is not None else "",
                        "delta_rf_minus_base": (
                            round(tr - tb, 2)
                            if tb is not None and tr is not None
                            else ""
                        ),
                    }
                )

    # —— 评测可靠性：三评测模型与跨评测均值的平方偏差和 ——
    ssd: Dict[str, float] = defaultdict(float)
    n_triples = 0
    for task in tasks_seen:
        loaded = {
            em: load_combo(latest[(task, em)])
            for em in EVAL_MODELS_ORDER
            if (task, em) in latest
        }
        if len(loaded) < 3:
            continue
        pts = {em: _per_article_totals(d) for em, d in loaded.items()}
        common = set.intersection(*(set(pts[em].keys()) for em in pts))
        for art in common:
            if not all(em in pts and art in pts[em] for em in EVAL_MODELS_ORDER):
                continue
            vals = [pts[em][art] for em in EVAL_MODELS_ORDER]
            mu = sum(vals) / 3
            for em, v in zip(EVAL_MODELS_ORDER, vals):
                ssd[em] += (v - mu) ** 2
            n_triples += 1

    ssd_rows = sorted(ssd.items(), key=lambda x: x[1])

    # —— Markdown 报告 ——
    md_lines: List[str] = [
        "# 评测结果汇总与消融分析",
        "",
        "**总分定义**：每篇生成配置 = 内容准确性(0–10) + 引用相关性(0–10)，最高 20。",
        "**Leaderboard 排名依据**：固定任务，对**每个生成配置**取各评测模型下的篇总分，再对**已有评测**求算术平均（通常为三套评测）；**任务内**按该均值降序排名。",
        "细粒度矩阵见 `eval_matrix_by_task.csv`；同构排名表见 `eval_leaderboard.csv`。",
        "",
        "## 1. Leaderboard（按任务：生成配置 × 跨评测均分，降序排名）",
        "",
    ]
    for task in tasks_seen:
        msub = [r for r in rows_variant if r["task"] == task]
        md_lines.extend(
            [
                f"### 1.{tasks_seen.index(task) + 1} 任务 `{task}`",
                "",
            ]
        )
        md_lines.append(
            md_table(
                [
                    "排名",
                    "生成配置",
                    "agent",
                    "backbone",
                    "gpt51",
                    "sonnet4.6",
                    "dpsk",
                    "跨评测均值",
                ],
                [
                    [
                        r["rank_in_task"],
                        r["variant"],
                        r["agent"],
                        r["backbone"],
                        r["total_gpt51"],
                        r["total_sonnet4.6"],
                        r["total_dpsk"],
                        r["mean_across_eval_models"],
                    ]
                    for r in msub
                ],
            )
        )
        md_lines.append("")

    md_lines.extend(
        [
            "## 2. 消融：Agent（base vs reasflow）",
            "同一任务、同一评测模型下，对所有生成 backbone 的篇总分取平均。",
            "",
        ]
    )
    md_lines.append(
        md_table(
            ["任务", "评测模型", "base 平均总分", "reasflow 平均总分", "差(reasflow−base)"],
            [
                [
                    r["task"],
                    r["eval_model"],
                    r["mean_base"],
                    r["mean_reasflow"],
                    r["delta_rf_minus_base"],
                ]
                for r in sorted(ab_agent, key=lambda x: (x["task"], x["eval_model"]))
            ],
        )
    )

    md_lines.extend(
        [
            "",
            "## 3. 消融：同 backbone 配对（base_* vs reasflow_*）",
            "",
        ]
    )
    md_lines.append(
        md_table(
            [
                "任务",
                "backbone",
                "评测模型",
                "base 总分",
                "reasflow 总分",
                "差",
            ],
            [
                [
                    r["task"],
                    r["backbone"],
                    r["eval_model"],
                    r["base_total"],
                    r["reasflow_total"],
                    r["delta_rf_minus_base"],
                ]
                for r in sorted(
                    ab_backbone,
                    key=lambda x: (x["task"], x["backbone"], x["eval_model"]),
                )
            ],
        )
    )

    md_lines.extend(
        [
            "",
            "## 4. 评测可靠性（三评测模型与组内均值的偏差）",
            f"对 **{n_triples}** 个 (任务, 生成配置) 三元组，计算三评测打分的均值 $\\mu$，",
            "再算各评测模型的 $\\sum (s-\\mu)^2$（越小表示越接近三者的「共识中心」）。",
            "",
        ]
    )
    md_lines.append(
        md_table(
            ["评测模型", "偏差平方和 SSD", "解释"],
            [
                [
                    em,
                    round(ssd[em], 3) if em in ssd else "",
                    "最小 → 相对最接近三评测平均" if ssd_rows and em == ssd_rows[0][0] else "",
                ]
                for em, _ in sorted(ssd.items(), key=lambda x: x[1])
            ]
        )
    )
    if ssd_rows:
        md_lines.append("")
        md_lines.append(
            f"**结论**：SSD 最小为 **`{ssd_rows[0][0]}`**（={round(ssd_rows[0][1], 3)}），"
            "在「与三模型均值距离」意义上最居中；注意这不等于「更正确」，仅衡量三评测一致性。"
        )

    md_path = OUT_DIR / "eval_analysis.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"已写: {md_path}")
    print(f"已写: {csv_path}")
    print(f"已写: {matrix_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
