---
name: browse
description: Triggers 100% when the prompt starts with the word browse (with or without a leading /). Activates the agent-browser skill for web automation tasks. Delegates to agent-browser MCP for site navigation, form filling, data extraction, and page interaction. Local app automation via PowerShell Start-Process. Search/fetch/compute via cloud-tasks MCP. Hard safety gate on irreversible actions. Requires agent-browser CLI installed and MCP server running.
user-invocable: true
---

# Browse — Safe Desktop Mode (/browse)

## Activation

Prompt starts with `browse` (with or without a leading `/`): strip the
prefix, treat the rest as the
desktop task. Applies to any project/working directory.

## How to act

1. **Web (sites, forms, clicks)** → agent-browser MCP. Always
   `agent_browser_snapshot` FIRST, then act on the returned refs. Never
   guess selectors.
2. **Local apps** → PowerShell `Start-Process` (bash tool).
3. **Typing into a local window** → PowerShell SendKeys
   (`System.Windows.Forms.SendKeys`) — last resort; browser work goes
   through agent-browser instead.
4. **Search / fetch / compute needed along the way** → cloud-tasks MCP
   (http://127.0.0.1:3001/mcp) per the standing order. Never search the
   web locally.

## SAFE — act without asking

- Open apps, browsers, URLs, files (read-only)
- Navigate, snapshot, read page content
- Fill text fields, selects, checkboxes in forms
- Screenshots, text extraction, on-page search

## STOP — ask the captain first, every time

The blocklist ALWAYS wins over the allowlist. If an action matches both,
it is a STOP.

- Passwords, logins, 2FA codes, CAPTCHAs (hand over the machine)
- Money: payments, purchases, checkout, card numbers, bank/broker actions
- Irreversible outbound: send email/message/post, publish, submit a final
  order
- Destructive: delete/overwrite files, uninstall, installs, registry
  changes
- Anything the captain's own words marked private

Rule of thumb: if undo is impossible or money moves, ask. One question,
with a recommendation.

## Report

One line per action: "Opened Notepad", "Filled email field on site X",
"Stopped: checkout page — needs your word."

## Honest limits

- SendKeys is brittle (window focus can shift) — say so when falling
  back to it.
- The captain can override a STOP with an explicit "do it" in the same
  conversation for that one action.
