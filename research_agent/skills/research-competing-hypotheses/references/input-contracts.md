# Langley input contracts

Use these shapes with the repository-pinned Langley version. Replace values;
do not send partial or deliberately invalid inputs to infer schemas.

## Matrix row

After `matrix next`, write one complete row and submit it with
`matrix set --evidence <evidence-id> --input <path>`:

```json
{"assessments":[
  {"hypothesis_id":"h001","rating":"consistent","strength":2,"rationale":"..."},
  {"hypothesis_id":"h002","rating":"neutral","rationale":"..."}
]}
```

Allowed ratings are `consistent`, `inconsistent`, `neutral`, and
`not_applicable`. Strength is required only for the first two.

## Conclusion

```json
{
  "summary":"...",
  "confidence":"low",
  "hypotheses":[
    {"hypothesis_id":"h001","assessment":"...","rationale":"..."}
  ],
  "critical_evidence_ids":["e001"],
  "critical_assumptions":["..."],
  "residual_uncertainty":"..."
}
```

Include exactly one assessment for every active hypothesis. `assessment` is an
analyst-authored string, not an enum. `confidence` must be exactly `low`,
`moderate`, `high`, or `unknown`; never use `medium`.

## Sensitivity

Submit with `sensitivity run --name <name> --input <path>`:

```json
{"reason":"...","changes":[{"evidence_id":"e001","new_credibility":"low"}]}
```

The change may instead use `hypothesis_id`, `new_rating`, and `strength` when
testing a matrix judgment. Use `sensitivity suggest` first and test every entry
in `data.candidates`, not only a diagnostic subset.

## Indicator

```json
{
  "description":"...",
  "observable_in":"...",
  "threshold":"...",
  "source":"...",
  "owner":"...",
  "supports":["h001"],
  "weakens":["h002"]
}
```

Submit with `indicator add --input <path>`.
