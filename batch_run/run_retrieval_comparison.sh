#!/bin/bash
# =============================================================================
# 检索线路对比实验: basic vs enhanced
# 2 tasks × 2 retrieval modes = 4 runs
# 生成/评测模型: gpt-5.4, API: llmmelon
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

# --- llmmelon API ---
MELON_URL="https://llmmelon.cloud/v1"
MELON_KEY="sk-YJXKVgR7WGtVPQhMIFRUCVf46h66nxq0cXUAzFiP0YbPTAmH"

# 评测侧使用 AIHUBMIX_* 通道（eval 的 use_aihubmix_for_all_models: true）
export AIHUBMIX_BASE_URL="$MELON_URL"
export AIHUBMIX_API_KEY="$MELON_KEY"
export CODEX_BASE_URL="$MELON_URL"
export CODEX_API_KEY="$MELON_KEY"
export OPENAI_BASE_URL="$MELON_URL"
export OPENAI_API_KEY="$MELON_KEY"

TASKS=("cuttingplane" "firstorder")
MODES=("basic" "enhanced")
MODEL="gpt-5.4"
EVAL_MODEL="gpt54"
SAMPLE=15

echo "============================================="
echo " 检索线路对比: basic vs enhanced"
echo " Tasks: ${TASKS[*]}"
echo " Model: $MODEL  API: llmmelon"
echo "============================================="
echo ""

# --- Phase 1: 生成 ---
echo ">>> Phase 1: 生成 Related Works"
for task in "${TASKS[@]}"; do
    for mode in "${MODES[@]}"; do
        variant="reasflow_${mode}_gpt54"
        echo ""
        echo "=== [$task / $variant] 开始生成 ==="
        python batch_run/run_one.py \
            --task "$task" \
            --variant "$variant" \
            --model "$MODEL" \
            --retrieval-mode "$mode" \
            --api-base-url "$MELON_URL" \
            --api-key "$MELON_KEY" \
            --skip-eval \
            --min-citations 30 \
        || echo "[WARN] $task / $variant 生成失败，继续下一个"
        echo "=== [$task / $variant] 生成完毕 ==="
    done
done

echo ""
echo ">>> Phase 2: 评测"
# --- Phase 2: 评测（每个 task 一次性评所有 variant）---
cd "$ROOT/eval-survey"
EVAL_PYTHON="eval/.venv/bin/python"
if [ ! -f "$EVAL_PYTHON" ]; then
    EVAL_PYTHON="python"
fi

for task in "${TASKS[@]}"; do
    echo ""
    echo "=== [$task] 评测 (eval-model=$EVAL_MODEL, sample=$SAMPLE, dim 1 2) ==="
    $EVAL_PYTHON -m eval.evaluator \
        --task "$task" \
        --eval-model "$EVAL_MODEL" \
        --sample "$SAMPLE" \
        --dim 1 2 \
    || echo "[WARN] $task 评测失败"
done

cd "$ROOT"
echo ""
echo ">>> Phase 3: 汇总"
python batch_run/summarize_eval_analysis.py 2>/dev/null || true

echo ""
echo "============================================="
echo " 完成！结果查看:"
echo "   eval-survey/eval/results/  (JSON + Markdown)"
echo "   batch_run/results/         (汇总 CSV)"
echo "============================================="
