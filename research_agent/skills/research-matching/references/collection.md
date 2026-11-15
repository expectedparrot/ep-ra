# Human and delegated preference collection

Use `roth --project <study> agent next --collection human` or `delegated` with
the selected scenario. Follow returned actions and `data.rerun`; do not transfer
stable-matching commands to team/review fielding. Human collection explicitly
supersedes canned preference files when selected.

## Human collection

Roth generates personalized native EDSL artifacts, previews, mappings, and
`handoff.json`. Use `skill:edsl-human-survey` for EP mechanics while preserving
Roth's exact identity fields and package registration. Review previews before
hosting. Register returned survey UUIDs, track status and delivery IDs, and
import the exact downloaded Results through the matching field's CLI.

Hosting and invitation delivery are distinct external actions. Carry forward
existing authorization, and confirm recipients and invitation scope before
sending. Inspect existing deliveries before retrying; never send again merely
because a local registration is missing. Keep contact maps, private preference
instructions, and organizer reports out of public artifacts. Candidate-facing
profiles should not expose private instructions or contact information.

For stable matching, participants rank candidates relative to “Remain unmatched”
and identify options they could not assess. Assessed options below the outside
option are rejected; unassessed options stay unknown. Oversized lists route to
screening, followed by a cross-batch ranking of accepted candidates. Independent
batch orders do not establish a global ranking. If the remaining set is still
too large, choose an explicit shortlist or revised ranking budget.

For teams/reviews, use the mode's `field` actions for assessment batches and
cross-batch ranks (or expertise ratings in review score mode). Preserve the
private contact map, frozen market, and response provenance. Assessment changes
invalidate stale ranks. Export completed preferences to a new file; no-preference
or unknown answers mean zero score, while exclusions remain hard constraints.

Importers check package identity and required answers. Preserve missing responses
and resolve rejected imports through the package; do not manually inject answers
into state. Explicit revised submissions retain history. JSON-only previews
cannot be published without a native build.

Upstream has offline native-artifact tests, but hosted presentation, respondent
binding, and delivery still need a service pilot before real recruitment. Do not
claim that local success verifies the deployed UI. Review a small authorized
cohort pilot before expanding fielding.

## Delegated stable-matching preferences

The organizer controls permission to delegate, confirmation policy, and any
benchmark requirement. Collect natural-language preference instructions before
scoring. Use `skill:workflow-model-selection` for a current model and specify
scope and budget. `score plan` retrieves candidate edges and prepares both
directional evaluations where delegation applies. Lexical retrieval can miss
candidates; preserve shortlist size, omitted-candidate audits, and coverage.

Inspect the generated plan, prompts, Jobs, ModelList/settings, and handoff. Cost
the exact effective Jobs and model settings with `ep jobs cost` before approved
execution through `ep`. A plan's evaluation budget is not a dollar cap. The
package's initial estimate may use defaults; customized output-token settings
must be reflected in the reviewed estimate. Build/inspect a costable Jobs
artifact using `ep --help` if the execution handoff supplies separate overrides.

Import native Results with `score import ... --edsl`, then inspect `score status`.
Preserve partial outputs and use `score retry` only for remaining tasks within
approved spending. Do not manually repair model IDs or scores to pass ingestion.
Equal scores become a reproducible strict order using saved tie-breaking inputs;
scores are comparable within a participant, not across participants.

Optional A-versus-B benchmarking separates calibration from held-out evaluation.
Use calibration to revise instructions, freeze predictions with `benchmark
predict`, and only then collect held-out answers. New predictions after held-out
answers require a new benchmark. Pairwise accuracy concerns sampled pairs in the
retrieved pool; synthetic fixtures provide no evidence of model quality.

Apply complete scores through `score apply`, preserving human rankings,
rejections, and pairwise constraints. Resolve inconsistent comparisons explicitly.
If confirmation is required, it binds to the exact ranking version; revisions
need renewed confirmation. Freeze only after those conditions are satisfied.
Final stability remains conditional on the frozen evaluated candidate graph.

[Delegation guide](https://github.com/expectedparrot/roth/blob/30572f698eced5f0aee96ed862045f54ba79638b/docs/delegation.md)
[Human collection guide](https://github.com/expectedparrot/roth/blob/30572f698eced5f0aee96ed862045f54ba79638b/docs/collection.md)
