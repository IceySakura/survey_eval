# Related Works 评测报告

**评测时间**: 2026-03-27T12:31:01.991932
**打分模型**: gpt51
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_dpsk**: 9.58/10
2. **reasflow_gpt51**: 9.58/10
3. **reasflow_gpt54**: 8.8/10
4. **base_sonnet4.6**: 8.08/10
5. **reasflow_sonnet4.6**: 7.96/10
6. **base_gpt54**: 5.59/10
7. **base_gpt51**: 5.0/10
8. **base_dpsk**: 4.27/10

### 引用相关性排名（1-10分）
1. **base_sonnet4.6**: 9.39/10
2. **reasflow_dpsk**: 8.67/10
3. **reasflow_gpt51**: 7.12/10
4. **base_gpt54**: 6.73/10
5. **reasflow_gpt54**: 4.97/10
6. **reasflow_sonnet4.6**: 3.42/10
7. **base_dpsk**: 2.25/10
8. **base_gpt51**: 1.0/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **12.801** / 20
- 跨配置平均 · 内容准确性: **7.357** / 10
- 跨配置平均 · 引用相关性: **5.444** / 10
- 各配置总分（CA+CR）:
  - **reasflow_dpsk**: 18.25 / 20
  - **base_sonnet4.6**: 17.47 / 20
  - **reasflow_gpt51**: 16.7 / 20
  - **reasflow_gpt54**: 13.77 / 20
  - **base_gpt54**: 12.32 / 20
  - **reasflow_sonnet4.6**: 11.38 / 20
  - **base_dpsk**: 6.52 / 20
  - **base_gpt51**: 6.0 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 4.27/10
- 验证引用数: 15
- 幻觉数量: 11
- 下载失败跳过: 0

**发现的幻觉:**
- `huang2025limuon`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题名为“LiMuon: Light and Fast Muon Optimizer for Large Models”且作
- `jordanmuon`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中多篇论文讨论或扩展 Muon 优化器，但标题均非《Muon: A Matrix-Aware Optimizer for Dee
- `gruntkowska2025non`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有标题或作者与“Non-Euclidean Broximal Point Method: A Blueprint for G
- `wang2024proximal`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有标题或作者与“A Decentralized Proximal Gradient Tracking Algorithm f
- `zhu2024sparkle`: misrepresentation - [multi-cite保护] 被引用论文 SPARKLE 研究的是去中心化双层优化的单循环原始-对偶统一框架及其收敛率，并比较不同异质性校正策略（如 gradient tracking、EXTRA、E

**引用相关性**: 2.25/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 13（评估 15 条（其中 8 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 4
- 不相关: 8

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✗ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
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

**内容准确性**: 5.59/10
- 验证引用数: 15
- 幻觉数量: 9
- 下载失败跳过: 0

**发现的幻觉:**
- `grishina2025chebyshev`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与题为“Accelerating Newton-Schulz Iteration for Orthogonalizatio
- `sfyraki2025lionsmuons`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目或作者与“Lions and Muons: Optimization via Stochastic Frank-Wol
- `lau2025polargrad`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目或作者与“PolarGrad: A Class of Matrix-Gradient Optimizers from 
- `bernstein2024oldoptimizer`: misrepresentation - [multi-cite保护] 被引论文《Old Optimizer, New Norm: An Anthology》主要贡献是：在关闭 EMA 后，将 Adam、Shampoo、Prodigy 统一解
- `xin2021topologyindependent`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目和内容与“A Stochastic Proximal Gradient Framework for Decentral

**引用相关性**: 6.73/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 31（评估 15 条（其中 7 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 4
- 弱相关: 3
- 不相关: 8

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017dpsgd`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018) → `tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_sonnet4.6

**内容准确性**: 8.08/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `nedic2009distributed`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目为“Distributed Subgradient Methods for Multi-Agent Optimizat
- `chen2025muon_spectral`: misrepresentation - 原文明确表明，该论文的核心结果是：在将 Muon 置于 Lion-K 框架下，证明 Muon（带 decoupled weight decay）等价于在一个带谱范数约束的优化问题上进行隐式正则，并给出
- `he2025lowrank`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无一篇标题或作者与“Low-Rank Orthogonalization for Large-Scale Matrix Opt
- `yuan2021removing`: misrepresentation - 该论文确实研究了数据异质性对去中心化SGD（特别是D2/Exact-diffusion）的影响，并重点分析了网络拓扑相关量 1-β（谱间隙）如何影响收敛的“transient stage”。可以说它说

**引用相关性**: 9.39/10
- Key References 覆盖: 7/7 (100%)
- 总引用数: 23（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 5
- 弱相关: 8
- 不相关: 2

**Key References 覆盖详情:**
- ✓ Muon Optimizer (Jordan et al., 2024) → `jordan2024muon`
- ✓ Convergence of Muon (Shen et al., 2025) → `li2025note`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018) → `tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_dpsk

**内容准确性**: 9.58/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `He2024AdjacentLD`: misrepresentation - [multi-cite保护] 被引论文 He2024AdjacentLD（Adjacent Leader Decentralized Stochastic Gradient Descent）提出的是一
- `Alghunaim2023LocalEF`: misrepresentation - [multi-cite保护] 该文提出 Local Exact-Diffusion (LED)，是一种去中心化优化算法，通过 exact diffusion 机制和本地更新在去中心化网络上获得更好的收

**引用相关性**: 8.67/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 47（评估 15 条）
- 强相关: 5
- 弱相关: 8
- 不相关: 2

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `Lian2017AsynchronousDP`
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✓ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018) → `Tang2018D2DT`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt51

**内容准确性**: 9.58/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `Hinton2022TheFA`: misrepresentation - [multi-cite保护] 该句将 Hinton (2022) 作为“来自稀疏子空间聚类和局部训练表述的相关视角”的一部分引用。Hinton 这篇 Forward-Forward 论文的核心内容是提
- `wu2018group`: exaggeration - 引用语句中说“Works on group normalization ... underscore the importance of geometry and spectrum for repre

**引用相关性**: 7.12/10
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
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt54

**内容准确性**: 8.8/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `shazeer2018adafactor`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中均为与大模型训练、内存高效优化相关但不同题目的论文，没有题目或作者与“Adafactor: Adaptive Learning
- `Vogels2019PowerSGDPL`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib 条目只有作者和年份信息（Vogels, Karimireddy, Jaggi, 2019），而候选列表中没有任何一条作者或年份同

**引用相关性**: 4.97/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 38（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 10
- 不相关: 3

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_sonnet4.6

**内容准确性**: 7.96/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `Takezawa2025FedMuonFL`: misrepresentation - 描述中关于 FedMuon 的核心思想基本准确：原文确实指出直接在 FedAvg 中使用 Muon 会因 LMO 偏置而不收敛，并提出通过额外机制来纠正这种偏置，从而得到 FedMuon，并且分析了近
- `gupta2018shampoo`: misrepresentation - 该描述将 Shampoo 归入一个由 “Old Optimizer, New Norm” 框架统一的视角中，称 Adam、Shampoo、Prodigy 都可被解释为在特定算子范数下的最速下降。这一统
- `Kong2024DecentralizedBO`: misrepresentation - 被引论文 Kong2024DecentralizedBO 是关于去中心化随机双层优化（decentralized stochastic bilevel optimization）及其瞬态迭代复杂度分析
- `Goyal2017AccurateLM`: misrepresentation - 引用的 Goyal et al. 2017 论文是关于在集中式/同步数据并行架构下，用大规模 minibatch SGD 高效训练 ImageNet（ResNet-50）的方法，并未研究或提出任何去中
- `zhu2024apollo`: misrepresentation - 描述中两点：
1）"approximates AdamW's adaptivity via low-rank random projection"：这一点基本准确。APOLLO 通过辅助低秩随机投影状

**引用相关性**: 3.42/10
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
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`
