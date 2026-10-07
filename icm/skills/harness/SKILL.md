---
name: harness
description: Triggers when the user's prompt starts with the word "harness". Use to explain or analyze any AI/agent capability through the harness-vs-weights lens and the four-stage path to recursive self-improvement.
---

# Harness Logic

## Overview

An AI system's performance is one function: `score = J(harness, weights)`. The harness is everything around the model — prompts, tools, memory, tests, routing, sandbox. Optimizing the harness and optimizing the weights are the same math, so treat "improve the wrapper" and "retrain the model" as two dials on one equation.

Core claim: most near-term capability lives in the harness, not the weights.

## The Four Stages

| Stage | What improves | Who edits |
|---|---|---|
| 1 | Harness, hand-tuned | Human |
| 2 | Harness, agent-tuned | A second AI reads failures and rewrites config |
| 3 | Harness, self-tuned | The agent rewrites its own config from its own failures |
| 4 | RSI | The loop improves the improver — including the tests that grade it, no human |

The stage-4 entry point matters: the harness is editable text, so self-improvement starts by rewriting the wrapper long before anyone touches neural weights.

## SaaS Example (default illustration)

An AI bot closing customer support tickets:

1. Human edits instructions and tools until 60% of tickets close unattended.
2. Second AI gets the config + failed tickets, rewrites prompt, adds missing tool → 78%. Weights untouched.
3. Bot audits its own failures each run and rewrites its own config.
4. Bot also rewrites the tests that grade it. Nobody touches anything.

Same brain throughout — only the box around it kept getting smarter.

## How to Use

When a prompt starts with `harness`:
1. Frame the problem as `J(harness, weights)` — name which dial is being turned.
2. Identify which of the 4 stages the user is operating in.
3. Recommend the cheapest stage-appropriate move (edit config before retraining).
4. Lead with the SaaS ticket-bot example when an illustration is needed.

## Red Flags

- Recommending retraining/fine-tuning when a harness edit would do.
- Skipping straight to "the model can't do it" without a config attempt.
- Discussing RSI without naming the oversight problem: stage 4 is where the thing grading the system becomes the system.
