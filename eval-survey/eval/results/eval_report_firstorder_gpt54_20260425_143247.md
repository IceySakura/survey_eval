# Related Works 评测报告

**评测时间**: 2026-04-25T14:29:04.449497
**打分模型**: gpt54
**评测文章**: reasflow_basic_gpt54
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_basic_gpt54**: 4.62/10

### 引用相关性排名（1-10分）
1. **reasflow_basic_gpt54**: 7.12/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **11.74** / 20
- 跨配置平均 · 内容准确性: **4.62** / 10
- 跨配置平均 · 引用相关性: **7.12** / 10
- 各配置总分（CA+CR）:
  - **reasflow_basic_gpt54**: 11.74 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### reasflow_basic_gpt54

**内容准确性**: 4.62/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 0

**发现的幻觉:**
- `sun2019worstcase`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选中没有与“Ruoyu Sun, Yinyu Ye, 2019”相符的论文。仅有候选0同时包含这两位作者，但年份为2024且标题明显不
- `kiwiel1983aggregate`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: An Aggregate Subgradient Descent Method for S
- `held1974validation`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Validation of subgradient optimization。LLM: 候
- `burke1985descent`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Descent methods for composite nondifferentiab
- `renegar2019faster`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 7.12/10
- Key References 覆盖: 8/10 (80%)
- 总引用数: 15（评估 15 条（其中 7 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 8
- 弱相关: 0
- 不相关: 7

**Key References 覆盖详情:**
- ✓ Validation of subgradient optimization (Held, Wolfe, Crowder, 1973) → `held1974validation`
- ✓ An aggregate subgradient method for nonsmooth convex minimization (Kiwiel, 1985) → `kiwiel1983aggregate`
- ✓ Descent methods for composite nondifferentiable optimization (Fletcher, 1985) → `burke1985descent`
- ✓ Finite termination of the proximal point algorithm (1988) → `ferris1991finite`
- ✓ Douglas-Rachford splitting and proximal point algorithm for monotone operators (Eckstein, Bertsekas, 1992) → `eckstein1992douglas`
- ✗ Primal-dual subgradient methods for convex problems (Nesterov, 2007)
- ✓ Accelerating cubic regularization of Newton's method (Nesterov, 2008) → `nesterov2007accelerating`
- ✗ The effect of deterministic noise in subgradient methods (d'Aspremont, 2008)
- ✓ Convergence of descent methods for semi-algebraic and tame problems (Attouch, Bolte, Svaiter, 2013) → `attouch2013convergence`
- ✓ From error bounds to complexity of first-order descent methods (Bolte et al., 2016) → `bolte2016errorbounds`
