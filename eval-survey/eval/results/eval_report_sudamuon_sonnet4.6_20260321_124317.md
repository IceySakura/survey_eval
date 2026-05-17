# Related Works 评测报告

**评测时间**: 2026-03-21T12:09:48.021147
**打分模型**: sonnet4.6
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_gpt54**: 10.0/10
2. **reasflow_dpsk**: 9.36/10
3. **base_gpt54**: 9.23/10
4. **base_sonnet4.6**: 8.96/10
5. **reasflow_sonnet4.6**: 8.93/10
6. **reasflow_gpt51**: 8.9/10
7. **base_dpsk**: 8.13/10
8. **base_gpt51**: 5.0/10

### 引用相关性排名（1-10分）
1. **base_sonnet4.6**: 9.94/10
2. **base_gpt54**: 8.84/10
3. **reasflow_dpsk**: 8.67/10
4. **reasflow_gpt51**: 6.97/10
5. **base_dpsk**: 5.3/10
6. **reasflow_gpt54**: 5.27/10
7. **reasflow_sonnet4.6**: 3.98/10
8. **base_gpt51**: 1.0/10

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 8.13/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `jordanmuon`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `yuan2021removing`: exaggeration - 描述称该论文实现了'network-topology-independent convergence rates'（与网络拓扑无关的收敛率），但这与论文实际内容不符。论文明确指出D²/Exact-di
- `amsel2025polar`: misrepresentation - The description cites amsel2025polar to support the claim that the matrix sign function can be 'appr
- `alghunaim2023local`: misrepresentation - 描述将该论文（alghunaim2023local）标注为 'Exact Diffusion (ED) / D²' 的原始提出论文，但实际上该论文提出的是 LED（Local Exact-Diffus
- `song2021optimal`: misrepresentation - 描述将该论文标注为'Gradient Tracking (GT)'，但实际上该论文提出的是'Optimal Gradient Tracking (OGT)'，是对GT方法的优化改进，同时达到梯度计算和

**引用相关性**: 5.3/10
- Key References 覆盖: 3/7 (43%)
- 总引用数: 20（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 8
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

**内容准确性**: 9.23/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `shazeer2018adafactor`: misrepresentation - [multi-cite保护] 描述将Adafactor归类为'curvature- or matrix-aware'方法，与K-FAC、Shampoo并列，暗示其核心是捕捉曲率或算子级几何结构，并称其
- `li2025note`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 8.84/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 37（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 8
- 弱相关: 6
- 不相关: 1

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017dpsgd`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018) → `yuan2019exactdiffusion / tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_sonnet4.6

**内容准确性**: 8.96/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 1

**发现的幻觉:**
- `amsel2025polar`: misrepresentation - The description attributes 'Newton-Schulz iterations' to this citation, but the paper's actual contr
- `nedic2009distributed`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Distributed Subgradient Methods for Multi-Age
- `he2025lowrank`: misrepresentation - 描述称该论文针对 foundation-model fine-tuning（微调），但实际上该论文明确针对 foundation model training（预训练），标题、摘要和实验（GPT-2 
- `yuan2021removing`: misrepresentation - The description states that Yuan et al. demonstrate data heterogeneity 'inflates the apparent spectr

**引用相关性**: 9.94/10
- Key References 覆盖: 7/7 (100%)
- 总引用数: 25（评估 15 条）
- 强相关: 8
- 弱相关: 7
- 不相关: 0

**Key References 覆盖详情:**
- ✓ Muon Optimizer (Jordan et al., 2024) → `jordan2024muon`
- ✓ Convergence of Muon (Shen et al., 2025) → `li2025note`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D2 (Yuan et al., 2017 / Tang et al., 2018) → `tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_dpsk

**内容准确性**: 9.36/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `Alghunaim2023LocalEF`: misrepresentation - 该论文（Alghunaim2023LocalEF）研究的是去中心化网络中的局部更新优化方法（Local Exact-Diffusion），与描述中所称的'matrix preconditioning 
- `Tang2018D2DT`: misrepresentation - [multi-cite保护] 描述将 Tang2018(D²) 归类为采用 gradient tracking 技术的方法，但 D² 的核心贡献是 variance reduction（方差缩减），而

**引用相关性**: 8.67/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 47（评估 15 条）
- 强相关: 5
- 弱相关: 9
- 不相关: 1

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `Lian2017AsynchronousDP`
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✓ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018) → `Tang2018D2DT`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt51

**内容准确性**: 8.9/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `Yang2015LearningW`: misrepresentation - 该论文确实是关于稀疏子空间聚类（sparse subspace clustering）的，这一标签是准确的。但描述将其置于联邦学习（federated learning）背景下，与'local-tra
- `Hinton2022TheFA`: misrepresentation - [multi-cite保护] Hinton's Forward-Forward Algorithm paper is about replacing backpropagation with two 
- `gupta2018shampoo`: misrepresentation - 第一处引用准确：将 Shampoo 描述为利用矩阵/张量结构的张量感知预条件器，与论文内容一致。但第二处引用存在实质性错误：Shampoo 被列入讨论 Push-Pull、时变图上加速方法和 DSGD

**引用相关性**: 6.97/10
- Key References 覆盖: 4/7 (57%)
- 总引用数: 64（评估 15 条）
- 强相关: 1
- 弱相关: 10
- 不相关: 4

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt54

**内容准确性**: 10.0/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**引用相关性**: 5.27/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 40（评估 15 条）
- 强相关: 2
- 弱相关: 12
- 不相关: 1

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_sonnet4.6

**内容准确性**: 8.93/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `Kong2024DecentralizedBO`: misrepresentation - 两处描述均存在实质性错误。第一处将 D-PSGD 的线性加速结果 O(σ/√nT) 归因于该论文，但该论文研究的是去中心化双层优化（D-SOBA），而非 D-PSGD；该论文确实讨论了谱间隙与瞬态复杂
- `Goyal2017AccurateLM`: misrepresentation - Goyal et al. (2017) 是关于集中式大批量分布式SGD的论文（线性学习率缩放+warmup策略，在256个GPU上训练ImageNet），与描述中'去中心化优化消除中心参数服务器、每个

**引用相关性**: 3.98/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 21（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 10
- 不相关: 2

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`
