"""Base Survey - 主入口

支持 cli 和 acp 模式。
"""

import argparse
import asyncio
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except AttributeError:
    pass

from .core.config import load_config, Config

PROJECT_NAME = "Base-Survey"


def setup_workspace(workspace_path: str) -> str:
    workspace = Path(workspace_path).resolve()
    for d in ["survey", "references", "documents", "data"]:
        (workspace / d).mkdir(parents=True, exist_ok=True)
    return str(workspace)


async def run_cli(args):
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown

    from .agents.survey import BaseSurveyAgent

    console = Console()
    config = load_config(args.config) if args.config else Config()
    workspace = setup_workspace(args.workspace)

    console.print(
        Panel.fit(
            f"[bold green]{PROJECT_NAME}[/bold green]\n"
            "基础调研 Agent - 仅文献搜索(Semantic Scholar)与文件系统工具\n\n"
            f"工作空间: {workspace}",
            title="欢迎",
        )
    )

    model_config = config.get_agent_config("survey")
    agent = BaseSurveyAgent(
        model_config=model_config,
        workspace=workspace,
        print_hint_msg=True,
        enable_compress=config.compression.enabled,
        compress_model=config.compression.model,
        max_context_tokens=config.compression.max_context_tokens,
        compress_threshold=config.compression.compress_threshold,
    )

    console.print("\n[bold]输入您的任务（输入 'exit' 退出）：[/bold]\n")

    while True:
        try:
            user_input = console.input("[bold blue]> [/bold blue]").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[yellow]再见！[/yellow]")
                break
            console.print("\n[dim]正在处理...[/dim]\n")
            result = await agent.run(user_input)
            console.print(
                Panel(
                    Markdown(result),
                    title="结果",
                    border_style="green",
                )
            )
            console.print()
        except KeyboardInterrupt:
            console.print("\n[yellow]已中断[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]错误: {e}[/red]")


async def run_acp_server(args):
    log_file = Path(__file__).parent.parent / "logs" / "acp_server.log"
    log_file.parent.mkdir(exist_ok=True)

    import logging

    logging.basicConfig(
        filename=str(log_file),
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    try:
        config = load_config(args.config) if args.config else Config()
        workspace = setup_workspace(args.workspace)
        model_config = config.get_agent_config("survey")

        from .acp.server import ACPServer, BaseSurveyFlowAgent

        def create_agent(client):
            return BaseSurveyFlowAgent(
                client=client,
                model_config=model_config,
                default_workspace=workspace,
                output_language=args.language,
                enable_compress=config.compression.enabled,
                compress_model=config.compression.model,
                max_context_tokens=config.compression.max_context_tokens,
                compress_threshold=config.compression.compress_threshold,
            )

        server = ACPServer(agent_factory=create_agent)
        try:
            print("ACP Server starting (Base-Survey)...", file=sys.stderr)
        except Exception:
            pass
        await server.run()
    except Exception as e:
        logging.error(f"ACP Server 启动失败: {e}", exc_info=True)
        try:
            import traceback
            traceback.print_exc(file=sys.stderr)
        except Exception:
            pass
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Base Survey - 基础调研 Agent"
    )
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        default="./workspace",
        help="工作区目录路径",
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="./etc/config.yaml",
        help="配置文件路径 (YAML)",
    )
    parser.add_argument(
        "--language", "-l",
        type=str,
        choices=["English", "Chinese"],
        default="Chinese",
        help="输出语言",
    )
    parser.add_argument(
        "--mode", "-m",
        type=str,
        choices=["cli", "acp"],
        default="cli",
        help="运行模式: cli / acp",
    )

    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        project_root = Path(__file__).parent.parent
        config_path = project_root / args.config
    if config_path.exists():
        args.config = str(config_path)
    else:
        args.config = None

    if args.mode == "acp":
        asyncio.run(run_acp_server(args))
    else:
        asyncio.run(run_cli(args))


if __name__ == "__main__":
    main()
