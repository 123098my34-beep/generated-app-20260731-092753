---
name: validate
inputs:
  - stages/03-execute/output/
  - stages/02-plan/output/triplets.md
  - skills/nomistake/SKILL.md
outputs:
  - stages/04-validate/output/
---

# Stage 04: Validate

## Inputs
| Layer | Source | Why |
|---|---|---|
| L4 | stages/03-execute/output/ | what execute produced |
| L4 | stages/02-plan/output/triplets.md | the acceptance rules |
| L3 | skills/nomistake/SKILL.md | the quality gate |

## Process
1. Run every triplet per references/verify-rules.md. Score each against its
   own acceptance rule; tag VERIFIED or UNVERIFIED.
2. For structural jobs, run the walk test: cold orientation from the root
   file alone.
3. Apply the nomistake gate: every claim scored, no unverified claims, buffer
   honest, edit surface works.
4. Write output/validate-report.md: one line per triplet (tag + command +
   result), the walk-test result, and the final verdict.

## Outputs
- output/validate-report.md

## Completion
Report to the captain: what passed, what is UNVERIFIED and why. A job with
UNVERIFIED triplets is not done — fix the root cause and re-run.
