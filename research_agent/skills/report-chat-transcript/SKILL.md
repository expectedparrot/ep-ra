---
name: report-chat-transcript
description: >
  Renders Concordia social simulation transcripts as chat-bubble HTML
  suitable for embedding in pandoc markdown reports. Replaces matplotlib
  dialogue charts with readable, styled conversation views. Use when
  you need to display simulation agent dialogue as a visual chat log
  in a study report.
tags: [report, visualization, simulation]
---

## When to use

After running a Concordia social simulation, the action log contains agent
dialogue turns. Rather than rendering these as matplotlib bar charts (which
truncate text), use this skill to produce chat-bubble HTML that can be
embedded directly in a pandoc markdown report.

## Workflow

1. **Extract turns** from the Concordia simulation JSON log:

   ```python
   from render_chat_transcript import extract_turns_from_log
   turns = extract_turns_from_log("path/to/sim_log.json")
   ```

2. **Render HTML**:

   ```python
   from render_chat_transcript import render_transcript_html
   render_transcript_html(turns, "writeup/chat_transcript.html")
   ```

3. **Embed in report** by placing a `<!-- CHAT_TRANSCRIPT -->` marker in
   `report.md`, then running:

   ```bash
   python scripts/embed_chat_in_report.py writeup/chat_transcript.html writeup/report.md
   ```

   This replaces the marker with raw HTML for the HTML build. For PDF,
   keep a markdown blockquote version alongside.

## CLI usage

```bash
# Render directly from a simulation log
python scripts/render_chat_transcript.py path/to/sim_log.json

# Output goes to sim_log_chat.html in the same directory
```

## Design notes

- All CSS is inline so the HTML works when embedded in pandoc output.
- Speaker 1 (left, blue) and Speaker 2 (right, coral) are configurable.
- Phase dividers appear between conversation phases.
- Font is system sans-serif to contrast with the report body (DejaVu Serif).
