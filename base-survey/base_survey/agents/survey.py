"""Base Survey Agent - 仅文献搜索(Semantic Scholar)与文件系统工具"""

from typing import Any, Callable, Dict, Optional

from agentscope.agent import ReActAgent
from agentscope.message import Msg

from .base import create_react_agent, content_to_str
from ..prompts.survey import get_base_survey_system_prompt
from ..tools.file_tools import create_file_tools
from ..tools.literature_tools import create_literature_tools
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseSurveyAgent:
    """Base Survey Agent

    仅整合文件系统工具和文献搜索工具（Semantic Scholar）。
    无 AutoSurvey、无 websearch、无 skill 工具。
    系统提示词仅包含工具说明，无角色指定。
    """

    def __init__(
        self,
        model_config: Dict[str, Any],
        workspace: str,
        print_hint_msg: bool = True,
        tool_call_callback: Optional[Callable] = None,
        compress_callback: Optional[Callable] = None,
        thinking_callback: Optional[Callable] = None,
        text_callback: Optional[Callable] = None,
        enable_compress: bool = True,
        compress_model: str = "gpt-4o-mini",
        max_context_tokens: int = 200000,
        compress_threshold: float = 0.7,
    ):
        self.model_config = model_config
        self.workspace = workspace
        self.print_hint_msg = print_hint_msg
        self.tool_call_callback = tool_call_callback
        self.compress_callback = compress_callback
        self.thinking_callback = thinking_callback
        self.text_callback = text_callback
        self.enable_compress = enable_compress
        self.compress_model = compress_model
        self.max_context_tokens = max_context_tokens
        self.compress_threshold = compress_threshold

        self.system_prompt = get_base_survey_system_prompt(workspace=workspace)

        all_tools = []
        all_tools.extend(create_file_tools(workspace))
        all_tools.extend(create_literature_tools())

        self.agent: ReActAgent = create_react_agent(
            name="BaseSurveyAgent",
            system_prompt=self.system_prompt,
            tool_funcs=all_tools,
            model_config=self.model_config,
            max_iters=500,
            print_hint_msg=self.print_hint_msg,
            tool_call_callback=self.tool_call_callback,
            compress_callback=self.compress_callback,
            thinking_callback=self.thinking_callback,
            text_callback=self.text_callback,
            enable_compress=self.enable_compress,
            compress_model=self.compress_model,
            max_context_tokens=self.max_context_tokens,
            compress_threshold=self.compress_threshold,
        )

        logger.info(f"BaseSurveyAgent 初始化完成，工作空间: {workspace}")

    async def run(self, prompt: str) -> str:
        """执行任务"""
        logger.info(f"开始执行任务: {prompt[:100]}...")
        user_msg = Msg(name="user", role="user", content=prompt)
        result = await self.agent.reply(user_msg)
        response = content_to_str(result.content) if result else "任务执行完成"
        logger.info(f"任务执行完成，响应长度: {len(response)}")
        return response
