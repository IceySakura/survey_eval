# Related Works 评测报告

**评测时间**: 2026-03-21T14:02:37.129311
**打分模型**: gpt51
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **base_sonnet4.6**: 9.5/10
2. **reasflow_gpt51**: 9.4/10
3. **reasflow_sonnet4.6**: 9.4/10
4. **base_gpt51**: 9.23/10
5. **base_dpsk**: 8.86/10
6. **reasflow_dpsk**: 8.8/10
7. **reasflow_gpt54**: 8.63/10
8. **base_gpt54**: 8.46/10

### 引用相关性排名（1-10分）
1. **base_sonnet4.6**: 8.67/10
2. **base_gpt54**: 8.58/10
3. **base_dpsk**: 8.25/10
4. **base_gpt51**: 7.34/10
5. **reasflow_gpt51**: 6.69/10
6. **reasflow_gpt54**: 6.08/10
7. **reasflow_sonnet4.6**: 5.43/10
8. **reasflow_dpsk**: 4.82/10

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 8.86/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `koloskova2019decentralized`: misrepresentation - 该论文确实研究了去中心化（peer-to-peer）场景下的通信压缩，并提出了 CHOCO-SGD，允许任意（包括强压缩）的压缩算子并给出非凸情形下的收敛与线性加速分析，因此“extends thes
- `li2019challenges`: misrepresentation - 描述中将 FedProx 归因于 Li et al., 2019《Federated Learning: Challenges, Methods, and Future Directions》（arX
- `rodio2025facets`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: The Many Facets of Variance Reduction in Fede
- `bao2025efskip`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: EFSkip: A New Error Feedback with Linear Spee
- `su2023joint`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Joint Sparsification and Quantization for Wir

**引用相关性**: 8.25/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 30（评估 15 条）
- 强相关: 10
- 弱相关: 5
- 不相关: 0

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2016fedavg`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2019scaffold`
- ✗ FedProx (Li et al., MLSys 2020)
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✓ FedSub → `zhang2025fedsub`
- ✓ FedLoRU → `park2024fedlru`
- ✓ ILoRA → `zhou2025ilora`
- ✓ GaLore (Zhao et al., 2024) → `zhao2024galore`

#### base_gpt51

**内容准确性**: 9.23/10
- 验证引用数: 15
- 幻觉数量: 1
- 下载失败跳过: 0

**发现的幻觉:**
- `rodio2025variance`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: The Many Facets of Variance Reduction in Fede
- `wang2024flora`: wrong_metadata - 给出的“原始论文信息”文本是一篇关于电商平台中带赞助产品的 Assortment Planning 论文（作者 Tang, Cai, Yuan, Han），与引用中所说的 FLoRA: Federat

**引用相关性**: 7.34/10
- Key References 覆盖: 5/9 (56%)
- 总引用数: 30（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 9
- 弱相关: 5
- 不相关: 1

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
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `khirirat2019memory`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Convergence Bounds for Compressed Gradient Me
- `alistarh2017qsgd`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: QSGD: Communication-Efficient SGD via Gradien
- `acar2021feddyn`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `xia2024chainlora`: wrong_metadata - 引用的元数据明显错误：原始论文信息显示的是一篇关于 c=2 共形场论中非可逆对偶对称性的高能理论物理论文（Aguilera Damia 等，hep-th/2401.04166），与 Chain of 

**引用相关性**: 8.58/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 38（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 8
- 弱相关: 5
- 不相关: 2

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

**内容准确性**: 9.5/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `bernstein2018signsgd`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: Convergence rate of sign stochastic gradient 
- `zhang2025fedsub`: misrepresentation - 相关描述有一定偏差但不算完全错误。原文中 FedSub 是通过将每个客户端的局部更新限制在低维子空间内，并在通信时只需上传低维参数（从而降低通信、计算和内存成本）；从算法结构上看，确实可以被理解为在共
- `stich2018sparsified`: None - S2 消歧命中候选 #0（无 arXiv，未做全文核对），固定 accuracy_level=2。 匹配题: The Error-Feedback Framework: Better Rates fo

**引用相关性**: 8.67/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 27（评估 15 条）
- 强相关: 9
- 弱相关: 6
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

**内容准确性**: 8.8/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 4.82/10
- Key References 覆盖: 3/9 (33%)
- 总引用数: 26（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 4
- 弱相关: 9
- 不相关: 2

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
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 6.69/10
- Key References 覆盖: 5/9 (56%)
- 总引用数: 53（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
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

**内容准确性**: 8.63/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `su2023non`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）
- `koloskova2021improved`: misrepresentation - 被引用论文 Koloskova et al. 2022 分析的是在去中心化学习中带有 gradient tracking 的算法在随机/无噪声情形下的收敛率，改进其对网络混合参数 p 的依赖；通信被建

**引用相关性**: 6.08/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 36（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 10
- 不相关: 3

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

**内容准确性**: 9.4/10
- 验证引用数: 15
- 幻觉数量: 2
- 下载失败跳过: 0

**发现的幻觉:**
- `li2019convergence`: not_found - Semantic Scholar 检索无结果，视为无法对应真实论文（按捏造处理）

**引用相关性**: 5.43/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 22（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 5
- 弱相关: 9
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
