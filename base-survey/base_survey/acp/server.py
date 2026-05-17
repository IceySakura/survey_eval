"""ACP Server 实现 - Zed 兼容"""

import asyncio
import io
import json
import logging
import sys
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from .protocol import (
    ACPError,
    ACPMethods,
    ACPNotification,
    ACPRequest,
    ACPResponse,
    InitializeResult,
    SessionNewResult,
    SessionUpdateKind,
    SessionUpdateParams,
)

log_path = Path(__file__).resolve().parents[2] / "logs" / "acp_server.log"
log_path.parent.mkdir(exist_ok=True)
logging.basicConfig(
    filename=str(log_path),
    level=logging.INFO,
    format="%(asctime)s - [acp-server] - %(levelname)s - %(message)s",
    encoding="utf-8",
    filemode="a",
)

_real_stdout = sys.stdout
_acp_mode = False


class _ACPNullWriter(io.TextIOBase):
    def write(self, s: str) -> int:
        try:
            if s:
                logging.debug(f"[ACP-STDOUT] {s.rstrip()}")
        except Exception:
            pass
        return len(s or "")

    def flush(self) -> None:
        return


def enable_acp_mode():
    global _acp_mode
    if _acp_mode:
        return
    _acp_mode = True
    sys.stdout = _ACPNullWriter()
    logging.info("[ACP] stdout 保护已启用")


def write_to_real_stdout(message: str):
    _real_stdout.write(message)
    _real_stdout.flush()


class ACPClient:
    def __init__(self, output_stream=None):
        self._output = output_stream or _real_stdout
        self._pending_requests: dict[str, asyncio.Future] = {}
        self._request_id = 0

    def send_notification(self, method: str, params: dict):
        notification = ACPNotification(method=method, params=params)
        payload = notification.to_json()
        logging.info(f"SEND_NOTIFY {method}: {payload[:500]}")
        write_to_real_stdout(payload + "\n")

    def send_session_update(
        self,
        session_id: str,
        kind: SessionUpdateKind,
        content: Any = None,
        tool_call_id: str = None,
        tool_name: str = None,
        tool_status: str = None,
        tool_input: dict = None,
        tool_output: str = None,
    ):
        params = SessionUpdateParams(
            session_id=session_id,
            kind=kind.value if isinstance(kind, SessionUpdateKind) else kind,
            content=content,
            tool_call_id=tool_call_id,
            tool_name=tool_name,
            tool_status=tool_status,
            tool_input=tool_input,
            tool_output=tool_output,
        )
        self.send_notification(ACPMethods.SESSION_UPDATE, params.to_dict())


class ACPServer:
    def __init__(self, agent_factory: Callable[[ACPClient], Any] = None):
        self._agent_factory = agent_factory
        self._running = False
        self._client = ACPClient()
        self._agent = None
        self._sessions: dict[str, dict] = {}
        self._current_task: asyncio.Task | None = None

    @property
    def client(self) -> ACPClient:
        return self._client

    def send_response(self, response: ACPResponse):
        write_to_real_stdout(response.to_json() + "\n")

    async def handle_request(self, request: ACPRequest) -> ACPResponse | None:
        method = request.method
        params = request.params
        try:
            if method == ACPMethods.INITIALIZE:
                result = await self._handle_initialize(params)
            elif method == ACPMethods.SESSION_NEW:
                result = await self._handle_session_new(params)
            elif method == ACPMethods.SESSION_LOAD:
                result = await self._handle_session_load(params)
            elif method == ACPMethods.SESSION_PROMPT:
                result = await self._handle_session_prompt(params, request.id)
            elif method == ACPMethods.SESSION_CANCEL:
                result = await self._handle_session_cancel(params)
            elif method == ACPMethods.AUTHENTICATE:
                result = await self._handle_authenticate(params)
            else:
                return ACPResponse.failure(
                    ACPError.method_not_found(method), request.id
                )
            if result is None:
                return None
            return ACPResponse.success(result, request.id)
        except Exception as e:
            logging.exception(f"Error handling ACP method '{method}': {e}")
            return ACPResponse.failure(
                ACPError.internal_error(str(e)), request.id
            )

    async def _handle_initialize(self, params: dict) -> dict:
        if self._agent_factory:
            self._agent = self._agent_factory(self._client)
        return InitializeResult().to_dict()

    async def _handle_session_new(self, params: dict) -> dict:
        session_id = str(uuid.uuid4())
        workspace = params.get("cwd") or "./workspace"
        if len(workspace) >= 2 and workspace[1] == ":":
            drive_letter = workspace[0].lower()
            rest_of_path = workspace[2:].replace("\\", "/")
            workspace = f"/mnt/{drive_letter}{rest_of_path}"
        workspace = str(Path(workspace).resolve())
        language = params.get("language", "Chinese")
        model_config_override = {}
        raw_model_config = params.get("modelConfig") or params.get(
            "model_config"
        ) or {}
        for src_key, dst_key in [
            ("model", "model"),
            ("apiType", "api_type"),
            ("api_type", "api_type"),
            ("temperature", "temperature"),
            ("maxTokens", "max_tokens"),
            ("max_tokens", "max_tokens"),
        ]:
            if src_key in raw_model_config:
                model_config_override[dst_key] = raw_model_config[src_key]
        self._sessions[session_id] = {
            "workspace": workspace,
            "language": language,
            "model_config_override": model_config_override,
            "messages": [],
            "meta": {},
        }
        return SessionNewResult(session_id=session_id).to_dict()

    async def _handle_session_load(self, params: dict) -> dict:
        session_id = params.get("sessionId") or params.get("session_id", "")
        if session_id not in self._sessions:
            raise ValueError(f"Session not found: {session_id}")
        return {"sessionId": session_id}

    async def _handle_session_prompt(
        self, params: dict, request_id: str | None = None
    ) -> dict:
        session_id = params.get("sessionId") or params.get("session_id", "")
        raw_prompt = params.get("prompt", "")
        if isinstance(raw_prompt, list):
            texts = []
            for item in raw_prompt:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        texts.append(item.get("text", ""))
                    elif "text" in item:
                        texts.append(item["text"])
                elif isinstance(item, str):
                    texts.append(item)
            prompt = "\n".join(texts)
        else:
            prompt = str(raw_prompt)

        if session_id not in self._sessions:
            raise ValueError(f"Session not found: {session_id}")

        session = self._sessions[session_id]
        meta = params.get("_meta") or params.get("meta") or {}
        if isinstance(meta, dict):
            filtered_meta = {}
            for k in ["baseUrl", "apiKey", "model", "apiType"]:
                if meta.get(k):
                    filtered_meta[k] = meta[k]
            if filtered_meta:
                session_meta = session.get("meta") or {}
                session_meta.update(filtered_meta)
                session["meta"] = session_meta

        if self._agent and hasattr(self._agent, "run"):

            async def run_task():
                try:
                    await self._agent.run(
                        prompt,
                        session_id=session_id,
                        workspace=session["workspace"],
                        language=session["language"],
                        session_meta=session.get("meta") or {},
                    )
                    if request_id is not None:
                        self.send_response(
                            ACPResponse.success(
                                {"stopReason": "end_turn"}, request_id
                            )
                        )
                except Exception as e:
                    logging.exception(f"[ACP] 任务出错: {e}")
                    try:
                        self._client.send_session_update(
                            session_id=session_id,
                            kind=SessionUpdateKind.AGENT_MESSAGE_CHUNK,
                            content=f"错误: {e}",
                        )
                    except OSError:
                        pass
                    if request_id is not None:
                        self.send_response(
                            ACPResponse.failure(
                                ACPError.internal_error(str(e)), request_id
                            )
                        )

            self._current_task = asyncio.create_task(run_task())
        else:
            self._client.send_session_update(
                session_id=session_id,
                kind=SessionUpdateKind.AGENT_MESSAGE_CHUNK,
                content=f"收到: {prompt}",
            )

        return None

    async def _handle_session_cancel(self, params: dict) -> dict:
        session_id = params.get("sessionId") or params.get("session_id", "")
        if self._current_task and not self._current_task.done():
            self._current_task.cancel()
            try:
                await self._current_task
            except asyncio.CancelledError:
                pass
        return None

    async def _handle_authenticate(self, params: dict) -> dict:
        return {"authenticated": True}

    async def run(self):
        enable_acp_mode()
        self._running = True
        _real_stdin = sys.stdin.buffer
        loop = asyncio.get_event_loop()
        while self._running:
            try:
                line_bytes = await loop.run_in_executor(
                    None, _real_stdin.readline
                )
                if not line_bytes:
                    break
                try:
                    line = line_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    line = line_bytes.decode("utf-8", errors="replace")
                line = line.strip()
                if not line:
                    continue
                try:
                    request = ACPRequest.from_json(line)
                except json.JSONDecodeError as e:
                    response = ACPResponse.failure(
                        ACPError.parse_error(str(e))
                    )
                    self.send_response(response)
                    continue
                response = await self.handle_request(request)
                if response is not None:
                    self.send_response(response)
            except Exception as e:
                try:
                    self.send_response(
                        ACPResponse.failure(ACPError.internal_error(str(e)))
                    )
                except Exception:
                    pass

    def stop(self):
        self._running = False


class BaseSurveyFlowAgent:
    """Base Survey Agent 封装，供 ACP 使用"""

    def __init__(
        self,
        client: ACPClient,
        model_config: dict,
        default_workspace: str = "./workspace",
        output_language: str = "Chinese",
        enable_compress: bool = True,
        compress_model: str = "gpt-4o-mini",
        max_context_tokens: int = 200000,
        compress_threshold: float = 0.7,
    ):
        self._client = client
        self._model_config = model_config
        self._default_workspace = default_workspace
        self._output_language = output_language
        self._agents: dict[str, Any] = {}
        self._enable_compress = enable_compress
        self._compress_model = compress_model
        self._max_context_tokens = max_context_tokens
        self._compress_threshold = compress_threshold

    def _build_effective_model_config(self, session_meta: dict | None) -> dict:
        import os

        base = dict(self._model_config) if self._model_config else {}
        meta = session_meta or {}

        if os.getenv("OPENAI_API_KEY") and not base.get("api_key"):
            base["api_key"] = os.getenv("OPENAI_API_KEY")
        if os.getenv("OPENAI_BASE_URL") and not base.get("base_url"):
            base["base_url"] = os.getenv("OPENAI_BASE_URL")

        if "apiKey" in meta:
            base["api_key"] = meta["apiKey"]
        if "baseUrl" in meta:
            base["base_url"] = meta["baseUrl"]
        if "model" in meta:
            base["model"] = meta["model"]
        if "apiType" in meta:
            base["api_type"] = meta["apiType"]

        if not base.get("api_key") or not base.get("base_url"):
            cfg_path = Path(__file__).resolve().parents[2] / "etc" / "config.yaml"
            if cfg_path.exists():
                try:
                    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
                    api_cfg = cfg.get("api", {})
                    if not base.get("base_url") and api_cfg.get("base_url"):
                        base["base_url"] = api_cfg.get("base_url")
                    if not base.get("api_key") and api_cfg.get("api_key"):
                        base["api_key"] = api_cfg.get("api_key")
                except Exception:
                    pass

        return base

    async def run(
        self,
        prompt: str,
        session_id: str = "",
        workspace: str = None,
        language: str = "Chinese",
        session_meta: dict | None = None,
    ) -> str:
        workspace = workspace or self._default_workspace
        model_config = self._build_effective_model_config(session_meta)

        def thinking_callback(thinking_text: str):
            self._client.send_session_update(
                session_id=session_id,
                kind=SessionUpdateKind.AGENT_THOUGHT_CHUNK,
                content=thinking_text,
            )

        def text_callback(text: str):
            self._client.send_session_update(
                session_id=session_id,
                kind=SessionUpdateKind.AGENT_MESSAGE_CHUNK,
                content=text,
            )

        def compress_callback(message: str):
            self._client.send_session_update(
                session_id=session_id,
                kind=SessionUpdateKind.AGENT_THOUGHT_CHUNK,
                content=f"[memory] {message}",
            )

        def tool_call_callback(
            tool_call_id: str,
            tool_name: str,
            tool_input: dict,
            status: str,
            tool_output: str = None,
        ):
            if status == "pending":
                self._client.send_session_update(
                    session_id=session_id,
                    kind=SessionUpdateKind.TOOL_CALL,
                    tool_call_id=tool_call_id,
                    tool_name=tool_name,
                    tool_status="pending",
                    tool_input=tool_input,
                )
            elif status == "completed":
                content = tool_output
                if "edit" in tool_name.lower() and tool_input:
                    content = {
                        "type": "diff",
                        "path": tool_input.get("path", ""),
                        "oldText": tool_input.get("old_string", ""),
                        "newText": tool_input.get("new_string", ""),
                    }
                self._client.send_session_update(
                    session_id=session_id,
                    kind=SessionUpdateKind.TOOL_CALL_UPDATE,
                    tool_call_id=tool_call_id,
                    tool_name=tool_name,
                    tool_status="completed",
                    content=content,
                    tool_output=tool_output,
                )
            elif status == "error":
                self._client.send_session_update(
                    session_id=session_id,
                    kind=SessionUpdateKind.TOOL_CALL_UPDATE,
                    tool_call_id=tool_call_id,
                    tool_name=tool_name,
                    tool_status="error",
                    content=tool_output,
                    tool_output=tool_output,
                )

        agent = self._agents.get(session_id)
        if agent is None:
            from ..agents.survey import BaseSurveyAgent

            agent = BaseSurveyAgent(
                model_config=model_config,
                workspace=workspace,
                print_hint_msg=False,
                tool_call_callback=tool_call_callback,
                compress_callback=compress_callback,
                thinking_callback=thinking_callback,
                text_callback=text_callback,
                enable_compress=self._enable_compress,
                compress_model=self._compress_model,
                max_context_tokens=self._max_context_tokens,
                compress_threshold=self._compress_threshold,
            )
            self._agents[session_id] = agent

        return await agent.run(prompt)
