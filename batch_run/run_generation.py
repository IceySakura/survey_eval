#!/usr/bin/env python3
"""批量生成 Related Works（全自动）

该脚本会读取 `batch_run/config.yaml`，对每个 (task, variant) 组合调用 `batch_run/run_one.py`
完成生成并复制产物到 `eval-survey/sources/{task}/{variant}/`。

用法：
  python batch_run/run_generation.py
  python batch_run/run_generation.py --task sudamuon
  python batch_run/run_generation.py --variant base_gpt51
  python batch_run/run_generation.py --dry-run
  python batch_run/run_generation.py --max-workers 2 --force
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

# 添加项目根目录
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from batch_run.utils.plan_utils import get_plan_for_agent


def load_config(config_path: Path) -> dict:
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _has_outputs(eval_sources: Path, task: str, variant_name: str) -> bool:
    tex = eval_sources / task / variant_name / "related_works.tex"
    bib = eval_sources / task / variant_name / "references.bib"
    return tex.exists() and bib.exists() and tex.stat().st_size > 0 and bib.stat().st_size > 0


def _run_one(
    task: str,
    variant: str,
    model: str | None,
    log_dir: Path,
) -> dict:
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"gen_{task}__{variant}__{ts}.log"
    cmd = [sys.executable, str(ROOT / "batch_run" / "run_one.py"), "--task", task, "--variant", variant, "--skip-eval"]
    # 小规模/健康检查：可通过环境变量降低 min_citations
    if os.getenv("BATCH_MIN_CITATIONS"):
        cmd += ["--min-citations", os.getenv("BATCH_MIN_CITATIONS")]
    if model:
        cmd += ["--model", model]

    started_at = time.time()
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"[cmd] {' '.join(cmd)}\n\n")
        f.flush()
        proc = subprocess.Popen(
            cmd,
            cwd=str(ROOT),
            stdout=f,
            stderr=subprocess.STDOUT,
            text=True,
            env={**os.environ},
        )
        rc = proc.wait()
    return {
        "task": task,
        "variant": variant,
        "model": model,
        "returncode": rc,
        "log_path": str(log_path),
        "elapsed_s": round(time.time() - started_at, 2),
    }


def main():
    parser = argparse.ArgumentParser(description="批量生成 Related Works")
    parser.add_argument("--config", type=Path, default=ROOT / "batch_run" / "config.yaml")
    parser.add_argument("--task", type=str, help="只跑指定任务")
    parser.add_argument("--variant", type=str, help="只跑指定变体")
    parser.add_argument("--dry-run", action="store_true", help="仅打印计划，不执行")
    parser.add_argument("--max-workers", type=int, default=1, help="并发数（默认1）")
    parser.add_argument("--force", action="store_true", help="即使已有产物也强制重跑")
    parser.add_argument("--log-dir", type=Path, default=ROOT / "batch_run" / "logs", help="日志目录")

    args = parser.parse_args()
    config = load_config(args.config)
    paths = config.get("paths", {})
    tasks = config.get("tasks", [])
    variants = config.get("variants", [])

    if args.task:
        tasks = [t for t in tasks if t == args.task]
    if args.variant:
        variants = [v for v in variants if v["name"] == args.variant]

    eval_sources = ROOT / paths.get("eval_sources", "eval-survey/sources")

    if args.dry_run:
        print("=== 批量生成计划 (dry-run) ===\n")
        for task in tasks:
            plan_path = eval_sources / task / "survey_plan.md"
            if not plan_path.exists():
                print(f"  [SKIP] {task}: survey_plan.md 不存在")
                continue
            plan_preview = get_plan_for_agent(plan_path)[:200] + "..."
            print(f"  Task: {task}")
            for v in variants:
                cfg = v.get("config", "survey")
                print(f"    -> {v['name']} (agent={v['agent']}, config={cfg}, model={v.get('model')})")
            print()
        return

    # 任务清单
    jobs: list[tuple[str, dict]] = []
    for task in tasks:
        plan_path = eval_sources / task / "survey_plan.md"
        if not plan_path.exists():
            print(f"[SKIP] {task}: survey_plan.md 不存在")
            continue
        for v in variants:
            jobs.append((task, v))

    if not jobs:
        print("没有可执行的任务（请检查 config.yaml / sources 目录）")
        return

    # 跳过已有产物
    runnable: list[tuple[str, dict]] = []
    skipped = 0
    for task, v in jobs:
        name = v["name"]
        if not args.force and _has_outputs(eval_sources, task, name):
            skipped += 1
            continue
        runnable.append((task, v))

    print(f"=== 批量生成开始 ===")
    print(f"总组合数: {len(jobs)}  将运行: {len(runnable)}  跳过(已有产物): {skipped}")
    print(f"日志目录: {args.log_dir}")
    print("")

    results: list[dict] = []
    if args.max_workers <= 1:
        for task, v in runnable:
            r = _run_one(task=task, variant=v["name"], model=v.get("model"), log_dir=args.log_dir)
            results.append(r)
            status = "OK" if r["returncode"] == 0 else f"FAIL(rc={r['returncode']})"
            print(f"[{status}] {task} / {v['name']}  ({r['elapsed_s']}s)  log={r['log_path']}")
    else:
        with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
            futs = [
                ex.submit(_run_one, task, v["name"], v.get("model"), args.log_dir)
                for task, v in runnable
            ]
            for fut in as_completed(futs):
                r = fut.result()
                results.append(r)
                status = "OK" if r["returncode"] == 0 else f"FAIL(rc={r['returncode']})"
                print(f"[{status}] {r['task']} / {r['variant']}  ({r['elapsed_s']}s)  log={r['log_path']}")

    out_dir = ROOT / "batch_run" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"generation_run_{ts}.json"
    out_path.write_text(json.dumps({"jobs": results}, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = sum(1 for r in results if r["returncode"] == 0)
    fail = sum(1 for r in results if r["returncode"] != 0)
    print("")
    print(f"=== 批量生成完成 === OK={ok} FAIL={fail} 详情: {out_path}")


if __name__ == "__main__":
    main()
