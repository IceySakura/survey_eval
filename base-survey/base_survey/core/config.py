"""配置管理模块"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any
import os
import yaml


@dataclass
class APIConfig:
    """API 公共配置"""
    base_url: str = "https://api.openai.com/v1"
    api_key: str = ""

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY", "") or os.getenv("CODEX_API_KEY", "")
        if self.base_url == "https://api.openai.com/v1":
            self.base_url = os.getenv("OPENAI_BASE_URL", "") or os.getenv("CODEX_BASE_URL", "") or self.base_url


@dataclass
class AgentLLMConfig:
    """单个 Agent 的 LLM 配置"""
    model: str = "gpt-4o"
    api_type: str = "openai"
    temperature: float = 0.7
    max_tokens: int = 16384
    stream: bool = True

    def to_dict(self, api_config: APIConfig) -> Dict[str, Any]:
        return {
            "model": self.model,
            "api_type": self.api_type,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "base_url": api_config.base_url,
            "api_key": api_config.api_key or os.getenv("OPENAI_API_KEY", "") or os.getenv("CODEX_API_KEY", ""),
            "stream": bool(self.stream),
        }


@dataclass
class AgentConfigs:
    """各 Agent 独立 LLM 配置"""
    survey: AgentLLMConfig = field(default_factory=AgentLLMConfig)


@dataclass
class CompressionConfig:
    """上下文压缩配置"""
    enabled: bool = True
    model: str = "gpt-4o-mini"
    max_context_tokens: int = 200000
    compress_threshold: float = 0.7
    preserve_threshold: float = 0.3


@dataclass
class Config:
    """全局配置"""
    max_iters: int = 500
    api: APIConfig = field(default_factory=APIConfig)
    agents: AgentConfigs = field(default_factory=AgentConfigs)
    compression: CompressionConfig = field(default_factory=CompressionConfig)
    workspace: Optional[Path] = None

    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        agent_llm = getattr(self.agents, agent_name, None)
        if agent_llm is None:
            agent_llm = AgentLLMConfig()
        return agent_llm.to_dict(self.api)

    @classmethod
    def from_yaml(cls, config_path: Path) -> "Config":
        if not config_path.exists():
            return cls()
        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        api_data = data.get("api", {})
        api_config = APIConfig(
            base_url=api_data.get("base_url", "https://api.openai.com/v1"),
            api_key=api_data.get("api_key", ""),
        )
        agents_data = data.get("agents", {})
        agents_config = AgentConfigs()
        for agent_name in ["survey"]:
            agent_data = agents_data.get(agent_name, {})
            agent_llm = AgentLLMConfig(
                model=agent_data.get("model", "gpt-4o"),
                api_type=agent_data.get("api_type", "openai"),
                temperature=agent_data.get("temperature", 0.7),
                max_tokens=agent_data.get("max_tokens", 16384),
                stream=bool(agent_data.get("stream", True)),
            )
            setattr(agents_config, agent_name, agent_llm)
        compression_data = data.get("compression", {})
        compression_config = CompressionConfig(
            enabled=compression_data.get("enabled", True),
            model=compression_data.get("model", "gpt-4o-mini"),
            max_context_tokens=compression_data.get(
                "max_context_tokens", 200000
            ),
            compress_threshold=compression_data.get("compress_threshold", 0.7),
            preserve_threshold=compression_data.get(
                "preserve_threshold", 0.3
            ),
        )
        return cls(
            max_iters=data.get("max_iters", 500),
            api=api_config,
            agents=agents_config,
            compression=compression_config,
        )


def load_config(config_path: Optional[str] = None) -> Config:
    if config_path:
        return Config.from_yaml(Path(config_path))
    return Config()
