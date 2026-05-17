"""Agent 工具函数 - 创建 ReActAgent"""

import os
import inspect
import uuid
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Literal

from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel
from agentscope.formatter import OpenAIChatFormatter
from agentscope.tool import Toolkit, ToolResponse
from agentscope.message import TextBlock, Msg
from agentscope.memory import InMemoryMemory

from ..memory import CompressedMemory


class ThinkingModelWrapper:
    """包装 Model，拦截响应并提取 thinking 和 text 内容

    用于 Claude extended thinking / OpenAI reasoning 模型。
    支持 <think> 标签、reasoning_content。
    """

    def __init__(
        self,
        model,
        thinking_callback: Optional[Callable[[str], None]] = None,
        text_callback: Optional[Callable[[str], None]] = None,
    ):
        self._model = model
        self._thinking_callback = thinking_callback or (lambda _: None)
        self._text_callback = text_callback or (lambda _: None)

    async def __call__(self, *args, **kwargs):
        result = self._model(*args, **kwargs)
        if inspect.iscoroutine(result):
            result = await result
        if inspect.isasyncgen(result):
            return self._wrap_stream(result)
        else:
            self._process_response(result)
            return result

    async def _wrap_stream(self, stream):
        last_text = ""
        last_thinking = ""

        def _handle_text(current: str):
            nonlocal last_text
            current = current or ""
            if current.startswith(last_text):
                delta = current[len(last_text):]
            else:
                delta = current
            last_text = current
            if delta and str(delta).strip():
                self._text_callback(str(delta))

        def _handle_thinking(current: str):
            nonlocal last_thinking
            current = current or ""
            if current.startswith(last_thinking):
                delta = current[len(last_thinking):]
            else:
                delta = current
            last_thinking = current
            if delta and str(delta).strip():
                self._thinking_callback(str(delta))

        async for response in stream:
            content = getattr(response, "content", None)
            if isinstance(content, list):
                for block in content:
                    if hasattr(block, "type"):
                        if block.type == "text":
                            _handle_text(getattr(block, "text", ""))
                        elif block.type == "thinking":
                            _handle_thinking(getattr(block, "thinking", ""))
                    elif isinstance(block, dict):
                        if block.get("type") == "text":
                            _handle_text(block.get("text", ""))
                        elif block.get("type") == "thinking":
                            _handle_thinking(block.get("thinking", ""))
                    if hasattr(block, "reasoning_content") and block.reasoning_content:
                        _handle_thinking(str(block.reasoning_content))
            yield response

    def _process_response(self, response):
        content = getattr(response, "content", None)
        all_text = []
        all_thinking = []
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    block_type = block.get("type", "")
                    if block_type == "thinking":
                        all_thinking.append(block.get("thinking", ""))
                    elif block_type == "text":
                        text = block.get("text", "")
                        if text:
                            think_content, plain_text = self._split_think_tags(text)
                            if think_content:
                                all_thinking.append(think_content)
                            if plain_text:
                                all_text.append(plain_text)
                elif hasattr(block, "type"):
                    if block.type == "thinking":
                        all_thinking.append(getattr(block, "thinking", ""))
                    elif block.type == "text":
                        text = getattr(block, "text", "")
                        if text:
                            think_content, plain_text = self._split_think_tags(text)
                            if think_content:
                                all_thinking.append(think_content)
                            if plain_text:
                                all_text.append(plain_text)
                if hasattr(block, "reasoning_content") and block.reasoning_content:
                    all_thinking.append(block.reasoning_content)
        elif isinstance(content, str) and content.strip():
            think_content, plain_text = self._split_think_tags(content)
            if think_content:
                all_thinking.append(think_content)
            if plain_text:
                all_text.append(plain_text)
        if all_thinking:
            self._thinking_callback("\n".join(all_thinking))
        if all_text:
            self._text_callback("\n".join(all_text))

    def _split_think_tags(self, text: str) -> tuple[str, str]:
        """分离 <think> 标签内容和普通文本"""
        import re
        pattern = r"<think>(.*?)</think>"
        matches = re.findall(pattern, text, re.DOTALL)
        thinking = "\n".join(m.strip() for m in matches if m.strip())
        plain = re.sub(pattern, "", text, flags=re.DOTALL).strip()
        return thinking, plain

    def __getattr__(self, name):
        return getattr(self._model, name)


def _get_model_and_formatter(
    model_config: Dict[str, Any],
    api_type: Literal["openai"] = "openai",
):
    api_key = model_config.get("api_key") or os.getenv("OPENAI_API_KEY") or os.getenv("CODEX_API_KEY")
    base_url = model_config.get("base_url")
    model_name = model_config.get("model", "gpt-4o")
    temperature = model_config.get("temperature", 0.7)
    max_tokens = model_config.get("max_tokens", 16384)
    stream = model_config.get("stream", True)
    if base_url and "codex-for.me" in str(base_url):
        stream = True

    model_lower = model_name.lower()
    if any(x in model_lower for x in ["gpt-4o", "gpt-5", "o1", "o3"]):
        token_param = {"max_completion_tokens": max_tokens}
    else:
        token_param = {"max_tokens": max_tokens}

    generate_kwargs = {"temperature": temperature}
    generate_kwargs.update(token_param)

    model = OpenAIChatModel(
        model_name=model_name,
        api_key=api_key,
        client_args={"base_url": base_url, "timeout": 120.0}
        if base_url
        else {"timeout": 120.0},
        generate_kwargs=generate_kwargs,
        stream=stream,
    )
    formatter = OpenAIChatFormatter()
    return model, formatter


def content_to_str(content: Any) -> str:
    """将 Msg.content 转换为字符串，处理 list[ContentBlock] 的情况"""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if hasattr(block, "text"):
                parts.append(block.text)
            elif isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
            elif hasattr(block, "get_text_content"):
                parts.append(block.get_text_content())
            else:
                parts.append(str(block))
        return "\n".join(parts)
    return str(content)


def wrap_tool_func(
    func: Callable,
    tool_call_callback: Optional[Callable] = None,
) -> Callable:
    """包装工具函数"""
    LOG_DIR = os.path.join(os.getcwd(), "logs")
    os.makedirs(LOG_DIR, exist_ok=True)
    MAX_UI_CHARS = 1200

    def _write_tool_log(tool_name: str, tool_call_id: str, status: str, payload: str):
        try:
            log_path = os.path.join(LOG_DIR, f"{tool_name}_{tool_call_id}.log")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[status] {status}\n")
                f.write(payload)
                f.write("\n\n")
        except Exception:
            pass

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            tool_name = func.__name__
            tool_call_id = str(uuid.uuid4())[:8]
            if tool_call_callback:
                tool_call_callback(tool_call_id, tool_name, kwargs, "pending", None)
            _write_tool_log(tool_name, tool_call_id, "pending", f"INPUT:\n{kwargs}")
            try:
                result = await func(*args, **kwargs)
                output_text = (
                    content_to_str(result.content)
                    if isinstance(result, ToolResponse)
                    else (str(result) if result is not None else "")
                )
                _write_tool_log(
                    tool_name, tool_call_id, "completed", f"OUTPUT(full):\n{output_text}"
                )
                ui_text = output_text
                if ui_text and len(ui_text) > MAX_UI_CHARS:
                    ui_text = (
                        ui_text[:MAX_UI_CHARS]
                        + "\n...[输出已截断，查看 logs/ 文件获取完整内容]"
                    )
                if tool_call_callback:
                    tool_call_callback(
                        tool_call_id, tool_name, kwargs, "completed", ui_text
                    )
                if isinstance(result, ToolResponse):
                    return result
                return ToolResponse(content=[TextBlock(type="text", text=output_text)])
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                if tool_call_callback:
                    tool_call_callback(
                        tool_call_id, tool_name, kwargs, "error", error_msg
                    )
                _write_tool_log(tool_name, tool_call_id, "error", f"ERROR:\n{error_msg}")
                return ToolResponse(content=[TextBlock(type="text", text=error_msg)])

        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            tool_name = func.__name__
            tool_call_id = str(uuid.uuid4())[:8]
            if tool_call_callback:
                tool_call_callback(tool_call_id, tool_name, kwargs, "pending", None)
            _write_tool_log(tool_name, tool_call_id, "pending", f"INPUT:\n{kwargs}")
            try:
                result = func(*args, **kwargs)
                output_text = (
                    content_to_str(result.content)
                    if isinstance(result, ToolResponse)
                    else (str(result) if result is not None else "")
                )
                _write_tool_log(
                    tool_name, tool_call_id, "completed", f"OUTPUT(full):\n{output_text}"
                )
                ui_text = output_text
                if ui_text and len(ui_text) > MAX_UI_CHARS:
                    ui_text = (
                        ui_text[:MAX_UI_CHARS]
                        + "\n...[输出已截断，查看 logs/ 文件获取完整内容]"
                    )
                if tool_call_callback:
                    tool_call_callback(
                        tool_call_id, tool_name, kwargs, "completed", ui_text
                    )
                if isinstance(result, ToolResponse):
                    return result
                return ToolResponse(content=[TextBlock(type="text", text=output_text)])
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                if tool_call_callback:
                    tool_call_callback(
                        tool_call_id, tool_name, kwargs, "error", error_msg
                    )
                _write_tool_log(tool_name, tool_call_id, "error", f"ERROR:\n{error_msg}")
                return ToolResponse(content=[TextBlock(type="text", text=error_msg)])

        return sync_wrapper


def create_react_agent(
    name: str,
    system_prompt: str,
    tool_funcs: List[Callable],
    model_config: Dict[str, Any],
    max_iters: int = 500,
    print_hint_msg: bool = True,
    tool_call_callback: Optional[Callable] = None,
    compress_callback: Optional[Callable] = None,
    thinking_callback: Optional[Callable] = None,
    text_callback: Optional[Callable] = None,
    enable_compress: bool = True,
    compress_model: str = "gpt-4o-mini",
    max_context_tokens: int = 200000,
    compress_threshold: float = 0.6,
) -> ReActAgent:
    """创建 ReActAgent 实例"""
    api_type = model_config.get("api_type", "openai")
    model, formatter = _get_model_and_formatter(model_config, api_type)

    model_name = model_config.get("model", "").lower()
    if (
        "thinking" in model_name
        or "reasoning" in model_name
        or thinking_callback
        or text_callback
    ):
        model = ThinkingModelWrapper(model, thinking_callback, text_callback)

    toolkit = Toolkit()
    for func in tool_funcs:
        wrapped_func = wrap_tool_func(func, tool_call_callback)
        toolkit.register_tool_function(wrapped_func)

    if enable_compress:
        memory = CompressedMemory(
            max_tokens=max_context_tokens,
            compress_threshold=compress_threshold,
            compress_model=compress_model,
            compress_callback=compress_callback,
            api_key=model_config.get("api_key"),
            base_url=model_config.get("base_url"),
        )
    else:
        memory = InMemoryMemory()

    agent = ReActAgent(
        name=name,
        sys_prompt=system_prompt,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        memory=memory,
        max_iters=max_iters,
        print_hint_msg=print_hint_msg,
    )

    original_generate_response = agent.generate_response

    def generate_response(response: str, **kwargs):
        safe_response = content_to_str(response)
        return original_generate_response(safe_response, **kwargs)

    agent.generate_response = generate_response
    agent.toolkit.remove_tool_function("generate_response")
    agent.toolkit.register_tool_function(generate_response)

    return agent
