# Related Works 评测报告

**评测时间**: 2026-04-25T14:50:58.481758
**打分模型**: gpt54
**评测文章**: reasflow_basic_gpt54, reasflow_enhanced_gpt54
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_enhanced_gpt54**: 7.82/10
2. **reasflow_basic_gpt54**: 4.19/10

### 引用相关性排名（1-10分）
1. **reasflow_basic_gpt54**: 6.05/10
2. **reasflow_enhanced_gpt54**: 5.2/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **11.63** / 20
- 跨配置平均 · 内容准确性: **6.005** / 10
- 跨配置平均 · 引用相关性: **5.625** / 10
- 各配置总分（CA+CR）:
  - **reasflow_enhanced_gpt54**: 13.02 / 20
  - **reasflow_basic_gpt54**: 10.24 / 20

### 综合总分
> 总分 = 内容准确性(1-10) + 引用相关性(1-10)，满分20分
1. **reasflow_enhanced_gpt54**: 13.02 / 20
2. **reasflow_basic_gpt54**: 10.24 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### reasflow_basic_gpt54

**内容准确性**: 4.19/10
- 验证引用数: 15
- 幻觉数量: 8
- 下载失败跳过: 0

**发现的幻觉:**
- `sun2019worstcase`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选中没有与 2019 年、作者为 Ruoyu Sun 和 Yinyu Ye 的论文相符的条目。仅候选 0 同时包含两位作者，但年份为 
- `kiwiel1983aggregate`: fabricated - 候选共 3 条，LLM 判定无与 Bib 对应的论文。理由: 候选中没有与题名“An aggregate subgradient method for nonsmooth convex minimiz
- `held1974validation`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Validation of subgradient optimization。LLM: 候
- `burke1985descent`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Descent methods for composite nondifferentiab
- `renegar2019faster`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 6.05/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 14（评估 15 条（其中 8 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 7
- 弱相关: 0
- 不相关: 8

**Key References 覆盖详情:**
- ✓ Validation of subgradient optimization (Held, Wolfe, Crowder, 1973) → `held1974validation`
- ✗ An aggregate subgradient method for nonsmooth convex minimization (Kiwiel, 1985)
- ✓ Descent methods for composite nondifferentiable optimization (Fletcher, 1985) → `burke1985descent`
- ✓ Finite termination of the proximal point algorithm (1988) → `ferris1991finite`
- ✓ Douglas-Rachford splitting and proximal point algorithm for monotone operators (Eckstein, Bertsekas, 1992) → `eckstein1992douglas`
- ✗ Primal-dual subgradient methods for convex problems (Nesterov, 2007)
- ✓ Accelerating cubic regularization of Newton's method (Nesterov, 2008) → `nesterov2007accelerating`
- ✗ The effect of deterministic noise in subgradient methods (d'Aspremont, 2008)
- ✓ Convergence of descent methods for semi-algebraic and tame problems (Attouch, Bolte, Svaiter, 2013) → `attouch2013convergence`
- ✓ From error bounds to complexity of first-order descent methods (Bolte et al., 2016) → `bolte2016errorbounds`

#### reasflow_enhanced_gpt54

**内容准确性**: 7.82/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**发现的幻觉:**
- `Kiwiel_1983`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: An aggregate subgradient method for nonsmooth
- `Kim_1991`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Convergence of a generalized subgradient meth
- `Panier_1987`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: An active set method for solving linearly con
- `Kiwiel_1995`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Proximal level bundle methods for convex nond
- `unknown1998bundle`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: A bundle Bregman proximal method for convex n

**引用相关性**: 5.2/10
- Key References 覆盖: 2/10 (20%)
- 总引用数: 58（评估 15 条）
- 强相关: 6
- 弱相关: 9
- 不相关: 0

**Key References 覆盖详情:**
- ✗ Validation of subgradient optimization (Held, Wolfe, Crowder, 1973)
- ✓ An aggregate subgradient method for nonsmooth convex minimization (Kiwiel, 1985) → `Kiwiel_1983`
- ✗ Descent methods for composite nondifferentiable optimization (Fletcher, 1985)
- ✗ Finite termination of the proximal point algorithm (1988)
- ✗ Douglas-Rachford splitting and proximal point algorithm for monotone operators (Eckstein, Bertsekas, 1992)
- ✓ Primal-dual subgradient methods for convex problems (Nesterov, 2007) → `Nesterov_2007`
- ✗ Accelerating cubic regularization of Newton's method (Nesterov, 2008)
- ✗ The effect of deterministic noise in subgradient methods (d'Aspremont, 2008)
- ✗ Convergence of descent methods for semi-algebraic and tame problems (Attouch, Bolte, Svaiter, 2013)
- ✗ From error bounds to complexity of first-order descent methods (Bolte et al., 2016)
