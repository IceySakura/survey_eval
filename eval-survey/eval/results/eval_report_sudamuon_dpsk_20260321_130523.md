# Related Works 评测报告

**评测时间**: 2026-03-21T12:43:17.947930
**打分模型**: dpsk
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_dpsk**: 10.0/10
2. **reasflow_gpt54**: 9.4/10
3. **base_sonnet4.6**: 9.36/10
4. **base_dpsk**: 9.06/10
5. **base_gpt54**: 8.93/10
6. **reasflow_gpt51**: 8.76/10
7. **reasflow_sonnet4.6**: 8.43/10
8. **base_gpt51**: 5.0/10

### 引用相关性排名（1-10分）
1. **base_sonnet4.6**: 8.24/10
2. **reasflow_dpsk**: 8.07/10
3. **base_gpt54**: 7.84/10
4. **reasflow_gpt51**: 6.93/10
5. **base_gpt51**: 6.0/10
6. **base_dpsk**: 5.77/10
7. **reasflow_gpt54**: 4.19/10
8. **reasflow_sonnet4.6**: 2.51/10

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 9.06/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `jordanmuon`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `alghunaim2023local`: misrepresentation - 描述称“Exact Diffusion (ED) / D²”是一种“primal-dual formulation that provably removes heterogeneity influe
- `song2021optimal`: misrepresentation - 描述中“Maintains a tracking variable that estimates the global gradient, effectively compensating for l

**引用相关性**: 5.77/10
- Key References 覆盖: 4/7 (57%)
- 总引用数: 20（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 12
- 不相关: 1

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018) → `alghunaim2023local`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `yuan2021unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_gpt51

**内容准确性**: 5.0/10
- 验证引用数: 0
- 幻觉数量: 0
- 下载失败跳过: 0

**引用相关性**: 6.0/10
- Key References 覆盖: 6/7 (86%)
- 总引用数: 0（评估 0 条）
- 强相关: 0
- 弱相关: 0
- 不相关: 0

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025muon`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018) → `yuan2017exact`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_gpt54

**内容准确性**: 8.93/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `bernstein2024oldoptimizer`: misrepresentation - 描述将论文归入关于“矩阵正交化”和“基于矩阵符号算子的极化方向”的研究脉络中，这与论文的实际内容严重不符。论文《Old Optimizer, New Norm: An Anthology》的核心论点是
- `li2025note`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 7.84/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 37（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 7
- 不相关: 5

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017dpsgd`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018) → `tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_sonnet4.6

**内容准确性**: 9.36/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**发现的幻觉:**
- `nedic2009distributed`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Distributed Subgradient Methods for Multi-Age
- `he2025lowrank`: misrepresentation - 描述声称该论文“targets foundation-model fine-tuning rather than serverless decentralized training”。然而，根据提供的

**引用相关性**: 8.24/10
- Key References 覆盖: 6/7 (86%)
- 总引用数: 25（评估 15 条）
- 强相关: 4
- 弱相关: 7
- 不相关: 4

**Key References 覆盖详情:**
- ✓ Muon Optimizer (Jordan et al., 2024) → `jordan2024muon`
- ✗ Convergence of Muon (Shen et al., 2025)
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018) → `tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_dpsk

**内容准确性**: 10.0/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**引用相关性**: 8.07/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 47（评估 15 条）
- 强相关: 3
- 弱相关: 7
- 不相关: 5

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `Lian2017AsynchronousDP`
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✓ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018) → `Tang2018D2DT`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt51

**内容准确性**: 8.76/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `Yang2015LearningW`: misrepresentation - Related Works 中的描述将论文 'Learning with ℓ0-Graph: ℓ0-Induced Sparse Subspace Clustering' 归类为与 'local-tr
- `Hinton2022TheFA`: misrepresentation - 描述将Hinton2022TheFA（即本论文）与‘sparse subspace clustering and local-training formulations’并列引用，暗示其工作属于或支持
- `wu2018group`: exaggeration - Related Works 中的描述将论文 'Group Normalization' 置于一个关于 'geometry and spectrum for representation learnin

**引用相关性**: 6.93/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 63（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 2
- 不相关: 11

**Key References 覆盖详情:**
- ✓ Muon Optimizer (Jordan et al., 2024) → `wang2025muon`
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✗ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt54

**内容准确性**: 9.4/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `adam2014method`: wrong_metadata - 描述中称该论文（Adam: A Method for Stochastic Optimization）将Adam类更新解释为“在不同几何下的最速下降而非欧几里得SGD的微小变体”。然而，原始论文的核心

**引用相关性**: 4.19/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 39（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 4
- 不相关: 9

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_sonnet4.6

**内容准确性**: 8.43/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `Hu2025ABD`: misrepresentation - 描述存在实质性错误。论文提出的算法是“Exact-Diffusion with Momentum (EDM)”，它是在Exact Diffusion框架上结合了动量技术。然而，描述中声称“Gradie
- `abreu2025potential`: misrepresentation - 描述中引用的内容不完整且存在轻微偏差。原始描述为：'\citet{abreu2025potential} establish an empirical upper bound showing that
- `Kong2024DecentralizedBO`: misrepresentation - 描述中关于Kong2024DecentralizedBO的部分存在不准确之处。1) 论文标题为《Decentralized Bilevel Optimization: A Perspective fr
- `Goyal2017AccurateLM`: misrepresentation - 描述将论文错误归类为关于‘去中心化优化’的研究。原始论文《Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour》的核心贡献是提出线性缩放
- `he2025demuon`: misrepresentation - 描述中关于DeMuon的以下两点与原文存在偏差：1. 原文明确提出了DeMuon是第一个具有可证明复杂度保证的去中心化Muon扩展，而描述称其为“第一个去中心化Muon算法”，此表述在核心贡献上基本准

**引用相关性**: 2.51/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 21（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 2
- 不相关: 11

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`
