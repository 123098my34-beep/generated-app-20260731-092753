# Anti-patterns (L3)

What breaks an ICM workspace. Distilled from the paper (§5.2, Table 1),
the icm-architect skill, and practitioner reports.

1. **The monolithic prompt.** Loading every stage's instructions, all
   reference material, and all prior outputs into one context. Pushes the
   window past 40k tokens where retrieval degrades. Fix: layered loading —
   each stage loads only its Inputs table.
2. **Undifferentiated context.** Mixing stable rules (L3) with per-run
   artifacts (L4) in one folder. The model can't tell what constrains it
   from what it should transform. Fix: references/ vs output/.
3. **Binary or opaque outputs.** An intermediate artifact only a tool can
   read. Fix: plain text — markdown and JSON. Any human with a text editor
   can inspect or modify any artifact.
4. **Skipping the review gate.** The gate is the feature: it's where the
   human course-corrects cheapest. Fix: stop between stages unless the
   captain pre-approved skipping.
5. **Framework lock-in.** Orchestration logic in code, so changing stage
   order or a prompt means a redeploy. Fix: the folder is the orchestration;
   rename a folder, edit a markdown file.
6. **Tests that confirm belief.** Writing triplets after seeing the answer.
   Fix: propose before solving (AZR).
7. **Hiding failures.** A buffer that only logs successes. Fix: log every
   attempt, including what was discarded and why.
8. **Over-automating.** Automating what a human should decide. Fix: keep
   judgment at the gates; automate only the mechanical.
9. **Building for concurrency you don't have.** ICM is sequential and
   local-first by design. Concurrent users need infrastructure ICM was
   designed to avoid — that's a different tool.
10. **Branching inside a stage.** Complex mid-pipeline branching is awkward
    in ICM. Fix: the human decides between stages (run 3a or 3b based on
    stage 2's output).
11. **Automating what doesn't repeat.** Jake's rule of thumb: only automate
    if you would do it 100 times in a row. One-off automation is a tax, not a
    leverage. Fix: keep the human in the loop for anything under the
    threshold.
12. **Automating what the platform will absorb.** "Is the thing you just
    automated going to be a builtin feature in 6 months?" If yes, you built
    something the platform will make obsolete. Fix: automate above the
    platform's roadmap, not on top of today's gap.
13. **Wrong-layer automation.** Building level-3 machinery (automating the
    automation) for a level-2 problem (automated once). Fix: automate the
    layer where the work actually repeats; don't meta-automate one-offs.
14. **Integration machinery for paste-able steps.** When two steps can be
    connected by pasting output into the next input, don't build an
    integration framework to do it. Fix: paste. Frameworks are for steps
    that can't be pasted.
