#!/usr/bin/env python3
"""测试消融用模型的可用性（仅测 BATCH_EVAL_PLAN 中列出的）"""

import os
import requests
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "eval-survey" / "eval" / "config.yaml"
BATCH_ENV = ROOT / "batch_run" / ".env"


def _apply_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        k, v = k.strip(), v.strip().strip("'").strip('"')
        if k and (k not in os.environ or not os.environ.get(k)):
            os.environ[k] = v


# 与 run_one 一致：先 batch_run/.env
_apply_env_file(BATCH_ENV)


def _codex_base() -> str:
    return (
        os.getenv("CODEX_BASE_URL")
        or os.getenv("CODEX_API_BASE")
        or "https://api-vip.codex-for.me/v1"
    ).rstrip("/")


def _codex_key() -> str:
    return os.getenv("CODEX_API_KEY", "")


# 消融模型：GPT → Codex；其余 → AIHubMix（见 batch_run/.env 说明）
# (alias, model_id, api)  api: aihubmix | codex
MODELS = [
    ("gpt-5.1", "gpt-5.1", "codex"),
    ("gpt-5.4", "gpt-5.4", "codex"),
    ("gpt4o", "gpt-4o", "codex"),
    ("dpsk", "deepseek-v3.2", "aihubmix"),
    ("sonnet4.6", "claude-sonnet-4-6", "aihubmix"),
]


def test_model(base_url: str, api_key: str, model: str, use_max_tokens: bool = False) -> tuple[bool, str]:
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say hello in one word."}],
    }
    payload["max_completion_tokens" if use_max_tokens else "max_tokens"] = 10
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            content = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            return True, content.strip()[:50] if content else "ok"
        err = r.json().get("error", {}) if r.text else {}
        msg = err.get("message", r.text[:200]) if isinstance(err, dict) else r.text[:200]
        return False, msg
    except Exception as e:
        return False, str(e)


def main():
    with open(CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    aihubmix_url = os.getenv("AIHUBMIX_BASE_URL") or cfg["api"].get("base_url", "")
    aihubmix_key = os.getenv("AIHUBMIX_API_KEY") or cfg["api"].get("api_key", "")
    codex_url = _codex_base()
    codex_key = _codex_key()

    print("消融模型可用性测试\n" + "=" * 50)
    for alias, model_id, api in MODELS:
        url = aihubmix_url if api == "aihubmix" else codex_url
        key = aihubmix_key if api == "aihubmix" else codex_key
        use_max = api == "aihubmix" or "gpt-5" in model_id
        ok, msg = test_model(url, key, model_id, use_max_tokens=use_max)
        status = "✓" if ok else "✗"
        src = f" [{api}]" if api == "codex" else ""
        print(f"  {status} {alias} (id={model_id}){src}: {msg}")
    print("=" * 50)


if __name__ == "__main__":
    main()
