# Related Works 评测报告

**评测时间**: 2026-03-21T13:05:23.703556
**打分模型**: gpt51
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_gpt51**: 10.0/10
2. **base_gpt51**: 9.83/10
3. **base_gpt54**: 9.5/10
4. **base_sonnet4.6**: 9.5/10
5. **reasflow_gpt54**: 8.63/10
6. **reasflow_sonnet4.6**: 8.63/10
7. **reasflow_dpsk**: 8.6/10
8. **base_dpsk**: 7.86/10

### 引用相关性排名（1-10分）
1. **base_gpt51**: 9.4/10
2. **base_dpsk**: 8.38/10
3. **reasflow_dpsk**: 8.13/10
4. **reasflow_gpt51**: 8.13/10
5. **reasflow_sonnet4.6**: 7.08/10
6. **base_sonnet4.6**: 7.05/10
7. **base_gpt54**: 6.92/10
8. **reasflow_gpt54**: 6.47/10

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 7.86/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `xiang2023partial`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目和作者同时与“Partial participation in federated learning: Algorit
- `mcmahan2017fedavg`: wrong_metadata - 描述中的论文元数据与给出的原始论文内容完全不符。Related Works 描述的是联邦学习中的 FedAvg 算法（McMahan 等 2017，联邦学习、通信效率、局部 SGD 与服务器聚合等），
- `zhang2022lightweight`: fabricated - 候选共 3 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中的论文在标题、作者及年份上均与给定 Bib 条目不符，因此没有同一篇论文的合理匹配。
- `karimireddy2020scaffold`: exaggeration - 描述中两点需要区分：
1）关于方法本身：描述称 SCAFFOLD 使用 control variates（方差减少技术）来纠正 client drift，这与原文完全一致，SCAFFOLD 确实通过控
- `neymeyer2012geometric`: misrepresentation - 该文确实给出了预条件最速下降（用于对称正定广义特征值问题）的几何收敛理论，讨论了收敛率与预条件器等的关系，因此说其提供了“geometric convergence theory of precond

**引用相关性**: 8.38/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 34（评估 15 条（其中 3 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 7
- 弱相关: 5
- 不相关: 3

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019fedavg`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021fedavg`
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `tang2018d2`
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `stich2019errorfeedback / richtarik2021ef21`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `he2023lowerbounds`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✗ FedMuon — matrix orthogonalization in FL (Liu et al., 2025)
- ✓ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025) → `takezawa2025teleportation`

#### base_gpt51

**内容准确性**: 9.83/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `xie2024MHpFLID`: misrepresentation - [multi-cite保护] 相关描述中有两处与原文不符：
1) 上文将 xie2024MHpFLID 归入“利用蒸馏式个性化和聚类（clustering）处理系统和模型异质性”的工作之列，而 MH-

**引用相关性**: 9.4/10
- Key References 覆盖: 8/10 (80%)
- 总引用数: 42（评估 15 条）
- 强相关: 6
- 弱相关: 9
- 不相关: 0

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2019convergencefedavg`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `yang2021linear`
- ✓ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018) → `tang2018d2`
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `karimireddy2019errorfeedback / richtarik2021ef21`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `he2023lowerboundsStoch`
- ✓ GoLore — subspace optimization with convergence guarantees (He et al., 2024) → `he2024subspaceLLM`
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✗ FedMuon — matrix orthogonalization in FL (Liu et al., 2025)
- ✓ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025) → `takezawa2025teleportation`

#### base_gpt54

**内容准确性**: 9.5/10
- 验证引用数: 15
- 幻觉数量: 0
- 下载失败跳过: 0

**发现的幻觉:**
- `tyou2024localgecl`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: A Localized Primal-Dual Method for Centralize
- `tinyfel2025`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: TinyFEL: Communication, Computation, and Memo
- `alistarh2016qsgd`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: QSGD: Communication-Efficient SGD via Gradien

**引用相关性**: 6.92/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 35（评估 15 条）
- 强相关: 6
- 弱相关: 9
- 不相关: 0

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

**内容准确性**: 9.5/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**发现的幻觉:**
- `fallah2020personalized`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Personalized Federated Learning with Theoreti
- `koloskova2019decentralized`: misrepresentation - 第一处描述："\citet{koloskova2019decentralized} show that arbitrary communication compression can be incor
- `li2023analysis`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Analysis of Error Feedback in Federated Non-C

**引用相关性**: 7.05/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 26（评估 15 条）
- 强相关: 12
- 弱相关: 3
- 不相关: 0

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

**内容准确性**: 8.6/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `horvath2023stochastic`: misrepresentation - 该文的核心是在分布式随机优化中研究梯度量化（任意压缩算子）与方差缩减技术（如 DIANA 型方法），给出带压缩的收敛率与线性收敛保证。文中分析允许压缩算子为有偏/一般量化算子，并通过特殊构造的控制变量
- `Cheng2023MomentumBN`: exaggeration - 相关描述中两点与原文略有偏差：
1）“Momentum has been shown to provably benefit FL under unbounded heterogeneity”基本符合
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `Tang2018D2DT`: misrepresentation - 引用该文作为“system heterogeneity, including ... decentralized data distributions”的例子，在字面上有一定合理性：Tang et a

**引用相关性**: 8.13/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 40（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 7
- 弱相关: 5
- 不相关: 3

**Key References 覆盖详情:**
- ✗ FedAvg convergence under non-IID (Li et al., ICLR 2020)
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
- 幻觉数量: 0
- 下载失败跳过: 0

**引用相关性**: 8.13/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 72（评估 15 条）
- 强相关: 7
- 弱相关: 6
- 不相关: 2

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

#### reasflow_gpt54

**内容准确性**: 8.63/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `yuan2020federated`: misrepresentation - 该描述把论文总结为：『federated composite optimization 指出结构化约束会改变聚合的几何性质，而不仅仅是压缩通信消息』。原文确实研究了带非光滑正则项（结构化约束）的联邦优
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 6.47/10
- Key References 覆盖: 4/10 (40%)
- 总引用数: 46（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 5
- 弱相关: 7
- 不相关: 3

**Key References 覆盖详情:**
- ✗ FedAvg convergence under non-IID (Li et al., ICLR 2020)
- ✓ SCAFFOLD d drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✗ D b2 d decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✗ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019)
- ✗ Lower bounds for compressed distributed optimization (He et al., 2023)
- ✗ GoLore d subspace optimization with convergence guarantees (He et al., 2024)
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon d matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION d scalable decentralized learning (Takezawa & Stich, ICLR 2025)

#### reasflow_sonnet4.6

**内容准确性**: 8.63/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `reguieg2023comparative`: misrepresentation - [multi-cite保护] 引用将 Reguieg et al. (2023) 这篇论文归类为“meta-learning”个性化策略，用于应对统计异质性。但原文是一篇对 FedAvg 与 Per-
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 7.08/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 37（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 7
- 不相关: 2

**Key References 覆盖详情:**
- ✗ FedAvg convergence under non-IID (Li et al., ICLR 2020)
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✗ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019)
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `He2023LowerBA`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)
