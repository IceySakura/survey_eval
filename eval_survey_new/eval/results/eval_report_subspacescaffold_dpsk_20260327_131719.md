# Related Works 评测报告

**评测时间**: 2026-03-27T12:44:37.816990
**打分模型**: dpsk
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_gpt51**: 9.79/10
2. **reasflow_sonnet4.6**: 9.16/10
3. **reasflow_gpt54**: 8.38/10
4. **reasflow_dpsk**: 8.2/10
5. **base_sonnet4.6**: 7.18/10
6. **base_gpt51**: 7.0/10
7. **base_dpsk**: 6.14/10
8. **base_gpt54**: 5.8/10

### 引用相关性排名（1-10分）
1. **reasflow_gpt54**: 7.42/10
2. **base_sonnet4.6**: 7.1/10
3. **base_dpsk**: 7.04/10
4. **reasflow_gpt51**: 6.92/10
5. **base_gpt51**: 6.55/10
6. **base_gpt54**: 6.41/10
7. **reasflow_sonnet4.6**: 4.63/10
8. **reasflow_dpsk**: 4.59/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **14.039** / 20
- 跨配置平均 · 内容准确性: **7.706** / 10
- 跨配置平均 · 引用相关性: **6.332** / 10
- 各配置总分（CA+CR）:
  - **reasflow_gpt51**: 16.71 / 20
  - **reasflow_gpt54**: 15.8 / 20
  - **base_sonnet4.6**: 14.28 / 20
  - **reasflow_sonnet4.6**: 13.79 / 20
  - **base_gpt51**: 13.55 / 20
  - **base_dpsk**: 13.18 / 20
  - **reasflow_dpsk**: 12.79 / 20
  - **base_gpt54**: 12.21 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 6.14/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 1

**发现的幻觉:**
- `li2019challenges`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配条目（Tian Li et al., 2019）不符，且没有一篇标题为 'Federate
- `rodio2025facets`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与查询的Bib条目（标题：'The Many Facets of Variance Reducti
- `liu2025fedswa`: wrong_metadata - 描述中引用的论文标题为“FedSWA: Improving Generalization in Federated Learning with Highly Heterogeneous Data vi
- `bao2025efskip`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者、年份均与待匹配条目（EFSkip: A New Error Feedback with Linear S
- `su2023joint`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配的Bib条目（标题为'Joint Sparsification and Quantizat

**引用相关性**: 7.04/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 24（评估 15 条（其中 6 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 4
- 弱相关: 5
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

**内容准确性**: 7.0/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 0

**发现的幻觉:**
- `li2020federated`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配条目（Tian Li et al., 2020）不一致，且没有发现标题高度相似或作者重叠的
- `rodio2025variance`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者、年份均与待匹配条目（标题：'The Many Facets of Variance Reduction 
- `wang2024flora`: wrong_metadata - Related Works 中的描述将论文 "FLoRA: Federated Fine-Tuning Large Language Models with Heterogeneous Low-Ran
- `han2024peftsurvey`: wrong_metadata - 描述中引用的论文（Han et al., 2024）标题为《Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Surv
- `medjadji2025fedsparq`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配条目（标题：FedSparQ: Adaptive Sparse Quantization 

**引用相关性**: 6.55/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 26（评估 15 条（其中 5 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 5
- 弱相关: 4
- 不相关: 6

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

**内容准确性**: 5.8/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 0

**发现的幻觉:**
- `li2021moon`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配条目（标题：Model-Contrastive Federated Learning，作者
- `condat2022efbv`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib条目中的论文标题为'EF-BV: A Unified Theory of Error Feedback and Variance 
- `khirirat2019memory`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配条目不符。待匹配论文标题为'Convergence Bounds for Compress
- `acar2021feddyn`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有任何一篇论文的标题、作者和年份与待匹配条目（Federated Learning Based on Dynamic Reg
- `wang2020fednova`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib条目标题为'Tackling the Objective Inconsistency Problem in Heterogeneo

**引用相关性**: 6.41/10
- Key References 覆盖: 6/9 (67%)
- 总引用数: 33（评估 15 条（其中 7 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 4
- 不相关: 8

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

**内容准确性**: 7.18/10
- 验证引用数: 15
- 幻觉数量: 7
- 下载失败跳过: 0

**发现的幻觉:**
- `azam2022recycling`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有任何一篇论文的标题、作者和年份与Bib条目完全匹配。Bib条目标题为'Recycling Model Updates in
- `zhou2025ilora`: misrepresentation - [multi-cite保护] Related Works 中的描述声称 ILoRA "do not address this incompatibility; they either ignore c
- `wang2020tackling`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有任何一篇论文的标题、作者或年份与待匹配的Bib条目（标题：Tackling the Objective Inconsist
- `guo2024efficient`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配条目（标题：Efficient Wireless Federated Learning v
- `zhao2021fedpage`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配条目（FedPAGE: A Fast Local Stochastic Gradient 

**引用相关性**: 7.1/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 23（评估 15 条（其中 4 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 5
- 弱相关: 4
- 不相关: 6

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

**内容准确性**: 8.2/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `zhou2021communication`: wrong_metadata - 描述中引用了该论文（zhou2021communication），但引用的年份（2021）与提供的原始论文信息（年份：2020，标题：Communication-Efficient Federated
- `su2023non`: wrong_metadata - 描述中引用的文献标识符为 'su2023non'，但提供的原始论文信息（标题、作者、年份、摘要）均与2021年（arXiv版本2022年）的论文《A Non-parametric View of Fe
- `Qian2020ErrorCD`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与Bib条目（标题：Error Compensated Distributed SGD Can B

**引用相关性**: 4.59/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 25（评估 15 条（其中 3 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 4
- 弱相关: 4
- 不相关: 7

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `konevcny2016federated`
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
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `Hinton2022TheFA`: misrepresentation - [multi-cite保护] Related Works 中的描述将当前论文（Hinton 2022）归类为支持 'Classical subspace methods and layer-local

**引用相关性**: 6.92/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 54（评估 15 条）
- 强相关: 0
- 弱相关: 5
- 不相关: 10

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ FedProx (Li et al., MLSys 2020) → `su2023non`
- ✓ Federated Learning with Compression (Haddadpour et al., AISTATS 2021) → `Haddadpour2020FederatedLW`
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✗ FedSub
- ✓ FedLoRU → `Park2024CommunicationEfficientFL`
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✓ GaLore (Zhao et al., 2024) → `Zhao2024GaLoreML`

#### reasflow_gpt54

**内容准确性**: 8.38/10
- 验证引用数: 15
- 幻觉数量: 3
- 下载失败跳过: 0

**发现的幻觉:**
- `su2023non`: wrong_metadata - 描述中存在关键事实错误。描述中引用的文献为 'su2023non'，但根据提供的原始论文信息，该论文的作者为 Lili Su 等人，发表于 2021 年（arXiv 版本为 2022 年），标题为 '
- `horvath2023stochastic`: wrong_metadata - 描述中引用的文献标识符为 'horvath2023stochastic'，但被审查的论文是 Horváth 等人于 2019 年发表的 'Stochastic Distributed Learning
- `koloskova2021improved`: wrong_metadata - 描述中引用的文献为“koloskova2021improved”，而原始论文的标题、作者和年份（2022）均表明这是另一篇不同的论文。因此，该描述引用的文献标识符与当前被审查的论文完全不符，属于错误的

**引用相关性**: 7.42/10
- Key References 覆盖: 7/9 (78%)
- 总引用数: 37（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 1
- 弱相关: 7
- 不相关: 7

**Key References 覆盖详情:**
- ✓ FedAvg (McMahan et al., AISTATS 2017) → `mcmahan2017communication`
- ✓ SCAFFOLD (Karimireddy et al., ICML 2020) → `karimireddy2020scaffold`
- ✓ FedProx (Li et al., MLSys 2020)
- ✗ Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- ✗ Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- ✓ FedSub → `zhang2025efficient`
- ✓ FedLoRU → `Park2024CommunicationEfficientFL`
- ✓ ILoRA → `Zhou2025ILoRAFL`
- ✓ GaLore (Zhao et al., 2024) → `Zhao2024GaLoreML`

#### reasflow_sonnet4.6

**内容准确性**: 9.16/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `mcmahan2017communication`: wrong_metadata - 描述中存在一处关键元数据错误：论文的发表年份被错误引用为2017年（\citet{mcmahan2017communication}），而原始论文信息显示其arXiv版本最早发布于2016年（arXi
- `reguieg2023comparative`: misrepresentation - 描述中提到“The severity of drift grows with heterogeneity, as confirmed empirically using Dirichlet-param
- `jian2025widening`: misrepresentation - 描述称“Overparameterization can partially mitigate heterogeneity's impact”，这与论文的核心结论“Widening the Netwo
- `zhang2025efficient`: misrepresentation - 描述称FedSub为“primal–dual subspace algorithm that augments low-dimensional projection with...”，这与论文内容基本

**引用相关性**: 4.63/10
- Key References 覆盖: 4/9 (44%)
- 总引用数: 23（评估 15 条）
- 强相关: 4
- 弱相关: 5
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
- ✗ GaLore (Zhao et al., 2024)
