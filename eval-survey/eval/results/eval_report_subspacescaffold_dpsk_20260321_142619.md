# Related Works 评测报告

**评测时间**: 2026-03-21T14:02:37.133485
**打分模型**: dpsk
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **base_sonnet4.6**: 9.42/10
2. **reasflow_gpt51**: 9.4/10
3. **reasflow_sonnet4.6**: 8.73/10
4. **reasflow_dpsk**: 8.63/10
5. **base_dpsk**: 8.6/10
6. **base_gpt51**: 8.46/10
7. **base_gpt54**: 8.46/10
8. **reasflow_gpt54**: 8.2/10

### 引用相关性排名（1-10分）
1. **base_dpsk**: 8.36/10
2. **base_sonnet4.6**: 8.27/10
3. **base_gpt54**: 8.02/10
4. **base_gpt51**: 6.7/10
5. **reasflow_gpt54**: 5.95/10
6. **reasflow_gpt51**: 5.72/10
7. **reasflow_sonnet4.6**: 5.09/10
8. **reasflow_dpsk**: 4.18/10

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 8.6/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 1

**发现的幻觉:**
- `koloskova2019decentralized`: misrepresentation - 描述称该论文“扩展这些技术到点对点设置”，这基本准确，因为论文确实研究了去中心化学习与任意压缩。然而，描述隐含地将该论文与“不确定性原理”建立了一种直接的、方法上的扩展关系，这并不准确。原始论文并未引
- `li2019challenges`: misrepresentation - 描述存在实质性错误。论文《Federated Learning: Challenges, Methods, and Future Directions》是一篇综述性文章，主要讨论了联邦学习的独特挑战、
- `rodio2025facets`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: The Many Facets of Variance Reduction in Fede
- `bao2025efskip`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: EFSkip: A New Error Feedback with Linear Spee
- `karimireddy2019scaffold`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: SCAFFOLD: Stochastic Controlled Averaging for

**引用相关性**: 8.36/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 30（评估 15 条）
- 强相关: 5
- 弱相关: 9
- 不相关: 1

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

**内容准确性**: 8.46/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `zhao2024galore`: misrepresentation - 描述中称GaLore 'project gradients onto a learned low-rank subspace'。根据原始论文摘要和内容，GaLore（梯度低秩投影）的核心是将梯度（gr
- `rodio2025variance`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: The Many Facets of Variance Reduction in Fede
- `wang2024flora`: wrong_metadata - Related Works 中引用的论文标题为 'FLoRA: Federated Fine-Tuning Large Language Models with Heterogeneous Low-R
- `han2024peftsurvey`: wrong_metadata - Related Works 中引用的论文 'Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey' (Han

**引用相关性**: 6.7/10
- Key References 覆盖: 5/9 (56%)
- 总引用数: 29（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 5
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

**内容准确性**: 8.46/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `khirirat2019memory`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Convergence Bounds for Compressed Gradient Me
- `alistarh2017qsgd`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: QSGD: Communication-Efficient SGD via Gradien
- `acar2021feddyn`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `xia2024chainlora`: wrong_metadata - 描述将论文“Chain of LoRA: Efficient Fine-tuning of Language Models via Residual Learning”（作者：Wenhan Xia, 

**引用相关性**: 8.02/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 38（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 5
- 弱相关: 6
- 不相关: 4

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

**内容准确性**: 9.42/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 2

**发现的幻觉:**
- `bernstein2018signsgd`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Convergence rate of sign stochastic gradient 
- `zhang2025fedsub`: misrepresentation - [multi-cite保护] 描述称“FedSub projects local gradients onto a shared low-dimensional subspace before agg
- `stich2018sparsified`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: The Error-Feedback Framework: Better Rates fo

**引用相关性**: 8.27/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 27（评估 15 条）
- 强相关: 6
- 弱相关: 8
- 不相关: 1

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

**内容准确性**: 8.63/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `zhou2021communication`: misrepresentation - [multi-cite保护] Related Works 中的描述将当前论文 (Zhou et al., 2020) 作为示例，用于说明“their analyses often rely on co
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 4.18/10
- Key References 覆盖: 3/9 (33%)
- 总引用数: 26（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 6
- 不相关: 6

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

**内容准确性**: 9.4/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 5.72/10
- Key References 覆盖: 5/9 (56%)
- 总引用数: 53（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 0
- 弱相关: 5
- 不相关: 10

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

**内容准确性**: 8.2/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `koloskova2021improved`: wrong_metadata - Related Works 中的描述引用了该论文（koloskova2021improved），但提供的原始论文信息是2022年的论文《An Improved Analysis of Gradient

**引用相关性**: 5.95/10
- Key References 覆盖: 5/9 (56%)
- 总引用数: 35（评估 15 条（其中 3 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 5
- 不相关: 8

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✗ FedSub
- ✓ FedLoRU → `Park2024CommunicationEfficientFL`
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✓ GaLore (Zhao et al., 2024) → `Zhao2024GaLoreML`

#### reasflow_sonnet4.6

**内容准确性**: 8.73/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `mcmahan2017communication`: wrong_metadata - 描述中引用的作者年份为 'mcmahan2017communication'，但根据提供的原始论文信息，该论文的 arXiv 版本日期为 2023 年（v4），且其首次公开（arXiv v1）年份为 
- `reguieg2023comparative`: misrepresentation - 描述中提到“The severity of drift grows with heterogeneity, as confirmed empirically using Dirichlet-param
- `Condat2024LoCoDLCD`: misrepresentation - 描述称LoCoDL在“primal–dual framework”中统一了本地训练和无偏压缩。然而，根据提供的论文摘要和引言，LoCoDL被描述为一种利用本地训练和压缩的通信高效算法，并适用于一大类无
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `jian2025widening`: misrepresentation - 描述称'Overparameterization can partially mitigate heterogeneity's impact'，这与论文的核心结论'网络宽度增加可以减轻数据异构性的影响

**引用相关性**: 5.09/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 22（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 5
- 弱相关: 5
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
- ✗ GaLore (Zhao et al., 2024)
