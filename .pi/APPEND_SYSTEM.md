# Expected Parrot research agent instructions for Pi

These are Pi-specific instructions. The shared EP Agent research prompt is
loaded separately by the extension.

For study files, use a `sessions/` directory beneath the current project unless
the user or project has a different established workspace convention.

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
- When `ep present` returns a `PRESENT_FILE` marker, the EP Agent extension
  opens text artifacts in Pi's scrollable file viewer. Wait for the user to
  close the viewer before continuing. Binary files are reported by path because
  Pi's terminal viewer cannot render them.

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
