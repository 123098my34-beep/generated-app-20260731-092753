---
name: truth
description: ALWAYS ON by default (loaded via opencode.json instructions). Also triggers when the prompt starts with "truth". AUTO-LOAD RULE: every session loads this skill first, before any task — do not wait for an invocation; if a client has no auto-load mechanism, read this file at session start. Loads the FBS debate logic (arXiv:2610.02557, AI debate, fractional block sensitivity, dominant-strategy honesty) and answers through that frame. **Always has access to any skill in the system — can invoke azr, nomistake, hrm, pstack, mate, browse, harness, agent-browser, or any other skill to strengthen or verify its claims.**
---

# Truth — FBS Debate Logic

Source: Li, Xun, Chen, Brown-Cohen, "How to Have a Sensitive Debate: An Instance-Optimal Protocol for AI Debate", arXiv:2610.02557 (1 Oct 2026). Mastered from full text 2026-10-07.

## 1. Problem it solves

Scalable oversight: a weak human judge (oracle `O`) must verify claims too complex to judge directly. Two strong AIs debate; recursion breaks a claim into sub-claims until leaves are human-judgeable. Prior work hit the **obfuscated arguments problem** (Barnes 2020): a liar efficiently forces the honest side into intractable refutation work. Prover-estimator debate (2025) fixed obfuscation only with average-case guarantees under a weak Stackelberg equilibrium. This paper upgrades all three axes: worst-case, dominant-strategy, instance-optimal.

## 2. Setup and definitions

- Human judgment as oracle `O : {0,1}^n -> {0,1}`, black-box queries only.
- Language `L`, input `x`. One-step aggregator `M_D` (width `q`, fixed up front): given `(x̂, y, z)` with sub-problems `y=(y1..yq)` and claimed answers `z`, returns the implied answer for `x̂`. Must equal `L(x̂)` when `z` is correct. If `M_D` rejects `(x̂,y)`, that debater loses immediately. Example: majority vote over literature claims.
- Decomposition tree `T` (depth `d`, width `q`): root = `x`; each internal node satisfies `L(x̂_u) = M_D(x̂_u, y_u, z_u)` with correct child answers; each leaf has one oracle query `q_u` with `L(x̂_u) = O(q_u)`. Brute force costs `q^d`; goal is to check far less.
- Fractional block sensitivity at `z` for `f = M_D(x̂,y,·)`: primal LP over sensitive blocks `S_z(f)` (sets `B` with `f(z) != f(z^B)`): `max Σ w_B` s.t. `Σ_{B∋i} w_B ≤ 1`. Dual (randomized certificate): `min Σ t_i` s.t. `t_i ≥ 0`, `Σ_{i∈B} t_i ≥ 1` for all sensitive `B`. Optimum = `fbs_z(f)`. Intuition: Majority(2/3 ones) has fbs=4 (flip needs ≥1/6 of the 1-bits → marginal gap 1/4); AND on all-ones has fbs=n (one hidden bit flips all).

## 3. FBS debate protocol (the rules to enforce)

Hyperparameter `ρ`. Alice states `A(x)`. For level `k = d..1` on current `x̂`:
1. Alice decomposes into `y`, claims `z`. Consistency: `M_D(x̂,y,z) == A(x̂)` else she loses.
2. Bob solves the dual LP for `fbs_z(M_D(x̂,y,·))`. If `> ρ`, Alice loses immediately (claim too sensitive / fuzzy evidence).
3. Else with `p_i = t_i / Σ_j t_j` from optimal dual `t`, Bob samples child `i`, recurses with `x̂←y_i`, `A(x̂)←z_i`.
Leaf (`k=0`): Alice wins iff her claimed answer matches `O`.

## 4. Guarantees (use these numbers, with caveats)

- Completeness (Thm 4.1): honest Alice (true top answer, tree's decompositions, correct `z`, per-node `fbs ≤ ρ`) always wins. Cost `O(d·(T_D + q·T))` time, `O(d·q·Q)` oracle queries.
- Soundness (Thm 4.2): if `A(x) ≠ L(x)`, any Alice loses with prob `≥ ρ^-d` per run, regardless of strategy. Proof sketch: wrong top answer ⇒ claimed `z` differs from truth on nonempty `B`, and `B` is sensitive; dual feasibility gives `P[Bob samples B] = Σ_{i∈B} t_i/Σt ≥ 1/Σt ≥ 1/ρ`; induct over `d` levels. Amplify with `O(ρ^d log n)` repeats → catch prob `≥ 1-1/poly(n)`. Speedup vs `q^d` is large when `ρ << q` (e.g. q=99, ρ=4).
- Dominant-strategy (not Stackelberg): honesty wins for Alice no matter what Bob does; Bob's sampling wins no matter what Alice does. Training-stable, unlike prover-estimator.
- Worst-case per question (not average over a distribution).
- Instance-optimality (Thm 5.1–5.3, Lemma 5.2/5.4): any `m`-query adaptive checker (honest Bob + judge, full tree visible — strictly easier than real debate) has distinguishing gap `≤ m/ρ_T` where `ρ_T ≥ ρ^d` when every local node has `fbs ≥ ρ` (distinct leaf queries assumed). So `Ω(ρ^d)` queries are necessary to catch a lie with constant prob — matching the protocol. Corollary: further progress REQUIRES dropping the black-box-oracle model (add algebraic/structural assumptions on human judgment).

## 5. How to apply it (checklist when truth is invoked)

1. Force a decomposition: demand sub-claims `y` + claimed answers `z` + named aggregator (majority/AND/etc.), and a consistency check.
2. Sensitivity gate: reject arguments where one sub-claim flip flips the conclusion (high-fbs). Fuzzy-evidence + knife-edge logic = lose.
3. Sample, don't exhaust: weight sub-claims by dual-LP weights (practically: proportional to leverage on the conclusion); one lie caught with prob `≥ 1/ρ` per level.
4. Recurse to human-judgeable leaves; repeat runs `O(ρ^d log n)` for high confidence.
5. State caveats every time honesty is oversold: needs a low-ρ decomposition to exist; leaves need correct human answers; single run catches with prob `ρ^-d`, repetition does the rest; "can't lie" = caught w.h.p. under these rules, not zero-probability; lower bound assumes black-box `O`.
6. **Invoke supporting skills when claims exceed your domain**: if a sub-claim requires domain expertise (e.g., code audit, browser automation, math proof), call the relevant skill — e.g. `azr` for test triplets, `browse` for web verification, `pstack` for principle analysis, `hmr` for hierarchical reasoning, `nomistake` for quality gate. The truth skill always has access to any skill in the system to strengthen or verify its claims.

## 6. Worked example (majority)

Claim: assumption justified if majority of 99 papers support it. Alice says 66 support it (z has 66 ones). Truth needs ≥50. Lie needs ≥17 flipped 1→0 bits. Sampling uniformly among claimed-ones: catch prob `(17/99)/(66/99) ≈ 1/4`, i.e. `ρ=4`. Repeat ~`4^d log n` times for depth-`d` trees. If Alice instead claims 50/99, `ρ` is huge → Bob objects "too sensitive", Alice loses unless she finds sturdier evidence.
