---
name: edsl-object-publishing
description: >
  Saving EDSL objects locally and pushing/publishing them to Expected Parrot.
  Use when pushing any EDSL object, or when the user wants to
  push, publish, share, or upload Surveys, Results, AgentLists, ScenarioLists,
  Prompts, or any other EDSL object to Expected Parrot. MUST be consulted before any
  push, publish, share, or upload an object with a meaningful alias.
tags: [edsl, reference, publishing]
---

# Saving and Publishing to Expected Parrot

How to persist EDSL objects locally and share them via Expected Parrot.
The object itself is defined in another Python file e.g.,
`study_survey.py`, `study_agent_list.py`, or `study_scenario.py`.

Any EDSL object can be pushed: Survey, AgentList, Scenario, Results, Prompt, and others.

> **Terminology rule:** In reports and any user-facing material, always say "Expected Parrot" — never "Coop". "Coop" is internal infrastructure terminology and must not appear in `report.md` or any deliverable.

## Pushing to Expected Parrot

Before every `ep push` call, determine:

1. **Alias** — a meaningful URL slug (see Alias Rules below). **Required for every push.**
2. **Description** — a human-readable sentence or two explaining what the object is, what study it belongs to, and what it contains. Write it for a stranger on Expected Parrot who has no other context.

   **Never use a local filepath as the description.** A path like `/Users/alice/ep-agent/sessions/topic_xyz/study_a/writeup/report.html` is meaningless to anyone else and tells a reader nothing about what the object is.

   Good: `"Agent panel for the data-center opposition study — 12 personas representing local residents, activists, and business owners across two counties."`
   Bad: `"/Users/alice/sessions/topic_data-center-opposition/study_a/edsl_jobs/job_a/study_agent_list.py"`

   If you are pushing a report HTML, write: `"Study report: <topic> — <one-line description of what the report covers>."` If you are pushing a survey, agents, scenarios, or results, follow the same pattern: object type + study topic + what it contains.

3. **Visibility** — one of `"public"`, `"private"`, or `"unlisted"`. **Always ask the user before pushing.** Never assume or default silently.

   What each setting means:
   - `"public"` — anyone can find and view this object. It appears in search results and public listings on Expected Parrot.
   - `"unlisted"` — anyone who has the link can view it, but it does not appear in search results or public listings. Good for sharing with specific people without making the object broadly discoverable.
   - `"private"` — only you can see it by default. You can still share it with specific Expected Parrot users individually. You can change this setting at any time.

   **Never use `"public"` unless the user explicitly says so.** Before every push, ask:

   > "What visibility would you like for these objects? Options: **public** (appears in search results, anyone can find it), **unlisted** (anyone with the link can view it, but it won't appear in search), or **private** (only you can see it — you can still share it with specific users, and you can change this setting at any time). Unlisted is the most common choice for studies."

   If the user has already stated a preference earlier in the session, apply it — but confirm before pushing if anything has changed (e.g. switching from a private pilot to a shareable report).

Then push the saved object directly:

```bash
ep push edsl_jobs/job_a/agent_list.ep \
  --alias "<meaningful-slug>" \
  --description "<meaningful description>" \
  --visibility "<confirmed-by-user>"
```
The command returns JSON containing the URL, alias, and visibility; preserve it
as evidence and show the relevant link to the user.

## Prompts

A `Prompt` has no `.ep` package format. Save it as JSON:

```python
prompt.save("prompts/transcript_summary.json")
```

Then push the `.json` file:

```bash
ep push prompts/transcript_summary.json \
  --alias "<meaningful-slug>" \
  --description "<meaningful description>" \
  --visibility "<confirmed-by-user>"
```

Each push of a JSON file creates a new object, so update a pushed prompt with
`Prompt.patch("<uuid>", value=revised)` instead of pushing again. `ep pull` and
`ep clone` do not support prompts.

## Hand off a survey for editing in the Builder

When the researcher says they want to edit a survey themselves, pushing the
saved `survey.ep` is the handoff to the visual Builder. Do not give them EDSL or
Python editing instructions unless they separately ask for code.

Wanting to edit is **not consent to upload or publish local study content**.
Explain that Builder editing requires a remote Expected Parrot object and ask
whether they want that handoff. Do not run `ep push` until they explicitly
agree. If they decline, stop the Builder workflow and ask whether they want a
local artifact or code-based editing help instead; do not show code unless they
request it.

After explicit remote-publication consent, confirm the required alias,
description, and visibility, then push the package with `ep push` and direct the
researcher to the returned Expected Parrot URL. Tell them to open the survey in
the Builder, edit it, and save it there. Wait for their confirmation that it is
saved, then synchronize the same local package:

```bash
ep pull /absolute/path/to/edsl_jobs/job_a/survey.ep
ep surveys show /absolute/path/to/edsl_jobs/job_a/survey.ep
```

The `.ep` package stores its Expected Parrot linkage, so `ep pull` retrieves
the Builder revision in place. Loading the linked package through
`Survey.git.load(...)` also checks for a newer remote revision, but prefer the
explicit pull after a user editing handoff. Inspect and summarize the saved
changes, then rebuild downstream `jobs.ep` from this refreshed survey. Never
reuse a `jobs.ep` built before the Builder edit: it still contains the old
survey. Do not rerun a survey-construction script before pulling, because it
can replace the researcher's saved revision before it is synchronized.

The researcher does not need to export or upload another survey file after
each edit. Stop and wait for them to say they have saved before pulling.

**Record the URL in the report.** Every URL returned by `ep push` should be added to the Methods section of `writeup/report.md` under a "Study objects on Expected Parrot" paragraph. See `research_agent/skills/report-authoring/references/transparency.md` section 5 for the format.

**When to push:** For a survey, finish the preview-and-iteration cycle and get
the researcher's content confirmation before the normal publication push. The
exception is an explicitly approved Builder handoff, where the remote push is
what makes visual editing possible. Once the survey is finalized and the user
has approved publication and visibility, push all required objects (survey,
agent list, scenario list) before running the job. Generate results through the
Makefile's `ep run ... --output data/results.ep` target, then load and push
`data/results.ep`. Do not write the report until all required URLs are in hand.

```bash
# Visibility must be confirmed with the user before these commands run.
ep push edsl_jobs/job_a/survey.ep --alias upwork-interview-survey --description "..." --visibility "<confirmed>"
ep push edsl_jobs/job_a/agent_list.ep --alias upwork-interview-personas --description "..." --visibility "<confirmed>"
ep push edsl_jobs/job_a/scenario_list.ep --alias upwork-interview-scenarios --description "..." --visibility "<confirmed>"

# Push saved Results only after ep run completed successfully.
ep push data/results.ep --alias upwork-interview-results --description "..." --visibility "<confirmed>"
```

## Alias Rules — ALWAYS provide an alias

**Never call `ep push` without `--alias`.** Without one, Expected Parrot assigns a random three-word slug (e.g. `cream-square-apple`) that is meaningless and impossible to find later.

- Must be a valid URL slug: lowercase, hyphens, no spaces or special characters.
- Generate from a descriptive name. If the user provides one, slugify it. If not, derive one from the study context: combine the study topic, object type, and any distinguishing detail.
- Format: `<topic>-<object-type>` or `<topic>-<object-type>-<detail>`
- Examples:
  - "US Senators 2024" agent list → `us-senators-2024-agents`
  - Upwork user interview personas → `upwork-interview-personas`
  - Price sensitivity survey → `price-sensitivity-survey`
  - Results from a corn chips study → `corn-chips-results`
- If unsure what alias to use, ask the user before pushing.

## Error Handling

If the push fails (e.g., alias already taken), update the alias or description and retry.

## Viewing and Updating Object Metadata

Use metadata commands to inspect or update visibility, alias, and description
without fetching and re-uploading content.

```bash
ep metadata <uuid>
ep update-metadata <uuid> --visibility public
ep update-metadata <uuid> --description "Updated description" --alias new-slug
```

## Sharing Objects with Specific Users

Private objects can be shared with individual Expected Parrot users by username or email. The recipient is notified by email automatically.

```bash
ep share <uuid> --user alice
ep share <uuid> --user alice@example.com
ep shared <uuid>
ep unshare <uuid> --user alice
```

If the email address has no Expected Parrot account, an invitation is sent and access is granted when they sign up (`unregistered_shared_with` in the response).

## Quick Reference

| Task | Method |
|------|--------|
| Save locally | `obj.git.save('filename.ep')` |
| Push to Expected Parrot | `ep push object.ep --visibility ... --description "..." --alias ...` |
| Visibility options | `"public"` (searchable), `"unlisted"` (anyone with link), `"private"` (you only, shareable individually) — always ask user |
| Inspect metadata | `coop.get_metadata(uuid)` |
| Update visibility/alias/description | `coop.patch_metadata(uuid, visibility=..., alias=..., description=...)` |
| Share with a specific user | `coop.share_object(uuid, "username_or_email")` |
| See who has access | `coop.get_object_shared_users(uuid)` |
| Remove access | `coop.unshare_object(uuid, "username_or_email")` |
| Report label | "Study objects on Expected Parrot" (never "Coop") |
