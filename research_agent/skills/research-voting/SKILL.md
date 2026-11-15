---
name: research-voting
description: >
  Designs and analyzes group preference decisions with the installed Voting
  CLI: ranked, approval, score, grade, allocation, single- or multi-winner
  ballots; method comparison; Condorcet analysis; roadmap prioritization; and
  synthetic or Humanize preference collection. Use when people or simulated
  personas choose among options and the aggregation rule is part of the
  research question. Do not use for administering public elections.
tags: [study-type, external-tool, quantitative, data-collection, edsl]
---

# Preference aggregation with Voting

Use Voting as the project, option, voter, election, ballot, count, comparison,
plot, and provenance owner. Do not recreate ballot validation, counting methods,
EDSL job generation, Humanize collection, or method-comparison logic in ad hoc
Python.

## Route the request

Use this skill when a group must express preferences over known options and the
goal is a transparent collective ranking, winner, or allocation. Common cases
include roadmap priorities, hiring panels, participatory budgets, employee or
customer rankings, committee decisions, and research on voting rules.

Route instead to:

- `skill:research-matching` for participant matching, team/project assignment,
  or reviewer allocation with capacities and conflicts;
- `skill:research-decision-support` for criterion-weighted evaluation without a
  respondent electorate;
- `skill:research-conjoint` for estimating attribute-level tradeoffs or
  willingness to pay;
- `skill:research-survey` for ordinary measurement without collective-choice
  aggregation;
- `skill:research-product-design` when the option space still needs to be
  generated or narrowed.

Voting is research and decision-support software, not election-administration
software. Do not use it to operate governmental elections, certify official
results, establish voter eligibility under law, or make claims about legal
compliance.

## Bootstrap and follow package state

After `skill:workflow-session-start`, use `skill:workflow-file-layout` and keep
the Voting project inside the approved study root. Verify the locked commands
once:

```bash
voting version
ep check
voting agent-bootstrap
```

`agent-bootstrap` is valid before initialization and when resuming. Treat its
versioned JSON envelope, project state, and `next_steps` as authoritative. Run
`voting next` after each material mutation and execute its returned action
instead of guessing syntax or inspecting package internals. Use `voting status`
to summarize the inferred phase.

Use `voting docs show <topic>` only when the current decision requires that
topic. In particular, read `ballot-types` before fixing the ballot and
`voting-methods` before choosing a count. Do not load every guide by default.

## Define the decision before collecting ballots

Confirm or infer a draft, then obtain user agreement on:

- the decision, options, electorate, and whether weights or eligibility apply;
- single- versus multi-winner outcome and number of seats;
- the preference information respondents can reasonably provide;
- the ballot type and its loss of information;
- primary counting method, comparison methods, tie policy, and seed if relevant;
- collection source: existing ballots, direct entry, simulated personas, or
  Humanize respondents;
- success criteria, report detail, privacy constraints, and approval boundaries.

Do not choose plurality merely because it is familiar. Match ballot type to the
elicitation burden and decision: ranking captures order, approval captures an
acceptable set, score/grade captures intensity, and allocation captures a
budgeted distribution. A ballot cannot recover preference information it never
collected.

Make weights and eligibility explicit and justify them. Never infer stakeholder
weights from seniority, demographic traits, or conversational dominance. Record
the substantive consequences of the selected rule and tie policy.

## Collect preferences through one explicit path

### Existing or directly supplied ballots

Use Voting's import or ballot commands and preserve respondent identifiers,
weights, source, and collection provenance. Do not silently repair invalid or
partial ballots. Run `voting ballot validate <election-id>` before counting and
surface exclusions or normalization decisions.

### Simulated personas

Register only traits relevant to the decision. Let Voting generate the portable
EDSL Jobs package; Voting never executes inference. Before generating the final
job, load `skill:workflow-model-selection` and choose one current model with one
bounded catalog query.

Inspect and cost the exact generated artifact, obtain approval, then execute it
through `ep`:

```text
voting survey generate <election-id> ...
voting survey show <election-id>
ep jobs cost <exact-jobs.ep>
ep run <exact-jobs.ep> --output <exact-results.ep>
voting ballot import --election <election-id> --from-results <exact-results.ep>
```

Use exact paths returned by Voting rather than the schematic paths above. A
changed option set, voter panel, model, job, or retry requires new inspection,
costing, and approval. Describe results as simulated-persona preferences, not
population estimates or human votes.

### Humanize respondents

Generating a local model-free survey is reversible. Publishing, emailing,
retrieving remote responses, or otherwise contacting people is an external side
effect and requires explicit authorization at that step. Verify the exact
election, options, ballot type, respondent list, invitation text, and visibility
before publishing or sending invitations. Never treat publication as completed
fielding or invent missing responses.

Keep emails and private ballots out of prompts and reports unless explicitly
authorized. Report small-cell and re-identification risks when preferences are
sensitive.

## Count and compare deliberately

Validate ballots before every interpretation. Run the prespecified primary
method, then use `count compare` for compatible alternatives when robustness to
the aggregation rule matters. Saved count results are immutable evidence; do not
overwrite an inconvenient result or manually recompute it elsewhere.

Interpret agreement across methods as rule robustness for these ballots—not
proof of broad social consensus. Treat disagreement as a substantive finding:
identify which properties of the rules and preference distribution change the
outcome. Inspect pairwise, rank-distribution, score, and method-comparison plots
only when compatible with the ballot and decision.

Report ties, exhausted or invalid ballots, incomplete rankings, weights,
eligibility, turnout/coverage, seat completion, Condorcet cycles, and
method-specific warnings. Do not select whichever method produces the preferred
winner after seeing results without labeling that choice as post hoc.

## Deliver

Preserve `.voting/` as the source of truth. The handoff must identify the exact
option set, electorate, election configuration, ballot provenance, validation
result, count IDs, methods, winners/rankings, method disagreements, plots, and
limitations.

Voting's saved results and plots are analytic evidence. For a stakeholder
deliverable, load `skill:report-authoring`; the research agent owns
`writeup/report.md` and branded HTML. Explain why the ballot and methods fit the
decision, distinguish simulated from human preferences, and describe what would
change the result.

## Golden rules

- Follow `agent-bootstrap`, then `voting next`; do not duplicate the state
  machine in the skill.
- Make ballot information loss and counting-rule assumptions explicit.
- Keep weights and eligibility deliberate and auditable.
- Validate before counting and preserve every saved result.
- Obtain approval before inference, publication, invitations, or remote response
  retrieval.
- Never present synthetic ballots as human votes or Voting as public-election
  administration.
