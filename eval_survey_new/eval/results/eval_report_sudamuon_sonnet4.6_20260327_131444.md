# Related Works 评测报告

**评测时间**: 2026-03-27T12:44:28.027620
**打分模型**: sonnet4.6
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_dpsk**: 9.58/10
2. **reasflow_sonnet4.6**: 9.31/10
3. **reasflow_gpt51**: 9.07/10
4. **reasflow_gpt54**: 8.8/10
5. **base_sonnet4.6**: 8.08/10
6. **base_gpt54**: 5.8/10
7. **base_gpt51**: 5.0/10
8. **base_dpsk**: 4.18/10

### 引用相关性排名（1-10分）
1. **base_sonnet4.6**: 9.79/10
2. **reasflow_dpsk**: 8.67/10
3. **base_gpt54**: 7.19/10
4. **reasflow_gpt51**: 6.79/10
5. **reasflow_gpt54**: 5.1/10
6. **reasflow_sonnet4.6**: 3.98/10
7. **base_dpsk**: 3.38/10
8. **base_gpt51**: 1.0/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **13.215** / 20
- 跨配置平均 · 内容准确性: **7.478** / 10
- 跨配置平均 · 引用相关性: **5.737** / 10
- 各配置总分（CA+CR）:
  - **reasflow_dpsk**: 18.25 / 20
  - **base_sonnet4.6**: 17.87 / 20
  - **reasflow_gpt51**: 15.86 / 20
  - **reasflow_gpt54**: 13.9 / 20
  - **reasflow_sonnet4.6**: 13.29 / 20
  - **base_gpt54**: 12.99 / 20
  - **base_dpsk**: 7.56 / 20
  - **base_gpt51**: 6.0 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 4.18/10
- 验证引用数: 15
- 幻觉数量: 10
- 下载失败跳过: 0

**发现的幻觉:**
- `huang2025limuon`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'LiMuon: Light and Fast Muon Optimizer for Large Models'（作者
- `jordanmuon`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Muon: A Matrix-Aware Optimizer for Deep Learning'（作者 Michae
- `gruntkowska2025non`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Non-Euclidean Proximal Point Method: A Blueprint for Geomet
- `wang2024proximal`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与目标论文'A Decentralized Proximal Gradient Tracking Algorithm fo
- `grishina2025accelerating`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Accelerating Newton-Schulz Iteration for Orthogonalization 

**引用相关性**: 3.38/10
- Key References 覆盖: 3/7 (43%)
- 总引用数: 13（评估 15 条（其中 8 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 4
- 弱相关: 3
- 不相关: 8

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✗ Exact Diffusion / D2 (Yuan et al., 2017 / Tang et al., 2018)
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

**内容准确性**: 5.8/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 0

**发现的幻觉:**
- `grishina2025chebyshev`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Accelerating Newton-Schulz Iteration for Orthogonalization 
- `sfyraki2025lionsmuons`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'Lions and Muons: Optimization via Stochastic Frank-Wolfe'（
- `lau2025polargrad`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'PolarGrad: A Class of Matrix-Gradient Optimizers from a Uni
- `xin2021topologyindependent`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与目标论文'A Stochastic Proximal Gradient Framework for Decentrali
- `shazeer2018adafactor`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'Adafactor: Adaptive Learning Rates with Sublinear Memory C

**引用相关性**: 7.19/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 31（评估 15 条（其中 7 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 2
- 不相关: 7

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017dpsgd`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018) → `yuan2019exactdiffusion, tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_sonnet4.6

**内容准确性**: 8.08/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `nedic2009distributed`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 Nedić 和 Ozdaglar 2009年发表的 'Distributed Subgradient Methods 
- `chen2025muon_spectral`: misrepresentation - 描述称该论文证明 Muon '在每一步隐式求解一个谱范数约束的信赖域子问题（trust-region subproblem at each step）'，但实际上该论文的核心贡献是：通过将 Muon 
- `he2025lowrank`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Low-Rank Orthogonalization for Large-Scale Matrix Optimizat
- `yuan2021removing`: misrepresentation - The description states that the paper shows data heterogeneity 'inflates the apparent spectral gap o

**引用相关性**: 9.79/10
- Key References 覆盖: 7/7 (100%)
- 总引用数: 23（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 8
- 弱相关: 5
- 不相关: 2

**Key References 覆盖详情:**
- ✓ Muon Optimizer (Jordan et al., 2024) → `jordan2024muon`
- ✓ Convergence of Muon (Shen et al., 2025) → `li2025note`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D2 (Yuan et al., 2017 / Tang et al., 2018) → `tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_dpsk

**内容准确性**: 9.58/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `Alghunaim2023LocalEF`: misrepresentation - [multi-cite保护] 描述将该论文归类为展示'矩阵预处理（matrix preconditioning）可加速分布式收敛'的工作，但该论文（LED）的核心贡献是局部更新（local updat
- `Tang2018D2DT`: misrepresentation - [multi-cite保护] D² 的核心贡献是方差缩减（variance reduction）扩展，用于降低不同 worker 间数据异质性带来的收敛问题。然而，描述将 Tang2018D2DT（即

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

**内容准确性**: 9.07/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 0

**发现的幻觉:**
- `Yang2015LearningW`: misrepresentation - 该论文确实是关于稀疏子空间聚类（sparse subspace clustering）的，描述中提到'sparse subspace clustering'这一部分与论文内容一致。然而，将其与'loc
- `Hinton2022TheFA`: misrepresentation - [multi-cite保护] Hinton的Forward-Forward算法论文是关于用两次前向传播替代反向传播的神经网络学习方法，与描述中所指的'稀疏子空间聚类'和联邦学习语境下的'局部训练公式'
- `gupta2018shampoo`: misrepresentation - 第一处引用准确：将Shampoo描述为利用矩阵/张量结构的经典张量感知预条件器，与论文内容一致。但第二处引用将Shampoo与PushPull、DSGD-CECA等分布式优化方法并列，描述其'细化谱依

**引用相关性**: 6.79/10
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

**内容准确性**: 8.8/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `shazeer2018adafactor`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'Adafactor: Adaptive Learning Rates with Sublinear Memory C
- `Vogels2019PowerSGDPL`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 Thijs Vogels, Sai Praneeth Karimireddy, Martin Jaggi (2019)

**引用相关性**: 5.1/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 38（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 9
- 不相关: 3

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_sonnet4.6

**内容准确性**: 9.31/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 2

**发现的幻觉:**
- `Goyal2017AccurateLM`: misrepresentation - Goyal et al. (2017) 是关于集中式大批量分布式SGD训练的论文，其核心贡献是线性学习率缩放规则和warmup策略，用于中心化的分布式训练（256个GPU集中训练）。然而描述将其引用来

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
