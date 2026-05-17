"""LLM API 客户端封装

端点由 eval/config.yaml 的 eval_api.use_aihubmix_for_all_models（或环境变量
EVAL_USE_AIHUBMIX=1）及模型 id 共同决定：

- **统一 HubMix**：所有打分模型走 AIHUBMIX_*（Codex 不可用时）。
- **分流模式**：GPT 系优先 CODEX_*；DeepSeek/Claude 等走 AIHUBMIX_*。

Codex（codex-for.me）必须 stream=true；HubMix 默认非流式（可用 eval_api.aihubmix_stream 打开）。
"""

import json
import time
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import requests
import yaml

logger = logging.getLogger(__name__)


def _strip(s: Optional[str]) -> str:
    return (s or "").strip()


def _uses_max_completion_tokens(model: str) -> bool:
    """OpenAI 新 chat 与多数 HubMix 上的 GPT 路由要求 max_completion_tokens，拒绝 max_tokens。"""
    m = (model or "").lower()
    return any(
        x in m
        for x in (
            "gpt-4o",
            "gpt-5",
            "gpt-3.5",
            "gpt-4-turbo",
            "o1",
            "o3",
            "o4",
            "chatgpt",
        )
    )


def _model_uses_aihubmix(model: str) -> bool:
    """DeepSeek / Claude 等非 Codex 主力线路走 AIHubMix。"""
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


def _hubmix_creds(cfg: dict) -> Tuple[str, str]:
    ea = cfg.get("eval_api") or {}
    base = _strip(os.getenv("AIHUBMIX_BASE_URL")) or _strip(ea.get("aihubmix_base_url"))
    key = _strip(os.getenv("AIHUBMIX_API_KEY")) or _strip(ea.get("aihubmix_api_key"))
    return base, key


def _use_aihubmix_for_all(cfg: dict) -> bool:
    v = _strip(os.getenv("EVAL_USE_AIHUBMIX")).lower()
    if v in ("1", "true", "yes", "on"):
        return True
    if v in ("0", "false", "no", "off"):
        return False
    ea = cfg.get("eval_api") or {}
    return bool(ea.get("use_aihubmix_for_all_models", False))


def _resolve_credentials(
    model: str,
    cfg: dict,
) -> Tuple[str, str, str]:
    """返回 (base_url, api_key, route_label)。"""
    ea = cfg.get("eval_api") or {}
    api_fallback = cfg.get("api") or {}

    if _use_aihubmix_for_all(cfg):
        base, key = _hubmix_creds(cfg)
        if base and key:
            return base, key, "aihubmix"
        logger.error(
            "已开启统一 AIHubMix（eval_api.use_aihubmix_for_all_models 或 EVAL_USE_AIHUBMIX=1），"
            "但未配置 AIHUBMIX_BASE_URL + AIHUBMIX_API_KEY（或 eval_api.aihubmix_*），"
            "将回退 Codex / OPENAI"
        )

    if _model_uses_aihubmix(model):
        base, key = _hubmix_creds(cfg)
        if base and key:
            return base, key, "aihubmix"
        logger.warning(
            "模型 %s 应走 AIHubMix，但未配置 AIHUBMIX_*，将回退 OPENAI/CODEX",
            model,
        )

    # GPT / 默认：Codex 优先于 OPENAI
    base = _strip(os.getenv("CODEX_BASE_URL")) or _strip(ea.get("codex_base_url"))
    key = _strip(os.getenv("CODEX_API_KEY")) or _strip(ea.get("codex_api_key"))
    if base and key:
        return base, key, "codex"

    base = _strip(os.getenv("OPENAI_BASE_URL")) or _strip(api_fallback.get("base_url", ""))
    key = _strip(os.getenv("OPENAI_API_KEY")) or _strip(api_fallback.get("api_key", ""))
    if base and key:
        return base, key, "openai"

    return (
        _strip(api_fallback.get("base_url")) or "https://api.openai.com/v1",
        _strip(api_fallback.get("api_key", "")),
        "config_fallback",
    )


class LLMClient:
    """LLM API 客户端"""

    def __init__(
        self,
        config_path: Optional[Path] = None,
        model_override: Optional[str] = None,
    ):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"

        self.config = self._load_config(config_path)
        self.model = model_override or self.config["llm"]["model"]

        self.api_base_url, self.api_key, self._route = _resolve_credentials(
            self.model, self.config
        )
        logger.info(
            "评测 LLM 路由: %s | base=%s | model=%s",
            self._route,
            self.api_base_url,
            self.model,
        )

        self.temperature = self.config["llm"]["temperature"]
        self.max_tokens = self.config["llm"]["max_tokens"]

        ea = self.config.get("eval_api") or {}
        self._rate_limit_interval = float(ea.get("rate_limit_seconds", 1.0))
        self._max_retries = int(ea.get("request_retries", 6))
        self._connect_timeout = float(ea.get("connect_timeout", 30))
        self._read_timeout = float(ea.get("read_timeout", 180))

        self._last_request_time = 0.0
        bu = str(self.api_base_url).lower()
        ea = self.config.get("eval_api") or {}
        if self._route == "aihubmix":
            self._force_stream = bool(ea.get("aihubmix_stream", False))
        else:
            self._force_stream = "codex-for.me" in bu

    def _load_config(self, config_path: Path) -> dict:
        if config_path.exists():
            with open(config_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            return data
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    def _rate_limit(self) -> None:
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self._rate_limit_interval:
            time.sleep(self._rate_limit_interval - elapsed)
        self._last_request_time = time.time()

    def _backoff_sleep(self, attempt: int) -> None:
        time.sleep(min(2 ** attempt, 32) + 0.5 * attempt)

    def chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
    ) -> Optional[str]:
        self._rate_limit()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        url = f"{self.api_base_url.rstrip('/')}/chat/completions"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        mt = max_tokens if max_tokens is not None else self.max_tokens
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
        }
        if _uses_max_completion_tokens(self.model):
            payload["max_completion_tokens"] = mt
        else:
            payload["max_tokens"] = mt
        if self._force_stream:
            payload["stream"] = True

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        timeout = (self._connect_timeout, self._read_timeout)
        use_stream = bool(self._force_stream)

        for attempt in range(self._max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    stream=use_stream,
                    timeout=timeout,
                )

                if response.status_code == 200:
                    if use_stream:
                        text = self._parse_stream_content(response)
                        if text:
                            return text
                        logger.warning(
                            "流式解析为空，尝试重试 (%s/%s)",
                            attempt + 1,
                            self._max_retries,
                        )
                        if attempt < self._max_retries - 1:
                            self._backoff_sleep(attempt)
                        continue
                    try:
                        result = response.json()["choices"][0]["message"]["content"]
                    except (KeyError, IndexError, TypeError) as e:
                        logger.warning("非流式响应结构异常: %s", e)
                        result = None
                    if isinstance(result, str) and result.strip():
                        return result
                    if attempt < self._max_retries - 1:
                        self._backoff_sleep(attempt)
                    continue
                elif response.status_code == 429:
                    wait_time = (attempt + 1) * 5
                    logger.warning("API 限流，等待 %ss 后重试...", wait_time)
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(
                        "API 错误 (%s): %s",
                        response.status_code,
                        response.text[:300],
                    )
                    if attempt < self._max_retries - 1:
                        self._backoff_sleep(attempt)
                        continue
                    return None

            except requests.RequestException as e:
                logger.error("请求失败: %s", e)
                if attempt < self._max_retries - 1:
                    self._backoff_sleep(attempt)

        return None

    def _parse_stream_content(self, response: requests.Response) -> Optional[str]:
        """解析 SSE，拼接 delta.content / reasoning_content / 末包 message.content。"""
        chunks: list[str] = []
        try:
            for raw_line in response.iter_lines(decode_unicode=False):
                if not raw_line:
                    continue
                try:
                    line = raw_line.decode("utf-8", errors="replace").strip()
                except Exception:
                    continue
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    obj = json.loads(data)
                except json.JSONDecodeError:
                    continue
                ch0 = obj.get("choices", [{}])[0]
                delta = ch0.get("delta") or {}
                if isinstance(delta, dict):
                    for k in ("content", "reasoning_content"):
                        v = delta.get(k)
                        if isinstance(v, str) and v:
                            chunks.append(v)
                msg = ch0.get("message")
                if isinstance(msg, dict):
                    mc = msg.get("content")
                    if isinstance(mc, str) and mc:
                        chunks.append(mc)
            text = "".join(chunks).strip()
            if text:
                return text
            logger.error("流式响应解析为空")
            return None
        except requests.RequestException as e:
            logger.error("流式响应读取失败: %s", e)
            return None

    @staticmethod
    def _normalize_json_like(text: str) -> str:
        text = re.sub(r"(:\s*)\+(\d+(?:\.\d+)?)", r"\1\2", text)
        return text

    @staticmethod
    def _strip_markdown_json_fence(text: str) -> str:
        m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?```", text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        return text.strip()

    @staticmethod
    def _parse_json_dict_from_text(text: str) -> Optional[Dict[str, Any]]:
        """整段或混排（Claude 常先写分析再贴 JSON）中解析出第一个 JSON object。"""
        text = (text or "").strip()
        if not text:
            return None
        inner = LLMClient._strip_markdown_json_fence(text)
        for chunk in (inner, text):
            chunk = LLMClient._normalize_json_like(chunk.strip())
            try:
                obj = json.loads(chunk)
                if isinstance(obj, dict):
                    return obj
            except json.JSONDecodeError:
                pass
            dec = json.JSONDecoder()
            start = 0
            while True:
                i = chunk.find("{", start)
                if i < 0:
                    break
                try:
                    obj, _end = dec.raw_decode(chunk, i)
                    if isinstance(obj, dict) and obj:
                        return obj
                except json.JSONDecodeError:
                    pass
                start = i + 1
        return None

    def chat_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        response = self.chat(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            json_mode=True,
        )

        if not response:
            return None

        raw = response.strip()
        obj = self._parse_json_dict_from_text(raw)
        if obj is not None:
            if not raw.lstrip().startswith("{"):
                logger.info("已从混排/非 JSON 前缀的模型回复中提取 JSON（常见于 Claude + HubMix）")
            return obj
        logger.warning("JSON 解析失败（含兜底）\nResponse 前缀: %s", raw[:280])
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = LLMClient()
    out = client.chat("Say hello in JSON format", json_mode=True)
    print(out)
