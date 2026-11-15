---
name: workflow-file-layout
description: >
  Creates reproducible study directories and standard runtime/report assets.
  Use when allocating a neutral new study scaffold before writing plan.md,
  adding an approved method-specific template, or deciding where artifacts
  belong.
tags: [workflow, file-organization]
---

# Create a study layout

Create the neutral scaffold with both commands before writing `plan.md`:

```bash
ep study start --root . --topic "<topic>"
ep study scaffold <absolute-study-root-from-start>
```

`study start` allocates an empty directory; reuse it if orientation already
allocated it. Run its `data.next_action` scaffold command once, using the
absolute `study_root`. With `--no-create`, review prior context and allocate
only when a fresh study is chosen. The template-free
scaffold installs the portable Makefile, directories, `analysis/plot_style.py`,
and branded `writeup/report.css`, but no substantive source stubs. After plan
approval, apply any method template idempotently to this same directory.
The neutral scaffold's `next_action` requests the plan and approval; apply the
method template once afterward.

For every EDSL survey, apply the survey template after plan approval once its
model and validation invariants are known:

```bash
ep study scaffold \
  sessions/topic_<alias>/study_<letter> --template survey \
  --expected-rows 10 \
  --required-answer favorite_color \
  --required-answer color_reason \
  --model "<confirmed-model>" \
  --run-description "Favorite color survey - 10 personas"
```

When one structured survey repeats across items, stimuli, or vignettes, add
`--with-scenarios`. The scaffold then creates
`edsl_jobs/job_a/study_scenario_list.py`, builds `scenario_list.ep`, and wires
`--scenarios` into the owned Jobs target. Do not inspect `ep jobs build --help`
or replace this with multiple parallel survey questions.

For a standalone AgentList, use its deterministic CSV-to-package template:

```bash
ep study scaffold \
  sessions/topic_<alias>/study_<letter> --template agent-list \
  --expected-agents 100 \
  --required-trait state --required-trait party \
  --group-trait state --expected-group-size 2 \
  --required-source-domain senate.gov
```

For AgentLists, write the manifest's normalized CSV, provenance JSON, and
separate raw-source artifact. Include `raw_source_path` and `source_sha256`;
never embed source responses in normalizer code or change the owned `.ep`
artifact path.

Validation is frozen; follow [amendment rules](references/full-layout.md),
never weaken failed QA.

The command returns a bounded JSON manifest. If `required_skill` is present,
load that skill before touching `next_edits`. Read each listed source once,
edit only its marked study-data section, and use the owned targets directly.
Do not inspect the Makefile, gate spec, or directory after a successful
scaffold.

First edit every manifest `next_edits` file. Then execute the returned
`phase_commands` exactly: `after_source_edits` once with real approval
evidence, `after_spend_approval` once after cost approval,
`after_inference` once, and `after_report` once. Do not reconstruct their
individual Make or `ep workflow` steps.

Preserve sources' construction/save architecture. Use absolute Make calls:
`make -C "$(pwd)/sessions/.../study_a" edsl-objects`.
The manifest's `prepare APPROVAL_EVIDENCE="..."` initializes gates, builds
objects, and estimates cost; `post-run` processes inference; `complete` finishes
the report. Use
`retry-data RETRY_REASON="..."` only for an approved retry. Never `cd` into a
study, author survey gate JSON, or attest an objective gate.

Use `README.md` as the reproducibility log. Put EDSL construction in
`edsl_jobs/`, analysis code in `analysis/`, saved results in `data/`, and the
single report source at `writeup/report.md`.

Read [full-layout.md](references/full-layout.md) only for simulation layouts,
predecessor provenance, manual report assets, complex Makefile wiring, or
portable-copy requirements.
