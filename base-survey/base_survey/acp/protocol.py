"""ACP 协议定义 - Zed 兼容的 Agent Communication Protocol"""

from dataclasses import dataclass, field
from typing import Any, Optional, Dict
from enum import Enum
import json
import uuid

MAX_TOOL_OUTPUT_CHARS = 4000


def _truncate_text(text: str, limit: int = MAX_TOOL_OUTPUT_CHARS) -> str:
    if len(text) <= limit:
        return text
    return f"{text[:limit]}\n...[truncated {len(text) - limit} chars]"


@dataclass
class ACPError:
    code: int
    message: str
    data: Optional[Any] = None

    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

    def to_dict(self) -> dict:
        result = {"code": self.code, "message": self.message}
        if self.data is not None:
            result["data"] = self.data
        return result

    @classmethod
    def parse_error(cls, data: Any = None) -> "ACPError":
        return cls(cls.PARSE_ERROR, "Parse error", data)

    @classmethod
    def method_not_found(cls, method: str) -> "ACPError":
        return cls(cls.METHOD_NOT_FOUND, f"Method not found: {method}")

    @classmethod
    def internal_error(cls, data: Any = None) -> "ACPError":
        return cls(cls.INTERNAL_ERROR, "Internal error", data)


@dataclass
class ACPRequest:
    method: str = ""
    params: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    jsonrpc: str = "2.0"

    def to_dict(self) -> dict:
        return {
            "jsonrpc": self.jsonrpc,
            "method": self.method,
            "params": self.params,
            "id": self.id,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=True)

    @classmethod
    def from_dict(cls, data: dict) -> "ACPRequest":
        return cls(
            jsonrpc=data.get("jsonrpc", "2.0"),
            method=data.get("method", ""),
            params=data.get("params", {}),
            id=data.get("id", str(uuid.uuid4())),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "ACPRequest":
        return cls.from_dict(json.loads(json_str))


@dataclass
class ACPResponse:
    result: Optional[Any] = None
    error: Optional[ACPError] = None
    id: Optional[str] = None
    jsonrpc: str = "2.0"

    def to_dict(self) -> dict:
        response = {"jsonrpc": self.jsonrpc, "id": self.id}
        if self.error is not None:
            response["error"] = self.error.to_dict()
        else:
            response["result"] = self.result
        return response

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=True)

    @classmethod
    def success(cls, result: Any, request_id: str) -> "ACPResponse":
        return cls(result=result, id=request_id)

    @classmethod
    def failure(
        cls, error: ACPError, request_id: Optional[str] = None
    ) -> "ACPResponse":
        return cls(error=error, id=request_id)


@dataclass
class ACPNotification:
    method: str = ""
    params: dict = field(default_factory=dict)
    jsonrpc: str = "2.0"

    def to_dict(self) -> dict:
        return {
            "jsonrpc": self.jsonrpc,
            "method": self.method,
            "params": self.params,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=True)


class ACPMethods:
    INITIALIZE = "initialize"
    SESSION_NEW = "session/new"
    SESSION_LOAD = "session/load"
    SESSION_PROMPT = "session/prompt"
    SESSION_CANCEL = "session/cancel"
    AUTHENTICATE = "authenticate"
    SESSION_UPDATE = "session/update"


class SessionUpdateKind(str, Enum):
    AGENT_MESSAGE_CHUNK = "agent_message_chunk"
    AGENT_THOUGHT_CHUNK = "agent_thought_chunk"
    TOOL_CALL = "tool_call"
    TOOL_CALL_UPDATE = "tool_call_update"


@dataclass
class InitializeResult:
    protocol_version: int = 1
    server_info: Dict[str, Any] = field(
        default_factory=lambda: {
            "name": "Base-Survey",
            "version": "1.0.0",
        }
    )
    server_capabilities: Dict[str, Any] = field(
        default_factory=lambda: {
            "streaming": True,
            "tools": True,
        }
    )

    def to_dict(self) -> dict:
        return {
            "protocolVersion": self.protocol_version,
            "serverInfo": self.server_info,
            "serverCapabilities": self.server_capabilities,
        }


@dataclass
class SessionNewResult:
    session_id: str = ""

    def to_dict(self) -> dict:
        return {"sessionId": self.session_id}


@dataclass
class SessionUpdateParams:
    session_id: str = ""
    kind: str = ""
    content: Any = None
    tool_call_id: Optional[str] = None
    tool_name: Optional[str] = None
    tool_status: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_output: Optional[str] = None

    def to_dict(self) -> dict:
        update = {"sessionUpdate": self.kind}
        if self.kind == SessionUpdateKind.AGENT_MESSAGE_CHUNK.value:
            if self.content is not None:
                update["content"] = (
                    {"type": "text", "text": self.content}
                    if isinstance(self.content, str)
                    else self.content
                )
        elif self.kind == SessionUpdateKind.TOOL_CALL.value:
            if self.tool_call_id:
                update["toolCallId"] = self.tool_call_id
            if self.tool_name:
                update["title"] = self.tool_name
            update["kind"] = self._map_tool_kind(self.tool_name) if self.tool_name else "other"
            update["status"] = self.tool_status or "pending"
            update["rawInput"] = self.tool_input or {}
            update["rawOutput"] = {}
            update["content"] = []
            update["locations"] = []
        elif self.kind == SessionUpdateKind.TOOL_CALL_UPDATE.value:
            if self.tool_call_id:
                update["toolCallId"] = self.tool_call_id
            update["status"] = self.tool_status or "completed"
            if self.tool_output is not None:
                update["rawOutput"] = {
                    "result": _truncate_text(self.tool_output)
                }
            if self.content is not None:
                if isinstance(self.content, str):
                    update["content"] = [
                        {
                            "type": "content",
                            "content": {
                                "type": "text",
                                "text": _truncate_text(self.content),
                            },
                        }
                    ]
                elif isinstance(self.content, dict):
                    update["content"] = [self.content]
                else:
                    update["content"] = self.content
        elif self.kind == SessionUpdateKind.AGENT_THOUGHT_CHUNK.value:
            if self.content is not None:
                update["content"] = (
                    {"type": "text", "text": self.content}
                    if isinstance(self.content, str)
                    else self.content
                )
        else:
            if self.content is not None:
                update["content"] = self.content

        return {"sessionId": self.session_id, "update": update}

    def _map_tool_kind(self, tool_name: str) -> str:
        """将工具名映射到 ACP kind 类型"""
        tool_name_lower = tool_name.lower() if tool_name else ""
        if "read" in tool_name_lower:
            return "read"
        elif "write" in tool_name_lower:
            return "edit"
        elif "edit" in tool_name_lower:
            return "edit"
        elif "delete" in tool_name_lower or "remove" in tool_name_lower:
            return "delete"
        elif "list" in tool_name_lower or "search" in tool_name_lower:
            return "search"
        elif "run" in tool_name_lower or "terminal" in tool_name_lower or "exec" in tool_name_lower:
            return "execute"
        elif "think" in tool_name_lower or "plan" in tool_name_lower:
            return "think"
        elif "fetch" in tool_name_lower or "http" in tool_name_lower or "api" in tool_name_lower:
            return "fetch"
        else:
            return "other"
