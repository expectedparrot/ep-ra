---
name: ep-agent-codex-setup
description: Set up Codex to use Expected Parrot research skills and EP-backed research workflows.
---

# EP Agent setup for Codex

EP Agent provides research workflow instructions as skills. This plugin does
not install the Python environment, EDSL, the EP CLI, or an Expected Parrot API
key.

When helping the user get started:

1. Ask what research question or project they want to work on.
2. Load and follow `workflow-session-start` before beginning a research
   workflow. Use `workflow-file-layout` when creating durable study files.
3. Treat the currently selected project directory as the workspace. Never
   assume a fixed path such as `/home/user`.
4. Ask the user directly for missing research choices and wait for their
   response. Before paid inference or consequential publishing, explain the
   choice and expected cost or effect and get explicit approval.
5. For EDSL-backed work, confirm the EP runtime is installed and configured,
   including `EXPECTED_PARROT_API_KEY` or the user's supported EP
   authentication. Do not expose secret values in chat or files.

The plugin only installs skills and this setup workflow. It does not grant
access to an EP account or automatically configure external services such as
Firecrawl.
