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

## Required workflow

1. After plan approval, load `skill:workflow-file-layout` and use its
   `agent-list` template. Supply the expected count, every required trait, and
   `--required-source-domain` when the user requires an authoritative domain.
   Trust its manifest; do not inspect or replace scaffold-owned files.
2. If current web data supplies the members or traits, load
   `skill:workflow-web-scraping` before fetching anything. For a known
   structured directory, use Firecrawl to discover or confirm the canonical
   machine-readable source. Use the
   authoritative source named or implied by the user. Do not silently replace
   an authoritative source with Wikipedia or another secondary source; stop
   and disclose the source problem if the required fields cannot be obtained.
3. Keep source bytes out of generated code. Save the official XML, JSON, CSV,
   or HTML response under `data/raw/` with a bounded download, then write a
   short normalizer that reads that file and produces the scaffold-owned
   `agents.csv`. Never paste records or a complete response into a Python
   string literal. Record source URL, retrieval date, raw-source path, and its
   SHA-256 in `provenance.json`. Do not probe ambient Python packages or install
   scraping dependencies.
4. Run `make -C <absolute-study-root> agent-list qa workflow-verify`. The
   scaffold uses `ep agents create --name-field name` to build
   `data/cooked/agent_list.ep`, then validates it through
   `AgentList.git.load(...)`. Do not call `.save(...)`, invent `.json.gz`
   output, or repair a gate to accept a different artifact format/path. Fix the
   producer when `agent_list.ep` is absent or invalid.
5. Present `data/cooked/agent_list.ep` with the scaffold-owned target and give
   a concise validation/provenance summary.

## Construction invariants

- `name` is reserved. With Python construction use
  `Agent(name="Alice", traits={"age": 25})`; never put `name` in traits.
- With tabular input use `--name-field name` or
  `AgentList.from_source(..., name_field="name")`.
- All agents must share the same instruction string. Put individuality in
  traits, not per-agent instructions.
- Validate exact count, unique names, required-trait completeness, and every
  domain invariant approved in the plan.
- Treat raw-source separation as a completion invariant. The scaffold QA
  verifies the raw file and checksum and rejects Python string literals larger
  than 4 KiB, which usually indicate embedded source data.
- For constructed combinations or ordered lists, shuffle with a recorded fixed
  seed only when downstream truncation could bias the sample. Preserve source
  order when it has substantive meaning.

## Direct construction when no scaffold is needed

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
