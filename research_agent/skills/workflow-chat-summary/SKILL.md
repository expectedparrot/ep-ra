---
name: workflow-chat-summary
description: >
  Write a compact Markdown handoff only when the user explicitly requests a
  session summary or durable continuation brief. Use when the user asks for a
  handoff summary; do not use automatically at study completion.
tags: [workflow]
---

# Compact handoff summary

Use this skill only for an explicit handoff request. Normal studies already
retain their plan, workflow evidence, Results, report, transcript, and README;
do not create another summary by default.

Write one short `chat_summary.md` at the study root containing:

- the objective and completed outcome;
- authoritative artifact paths;
- important decisions and exact model;
- actual cost when available;
- unresolved blockers or the next useful action.

Prefer facts already recorded in workflow state and deliverables. Do not repeat
the report, narrate routine tool use, or create `session_notes.md`.

Never render `chat_summary.md` to HTML. The Markdown file is internal handoff
state, not another user deliverable. Present it only when the user requested
the summary itself.
