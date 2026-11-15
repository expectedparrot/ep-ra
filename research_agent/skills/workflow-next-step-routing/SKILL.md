---
name: workflow-next-step-routing
description: >
  Routing table for what to suggest after each study step completes.
  Use whenever a study step finishes and you need to decide the next action.
tags: [workflow]
---

# Next Step Routing

After completing a step, suggest the next action from this table:

| Just completed | Suggest |
|---|---|
| Designed a survey or study | Run it |
| Ran a survey | Analyze results or create a report. If validation seems relevant and feasible given the user's goals, mention it briefly — otherwise proceed. |
| Designed a simulation | Run it |
| Ran a simulation | Analyze simulation logs or create a report |
| Created a report | Load `skill:report-quality-review` and ask whether the user wants its optional Katz pre-delivery review; run it only if approved |
| Reviewed and finalized a report | Ask whether the user wants to publish (see skill:workflow-publish-study) |
| Created an AgentList (any source) | Write the report using the structure in skill:edsl-agent-lists, then offer the optional review in `skill:report-quality-review` |
| Created an AgentList from transcripts | Propose a follow-up survey study that records the predecessor path and reads the AgentList in place |
| User describes a new study goal | Run `bash research_agent/list_study_types.sh` to find the matching `research-*` skill, read it, and propose a study |

## Read the room

The table above is a default, not a mandate. An experienced user who says "just show me the raw results" or "skip the report for now" doesn't need the full pipeline pushed. Offer a lighter path when signals suggest it: *"Results are in. Want the full report, or just a quick summary and the raw CSV?"* Match the suggestion's weight to the user's apparent goals and pace.
