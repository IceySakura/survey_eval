# Related Works 评测报告

**评测时间**: 2026-03-27T12:44:31.914746
**打分模型**: sonnet4.6
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **base_gpt51**: 9.79/10
2. **reasflow_gpt51**: 9.79/10
3. **reasflow_gpt54**: 9.58/10
4. **reasflow_dpsk**: 9.28/10
5. **reasflow_sonnet4.6**: 8.98/10
6. **base_dpsk**: 6.56/10
7. **base_sonnet4.6**: 5.98/10
8. **base_gpt54**: 4.6/10

### 引用相关性排名（1-10分）
1. **base_gpt51**: 9.53/10
2. **reasflow_dpsk**: 8.97/10
3. **reasflow_sonnet4.6**: 8.89/10
4. **reasflow_gpt51**: 8.29/10
5. **base_dpsk**: 7.83/10
6. **reasflow_gpt54**: 7.43/10
7. **base_sonnet4.6**: 5.33/10
8. **base_gpt54**: 4.66/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **15.686** / 20
- 跨配置平均 · 内容准确性: **8.07** / 10
- 跨配置平均 · 引用相关性: **7.616** / 10
- 各配置总分（CA+CR）:
  - **base_gpt51**: 19.32 / 20
  - **reasflow_dpsk**: 18.25 / 20
  - **reasflow_gpt51**: 18.08 / 20
  - **reasflow_sonnet4.6**: 17.87 / 20
  - **reasflow_gpt54**: 17.01 / 20
  - **base_dpsk**: 14.39 / 20
  - **base_sonnet4.6**: 11.31 / 20
  - **base_gpt54**: 9.26 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 6.56/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 1

**发现的幻觉:**
- `xiang2023partial`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与标题'Partial participation in federated learning: Algorithms a
- `zhang2022lightweight`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Lightweight local updates for computational heterogeneity i
- `lian2017decentralized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Decentralized parallel stochastic gradient descent'（Xiangru
- `condat2022efbv`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'EF-BV: A unified theory of error feedback and variance red
- `neymeyer2012geometric`: misrepresentation - 论文确实建立了预条件最速下降迭代的几何收敛理论，这部分描述准确。但描述称该理论为'低秩近似提供了原则性基础'存在轻微偏差——原论文专注于广义特征值问题的收敛估计（结合Rayleigh-Ritz程序），

**引用相关性**: 7.83/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 32（评估 15 条（其中 5 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 8
- 弱相关: 2
- 不相关: 5

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019fedavg`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021fedavg`
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `tang2018d2`
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `stich2019errorfeedback, richtarik2021ef21`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `he2023lowerbounds`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✗ FedMuon — matrix orthogonalization in FL (Liu et al., 2025)
- ✓ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025) → `takezawa2025teleportation`

#### base_gpt51

**内容准确性**: 9.79/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `wang2019slowmo`: misrepresentation - 描述称SlowMo「improving robustness to stale or noisy local updates」，但论文实际强调的贡献是提升优化和泛化性能（optimization an

**引用相关性**: 9.53/10
- Key References 覆盖: 8/10 (80%)
- 总引用数: 42（评估 15 条）
- 强相关: 7
- 弱相关: 6
- 不相关: 2

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergencefedavg`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021linear`
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `tang2018d2`
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `karimireddy2019errorfeedback, richtarik2021ef21`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `he2023lowerboundsStoch`
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
- `tyou2024localgecl`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'A Localized Primal-Dual Method for Centralized/Decentralize
- `sahu2021rethinking`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Rethinking Gradient Sparsification as Total Error Minimizat
- `tinyfel2025`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'TinyFEL: Communication, Computation, and Memory Efficient T
- `li2018fedprox`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'Federated Optimization in Heterogeneous Networks'（Tian Li 
- `ghiasvand2024robust`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Robust Decentralized Learning With Local Updates and Gradie

**引用相关性**: 4.66/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 26（评估 15 条（其中 9 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 4
- 弱相关: 2
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

**内容准确性**: 5.98/10
- 验证引用数: 15
- 幻觉数量: 8
- 下载失败跳过: 0

**发现的幻觉:**
- `wang2020tackling`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Tackling the Objective Inconsistency Problem in Heterogeneo
- `dinh2020personalized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Personalized Federated Learning with Moreau Envelopes'（Dinh
- `fallah2020personalized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 Fallah et al. (2020) 的 'Personalized Federated Learning wit
- `koloskova2019decentralized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Decentralized Deep Learning with Arbitrary Communication Co
- `li2023analysis`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与目标论文（Analysis of Error Feedback in Federated Non-Convex Opti

**引用相关性**: 5.33/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 20（评估 15 条（其中 6 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 8
- 弱相关: 1
- 不相关: 6

**Key References 覆盖详情:**
- ✗ FedAvg convergence under non-IID (Li et al., ICLR 2020)
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021achieving`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `karimireddy2019error, richtarik2021ef21`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `he2023unbiased`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)

#### reasflow_dpsk

**内容准确性**: 9.28/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `koloskova2021improved`: wrong_metadata - 描述将该论文定位为梯度跟踪方法用于纠正去中心化设置中偏差的关键工作，与论文实际内容基本一致。但引用键为 'koloskova2021improved'，而该论文实际提交于2022年（arXiv:220
- `horvath2023stochastic`: misrepresentation - The description attributes 'error feedback and bias compensation mechanisms' to this paper, but the 

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

**内容准确性**: 9.79/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**发现的幻觉:**
- `ren2024low`: misrepresentation - 方法名称 'low-rank prune-and-factorize' 与论文标题完全一致，描述准确。但将该论文归类于 'reduce trainable parameters'（减少可训练参数，通常

**引用相关性**: 8.29/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 72（评估 15 条）
- 强相关: 7
- 弱相关: 3
- 不相关: 5

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergence`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✗ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019)
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `He2023LowerBA`
- ✓ GoLore — subspace optimization with convergence guarantees (He et al., 2024) → `pan2025unbiased`
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)

#### reasflow_gpt54

**内容准确性**: 9.58/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `yuan2020federated`: misrepresentation - 描述称该论文'highlights that structured constraints alter aggregation geometry rather than merely compress
- `su2023non`: misrepresentation - [multi-cite保护] 该论文（su2023non）的核心贡献是从非参数（RKHS）视角分析FedAvg和FedProx的收敛性与统计效率，证明这两种算法在异构设置下仍能达到最优误差率，并提出'

**引用相关性**: 7.43/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 48（评估 15 条）
- 强相关: 7
- 弱相关: 6
- 不相关: 2

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

**内容准确性**: 8.98/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `Zhang2022CCFedAvgCC`: misrepresentation - 描述将CC-FedAvg归类为处理'architectural heterogeneity（架构异构性）'的方法，但该论文实际上针对的是'computational heterogeneity（计算异
- `horvoth2022natural`: misrepresentation - 描述将 Natural Compression 归类为 'unbiased quantization schemes'（无偏量化方案），但实际上 Natural Compression 是一种有偏（b

**引用相关性**: 8.89/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 39（评估 15 条）
- 强相关: 8
- 弱相关: 7
- 不相关: 0

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergence`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `stich2018sparsified`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `He2023LowerBA`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)
