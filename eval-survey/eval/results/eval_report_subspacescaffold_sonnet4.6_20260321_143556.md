# Related Works 评测报告

**评测时间**: 2026-03-21T14:02:37.137904
**打分模型**: sonnet4.6
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **base_sonnet4.6**: 9.33/10
2. **reasflow_sonnet4.6**: 9.23/10
3. **base_dpsk**: 9.1/10
4. **base_gpt54**: 9.06/10
5. **base_gpt51**: 9.0/10
6. **reasflow_gpt51**: 8.9/10
7. **reasflow_dpsk**: 8.33/10
8. **reasflow_gpt54**: 8.33/10

### 引用相关性排名（1-10分）
1. **base_dpsk**: 8.89/10
2. **base_sonnet4.6**: 8.8/10
3. **base_gpt54**: 8.79/10
4. **base_gpt51**: 8.12/10
5. **reasflow_gpt54**: 7.9/10
6. **reasflow_gpt51**: 6.66/10
7. **reasflow_dpsk**: 5.86/10
8. **reasflow_sonnet4.6**: 5.56/10

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 9.1/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 1

**发现的幻觉:**
- `rodio2025facets`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: The Many Facets of Variance Reduction in Fede
- `liu2025fedswa`: misrepresentation - 描述称 FedSWA 采用 'momentum-based stochastic controlled weight averaging'，但实际上论文中 momentum-based 机制属于 Fe
- `bao2025efskip`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: EFSkip: A New Error Feedback with Linear Spee
- `su2023joint`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Joint Sparsification and Quantization for Wir
- `zhao2018non-iid`: misrepresentation - 该论文确实展示了非IID数据下联邦学习性能下降的问题，并通过'权重散度'（weight divergence）和地球移动距离（EMD）来解释局部模型偏离全局最优的现象，这与描述中'客户端模型偏离全局最

**引用相关性**: 8.89/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 30（评估 15 条）
- 强相关: 9
- 弱相关: 6
- 不相关: 0

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

**内容准确性**: 9.0/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 1

**发现的幻觉:**
- `rodio2025variance`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: The Many Facets of Variance Reduction in Fede
- `zhou2025ilora`: misrepresentation - [multi-cite保护] 第一处描述准确反映了 ILoRA 解决 misaligned client subspaces 和 rank incompatibility 的核心贡献。但第二处将 IL
- `han2024peftsurvey`: wrong_metadata - 论文实际内容与元数据严重不符：提供的论文内容是关于LLM中文化表示的调查（'Towards Measuring and Modeling Culture in LLMs'，作者为Adilazuarda

**引用相关性**: 8.12/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 30（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 9
- 弱相关: 5
- 不相关: 1

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

**内容准确性**: 9.06/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**发现的幻觉:**
- `khirirat2019memory`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Convergence Bounds for Compressed Gradient Me
- `alistarh2017qsgd`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: QSGD: Communication-Efficient SGD via Gradien
- `acar2021feddyn`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 8.79/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 39（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 9
- 弱相关: 5
- 不相关: 1

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

**内容准确性**: 9.33/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `bernstein2018signsgd`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Convergence rate of sign stochastic gradient 
- `zhao2021fedpage`: misrepresentation - 描述称 FedPAGE 通过方差缩减梯度估计器'加速本地收敛（accelerating local convergence）'，但论文的核心贡献实际上是降低通信轮次（communication com
- `stich2018sparsified`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: The Error-Feedback Framework: Better Rates fo
- `konecny2016federated`: misrepresentation - 描述称该论文提出了「减少通信轮次（communication rounds）」的策略，但实际上该论文的结构化更新（structured updates）和草图更新（sketched updates）旨

**引用相关性**: 8.8/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 27（评估 15 条）
- 强相关: 10
- 弱相关: 5
- 不相关: 0

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

**内容准确性**: 8.33/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `konevcny2016federated`: misrepresentation - 描述1将FedAvg算法（通过多步本地SGD摊销通信成本）归因于konevcny2016federated，但FedAvg实际上由McMahan et al. 2017提出。本文（Konečný et
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 5.86/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 26（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 7
- 不相关: 2

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

**内容准确性**: 8.9/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `Zhang2022CCFedAvgCC`: misrepresentation - [multi-cite保护] 描述将CC-FedAvg定位为'展示计算和参与不平衡如何加剧漂移'的研究，但实际上CC-FedAvg的核心贡献是提出一种通过模型估计替代计算密集型本地训练的方法，以解决计
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `Ma2017ImplicitRI`: misrepresentation - 该论文的核心贡献是证明梯度下降在相位恢复、矩阵补全、盲解卷积等非凸问题中具有隐式正则化效果并线性收敛，确实涉及低秩/低维结构。描述将其归纳为'许多问题具有有效的低维结构'在一定程度上是合理的，但将其置
- `collins2022fedavg`: misrepresentation - [multi-cite保护] Description 1 states that the representation-learning view of Collins et al. (2022) h

**引用相关性**: 6.66/10
- Key References 覆盖: 5/9 (56%)
- 总引用数: 53（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 7
- 不相关: 6

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

**内容准确性**: 8.33/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `koloskova2021improved`: misrepresentation - 描述称该论文'motivate historical correction when communication is lossy'（在有损通信时激励历史校正），但该论文的实际贡献是改进梯度跟踪（Gr

**引用相关性**: 7.9/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 36（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 4
- 弱相关: 9
- 不相关: 2

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

**内容准确性**: 9.23/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `jian2025widening`: misrepresentation - 描述称过参数化'can partially mitigate'异质性影响，但论文实际证明在无限宽度时影响完全消失（vanishing），理论结论比'partially'更强。此外，'greater m

**引用相关性**: 5.56/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 22（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 6
- 弱相关: 8
- 不相关: 1

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
