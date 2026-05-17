#!/usr/bin/env bash
set -euo pipefail

# 确保 PATH 包含 uv
export PATH="/home/iceysakura/.local/bin:/snap/bin:$PATH"

cd /home/iceysakura/1/pylab/paper_gen/base-survey

# 创建 workspace（如果不存在）
mkdir -p ./workspace

# 启动 ACP 模式（Zed IDE 集成）
exec uv run python -m base_survey --mode acp --workspace ./workspace --config ./etc/config.yaml 2>/dev/null
