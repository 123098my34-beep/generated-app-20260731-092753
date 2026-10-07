---
name: execute
inputs:
  - stages/02-plan/output/
  - stages/01-intake/output/
outputs:
  - stages/03-execute/output/
---

# Stage 03: Execute

## Inputs
| Layer | Source | Why |
|---|---|---|
| L4 | stages/02-plan/output/ | the units and their triplets |
| L4 | stages/01-intake/output/ | the brief (constraints live here) |

## Process
1. Solve unit by unit, in dependency order. Moderate-difficulty rule: split
   anything unprovable into smaller pieces until each sits at the edge of
   what you can prove.
2. Run each unit's triplets as you solve it. A unit is done when its
   triplets pass — not when it looks done.
3. Log every attempt to buffer/BUFFER.md: what was tried, what ran, what it
   returned. Keep only execution-verified results; discard the rest, but log
   the discards. The buffer is the only memory of progress.
4. Write the unit's artifacts to output/ (or to the real paths the job
   targets — the brief says where the deliverable lives).

## Outputs
- output/ per-unit artifacts + buffer/BUFFER.md rows

## Completion
Review gate: the captain checks the artifacts against the brief. Edits here
are picked up by 04-validate.
