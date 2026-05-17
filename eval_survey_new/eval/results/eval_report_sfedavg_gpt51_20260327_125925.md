# Related Works 评测报告

**评测时间**: 2026-03-27T12:44:30.475095
**打分模型**: gpt51
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **base_gpt51**: 10.0/10
2. **reasflow_gpt51**: 10.0/10
3. **reasflow_gpt54**: 9.79/10
4. **reasflow_sonnet4.6**: 9.58/10
5. **reasflow_dpsk**: 9.37/10
6. **base_sonnet4.6**: 5.8/10
7. **base_dpsk**: 5.38/10
8. **base_gpt54**: 4.6/10

### 引用相关性排名（1-10分）
1. **base_gpt51**: 9.27/10
2. **reasflow_dpsk**: 8.97/10
3. **reasflow_gpt51**: 8.83/10
4. **reasflow_sonnet4.6**: 8.19/10
5. **reasflow_gpt54**: 7.3/10
6. **base_dpsk**: 6.32/10
7. **base_sonnet4.6**: 5.06/10
8. **base_gpt54**: 4.39/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **15.356** / 20
- 跨配置平均 · 内容准确性: **8.065** / 10
- 跨配置平均 · 引用相关性: **7.291** / 10
- 各配置总分（CA+CR）:
  - **base_gpt51**: 19.27 / 20
  - **reasflow_gpt51**: 18.83 / 20
  - **reasflow_dpsk**: 18.34 / 20
  - **reasflow_sonnet4.6**: 17.77 / 20
  - **reasflow_gpt54**: 17.09 / 20
  - **base_dpsk**: 11.7 / 20
  - **base_sonnet4.6**: 10.86 / 20
  - **base_gpt54**: 8.99 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 5.38/10
- 验证引用数: 15
- 幻觉数量: 9
- 下载失败跳过: 0

**发现的幻觉:**
- `xiang2023partial`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选条目中无一篇论文在标题、作者（Wei Xiang, Ming Li, Hao Chen）和年份上与“Partial particip
- `mcmahan2017fedavg`: wrong_metadata - 给出的原始论文内容是关于宇宙学中 constant-roll inflation 的理论与观测对比（arXiv:1702.05847，Motohashi & Starobinsky），与联邦学习或 F
- `he2023lowerbounds`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无标题为“Lower bounds and nearly optimal algorithms in distributed 
- `zhang2022lightweight`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题名或作者与“Lightweight local updates for computational heterogene
- `lian2017decentralized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有标题为或接近“Decentralized parallel stochastic gradient descent”，作者

**引用相关性**: 6.32/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 30（评估 15 条（其中 7 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 2
- 不相关: 7

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019fedavg`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021fedavg`
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `tang2018d2`
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `stich2019errorfeedback, richtarik2021ef21`
- ✗ Lower bounds for compressed distributed optimization (He et al., 2023)
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✗ FedMuon — matrix orthogonalization in FL (Liu et al., 2025)
- ✓ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025) → `takezawa2025teleportation`

#### base_gpt51

**内容准确性**: 10.0/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**引用相关性**: 9.27/10
- Key References 覆盖: 8/10 (80%)
- 总引用数: 42（评估 15 条）
- 强相关: 5
- 弱相关: 10
- 不相关: 0

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergencefedavg`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021linear`
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `tang2018d2`
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `karimireddy2019errorfeedback, richtarik2021ef21, zheng2019blockmomentumEF`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `he2022lowerbounds, he2023lowerboundsStoch`
- ✓ GoLore — subspace optimization with convergence guarantees (He et al., 2024) → `he2024subspaceLLM`
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✗ FedMuon — matrix orthogonalization in FL (Liu et al., 2025)
- ✓ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025) → `takezawa2025teleportation`

#### base_gpt54

**内容准确性**: 4.6/10
- 验证引用数: 15
- 幻觉数量: 9
- 下载失败跳过: 0

**发现的幻觉:**
- `tyou2024localgecl`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无题目或作者与“A Localized Primal-Dual Method for Centralized/Decentra
- `sahu2021rethinking`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目或作者与“Rethinking Gradient Sparsification as Total Error Mini
- `tinyfel2025`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有标题或作者、年份与“TinyFEL: Communication, Computation, and Memory Eff
- `li2018fedprox`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中不存在标题或作者与“Tian Li et al., 2020, Federated Optimization in Heter
- `ghiasvand2024robust`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选中虽有多篇关于去中心化梯度追踪/本地更新的论文，但均与给定题目和作者（Sajjad Ghiasvand 等, 2024）不符，未找到

**引用相关性**: 4.39/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 26（评估 15 条（其中 9 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 4
- 不相关: 9

**Key References 覆盖详情:**
- ✗ FedAvg convergence under non-IID (Li et al., ICLR 2020)
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2019scaffold`
- ✗ Linear speedup under partial participation (Yang et al., ICLR 2021)
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `tang2018d2`
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `richtarik2021ef21`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `huang2022lowerbounds`
- ✓ GoLore — subspace optimization with convergence guarantees (He et al., 2024) → `he2024subspace`
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✗ FedMuon — matrix orthogonalization in FL (Liu et al., 2025)
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)

#### base_sonnet4.6

**内容准确性**: 5.8/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 0

**发现的幻觉:**
- `wang2020tackling`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目或作者与《Tackling the Objective Inconsistency Problem in Hetero
- `dinh2020personalized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有标题或作者与“Personalized Federated Learning with Moreau Envelopes”
- `fallah2020personalized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目和作者同时与“Personalized Federated Learning with Theoretical Gua
- `koloskova2019decentralized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目为“Decentralized Deep Learning with Arbitrary Communication 
- `li2023analysis`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目和作者同时匹配“Analysis of Error Feedback in Federated Non-Convex 

**引用相关性**: 5.06/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 19（评估 15 条（其中 7 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 8
- 弱相关: 0
- 不相关: 7

**Key References 覆盖详情:**
- ✗ FedAvg convergence under non-IID (Li et al., ICLR 2020)
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021achieving`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `karimireddy2019error; richtarik2021ef21`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `he2023unbiased`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)

#### reasflow_dpsk

**内容准确性**: 9.37/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `horvath2023stochastic`: misrepresentation - 该论文确实研究了在分布式随机优化中结合梯度压缩（量化）和方差降低的算法，并讨论了压缩算子带来的附加方差 ω，属于广义上的“误差/方差补偿”类方法，用来稳定带压缩的训练。但描述中有两点偏差：
1）论文并
- `Cheng2023MomentumBN`: misrepresentation - 相关描述中有两点与原文存在偏差：
1）"Momentum has been shown to provably benefit FL under unbounded heterogeneity" 基本
- `Tang2018D2DT`: misrepresentation - 被引用论文 Tang2018D2DT 主要研究的是在去中心化数据分布下的去中心化 SGD（D2 算法），重点是当不同 worker 数据分布差异较大时收敛性能如何，以及通过方差缩减缓解这一问题。Rel

**引用相关性**: 8.97/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 41（评估 15 条）
- 强相关: 8
- 弱相关: 5
- 不相关: 2

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergence`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `Tang2018D2DT`
- ✗ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019)
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `He2023LowerBA`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)

#### reasflow_gpt51

**内容准确性**: 10.0/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**引用相关性**: 8.83/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 72（评估 15 条）
- 强相关: 7
- 弱相关: 6
- 不相关: 2

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergence`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `Fatkhullin2023MomentumPI`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `He2023LowerBA`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)

#### reasflow_gpt54

**内容准确性**: 9.79/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `yuan2020federated`: misrepresentation - 该论文确实研究了带非光滑正则项/结构化约束（如稀疏、低秩、单调性或一般约束）的联邦复合优化问题，并指出现有如 FedAvg 的“朴素扩展”在此类情形下不适用，提出 FedDualAvg 以更好地处理这

**引用相关性**: 7.3/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 48（评估 15 条）
- 强相关: 6
- 弱相关: 8
- 不相关: 1

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergence`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✗ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019)
- ✗ Lower bounds for compressed distributed optimization (He et al., 2023)
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)

#### reasflow_sonnet4.6

**内容准确性**: 9.58/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `Zhang2022CCFedAvgCC`: misrepresentation - 该文确实提出了一个在联邦学习中针对计算资源异质性的“computation‑customized”变体 CC-FedAvg，用以降低本地计算开销，这与描述中“computation-customize
- `reguieg2023comparative`: misrepresentation - [multi-cite保护] 被引论文 Reguieg et al. 2023 的工作是比较 FedAvg 与 Per-FedAvg 在 Dirichlet 异质数据上的表现，属于个性化联邦学习算法的

**引用相关性**: 8.19/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 39（评估 15 条）
- 强相关: 8
- 弱相关: 7
- 不相关: 0

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergence`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✗ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019)
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `He2023LowerBA`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)
