"""Survey Plan 预处理工具

- get_plan_for_agent: 移除 Key References 及之后内容，供 Agent 写作使用
- 评测时使用完整 survey_plan.md（含 Key References）作为 GT
"""

import re
from pathlib import Path
from typing import Optional


def get_plan_for_agent(plan_path: Path) -> str:
    """从 survey_plan.md 中移除 Key References 及之后内容，供 Agent 使用。

    Agent 不应看到 Key References 列表，否则相当于泄露了引用相关性的 GT。
    评测时使用完整 plan 进行 Key References 覆盖检查。

    Args:
        plan_path: survey_plan.md 路径

    Returns:
        不含 Key References 的 plan 文本
    """
    text = plan_path.read_text(encoding="utf-8")
    # 匹配 "## Key References" 或 "## Key Reference" 开头，截断
    match = re.search(r"\n## Key Reference[s]?\s*\n", text, re.IGNORECASE)
    if match:
        return text[: match.start()].rstrip()
    return text.rstrip()


def get_full_plan(plan_path: Path) -> str:
    """获取完整 plan（含 Key References），供评测使用。"""
    return plan_path.read_text(encoding="utf-8").rstrip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python plan_utils.py <survey_plan.md>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    agent_plan = get_plan_for_agent(path)
    print("=== Plan for Agent (no Key References) ===")
    print(agent_plan)
    print("\n--- END ---")
