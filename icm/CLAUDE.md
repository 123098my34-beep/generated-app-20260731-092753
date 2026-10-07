# ICM — Universal Task Workspace (L0)

This folder is the operating system for any task in this repo: products,
services, automations, AI agents, content, analysis. One agent, reading the
right files at the right moment, does the work a multi-agent framework would.
The folder structure IS the orchestration.

Built on Interpretable Context Methodology (Van Clief & McDermott,
arXiv:2603.16021), extended with the AZR verification loop: test triplets are
proposed before solving, execution is the only referee, and every claim is
tagged VERIFIED or UNVERIFIED.

**Default:** every request is an ICM job. It enters through `source/job.md`
and stages/01-intake, runs back-to-back (auto-run), and the captain reviews
the final artifact. No opt-in, no exceptions — see CONTEXT.md.

## The five layers
| Layer | File | Question it answers |
|---|---|---|
| L0 | CLAUDE.md (this file) | Where am I? |
| L1 | CONTEXT.md | Where do I go? |
| L2 | stages/NN-*/CONTEXT.md | What do I do? |
| L3 | references/, skills/ | What rules apply? |
| L4 | source/, stages/*/output/, buffer/ | What am I working with? |

## Routing
| Job | Go to |
|---|---|
| any request (build / fix / automate / research / content / question) | stages/01-intake |
| check what a run produced | stages/*/output/ |
| quality gate rules | skills/nomistake/SKILL.md |
| runnable check | `python scripts/selftest.py` |

## What to Load
| Resource | When |
|---|---|
| stages/{current}/CONTEXT.md | always — the current stage contract |
| references/*.md | per the stage's Inputs table |
| skills/azr/SKILL.md | 02-plan and 03-execute — propose triplets, log attempts |
| skills/nomistake/SKILL.md | 04-validate — quality gate |

## What NOT to Load
| Resource | Why |
|---|---|
| other stages' outputs | upstream context only — load what the current stage's Inputs table lists |
| .icm/ | runtime state, not agent context |
| all skills at once | load only what the current stage needs |

## Review gate
Gates auto-run by default: stages 01 → 04 run back-to-back without stopping,
and the captain reviews the final artifact at the end. The captain — and
only the captain — can explicitly approve a different mode for a specific
task (e.g. stop at each gate, or skip a stage); silence is not approval, and
the default re-applies to the next request.
