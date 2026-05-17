# Related Works Writing Plan

## Role
You are a senior researcher writing a Related Work section for a paper on Communication-Efficient Federated Learning. Target venues: ICML, NeurIPS, ICLR.

## Task
Write a **Related Work** section covering three key areas, highlighting gaps that motivate our work (Subspace-SCAFFOLD).

## Sections

### 1. Federated Learning
* **FedAvg** as the foundational algorithm
* **Data Heterogeneity Challenge:** Non-IID data causes "Client Drift"
* **Variance Reduction:**
    - SCAFFOLD: control variates to correct gradient direction
    - FedProx: proximal regularization
* **Key Issue:** These methods require full-dimension updates and auxiliary variables, creating memory overhead for large models

### 2. Communication Compression
* **Quantization:** Reducing bit-width of transmitted values
* **Sparsification:** Transmitting only top-k gradients
* **Error Feedback (EF):** Accumulating compression error to preserve convergence
* **Key Issue:** EF requires storing error vectors ($\mathbb{R}^d$), exacerbating memory bottleneck; compression introduces variance that hurts convergence under heterogeneity

### 3. Subspace Learning
* **Low-Rank Gradient Approximation:** GaLore, etc.
* **Subspace Optimization in FL:** FedSub, FedLoRU, ILoRA
* **Benefits:** Reduces compute, communication, and memory simultaneously
* **Key Issue (The Gap):** Existing subspace methods are incompatible with SCAFFOLD-like variance reduction. When the subspace switches, historical control variate accumulation becomes invalid.

## Key References
- FedAvg (McMahan et al., AISTATS 2017)
- SCAFFOLD (Karimireddy et al., ICML 2020)
- FedProx (Li et al., MLSys 2020)
- Federated Learning with Compression (Haddadpour et al., AISTATS 2021)
- Communication-Efficient FL via Compressed Error Feedback (Valdeira et al., 2024)
- FedSub
- FedLoRU
- ILoRA
- GaLore (Zhao et al., 2024)
