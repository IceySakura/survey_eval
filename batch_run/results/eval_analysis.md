# 评测结果汇总与消融分析

**总分定义**：每篇生成配置 = 内容准确性(0–10) + 引用相关性(0–10)，最高 20。
**Leaderboard 排名依据**：固定任务，对**每个生成配置**取各评测模型下的篇总分，再对**已有评测**求算术平均（通常为三套评测）；**任务内**按该均值降序排名。
细粒度矩阵见 `eval_matrix_by_task.csv`；同构排名表见 `eval_leaderboard.csv`。

## 1. Leaderboard（按任务：生成配置 × 跨评测均分，降序排名）

### 1.1 任务 `cuttingplane`

| 排名 | 生成配置 | agent | backbone | gpt51 | sonnet4.6 | dpsk | 跨评测均值 |
| --- | --- | --- | --- | --- | --- | --- | --- |

### 1.2 任务 `firstorder`

| 排名 | 生成配置 | agent | backbone | gpt51 | sonnet4.6 | dpsk | 跨评测均值 |
| --- | --- | --- | --- | --- | --- | --- | --- |

### 1.3 任务 `sfedavg`

| 排名 | 生成配置 | agent | backbone | gpt51 | sonnet4.6 | dpsk | 跨评测均值 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | base_gpt51 | base | gpt51 | 19.23 | 19.53 | 19.0 | 19.253 |
| 2 | reasflow_gpt51 | reasflow | gpt51 | 18.13 | 18.16 | 17.03 | 17.773 |
| 3 | base_gpt54 | base | gpt54 | 16.42 | 16.73 | 16.59 | 16.58 |
| 4 | base_sonnet4.6 | base | sonnet4.6 | 16.55 | 16.64 | 15.98 | 16.39 |
| 5 | reasflow_dpsk | reasflow | dpsk | 16.73 | 17.06 | 15.13 | 16.307 |
| 6 | base_dpsk | base | dpsk | 16.24 | 16.27 | 14.87 | 15.793 |
| 7 | reasflow_sonnet4.6 | reasflow | sonnet4.6 | 15.71 | 16.47 | 15.04 | 15.74 |
| 8 | reasflow_gpt54 | reasflow | gpt54 | 15.1 | 15.76 | 14.36 | 15.073 |

### 1.4 任务 `subspacescaffold`

| 排名 | 生成配置 | agent | backbone | gpt51 | sonnet4.6 | dpsk | 跨评测均值 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | base_sonnet4.6 | base | sonnet4.6 | 18.17 | 18.13 | 17.69 | 17.997 |
| 2 | base_dpsk | base | dpsk | 17.11 | 17.99 | 16.96 | 17.353 |
| 3 | base_gpt54 | base | gpt54 | 17.04 | 17.85 | 16.48 | 17.123 |
| 4 | base_gpt51 | base | gpt51 | 16.57 | 17.12 | 15.16 | 16.283 |
| 5 | reasflow_gpt51 | reasflow | gpt51 | 16.09 | 15.56 | 15.12 | 15.59 |
| 6 | reasflow_gpt54 | reasflow | gpt54 | 14.71 | 16.23 | 14.15 | 15.03 |
| 7 | reasflow_sonnet4.6 | reasflow | sonnet4.6 | 14.83 | 14.79 | 13.82 | 14.48 |
| 8 | reasflow_dpsk | reasflow | dpsk | 13.62 | 14.19 | 12.81 | 13.54 |

### 1.5 任务 `sudamuon`

| 排名 | 生成配置 | agent | backbone | gpt51 | sonnet4.6 | dpsk | 跨评测均值 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | reasflow_dpsk | reasflow | dpsk | 18.53 | 18.03 | 18.07 | 18.21 |
| 2 | base_sonnet4.6 | base | sonnet4.6 | 17.88 | 18.9 | 17.6 | 18.127 |
| 3 | base_gpt54 | base | gpt54 | 17.13 | 18.07 | 16.77 | 17.323 |
| 4 | reasflow_gpt51 | reasflow | gpt51 | 16.6 | 15.87 | 15.69 | 16.053 |
| 5 | reasflow_gpt54 | reasflow | gpt54 | 15.1 | 15.27 | 13.59 | 14.653 |
| 6 | base_dpsk | base | dpsk | 12.73 | 13.43 | 14.83 | 13.663 |
| 7 | reasflow_sonnet4.6 | reasflow | sonnet4.6 | 11.09 | 12.91 | 10.94 | 11.647 |
| 8 | base_gpt51 | base | gpt51 | 6.0 | 6.0 | 11.0 | 7.667 |

## 2. 消融：Agent（base vs reasflow）
同一任务、同一评测模型下，对所有生成 backbone 的篇总分取平均。

| 任务 | 评测模型 | base 平均总分 | reasflow 平均总分 | 差(reasflow−base) |
| --- | --- | --- | --- | --- |
| sfedavg | dpsk | 16.61 | 15.39 | -1.22 |
| sfedavg | gpt51 | 17.11 | 16.418 | -0.692 |
| sfedavg | sonnet4.6 | 17.293 | 16.863 | -0.43 |
| subspacescaffold | dpsk | 16.572 | 13.975 | -2.597 |
| subspacescaffold | gpt51 | 17.223 | 14.812 | -2.41 |
| subspacescaffold | sonnet4.6 | 17.773 | 15.193 | -2.58 |
| sudamuon | dpsk | 15.05 | 14.572 | -0.478 |
| sudamuon | gpt51 | 13.435 | 15.33 | 1.895 |
| sudamuon | sonnet4.6 | 14.1 | 15.52 | 1.42 |

## 3. 消融：同 backbone 配对（base_* vs reasflow_*）

| 任务 | backbone | 评测模型 | base 总分 | reasflow 总分 | 差 |
| --- | --- | --- | --- | --- | --- |
| sfedavg | dpsk | dpsk | 14.87 | 15.13 | 0.26 |
| sfedavg | dpsk | gpt51 | 16.24 | 16.73 | 0.49 |
| sfedavg | dpsk | sonnet4.6 | 16.27 | 17.06 | 0.79 |
| sfedavg | gpt51 | dpsk | 19.0 | 17.03 | -1.97 |
| sfedavg | gpt51 | gpt51 | 19.23 | 18.13 | -1.1 |
| sfedavg | gpt51 | sonnet4.6 | 19.53 | 18.16 | -1.37 |
| sfedavg | gpt54 | dpsk | 16.59 | 14.36 | -2.23 |
| sfedavg | gpt54 | gpt51 | 16.42 | 15.1 | -1.32 |
| sfedavg | gpt54 | sonnet4.6 | 16.73 | 15.76 | -0.97 |
| sfedavg | sonnet4.6 | dpsk | 15.98 | 15.04 | -0.94 |
| sfedavg | sonnet4.6 | gpt51 | 16.55 | 15.71 | -0.84 |
| sfedavg | sonnet4.6 | sonnet4.6 | 16.64 | 16.47 | -0.17 |
| subspacescaffold | dpsk | dpsk | 16.96 | 12.81 | -4.15 |
| subspacescaffold | dpsk | gpt51 | 17.11 | 13.62 | -3.49 |
| subspacescaffold | dpsk | sonnet4.6 | 17.99 | 14.19 | -3.8 |
| subspacescaffold | gpt51 | dpsk | 15.16 | 15.12 | -0.04 |
| subspacescaffold | gpt51 | gpt51 | 16.57 | 16.09 | -0.48 |
| subspacescaffold | gpt51 | sonnet4.6 | 17.12 | 15.56 | -1.56 |
| subspacescaffold | gpt54 | dpsk | 16.48 | 14.15 | -2.33 |
| subspacescaffold | gpt54 | gpt51 | 17.04 | 14.71 | -2.33 |
| subspacescaffold | gpt54 | sonnet4.6 | 17.85 | 16.23 | -1.62 |
| subspacescaffold | sonnet4.6 | dpsk | 17.69 | 13.82 | -3.87 |
| subspacescaffold | sonnet4.6 | gpt51 | 18.17 | 14.83 | -3.34 |
| subspacescaffold | sonnet4.6 | sonnet4.6 | 18.13 | 14.79 | -3.34 |
| sudamuon | dpsk | dpsk | 14.83 | 18.07 | 3.24 |
| sudamuon | dpsk | gpt51 | 12.73 | 18.53 | 5.8 |
| sudamuon | dpsk | sonnet4.6 | 13.43 | 18.03 | 4.6 |
| sudamuon | gpt51 | dpsk | 11.0 | 15.69 | 4.69 |
| sudamuon | gpt51 | gpt51 | 6.0 | 16.6 | 10.6 |
| sudamuon | gpt51 | sonnet4.6 | 6.0 | 15.87 | 9.87 |
| sudamuon | gpt54 | dpsk | 16.77 | 13.59 | -3.18 |
| sudamuon | gpt54 | gpt51 | 17.13 | 15.1 | -2.03 |
| sudamuon | gpt54 | sonnet4.6 | 18.07 | 15.27 | -2.8 |
| sudamuon | sonnet4.6 | dpsk | 17.6 | 10.94 | -6.66 |
| sudamuon | sonnet4.6 | gpt51 | 17.88 | 11.09 | -6.79 |
| sudamuon | sonnet4.6 | sonnet4.6 | 18.9 | 12.91 | -5.99 |

## 4. 评测可靠性（三评测模型与组内均值的偏差）
对 **24** 个 (任务, 生成配置) 三元组，计算三评测打分的均值 $\mu$，
再算各评测模型的 $\sum (s-\mu)^2$（越小表示越接近三者的「共识中心」）。

| 评测模型 | 偏差平方和 SSD | 解释 |
| --- | --- | --- |
| gpt51 | 5.877 | 最小 → 相对最接近三评测平均 |
| sonnet4.6 | 11.751 |  |
| dpsk | 22.747 |  |

**结论**：SSD 最小为 **`gpt51`**（=5.877），在「与三模型均值距离」意义上最居中；注意这不等于「更正确」，仅衡量三评测一致性。