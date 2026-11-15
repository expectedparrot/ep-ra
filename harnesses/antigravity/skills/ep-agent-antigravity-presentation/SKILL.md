---
name: ep-agent-antigravity-presentation
description: >
  Present completed local research files to users in Google Antigravity. Use
  when a research workflow asks to present an artifact with ep present.
---

# Presenting files in Google Antigravity

Antigravity does not consume EDSL's `PRESENT_FILE` marker as an artifact-pane
command. When a workflow asks to present a local file:

1. Run `ep present <absolute-file-path>` as a standalone command to validate the
   artifact and retain the presentation marker in the tool output.
2. Tell the user the artifact's name and project-relative path so they can open
   it in Antigravity's file view. Do not say the marker opened the file.
3. Keep the handoff short and explain what the artifact contains.

Keep artifacts inside the active project so Antigravity can access them under
its workspace file-access settings.
