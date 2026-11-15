# Premortem CLI quick reference

Use JSON output as the agent contract. Run `premortem <command> --help` only
when a surfaced `next_action` requires an option not shown here.

| Command | Purpose |
|---|---|
| `premortem agent-start` | Return method, current phase, approvals, and next actions |
| `premortem init` | Initialize `.premortem/` project state |
| `premortem status` | Summarize current project state |
| `premortem workflow` | Return current phase and next actions |
| `premortem workflow next` | Show the next workflow action |
| `premortem workflow validate` | Detect dangling references, duplicates, self-loops, and cycles |
| `premortem persona ...` | Manage stakeholder personas |
| `premortem reason ...` | Manage failure reasons |
| `premortem graph ...` | Manage causal nodes and edges |
| `premortem score ...` | Score causal nodes |
| `premortem mitigate ...` | Manage mitigations |
| `premortem job generate <phase>` | Build a portable model-free EDSL Jobs package |
| `premortem ingest <phase> --from <results.ep>` | Ingest explicit EDSL Results |
| `premortem report context` | Export canonical evidence and writing brief |
| `premortem report html` | Generate an optional convenience view for inspection; never the final agent-authored report |
| `premortem docs` | Read built-in method guidance |

Generated inference always remains explicit:

```bash
premortem job generate reasons --output jobs/reasons.jobs.ep
ep jobs cost jobs/reasons.jobs.ep
ep run jobs/reasons.jobs.ep --model <confirmed-model> --output jobs/reasons-results.ep
premortem ingest reasons --from jobs/reasons-results.ep
premortem workflow
```

Do not use legacy `premortem analyze ...` commands. Do not install or upgrade
Premortem from inside a study; the ep-agent lock owns its revision.
