# Related Works 评测报告

**评测时间**: 2026-03-21T14:00:53.771508
**打分模型**: dpsk
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **base_gpt51**: 10.0/10
2. **base_gpt54**: 9.5/10
3. **reasflow_gpt51**: 9.4/10
4. **base_sonnet4.6**: 9.16/10
5. **reasflow_gpt54**: 8.63/10
6. **reasflow_dpsk**: 8.26/10
7. **reasflow_sonnet4.6**: 7.83/10
8. **base_dpsk**: 7.43/10

### 引用相关性排名（1-10分）
1. **base_gpt51**: 9.0/10
2. **reasflow_gpt51**: 7.63/10
3. **base_dpsk**: 7.44/10
4. **reasflow_sonnet4.6**: 7.21/10
5. **base_gpt54**: 7.09/10
6. **reasflow_dpsk**: 6.87/10
7. **base_sonnet4.6**: 6.82/10
8. **reasflow_gpt54**: 5.73/10

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 7.43/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `xiang2023partial`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有任何一篇论文的标题、作者和年份与待匹配条目（标题：Partial participation in federated l
- `mcmahan2017fedavg`: wrong_metadata - 提供的“原始论文信息”部分的内容与描述中引用的论文（McMahan et al., 2017, FedAvg）完全无关。提供的摘录是关于宇宙学“Constant-roll inflation”的论文，
- `zhang2022lightweight`: fabricated - 候选共 3 条，LLM 判定无与 Bib 对应的论文。理由: 所有候选论文的标题、作者、年份均与待匹配论文不一致，且主题相关性较弱（待匹配论文关注计算异构性与轻量本地更新，而候选论文聚焦隐私增强、区块
- `karimireddy2020scaffold`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: SCAFFOLD: Stochastic Controlled Averaging for
- `li2020fedprox`: wrong_metadata - 提供的“原始论文信息”与描述中引用的论文“FedProx: Federated optimization in heterogeneous networks”完全不符。所提供的摘录来自一篇标题为“Ad

**引用相关性**: 7.44/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 33（评估 15 条（其中 4 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 7
- 不相关: 5

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
- 弱相关: 11
- 不相关: 1

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

**内容准确性**: 9.5/10
- 验证引用数: 15
- 幻觉数量: 0
- 下载失败跳过: 0

**发现的幻觉:**
- `tyou2024localgecl`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: A Localized Primal-Dual Method for Centralize
- `tinyfel2025`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: TinyFEL: Communication, Computation, and Memo
- `alistarh2016qsgd`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: QSGD: Communication-Efficient SGD via Gradien

**引用相关性**: 7.09/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 35（评估 15 条）
- 强相关: 2
- 弱相关: 12
- 不相关: 1

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2018fedprox`
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

**内容准确性**: 9.16/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `fallah2020personalized`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Personalized Federated Learning with Theoreti
- `li2023analysis`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Analysis of Error Feedback in Federated Non-C
- `zhao2024galore`: misrepresentation - 描述称“<citet{zhao2024galore}> extend this idea to full pre-training via \emph{GaLore}: instead of rest
- `li2018fedprox`: misrepresentation - 描述存在两处不准确之处：1. 引用的作者年份标识符为 'li2018fedprox'，但论文实际发表年份为2020（arXiv版本为2018年12月首次提交）。2. 描述中称论文作者为 'li2018
- `condat2024locodl`: misrepresentation - 描述称LoCoDL提供了一个“principled primal-dual framework”。然而，根据提供的论文摘要和引言，LoCoDL被描述为一种结合了本地训练和压缩的通信高效算法，并提到其理

**引用相关性**: 6.82/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 26（评估 15 条）
- 强相关: 5
- 弱相关: 10
- 不相关: 0

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `mcmahan2017communication`
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

**内容准确性**: 8.26/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `daning2017weighted`: misrepresentation - 论文《Weighted parallel SGD for distributed unbalanced-workload training system》的核心贡献是提出WP-SGD算法，以解决在异构
- `Cheng2023MomentumBN`: misrepresentation - 描述中称 'momentum methods have limited scalability validation'，这并非论文《Momentum Benefits Non-IID Federate
- `Tran-Dinh2021FedDRR`: misrepresentation - 描述中提及该论文“handle nonsmooth regularizers but rely on standard smoothness assumptions”。该论文确实处理了包含非光滑正则项
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `Tang2018D2DT`: misrepresentation - 描述中提及的“drift phenomenon is exacerbated by system heterogeneity, including unbalanced workloads and d

**引用相关性**: 6.87/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 40（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 0
- 弱相关: 10
- 不相关: 5

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

**内容准确性**: 9.4/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**发现的幻觉:**
- `xu2023determine`: wrong_metadata - 描述中引用的文献标识符为 'xu2023determine'，年份为2023，标题为 'optimal noise subspace selection'。然而，所提供的原始论文信息显示，该论文的作者

**引用相关性**: 7.63/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 71（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 5
- 不相关: 7

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

**内容准确性**: 8.63/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `zhang2025efficient`: misrepresentation - 描述中的核心事实（"FedSub projects local training into subspaces and uses low-dimensional dual variables to c

**引用相关性**: 5.73/10
- Key References 覆盖: 4/10 (40%)
- 总引用数: 46（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 8
- 不相关: 5

**Key References 覆盖详情:**
- ✗ FedAvg convergence under non-IID (Li et al., ICLR 2020)
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

**内容准确性**: 7.83/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `Yuan2020FederatedAS`: misrepresentation - 描述中关于该论文的部分（'further demonstrated that acceleration reduces synchronization rounds to O(M^{1/3}) via
- `horvoth2022natural`: wrong_metadata - 描述中引用的年份（2022）与提供的原始论文信息（arXiv版本日期为2022年，但原始arXiv提交为2019年）存在轻微偏差，且引用的作者名拼写（'horvoth'）存在笔误，应为'horvath
- `mcmahan2017communication`: wrong_metadata - 描述中引用的文献标识符为 `\citet{mcmahan2017communication}`，这与提供的原始论文信息（标题：Communication-Efficient Learning of D
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 7.21/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 37（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 8
- 不相关: 4

**Key References 覆盖详情:**
- ✗ FedAvg convergence under non-IID (Li et al., ICLR 2020)
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `stich2018sparsified`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `He2023LowerBA`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)
