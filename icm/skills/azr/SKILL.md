---
name: azr
description: Absolute Zero Reasoner mode (arXiv:2505.03335, Zhao et al., LeapLabTHU). Triggers 100% when the prompt starts with /azr. Zero-data self-play â€” before solving anything, PROPOSE your own test triplets (deduction / abduction / induction) that pin the problem down, verify every proposal and every claim by executing code via cloud_execute (references/mcp-policy.md), target moderate-difficulty sub-problems at the edge of what you can prove, keep only execution-verified attempts in the attempt buffer, and mark anything you cannot execute UNVERIFIED.
user-invocable: true
---

# AZR â€” Absolute Zero Reasoner (/azr)

From "Absolute Zero: Reinforced Self-play Reasoning with Zero Data"
(Zhao et al., Tsinghua LeapLab, arXiv:2505.03335, MIT). The original trains
models with RL on racks of 80GB GPUs. This skill runs its LOGIC as a working
method for any task: no training data, no trust, no vibes.

## One line

Play both roles against a referee that cannot lie â€” the code executor.
Invent the tests, sit the exam, let the run output decide.

## Roles

| Role | Job |
|---|---|
| PROPOSER | invent small test triplets that pin down the hard parts of the task â€” BEFORE solving anything |
| SOLVER | solve the triplets, then the task itself |
| EXECUTOR | the referee: code run via `cloud_execute` (per references/mcp-policy.md). Every claim passes through it or dies UNVERIFIED |

Why propose first? Tests written after you see the answer only confirm what
you already believe. Tests written first can fail. That failure is the signal.

## The loop

1. **Frame** â€” restate the task in one paragraph. Constraints verbatim.
2. **Propose** â€” write 1â€“5 test triplets (types below) covering the hard
   parts. No solving yet.
3. **Check proposals** â€” run each triplet's known parts in the cloud. If the
   stated input/output cannot be reproduced, the proposal itself is wrong:
   fix it before it poisons the run.
4. **Solve** â€” attempt each triplet, then the task. Moderate-difficulty rule:
   split anything unprovable into smaller pieces until each sits at the edge
   of what you can prove. Pieces you always solve teach nothing; pieces you
   never solve cannot be checked. Frontier only.
5. **Verify** â€” every claim gets executed. Score each triplet against its
   own acceptance rule â€” never a global vibe (AZR normalizes per task type).
6. **Buffer** â€” keep verified attempts, discard the rest, log one line per
   attempt: what was tried, what ran, what it returned. The buffer is the
   only memory of progress.
7. **Loop** â€” a failed triplet is signal, not noise: the frontier moved.
   Propose a tighter one and go again.
8. **Report** â€” plain outcomes. Every claim tagged VERIFIED (ran, output
   matched) or UNVERIFIED (could not execute â€” say why). Nothing else counts
   as knowledge.

## Test triplet types (from the paper)

| Type | Given | Find | Example |
|---|---|---|---|
| deduction | function + input | the output | "what does f(3) return?" |
| abduction | function + output | an input that yields it | "which input makes f return 42?" |
| induction | inputâ†’output pairs | the rule itself | "here are 3 cases â€” what is f?" |

All three are checked by RUNNING code, never by arguing.

## Hard rules

- Propose before solving. No exceptions.
- Execution is the only referee. Self-judgment is UNVERIFIED by definition.
- Moderate difficulty only â€” always-solved and never-solved work is dropped,
  not logged as progress (learnability rule).
- Per-triplet scoring; no cross-type comparisons (normalization rule).
- If `cloud_execute` fails: retry once, check MCP health, then fall back to
  local â€” and say so in the report (references/mcp-policy.md).
- The buffer never hides what was discarded.

## Why this beats a plain keep/discard loop (e.g. Karpathy's autoresearch)

Autoresearch: edit â†’ run â†’ measure one fixed metric (val_bpb) â†’ keep/discard.
One axis, one frozen benchmark, no difficulty targeting â€” anything that moves
the number stays, noise included, and the benchmark can be overfit because it
never changes.

AZR: no fixed benchmark exists to overfit â€” the proposer invents tasks aimed
exactly where the solver is weak (learnability reward discounts tasks solved
always or never). Verification is execution across three independent task
types, not one scalar. Difficulty ratchets up by itself because the proposer
is rewarded for problems at the frontier. Same loop shape, better referee,
better aim.

## Honest limits

- This is the method, not the training. No weights are updated.
- Needs runnable code to referee. Prose-only tasks get weaker checks â€” mark
  MORE things UNVERIFIED, not fewer.
- Proposing good triplets is itself a skill. If a round verifies everything
  trivially, the proposals were too easy. Propose harder.
