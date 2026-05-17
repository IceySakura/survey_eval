# Related Works 评测报告

**评测时间**: 2026-03-27T12:44:33.320921
**打分模型**: dpsk
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **base_gpt51**: 10.0/10
2. **reasflow_gpt54**: 9.79/10
3. **reasflow_gpt51**: 9.4/10
4. **reasflow_dpsk**: 9.37/10
5. **reasflow_sonnet4.6**: 8.56/10
6. **base_sonnet4.6**: 5.98/10
7. **base_dpsk**: 5.38/10
8. **base_gpt54**: 4.6/10

### 引用相关性排名（1-10分）
1. **base_gpt51**: 9.0/10
2. **reasflow_dpsk**: 7.82/10
3. **reasflow_sonnet4.6**: 7.51/10
4. **reasflow_gpt51**: 7.04/10
5. **base_dpsk**: 6.49/10
6. **reasflow_gpt54**: 6.36/10
7. **base_sonnet4.6**: 5.06/10
8. **base_gpt54**: 4.39/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **14.594** / 20
- 跨配置平均 · 内容准确性: **7.885** / 10
- 跨配置平均 · 引用相关性: **6.709** / 10
- 各配置总分（CA+CR）:
  - **base_gpt51**: 19.0 / 20
  - **reasflow_dpsk**: 17.19 / 20
  - **reasflow_gpt51**: 16.44 / 20
  - **reasflow_gpt54**: 16.15 / 20
  - **reasflow_sonnet4.6**: 16.07 / 20
  - **base_dpsk**: 11.87 / 20
  - **base_sonnet4.6**: 11.04 / 20
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
- `xiang2023partial`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib条目标题为'Partial participation in federated learning: Algorithms and
- `mcmahan2017fedavg`: wrong_metadata - 描述中引用的论文标题为 'Federated learning of deep networks using model averaging'，作者为 Brendan McMahan 等人，年份为 2
- `stich2018sparsification`: misrepresentation - 描述将论文（Stich et al., 2018）的方法“top-k”归类为“biased/contractive compressors”。该论文确实分析了top-k等压缩方法，并证明了在结合误差补
- `zhang2022lightweight`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 所有候选论文的标题、作者和年份均与待匹配的Bib条目（标题：Lightweight local updates for computat
- `lian2017decentralized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者或年份均与待匹配条目（Decentralized parallel stochastic gradient

**引用相关性**: 6.49/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 30（评估 15 条（其中 7 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 6
- 不相关: 7

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019fedavg`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021fedavg`
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `tang2018d2`
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `stich2019errorfeedback`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `he2023lowerbounds`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✗ FedMuon — matrix orthogonalization in FL (Liu et al., 2025)
- ✓ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025) → `takezawa2025teleportation`

#### base_gpt51

**内容准确性**: 10.0/10
- 验证引用数: 15
- 幻觉数量: 0
- 下载失败跳过: 0

**引用相关性**: 9.0/10
- Key References 覆盖: 8/10 (80%)
- 总引用数: 42（评估 15 条）
- 强相关: 3
- 弱相关: 10
- 不相关: 2

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergencefedavg`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021linear`
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `tang2018d2`
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `karimireddy2019errorfeedback`
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
- `tyou2024localgecl`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者、年份均与查询的Bib条目（标题：A Localized Primal-Dual Method for C
- `sahu2021rethinking`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配条目（标题：Rethinking Gradient Sparsification as T
- `tinyfel2025`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 待匹配论文标题为 'TinyFEL: Communication, Computation, and Memory Efficient 
- `li2018fedprox`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 待匹配论文为 Li 等人 2020 年的 'Federated Optimization in Heterogeneous Networ
- `ghiasvand2024robust`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 待匹配论文标题为 'Robust Decentralized Learning With Local Updates and Gradi

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

**内容准确性**: 5.98/10
- 验证引用数: 15
- 幻觉数量: 8
- 下载失败跳过: 0

**发现的幻觉:**
- `wang2020tackling`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib 条目标题为 'Tackling the Objective Inconsistency Problem in Heterogen
- `dinh2020personalized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者、年份均与待匹配条目（标题：Personalized Federated Learning with Mo
- `fallah2020personalized`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配论文（标题为'Personalized Federated Learning with T
- `li2023analysis`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib条目标题核心要素为'Error Feedback in Federated Non-Convex Optimization wit
- `huang2022lower`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无标题、作者、年份均匹配的论文。Bib条目标题为'Lower Bounds and Nearly Optimal Algori

**引用相关性**: 5.06/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 20（评估 15 条（其中 6 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 3
- 不相关: 6

**Key References 覆盖详情:**
- ✗ FedAvg convergence under non-IID (Li et al., ICLR 2020)
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021achieving`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `karimireddy2019error`
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
- `daning2017weighted`: misrepresentation - 描述中提到“unbalanced workloads”并引用了该论文，这符合论文的核心主题（针对不平衡工作负载的分布式训练系统）。然而，描述将“unbalanced workloads”作为“syst
- `Tang2018D2DT`: misrepresentation - 描述中提到 'This drift phenomenon is exacerbated by system heterogeneity, including unbalanced workloads 
- `Rajbhandari2019ZeROMO`: misrepresentation - 描述称ZeRO“partition optimizer states but are designed for centralized training”。ZeRO确实对优化器状态（以及梯度和参数）进

**引用相关性**: 7.82/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 41（评估 15 条）
- 强相关: 2
- 弱相关: 9
- 不相关: 4

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

**内容准确性**: 9.4/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**发现的幻觉:**
- `xu2023determine`: wrong_metadata - 描述中引用的文献标识符为 'xu2023determine'，而提供的原始论文信息显示作者为 Kaijie Xu，年份为 2021，标题为 'How to Determine an Optimal N

**引用相关性**: 7.04/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 71（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 5
- 不相关: 8

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
- `Pagliardini2024TheAO`: misrepresentation - [multi-cite保护] 描述中提到论文的方法涉及“memory can either grow through extra moving averages or be shifted acros

**引用相关性**: 6.36/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 48（评估 15 条）
- 强相关: 3
- 弱相关: 7
- 不相关: 5

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

**内容准确性**: 8.56/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `su2023non`: wrong_metadata - 描述中存在关键事实错误。被引用的论文（su2023non）与当前审查的论文（标题：A Non-parametric View of FedAvg and FedProx: Beyond Station
- `Yuan2020FederatedAS`: misrepresentation - 描述中“further demonstrated that acceleration reduces synchronization rounds to $\mathcal{O}(M^{1/3})$ 
- `horvoth2022natural`: wrong_metadata - 描述中引用的年份（2022）和作者名（Horvoth）与原始论文信息不符。原始论文的arXiv版本标注为2019年（arXiv:1905.10988v3），作者为Samuel Horvath等。虽然该
- `mcmahan2017communication`: wrong_metadata - 描述中存在引用年份错误。原始论文的arXiv版本发布于2016年（v1），最终版本发布于2023年，但该论文在学术界通常被称为“McMahan 2016”或“McMahan et al., 2016”

**引用相关性**: 7.51/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 39（评估 15 条）
- 强相关: 4
- 弱相关: 8
- 不相关: 3

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
