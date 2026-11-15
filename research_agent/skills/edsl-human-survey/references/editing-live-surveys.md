## Editing a survey after `.humanize()`

A humanized survey is live as soon as `.humanize()` returns. When the
researcher asks to change it, decide first whether the change can be patched
onto the existing survey or needs a new deployment. Patching keeps the same
UUID, links, and collected responses. Redeploying creates a separate survey
with new links, and responses stay split between the two.

### Patch in place

These settings live outside the survey structure and can change on the live
survey. Respondents keep the same links.

| Change | Call |
|---|---|
| Optional flags, formats, preselection, time limits, attention checks, submitting indicators, intro screens | `Coop().patch_human_survey_humanize_schema(uuid, {"questions": {...}})` |
| `QuestionInterview` settings: interviewer name, checklist, end policy, end message, language, voice (how the AI sounds) | `Coop().patch_human_survey_humanize_schema(uuid, {"questions": {"q": {"text_interview_config": {...}}}})`, or `voice_interview_config` for voice (including `voice_option`) |
| `QuestionInterview` mode (text, voice, or both) | `Coop().patch_human_survey_humanize_schema(uuid, {"questions": {"q": {"interview_mode": "voice"}}})` |
| Progress display, logo | `Coop().patch_human_survey_humanize_schema(uuid, {"survey": {...}})` |
| Custom CSS | `Coop().patch_human_survey_css(uuid, css)` — see `skill:edsl-human-survey-css` |
| Question JavaScript | see `skill:edsl-human-survey-javascript` |
| Agent-list delivery map, anonymity, resubmission | `Coop().patch_human_survey_agent_list(uuid, delivery_map=..., anonymous=..., allow_resubmit=...)` |
| Whether AI agents may take the survey | see `skill:edsl-human-survey-agent-access` |
| Emails, reminders, follow-ups | see `skill:edsl-human-survey-notifications` |

Schema patches are deep-merged, and lists replace the existing value (see
"Updating the schema on a live survey" in `references/humanize-schema.md`).
Read the current schema with `Coop().get_human_survey_humanize_schema(uuid)`
before patching a list such as checklist items, and send the full new list.

### Redeploy with `.humanize()`

Anything stored in the survey, scenario list, or agent list needs a new
deployment:

- question text, options, question type, or `question_name`
- adding, removing, or reordering questions
- skip logic and piping
- a `QuestionInterview`'s `interview_guide`
- scenarios or `scenario_list_method`
- respondents in the agent list, or their traits

If a single request mixes both kinds of change, put everything in the new
deployment, since the new survey starts from its own `humanize_schema`.

### Pulling a deployed survey

Pull a deployed survey to reuse or inspect it, and before every change, so
the work starts from what is deployed and not from a local file that may have
drifted. A human survey links to separate Coop objects:

```python
from edsl import Coop, Survey, ScenarioList, AgentList

coop = Coop()
info = coop.get_human_survey(uuid)
survey = Survey.pull(info["survey_uuid"])
scenarios = (
    ScenarioList.pull(info["scenario_list_uuid"])
    if info["scenario_list_uuid"]
    else None
)

agent_config = coop.get_human_survey_agent_list(uuid)["agent_list_config"]
agents = AgentList.pull(agent_config["uuid"]) if agent_config else None

humanize_schema = coop.get_human_survey_humanize_schema(uuid)
agent_access = coop.get_human_survey_agent_access(uuid)
```

`info["agent_list_uuid"]` is always `None`; take the agent list's UUID from
`get_human_survey_agent_list()`. That call also returns the `delivery_map`,
`anonymous`, and `allow_resubmit` settings.

No call returns the `scenario_list_method`. Find it in the study's notes or
deployment code, or ask the researcher; don't guess, because it controls how
respondents are assigned scenarios.

To redeploy, make the requested changes to these objects and deploy them with
everything the old survey had, so an edit to one question doesn't reset the
rest. Reuse the human survey's name with a version suffix so the two surveys
are easy to tell apart:

```python
new_info = survey.by(scenarios).by(agents).humanize(
    human_survey_name=f"{info['name']} v2",
    scenario_list_method=scenario_list_method,
    humanize_schema=humanize_schema,
    delivery_map=agent_config["delivery_map"],
)
new_uuid = new_info["uuid"]

coop.patch_human_survey_agent_list(
    new_uuid,
    anonymous=agent_config["anonymous"],
    allow_resubmit=agent_config["allow_resubmit"],
)
if agent_access["configured"]:
    coop.patch_human_survey_agent_access(
        new_uuid,
        {
            key: agent_access[key]
            for key in ("enabled", "participation_mode", "instructions", "question_settings")
        },
        survey=survey,
    )
```

Leave out `.by(scenarios)` and `scenario_list_method` when the survey has no
scenarios, and `.by(agents)`, `delivery_map`, and the agent-list patch when it
has no agent list. If the edit renamed or removed a question, update its
entries in `humanize_schema` and `question_settings` to match.

### Preview before applying

Render every change runway can show before applying it, whether it is a patch
or a redeploy: question text, options, order, CSS, formats, progress, logo.
Apply the change to the pulled survey or schema locally, save the survey,
schema, and scenarios, and render them with runway
(`skill:edsl-human-survey-preview`). Wait for the researcher to confirm the
preview before patching or calling `.humanize()`.

Runway cannot show validation, skip logic, JavaScript, or interviews. Check
those through the live `preview_url` after applying the change.

### Confirm before applying

Never patch or redeploy without the researcher's confirmation, even when no
responses exist. Check the response count with `ep humanize status <uuid>`,
and alongside the preview tell the researcher what the change affects:

- **Patch**: any responses already submitted were collected under the old
  settings, and the stored schema keeps no history. Once the patch is
  applied, record the patch time and what changed in the study's notes so the
  analysis can split responses at that point.
- **Redeploy**: the new survey gets new links, and the old survey stays live
  at its old ones. If responses already exist, data is split across two
  surveys, and the researcher decides whether the versions can be pooled.
  Wording and option changes usually mean they are not comparable.

### After a redeploy

Test the new deployment through its `preview_url`, as with any deployment.

The old survey's links, email schedules, callbacks, and Prolific study keep
pointing at the old survey. Tell the researcher which of these exist for this
survey, and act only on what they ask for:

| Channel | New survey | Old survey |
|---|---|---|
| Personalized links | `Coop().get_human_survey_respondent_links(new_uuid, ...)` | — |
| Email schedules and callbacks | set up again (`skill:edsl-human-survey-notifications`) | deactivate |
| Prolific | create a new study (`skill:edsl-prolific-study`) | `Coop().pause_prolific_study(old_uuid, study_id)` or `Coop().stop_prolific_study(old_uuid, study_id)`, with `study_id` from `Coop().list_prolific_studies(old_uuid)` |
