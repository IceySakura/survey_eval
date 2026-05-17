"""CompressedMemory - 带上下文压缩功能的 Memory 类"""

import re
from typing import Any, Callable, Optional, Union, Iterable

from agentscope.memory import MemoryBase
from agentscope.message import Msg

try:
    import tiktoken
    _tokenizer = tiktoken.get_encoding("cl100k_base")
except ImportError:
    tiktoken = None
    _tokenizer = None

COMPRESS_TOKEN_THRESHOLD = 0.7
COMPRESS_PRESERVE_THRESHOLD = 0.3

COMPRESS_SYSTEM_PROMPT = """
You are the component that summarizes internal chat history into a structured state snapshot.

When the conversation history grows too large, you will be invoked to distill the entire history into a concise, structured XML snapshot. This snapshot is CRITICAL, as it will become the agent's *only* memory of the past.

First, you will think through the entire history in a private <scratchpad>. Review the user's overall goal, the agent's actions, tool outputs, file modifications, and any unresolved questions.

After your reasoning is complete, generate the final <state_snapshot> XML object.

The structure MUST be as follows:

<state_snapshot>
    <overall_goal>
        <!-- A single, concise sentence describing the user's high-level objective. -->
    </overall_goal>

    <key_knowledge>
        <!-- Crucial facts, conventions, and constraints the agent must remember. -->
    </key_knowledge>

    <file_system_state>
        <!-- List files that have been created, read, modified, or deleted. -->
    </file_system_state>

    <recent_actions>
        <!-- A summary of the last few significant agent actions and their outcomes. -->
    </recent_actions>

    <current_plan>
        <!-- The agent's step-by-step plan. Mark completed steps. -->
    </current_plan>

    <errors_and_issues>
        <!-- Any errors encountered and their resolutions, or unresolved issues. -->
    </errors_and_issues>
</state_snapshot>
""".strip()

COMPRESS_USER_PROMPT = """Please analyze the following conversation history and generate a structured state snapshot.

First, reason in your <scratchpad> about what information is critical to preserve.
Then, generate the <state_snapshot> XML with all essential details.

Conversation history:
{text}
"""


def count_tokens(text: str) -> int:
    if _tokenizer is not None:
        return len(_tokenizer.encode(text))
    return len(text) // 3


def msg_to_text(msg: Msg) -> str:
    content = msg.content
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        parts = []
        for block in content:
            if hasattr(block, "text"):
                parts.append(block.text)
            elif isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
            else:
                parts.append(str(block))
        return "\n".join(parts)
    return str(content)


def extract_state_snapshot(text: str) -> str:
    match = re.search(r"<state_snapshot>(.*?)</state_snapshot>", text, re.DOTALL)
    if match:
        return f"<state_snapshot>{match.group(1)}</state_snapshot>"
    return text


class CompressedMemory(MemoryBase):
    """带上下文压缩功能的 Memory 类"""

    def __init__(
        self,
        max_tokens: int = 200000,
        compress_threshold: float = COMPRESS_TOKEN_THRESHOLD,
        preserve_threshold: float = COMPRESS_PRESERVE_THRESHOLD,
        compress_model: str = "gpt-4o-mini",
        compress_callback: Optional[Callable[[str], None]] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.content: list[Msg] = []
        self.max_tokens = max_tokens
        self.compress_threshold = compress_threshold
        self.preserve_threshold = preserve_threshold
        self.compress_model = compress_model
        self.compress_callback = compress_callback
        self.api_key = api_key
        self.base_url = base_url
        self._state_snapshot: Optional[str] = None
        self._current_tokens = 0
        self._compression_count = 0

    def state_dict(self) -> dict:
        return {
            "content": [_.to_dict() for _ in self.content],
            "state_snapshot": self._state_snapshot,
            "current_tokens": self._current_tokens,
            "compression_count": self._compression_count,
        }

    def load_state_dict(self, state_dict: dict, strict: bool = True) -> None:
        self.content = []
        for data in state_dict.get("content", []):
            data.pop("type", None)
            self.content.append(Msg.from_dict(data))
        self._state_snapshot = state_dict.get("state_snapshot")
        self._current_tokens = state_dict.get("current_tokens", 0)
        self._compression_count = state_dict.get("compression_count", 0)

    async def size(self) -> int:
        return len(self.content)

    async def retrieve(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError(
            "The retrieve method is not implemented in CompressedMemory."
        )

    async def delete(
        self,
        msg_ids: list[str],
        **kwargs: Any,
    ) -> int:
        """按消息 ID 删除。兼容 MemoryBase 接口。"""
        msg_id_set = set(msg_ids)
        initial_size = len(self.content)
        self.content = [msg for msg in self.content if msg.id not in msg_id_set]
        self._recalculate_tokens()
        return initial_size - len(self.content)

    async def add(
        self,
        memories: Union[list[Msg], Msg, None],
        marks: str | list[str] | None = None,
        allow_duplicates: bool = False,
        **kwargs: Any,
    ) -> None:
        if memories is None:
            return
        if isinstance(memories, Msg):
            memories = [memories]
        if not isinstance(memories, list):
            raise TypeError(
                f"memories should be a list of Msg or a single Msg, got {type(memories)}."
            )
        for msg in memories:
            if not isinstance(msg, Msg):
                raise TypeError(
                    f"memories should be a list of Msg or a single Msg, got {type(msg)}."
                )
        if not allow_duplicates:
            existing_ids = [_.id for _ in self.content]
            memories = [_ for _ in memories if _.id not in existing_ids]
        new_tokens = sum(count_tokens(msg_to_text(msg)) for msg in memories)
        self._current_tokens += new_tokens
        self.content.extend(memories)
        threshold_tokens = int(self.max_tokens * self.compress_threshold)
        if self._current_tokens > threshold_tokens:
            await self._compress()

    async def delete_by_mark(
        self,
        mark: str | list[str],
        *args: Any,
        **kwargs: Any,
    ) -> int:
        """按 mark 删除消息。本实现不使用 mark 系统，无操作返回 0。"""
        return 0

    async def get_memory(
        self,
        mark: str | None = None,
        exclude_mark: str | None = None,
        prepend_summary: bool = True,
        **kwargs: Any,
    ) -> list[Msg]:
        """获取记忆。兼容 AgentScope ReActAgent 的 get_memory(exclude_mark=...) 调用。
        本实现不使用 mark 系统，直接返回全部内容。"""
        if self._state_snapshot:
            snapshot_msg = Msg(
                name="user",
                role="user",
                content=self._state_snapshot,
            )
            ack_msg = Msg(
                name="assistant",
                role="assistant",
                content="I've reviewed the state snapshot and understand the context. Let me continue from where we left off.",
            )
            return [snapshot_msg, ack_msg] + self.content
        return self.content

    async def clear(self) -> None:
        self.content = []
        self._state_snapshot = None
        self._current_tokens = 0
        self._compression_count = 0

    def _recalculate_tokens(self) -> None:
        self._current_tokens = sum(
            count_tokens(msg_to_text(msg)) for msg in self.content
        )
        if self._state_snapshot:
            self._current_tokens += count_tokens(self._state_snapshot)

    def _find_compress_split_point(self) -> int:
        if not self.content:
            return 0
        preserve_tokens = int(self._current_tokens * self.preserve_threshold)
        tokens_count = 0
        split_point = len(self.content)
        for i in range(len(self.content) - 1, -1, -1):
            msg_tokens = count_tokens(msg_to_text(self.content[i]))
            if tokens_count + msg_tokens > preserve_tokens:
                break
            tokens_count += msg_tokens
            split_point = i
        return split_point

    async def _compress(self) -> None:
        if len(self.content) < 4:
            return
        if self.compress_callback:
            self.compress_callback("正在压缩上下文，生成结构化状态快照...")
        split_point = self._find_compress_split_point()
        if split_point == 0:
            if self.compress_callback:
                self.compress_callback("消息都在保留范围内，跳过压缩")
            return
        compress_msgs = self.content[:split_point]
        keep_msgs = self.content[split_point:]
        compress_text = self._format_messages_for_compression(compress_msgs)
        new_snapshot = await self._call_compress_model(compress_text)
        self._state_snapshot = new_snapshot
        self.content = keep_msgs
        self._compression_count += 1
        self._recalculate_tokens()
        if self.compress_callback:
            self.compress_callback(
                f"上下文压缩完成 (第 {self._compression_count} 次)，"
                f"当前 token 数: {self._current_tokens}"
            )

    def _format_messages_for_compression(self, messages: list[Msg]) -> str:
        parts = []
        if self._state_snapshot:
            parts.append("[Previous State Snapshot]")
            parts.append(self._state_snapshot)
            parts.append("\n[New Conversation Since Last Snapshot]")
        for msg in messages:
            role = msg.role or "unknown"
            name = msg.name or role
            content = msg_to_text(msg)
            if len(content) > 2000:
                content = content[:2000] + "\n... [truncated]"
            parts.append(f"[{name}({role})]: {content}")
        return "\n\n".join(parts)

    async def _call_compress_model(self, text: str) -> str:
        import openai

        client = openai.AsyncClient(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        prompt = COMPRESS_USER_PROMPT.replace("{text}", text)
        try:
            response = await client.chat.completions.create(
                model=self.compress_model,
                messages=[
                    {"role": "system", "content": COMPRESS_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
            )
            result = response.choices[0].message.content.strip()
            return extract_state_snapshot(result)
        except Exception as e:
            if self.compress_callback:
                self.compress_callback(f"压缩模型调用失败: {e}，使用简单截断")
            return self._generate_fallback_snapshot(text)

    def _generate_fallback_snapshot(self, text: str) -> str:
        if len(text) > 1500:
            truncated = (
                text[:750] + "\n\n... [content truncated] ...\n\n" + text[-750:]
            )
        else:
            truncated = text
        return f"""<state_snapshot>
    <overall_goal>
        [Unable to generate - compression model failed]
    </overall_goal>

    <key_knowledge>
        - Compression failed, using simple truncation
        - Original conversation length: {len(text)} characters
    </key_knowledge>

    <file_system_state>
        [See truncated conversation below]
    </file_system_state>

    <recent_actions>
        [Truncated conversation summary]
        {truncated}
    </recent_actions>

    <current_plan>
        [Continue from recent actions]
    </current_plan>

    <errors_and_issues>
        - Compression model call failed
    </errors_and_issues>
</state_snapshot>"""
