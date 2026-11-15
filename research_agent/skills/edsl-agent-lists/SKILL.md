---
name: edsl-agent-lists
description: >
  Build, import, validate, and save EDSL AgentLists from lists, tabular files,
  current web directories, or programmatic combinations. Use whenever an
  AgentList itself is created or populated for a survey or simulation.
tags: [edsl, reference, data-collection]
---

# Build an AgentList

Create the smallest reproducible pipeline that produces the requested local
artifact. Do not add a report or publishing step unless the user requested it.

## Choose the workflow

For a one-off or small agent list, use the quick path: create the requested
artifact in the active project (or the location the user specifies), with only
the source and provenance files needed to make it useful. Do not require a study
scaffold, formal plan, Makefile, or workflow gates. Validate the saved `.ep`
artifact by loading it and checking the requested count, names, traits, and
other stated requirements.

Use the managed-study path when the user requests reproducibility, progress
tracking, multiple dependent phases, or an agent list as part of a full study.
Then, after plan approval, load `skill:workflow-file-layout` and use its
`agent-list` template. Supply the expected count, every required trait, and
`--required-source-domain` when the user requires an authoritative domain.
Trust its manifest; do not inspect or replace scaffold-owned files.

For either path, if current web data supplies the members or traits, load
`skill:workflow-web-scraping` before fetching anything. For a known structured
directory, use Firecrawl to discover or confirm the canonical machine-readable
source. Use the authoritative source named or implied by the user. Do not
silently replace an authoritative source with Wikipedia or another secondary
source; stop and disclose the source problem if the required fields cannot be
obtained.
Keep source bytes out of generated code. For managed studies, save the official
XML, JSON, CSV, or HTML response under `data/raw/`; for quick artifacts, keep
the raw response in a clearly named local source file when needed. Use a bounded
download, then write a short normalizer that reads that file. Never paste
records or a complete response into a Python string literal. Record source URL,
retrieval date, raw-source path, and its SHA-256 when sourcing current web data.
Do not probe ambient Python packages or install scraping dependencies.

For managed studies, run
`make -C <absolute-study-root> agent-list qa workflow-verify`. The scaffold
uses `ep agents create --name-field name` to build
`data/cooked/agent_list.ep`, then validates it through
`AgentList.git.load(...)`. Do not call `.save(...)`, invent `.json.gz` output,
or repair a gate to accept a different artifact format/path. Fix the producer
when `agent_list.ep` is absent or invalid.
Present the saved `.ep` artifact and give a concise validation/provenance
summary. Use the scaffold-owned target for managed studies.

## Construction invariants

- `name` is reserved. With Python construction use
  `Agent(name="Alice", traits={"age": 25})`; never put `name` in traits.
- With tabular input use `--name-field name` or
  `AgentList.from_source(..., name_field="name")`.
- All agents must share the same instruction string. Put individuality in
  traits, not per-agent instructions.
- Validate exact count, unique names, required-trait completeness, and every
  domain invariant the user specified (or approved in a managed-study plan).
- Treat raw-source separation as a completion invariant. The scaffold QA
  verifies the raw file and checksum and rejects Python string literals larger
  than 4 KiB, which usually indicate embedded source data, for managed studies.
  For quick artifacts, keep source data separate from code and preserve source
  details when using current web data.
- For constructed combinations or ordered lists, shuffle with a recorded fixed
  seed only when downstream truncation could bias the sample. Preserve source
  order when it has substantive meaning.

## Quick path: direct construction when suitable

For a tiny in-memory list, the persistence boundary is still mandatory:

```python
from edsl import Agent, AgentList

agent_list = AgentList([
    Agent(name="Alice", traits={"age": 25, "occupation": "teacher"}),
    Agent(name="Bob", traits={"age": 35, "occupation": "doctor"}),
])

if __name__ == "__main__":
    agent_list.git.save("agent_list.ep")
```

Load the result with `AgentList.git.load("agent_list.ep")`.

Load `skill:edsl-object-publishing` only after the user explicitly requests a
remote object. Load `skill:workflow-completion-checklist` only when a report or
larger AgentList study deliverable was requested.
