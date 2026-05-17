# Related Works 评测系统

针对 AI agent 生成的 Related Works 段落，进行多维度、公平可复现的自动化评测。

---

## 目录结构

```
eval-survey/
├── sources/                         # 待评测数据（按任务组织）
│   ├── sudamuon/                    # 任务：去中心化 Muon 优化器
│   │   ├── survey_plan.md           # 写作任务说明（评测基准）
│   │   ├── eval_config.yaml        # 可选：任务级评测配置（no_sample、白名单等）
│   │   ├── ours/                    # Agent A 输出
│   │   │   ├── related_works.tex
│   │   │   └── references.bib
│   │   └── reas/                    # Agent B 输出
│   │       ├── related_works.tex
│   │       └── references.bib
│   └── sfedavg/                     # 任务：子空间联邦学习
│       ├── survey_plan.md
│       └── ours/
│           ├── related_works.tex
│           └── references.bib
└── eval/                            # 评测系统
    ├── config.yaml                  # 配置文件
    ├── evaluator.py                 # 主入口
    ├── pyproject.toml
    ├── .venv/                       # uv 虚拟环境
    ├── metrics/
    │   ├── content_accuracy.py      # 维度1：内容准确性（先跑）
    │   ├── citation_relevance.py    # 维度2：引用相关性
    │   ├── instruction_following.py # 维度3：指令遵循
    │   └── writing_quality.py       # 维度4：写作质量
    ├── utils/
    │   ├── bib_parser.py            # BibTeX 解析 + tex 引用上下文提取
    │   ├── llm_client.py            # LLM API 封装（aihubmix）
    │   ├── paper_fetcher.py         # arXiv PDF 下载（带本地缓存）
    │   └── literature_search.py     # 文献搜索（Semantic Scholar，无 arXiv 时用于幻觉检测）
    ├── cache/                       # 下载的 PDF 文本缓存（自动生成）
    └── results/                     # 评测结果（自动生成，带任务名+时间戳）
        ├── eval_result_sudamuon_20260228_173606.json
        └── eval_report_sudamuon_20260228_173606.md
```

---

## 快速开始

```bash
cd eval-survey

# 激活虚拟环境
source eval/.venv/bin/activate

# 指定任务，运行完整评测（抽样加速）
python -m eval.evaluator --task sfedavg

# 查看最新结果
ls eval/results/
```

---

## 四维评测指标

### 总体设计思路

| 维度 | 类型 | 输出 | 方法 |
|------|------|------|------|
| 1. 内容准确性 | 客观 | 1-10 分 | 每篇独立打分（先跑） |
| 2. 引用相关性 | 客观 | 1-10 分 | 每篇独立打分 |
| 3. 指令遵循 | 主观 | -5 到 +5 相对分 | AB-BA 对称评测，子维度相对打分 |
| 4. 写作质量 | 主观 | -5 到 +5 相对分 | AB-BA 对称评测，子维度相对打分 |

维度 1/2 直接对每篇文章打分，可横向比较；维度 3/4 采用对称两轮比较，消除大模型对位置的偏好。评测时先跑内容准确性，再跑引用相关性（前者检测出的完全捏造会联动后者）。

**总分汇总（仅两篇文章时）**：
- `总分 = 内容准确性(1-10) + 引用相关性(1-10) + dim3相对优势分(0~5) + dim4相对优势分(0~5)`
- 满分 30 分；主观维度胜者获得 `|relative_score|` 的优势分，败者获得 0 分
- 使客观分数和主观胜负可以合并为一个可比较的单一总分

---

### 维度2：引用文献相关性

**目标**：检查 tex 中**实际引用**的每篇文献是否与 `survey_plan.md` 中要求的主题一致，重点考察对 Plan 中关键文献的覆盖情况。

> ⚠️ **只评估 tex 中被 `\cite{}` 引用的文献**，bib 文件中存在但未被引用的条目一律跳过，避免对未使用文献的误判。

**评测分两步进行**：

#### 步骤1：Key References 覆盖检查（全量，1次 LLM 调用）

将 Plan 中 "Key References" 列表与实际引用的全部论文（cite key + 标题）一次性交给 LLM，逐条判断是否被引用或有等价替代（如同一论文的 arXiv 版与会议版）。

这是总分的主体部分（0-7分），**两篇文章面对同一份 checklist，公平对比**，不受引用集合大小影响。

#### 步骤2：抽样质量打分（支持 `--sample`）

随机抽取若干引用，逐篇用 LLM 判断相关性（0/1/2），计算：
- **强相关比例** → 质量加分（0-2分）
- **不相关比例** → 偏题惩罚（超过 20% 才扣分，最多扣约 1.6 分）

少量偏题引用（<20%）不扣分，允许合理的"广泛背景覆盖"写作风格。

**相关性评分标准**：

| 分值 | 含义 |
|------|------|
| 2 | **强相关**：Plan Key References 中明确列出；该方向的核心代表性工作；直接激发本研究动机的背景工作 |
| 1 | **弱相关**：相邻技术领域，与主题有交叉但非核心；较宽泛的背景引用 |
| 0 | **不相关**：与 Plan 描述的所有核心方向均无明显关联 |

**总分计算**：

```
score = coverage_rate × 7          （覆盖分，0-7）
      + hr_rate × 2                 （质量加分，0-2）
      - max(0, irr_rate - 0.2) × 2  （偏题惩罚，超过20%不相关才扣）
```

结果 clamp 到 [0, 10] 后映射到 1-10 分。其中 hr\_rate 为抽样中强相关比例，irr\_rate 为不相关比例。

---

### 维度1：文献内容准确性（无幻觉）

**目标**：验证 tex 文件中对每篇引用论文的描述是否与原文一致，检测幻觉。

**验证模式**：

| 类型 | 条件 | 验证方式 |
|------|------|----------|
| 全文验证 | 有 arXiv ID（从 bib 的 `eprint`/`url`/`journal` 提取） | 下载 PDF，LLM 比对描述与原文 |
| S2+LLM 验证 | 无 arXiv ID | Semantic Scholar 检索 bib，LLM 根据摘要判断是否幻觉 |

**流程**：

1. 从 tex 文件提取每个 `\cite{}` 前后约 300 字符的上下文描述
2. 从 bib 条目中直接提取 arXiv ID（支持 `eprint`、`url`、`journal` 字段）
3. **有 arXiv ID**：通过 arXiv 下载 PDF，用 LLM 比对描述与原文（前 3000 字符）
4. **无 arXiv ID**：用 Semantic Scholar 按标题+作者检索，若找到匹配则用 LLM 比对描述与摘要；未找到则判为幻觉

**幻觉类型**：

| 类型 | 含义 |
|------|------|
| `wrong_metadata` | 作者、年份、会议等元信息错误 |
| `misrepresentation` | 内容描述与原文实质不符 |
| `exaggeration` | 夸大或歪曲论文贡献 |

**严重程度**：

| 分值 | 含义 |
|------|------|
| 0 | 无问题 |
| 1 | 轻微（不影响读者理解） |
| 2 | 严重（会误导读者） |

**总分计算**：只计入验证成功的条目，PDF 下载失败的记为未验证（不纳入得分），映射到 1-10 分。

> **维度1 / 维度2 联动**：当两个维度同时评测时，维度1（内容准确性）**先于**维度2（引用相关性）运行。维度1 检测出 `accuracy_level == 0`（完全捏造）的论文，其 cite key 集合会传递给维度2。维度2 在质量打分时直接将这些条目标记为 `relevance_score=0`（不相关），不参与 LLM 抽样，同时计入偏题惩罚。这样可以避免一篇根本不存在的论文影响相关性的讨论。

---

### 维度3：计划遵循度（Plan Adherence）

**目标**：评估 Related Works 是否正确遵循 `survey_plan.md` 的**内容要求**。纯内容覆盖检查，不涉及写作风格或语言质量判断。

**评测方法（AB-BA 对称 + 相对打分）**：

```
第一轮：文章A 在前，文章B 在后 → LLM 对每个子维度打 -2 到 +2 的相对分（正=A好）
第二轮：文章B 在前，文章A 在后 → LLM 对每个子维度打分后取反（统一为 article_a 视角）
最终：两轮平均，归一化到 [-5, +5]
```

对称设计消除大模型对"先读到的文章"的偏好；相对打分比"选出胜者"信息量更丰富，并可与客观分数合并为总分。

**评估子维度**：

| 子维度 | 检查点 | 相对分含义 |
|--------|--------|-----------|
| 主题覆盖 (topic_coverage) | Plan 要求讨论的每个研究方向是否有实质性讨论 | +2=A明显更全面 |
| 叙事脉络 (narrative_arc) | 叙述的逻辑推进顺序是否与 Plan 故事线一致 | +2=A明显更连贯 |
| 任务完成 (task_fulfillment) | Plan 的 Writing Requirements 中的具体指令是否被满足 | +2=A明显更完整 |

**设计要点**：关键文献覆盖已由维度2客观统计，本维度不重复评估。仅评估内容覆盖，不评写作风格。

---

### 维度4：学术写作质量（Writing Craft）

**目标**：评价作为**论文有机组成部分**的写作水平，而非作为独立综述的完整度。

**评测方法**：与维度3 相同的 AB-BA 对称两轮相对打分，归一化到 [-5, +5]。

**评价定位**：Related Works 是研究论文的一个章节，不是独立综述。顶级会议论文中，最好的 Related Works 用最少的篇幅传递最多的信息，每一句话都为论文的贡献服务。评价标准天然偏好高密度、论文嵌入式的写作风格。

**评估子维度**：

| 子维度 | 标准 | 相对分含义 |
|--------|------|-----------|
| 信息密度 (density) | 同等内容量下用更少篇幅完成 | +2=A明显更精炼 |
| 技术深度 (depth) | 讨论是否深入到方法机制、理论假设层面，而非"X 提出了 Y" | +2=A明显更深入 |
| 批判性综合 (synthesis) | 是否自然对比不同方法、指出联系和权衡；叙述中有机指出局限优于孤立标签 | +2=A明显更综合 |
| 动机涌现 (motivation) | 读完后读者是否自然理解为什么需要本文；动机有机涌现优于文末显式声明 | +2=A明显更自然 |

**设计要点**：冗余的显式格式标签和仅重复前文信息的 Gap 段落被视为负面因素，而非加分项。

---

## 使用方式

### 基本用法

```bash
cd eval-survey
source eval/.venv/bin/activate

# 默认评测（仅客观：内容准确性 + 引用相关性）
python -m eval.evaluator --task sudamuon

# 抽样加速（推荐日常使用）
python -m eval.evaluator --task sudamuon --sample 15

# 完整评测（含主观维度 3+4）
python -m eval.evaluator --task sudamuon --dim 1 2 3 4

# 只评测主观维度（快，约30秒）
python -m eval.evaluator --task sudamuon --dim 3 4

# 快速模式（跳过内容准确性）
python -m eval.evaluator --task sudamuon --quick
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--task` | 自动检测 | 任务名，对应 `sources/{task}/` 目录（如 `sudamuon`、`sfedavg`） |
| `--dim` | 1 2 | 要评测的维度，默认只做客观（1=内容准确性, 2=引用相关性），可加 3 4 做主观 |
| `--sample N` | 无（全量） | 维度1/2 的抽样数量（推荐 15-20） |
| `--seed N` | 42 | 随机种子，保证抽样可复现 |
| `--quick` | 否 | 跳过维度1（内容准确性） |
| `--config` | eval/config.yaml | 自定义配置文件路径 |
| `--eval-model` | 无 | 打分用 LLM 模型（消融：dpsk、gpt4o、sonnet4.6） |

### 速度参考（sudamuon 任务，ours 52条/reas 23条）

| 评测内容 | 抽样数 | 耗时估算 |
|----------|--------|---------|
| 维度1 内容准确性（仅有 arXiv ID 的条目） | 15 | ~3-5 分钟 |
| 维度2 引用相关性全量 | — | ~3 分钟 |
| 维度2 引用相关性抽样 | 15 | ~45 秒 |
| 维度3/4 | AB+BA 各2次 | ~30 秒 |

### 添加新任务

新建 `sources/{task}/` 目录，放入 `survey_plan.md` 和各 agent 的子目录：

```
sources/
└── new_task/
    ├── survey_plan.md       # 必须
    ├── agent_a/
    │   ├── related_works.tex
    │   └── references.bib
    └── agent_b/
        ├── related_works.tex
        └── references.bib
```

然后运行：

```bash
python -m eval.evaluator --task new_task --sample 15
```

### 添加新 agent

在已有任务目录下新建 agent 子目录，放入 tex 和 bib，系统自动发现：

```
sources/sudamuon/
├── survey_plan.md
├── ours/       # 已有
├── reas/       # 已有
└── new_agent/  # 新增，无需修改代码
    ├── related_works.tex
    └── references.bib
```

对于 3 篇文章，维度3/4 自动两两比较（`ours_vs_reas`、`ours_vs_new_agent`、`reas_vs_new_agent`）。

### 任务级评测配置（eval_config.yaml）

在任务目录下创建 `eval_config.yaml` 可覆盖默认行为：

```yaml
# 不抽样，全量评估（维度1/2）
no_sample: true

# 已知有效但无法被 S2/arXiv 确认的引用（如 blog、技术报告）
# 这些引用不会被判为捏造，引用相关性按正常流程评估
valid_non_academic_citations:
  - jordan2024muon  # 例：Muon 官方 blog，未在学术库收录
```

---

## 配置文件

`eval/config.yaml` 中可调整的关键参数：

```yaml
# LLM 模型配置（使用 aihubmix API）
llm:
  model: gpt-4o
  temperature: 0.3

# 评测配置
evaluation:
  objective:
    sample_size: 15             # 默认抽样数（--sample 优先级更高）
    seed: 42
    content_accuracy:
      max_papers_to_verify: 15

# 论文下载
paper_fetcher:
  max_chars: 50000              # PDF 提取的最大字符数
```

**环境变量**（可选）：在项目根目录创建 `.env`，或导出环境变量：
- `SEMANTIC_SCHOLAR_API_KEY`：用于无 arXiv 引用的 S2 检索，有 Key 时速率限制更宽松

---

## 输出格式

结果文件名带任务名和时间戳，同一任务多次运行不互相覆盖：

```
eval/results/
├── eval_result_sudamuon_20260228_173606.json
├── eval_report_sudamuon_20260228_173606.md
├── eval_result_sfedavg_20260228_180012.json
└── eval_report_sfedavg_20260228_180012.md
```

### JSON 结构（`eval_result_{task}_{timestamp}.json`）

```json
{
  "evaluation_time": "2026-02-28T17:36:06",
  "task": "sudamuon",
  "articles": ["ours", "reas"],
  "dimensions_evaluated": [1, 2, 3, 4],
  "objective_scores": {
    "ours": {
      "citation_relevance": {
        "score": 7.2,
        "total_citations": 42,
        "evaluated_citations": 15,
        "key_refs_total": 10,
        "key_refs_covered": 9,
        "coverage_rate": 0.9,
        "key_coverage": [
          {"key_ref": "SCAFFOLD (Karimireddy 2020)", "covered": true, "matched_cite_key": "karimireddy2020scaffold", "note": "..."},
          {"key_ref": "GoLore (He 2024)", "covered": false, "matched_cite_key": null, "note": "未找到等价引用"}
        ],
        "highly_relevant": 5,
        "weakly_relevant": 9,
        "irrelevant": 1,
        "details": [...]
      },
      "content_accuracy": {
        "score": 4.24,
        "total_citations": 37,
        "verified_citations": 5,
        "fulltext_verified": 5,
        "hallucination_count": 4,
        "hallucinations": [...]
      }
    }
  },
  "comparative_results": {
    "ours_vs_reas": {
      "instruction_following": { "final_winner": "ours", "round_ab": {...}, "round_ba": {...} },
      "writing_quality":        { "final_winner": "reas", "dimension_analysis": {...} }
    }
  },
  "summary": { ... }
}
```

### Markdown（`eval_report_{task}_{timestamp}.md`）

包含：执行摘要（排名/胜者）、各维度详细分数、幻觉问题清单、写作各维度分析。

---

## 注意事项

**维度1 内容准确性**：只有 bib 中带 arXiv ID 的文献才会被全文验证（如 `eprint` 或含 `arxiv.org` 的 `url`）。会议论文（NeurIPS/ICML）若 bib 中无 arXiv ID 则走 Semantic Scholar 检索 + LLM 判断。可在 bib 中补充 `eprint` 字段提高覆盖率。

**维度2 引用过滤**：系统自动跳过 bib 中存在但未被 tex 引用的条目，确保评分只针对实际使用的文献。

**Google Scholar**：已禁用（CAPTCHA 无法自动化）。**Semantic Scholar**：维度1 对无 arXiv ID 的引用使用 S2 检索 + LLM 判断幻觉，需配置 `SEMANTIC_SCHOLAR_API_KEY`（项目根目录 `.env` 或环境变量），有 Key 时速率限制更宽松。

**arXiv 下载缓存**：PDF 转换后缓存在 `eval/cache/text/`，重复运行自动复用，无需重新下载。

**可复现性**：抽样使用固定随机种子（默认 `--seed 42`），相同参数下每次结果一致。
