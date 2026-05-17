# Related Works 评测报告

**评测时间**: 2026-03-27T12:44:29.513389
**打分模型**: dpsk
**评测文章**: base_dpsk, base_gpt51, base_gpt54, base_sonnet4.6, reasflow_dpsk, reasflow_gpt51, reasflow_gpt54, reasflow_sonnet4.6
**评测维度**: [1, 2]

---

## 执行摘要

### 内容准确性排名（1-10分）
1. **reasflow_dpsk**: 9.79/10
2. **reasflow_gpt51**: 9.4/10
3. **reasflow_gpt54**: 8.8/10
4. **base_sonnet4.6**: 8.38/10
5. **reasflow_sonnet4.6**: 8.05/10
6. **base_gpt54**: 5.59/10
7. **base_dpsk**: 5.08/10
8. **base_gpt51**: 5.0/10

### 引用相关性排名（1-10分）
1. **reasflow_dpsk**: 8.8/10
2. **base_sonnet4.6**: 8.24/10
3. **base_gpt54**: 6.6/10
4. **reasflow_gpt51**: 6.14/10
5. **base_dpsk**: 5.25/10
6. **reasflow_gpt54**: 4.53/10
7. **base_gpt51**: 4.0/10
8. **reasflow_sonnet4.6**: 2.13/10

### 本组客观总分（多配置汇总）
- **每篇总分** = 内容准确性(0–10) + 引用相关性(0–10)，最高 **20**。
- **本组总分 run_mean_total** = 各生成配置上述总分的算术平均 = **13.223** / 20
- 跨配置平均 · 内容准确性: **7.511** / 10
- 跨配置平均 · 引用相关性: **5.711** / 10
- 各配置总分（CA+CR）:
  - **reasflow_dpsk**: 18.59 / 20
  - **base_sonnet4.6**: 16.62 / 20
  - **reasflow_gpt51**: 15.54 / 20
  - **reasflow_gpt54**: 13.33 / 20
  - **base_gpt54**: 12.19 / 20
  - **base_dpsk**: 10.33 / 20
  - **reasflow_sonnet4.6**: 10.18 / 20
  - **base_gpt51**: 9.0 / 20

---

## 详细评测结果

### 客观评测（维度1-2）

#### base_dpsk

**内容准确性**: 5.08/10
- 验证引用数: 15
- 幻觉数量: 12
- 下载失败跳过: 0

**发现的幻觉:**
- `he2025demuon`: misrepresentation - 描述声称DeMuon是第一个尝试去中心化Muon的工作，并指出其结合了梯度追踪与Muon的牛顿-舒尔茨正交化。然而，根据提供的论文摘要和引言，DeMuon论文本身明确宣称自己是第一个将Muon扩展到去
- `huang2025limuon`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib 条目标题为 'LiMuon: Light and Fast Muon Optimizer for Large Models'，作
- `jordanmuon`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib条目作者为Michael I. Jordan，年份2023；所有候选作者均不包含此人，且候选年份均为2025年，与Bib条目年份不
- `wang2024proximal`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者和年份均与待匹配条目（标题：A Decentralized Proximal Gradient Track
- `grishina2025accelerating`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有任何一篇论文的标题、作者或年份与待匹配条目相符。待匹配条目标题为'Accelerating Newton-Schulz I

**引用相关性**: 5.25/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 14（评估 15 条（其中 7 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 1
- 弱相关: 7
- 不相关: 7

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `sato2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018) → `alghunaim2023local`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `yuan2021unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_gpt51

**内容准确性**: 5.0/10
- 验证引用数: 0
- 幻觉数量: 0
- 下载失败跳过: 0

**引用相关性**: 4.0/10
- Key References 覆盖: 4/7 (57%)
- 总引用数: 0（评估 0 条）
- 强相关: 0
- 弱相关: 0
- 不相关: 0

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018) → `yuan2017exact`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✗ DeMuon (He et al., 2025)

#### base_gpt54

**内容准确性**: 5.59/10
- 验证引用数: 15
- 幻觉数量: 9
- 下载失败跳过: 0

**发现的幻觉:**
- `grishina2025chebyshev`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有任何一篇论文的标题、作者或年份与待匹配条目相符。待匹配条目标题为'Accelerating Newton-Schulz I
- `sfyraki2025lionsmuons`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib条目标题为'Lions and Muons: Optimization via Stochastic Frank-Wolfe'，作
- `lau2025polargrad`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中所有论文的标题、作者、年份均与待匹配论文（标题：PolarGrad: A Class of Matrix-Gradient O
- `bernstein2024oldoptimizer`: misrepresentation - [multi-cite保护] 描述将论文归入关于“矩阵正交化”和“极化方向”的系列工作，但论文的实际内容与此无关。论文的核心论点是：通过关闭指数移动平均，Adam、Shampoo和Prodigy等优化
- `xin2021topologyindependent`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib 条目标题强调 'Stochastic Proximal Gradient Framework' 和 'Topology-Inde

**引用相关性**: 6.6/10
- Key References 覆盖: 5/7 (71%)
- 总引用数: 31（评估 15 条（其中 7 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 4
- 不相关: 8

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✗ Convergence of Muon (Shen et al., 2025)
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017dpsgd`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018) → `tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### base_sonnet4.6

**内容准确性**: 8.38/10
- 验证引用数: 15
- 幻觉数量: 5
- 下载失败跳过: 0

**发现的幻觉:**
- `nedic2009distributed`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib条目标题为'Distributed Subgradient Methods for Multi-Agent Optimizatio
- `he2025lowrank`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有任何一篇论文的标题、作者和年份与待匹配的 Bib 条目（标题：Low-Rank Orthogonalization for
- `kingma2014adam`: misrepresentation - 描述中称Adam“对待每个参数条目对称，忽略了矩阵的内在算子几何结构”，这一论断本身是准确的，因为它是对Adam算法特性的客观描述。然而，在论文《Adam: A Method for Stochast
- `yuan2021removing`: misrepresentation - 描述中引用的论文（yuan2021removing）标题与提供的原始论文标题一致，年份（2021）与arXiv版本提交年份相符，核心主题（消除数据异质性影响、提升对网络拓扑的依赖性）也匹配。然而，描述

**引用相关性**: 8.24/10
- Key References 覆盖: 6/7 (86%)
- 总引用数: 23（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 5
- 弱相关: 7
- 不相关: 3

**Key References 覆盖详情:**
- ✓ Muon Optimizer (Jordan et al., 2024) → `jordan2024muon`
- ✗ Convergence of Muon (Shen et al., 2025)
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✓ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018) → `tang2018d2`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_dpsk

**内容准确性**: 9.79/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `Alghunaim2023LocalEF`: misrepresentation - 描述中提到“matrix preconditioning can accelerate convergence in distributed settings”，并将该论文（Alghunaim2023

**引用相关性**: 8.8/10
- Key References 覆盖: 6/7 (86%)
- 总引用数: 47（评估 15 条）
- 强相关: 4
- 弱相关: 5
- 不相关: 6

**Key References 覆盖详情:**
- ✓ Muon Optimizer (Jordan et al., 2024) → `tveit2025muon`
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `Lian2017AsynchronousDP`
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✓ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018) → `Tang2018D2DT`
- ✓ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022) → `alghunaim2022unified`
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt51

**内容准确性**: 9.4/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `Yang2015LearningW`: misrepresentation - Related Works 中的描述将 Yang2015LearningW 与稀疏子空间聚类和局部训练公式（local-training formulations）联系起来，暗示该论文与联邦学习中的客

**引用相关性**: 6.14/10
- Key References 覆盖: 4/7 (57%)
- 总引用数: 63（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 5
- 不相关: 8

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✓ Decentralized Parallel SGD (Lian et al., NeurIPS 2017) → `lian2017can`
- ✓ EXTRA (Shi et al., SIAM 2015) → `shi2015extra`
- ✗ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_gpt54

**内容准确性**: 8.8/10
- 验证引用数: 15
- 幻觉数量: 4
- 下载失败跳过: 0

**发现的幻觉:**
- `shazeer2018adafactor`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: 候选列表中没有任何一篇论文的标题、作者和年份与待匹配的Bib条目（Adafactor: Adaptive Learning Rates 
- `Vogels2019PowerSGDPL`: fabricated - 候选共 10 条，LLM 判定无与 Bib 对应的论文。理由: Bib条目中作者为Thijs Vogels, Sai Praneeth Karimireddy, Martin Jaggi，年份为201

**引用相关性**: 4.53/10
- Key References 覆盖: 3/7 (43%)
- 总引用数: 38（评估 15 条（其中 2 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 3
- 弱相关: 1
- 不相关: 11

**Key References 覆盖详情:**
- ✓ Muon Optimizer (Jordan et al., 2024) → `liu2025muon`
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D^2 (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`

#### reasflow_sonnet4.6

**内容准确性**: 8.05/10
- 验证引用数: 15
- 幻觉数量: 6
- 下载失败跳过: 0

**发现的幻觉:**
- `Takezawa2025FedMuonFL`: misrepresentation - 描述中存在不准确的细节。描述称论文 'introduce momentum aggregation and local-global alignment corrections to eliminat
- `Hu2025ABD`: misrepresentation - 描述存在实质性错误，会误导读者对论文工作的理解。具体问题如下：1. 描述将论文提出的“Exact-Diffusion with Momentum (EDM)”方法归入“gradient trackin
- `abreu2025potential`: misrepresentation - 描述中引用了该论文（Abreu et al., 2025），但引用的内容不完整且存在轻微的误导性拼接。论文摘要明确指出，与SOAP、Muon等强基线相比，完整的Gauss-Newton预条件处理实现了
- `Kong2024DecentralizedBO`: misrepresentation - 描述中关于该论文的部分存在不准确之处。论文《Decentralized Bilevel Optimization: A Perspective from Transient Iteration Com
- `Goyal2017AccurateLM`: misrepresentation - 描述完全错误。该论文（Goyal et al., 2017）的核心贡献是研究大规模分布式同步SGD，通过线性缩放学习率和预热方案，实现在大批量（如8192）下高效训练ImageNet，并保持模型精度。

**引用相关性**: 2.13/10
- Key References 覆盖: 2/7 (29%)
- 总引用数: 21（评估 15 条（其中 1 条为内容准确性检测的完全捏造，已直接计为不相关））
- 强相关: 2
- 弱相关: 2
- 不相关: 11

**Key References 覆盖详情:**
- ✗ Muon Optimizer (Jordan et al., 2024)
- ✓ Convergence of Muon (Shen et al., 2025) → `shen2025convergence`
- ✗ Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- ✗ EXTRA (Shi et al., SIAM 2015)
- ✗ Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- ✗ A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- ✓ DeMuon (He et al., 2025) → `he2025demuon`
