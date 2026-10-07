---
name: intake
inputs:
  - source/job.md
  - references/forms.md
outputs:
  - stages/01-intake/output/
---

# Stage 01: Intake

## Inputs
| Layer | Source | Why |
|---|---|---|
| L4 | source/job.md | the job, verbatim |
| L3 | references/forms.md | the job-form table |

## Process
1. Read the job verbatim. Do not paraphrase away constraints.
2. Classify the form: product | service | automation | agent | content | analysis.
   If the job matches none, say so and pick the closest — flag the mismatch.
3. Decide scope: inline (default) or too-big-for-inline (needs its own
   persistent workspace). Only flag too-big if the job has its own long-lived
   stage structure; most jobs are inline.
4. Write output/job-brief.md: the job verbatim, the form, the scope decision
   with reasons, and the constraints that must survive every later stage.

## Outputs
- output/job-brief.md

## Completion
Review gate: the captain checks the brief. A misclassified form is cheapest
to fix here — it poisons every downstream stage.
