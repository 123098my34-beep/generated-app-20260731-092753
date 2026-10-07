# Verify rules (L3)

The executor contract for stage 04 (validate). Execution is the only
referee; self-judgment is UNVERIFIED by definition.

## Running triplets
1. For each triplet in 02-plan's triplets.md, run its check (bash / python /
   node — whatever the triplet specifies).
2. Score each triplet against its own acceptance rule — never a global vibe.
3. Tag the result:
   - **VERIFIED** — it ran, and the output matched the acceptance rule.
   - **UNVERIFIED** — it could not be executed (say why), or it ran and
     mismatched.
4. Log every attempt in buffer/BUFFER.md: what was tried, what ran, what it
   returned. The buffer never hides what was discarded.

## Rules
- No claim without a run. "It should work" is UNVERIFIED.
- A triplet that always passes was too easy; propose a harder one next round.
- A triplet that always fails means the unit is mis-specified or the proposal
  was wrong — fix the root cause, don't patch the test.
- Per-triplet scoring; no cross-triplet comparisons.
- If a check can't run in this environment (no network, no tool), say so
  explicitly and tag UNVERIFIED — do not silently skip.

## The walk test (structural jobs)
For jobs that produce structure (a folder, a workspace, a scaffold), the
walk test is the referee: an agent with no memory opens the root file, finds
its way, acts, and reports status from the files alone. If it can't, the
structure is wrong — fix it until it can.
