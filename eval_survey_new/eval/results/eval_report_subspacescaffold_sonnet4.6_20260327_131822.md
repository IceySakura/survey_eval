# Related Works 评测报告

**评测时间**: 2026-03-27T12:44:37.381612
**打分模型**: sonnet4.6
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_sonnet4.6**: 9.78/10
2. **reasflow_gpt51**: 9.37/10
3. **reasflow_gpt54**: 9.23/10
4. **reasflow_dpsk**: 8.68/10
5. **base_gpt51**: 8.07/10
6. **base_gpt54**: 6.4/10
7. **base_sonnet4.6**: 6.07/10
8. **base_dpsk**: 5.6/10

### 引用相关性排名（1-10分）
1. **reasflow_gpt54**: 7.92/10
2. **base_gpt51**: 7.69/10
3. **reasflow_gpt51**: 7.53/10
4. **base_dpsk**: 7.44/10
5. **base_gpt54**: 7.41/10
6. **base_sonnet4.6**: 7.36/10
7. **reasflow_dpsk**: 6.07/10
8. **reasflow_sonnet4.6**: 5.64/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **15.032** / 20
- 跨配置平均 · 内容准确性: **7.9** / 10
- 跨配置平均 · 引用相关性: **7.133** / 10
- 各配置总分（CA+CR）:
  - **reasflow_gpt54**: 17.15 / 20
  - **reasflow_gpt51**: 16.9 / 20
  - **base_gpt51**: 15.76 / 20
  - **reasflow_sonnet4.6**: 15.42 / 20
  - **reasflow_dpsk**: 14.75 / 20
  - **base_gpt54**: 13.81 / 20
  - **base_sonnet4.6**: 13.43 / 20
  - **base_dpsk**: 13.04 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 5.6/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 2

**发现的幻觉:**
- `li2019challenges`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'Federated Learning: Challenges, Methods, and Future Direct
- `rodio2025facets`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与《The Many Facets of Variance Reduction in Federated Learning
- `liu2025fedswa`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: None of the candidates match 'FedSWA: Improving Generalization in Fe
- `bao2025efskip`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'EFSkip: A New Error Feedback with Linear Speedup for Compre
- `su2023joint`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Joint Sparsification and Quantization for Wireless Federate

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

**内容准确性**: 8.07/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 1

**发现的幻觉:**
- `li2020federated`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'Federated Learning: Challenges, Methods, and Future Direct
- `rodio2025variance`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与《The Many Facets of Variance Reduction in Federated Learning
- `medjadji2025fedsparq`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'FedSparQ: Adaptive Sparse Quantization with Error Feedback 

**引用相关性**: 7.69/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 28（评估 15 条（其中 3 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 8
- 弱相关: 4
- 不相关: 3

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ FedProx (Li et al., MLSys 2020) → `li2018federated`
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✓ FedSub → `zhang2025fedsub`
- ✗ FedLoRU
- ✓ ILoRA → `zhou2025ilora`
- ✓ GaLore (Zhao et al., 2024) → `zhao2024galore`

#### base_gpt54

**内容准确性**: 6.4/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `li2021moon`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Model-Contrastive Federated Learning'（Qinbin Li, Bingsheng 
- `condat2022efbv`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'EF-BV: A Unified Theory of Error Feedback and Variance Red
- `khirirat2019memory`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与目标论文'Convergence Bounds for Compressed Gradient Methods with
- `acar2021feddyn`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Federated Learning Based on Dynamic Regularization'（Durmus 
- `wang2020fednova`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Tackling the Objective Inconsistency Problem in Heterogeneo

**引用相关性**: 7.41/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 34（评估 15 条（其中 6 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 7
- 弱相关: 2
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

**内容准确性**: 6.07/10
- 验证引用数: 15
- 幻觉数量: 9
- 下载失败跳过: 0

**发现的幻觉:**
- `azam2022recycling`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'Recycling Model Updates in Federated Learning: Are Gradien
- `zhou2025ilora`: misrepresentation - [multi-cite保护] 描述称ILoRA等方法'do not address this incompatibility; they either ignore client drift enti
- `zhang2025fedsub`: misrepresentation - [multi-cite保护] The description claims FedSub and other subspace FL methods 'either ignore client dri
- `wang2020tackling`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Tackling the Objective Inconsistency Problem in Heterogeneo
- `guo2024efficient`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与'Efficient Wireless Federated Learning via Low-Rank Gradient

**引用相关性**: 7.36/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 22（评估 15 条（其中 5 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 4
- 不相关: 5

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

**内容准确性**: 8.68/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `su2023non`: misrepresentation - The paper does acknowledge that data heterogeneity causes local updates to diverge from the global o
- `konevcny2016federated`: misrepresentation - 第一段描述将 FedAvg 算法（通过多步本地 SGD 摊销通信成本）归因于 Konečný et al. (2016)，这是实质性错误。FedAvg 算法由 McMahan et al. (2017
- `Qian2020ErrorCD`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有与 'Error Compensated Distributed SGD Can Be Accelerated'（Xun 

**引用相关性**: 6.07/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 27（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 7
- 弱相关: 7
- 不相关: 1

**Key References 覆盖详情:**
- ✗ FedAvg (McMahan et al., AISTATS 2017)
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✓ Federated Learning with Compression (Haddadpour et al., AISTATS 2021) → `Haddadpour2020FederatedLW`
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✓ FedSub → `zhang2025efficient`
- ✗ FedLoRU
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✗ GaLore (Zhao et al., 2024)

#### reasflow_gpt51

**内容准确性**: 9.37/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `Zhang2022CCFedAvgCC`: misrepresentation - [multi-cite保护] 描述称 CC-FedAvg 展示了'计算和参与不平衡如何加剧漂移（drift）'，但实际上 CC-FedAvg 是一个解决计算异构性问题的方法论文，其核心贡献是提出模型估
- `daning2017weighted`: misrepresentation - [multi-cite保护] 描述将 WP-SGD 置于联邦学习（FedAvg、FedProx）的语境下，讨论其如何'加剧 drift'，但该论文实际上是针对异构分布式计算环境中不均衡工作负载的训练问
- `collins2022fedavg`: misrepresentation - [multi-cite保护] 第一处描述称 collins2022fedavg 指出 FedAvg '可能收敛到有偏的驻点（biased stationary points）'，这与论文实际内容相悖。

**引用相关性**: 7.53/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 54（评估 15 条）
- 强相关: 3
- 弱相关: 7
- 不相关: 5

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✓ Federated Learning with Compression (Haddadpour et al., AISTATS 2021) → `Haddadpour2020FederatedLW`
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✗ FedSub
- ✓ FedLoRU → `Park2024CommunicationEfficientFL`
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✓ GaLore (Zhao et al., 2024) → `Zhao2024GaLoreML`

#### reasflow_gpt54

**内容准确性**: 9.23/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 1

**发现的幻觉:**
- `su2023non`: misrepresentation - 该论文确实分析了FedProx在异构数据分布和不平衡数据集下的表现，这与描述中'imbalance and distribution shift'有对应。但描述将论文定性为'proximal obje
- `koloskova2021improved`: misrepresentation - 该论文的核心贡献是改进梯度跟踪（Gradient Tracking）方法在去中心化机器学习中的收敛性分析（改进对混合参数p的依赖），并提出新的证明技术。描述将其定性为'motivate histori

**引用相关性**: 7.92/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 38（评估 15 条）
- 强相关: 3
- 弱相关: 12
- 不相关: 0

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✓ FedSub → `zhang2025efficient`
- ✓ FedLoRU → `Park2024CommunicationEfficientFL`
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✓ GaLore (Zhao et al., 2024) → `Zhao2024GaLoreML`

#### reasflow_sonnet4.6

**内容准确性**: 9.78/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 1

**发现的幻觉:**
- `jian2025widening`: misrepresentation - 描述使用'partially mitigate'（部分缓解）来概括该论文的贡献，但论文实际证明的是随网络宽度增加，数据异质性的影响会逐渐消失（diminishes...ultimately vanis

**引用相关性**: 5.64/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 23（评估 15 条）
- 强相关: 6
- 弱相关: 9
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
