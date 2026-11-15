---
name: research-meeting-preparation
description: >
  Prepare decision meetings, retrospectives, and status syncs with the installed
  Treffen CLI. Use when the user wants participant pre-work, evidence-linked
  disagreements and themes, an agenda and pre-read, or to decide whether a
  meeting can move async. Also supports synthetic pre-work rehearsal and
  close-out of an existing Treffen meeting; ordinary transcript summarization
  and formal voting use their own workflows.
tags: [study-type, qualitative, analysis, data-collection, external-tool]
---

# Meeting preparation with Treffen

Treffen owns one meeting's consultation, instruments, collection artifacts,
response store, finding reviews, design, and close-out. It is a standalone CLI,
not an `ep` subcommand. Use its local workflow instead of rebuilding the state
machine. The installed `fielding` extra supports native EDSL artifacts and
Humanize integration. Local preparation does not call models.

## Establish the meeting outcome

Reuse the organizer's supplied context. Establish the required outcome and
accountable owner, meeting type (`decision`, `retro`, `status`), time and duration,
facts versus hypotheses, constraints, participants, privacy policy, and what
would make synchronous discussion unnecessary. A title alone is insufficient.
Choose short survey versus adaptive interview assignments by the input needed;
assignment is independent of expected attendance. Do not infer actual attendance
from `expected`, `not_expected`, or `unknown`.

Treffen organizes discussion; use `skill:research-voting` for formal ballot
aggregation, or `skill:research-decision-support` for weighted option scoring.
Use `skill:research-qualitative-data-analysis` for standalone transcript analysis.
Written pre-work may be inappropriate for a sensitive negotiation or a session
whose purpose is open exploration; preserve that purpose rather than forcing a
convergence exercise.

## Follow the installed workflow

Use `skill:workflow-file-layout` and `skill:workflow-plan-template` for study
artifacts. Orient and inspect the intended meeting directory:

```bash
treffen guide
treffen -C <meeting-dir> agent next
```

Read the JSON envelope's `status`, `data.phase`, `data.action`, `warnings`, and
`errors`. Actions contain a `kind`, prompts, and sometimes shell command strings
in `commands`; they are not argv arrays. Run commands in the meeting directory
or add `-C <meeting-dir>`; `-C` does not change the shell's working directory for
subsequent `ep` commands. Rerun `agent next` after material actions. Use command
`--help` to confirm syntax: the README/SPEC also describe future interfaces.

Read [collection.md](references/collection.md) to create meeting/instrument
bundles, build artifacts, deploy or ingest Humanize responses. Read
[evidence-and-design.md](references/evidence-and-design.md) when responses arrive,
for finding review, agenda/pre-read preparation, revisions, and close-out.
For requested synthetic pre-work, read [rehearsal.md](references/rehearsal.md).

Prepare concrete artifacts before requesting a missing approval. Record plan,
finding, design, and close-out approval only when the organizer has approved the
applicable contents; honor existing authorization for the same revision.
Permission to prepare a meeting does not authorize deployment, invitations,
reminders, paid model execution, or distribution. Preview/read-only work can
proceed while those external actions await authorization.

## Apply the published release's limits

This is an early implementation. A successful command or phase `complete` does
not establish that citations resolve, people consented, outputs are anonymized,
or earlier approvals cover revised inputs. The agent must review these facts.
`design build` creates a basic agenda, pre-read, fix-it list, and `hold`/`async`
recommendation; it does not allocate minutes or implement every advertised
meeting recommendation. Add a clearly identified agent-authored time budget and
rationale when needed, retaining the package's original artifacts.

Keep `.treffen/` state, manifests, raw responses, and review bookkeeping under
CLI control. The close-out Markdown draft is intentionally editable; see the
reference for that supported exception. Use deliberate audience-specific exports,
never the whole project directory. A preparation-only request can finish with
reviewable meeting materials; do not fabricate post-meeting notes to reach
`complete`.
