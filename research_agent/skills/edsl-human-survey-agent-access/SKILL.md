---
name: edsl-human-survey-agent-access
description: >
  Lets AI agents take a deployed EDSL survey through its agent link, and controls
  who produces the answers and what guidance agents get. Use when a survey's
  respondent is an AI agent or assistant outside Expected Parrot, such as the
  user's own agent or agents participants bring, or when the user wants to change
  how agents take a survey or separate agent responses from human ones.
tags: [edsl, data-collection]
---

# Human Survey Agent Access — Letting AI Agents Take a Survey

A human survey deployed with `.humanize()` (see `skill:edsl-human-survey`) can also
accept AI agents. A participant gives their AI agent the survey's **agent link**, and
the agent answers through Expected Parrot's API instead of a browser. Each agent
attempt is recorded as a response alongside browser responses, and marked as an agent
response in the results.

Agent access is **off** until the survey's owner turns it on. Only the owner can read
or change it.

A survey that requires sign-in (`survey.login_required`, see `skill:edsl-human-survey`)
can't be taken through its agent link, even with agent access on. If the researcher
wants both, ask which matters more before changing either setting.

## Confirm before enabling

Turning on agent access changes who can answer the survey, so confirm with the
researcher before calling anything that enables it:

- **Who answers**, which sets the participation mode (below). Autonomous responses are
  produced by the agent alone: they are not human data, and must be kept apart from
  human responses in any analysis.
- **Recruitment.** Autonomous agent attempts can't start from a paid panel link
  (Prolific parameters are refused). Don't suggest agent access as a way to fill a
  paid Prolific study.
- **What guidance agents get**, survey-wide and per question.

Don't take the survey yourself through the agent link to add responses. Only do it if
the researcher explicitly asks you to test the agent flow, and tell them the test
response will appear in their results.

## Participation modes

| Mode | Who answers | Use when |
|------|-------------|----------|
| `human_assisted` (default) | The participant. The agent asks each question and records their answers without answering for them. | Participants want to take the survey through their own AI assistant. Closest to ordinary human data. |
| `authorized_context` | The agent, from context the participant has authorized it to use, asking them when unsure. | Answers come from records or context the participant controls (e.g. their own documents), with them available to confirm. |
| `autonomous` | The agent alone, as described in the survey-wide instructions. | The researcher wants AI-generated responses through the human survey flow. Not human data. |

Recommend `human_assisted` unless the researcher's goal clearly calls for another mode.
When the survey is about the agent itself (its own experience, work, or
preferences), use `autonomous`: the agent is the respondent.
The mode is recorded on each response when its attempt starts, so changing it later
doesn't relabel responses already started.

## Reading and changing the config

```python
from edsl import Coop

coop = Coop()
uuid = "<human-survey-uuid>"

access = coop.get_human_survey_agent_access(uuid)
# {"configured": bool, "enabled": bool, "participation_mode": str,
#  "instructions": str | None, "question_settings": {name: {"instructions": str}}}

coop.patch_human_survey_agent_access(
    uuid,
    {
        "enabled": True,
        "participation_mode": "human_assisted",
        "instructions": (
            "Keep free-text answers to one or two sentences, and use the "
            "comment box to flag any answer that's an estimate."
        ),
        "question_settings": {
            "improvements": {
                "instructions": "Name at least one specific change, not a general comment."
            }
        },
    },
    survey=survey,  # the deployed Survey: checks question names before sending
)
```

`configured` is `False` if agent access has never been set; the other fields are then
their defaults (off, `human_assisted`, no guidance).

The patch is merged into the stored config:

- Fields left out are unchanged. Send only what changes, e.g. `{"enabled": False}` to
  pause agents while keeping the rest.
- `question_settings` merges by question name: naming one question changes only its
  settings.
- `"instructions": None` clears the survey-wide instructions. A question set to `None`
  in `question_settings` (`{"question_settings": {"q": None}}`) has its settings removed.

Always pass `survey=` when the survey is available. Without it, a misspelled question
name is accepted and the guidance never reaches the agent. An invalid patch raises
`AgentAccessValidationError` before anything is sent.

The same from the CLI:

```bash
ep humanize agent-access get <human-survey-uuid>
ep humanize agent-access patch <human-survey-uuid> --enabled --participation_mode human_assisted \
  --instructions "Keep free-text answers to one or two sentences." --survey survey.ep
ep humanize agent-access patch <human-survey-uuid> \
  --question_instructions "improvements=Name at least one specific change." \
  --clear_question old_question_name
ep humanize agent-access patch <human-survey-uuid> --disabled
```

`--config patch.json` takes a partial config as a JSON file; the other options apply on
top of it. `patch` refuses to run with no changes.

If `Coop` has no `patch_human_survey_agent_access`, the installed EDSL predates agent
access. Say so, and don't try to reach the API another way.

## Writing guidance for agents

- **Survey-wide `instructions`** (at most 4,000 characters): how answers should be
  given, e.g. length, what to do when unsure, which comment boxes to use. Keep it
  independent of any one respondent, so it works when many participants take the
  survey (for example through an agent list).
- **Per-question `question_settings`** (`instructions`, at most 2,000 characters
  each): what a good answer to that question looks like.
- **In `autonomous` mode**, the survey-wide instructions are the only description the
  agent has of how to answer. Describe the respondent it should answer as there, if
  the study needs one.
- Guidance is advisory: agents are asked to follow it, and nothing enforces it.

## The agent link

The agent link is the respondent link with `/respond/human-surveys/` replaced by
`/respond/agent/`:

```python
info = coop.get_human_survey(uuid)
agent_link = info["respondent_url"].replace("/respond/human-surveys/", "/respond/agent/")
```

Share it the way the researcher shares the browser link. It serves the agent its
instructions, including when to stop. When handing off, give the researcher the
agent link and say which participation mode is on.

## What agents can't answer

- **Timed questions** (a fixed time limit, in a survey that shows one question per
  page). The agent is told to stop and give the participant the browser link.
- **Voice-only interviews.** In `human_assisted` and `authorized_context` mode, the
  agent hands that page to the participant: it gives them a one-time link to answer
  it in their browser, then carries on. In `autonomous` mode there's no one to hand it
  to, so an agent can't complete the survey.

Text interviews and file uploads are answered by the agent. If the survey has timed
questions or voice-only interviews, tell the researcher before enabling access, so they
know which responses will need the participant or the browser.

**Custom JavaScript** runs only in a browser, so agent responses have no events from
question scripts, except on a page handed off to the participant, which runs its
scripts as usual. If the survey relies on scripts for measures (timing, behaviour,
interactive tasks), tell the researcher those measures will be missing for agent
responses (see `skill:edsl-human-survey-javascript`).

## In the results

Every response carries these fields, in the `agent.` namespace:

| Field | Meaning |
|-------|---------|
| `agent.collection_interface` | `browser`, or `agent_http` for an agent response |
| `agent.participation_mode` | the mode when the attempt started; empty for browser responses |
| `agent.client_name_self_reported` | the agent's client, as the agent reported it; not verified |
| `agent.model_name_self_reported` | the agent's model, as the agent reported it; not verified |
| `agent.handed_off_questions` | questions the participant answered in their browser through a handoff |

Split them before analysis, and report agent and human responses separately:

```python
results = coop.get_human_survey_responses(uuid)
human = results.filter("agent.collection_interface == 'browser'")
agents = results.filter("agent.collection_interface == 'agent_http'")
autonomous = results.filter("agent.participation_mode == 'autonomous'")
```

Never pool autonomous responses with human ones. Treat the self-reported client and
model as labels, not evidence.
