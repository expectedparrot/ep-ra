---
name: edsl-quirks
description: >
  Routes concrete EDSL compatibility failures and known API edge cases. Use
  when an EDSL command or script fails, or when implementing an advanced
  feature known to be fragile; do not load for routine survey construction.
tags: [edsl, reference]
---

# Diagnose an EDSL compatibility issue

Start from the exact error or fragile feature. Search the detailed reference
for the relevant term instead of reading it end to end:

```bash
rg -n "<error-fragment|feature-name>" \
  research_agent/skills/edsl-quirks/references/full-reference.md
```

Useful search terms include `ScenarioList.append`, `Jinja2`, `service_name`,
`empty collections`, `images`, `Results`, `repeated sampling`, `working
directory`, and `PDF`.

Prefer a stable `ep` command for routine inspection and execution. Apply the
smallest fix supported by the installed CLI help or the matching reference
section. Do not load unrelated quirks or replace a supported CLI operation
with ad hoc Python.
