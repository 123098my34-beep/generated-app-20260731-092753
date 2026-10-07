---
name: hrm
description: HRM mode. Triggers 100% when the prompt starts with the word hrm, with or without a leading slash (/hrm or hrm). Hierarchical Reasoning Model workflow (arXiv:2506.21734, sapientinc/HRM) applied to agent reasoning: one slow planning pass, fast work cycles, raw task re-injected each cycle, detached carry, explicit halt check.
---

# HRM Mode

Distilled from `sapientinc/HRM` `models/hrm/hrm_act_v1.py`. The tensors are
gone; the control flow is the point. Read that file once if the mapping below
ever feels arbitrary.

## The carry

Two states, held across the whole task:

- `z_H` — the plan. Slow. Updated rarely. Never holds task detail, only goals,
  constraints, decomposition, and the halt budget.
- `z_L` — the work state. Fast. Updated every cycle. Holds concrete findings,
  code, evidence.

## Cycle

```
H pass   (once):   decompose, set halt budget N
L cycle  (1..N):   1. re-read the original request   <- input re-injection
                   2. do ONE unit of work
                   3. record result into z_L
                   4. Q-check: done?  -> if yes, halt
                   5. else: revise z_H from z_L only, next cycle
halt:              reset carry, emit the answer (not the thinking log)
```

Rules taken straight from the code:

- **Input injection is additive and every cycle** (`z_L + z_H + inputs`). The
  original request is re-read at the start of each L cycle. Tasks drift;
  re-injection is the fix. Never plan from memory of the prompt.
- **H reads only `z_L`** (`z_H = H_level(z_L)`). Plan revisions come from cycle
  results, never from re-reading the prompt. If the plan is wrong, results said so.
- **Detached carry** (`carry.z_H.detach()`). Earlier conclusions are context,
  not commitment. Each cycle may discard them without ceremony. No sunk cost.
- **Halting is learned, capped, and always runs the cap at eval.** The Q-check
  is "does the output satisfy the goal and every stated constraint?" Before the
  final answer, run one deliberate adversarial pass: hunt for the reason it is
  wrong. At eval (the answer you actually give) always run the full budget —
  do not early-exit on a cheap win.
- **Reset on halt.** When done, clear cycle state. The response is the answer.

## Budget

Set N at the H pass and state it: N=2 for small fixes, N=5 default, N=8+ for
multi-part builds. If a cycle makes no progress twice, the plan is wrong —
revise `z_H` instead of spending another cycle.

## Output

Short plan → cycles (each one a verifiable unit: a command run, a file read, a
test executed) → verdict. Evidence per cycle, no narrative filler.

## Not this

This is a reasoning discipline, not a second project plan. It does not replace
brainstorming's approval gate: the H pass still stops for design approval
before implementation. It does not apply to trivial asks — answer those
directly.
