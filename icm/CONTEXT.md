# ICM — Task Router (L1)

## Default
Every request is an ICM job — no opt-in, no exceptions. When the captain sends
any message, this is what happens, without being asked:

1. Write the request verbatim in `source/job.md`. Do not paraphrase constraints
   away.
2. Walk the stages in order: 01-intake → 02-plan → 03-execute → 04-validate.
   Each stage's CONTEXT.md (L2) is the contract: read it, do only what it
   says to, write only where it says to write.
3. Stages run back-to-back (auto-run): the pipeline does NOT stop between
   stages. The captain reviews the final artifact at the end of the walk.
4. Report what passed, what is VERIFIED or UNVERIFIED, and any limitations.

This is the pipeline's default behavior. The captain can explicitly approve a
different mode for a specific task (e.g. skip a stage); silence is not
approval, and the default re-applies to the next request.

Why default-on: a framework that only runs when asked is a suggestion, not an
operating system. The structure is the orchestration — so route everything
through it.

## Job forms (what kind of task is this?)
| Form | Is this the job? | Shape |
|---|---|---|
| product | Build or fix a software artifact (app, tool, script, site) | pipeline: brief → build → test → ship |
| service | Deliverable for a client or customer (quote, report, deck, cleaning) | record library: one record per client/job |
| automation | Repeatable trigger → action (scheduled, event-driven, webhook) | pipeline + trigger definition |
| agent | An AI agent that acts autonomously (research, monitoring, assistant) | context map: nouns, actions, guardrails |
| content | Writing/media production (article, video script, deck) | pipeline: research → draft → produce |
| analysis | Research, comparison, decision support | record library: one record per question |

Every form flows through the same four stages. The form changes what
03-execute produces and what 04-validate checks — see references/forms.md.

Routing target for every form: **stages/01-intake**.

## Scope
Every job runs inline in this folder's four stages. "Too big" is a flag, not
an escape hatch: if a job needs its own persistent workspace (a product with
its own long-lived stage structure), 01-intake flags it in the job brief and
the captain decides — the request still enters through source/job.md and
stage 01 regardless.

## State
- `buffer/BUFFER.md` — the only memory of progress across runs. One line per
  attempt: what was tried, what ran, what it returned. The buffer is
  outcome-oriented (attempts + results), not a knowledge brain — memory
  exists to get outcomes, not to look like a brain.
- `.icm/` — runtime state. Never load into context.
