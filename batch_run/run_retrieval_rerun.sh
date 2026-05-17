#!/bin/bash
# =============================================================================
# 重跑失败的生成任务（cuttingplane 两条线路 + 其他失败项）
# 修复了 Responses API 路由问题后使用
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

# --- llmmelon API ---
MELON_URL="https://llmmelon.cloud/v1"
MELON_KEY="sk-YJXKVgR7WGtVPQhMIFRUCVf46h66nxq0cXUAzFiP0YbPTAmH"

export AIHUBMIX_BASE_URL="$MELON_URL"
export AIHUBMIX_API_KEY="$MELON_KEY"
export CODEX_BASE_URL="$MELON_URL"
export CODEX_API_KEY="$MELON_KEY"
export OPENAI_BASE_URL="$MELON_URL"
export OPENAI_API_KEY="$MELON_KEY"

MODEL="gpt-5.4"
EVAL_MODEL="gpt54"
SAMPLE=15

# 检查哪些 task/variant 缺少输出，只跑这些
TASKS=("cuttingplane" "firstorder")
MODES=("basic" "enhanced")
MISSING=()

for task in "${TASKS[@]}"; do
    for mode in "${MODES[@]}"; do
        variant="reasflow_${mode}_gpt54"
        tex="eval-survey/sources/${task}/${variant}/related_works.tex"
        bib="eval-survey/sources/${task}/${variant}/references.bib"
        if [ ! -s "$tex" ] || [ ! -s "$bib" ]; then
            MISSING+=("${task}:${mode}")
        fi
    done
done

if [ ${#MISSING[@]} -eq 0 ]; then
    echo "所有任务都已有输出，无需重跑"
    echo "直接进入评测阶段..."
else
    echo "需要重跑的任务: ${MISSING[*]}"
    echo ""

    for entry in "${MISSING[@]}"; do
        IFS=':' read -r task mode <<< "$entry"
        variant="reasflow_${mode}_gpt54"
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
        || echo "[WARN] $task / $variant 生成失败"
        echo "=== [$task / $variant] 生成完毕 ==="
        echo ""
    done
fi

# 评测
echo ">>> 评测阶段"
cd "$ROOT/eval-survey"
EVAL_PYTHON="eval/.venv/bin/python"
if [ ! -f "$EVAL_PYTHON" ]; then
    EVAL_PYTHON="python"
fi

for task in "${TASKS[@]}"; do
    # 检查是否至少有一个 variant 有输出
    has_output=false
    for mode in "${MODES[@]}"; do
        variant="reasflow_${mode}_gpt54"
        if [ -s "sources/${task}/${variant}/related_works.tex" ]; then
            has_output=true
            break
        fi
    done
    if [ "$has_output" = true ]; then
        echo "=== [$task] 评测 (eval-model=$EVAL_MODEL, sample=$SAMPLE, dim 1 2) ==="
        $EVAL_PYTHON -m eval.evaluator \
            --task "$task" \
            --eval-model "$EVAL_MODEL" \
            --sample "$SAMPLE" \
            --dim 1 2 \
        || echo "[WARN] $task 评测失败"
    else
        echo "[SKIP] $task: 无可评测的输出"
    fi
done

cd "$ROOT"
echo ""
python batch_run/summarize_eval_analysis.py 2>/dev/null || true
echo "完成！"
