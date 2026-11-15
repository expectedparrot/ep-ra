# EDSL participation and reactions

Ariel builds a personalized Survey, AgentList, Jobs, preview, Humanize schema,
and manifest for each participant. The manifest records instrument definitions,
identities, hashes, conversion scales, model metadata, and expected answers.
`field build` is local construction, not execution. Use new output directories.

## Simulated preferences

Choose the model/provider with `skill:workflow-model-selection`; review each
persona and context that will be transmitted. Build the round with the selected
model and inspect `ariel -C <study> next`. Inspect and cost the exact generated
Jobs before executing the returned `ep run` commands within the authorized
model, repetitions, and spending scope. Use the same effective settings in
costing and execution. An estimate is not an enforced billing cap.

For rent, the instrument elicits 10,000 room-value points, which Ariel converts
using the recorded total rent. Do not manually rescale Results before ingestion.
Other types use their own formats from `guide --type TYPE`.

Use the returned field ID and exact Results paths with `field ingest`. All
planned participant packages are required. Missing, duplicate, wrong-identity,
or altered-instrument responses reject registration. Preserve failures and
original artifacts; do not bypass ingestion by inserting answers into `.ariel/`.
A retry must fit the user's existing authorization or receive revised approval.
Use `skill:post-run-review` for native Results quality checks before interpretation.

Ariel marks authored test-model responses as fixtures; they are not evidence
from an LLM or from people. A completed simulation measures the specified personas
and model under those inputs, not a representative population's valuations.

## Human or mixed rounds

Set each participant's kind to `human` or `simulated`. The field builder provides
model-run commands only for simulated participants. For humans, use the provided
Humanize handoff and `skill:edsl-human-survey`: inspect a preview, host within the
approved scope, and send invitations only when authorized. A mixed round uses
the same valuation scale and solver for everyone.

Preserve `ariel_participant_id`, `ariel_field_id`, and `ariel_kind` traits.
Save the JSON stdout of each `ep humanize responses` download as a receipt;
pass the corresponding receipt(s) using `field ingest --human-receipts`.
Inspect help for the complete argument form. Retain one receipt per human Results
package, alongside the original `.ep` files.

EDSL reconstructs Humanize responses with a test-model transport. Ariel needs
the separate receipt to distinguish human collection from an authored fixture;
it checks native Results commit, response count, respondent/response UUIDs, and
instrument binding. This consistency check is not independent authentication
of a human identity. Do not relabel fixtures to get them through ingestion.

The documented simulated pilot did not exercise live Humanize hosting. Verify
hosted rendering and respondent binding with an authorized small pilot before
scaling real fielding. Keep participant evidence and organizer exports private
according to the study's agreed audience.

## Reactions and revisions

Build `field build --stage reactions` only for the current allocation and an
agreed follow-up. Each participant sees the public outcome, their own inputs,
and their own recorded history. Do not add other participants' private answers.
Preserve prior answers and comments verbatim, including mistakes and source labels.

Rent reactions test payment-direction/net-benefit comprehension and collect
fairness, acceptance, explanation, and reflection. Other applications have
their own reaction instruments. Use manifest counts and versions rather than
assuming a universal question count. Incorrect comprehension remains visible;
do not filter or correct answers before collecting a fairness judgment.

Numerical verification and subjective reactions are separate outcomes. A request
to revise valuations does not change the frozen allocation. Review the request
and, if proceeding, collect a complete new preference round. New preferences
invalidate old derived allocations and prevent stale reaction rounds from being
attached to a new one. Preserve earlier rounds and use a new study for independent
replications or changed study definitions/personas.

[Published participation workflow](https://github.com/expectedparrot/ariel/blob/449dcaf9c7fff888f1dcb27e10b61551ec01dcf3/README.md#human-and-mixed-participation)
