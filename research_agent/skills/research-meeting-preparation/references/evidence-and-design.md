# Findings, meeting design, and close-out

## Evidence review

Read original Results alongside `collection/<instrument-id>/normalized.jsonl`.
Treffen hashes copied packages and deduplicates the same package/index on ingest,
but different exports of overlapping responses can still double-count people.
Its `response_id` numbering restarts for every package. Keep an organizer-side
citation map from each response label to `source_hash`, `source_index`, instrument,
participant, and question; disambiguate references across packages before use.
Count unique participants separately from answers, and report missing coverage.

The agent authors a JSON list or `{"findings": [...]}`. Every finding needs a
unique `id`, `kind`, `claim`, `evidence`, and relevant `counterevidence`:

| Kind | Meaning and current design behavior |
|---|---|
| `consensus` | Supported agreement; goes in pre-read |
| `factual_crux` | Checkable disagreement; routed to async fix-its |
| `values_crux` | Priorities or risk preferences; routed to discussion |
| `theme` | Recurring idea with verified counts; routed to discussion |
| `exception` | Blocker, surprise, or decision request; routed to discussion |
| `gap` | Missing input/evidence; may have no response citation; routed async |
| `action_candidate` | Proposed action, not an agreed commitment; routed async |

`synthesis build --input <findings.json>` checks for nonempty evidence on non-gap
findings but does **not** resolve citations, recompute counts, or test whether
claims follow from responses. Do those checks before review. Lack of dissent
among respondents does not establish consensus among all invitees. Preserve
counterevidence and distinguish factual uncertainty from different priorities.

List findings with `synthesis list`; record the organizer's reviews with
`synthesis review <finding-id> --approve|--reject`. `design build` requires at
least one approved finding and no pending findings. If all are rejected, explain
the evidence gap; do not add a dummy finding to pass the gate.

## Design and revisions

`design build` writes agenda, pre-read, fix-its, and recommendation files under
`.treffen/design/<version>/`. The current rule recommends `hold` when approved
values cruxes, themes, or exceptions exist, otherwise `async`. It does not itself
optimize duration or produce `shorten`, `split`, or `cancel`. Evaluate that simple
recommendation against the actual meeting outcome. Give a separate, clearly
identified agent-authored time-boxed agenda or alternative recommendation when
needed; explain which unresolved issues actually require live discussion.

Review claims and evidence labels for the intended audience before any export.
`design approve` hashes the current package design; that hash does not approve
an independently edited export. Obtain approval of the actual participant-facing
revision before sending it, and retain its relationship to the source design.

This release checks the **existence** of several approval files, not end-to-end
freshness. Changing participants, instruments, responses, or reviews may leave
`next` pointing at an old approved design. Track the input/plan hashes and exact
reviewed files. After changes, explicitly re-propose/review the plan, rebuild
collection if necessary, rebuild/review affected synthesis and design, and renew
only the approvals invalidated by those changes. Do not delete or edit approval
JSON to force a transition. For a changed instrument after fielding, create a
new project revision and preserve the previous project and collected evidence;
do not mix responses from different questionnaires. Preserve prior outputs when
rerunning builds; synthesis/design directory names have second-level timestamps.

## After the meeting

When close-out is requested, use `closeout add-notes <path>` and `closeout build`.
The builder copies notes into a Markdown skeleton; it does not extract decisions,
owners, deadlines, actual attendance, or reconcile pre-work automatically. The
CLI explicitly allows editing `.treffen/closeout/decision-record.md` to complete
its pending sections. Fill them from actual notes, distinguish proposed actions
from commitments, retain dissent and unresolved questions, and ask only for
missing consequential facts. Actual attendance must come from observation.

Review the completed record with the organizer before `closeout approve`.
Passing its placeholder check alone is not evidence of a complete decision
record. Treat it as organizer-private: raw notes are embedded. Make a reviewed
redacted export for broader audiences rather than sharing the native draft.
