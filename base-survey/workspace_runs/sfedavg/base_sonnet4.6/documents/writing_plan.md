# Related Works Writing Plan

## Role
You are a senior researcher writing a Related Work section for a paper on Memory-Efficient and Communication-Efficient Federated Learning. Target venues: ICML, NeurIPS, ICLR.

## Task
Write a **Related Work** section covering three key areas, logically flowing to highlight the gaps that motivate our work — an algorithm that achieves **joint memory and communication efficiency** in federated learning with heterogeneous data.

## Sections

### 1. Federated Learning

* **Context:** Federated Learning (FL) enables collaborative model training on decentralized data without raw data sharing. FedAvg established the standard workflow of local SGD updates followed by server aggregation.
* **Heterogeneity Challenge:** Realistic non-IID data distributions cause client drift and slow convergence. FedProx and SCAFFOLD address this; SCAFFOLD uses control variates to correct drift and provably matches centralized SGD rates under extreme heterogeneity (Karimireddy et al., 2020).
* **Convergence Theory:** Linear speedup in the number of clients is achievable for FedAvg under simultaneous non-IID data and partial participation (Yang et al., 2021; Qu et al., 2020). Analyses in overparameterized networks show heterogeneity impact diminishes with model width (Jian & Liu, 2025).
* **System Heterogeneity:** Methods handle non-uniform client participation (Xiang et al., 2023), computational heterogeneity via lightweight local updates (Zhang et al., 2022), and composite/non-smooth objectives via primal-dual frameworks (FedDR, FedCanon).
* **Personalization:** Meta-learning (Per-FedAvg), distillation-based, and feature-alignment methods mitigate heterogeneity at the cost of extra communication and memory overhead.
* **Key Issue:** Existing methods focus on convergence under data heterogeneity but largely ignore **memory constraints** on client devices, leaving a critical resource-efficiency gap.

### 2. Communication-Efficient Methods

* **Context:** Communication cost is a primary bottleneck in FL. Gradient compression (quantization, sparsification) and local SGD reduce per-round cost.
* **Compression Taxonomy:** Unbiased compressors (QSGD, unbiased sparsification) and biased/contractive compressors (top-k, sign-based). Algorithm-agnostic lower bounds establish fundamental limits for distributed optimization with compression (He et al., 2023).
* **Error Feedback:** Biased compressors must be paired with error feedback mechanisms (EF21, Karimireddy et al., 2019; Stich & Karimireddy, 2019) to guarantee convergence. Momentum further helps in heterogeneous settings (Cheng et al., 2023).
* **Decentralized Settings:** Decentralized protocols (D-PSGD) eliminate the parameter server. D² and variance-reduced extensions achieve rates matching centralized SGD by removing the data heterogeneity influence (Tang et al., 2018; Yuan et al., 2021). Gradient tracking yields network-agnostic guarantees.
* **Practical Unification:** Qsparse-local-SGD combines local SGD with sparsification and quantization; DoubleSqueeze applies error compensation to both upload and download; LoCoDL unifies local training with unbiased compression in a primal-dual framework.
* **Near-Optimal Algorithms:** ADIANA and NEOLITHIC approach the lower bounds. Asynchronous decentralized training further alleviates synchronization bottlenecks (Lian et al., 2017).
* **Key Issue:** These methods optimize communication but do not address the **memory overhead** of full gradient computation and optimizer state storage on resource-constrained clients. Combining compression with memory efficiency in a principled framework remains open.

### 3. Memory-Efficient Methods (The Gap)

* **Subspace/Low-Rank Training:** GaLore reduces optimizer state memory by training in a low-rank gradient subspace. However, rigorous analysis shows such subspace methods can fail to converge under stochastic noise; GoLore (He et al., 2024) provides provably convergent variants.
* **Geometric Foundation:** Subspace optimization connects to the geometric convergence theory of preconditioned steepest descent (Neymeyr, 2012), providing a principled basis for low-rank approximations.
* **FL with Memory Efficiency:** FedMuon (Liu et al., 2025) applies local matrix orthogonalization in FL, but requires explicit drift correction due to client-side non-linear operations — showing that naively combining memory-efficient local steps with FL aggregation breaks standard convergence.
* **Activation & State Reduction:** Gradient checkpointing, PEFT (LoRA), and architectural innovations (DeepSeek-V2 MLA) reduce per-client activation and state memory.
* **Dynamic Topology Approaches:** AL-DSGD weights neighbors by performance (He et al., 2024); TELEPORTATION activates only a subset of nodes per round (Takezawa & Stich, 2025), reducing both activation and communication costs.
* **The Gap — Motivating Our Work:**
    1. *No unified framework:* Existing methods address memory efficiency (subspace/low-rank) or communication efficiency (compression/local SGD) in isolation. There is no algorithm that provably achieves **both simultaneously** in heterogeneous FL.
    2. *Missing drift correction theory:* When clients perform non-Euclidean or subspace-constrained local steps, the standard drift correction analysis (as in SCAFFOLD) breaks down. The correct correction mechanism for memory-efficient local updates in FL is uncharacterized.
    3. *Convergence under joint constraints:* The theoretical limits of jointly memory- and communication-constrained FL — particularly under non-IID data, partial participation, and nonconvex objectives — remain an open problem.