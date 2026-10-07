# Plan rules (L3)

Decomposition discipline for stage 02 (plan).

1. **Intent verbatim.** The job brief's wording is the source of truth. Never
   paraphrase constraints away; carry them into every unit they touch.
2. **Independent units.** Split the job into units that can run without each
   other. Independent units may run in parallel; only true dependencies
   serialize.
3. **Self-sufficient briefs.** Every unit names: goal, acceptance criteria,
   files/paths, definition of done, and how it will be verified.
4. **No under-specified briefs.** The most common failure is a brief that
   makes a worker guess. If a unit can't be fully specified, it isn't ready
   to plan.
5. **Volume never lowers the bar.** Every unit still gets full criteria; every
   result still gets verified in stage 04.
6. **Serialize only for true dependencies.** Same-file overlap is a signal to
   isolate, not a blocker.
7. **Refine the factory once.** L3 reference material must be setup-quality:
   "refine the starting data so that in the future, you never have to refine
   it again." If a product needs rework, the reference material was wrong —
   fix the reference, not the product.

## AZR rule: propose before solving
Before any unit is solved, write its test triplets (see skills/azr/SKILL.md):
- 1–5 triplets per unit, at the edge of what you can prove.
- Types: deduction (input → expected output), abduction (output → an input
  that yields it), induction (examples → the rule).
- If a triplet's known parts can't be reproduced when checked, the proposal
  is wrong — fix the proposal before it poisons the run.
- Tests written after you see the answer only confirm what you already
  believe. Tests written first can fail. That failure is the signal.
