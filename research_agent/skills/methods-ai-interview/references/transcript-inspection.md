# Inspect saved interview transcripts

Reuse the traversal in the study's existing runner/export helper first. Native
`Results` interview answers are already lists; do not use `ast.literal_eval`,
`eval`, or JSON decoding on them. Decoding belongs only at an explicitly
serialized export boundary.

| Meaning | Per-Result access | Flattened selection column |
|---|---|---|
| Agent name | `result.agent.name` | `agent.agent_name` |
| Agent trait | `result.agent.traits["career_stage"]` | `agent.career_stage` |
| Interview | `result.answer[question_name]` | `answer.<question_name>` |

`agent.name` is not the flattened selection column. Filter by stable agent
names, not discovered row indices. Inspect `results.columns` at most once if
you actually need flattened selection; do not guess successive `select()` calls.

The native answer schema is:

```python
[
    {"role": "interviewer", "content": [{"type": "text", "text": "What changed?"}]},
    {"role": "respondent", "content": [{"type": "text", "text": "My schedule."}]},
]
```

Preserve turn order and concatenate text blocks in order; content may contain
multiple blocks, non-text blocks, or no text. Do not assume `content[0]` is text.

For a named subset, run the installed helper directly (replace `<skill-base>`
with the absolute directory of the loaded `methods-ai-interview` skill):

```bash
python <skill-base>/scripts/export_interviews.py data/results.ep \
  --question si_legacy_story --agent senior_macro --agent midcareer_pubfin \
  --agent-trait career_stage --agent-trait subfield --format jsonl
```

The helper accepts files supported by `Results.load`, including `.ep` and
legacy JSON/gzip Results. JSONL gives one record per result with agent name,
requested traits, question, model/service, iteration, and ordered turns.
Use `--format markdown --output writeup/appendix.md` for a readable appendix.
Missing requested agents, absent questions, and non-native answers fail clearly
instead of returning a misleading empty or partially decoded export. Empty or
non-text turns remain present with empty text.

Use this helper for report excerpts/appendices instead of regenerating inline
Python. Inspection uses saved Results and does not authorize new inference.
