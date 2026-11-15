---
name: research-fair-division
description: >
  Allocate rooms and rent, indivisible goods, bivalued chores, project credit,
  or shared fares with the installed Ariel CLI. Use when the user wants fair
  division based on explicit or elicited participant valuations, mathematical
  verification, or separate human/simulated reactions to an allocation.
  Two-sided matching and team/project assignment belong to Roth.
tags: [study-type, quantitative, analysis, data-collection, external-tool]
---

# Fair division with Ariel

Ariel owns the specification, submitted inputs, frozen snapshots, mathematical
allocation, independent checks, fielding records, and organizer reports. Use its
installed CLI; do not reproduce the solver or edit `.ariel/` bookkeeping. Ariel
is a standalone executable, not an `ep` subcommand. Local solving makes no model
calls; EDSL collects optional preferences and reactions.

## Select the division problem

Reuse supplied information. Establish the items or cost to divide, participants,
valuation assumptions, organizer rules, and participation source. Choose the
method by its mathematical inputs, not simply because the user says “fair.”

| Type | Inputs and purpose |
|---|---|
| `rent` | One room per participant, total rent, and each person's room valuations |
| `goods` | Indivisible items with additive nonnegative integer values |
| `chores` | Additive easy/difficult costs with one common difficult-cost value |
| `credit` | Positive relative assessments of other contributors, excluding oneself |
| `fare` | A supplied coalition-cost table for a shared trip |

Read [methods.md](references/methods.md) for the selected method's limits and
checks before promising an outcome. Do not silently relax an unsupported budget,
exclusion, group preference, or size constraint.

Use `skill:research-matching` for two-sided partner matching, teams plus projects,
or reviewer assignment. Dividing rent among people who already share a home is
different from pairing roommates. Use `skill:research-voting` for a collective
winner/ranking, or `skill:research-decision-support` for weighted option scoring.

## Follow the package workflow

Use `skill:workflow-file-layout` and `skill:workflow-plan-template` when creating
a research study. Orient once, then inspect the new or existing project:

```bash
ariel guide --type <selected-type>
ariel -C <study> next
```

Read `status`, `data.phase`, `data.action`, `data.missing_decisions`,
`data.command`, external commands, and `next_steps`. Guidance works before
initialization. Resolve missing values using conversation and evidence, follow
the applicable command within existing authorization, then call `next` again.
Use `ariel capabilities` or command `--help` for unresolved interfaces. Returned
commands are shell command strings; do not assume Roth's `argv`/`data.rerun`
contract. Preserve quoting and use explicit paths for artifacts.

Initialize with the reviewed specification. Import complete supplied human
valuations only for an all-human study, with `--source human`; invented examples
use `--source fixture`. `ariel example` creates input files without importing
preferences; `ariel demo` completes an authored offline example. Neither supplies
missing real valuations.

For EDSL collection, read [participation.md](references/participation.md). Keep
human, LLM, and fixture sources separate. Preserve original Results, identities,
question signatures, and field manifests; complete-round ingestion is required.

Freeze the current inputs, solve, verify, and generate the organizer report
through the package. New preferences invalidate derived snapshots/allocations;
retain previous records and use new output directories. Infeasibility calls for
an explicit rule or input revision, not a silent relaxation.

## Report allocation and participant reactions separately

Explain assignments, payments or shares, individual outcomes, assumptions,
verification scope, solver claims, and any rounding effects. Mathematical
fairness does not establish subjective acceptance or truthful elicitation.
Retain the native HTML report and downloadable numerical evidence. For a broader
research narrative, use `skill:report-authoring` without recomputing Ariel's metrics.

Post-allocation reactions are optional. `next` can recommend them after a valid
allocation report; do not extend an allocation-only request to collect reactions
merely to reach phase `complete`. A requested valuation revision in a reaction
is not a new submitted valuation. Review it, then collect a complete new preference
round only if that next step is authorized.

Organizer reports include all submitted valuations in their evidence downloads.
Review audience and contents before sharing; generating a report does not
publish an allocation or notify participants. For controlled model-response
experiments, read [benchmarks.md](references/benchmarks.md).
