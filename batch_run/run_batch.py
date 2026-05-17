#!/usr/bin/env python3
"""全自动批量评测：生成（agentscope/base）→ eval-survey 评测 → 汇总

默认读取 `batch_run/config.yaml`：
- tasks: 任务列表（eval-survey/sources/{task}/survey_plan.md 必须存在）
- variants: 生成变体列表（run_one.py 支持的 variant 名）
- eval_models: 打分模型列表（传给 eval.evaluator --eval-model）

用法：
  python batch_run/run_batch.py
  python batch_run/run_batch.py --generate-only
  python batch_run/run_batch.py --eval-only
  python batch_run/run_batch.py --eval-only --resume   # 跳过已有 eval_result_{task}_{model}_*.json，换 key 后续跑
  python batch_run/run_batch.py --task sudamuon --variant reasflow_gpt51 --eval-model gpt4o
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _list_json_results(results_dir: Path) -> set[Path]:
    if not results_dir.exists():
        return set()
    return {p for p in results_dir.iterdir() if p.is_file() and p.name.endswith(".json")}


def latest_eval_result_path(results_dir: Path, task: str, eval_model: str) -> Path | None:
    """与 eval.evaluator 输出一致：eval_result_{task}_{eval_model}_*.json（取最新修改时间）。"""
    if not results_dir.is_dir():
        return None
    pat = f"eval_result_{task}_{eval_model}_*.json"
    candidates = list(results_dir.glob(pat))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _eval_json_looks_complete(data: dict) -> bool:
    """避免半截/损坏文件被当成已成功。"""
    if not isinstance(data, dict):
        return False
    if data.get("task") is None:
        return False
    if not data.get("articles"):
        return False
    return True


@dataclass(frozen=True)
class EvalRun:
    task: str
    eval_model: str
    sample: int | None
    quick: bool
    dim: tuple[int, ...] | None


def run_generation(
    config_path: Path,
    task: str | None,
    variant: str | None,
    max_workers: int,
    force: bool,
) -> int:
    cmd = [sys.executable, str(ROOT / "batch_run" / "run_generation.py"), "--config", str(config_path)]
    if task:
        cmd += ["--task", task]
    if variant:
        cmd += ["--variant", variant]
    if max_workers and max_workers != 1:
        cmd += ["--max-workers", str(max_workers)]
    if force:
        cmd += ["--force"]
    return subprocess.call(cmd, cwd=str(ROOT), env={**os.environ})


def run_one_eval(
    run: EvalRun,
    results_dir: Path,
) -> list[Path]:
    before = _list_json_results(results_dir)
    cmd = [sys.executable, "-m", "eval.evaluator", "--task", run.task, "--eval-model", run.eval_model]
    if run.quick:
        cmd.append("--quick")
    if run.sample is not None:
        cmd += ["--sample", str(run.sample)]
    if run.dim:
        cmd += ["--dim", *[str(d) for d in run.dim]]

    subprocess.run(cmd, cwd=str(ROOT / "eval-survey"), env={**os.environ}, check=True)

    after = _list_json_results(results_dir)
    new_files = sorted(after - before, key=lambda p: p.stat().st_mtime, reverse=True)
    # evaluator 可能同时写 json+md，这里只取 json；且只保留最新的一份 json
    return new_files[:1]


def _safe_get(d: dict, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def build_summary_rows(result_json: dict) -> list[dict]:
    task = result_json.get("task")
    eval_model = result_json.get("eval_model", "")
    dims = result_json.get("dimensions_evaluated", [])
    articles = result_json.get("articles", [])
    rows: list[dict] = []

    obj = result_json.get("objective_scores", {}) or {}
    for article in articles:
        row = {
            "task": task,
            "eval_model": eval_model,
            "dims": ",".join(str(x) for x in dims),
            "article": article,
            "citation_relevance_score": "",
            "content_accuracy_score": "",
            "total_score": "",
        }
        cr = _safe_get(obj, article, "citation_relevance")
        if isinstance(cr, dict):
            row["citation_relevance_score"] = cr.get("score", "")
            row["citation_total_citations"] = cr.get("total_citations", "")
            row["citation_key_refs_total"] = cr.get("key_refs_total", "")
            row["citation_key_refs_covered"] = cr.get("key_refs_covered", "")
            row["citation_coverage_rate"] = cr.get("coverage_rate", "")
        ca = _safe_get(obj, article, "content_accuracy")
        if isinstance(ca, dict):
            row["content_accuracy_score"] = ca.get("score", "")
            row["content_accuracy_total_citations"] = ca.get("total_citations", "")
            row["content_accuracy_verified_citations"] = ca.get("verified_citations", "")
            row["content_accuracy_hallucination_count"] = ca.get("hallucination_count", "")

        # 若 evaluator 输出了 total_scores（维度3/4时），一并收集
        total_scores = _safe_get(result_json, "summary", "total_scores", default={})
        if isinstance(total_scores, dict) and article in total_scores:
            row["total_score"] = total_scores.get(article, "")

        rows.append(row)

    return rows


def write_csv(rows: Iterable[dict], out_path: Path) -> None:
    rows = list(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        out_path.write_text("", encoding="utf-8")
        return
    # union fieldnames
    fieldnames: list[str] = []
    seen = set()
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                fieldnames.append(k)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    p = argparse.ArgumentParser(description="全自动批量评测（生成→评测→汇总）")
    p.add_argument("--config", type=Path, default=ROOT / "batch_run" / "config.yaml")
    p.add_argument("--task", type=str, default=None, help="只跑指定任务")
    p.add_argument("--variant", type=str, default=None, help="只跑指定变体（生成侧）")
    p.add_argument("--eval-model", type=str, default=None, help="只跑指定打分模型")
    p.add_argument("--generate-only", action="store_true")
    p.add_argument("--eval-only", action="store_true")
    p.add_argument("--max-workers", type=int, default=1, help="生成并发数（默认1）")
    p.add_argument("--force-generate", action="store_true", help="生成侧强制重跑")
    p.add_argument("--sample", type=int, default=15, help="eval.evaluator --sample（默认15）")
    p.add_argument("--quick", action="store_true", help="eval.evaluator --quick")
    p.add_argument("--dim", type=int, nargs="*", default=None, help="eval.evaluator --dim，如 1 2 3 4")
    p.add_argument(
        "--resume",
        action="store_true",
        help="评测断点续跑：若 eval-survey/eval/results/ 已有 eval_result_{task}_{eval_model}_*.json "
        "则跳过该组合（取最新文件参与汇总）。换 API Key 后直接加本参数续跑未完成的项。",
    )
    args = p.parse_args()

    cfg = load_yaml(args.config)
    tasks = cfg.get("tasks", [])
    variants = cfg.get("variants", [])
    eval_models = cfg.get("eval_models", [])

    if args.task:
        tasks = [t for t in tasks if t == args.task]
    if args.variant:
        variants = [v for v in variants if v.get("name") == args.variant]
    if args.eval_model:
        eval_models = [m for m in eval_models if m == args.eval_model]

    if not args.eval_only:
        rc = run_generation(
            config_path=args.config,
            task=args.task,
            variant=args.variant,
            max_workers=args.max_workers,
            force=args.force_generate,
        )
        if rc != 0:
            return rc
        if args.generate_only:
            return 0

    # eval
    results_dir = ROOT / "eval-survey" / "eval" / "results"
    out_dir = ROOT / "batch_run" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    manifest: list[dict] = []
    ts = time.strftime("%Y%m%d_%H%M%S")

    for task in tasks:
        for em in eval_models:
            run = EvalRun(
                task=task,
                eval_model=em,
                sample=args.sample if args.sample >= 0 else None,
                quick=bool(args.quick),
                dim=tuple(args.dim) if args.dim else None,
            )
            skipped = False
            result_path: Path | None = None
            if args.resume:
                existing = latest_eval_result_path(results_dir, task, em)
                if existing is not None:
                    try:
                        prev = json.loads(existing.read_text(encoding="utf-8"))
                    except (json.JSONDecodeError, OSError):
                        prev = None
                    if prev is not None and _eval_json_looks_complete(prev):
                        result_path = existing
                        skipped = True
                        print(f"[run_batch] 续跑跳过（已有结果）: {task} + {em} -> {existing.name}")

            if result_path is None:
                new_files = run_one_eval(run, results_dir=results_dir)
                if not new_files:
                    print(f"[run_batch] 警告: 未得到新结果 JSON，跳过汇总行: {task} + {em}")
                    continue
                result_path = new_files[0]

            manifest.append(
                {
                    "task": task,
                    "eval_model": em,
                    "result_json": str(result_path),
                    "skipped": skipped,
                }
            )
            data = json.loads(result_path.read_text(encoding="utf-8"))
            all_rows.extend(build_summary_rows(data))

    manifest_path = out_dir / f"batch_eval_manifest_{ts}.json"
    manifest_path.write_text(json.dumps({"runs": manifest}, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_csv = out_dir / f"batch_eval_summary_{ts}.csv"
    write_csv(all_rows, summary_csv)

    print(f"评测完成。manifest={manifest_path} summary={summary_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

