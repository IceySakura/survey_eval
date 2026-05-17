# Related Works 评测报告

**评测时间**: 2026-03-21T13:24:55.634233
**打分模型**: sonnet4.6
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **base_gpt51**: 10.0/10
2. **reasflow_gpt51**: 9.83/10
3. **base_gpt54**: 9.5/10
4. **base_sonnet4.6**: 9.16/10
5. **reasflow_dpsk**: 8.93/10
6. **reasflow_gpt54**: 8.63/10
7. **base_dpsk**: 7.89/10
8. **reasflow_sonnet4.6**: 7.86/10

### 引用相关性排名（1-10分）
1. **base_gpt51**: 9.53/10
2. **reasflow_sonnet4.6**: 8.61/10
3. **base_dpsk**: 8.38/10
4. **reasflow_gpt51**: 8.33/10
5. **reasflow_dpsk**: 8.13/10
6. **base_sonnet4.6**: 7.48/10
7. **base_gpt54**: 7.23/10
8. **reasflow_gpt54**: 7.13/10

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 7.89/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 1

**发现的幻觉:**
- `xiang2023partial`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与目标论文（标题：Partial participation in federated learning: Algorit
- `mcmahan2017fedavg`: wrong_metadata - 提供的论文内容与标题完全不符：标题声称是 McMahan 等人的联邦学习论文（FedAvg），但实际内容是 Motohashi & Starobinsky 关于宇宙暴胀（constant-roll i
- `zhang2022lightweight`: fabricated - 候选共 3 条，LLM 判定无与 Bib 对应的论文。理由: 三个候选论文均与目标论文不匹配。目标论文关注联邦学习中计算异构性的轻量级本地更新方法，作者为Yutong Zhang, Jian Wang
- `neymeyer2012geometric`: misrepresentation - The paper is accurately identified as establishing geometric convergence theory for preconditioned s

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
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `stich2019errorfeedback, richtarik2021ef21`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `he2023lowerbounds`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✗ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025)
- ✗ FedMuon — matrix orthogonalization in FL (Liu et al., 2025)
- ✓ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025) → `takezawa2025teleportation`

#### base_gpt51

**内容准确性**: 10.0/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 1

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

**内容准确性**: 9.5/10
- 验证引用数: 15
- 幻觉数量: 0
- 下载失败跳过: 0

**发现的幻觉:**
- `tyou2024localgecl`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: A Localized Primal-Dual Method for Centralize
- `tinyfel2025`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: TinyFEL: Communication, Computation, and Memo
- `alistarh2016qsgd`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: QSGD: Communication-Efficient SGD via Gradien

**引用相关性**: 7.23/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 35（评估 15 条）
- 强相关: 3
- 弱相关: 11
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
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `fallah2020personalized`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Personalized Federated Learning with Theoreti
- `koloskova2019decentralized`: misrepresentation - The first description accurately captures the paper's core contribution (arbitrary communication com
- `li2023analysis`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Analysis of Error Feedback in Federated Non-C
- `tang2019doublesqueeze`: misrepresentation - DoubleSqueeze 的核心贡献描述（对上传和下载两个方向均应用误差补偿压缩）是准确的，与论文摘要中'two-pass communication model, with error-compe
- `zhao2024galore`: misrepresentation - 描述称 GaLore 是将 LoRA 思想'扩展'到完整预训练（extend this idea），但实际上 GaLore 与 LoRA 的机制有本质区别：LoRA 在冻结权重上添加低秩矩阵，而 Ga

**引用相关性**: 7.48/10
- Key References 覆盖: 6/10 (60%)
- 总引用数: 26（评估 15 条）
- 强相关: 10
- 弱相关: 5
- 不相关: 0

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `li2018fedprox`
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

**内容准确性**: 8.93/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `horvath2023stochastic`: misrepresentation - 存在两个问题：(1) 引用标注为'horvath2023stochastic'，但该论文实际发表于2019年，存在年份元数据错误；(2) 描述将该论文定性为专注于'error feedback and
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

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

**内容准确性**: 9.83/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**发现的幻觉:**
- `ren2024low`: misrepresentation - 论文名称 'low-rank prune-and-factorize' 描述准确，但将其与 LoRA 等参数高效微调（PEFT）方法并列归类为 'reduce trainable parameters

**引用相关性**: 8.33/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 72（评估 15 条）
- 强相关: 7
- 弱相关: 2
- 不相关: 6

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

**内容准确性**: 8.63/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `yuan2020federated`: misrepresentation - 描述称该论文'强调结构化约束改变了聚合几何，而不仅仅是压缩消息'，这是对论文核心贡献的一种合理但有所偏差的概括。论文实际上提出了'原始平均的诅咒'（curse of primal averaging）
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 7.13/10
- Key References 覆盖: 5/10 (50%)
- 总引用数: 46（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 5
- 不相关: 4

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `mcmahan2017communication`
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

**内容准确性**: 7.86/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `Zhang2022CCFedAvgCC`: misrepresentation - CC-FedAvg 被归类为解决「架构异构性（architectural heterogeneity）」的方法，但这是错误的分类。该论文明确针对的是「计算异构性（computational heter
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `horvoth2022natural`: misrepresentation - 描述将natural compression归类为'unbiased quantization schemes'（无偏量化方案），但实际上natural compression是一种有偏（biased
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 8.61/10
- Key References 覆盖: 7/10 (70%)
- 总引用数: 37（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 7
- 弱相关: 5
- 不相关: 3

**Key References 覆盖详情:**
- ✓ FedAvg convergence under non-IID (Li et al., ICLR 2020) → `mcmahan2017communication`
- ✓ SCAFFOLD — drift correction (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ Linear speedup under partial participation (Yang et al., ICLR 2021) → `Yang2021AchievingLS`
- ✗ D² — decentralized with heterogeneity correction (Tang et al., ICML 2018)
- ✓ Error Feedback / EF21 (Stich & Karimireddy 2019; Karimireddy et al., ICML 2019) → `stich2018sparsified`
- ✓ Lower bounds for compressed distributed optimization (He et al., 2023) → `He2023LowerBA`
- ✗ GoLore — subspace optimization with convergence guarantees (He et al., 2024)
- ✓ An Efficient Subspace Algorithm for FL on Heterogeneous Data (Zhang, Xu & Yuan, 2025) → `zhang2025efficient`
- ✓ FedMuon — matrix orthogonalization in FL (Liu et al., 2025) → `liu2025fedmuon`
- ✗ TELEPORTATION — scalable decentralized learning (Takezawa & Stich, ICLR 2025)
