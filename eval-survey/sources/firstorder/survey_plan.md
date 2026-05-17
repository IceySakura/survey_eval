# Related Works Writing Plan

## Role
You are a senior researcher writing a Related Work section for a paper on Convergence Analysis of First-Order Optimization Methods. Target venues: Mathematical Programming, SIAM Journal on Optimization, Foundations of Computational Mathematics.

## Task
Write a **Related Work** section covering three key areas, logically flowing to highlight the gaps that motivate our work on unified convergence frameworks for composite first-order methods under relaxed smoothness assumptions.

## Sections

### 1. Subgradient Methods and Classical Convergence Theory
* **Context:** Subgradient methods form the backbone of nonsmooth convex optimization. The validation of subgradient optimization (Held, Wolfe, Crowder, 1973) established the practical viability of these methods for combinatorial problems via Lagrangian relaxation. Subsequent work developed aggregate subgradient methods (Kiwiel, 1985) and primal-dual subgradient formulations (Nesterov, 2007) that achieve optimal O(1/√T) rates for general convex problems.
* **Key Issue:** Classical subgradient theory assumes convexity or Lipschitz continuity globally, limiting its applicability to modern problems with composite structure or local smoothness properties.

### 2. Proximal and Splitting Methods
* **Context:** Proximal point algorithms and operator splitting methods provide a powerful framework for structured optimization. The Douglas-Rachford splitting method and its connection to the proximal point algorithm (Eckstein, Bertsekas, 1992) unified a broad class of decomposition approaches. Finite termination properties of proximal methods (1988), descent methods for composite nondifferentiable problems (Fletcher, 1985), and convergence of descent methods for semi-algebraic problems (Attouch, Bolte, Svaiter, 2013) have progressively expanded the scope of convergence guarantees.
* **Key Issue:** While proximal methods handle nonsmoothness elegantly, their convergence theory often requires strong structural assumptions (semi-algebraicity, KL property) that may not hold in general, and the interplay between splitting parameters and convergence rate is incompletely understood.

### 3. Modern Complexity and Acceleration (The Gap)
* **Context:** Recent work has established tight complexity bounds for first-order methods through constructive approaches and connections to differential equations. Error-bound-based complexity analysis (Bolte et al., 2016) revealed how regularity of the objective governs convergence speed. The effect of deterministic noise in subgradient methods (d'Aspremont, 2008), acceleration via cubic regularization (Nesterov, 2008), and coordinate descent complexity analysis (2016, 2019) have deepened our understanding of achievable rates.
* **The Gaps (Motivating our work):**
    1. *Unification gap:* Existing convergence frameworks treat smooth, nonsmooth, and composite problems separately; a unified theory that seamlessly interpolates between smoothness regimes and captures composite structure is lacking.
    2. *Relaxed assumptions gap:* Most complexity results assume global Lipschitz gradient continuity or bounded subgradients; convergence under weaker, locally-defined smoothness conditions (generalized smoothness, relative smoothness) remains fragmented.
    3. *Rate tightness gap:* While lower bounds exist for specific problem classes, matching upper bounds for composite methods under relaxed assumptions are often loose, leaving the optimal achievable rate uncertain.

## Key References
- Validation of subgradient optimization (Held, Wolfe, Crowder, 1973)
- An aggregate subgradient method for nonsmooth convex minimization (Kiwiel, 1985)
- Descent methods for composite nondifferentiable optimization (Fletcher, 1985)
- Finite termination of the proximal point algorithm (1988)
- Douglas-Rachford splitting and proximal point algorithm for monotone operators (Eckstein, Bertsekas, 1992)
- Primal-dual subgradient methods for convex problems (Nesterov, 2007)
- Accelerating cubic regularization of Newton's method (Nesterov, 2008)
- The effect of deterministic noise in subgradient methods (d'Aspremont, 2008)
- Convergence of descent methods for semi-algebraic and tame problems (Attouch, Bolte, Svaiter, 2013)
- From error bounds to complexity of first-order descent methods (Bolte et al., 2016)

## Writing Requirements
1. Each section should progress from classical to modern, building a narrative from foundational subgradient theory through structured splitting methods to contemporary complexity analysis.
2. The final section must clearly define the three-fold gap: lack of a unified framework across smoothness regimes, fragmented results under relaxed smoothness, and loose rate bounds for composite methods.
3. Emphasize both algorithmic contributions (method design, splitting strategies) and theoretical advances (complexity bounds, convergence certificates).
