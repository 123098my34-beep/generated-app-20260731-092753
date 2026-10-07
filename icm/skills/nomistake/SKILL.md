---
name: nomistake
description: Quality gate for ICM stage 04 (validate). Use when validating a run before reporting done. Checks that every claim is execution-verified, every triplet is scored, and nothing unverified is presented as fact.
---

# nomistake — the no-mistakes gate

The rule: **no claim without a run.** Before a job is reported done, the
validate stage checks:

1. **Every triplet scored.** Each triplet in 02-plan's triplets.md has a
   VERIFIED or UNVERIFIED tag with the command that was run and its output.
2. **No unverified claims in the report.** Anything tagged UNVERIFIED is
   listed as unverified in the final report — never smoothed over.
3. **The buffer is honest.** buffer/BUFFER.md logs every attempt, including
   failures and what was discarded.
4. **The walk test passed** (structural jobs): a cold agent oriented, acted,
   and reported from the files alone.
5. **The edit surface works:** every stage output is a plain-text file a human
   could open, read, and edit before the next stage runs.

If any check fails, the job is not done. Fix the root cause, re-run the
affected stage, re-validate.
