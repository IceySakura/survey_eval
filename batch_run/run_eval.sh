#!/bin/bash
# 批量评测脚本
# 在生成完成后，对每个任务 × 每个打分模型运行 eval
#
# 用法:
#   ./run_eval.sh                    # 全部任务，全部打分模型
#   ./run_eval.sh sudamuon            # 单任务，全部打分模型
#   ./run_eval.sh sudamuon sfedavg    # 多任务
#   EVAL_MODELS="gpt51" ./run_eval.sh  # 只跑 gpt51（覆盖默认）

set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/eval-survey"

# 激活虚拟环境
if [ -d "eval/.venv" ]; then
  source eval/.venv/bin/activate
fi

# 打分模型消融：gpt51, sonnet4.6, dpsk（须与 config.yaml eval_models 一致）
EVAL_MODELS="${EVAL_MODELS:-gpt51 sonnet4.6 dpsk}"

# 默认评测所有任务，可传参指定
TASKS="${1:-sudamuon sfedavg subspacescaffold}"

echo "=== 批量评测 ==="
echo "任务: $TASKS"
echo "打分模型: $EVAL_MODELS"
echo ""

for task in $TASKS; do
  if [ ! -d "sources/$task" ]; then
    echo "[SKIP] $task: 目录不存在"
    continue
  fi
  if [ ! -f "sources/$task/survey_plan.md" ]; then
    echo "[SKIP] $task: survey_plan.md 不存在"
    continue
  fi
  for eval_model in $EVAL_MODELS; do
    echo ">>> 评测: task=$task eval_model=$eval_model"
    python -m eval.evaluator --task "$task" --eval-model "$eval_model" --sample 15
    echo ""
  done
done

echo "=== 评测完成 ==="
echo "结果目录: eval-survey/eval/results/"
echo "文件名格式: eval_result_{task}_{eval_model}_{timestamp}.json"
