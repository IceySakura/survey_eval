# Related Works 评测报告

**评测时间**: 2026-03-21T11:51:52.270572
**打分模型**: gpt51
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_dpsk**: 10.0/10
2. **reasflow_gpt54**: 9.83/10
3. **reasflow_gpt51**: 9.33/10
4. **base_sonnet4.6**: 9.2/10
5. **base_gpt54**: 8.63/10
6. **base_dpsk**: 7.96/10
7. **reasflow_sonnet4.6**: 7.49/10
8. **base_gpt51**: 5.0/10

### 引用相关性排名（1-10分）
1. **base_sonnet4.6**: 8.68/10
2. **reasflow_dpsk**: 8.53/10
3. **base_gpt54**: 8.5/10
4. **reasflow_gpt51**: 7.27/10
5. **reasflow_gpt54**: 5.27/10
6. **base_dpsk**: 4.77/10
7. **reasflow_sonnet4.6**: 3.6/10
8. **base_gpt51**: 1.0/10

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 7.96/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `huang2025limuon`: misrepresentation - [multi-cite保护] 相关描述中指出“Leading to empirically superior convergence in training large-scale models \c
- `jordanmuon`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `zhu2024sparkle`: misrepresentation - [multi-cite保护] 该句将一系列文献归为在其设定下实现了“network topology only affects higher-order terms in the convergenc
- `yuan2021removing`: misrepresentation - 原文系统性研究的是 D2 / Exact-diffusion 在去除数据异质性影响后，其收敛过程对网络拓扑的依赖如何减弱，并给出在不同凸性设定下的非渐近收敛率，结论是“拓扑依赖被显著减弱/得到最优（最
- `alghunaim2023local`: misrepresentation - 被引用论文提出的是 Local Exact-Diffusion (LED)，是对 Exact Diffusion 方法在本地更新场景下的扩展与分析，并非原始的 Exact Diffusion / D^

**引用相关性**: 4.77/10
- Key References 覆盖: 3/7 (43%)
- 总引用数: 20（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 12
- 不相关: 1

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `yuan2021unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_gpt51

**内容准确性**: 5.0/10
- 验证引用数: 0
- 幻觉数量: 0
- 下载失败跳过: 0

**引用相关性**: 1.0/10
- Key References 覆盖: 0/7 (0%)
- 总引用数: 0（评估 0 条）
- 强相关: 0
- 弱相关: 0
- 不相关: 0

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✗ DeMuon (He et al., 2025)

#### base_gpt54

**内容准确性**: 8.63/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `sfyraki2025lionsmuons`: misrepresentation - 被引论文 sfyraki2025lionsmuons 研究的是将 Lion 与 Muon 这类优化器统一为随机 Frank–Wolfe（投影‑free）方法，并给出相应的收敛性分析及在重尾噪声下的鲁棒
- `bernstein2024oldoptimizer`: misrepresentation - [multi-cite保护] 被引论文《Old Optimizer, New Norm: An Anthology》主要贡献是：在关闭 EMA 后，从一阶陡降/范数几何的角度统一理解 Adam、Sha
- `li2025note`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 8.5/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 36（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 7
- 不相关: 2

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017dpsgd`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018) → `tang2018d2 / yuan2019exactdiffusion`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_sonnet4.6

**内容准确性**: 9.2/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `nedic2009distributed`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Distributed Subgradient Methods for Multi-Age
- `chen2025muon_spectral`: misrepresentation - 该论文的核心结论是：在将 Muon 置于 Lion-K 框架下并选择适当的凸映射（核范数）时，可将其理解为在带有 decoupled weight decay 的情形下，隐式地求解一个带有谱范数约束的
- `he2025lowrank`: misrepresentation - 描述中说 He 等人的 low-rank orthogonalization 工作“targets foundation-model fine-tuning（针对大模型微调）”，而原文摘要与引言明确表

**引用相关性**: 8.68/10
- Key References 覆盖: 6/7 (86%)
- 总引用数: 25（评估 15 条）
- 强相关: 6
- 弱相关: 9
- 不相关: 0

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
- 幻觉数量: 3
- 下载失败跳过: 0

**引用相关性**: 8.53/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 47（评估 15 条）
- 强相关: 4
- 弱相关: 10
- 不相关: 1

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `Lian2017AsynchronousDP`
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✓ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018) → `Tang2018D2DT`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt51

**内容准确性**: 9.33/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `Yang2015LearningW`: misrepresentation - 当前句子只给出了一个非常概括性的归类：'Related perspectives from sparse subspace clustering and local-training formulat
- `Hinton2022TheFA`: misrepresentation - [multi-cite保护] 引用中将 Hinton (2022) 与 “sparse subspace clustering and local-training formulations” 并列，
- `Shi2013OnTL`: misrepresentation - [multi-cite保护] Shi 2013 这篇论文研究的是在分布式共识优化场景下，将 ADMM 应用于带强凸局部目标的去中心化共识问题，并给出线性收敛率的理论分析。它确实是关于“去中心化 ADM
- `Takezawa2025ScalableDL`: misrepresentation - [multi-cite保护] 该论文确实提出了一种名为 TELEPORTATION 的去中心化训练方法，通过只激活部分节点并从之前的活跃节点拉取参数、在小拓扑上做 gossip，从而缓解大规模网络中因

**引用相关性**: 7.27/10
- Key References 覆盖: 4/7 (57%)
- 总引用数: 64（评估 15 条）
- 强相关: 2
- 弱相关: 10
- 不相关: 3

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✗ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt54

**内容准确性**: 9.83/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `adam2014method`: misrepresentation - [multi-cite保护] 引用中将 Adam 归入“norm-based reinterpretations of first-order methods，cast Adam-like updat

**引用相关性**: 5.27/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 40（评估 15 条）
- 强相关: 2
- 弱相关: 11
- 不相关: 2

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_sonnet4.6

**内容准确性**: 7.49/10
- 验证引用数: 15
- 幻觉数量: 8
- 下载失败跳过: 0

**发现的幻觉:**
- `pethick2025training`: misrepresentation - 从给出的正文摘录可以确认：
1）论文确实是围绕线性最小化 oracle（LMO）在某个范数球上的优化框架展开，并声称可以统一/涵盖多种现有优化方法，这与“formalize this perspect
- `Hu2025ABD`: exaggeration - 描述中将 Hu2025 这篇论文归入“EXTRA, Exact Diffusion, D^2”等 exact-convergence 方法的同类，并暗示其在固定步长下也达到精确收敛到全局最优点；而原文
- `gupta2018shampoo`: misrepresentation - 该描述将 Shampoo 表述为在“Old Optimizer, New Norm”框架下、可被解释为某种算子范数下的最速下降方法的一员。但 2018 年的 Shampoo 论文本身并未以非欧几里得几
- `Kong2024DecentralizedBO`: misrepresentation - 被引论文 Kong2024DecentralizedBO（“Decentralized Bilevel Optimization: A Perspective from Transient Itera
- `loshchilov2017decoupled`: misrepresentation - 该论文提出并系统分析的是“解耦权重衰减”（AdamW/SGDW）这一优化与正则化方式，重点在于说明 L2 正则与权重衰减对自适应优化器并不等价，并展示其在图像分类等任务中提升 Adam 泛化性能。描述

**引用相关性**: 3.6/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 20（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 9
- 不相关: 4

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`
