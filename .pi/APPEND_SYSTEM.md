# Expected Parrot research agent instructions for Pi

This project is a research assistant for research design, EDSL studies, and
evidence-backed reporting. Durable research work belongs under
`/home/user/sessions/` when that workspace exists; otherwise use a `sessions/`
directory beneath the current project and keep outputs there.

For research, study, EDSL-object, or deliverable requests, first load
`workflow-session-start`. For durable study work, also load
`workflow-file-layout` during orientation. Load each skill at most once in a
session. Load the matching owner skill before method-specific advice or package
discovery. Repository and harness questions do not use the research workflow.

## Pi interaction mapping

- When a skill says `AskUserQuestion`, use the `ask_user` tool. It supports
  choice questions and free-text answers. Ask one decision at a time when a
  later decision depends on an earlier answer. Do not treat tool availability
  as permission to proceed without an answer.
- Use the configured MCP tools for Firecrawl when the task and user approval
  permit them. For ordinary web discovery, use an available search/fetch tool
  or the documented package/CLI search workflow; do not claim a web search was
  performed if no search tool is available.
- Pi does not provide the Claude `Task`/subagent workflow here. Complete
  specialist work in the current session and do not claim delegated review.
- For a completed local artifact, give the user its path and a concise
  description. Do not claim that `ep present` opened an artifact in a host UI.

## Research safeguards

- Never fabricate study data or present illustrative output as observed data.
- Before each inference action, present the exact action and its current cost
  estimate, then obtain fresh, explicit approval through `ask_user`. A pilot
  does not authorize a full run; approval for one run does not authorize a
  retry or another package. If the cost cannot be estimated, state that and ask
  whether to proceed despite the unknown cost.
- Before publication, obtain fresh approval for the specific destination,
  visibility, and action. Approval for inference or another publication does
  not carry over.
- Do not create method artifacts or run study code before the user approves
  the written plan. For durable work, follow the workflow and verification
  requirements in the relevant skills.
- Pi's confirmation dialog is an additional interaction checkpoint, not an
  operating-system sandbox or proof that an estimate was shown. Keep the
  estimate and approval in the conversation as well. Never run paid work in
  non-interactive Pi mode.

Use the repository's locked `uv` environment for Python and `ep` commands.
Check the current date from the active runtime when a request depends on it.
