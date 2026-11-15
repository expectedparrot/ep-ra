# Preserve requested models through execution

Record explicit provider and exact-model constraints, including each requested
provider/model pairing, in the plan. A later
"also include this model" retains earlier selections unless the user replaces
them. Do not reinterpret model availability based on model-name branding or
`configured: false`; use the bounded server-backed catalog query described in
the skill. If no supported match is found after the documented recovery, report
the unresolved choice and wait before affected inference.

For a constrained selection, validate the saved ModelList or model-bearing Jobs
before costing. Replace `<skill-base>` with this loaded skill's absolute path:

```bash
python <skill-base>/scripts/check_requested_models.py edsl_jobs/job_a/model_list.ep \
  --service openai --require-pair openai '<catalog-confirmed-model>'
```

Repeat `--service` for allowed services and `--require-pair SERVICE MODEL` for
every model with an explicitly requested provider. Pair requirements match both
fields on the same selected model; a model on another allowed service does not
satisfy the request. For a multi-provider comparison:

```bash
python <skill-base>/scripts/check_requested_models.py edsl_jobs/job_a/model_list.ep \
  --service openai --service anthropic \
  --require-pair openai '<first-catalog-confirmed-model>' \
  --require-pair anthropic '<second-catalog-confirmed-model>'
```

Use `--require-model MODEL` only when the request permits that exact identifier
on any allowed service. It does not express a provider/model pairing. Pair
requirements can also be used without `--service`; they require those pairs
without restricting providers for additional models.

The check rejects an empty model list, off-provider models, missing required
models, or missing required pairs. Additional models within allowed services are not
implicitly rejected: "include X" is different from "only X". For an exact
approved roster, also review the complete `selected_models` output against the
plan. This helper checks saved selection, not current catalog availability.

Use the check as an objective workflow gate when explicit model constraints
apply. Validate the effective model artifact passed to the run: a CLI override
can replace embedded Jobs models, so checking only the embedded list would be
insufficient. Rebuild/recheck on selection changes and invalidate stale gate
evidence and cost approval. This helper is not an execution interceptor.
