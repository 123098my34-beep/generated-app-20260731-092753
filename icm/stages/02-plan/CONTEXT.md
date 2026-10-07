---
name: plan
inputs:
  - stages/01-intake/output/
  - references/plan-rules.md
  - skills/azr/SKILL.md
outputs:
  - stages/02-plan/output/
---

# Stage 02: Plan

## Inputs
| Layer | Source | Why |
|---|---|---|
| L4 | stages/01-intake/output/ | the brief: job verbatim, form, scope |
| L3 | references/plan-rules.md | decomposition discipline |
| L3 | skills/azr/SKILL.md | the propose-before-solving loop |

## Process
1. Decompose the job into units per plan-rules.md. Every unit gets: goal,
   acceptance criteria, files/paths, definition of done, verification command.
2. **Propose before solving.** For each unit, write 1–5 test triplets
   (deduction / abduction / induction) at the edge of what you can prove.
   Do not solve anything yet.
3. Check the proposals: run each triplet's known parts. If a stated
   input/output can't be reproduced, the proposal is wrong — fix it before
   it poisons the run.
4. Write output/plan.md (the units) and output/triplets.md (the triplets,
   each with its acceptance rule and how to run it).

## Outputs
- output/plan.md
- output/triplets.md

## Completion
Review gate: the captain checks that the units cover the job and the
triplets would actually catch a wrong solution.
