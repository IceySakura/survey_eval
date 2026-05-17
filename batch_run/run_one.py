#!/usr/bin/env python3
"""单次运行：选一组消融配置，跑完整流程（生成 → 复制 → 评测）

用法:
  python run_one.py --task sudamuon --variant base_gpt51
  python run_one.py --task sudamuon --variant base_gpt51 --model gpt-4o  # 覆盖模型名
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def _apply_env_file(path: Path, *, override: bool = False) -> None:
    """KEY=VALUE 行写入 os.environ；override=False 时仅填充未设置或为空的变量。"""
    import os

    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        k = k.strip()
        v = v.strip().strip("'").strip('"')
        if not k:
            continue
        if override or (k not in os.environ or not os.environ.get(k)):
            os.environ[k] = v


def _load_dotenv_if_present() -> None:
    """eval-survey/.env 先加载，再 batch_run/.env（后者覆盖，与 eval.evaluator 一致）"""
    _apply_env_file(ROOT / "eval-survey" / ".env", override=False)
    _apply_env_file(ROOT / "batch_run" / ".env", override=True)


def get_plan_for_agent(plan_path: Path) -> str:
    import re
    text = plan_path.read_text(encoding="utf-8")
    match = re.search(r"\n## Key Reference[s]?\s*\n", text, re.IGNORECASE)
    if match:
        return text[: match.start()].rstrip()
    return text.rstrip()


def load_batch_config(config_path: Path) -> dict:
    import yaml
    if not config_path.exists():
        return {}
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _model_uses_aihubmix(model: str) -> bool:
    """非 OpenAI/Codex 主力 GPT 线路的模型（DeepSeek、Claude 等）走 AIHubMix 兼容端。"""
    m = (model or "").lower()
    return any(
        x in m
        for x in (
            "deepseek",
            "sonnet",
            "claude",
            "anthropic",
            "gemini",
            "moonshot",
        )
    )


def _subprocess_env_for_llm(model: str, api_base_url: str | None = None, api_key: str | None = None) -> dict:
    """子进程环境：AIHubMix 模型注入 OPENAI_*，供 agentscope/base 的 APIConfig 读取。"""
    env = {**os.environ}
    if api_base_url and api_key:
        env["OPENAI_BASE_URL"] = api_base_url
        env["OPENAI_API_KEY"] = api_key
        print(f"[run_one] LLM 子进程已切换为自定义 API（{api_base_url}）")
        return env
    if not _model_uses_aihubmix(model):
        return env
    key = (os.environ.get("AIHUBMIX_API_KEY") or "").strip()
    base = (os.environ.get("AIHUBMIX_BASE_URL") or "").strip()
    if not key or not base:
        print(
            "[run_one] 警告: 当前模型应走 AIHubMix，但未设置 AIHUBMIX_API_KEY 或 "
            "AIHUBMIX_BASE_URL；仍将使用 CODEX/OPENAI，可能对 deepseek/sonnet 报 "
            "`no clients available`"
        )
        return env
    env["OPENAI_API_KEY"] = key
    env["OPENAI_BASE_URL"] = base
    print(f"[run_one] LLM 子进程已切换为 AIHubMix（模型: {model}）")
    return env


def update_config_model(
    config_path: Path,
    model: str,
    agent_type: str = "base",
    retrieval_mode: str | None = None,
    api_base_url: str | None = None,
    api_key: str | None = None,
) -> None:
    import yaml
    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if "agents" not in data:
        data["agents"] = {}
    for key in ["survey", "survey_auto"] if agent_type == "ag" else ["survey"]:
        if key not in data["agents"]:
            data["agents"][key] = {}
        data["agents"][key]["model"] = model
    if retrieval_mode and "paper_database" in data:
        data["paper_database"]["retrieval_mode"] = retrieval_mode
    if api_base_url:
        if "api" not in data:
            data["api"] = {}
        data["api"]["base_url"] = api_base_url
    if api_key:
        if "api" not in data:
            data["api"] = {}
        data["api"]["api_key"] = api_key
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def run_agentscope_survey(
    workspace: Path,
    config_path: Path,
    plan_path: Path,
    auto: bool = False,
    min_citations: int = 30,
    llm_model: str = "",
    api_base_url: str | None = None,
    api_key: str | None = None,
) -> bool:
    """通过 subprocess 调用 agentscope-survey CLI"""
    import subprocess
    base_dir = ROOT / "agentscope-survey"
    venv_python = base_dir / ".venv" / "bin" / "python"
    if not venv_python.exists():
        venv_python = sys.executable
    # CLI 的 console.input() 每次只读一行！不能直接传多行 plan。
    # 改为：plan 已写入 workspace/documents/writing_plan.md，只传一行指令让 agent 读文件并执行
    read_plan = "请先调用 read_file 读取 documents/writing_plan.md 获取完整写作计划。"
    hint = f"生成 related works 时请显式传参 min_citations={min_citations}（小规模测试可用较小值以加速）。"
    if auto:
        prompt = f"{read_plan} {hint} 然后按 plan 要求依次调用 survey_write_outline、survey_write_survey、survey_write_related_works，必须完成三步，将 related_works.tex 和 references.bib 输出到 survey/ 目录。\nexit\n"
    else:
        prompt = f"{read_plan} {hint} 然后按 plan 要求依次调用 survey_write_outline、survey_write_survey、survey_write_related_works，必须完成三步，将 related_works.tex 和 references.bib 输出到 survey/ 目录。\nexit\n"
    cmd = [str(venv_python), "-m", "agentscope_survey", "--mode", "cli", "-w", str(workspace), "-c", str(config_path)]
    if auto:
        cmd.append("--auto")
    # 不捕获 stdout，让外层（run_generation 的日志重定向）实时拿到输出，便于观察卡点
    proc = subprocess.Popen(
        cmd,
        cwd=str(base_dir),
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=_subprocess_env_for_llm(llm_model, api_base_url, api_key),
    )
    try:
        assert proc.stdin is not None
        proc.stdin.write(prompt)
        proc.stdin.flush()
        proc.stdin.close()
        proc.wait(timeout=900)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=30)
        print("[run_one] Agent 超时（900s），已终止进程")
    return proc.returncode == 0


def run_base_survey(
    workspace: Path,
    config_path: Path,
    plan_path: Path,
    min_citations: int = 30,
    llm_model: str = "",
    api_base_url: str | None = None,
    api_key: str | None = None,
) -> bool:
    """通过 subprocess 调用 base-survey CLI（单条指令驱动工具链）"""
    import subprocess
    base_dir = ROOT / "base-survey"
    venv_python = base_dir / ".venv" / "bin" / "python"
    if not venv_python.exists():
        venv_python = sys.executable  # fallback
    # base-survey 没有 survey_* 工具；必须走 literature_search + write_file 路径
    read_plan = "请先调用 read_file 读取 documents/writing_plan.md 获取完整写作计划。"
    hint = (
        "请使用 literature_search/literature_get_references/literature_get_citations 做文献调研，"
        "并使用 write_file 直接写出最终文件。"
    )
    prompt = (
        f"{read_plan} {hint} "
        "请直接产出并写入这两个文件："
        "survey/related_works.tex 和 survey/references.bib。"
        f" related works 目标引用数不少于 {min_citations}（小规模测试阈值）。\n"
        "exit\n"
    )
    # 传入 plan + exit，让 CLI 执行一次后退出
    proc = subprocess.Popen(
        [
            str(venv_python), "-m", "base_survey",
            "--mode", "cli",
            "-w", str(workspace),
            "-c", str(config_path),
        ],
        cwd=str(base_dir),
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=_subprocess_env_for_llm(llm_model, api_base_url, api_key),
    )
    try:
        assert proc.stdin is not None
        proc.stdin.write(prompt)
        proc.stdin.flush()
        proc.stdin.close()
        proc.wait(timeout=600)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=30)
        print("[run_one] base-survey 超时（600s），已终止进程")
        return False
    else:
        return proc.returncode == 0


def main():
    _load_dotenv_if_present()
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", default="sudamuon")
    parser.add_argument("--variant", default="base_gpt51")
    parser.add_argument("--config", type=Path, default=ROOT / "batch_run" / "config.yaml", help="批量配置文件（用于读取 eval_models 默认值）")
    parser.add_argument("--model", default=None, help="覆盖模型名，如 gpt-4o")
    parser.add_argument("--skip-eval", action="store_true", help="跳过评测")
    parser.add_argument(
        "--min-citations",
        type=int,
        default=30,
        help="related works 目标最小引用数",
    )
    parser.add_argument("--eval-model", default=None, help="评测模型别名或真实模型名；不传则使用 config 中 eval_models")
    parser.add_argument("--sample", type=int, default=5, help="评测抽样数（默认5）")
    parser.add_argument("--quick", action="store_true", help="评测 quick 模式（跳过维度1）")
    parser.add_argument("--dim", type=int, nargs="*", default=None, help="评测维度，如 --dim 1 2")
    parser.add_argument("--retrieval-mode", default=None, choices=["basic", "enhanced"], help="检索模式（仅 reasflow 有效）")
    parser.add_argument("--api-base-url", default=None, help="覆盖 agent config 的 api.base_url")
    parser.add_argument("--api-key", default=None, help="覆盖 agent config 的 api.api_key")
    args = parser.parse_args()

    sources_dir = ROOT / "eval-survey" / "sources"
    plan_path = sources_dir / args.task / "survey_plan.md"
    if not plan_path.exists():
        print(f"错误: {plan_path} 不存在")
        return 1

    plan_for_agent = get_plan_for_agent(plan_path)
    print(f"[run_one] Plan 长度: {len(plan_for_agent)} 字符")

    def _is_agentscope_variant(v: str) -> bool:
        return v.startswith("reasflow_") or v.startswith("ag_")

    # variant → model 映射
    VARIANT_MODEL = {
        "base_gpt51": "gpt-5.1",
        "base_gpt54": "gpt-5.4",
        "base_dpsk": "deepseek-v3.2",
        "base_sonnet4.6": "claude-sonnet-4-6",
        "reasflow_gpt51": "gpt-5.1",
        "reasflow_gpt54": "gpt-5.4",
        "reasflow_dpsk": "deepseek-v3.2",
        "reasflow_sonnet4.6": "claude-sonnet-4-6",
        "reasflow_basic_gpt54": "gpt-5.4",
        "reasflow_enhanced_gpt54": "gpt-5.4",
        "ag_chat_gpt51": "gpt-5.1",
        "ag_chat_gpt54": "gpt-5.4",
        "ag_auto_gpt51": "gpt-5.1",
        "ag_auto_gpt54": "gpt-5.4",
    }
    model = args.model or VARIANT_MODEL.get(args.variant, "gpt-4o")

    min_citations = args.min_citations

    # 选择 agent + 隔离 workspace（按 task/variant 独立目录，避免残留）
    if args.variant.startswith("base_"):
        agent_dir = ROOT / "base-survey"
        config_path = agent_dir / "etc" / "config.yaml"
        workspace = agent_dir / "workspace_runs" / args.task / args.variant
    elif _is_agentscope_variant(args.variant):
        agent_dir = ROOT / "agentscope-survey"
        config_path = agent_dir / "etc" / "config.yaml"
        workspace = agent_dir / "workspace_runs" / args.task / args.variant
    else:
        print("暂只支持 base_*、reasflow_* variant（ag_* 仅兼容旧名）")
        return 1

    # 修改 config
    agent_type = "ag" if _is_agentscope_variant(args.variant) else "base"
    update_config_model(
        config_path, model, agent_type,
        retrieval_mode=args.retrieval_mode,
        api_base_url=args.api_base_url,
        api_key=args.api_key,
    )
    print(f"[run_one] Config 已更新: model={model}" +
          (f", retrieval_mode={args.retrieval_mode}" if args.retrieval_mode else "") +
          (f", api_base_url={args.api_base_url}" if args.api_base_url else ""))

    survey_dir = workspace / "survey"

    if args.variant.startswith("base_"):
        if workspace.exists():
            shutil.rmtree(workspace)
        (workspace / "survey").mkdir(parents=True, exist_ok=True)
        plan_file = workspace / "documents" / "writing_plan.md"
        plan_file.parent.mkdir(parents=True, exist_ok=True)
        plan_file.write_text(plan_for_agent, encoding="utf-8")
        run_base_survey(
            workspace,
            config_path,
            plan_file,
            min_citations=min_citations,
            llm_model=model,
            api_base_url=args.api_base_url,
            api_key=args.api_key,
        )
    else:
        if workspace.exists():
            shutil.rmtree(workspace)
        (workspace / "survey").mkdir(parents=True, exist_ok=True)
        plan_file = workspace / "documents" / "writing_plan.md"
        plan_file.parent.mkdir(parents=True, exist_ok=True)
        plan_file.write_text(plan_for_agent, encoding="utf-8")
        # reasflow / ag_*：批量一律 CLI --auto（Reasoning/AutoSurvey 多步）
        run_agentscope_survey(
            workspace,
            config_path,
            plan_file,
            auto=True,
            min_citations=min_citations,
            llm_model=model,
            api_base_url=args.api_base_url,
            api_key=args.api_key,
        )

    # 检查输出：必须由 agent 直接生成最终结果（不做补生成兜底）
    tex_path = survey_dir / "related_works.tex"
    bib_path = survey_dir / "references.bib"
    if not tex_path.exists() or not bib_path.exists():
        print(f"[run_one] 未找到输出: related_works.tex={tex_path.exists()}, references.bib={bib_path.exists()}")
        ls = list(survey_dir.iterdir()) if survey_dir.exists() else []
        print(f"  workspace/survey 内容: {[p.name for p in ls]}")
        return 1

    # 复制到 eval
    dest_dir = sources_dir / args.task / args.variant
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(tex_path, dest_dir / "related_works.tex")
    shutil.copy2(bib_path, dest_dir / "references.bib")
    print(f"[run_one] 已复制到 {dest_dir}")

    # 评测
    if not args.skip_eval:
        import subprocess
        cfg = load_batch_config(args.config)
        eval_models = [args.eval_model] if args.eval_model else cfg.get("eval_models", [])
        if not eval_models:
            eval_models = ["dpsk"]  # 最后兜底

        for em in eval_models:
            eval_cmd = [
                sys.executable, "-m", "eval.evaluator",
                "--task", args.task,
                "--eval-model", em,
                "--sample", str(args.sample),
            ]
            if args.quick:
                eval_cmd.append("--quick")
            if args.dim:
                eval_cmd += ["--dim", *[str(x) for x in args.dim]]

            print(f"[run_one] 运行评测: {' '.join(eval_cmd)}")
            subprocess.run(
                eval_cmd,
                cwd=str(ROOT / "eval-survey"),
                env={**__import__("os").environ, "PATH": __import__("os").environ.get("PATH", "")},
            )

    print("[run_one] 完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
