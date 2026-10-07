# Job forms (L3)

How each form flows through the four stages. Distilled from the ICM paper,
the icm-architect skill's forms, and this repo's practice.

## product (pipeline)
- 01-intake: what artifact, what change, what does "done" look like?
- 02-plan: decompose into units (scaffold / feature / test); triplets per unit.
- 03-execute: build unit by unit; run each unit's tests as you go.
- 04-validate: run the full triplet set; walk test if the product has a UI.
- Ships when: every triplet VERIFIED + human gate passed.

## service (record library)
- One record per client/job under the service's own folder (e.g. a quote,
  a report). The record is the L4 artifact; the service definition is L3.
- 02-plan: what does this client's record need? Triplets = acceptance
  criteria for the deliverable (numbers correct, format right, sent).
- 04-validate: check the record against the client's requirements verbatim.

## automation (pipeline + trigger)
- The deliverable is a trigger definition: what fires, what runs, what it
  writes. Triplets fire the trigger (or a dry-run of it) and assert the
  side effect.
- 04-validate: dry-run the trigger; assert the exact side effect. Never
  validate an automation by reading its code.

## agent (context map)
- The deliverable is a context map: nouns (entities), movements (actions),
  guardrails (what it must never do), and the files it reads/writes.
- Triplets = scenarios: given input X, the agent must produce Y and must
  never do Z. 04-validate runs the scenarios.

## content (pipeline)
- research → draft → produce. Triplets check the draft against the brief
  (voice, length, structure) before production.

## analysis (record library)
- One record per question. Triplets = the claim + its evidence: every claim
  in the record must cite a source that was actually fetched.
