# Related Works Writing Plan

## Role
You are a senior researcher writing a Related Work section for a paper on Decentralized Optimization and Matrix-Aware Optimizers. Target venues: ICML, NeurIPS, ICLR.

## Task
Write a **Related Work** section covering three key areas, logically flowing to highlight the gaps that motivate our work (**SUDA-Muon**).

## Sections

### 1. Muon and Matrix-Aware Optimizers
* **Context:** Modern deep learning models heavily rely on matrix-structured parameters (e.g., Transformers, MLPs). Traditional Euclidean optimizers (SGD, Adam) ignore this geometry.
* **Muon Optimizer:** Replaces standard gradients with a polarized direction via the matrix sign operator ($\operatorname{msgn}$), computed exactly via SVD or approximately via Newton-Schulz iterations. This provides scale-invariant updates aligned with operator geometry.
* **Current Status:** Recent theoretical works (Shen et al., 2025; etc.) have established non-convex convergence guarantees for single-node Muon.
* **Key Issue:** These guarantees are limited to centralized or single-node settings.

### 2. Decentralized Optimization & Heterogeneity Correction
* **Context:** Decentralized Parallel SGD (DPSGD) avoids parameter server bottlenecks but suffers from "Client Drift" due to data heterogeneity (Non-IID data).
* **Heterogeneity Correction:** A rich literature has developed to correct this drift using tracking or primal-dual methods: EXTRA, Exact Diffusion (ED) / D$^2$, and Gradient Tracking (GT).
* **Unification (SUDA):** The SUDA framework elegantly unifies these diverse strategies into a single primal-dual recursion using low-degree polynomials of the mixing matrix, providing refined analyses where network topology only affects higher-order terms.
* **Key Issue:** These classic decentralized frameworks are designed for standard Euclidean gradients and do not accommodate the nonlinear matrix orthogonalization required by Muon.

### 3. Decentralized Muon (The Gap)
* **Initial Attempts:** DeMuon is the pioneering work that extends Muon to decentralized graphs by combining gradient tracking with Muon's matrix polarization.
* **The Gaps (Motivating our work):** 
    1. *Algorithmic constraint:* Existing designs like DeMuon are tied to a *single* communication template (gradient tracking). They lack a unified perspective to accommodate other powerful schemes like ED or EXTRA.
    2. *Theoretical constraint:* Current analyses do not exploit the refined, topology-separated convergence phenomena seen in SUDA-style frameworks. 
    3. *The Linear Speedup Problem:* It is a well-known property that decentralized SGD achieves asymptotic linear speedup (scaling with network size $N$). However, the interplay between Muon's non-linear local polarization and network averaging is deeply underexplored, leaving it unknown whether serverless Muon can achieve this speedup.

## Key References
- Muon Optimizer (Jordan et al., 2024)
- Convergence of Muon (Shen et al., 2025)
- Decentralized Parallel SGD (Lian et al., NeurIPS 2017)
- EXTRA (Shi et al., SIAM 2015)
- Exact Diffusion / D$^2$ (Yuan et al., 2017 / Tang et al., 2018)
- A Unified and Refined Convergence Analysis for Non-Convex Decentralized Learning (Alghunaim et al., IEEE TAC 2022)
- DeMuon (He et al., 2025)

## Writing Requirements
1. Each section should flow logically to the next, transitioning from optimization primitives to decentralized systems, and finally to their intersection.
2. The final section (Decentralized Muon) must clearly define the two-fold gap: the lack of a unified communication-correction structure, and the lack of clarity regarding topology separation and linear speedup.
