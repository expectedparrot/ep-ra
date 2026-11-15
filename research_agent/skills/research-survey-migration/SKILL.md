---
name: research-survey-migration
description: >
  Migrates existing Qualtrics and SurveyMonkey surveys into auditable EDSL
  Survey artifacts with the installed Zugunruhe CLI. Use when a user wants to
  capture, convert, reconstruct, restyle, preview, or move an existing hosted
  Qualtrics or SurveyMonkey questionnaire into Expected Parrot or Humanize.
tags: [study-type, external-tool, data-collection, edsl]
---

# Survey migration with Zugunruhe

Use Zugunruhe as the state, traversal, reconstruction, styling, provenance, and
migration-audit owner. Do not recreate its browser capture, branch traversal,
Survey conversion, style extraction, or audit reporting in skill scripts or ad
hoc Python.

## Fit and boundaries

Use this skill for an existing Qualtrics or SurveyMonkey survey that needs to
become an EDSL Survey. Route ordinary survey creation or revision to
`skill:research-survey`; route analysis of exported response rows to the
appropriate analysis skill. A migrated Survey may subsequently undergo survey
testing, but migration and instrument testing are separate stages.

Zugunruhe reconstructs the source and produces migration evidence. It does not
prove that inferred routing is correct, validate the instrument scientifically,
or own the research agent's final branded report.

## Start from the package-owned workflow

After `skill:workflow-session-start`, load `skill:workflow-file-layout` and keep
the migration under the approved study root. Verify the locked tool once:

```bash
zugunruhe --version
zugunruhe doctor
zugunruhe agent guide
zugunruhe agent next -C <migration-root>
```

Treat the versioned JSON envelope as authoritative. Follow the recommended
structured action returned by `agent next`; do not guess command shapes, inspect
package internals, or replace the workflow with top-level legacy
`zugunruhe guide`/`zugunruhe next` calls. Run `agent next` again after each
successful mutation. Use `agent status` when resuming and `agent history` when
auditing how the state was produced.

Execute returned actions from their declared `cwd` using their exact `argv`.
Check mutation, side-effect, and approval metadata before execution. Stop when
the package returns an explicit terminal state.

## Plan before live traversal

Establish:

- the exact source platform and URL;
- whether the URL is a disposable/test link or a production survey;
- authentication requirements and how credentials will remain out of logs;
- expected pages, branches, languages, quotas, randomization, and termination
  behavior, if known;
- the desired output: EDSL structure only, visual styling, local preview, or an
  eventual Humanize publication;
- the review owner and completion criteria.

Opening and navigating a hosted survey is an external side effect: some
platforms save partial responses during navigation, and a generic Next action
may submit a final page. Present this risk and obtain explicit approval before
the first live traversal. Prefer a test survey or disposable response link.

Do not put passwords, tokens, cookies, or authenticated state into prompts,
commands, checked-in fixtures, screenshots, manifests, or transcripts. Use only
the authentication mechanism documented by `zugunruhe agent docs`.

## Capture and reconstruct

Let `agent next` drive capture, bounded diagnostics, reconstruction, styling,
and audit generation. Preserve the package's durable source manifest,
screenshots, captured HTML, route evidence, generated EDSL artifacts, style
artifacts, and migration report.

For a real migration, require exhaustive traversal. Diagnostic page or branch
caps may be used for a smoke test, but any cap, failed path, or
`traversal_complete: false` means the capture is incomplete. Never describe it
as a completed migration or silently omit unreachable material.

Do not hand-edit generated survey or style artifacts merely to make a validation
check pass. Record the discrepancy through the package-owned issue/review
mechanism, fix the source mapping or an explicit reviewed override, and retain
the change in migration history.

## Review the migration

Browser reconstruction is evidence-producing, not authoritative. Before calling
the migration ready, compare source evidence against the generated Survey for:

- exact wording, instructions, options, validation, and requiredness;
- display and skip logic, loops, piping, and termination behavior;
- embedded data, quotas, scoring, and randomization;
- page grouping, question identity, and language variants;
- typography, colors, spacing, controls, buttons, and responsive behavior;
- unsupported or inferred behavior and every failed traversal path.

Use the package's audit report and structured review status. Require explicit
adjudication of inferred routing and material discrepancies. Preserve unresolved
limitations in the handoff rather than translating uncertainty into certainty.

## Preview and publication boundary

Preview locally before any publication. Verify the exact generated Survey and
Humanize schema/style artifacts identified by Zugunruhe. Publication creates an
externally visible object and requires explicit user authorization for the exact
artifact, name, and visibility. Do not treat a successful preview as permission
to publish.

After publication, retain returned identifiers and URLs in migration state and
verify the hosted result against the reviewed local preview. Do not collect
human responses unless the user separately authorizes fielding.

## Handoff and reporting

The completed handoff must identify:

- source platform and source-survey identity without exposing credentials;
- Zugunruhe version and migration-state root;
- canonical generated EDSL Survey artifact;
- traversal completeness and failed/capped paths;
- source and generated artifact hashes where available;
- reviewed discrepancies, overrides, inferred rules, and unresolved risks;
- local preview and publication status;
- recommended downstream survey-testing step.

Treat Zugunruhe's HTML as a migration audit artifact. If the user requests a
stakeholder report, load `skill:report-authoring`; the research agent owns the
final branded narrative and links its claims to the package-owned evidence.

## Golden rules

- Let `zugunruhe agent next` own sequencing.
- Obtain approval before live traversal and again before publication.
- Never call capped or failed-path traversal complete.
- Preserve raw capture and generated artifacts as provenance.
- Review inferred logic against source evidence before handoff.
- Keep migration distinct from instrument validation and human fielding.
