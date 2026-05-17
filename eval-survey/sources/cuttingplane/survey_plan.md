# Related Works Writing Plan

## Role
You are a senior researcher writing a Related Work section for a paper on Cutting Plane Methods for Mixed Integer Programming. Target venues: Mathematical Programming, SIAM Journal on Optimization, Operations Research.

## Task
Write a **Related Work** section covering three key areas, logically flowing to highlight the gaps that motivate our work on strengthened cutting plane generation via structured disjunctions.

## Sections

### 1. Classical Cutting Plane Theory and Gomory Cuts
* **Context:** The cutting plane approach to integer programming originated with Gomory's seminal fractional cuts and was later formalized through the theory of valid inequalities and polyhedra. Chvátal's work on closures provided a systematic framework for iteratively tightening LP relaxations, while intersection cuts from outer polars (Balas, 1971) offered a geometric perspective on cut generation from convex sets.
* **Key Issue:** Classical Gomory cuts and Chvátal closure rounds converge slowly in practice; optimizing over even the first Chvátal closure is computationally expensive, motivating the search for stronger, more targeted cut families.

### 2. Lift-and-Project and Disjunctive Cuts
* **Context:** The lift-and-project framework (Balas, Ceria, Cornuéjols, 1993) introduced a systematic way to derive cuts for mixed 0-1 programs by exploiting simple disjunctions in a lifted space. Disjunctive programming provides a unifying theory that subsumes Gomory cuts, split cuts, and intersection cuts as special cases. Extensions to conic settings (conic mixed-integer rounding) and to general mixed-integer programs have broadened the applicability of these methods.
* **Key Issue:** While lift-and-project cuts are theoretically powerful, their practical strength depends heavily on the choice of disjunctions, and current selection heuristics lack structural guarantees on cut quality.

### 3. Modern Cut Generation and Integration with Branch-and-Bound (The Gap)
* **Context:** Recent advances focus on understanding the rank and strength of various cut families, integrating cut generation within branch-and-bound frameworks (branch-and-cut), and developing complexity-theoretic perspectives on cutting plane proofs. Valid inequalities derived from specific substructures (knapsack, mixing sets, simple mixed-integer sets) have proven especially effective in practice.
* **The Gaps (Motivating our work):**
    1. *Structural gap:* Existing disjunctive cut procedures select disjunctions heuristically without exploiting the algebraic structure of the underlying integer lattice, leaving potential strength on the table.
    2. *Computational gap:* The separation problem for strong cut families remains expensive; scalable methods that balance cut strength and separation cost are needed.
    3. *Theoretical gap:* The relationship between lattice geometry and achievable closure rank for structured disjunctions is not well understood, limiting our ability to predict and guarantee convergence speed.

## Key References
- Intersection cuts from outer polars (Balas, 1971)
- Chvátal closures for mixed integer programming (Cook, Kannan, Schrijver, 1988)
- Lift-and-project cutting plane algorithm for mixed 0-1 programs (Balas, Ceria, Cornuéjols, 1993)
- Optimizing over the first Chvátal closure (Fischetti, Lodi, 2003)
- Valid inequalities based on simple mixed-integer sets (Atamtürk, 2005)
- Valid inequalities for mixed integer linear programs (Marchand et al., 2007)
- Conic mixed-integer rounding cuts (Atamtürk, Narayanan, 2008)
- Generalized intersection cuts and a new cut generating paradigm (Conforti, Cornuéjols, Zambelli, 2011)
- Complexity of branch-and-bound and cutting planes in mixed-integer optimization (2022)

## Writing Requirements
1. Each section should flow logically from foundational theory to modern algorithmic practice, culminating in the identified gaps.
2. The final section must clearly articulate the three-fold gap: heuristic disjunction selection without lattice-geometric guarantees, computational cost of separation, and incomplete understanding of closure rank for structured families.
3. Cover both theoretical contributions (polyhedral theory, closure rank) and computational methods (separation algorithms, branch-and-cut integration).
