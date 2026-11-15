# Consultation and collection

## Local inputs

The published [README and examples](https://github.com/expectedparrot/treffen/tree/8d6b7ae2bcc37999cc643b1732c5955599e5744a)
are useful starting points. Copy only relevant structure, replacing all example
people, dates, and purported evidence. Schema files are in upstream `docs/schemas/`;
`treffen schema validate` is not implemented at this pin. Use `init --dry-run`
and `apply --dry-run`, then inspect the built artifacts, since validation does
not enforce every nested field described by the schemas.

A meeting bundle uses `schema_version: treffen.meeting-bundle/1.0`, `project`
with `title` and `meeting_type`, `outcome` with `text` and `decision_owner`,
`participants`, and `context`. Participants have stable `id`, `display_name`,
`role`, and `attendance_expectation`; the decision owner must be a participant
in the bundle. Context entries have `id`, `kind` (`fact`, `hypothesis`,
`constraint`, `history`), and `text`. Record assumptions as hypotheses.

```bash
treffen init <meeting-dir> --input <meeting.json> --dry-run
treffen init <meeting-dir> --input <meeting.json>
treffen -C <meeting-dir> plan propose
```

Review the actual plan and consultation before `plan approve`. An instrument
bundle uses `schema_version: treffen.instrument-bundle/1.0` and an `instruments`
list. Each instrument has `id`, participant IDs, `privacy_policy`, and `questions`.
Questions need `id`, `type`, and `text`, plus type-specific fields. Prefer simple
underscore identifiers; ensure they remain unique after EDSL name normalization.
Apply the instruments before final plan review where practical so the reviewed
state includes the actual questions and assignments.

```bash
treffen -C <meeting-dir> apply --input <instruments.json> --dry-run
treffen -C <meeting-dir> apply --input <instruments.json>
treffen -C <meeting-dir> plan propose
# After review and approval of this plan and the current instruments:
treffen -C <meeting-dir> plan approve --revision <reviewed-revision>
treffen -C <meeting-dir> collection build
```

Use `skill:edsl-surveys` for typed question and survey-logic design, and
`skill:methods-ai-interview` for bounded adaptive interviews. Treffen's builder
supports groups and skip rules, plus piping in question text; do not assume it
implements every EDSL stop/jump/checklist field mentioned in the product design.
Inspect the native Survey to verify requested behavior survived construction.

## Humanize boundary

`collection build` writes each instrument's Survey, AgentList, model-free Jobs,
Humanize schema, and manifest with input hash, plan revision, expected response
count, and Git commits. Inspect those artifacts and their participant assignments.
Use `skill:edsl-human-survey` for hosted compatibility and deployment guidance.
Run `ep humanize preview --survey <actual-survey-path>` before deployment.

`treffen -C <meeting-dir> collection deploy <instrument-id> --approve` creates a
Humanize survey from the built **Jobs** and schema. Do not replace the Jobs with
an unbound Survey: the Jobs carry the assigned participant agents. `--approve`
records an authorization already given; it is not a way to obtain it. If creation
succeeds but local registration fails, recover the existing UUID with
`collection register <instrument-id> --human-survey <uuid>` rather than creating
a duplicate. Inspect `collection remote-status <instrument-id>` as needed.

`collection respondents <instrument-id> --output <private-file.json>` retrieves
personal links. Treat them as bearer credentials and send each participant only
their own link when sending is authorized. Email and reminders are separate
Humanize operations; see `skill:edsl-human-survey-notifications`. Treffen has no
implemented email/reminder command at this pin.

Retrieve with `collection fetch <instrument-id>`, or import separately retrieved
native Results using `collection ingest <instrument-id> --results <results.ep>`.
Keep originals and manifests. Before ingest, verify the intended instrument's
questions, assigned `participant_id` traits, provenance, and completion status;
the normalizer itself does not enforce this binding. Missing identities or
answers are gaps to resolve, not values to invent. Human responses carried in
EDSL Results are distinct from model-generated answers.

## Privacy policies

| Policy | Intended audience rule |
|---|---|
| `attributed` | Identity may appear in approved shared outputs |
| `anonymous-shared` | Organizer can see identity; shared artifacts must remove identifying detail |
| `organizer-private` | Individual answers and attributable paraphrases stay with organizer |

The policy string does not anonymize generic design exports. Review finding
claims and evidence labels before they enter participant materials; names,
roles, distinctive quotations, and small groups can identify people. Do not
promise anonymity from the organizer. Keep raw Results, rosters, personal URLs,
and unredacted notes out of shared exports.
