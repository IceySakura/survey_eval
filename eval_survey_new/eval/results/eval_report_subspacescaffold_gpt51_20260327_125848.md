# Related Works 评测报告

**评测时间**: 2026-03-27T12:44:35.220832
**打分模型**: gpt51
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_sonnet4.6**: 10.0/10
2. **reasflow_gpt51**: 9.79/10
3. **reasflow_dpsk**: 9.4/10
4. **reasflow_gpt54**: 9.28/10
5. **base_gpt51**: 7.6/10
6. **base_sonnet4.6**: 6.88/10
7. **base_gpt54**: 6.4/10
8. **base_dpsk**: 6.19/10

### 引用相关性排名（1-10分）
1. **base_sonnet4.6**: 7.49/10
2. **base_dpsk**: 7.44/10
3. **base_gpt54**: 7.28/10
4. **base_gpt51**: 6.64/10
5. **reasflow_gpt51**: 6.48/10
6. **reasflow_gpt54**: 6.23/10
7. **reasflow_sonnet4.6**: 5.5/10
8. **reasflow_dpsk**: 5.16/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **14.72** / 20
- 跨配置平均 · 内容准确性: **8.192** / 10
- 跨配置平均 · 引用相关性: **6.527** / 10
- 各配置总分（CA+CR）:
  - **reasflow_gpt51**: 16.27 / 20
  - **reasflow_gpt54**: 15.51 / 20
  - **reasflow_sonnet4.6**: 15.5 / 20
  - **reasflow_dpsk**: 14.56 / 20
  - **base_sonnet4.6**: 14.37 / 20
  - **base_gpt51**: 14.24 / 20
  - **base_gpt54**: 13.68 / 20
  - **base_dpsk**: 13.63 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 6.19/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 0

**发现的幻觉:**
- `li2019challenges`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题为或接近“Federated Learning: Challenges, Methods, and Future Dir
- `rodio2025facets`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中均未出现题为或接近“The Many Facets of Variance Reduction in Federated Le
- `liu2025fedswa`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目或作者与“FedSWA: Improving Generalization in Federated Learning
- `bao2025efskip`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无题目含 EFSkip 关键词或与“EFSkip: A New Error Feedback with Linear Spee
- `su2023joint`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中均未出现题为“Joint Sparsification and Quantization for Wireless Feder

**引用相关性**: 7.44/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 24（评估 15 条（其中 6 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 7
- 弱相关: 2
- 不相关: 6

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2016fedavg`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2019scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✓ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024) → `valdeira2025vertical`
- ✓ FedSub → `zhang2025fedsub`
- ✓ FedLoRU → `park2024fedlru`
- ✓ ILoRA → `zhou2025ilora`
- ✓ GaLore (Zhao et al., 2024) → `zhao2024galore`

#### base_gpt51

**内容准确性**: 7.6/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `li2020federated`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无标题为“Federated Learning: Challenges, Methods, and Future Direct
- `rodio2025variance`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中均未出现标题或作者与“The Many Facets of Variance Reduction in Federated L
- `wang2024flora`: wrong_metadata - 被引用论文 Wang et al.~\cite{wang2024flora} 标题为《FLoRA: Federated Fine-Tuning Large Language Models with H
- `medjadji2025fedsparq`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无标题或作者与“FedSparQ: Adaptive Sparse Quantization with Error Feedb

**引用相关性**: 6.64/10
- Key References 覆盖: 5/9 (56%)
- 总引用数: 27（评估 15 条（其中 4 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 8
- 弱相关: 3
- 不相关: 4

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✓ FedSub → `zhang2025fedsub`
- ✗ FedLoRU
- ✓ ILoRA → `zhou2025ilora`
- ✓ GaLore (Zhao et al., 2024) → `zhao2024galore`

#### base_gpt54

**内容准确性**: 6.4/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 0

**发现的幻觉:**
- `li2021moon`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无题目或作者与“Model-Contrastive Federated Learning (Qinbin Li, Bingsh
- `condat2022efbv`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无题名或作者与“EF-BV: A Unified Theory of Error Feedback and Variance 
- `khirirat2019memory`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无题目和作者与“Convergence Bounds for Compressed Gradient Methods with
- `acar2021feddyn`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题为或接近“Federated Learning Based on Dynamic Regularization”，且作者
- `wang2020fednova`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目或作者与“Tackling the Objective Inconsistency Problem in Hetero

**引用相关性**: 7.28/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 34（评估 15 条（其中 6 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 3
- 不相关: 6

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ FedProx (Li et al., MLSys 2020) → `sahu2020fedprox`
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✓ FedSub → `zhang2025fedsub`
- ✗ FedLoRU
- ✓ ILoRA → `zhou2025ilora`
- ✓ GaLore (Zhao et al., 2024) → `zhao2024galore`

#### base_sonnet4.6

**内容准确性**: 6.88/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `azam2022recycling`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有标题或作者与“Recycling Model Updates in Federated Learning: Are Gra
- `zhang2025fedsub`: misrepresentation - [multi-cite保护] 相关工作中两处对 Zhang et al. (2025, FedSub) 的描述均与论文摘录不符：
1) “FedSub projects local gradients
- `wang2020tackling`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中无标题或作者与“Tackling the Objective Inconsistency Problem in Heterog
- `guo2024efficient`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目包含“Efficient Wireless Federated Learning via Low-Rank Gradi
- `zhao2021fedpage`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目或作者与“FedPAGE: A Fast Local Stochastic Gradient Method for C

**引用相关性**: 7.49/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 23（评估 15 条（其中 4 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 5
- 弱相关: 6
- 不相关: 4

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ FedProx (Li et al., MLSys 2020) → `li2020fedprox`
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✓ FedSub → `zhang2025fedsub`
- ✓ FedLoRU → `park2024fedloru`
- ✓ ILoRA → `zhou2025ilora`
- ✓ GaLore (Zhao et al., 2024) → `zhao2024galore`

#### reasflow_dpsk

**内容准确性**: 9.4/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `Qian2020ErrorCD`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有题目和作者同时匹配“Error Compensated Distributed SGD Can Be Accelerate

**引用相关性**: 5.16/10
- Key References 覆盖: 3/9 (33%)
- 总引用数: 27（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 8
- 不相关: 1

**Key References 覆盖详情:**
- ✗ FedAvg (McMahan et al., AISTATS 2017)
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✓ Federated Learning with Compression (Haddadpour et al., AISTATS 2021) → `Haddadpour2020FederatedLW`
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✗ FedSub
- ✗ FedLoRU
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✗ GaLore (Zhao et al., 2024)

#### reasflow_gpt51

**内容准确性**: 9.79/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `daning2017weighted`: misrepresentation - 被引用论文提出的是用于异构/不均衡工作负载分布式训练的加权并行 SGD（WP-SGD），重点在于通过对不同节点模型进行加权聚合，在节点处理数据量和计算性能不一致时，仍能获得较好的收敛效果；确实讨论了异

**引用相关性**: 6.48/10
- Key References 覆盖: 5/9 (56%)
- 总引用数: 54（评估 15 条）
- 强相关: 1
- 弱相关: 9
- 不相关: 5

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✓ Federated Learning with Compression (Haddadpour et al., AISTATS 2021) → `Haddadpour2020FederatedLW`
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✗ FedSub
- ✗ FedLoRU
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✓ GaLore (Zhao et al., 2024) → `Zhao2024GaLoreML`

#### reasflow_gpt54

**内容准确性**: 9.28/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `su2023non`: misrepresentation - 被引论文主要是在非参数回归（RKHS）框架下重新分析 FedAvg 和 FedProx 的收敛与统计效率，给出在异质数据、非平衡样本下的误差收敛率，并提出“federation gain”等概念，用于
- `koloskova2021improved`: misrepresentation - 相关工作中的描述是："Related tracking analyses in decentralized learning further motivate historical correctio

**引用相关性**: 6.23/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 38（评估 15 条）
- 强相关: 2
- 弱相关: 12
- 不相关: 1

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✗ FedSub
- ✗ FedLoRU
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✓ GaLore (Zhao et al., 2024) → `Zhao2024GaLoreML`

#### reasflow_sonnet4.6

**内容准确性**: 10.0/10
- 验证引用数: 15
- 幻觉数量: 0
- 下载失败跳过: 0

**引用相关性**: 5.5/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 23（评估 15 条）
- 强相关: 5
- 弱相关: 10
- 不相关: 0

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✓ Federated Learning with Compression (Haddadpour et al., AISTATS 2021) → `Haddadpour2020FederatedLW`
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✗ FedSub
- ✗ FedLoRU
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✗ GaLore (Zhao et al., 2024)
