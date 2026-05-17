# 批量评测计划

## 一、整体流程

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  sources/       │     │  Agent 生成       │     │  eval-survey/   │     │  汇总分析       │
│  survey_plan.md │ ──► │  (tex + bib)     │ ──► │  评测打分       │ ──► │  leaderboard    │
│  (不含 Key Ref) │     │  按 plan 写作    │     │  (含 Key Ref GT)│     │  消融分析       │
└─────────────────┘     └──────────────────┘     └─────────────────┘     └─────────────────┘
```

**主入口**：`python batch_run/run_batch.py`（一键完成 生成→评测→汇总）

## 二、关键设计

### 2.1 Survey Plan 与 Key References

- **Agent 输入**：`survey_plan.md` 中 **移除 `## Key References` 及其之后的内容**，只给 Agent 提供 Role、Task、Sections、Writing Requirements
- **评测 GT**：评测时使用完整 `survey_plan.md`（含 Key References），作为引用相关性的 GT 进行打分

**实现方式**：`batch_run/utils/plan_utils.py` 的 `get_plan_for_agent()` 截断 Key References；`run_one.py` 中也有同名函数。评测时 `eval.evaluator` 仍用原始 `survey_plan.md`。

### 2.2 输出格式

每个 Agent 运行必须产出：
- `related_works.tex`
- `references.bib`

生成后复制到 `eval-survey/sources/{task}/{variant_name}/` 目录。

### 2.3 消融模型矩阵

**生成侧**（Agent 模型，共 8 组，与 `batch_run/config.yaml` 一致）：

| 类型 | 配置 | 模型组合 | variant 代号 |
|------|------|----------|-------------|
| **agentscope（reasflow）** | survey_auto + CLI `--auto` | gpt-5.1, gpt-5.4, deepseek-v3.2, claude-sonnet-4-6 | `reasflow_gpt51` / `reasflow_gpt54` / `reasflow_dpsk` / `reasflow_sonnet4.6` |
| **base** | survey | gpt-5.1, gpt-5.4, deepseek-v3.2, claude-sonnet-4-6 | `base_gpt51` / `base_gpt54` / `base_dpsk` / `base_sonnet4.6` |

**agentscope 批量路径**：统一走 CLI `--auto`（多步 AutoSurvey）；`etc/config.yaml` 中 `agents.survey` 与 `agents.survey_auto` 的 model 由脚本同步写入。

**打分侧**（评测 LLM 消融）：

| 别名 | 实际 model id | 说明 |
|------|--------------|------|
| gpt51 | gpt-5.1 | 打分模型 1 |
| sonnet4.6 | claude-sonnet-4-6 | 打分模型 2 |
| dpsk | deepseek-v3.2 | 打分模型 3 |

**API 路由**：GPT 系列走 Codex（`CODEX_BASE_URL` / `CODEX_API_KEY`）；DeepSeek / Claude 走 AIHubMix（`AIHUBMIX_BASE_URL` / `AIHUBMIX_API_KEY`），由 `run_one.py` 和 `eval/utils/llm_client.py` 自动切换。

---

## 三、任务列表

`eval-survey/sources/` 下现有任务（3 个，每个均有 `survey_plan.md` 和 8 组已生成产物）：
- `sudamuon` - 去中心化 Muon 优化器
- `sfedavg` - 子空间联邦学习
- `subspacescaffold` - 通信高效联邦学习

每个任务需有 `survey_plan.md`。批量生成时遍历所有任务。

---

## 四、脚本体系

### 4.1 入口脚本

| 脚本 | 用途 | 典型用法 |
|------|------|---------|
| `batch_run/run_batch.py` | **主入口**：生成 → 评测 → 汇总 | `python batch_run/run_batch.py` |
| `batch_run/run_generation.py` | 批量生成（遍历 task × variant） | `python batch_run/run_generation.py --dry-run` |
| `batch_run/run_one.py` | 单次生成 + 可选评测 | `python batch_run/run_one.py --task sudamuon --variant base_gpt51` |
| `batch_run/run_eval.sh` | 独立评测（Shell 脚本） | `./batch_run/run_eval.sh sudamuon` |
| `batch_run/summarize_eval_analysis.py` | 从 eval JSON 汇总 leaderboard + 消融表 | `python batch_run/summarize_eval_analysis.py` |
| `batch_run/test_models.py` | 测试消融用模型的 API 可用性 | `python batch_run/test_models.py` |

### 4.2 常用命令

**全量批量（生成 + 评测 + 汇总）**：
```bash
python batch_run/run_batch.py
```

**仅评测（跳过生成，适用于已有产物）**：
```bash
python batch_run/run_batch.py --eval-only
```

**断点续跑（跳过已有 eval 结果，换 API Key 后续跑）**：
```bash
python batch_run/run_batch.py --eval-only --resume
```

**生成侧 dry-run（预览计划，不执行）**：
```bash
python batch_run/run_generation.py --dry-run
```

**单任务单 variant**：
```bash
python batch_run/run_one.py --task sudamuon --variant base_gpt51 --skip-eval
```

**独立评测脚本**：
```bash
# 全部任务，默认打分模型 gpt51 sonnet4.6 dpsk
./batch_run/run_eval.sh

# 单任务
./batch_run/run_eval.sh sudamuon

# 覆盖打分模型
EVAL_MODELS="gpt51" ./batch_run/run_eval.sh
```

**单次评测**：
```bash
cd eval-survey
python -m eval.evaluator --task sudamuon --eval-model gpt51 --sample 15
```

**汇总分析（从已有 eval JSON 生成 leaderboard + 消融表）**：
```bash
python batch_run/summarize_eval_analysis.py
```

### 4.3 工作区与输出路径

| Agent | 批量工作区路径 | 输出文件 |
|-------|----------------|----------|
| agentscope-survey | `agentscope-survey/workspace_runs/{task}/{variant}/` | `survey/related_works.tex`、`survey/references.bib` |
| base-survey | `base-survey/workspace_runs/{task}/{variant}/` | `survey/related_works.tex`、`survey/references.bib` |

批量生成时 `run_one.py` 为每个 (task, variant) 创建独立 workspace 目录，运行前自动清空。

### 4.4 配置文件位置（消融时修改）

| Agent | 配置文件 | 消融需修改的 key |
|-------|----------|------------------|
| agentscope-survey（reasflow） | `etc/config.yaml` | `agents.survey.model` 与 `agents.survey_auto.model`（脚本同步写入） |
| base-survey | `etc/config.yaml` | `agents.survey.model` |

---

## 五、目录结构

### 5.1 生成阶段

```
paper_gen/
├── agentscope-survey/
│   ├── etc/config.yaml          # 含 survey、survey_auto 两个 agent config
│   ├── workspace_runs/          # 批量生成的隔离工作区（按 task/variant）
│   └── .venv/                   # 独立虚拟环境
├── base-survey/
│   ├── etc/config.yaml
│   ├── workspace_runs/
│   └── .venv/
└── batch_run/
    ├── config.yaml              # 任务、变体、eval_models、路径配置
    ├── config_small.yaml        # 小规模健康检查配置
    ├── run_batch.py             # 主入口
    ├── run_generation.py        # 批量生成
    ├── run_one.py               # 单次生成
    ├── run_eval.sh              # 独立评测脚本
    ├── summarize_eval_analysis.py # 汇总分析
    ├── test_models.py           # 模型可用性测试
    ├── utils/plan_utils.py      # get_plan_for_agent()
    ├── .env                     # API Key 配置
    ├── logs/                    # 生成/评测日志
    └── results/                 # 汇总产物
        ├── eval_analysis.md
        ├── eval_leaderboard.csv
        ├── eval_matrix_by_task.csv
        └── batch_eval_summary_*.csv
```

### 5.2 评测阶段

```
eval-survey/
├── sources/
│   ├── sudamuon/
│   │   ├── survey_plan.md           # 完整 plan（含 Key References，评测用）
│   │   ├── eval_config.yaml         # 可选：任务级评测配置
│   │   ├── reasflow_gpt51/          # 各 variant 的生成产物
│   │   │   ├── related_works.tex
│   │   │   └── references.bib
│   │   ├── reasflow_gpt54/
│   │   ├── reasflow_dpsk/
│   │   ├── reasflow_sonnet4.6/
│   │   ├── base_gpt51/
│   │   ├── base_gpt54/
│   │   ├── base_dpsk/
│   │   └── base_sonnet4.6/
│   ├── sfedavg/
│   └── subspacescaffold/
├── eval/
│   ├── evaluator.py             # 评测主入口
│   ├── config.yaml              # 评测配置
│   ├── .venv/                   # 评测虚拟环境
│   ├── cache/                   # PDF 和搜索缓存
│   ├── results/                 # 评测结果 JSON + Markdown
│   ├── utils/                   # llm_client, paper_fetcher 等
│   └── metrics/                 # 四维度评测器
└── .env                         # 评测 API Key
```

---

## 六、评测维度

| 维度 | 类型 | 分值范围 | 说明 |
|------|------|---------|------|
| 1. 内容准确性 | 客观 | 0–10 | 抽样验证引用内容是否与原文一致，检测幻觉 |
| 2. 引用相关性 | 客观 | 0–10 | Key References 覆盖率 + 引用质量评分（联动维度1排除捏造） |
| 3. 指令遵循 | 主观 AB | 相对分 | 对比两篇文章对 plan 的遵循度 |
| 4. 写作质量 | 主观 AB | 相对分 | 对比两篇文章的写作质量 |

默认只跑维度 1+2（客观评测）。加 `--dim 1 2 3 4` 完整评测。

**总分**：每篇 = 内容准确性(0–10) + 引用相关性(0–10)，最高 20。

---

## 七、汇总产物

`summarize_eval_analysis.py` 生成：

| 文件 | 内容 |
|------|------|
| `eval_analysis.md` | Markdown 报告：Leaderboard + agent 消融 + backbone 消融 + 评测可靠性 |
| `eval_leaderboard.csv` | 按任务内排名：variant × 跨评测均分 |
| `eval_matrix_by_task.csv` | 生成配置 × 评测模型的全量总分矩阵 |
| `eval_citation_stats.csv` | 各配置的引用条数、Key Ref 覆盖、CR 分等 |

---

## 八、配置文件管理

每个 variant 需要不同的 `model`。`run_one.py` 的 `update_config_model()` 在每次运行前动态写 `etc/config.yaml`：
- agentscope（reasflow）：同时写 `agents.survey.model` 和 `agents.survey_auto.model`
- base：写 `agents.survey.model`

API Key 配置在 `batch_run/.env`（参考 `.env.example`）：
- GPT 模型：`CODEX_BASE_URL` + `CODEX_API_KEY`
- 非 GPT（DeepSeek / Claude）：`AIHUBMIX_BASE_URL` + `AIHUBMIX_API_KEY`

---

## 九、检查清单

- [x] 实现 `get_plan_for_agent()`，正确截断 Key References
- [x] agentscope `survey_auto` config 支持，auto 模式下使用
- [x] 确认 API 模型名：gpt-5.1、gpt-5.4、deepseek-v3.2、claude-sonnet-4-6
- [x] 实现批量生成脚本（run_generation.py → run_one.py → 启动 agent → 复制结果）
- [x] 输出路径：`workspace/survey/related_works.tex`、`references.bib`
- [x] 复制逻辑：workspace/survey/* → eval-survey/sources/{task}/{variant_name}/
- [x] 编写批量评测脚本（run_batch.py --eval-only / run_eval.sh）
- [x] 三个任务均有 `survey_plan.md`
- [x] 3 任务 × 8 variant 共 24 组产物已生成
- [x] 3 任务 × 3 评测模型共 9 组评测结果已生成
- [x] summarize_eval_analysis.py 汇总 + 消融分析
- [x] run_eval.sh eval_models 与 config.yaml 同步（gpt51, sonnet4.6, dpsk）
- [x] summarize_eval_analysis.py 支持任意新增任务（不再硬编码任务名）

---

## 十、执行顺序建议

1. 配置 `batch_run/.env`（参考 `.env.example`）
2. `python batch_run/test_models.py` 验证所有模型可用
3. `python batch_run/run_generation.py --dry-run` 预览生成计划
4. 先单任务单 variant 跑通：`python batch_run/run_one.py --task sudamuon --variant base_gpt51`
5. 全量生成：`python batch_run/run_generation.py`
6. 全量评测 + 汇总：`python batch_run/run_batch.py --eval-only`
7. 汇总分析：`python batch_run/summarize_eval_analysis.py`
