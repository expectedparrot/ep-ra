---
name: edsl-human-survey
description: >
  Designs human-survey behavior and deploys EDSL surveys to real respondents
  via the web. Use for capability questions about background thinking steps,
  piping, grouped pages, informational steps, and interview blocks during design, or for survey deployment,
  styling, per-respondent personalization, recruitment, editing a deployed
  survey, and response retrieval.
tags: [edsl, data-collection, qualitative]
---

# Human Survey Deployment — Sending EDSL Surveys to Real Humans
**Communication note:** For browser participation, always hand off these three URLs as clickable Markdown links: `[Preview survey](<preview_url>)`, `[Participant link](<respondent_url>)`, and `[Survey dashboard](<admin_url>)`, replacing placeholders with actual URLs. For external AI-agent participation, replace the participant link with `[Agent participation link](<agent_link>)` using the documented derivation in skill:edsl-human-survey-agent-access; keep the browser preview and survey dashboard links. If both participation routes are intended, provide both with distinct labels. Do not use bare URLs or code formatting. Recover missing links from existing deployment metadata; never guess or redeploy to obtain them. Retrieve responses yourself when requested; do not hand the user retrieval instructions. Show code only when explicitly requested. For interviews, follow the required deployment handoff in skill:research-interview-design.

The `.humanize()` method converts an EDSL survey into a web-hosted survey on Expected Parrot (Coop) that real people fill out in a browser. Results come back as standard EDSL `Results` objects.

For a concise account of how question types compose, read the
[composition reference](../edsl-surveys/references/composition-contracts.md).
The deployment approvals below apply to creating a live survey, not to reading
capability guidance during design.

## Confirm before deployment

Present the draft with a runway preview (`skill:edsl-human-survey-preview`)
and iterate until the researcher confirms
the survey content. Then confirm how they want to reach human respondents—for
example, a single shared link, one personalized link per known respondent,
Expected Parrot email delivery, Prolific recruitment, or an agent link for AI
agents. Resolve the required respondent list, personalization, visibility,
account-login requirement, and delivery settings, and wait for the researcher's answer before calling
`.humanize()`.

If the respondent is an AI agent, confirm agent access and the participation
mode with `skill:edsl-human-survey-agent-access` before deploying, and share the
agent link, not `respondent_url`.

After deployment, use the returned `preview_url` to test the actual live flow
before sharing any `respondent_url` with participants.

## Pulling or changing a deployed survey

Calling `.humanize()` creates a live survey and respondent links. Before
pulling a deployed survey or making any change to it, read
[editing live surveys](references/editing-live-surveys.md). Its "Pulling a
deployed survey" section shows how to fetch the survey, scenarios, agents, and
humanize schema behind a human survey UUID, for reuse, inspection, or editing.

Some changes can be patched onto the live survey; changes to questions,
wording, options, scenarios, agents, or flow need a new deployment with new
links. The reference covers which is which, how to preview a change, and what
to confirm with the researcher before applying it.

## Basic usage

### Math in survey text

Whenever survey text includes mathematical notation, wrap the expression in
double dollar signs, for example `$$x^2$$`. Use this in ordinary LLM surveys
too, since a survey may later be deployed through Humanize, where this notation
renders as math for respondents.

```python
from edsl import Survey, QuestionFreeText, QuestionMultipleChoice

q1 = QuestionMultipleChoice(
    question_name="preference",
    question_text="Which do you prefer?",
    question_options=["Option A", "Option B", "Option C"],
)
q2 = QuestionFreeText(
    question_name="why",
    question_text="Why did you choose that?",
)

survey = Survey([q1, q2])

info = survey.humanize(
    human_survey_name="Preference Study",
    survey_visibility="unlisted",
)

print(info["respondent_url"])  # share this link with respondents
print(info["admin_url"])       # monitor responses here
```

### `.humanize()` parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `human_survey_name` | str | `"New survey"` | Researcher-facing name on your Coop content page (NOT shown to participants). Set a clear, specific one so you can find the survey later. |
| `survey_description` | str \| None | None | Researcher-facing description. Technically optional, but set it (e.g. topic + date) so surveys are easy to identify on your content page. |
| `survey_alias` | str \| None | None | URL-friendly alias |
| `survey_visibility` | str | `"private"` | `"private"`, `"public"`, or `"unlisted"` |
| `humanize_schema` | dict \| None | None | Schema for question settings and survey options, including account-login requirements (see below) |
| `agent_list_description` | str \| None | None | Researcher-facing description of an attached `AgentList`. Echo the study name here too, so the agent list is findable alongside the survey (see "With agents"). |
| `delivery_map` | DeliveryMap \| None | None | Maps delivery channels to agent trait columns. Only needed if Coop will send the links — see `skill:edsl-human-survey-notifications`. |

### Return value

`survey.humanize()` returns a `Scenario` (dict-like) with these keys:

| Key | Description |
|-----|-------------|
| `uuid` | Human survey UUID — needed to fetch responses later |
| `respondent_url` | Public link for respondents |
| `preview_url` | Live test link; test responses are not added to results |
| `admin_url` | Admin dashboard link |
| `name` | Survey name |
| `n_complete`, `n_in_progress` | Completed and still-in-progress response counts (0 at creation) |
| `survey_uuid` | UUID of the pushed survey object |
| `scenario_list_uuid` | UUID of the pushed scenario list (if any) |

**Save the `uuid`** — you need it to retrieve responses yourself when requested.
## Showing the user the survey — two kinds of preview

There are **two distinct ways** to let the user see a survey before real respondents do, and they serve different purposes. Make sure the user knows both are available — do not assume they know they can walk through a live survey without polluting the data.

**1. Draft / pre-deployment preview — runway.** Render the saved survey to a local HTML file that looks like the live survey, *without creating a live survey*. Scenarios, images, question groups, and custom CSS all render. Use this while iterating on the design; the workflow is in **`skill:edsl-human-survey-preview`**. Agent traits, prior answers, and skip logic do not render — check those with option 2.

**2. Live-survey test link — take the real survey without adding to the results.** When a survey is deployed via `.humanize()`, the returned dict already includes a **`preview_url`** — the respondent URL with `save_response=false` appended. Opening it walks through the *actual live survey* — piping, scenarios, images, skip logic, and all — but the run **does not appear in the survey's results** or count as a response. Don't tell the user a preview records nothing: its custom JavaScript events and its chats with the survey assistant are kept, and returned only when asked for with `include_previews=True`, marked `is_preview` (see `skill:edsl-human-survey-javascript` and `skill:edsl-human-survey-assistant`). Chats with the assistant on a preview are charged.

```python
info = survey.humanize(human_survey_name="...")
print(info["preview_url"])     # take the live survey end-to-end; not added to results
print(info["respondent_url"])  # the real link to share with respondents
```

`Coop().get_human_survey(uuid)` returns the same `preview_url` key for an already-deployed survey. Use this to verify piping, personalization, and any flow-control rules behave correctly on the real survey before sharing `respondent_url` with respondents. Offer the user this link whenever the survey has agent traits, piped answers, or skip rules that a runway preview cannot render. If the survey requires sign-in, the preview does too: open it signed in to any Expected Parrot account.

When the survey is deployed with an agent list, each respondent has their own link and so its own preview URL — get them all at once with `get_human_survey_respondent_links(..., include_preview_urls=True)` (see "With agents").

## Memory and piping — humanize does not use survey memory modes

EDSL **survey memory APIs only affect LLM agent runs** (`.by(agents).by(models).run()`). They do **not** work in humanize:

- `set_full_memory_mode()`
- `add_targeted_memory()`
- `add_memory_collection()`
- `set_lagged_memory()`

Calling these on a survey you plan to `.humanize()` has no effect on what human respondents see. Prior answers reach later questions only through **piping** — embed `{{ q_name.answer }}` in `question_text`, `interview_guide`, option labels, thinking-question prompts, etc. Coop resolves those templates when the respondent advances. The same template syntax reaches scenario fields (`{{ scenario.field }}`) and agent traits (`{{ agent.trait_name }}`; see "With agents").

```python
# Follow-up tailored to a screener answer
q_followup = QuestionFreeText(
    question_name="why_churned",
    question_text="You said you left because of {{ screener.answer }}. Tell us more.",
)

# Interview guide informed by earlier answers
q_interview = QuestionInterview(
    question_name="depth",
    question_text="Thanks — we'd like to learn more about your experience.",
    interview_guide=(
        "The respondent's employment status is {{ employment.answer }}. "
        "Explore the factors behind their career choice..."
    ),
)
```

For invisible server-side steps that pipe into visible questions, see "Invisible thinking questions" below. For memory modes in agent simulation, see **skill:edsl-surveys**.

## Pages and informational steps

For multi-question pages, section boundaries, introductions, and completion
notices, read [grouped pages and messages](references/grouped-pages-and-messages.md).

## Humanize schema — styling and question configuration

Read [the humanize schema reference](references/humanize-schema.md) for optional questions, format controls, matrix carousel and preselection, survey progress, logos and the asset library, question time limits, attention checks, exclusive options, Select all controls, submitting indicators, the support matrix, and reading/patching live schemas. For an AI chat assistant beside the form, see `skill:edsl-human-survey-assistant`.

## Custom CSS

For CSS classes, programmatic styling with `SurveyCSS`, and patching a live survey's CSS, see `skill:edsl-human-survey-css`.

## Custom JavaScript

For interactive tasks, timing or behavioural measures, and logging events from a question, see `skill:edsl-human-survey-javascript`. It is available on approved accounts only; check access before planning a study around it.

## With scenarios

When using scenarios, call `.humanize()` on a `Jobs` object (not directly on the survey). You must specify a `scenario_list_method`.

```python
from edsl import Scenario, ScenarioList

scenarios = ScenarioList([
    Scenario({"product": "Widget A", "price": "$10"}),
    Scenario({"product": "Widget B", "price": "$25"}),
])

q = QuestionFreeText(
    question_name="opinion",
    question_text="What do you think of {{ scenario.product }} at {{ scenario.price }}?",
)
survey = Survey([q])

info = survey.by(scenarios).humanize(
    human_survey_name="Product Feedback",
    scenario_list_method="randomize",
)
```

### Scenario list methods

| Method | Behavior |
|--------|----------|
| `"randomize"` | Each respondent gets a random scenario (with replacement) |
| `"ordered"` | Scenarios are assigned sequentially in server-side arrival order over one shared link. Use only for anonymous even distribution — it does **not** bind a specific respondent to a specific scenario, so never use it to deliver personalized/identifying rows (see "Personalizing a survey per respondent"). |
| `"loop"` | Survey is expanded — every question is repeated for every scenario |
| `"single_scenario"` | Exactly one scenario is used for all respondents (list must have length 1) |

**Rules:**
- If you attach scenarios, you **must** specify `scenario_list_method`.
- If you specify a method, you **must** attach scenarios.
- Models are **not supported** with humanize — the survey goes to real humans. Agents *are* supported; see below.

## With agents

Attach an `AgentList` via `.by()` to give each respondent their own link carrying their own trait values. Reference the traits anywhere a template is resolved — `question_text`, option labels, `interview_guide`, thinking-question prompts — with **`{{ agent.<trait_name> }}`**. Coop fills them in from the agent bound to whichever link the respondent opened.

```python
from edsl.questions import QuestionFreeText, QuestionLinearScale
from edsl.surveys import Survey
from edsl.agents import Agent, AgentList

q1 = QuestionLinearScale(
    question_name="satisfaction",
    question_text="{{ agent.first_name }}, how satisfied are you with your {{ agent.plan }} plan?",
    question_options=[1, 2, 3, 4, 5],
    option_labels={1: "Very dissatisfied", 5: "Very satisfied"},
)
q2 = QuestionFreeText(
    question_name="missing_feature",
    question_text="What would make the {{ agent.plan }} plan more useful for your team?",
)

agents = AgentList([
    Agent({"first_name": "Alex", "plan": "Starter"}),
    Agent({"first_name": "Jordan", "plan": "Pro"}),
    Agent({"first_name": "Sam", "plan": "Enterprise"}),
])

survey = Survey([q1, q2])

info = survey.by(agents).humanize(
    human_survey_name="Q3 2026 plan satisfaction check-in",
    survey_description="Q3 2026 plan satisfaction check-in",
    agent_list_description="Q3 2026 plan satisfaction check-in — active subscribers",
)
```

Unlike scenarios, agents take no `scenario_list_method`: one `.humanize()` call mints **one link per agent**, and the agent-to-link binding is fixed at deployment rather than by arrival order. This is the mechanism to reach for whenever the respondent list is known up front and each person should see content specific to them.

### Getting each respondent's link

`get_human_survey_respondent_links` returns the per-respondent links merged with the agent traits, so you can tell which link belongs to whom:

```python
from edsl import Coop

Coop().get_human_survey_respondent_links(
    info["uuid"],
    save_path="subscriber_links.csv",
    include_preview_urls=True,
)
```

Columns: `agent_index`, `respondent_uuid`, `url`, `preview_url` (only with `include_preview_urls=True`), `response_status`, then one column per agent trait — so in the example above, `first_name` and `plan`.

Each `url` is that one agent's link — send it to that person and no one else. Each `preview_url` is the same link with `save_response=false`, so you can walk that respondent's personalized survey end-to-end without it counting as their response.

**To check an agent's link, always open its `preview_url` — never the `url`.** The `url` is that respondent's one live link: opening it and answering records a response against them and flips their `response_status`, so a respondent who later opens their own link finds it already used. This applies to the user too — when showing them what a personalized link looks like, hand over the `preview_url`, and only pass out the `url` values when you are actually distributing the survey. Note also that these links are bearer tokens: whoever holds one sees that agent's traits (see "Personalizing a survey per respondent").

`response_status` in the same CSV also gives a per-person completion view without a separate call.

### Emailing the links

If you want Coop to send the links rather than distributing them yourself, carry each address as a trait and pass a `delivery_map` at deployment naming that trait:

```python
from edsl.coop.coop_humanize_notifications import ChannelConfig, DeliveryMap

agents = AgentList([
    Agent({"first_name": "Alex", "plan": "Starter", "email_address": "alex@example.com"}),
    Agent({"first_name": "Jordan", "plan": "Pro", "email_address": "jordan@example.com"}),
])

info = survey.by(agents).humanize(
    human_survey_name="Q3 2026 plan satisfaction check-in",
    survey_description="Q3 2026 plan satisfaction check-in",
    agent_list_description="Q3 2026 plan satisfaction check-in — active subscribers",
    delivery_map=DeliveryMap(email=ChannelConfig(col_name="email_address")),
)
```

`col_name` must match the trait key holding the address. Everything after that — sending, subject and template content, reminders, scheduled campaigns, completion callbacks, delivery tracking — belongs to **`skill:edsl-human-survey-notifications`**. Read it whenever email is in scope; do not improvise sends from this skill.

## Personalizing a survey per respondent

**Rule — respondent-level data means one tokenized link per person.** If the user gives you respondent-level data to personalize with, you **must** deploy it as an agent list so each person gets their own tokenized link (see "With agents"). Do **not** build a single shared link that asks respondents to identify themselves and then retrieves or applies their row. A respondent can enter someone else's identifier — or talk an AI interviewer into looking up another respondent's record — and reach personalization that is not theirs. This is not a trade-off to weigh against convenience, and the protection must not be circumventable by anything the respondent types or says: no question, no thinking question, and no interview guide may look a respondent up in preexisting data.

Personalizing from **answers given during the survey** is fine, as long as those answers are not used to look up preexisting respondent-level data. The line is the lookup, not the tailoring.

**First, check that the inputs actually exist — do not assume.** Before designing any personalization, inspect what the user gave you. Do they have a list of *who* the respondents are, and does it carry the fields to tailor on? That list is what makes personalization-in-advance possible; without it there is nothing to bind content to. Users often ask for per-respondent personalization without having supplied the respondent list or the tailoring content. If either is missing, ambiguous, or you are inferring it, **stop and ask** — do not invent a respondent list or guess which column holds the personalized content. Confirm before building.

A rule the user gives you ("greet returning customers warmly, ask new ones how they heard about us") is not by itself personalization-in-advance — the rule still needs a **signal** to key off. Sort out which kind you have, because it changes the whole design:

- **Mid-survey adaptation** — the signal is an **answer collected during the survey** ("are you a returning customer?"). This needs nothing set up in advance — no respondent list, no dataset: just ask the question, then pipe the answer (`{{ q.answer }}`) or branch with skip logic. Most "personalization" requests are really this. Reach for it first — it is the simplest thing that works.
- **Personalization-in-advance** — the tailoring must be in place **before the respondent answers anything** (their name already known, their account history, a pre-assigned segment). Only this needs an identity established up front, and it is where the mechanism constraints below bite.

**Nothing in humanize fetches personalized content from a value the respondent types in.** Scenarios and agent traits both bind at deployment — `scenario_list_method` is only `randomize` / `ordered` / `loop` / `single_scenario`, and an agent is fixed to the link it was minted with. Skip rules (`add_rule` / `add_skip_rule`) only branch among **pre-written** questions on the basis of *answers* — they fetch nothing. So personalization-in-advance requires knowing who the respondents are **before you deploy**. If the user doesn't know that, say so rather than engineering around it: the tailoring has to come from answers collected during the survey instead. And do not route rich per-respondent personalization through skip logic alone — it forces you to duplicate the entire question set for every variant.

**One deliberate exception — per-item follow-ups.** If the goal is to ask the *same* block of questions once per item of a list the respondent just typed ("name your departments, then 3 questions about each"), `Survey.loop_over` is the right tool and it does work in humanize: it expands at build time into piped copies plus skip rules, both of which humanize supports. That is duplication-plus-skip-logic done deliberately, with a `max_items` cap — not the open-ended personalization warned against above. Caveat: there is no loop-aware web renderer yet, so respondents see `max_items` separate questions and the default labels read `head__loop0__depts`; set `question_text` so each copy reads naturally and expect a longer-looking form. See **skill:edsl-surveys**.

**Security — flag this to the user before building any advance personalization.** A human survey can require sign-in to an Expected Parrot account, which authenticates the account and records its username. That does not verify that the account belongs to the intended recipient of a personalized link. A per-respondent link is still a **bearer token**: a forwarded email, shared screen, leaked URL, or message sent to the wrong address lets whoever holds the link see that respondent's content. So whenever the personalized content is sensitive or identifying, explain both controls clearly: *"respondents can be required to sign in to an Expected Parrot account, but the survey does not check that the signed-in account is the person this personalized link was intended for. The link can still be forwarded. Is that acceptable, or should we limit the content to non-sensitive fields?"* Get an explicit decision and record it in `plan.md`. Do not present account sign-in or a unique link as proof that the intended person opened the survey.

Paths for personalization-in-advance, in order of preference — clarify which the user wants before writing `plan.md`:

- **Agent list with per-respondent links (preferred; least exposure).** Put each person's row in an `Agent`, pipe the fields with `{{ agent.<trait> }}`, and send each person the link that `get_human_survey_respondent_links` pairs with their row — see "With agents". One deployment, one question set, and the binding is fixed at deployment rather than by arrival order. The link is still a bearer token (see security note above), but nothing else here exposes less.
- **Shared link + branch on an entered/initial answer (finite variants).** When the signal is a small fixed set (e.g. a few segments, or a chosen language), ask it up front and branch each downstream question's *wording* with Jinja `{% if %}` in `question_text` (see **skill:edsl-surveys** — "Jinja if/then for per-answer wording"), or use skip logic to show/hide whole questions. Not for arbitrary per-respondent content.

Record whether the tailoring is mid-survey adaptation or personalization-in-advance, the mechanism, its constraints, and any failure handling in `plan.md`.

**Show the user any personalization text before wiring it in.** When you draft a summary or other text derived from the user's data/instructions to pipe into an `interview_guide`, question, or thinking-question prompt, describe what it says, which fields it uses, and where it goes, and offer to show the full draft. Don't deploy or run personalized content until the user has approved it.

## Retrieving responses

```bash
# Using the UUID returned by `ep humanize create`:
ep humanize responses <survey_uuid> --output data/human_responses.ep
ep results columns --file data/human_responses.ep
ep results head data/human_responses.ep \
  --column answer.preference \
  --column answer.why
```

For a response window, the Python API supports
`Coop().get_human_survey_responses(uuid, started_after="2026-09-01T00:00:00Z",
started_before="2026-09-08T00:00:00Z")`. Bounds are inclusive and refer to when
the respondent **opened** the survey, not submission time. Use timezone-aware
datetimes or ISO 8601 strings with explicit offsets. Save the returned object
with `.git.save(...)` and inspect it normally. The current responses CLI has no
corresponding timestamp flags; do not invent them. In-progress responses are left
out by default; to include and analyse them, read `references/in-progress-responses.md`.

### Listing your human surveys

```python
listing = coop.list_human_surveys(page=1, page_size=10, search_query="preference")
# Returns: {"human_surveys": [{"uuid", "name", "visibility", "created_ts", "n_complete", "n_in_progress"}, ...],
#           "current_page", "page_size", "total_pages", "total_count"}
```

### Checking status

```python
status = coop.get_human_survey(info["uuid"])
print(f"Completed: {status['n_complete']}, in progress: {status['n_in_progress']}")
```

### Working with file upload responses

If the survey includes a `QuestionFileUpload`, each response's answer for that question is a list of file-info dicts. Use `FileStore.from_file_upload_answer` (single file) or `FileStoreList.from_file_upload_answers` (all files) to download and wrap them:

`QuestionFileUpload` is a respondent-facing humanize question, not a way for
the researcher to attach a stimulus. For survey authoring and Builder advice,
keep three actions distinct: create the upload question in the EDSL survey,
publish/import the saved survey into Builder, and later download respondent
upload answers. The Builder handoff is a remote publication: load
`skill:edsl-object-publishing` and obtain explicit consent plus a meaningful
alias, description, and visibility before pushing. Verify the current Builder
UI before claiming it can or cannot create that question type directly. Even if
a control is absent, the supported EDSL question can remain in the pushed
`survey.ep` while the researcher edits other survey fields in Builder.

```python
from edsl.scenarios import FileStore, FileStoreList

results = coop.get_human_survey_responses(info["uuid"])

uploaded_files = results[0]["answer"]["my_upload_question"]  # list of file dicts

fsl = FileStoreList.from_file_upload_answers(uploaded_files)  # all files
fs  = FileStore.from_file_upload_answer(uploaded_files[0])    # single file
```

The returned `FileStore` / `FileStoreList` objects behave like any other — you can inspect, filter, or pass them into further EDSL workflows.

## QR codes

Generate a QR code for a survey's respondent URL:

```python
from edsl import Coop

coop = Coop()
qr = coop.get_human_survey_qr_code(info["uuid"])

# Save as PNG
qr.save("my_survey_qr.png")
```

## Prolific integration

For **paid recruitment via Prolific** — sample size, payment, cost estimation,
eligibility filters, publishing, monitoring, and collecting responses — use the
dedicated **`skill:edsl-prolific-study`**. It is the canonical reference for the
full Prolific lifecycle; read it whenever a study involves paid recruitment.
In particular: Prolific `name` / `description` are **participant-facing listing
copy** — do not reuse Coop `human_survey_name` or internal study labels.

## Using QuestionInterview with humanize

Read [the QuestionInterview deployment reference](references/question-interview.md) for intro screens, voice pacing, speaking-voice options, voice/text configuration, structured questions, mid-interview images, end policies, and reply-state behavior.

## Using QuestionEdit with humanize

For a task where respondents revise supplied copy, use `QuestionEdit`. It
returns the complete revised text; Humanize provides a direct editor with
tracked insertions and deletions. Its `text_to_edit` can be piped from an
earlier answer or filled from scenario data.

- The text box starts filled with `text_to_edit`, so submitting it unchanged is a
  valid answer: "no edits" arrives as the original text, not a blank.
- Clearing the box is rejected unless the question is `optional` in the humanize
  schema.
- Results hold only the final text, not the tracked changes. To analyse what
  changed, compare each answer with the text that was supplied.

## Invisible thinking questions

A humanized survey can include **thinking questions** (`thinking_question`-wrapped) that run **server-side and are never shown to the respondent**, then feed their result into a later visible question via piping (`{{ q_name.answer }}`).

Each one runs an AI inference step with its own model and system prompt — no respondent, no agent persona — between the questions the human sees. Use them to classify, summarize, or reason about prior answers — or an uploaded file — and then present a tailored or branched follow-up. They work on what the respondent has already given you; to tailor on facts you knew beforehand, put those in agent traits and pipe `{{ agent.<trait> }}` instead (see "With agents"), which is deterministic and costs nothing per response. The respondent auto-advances past them, landing on the next human-input question. Thinking-question inference is billed to the survey owner (see `skill:edsl-surveys-cost`).

Because the respondent waits while that inference runs, set a `submitting_indicator` on the question they submit just before it — see "Submitting indicator" above. The same applies to an image generation question, where the wait is longer still.

Full flow, a worked example, and piping/file notes → `references/background-questions.md`. For the wrapper API itself, see `skill:edsl-surveys`.

If a background question fails with an error a retry could fix, it is retried once. If that fails too, or the error isn't retryable, the respondent sees "This survey can't continue right now" and stops. To find out why, read its runs (`ep humanize background summary <uuid>` first) — the debugging steps and what each error kind means are under "When a background question fails" in `references/background-questions.md`.

### Generated images (`QuestionImageGeneration`)

`QuestionImageGeneration` occupies the same invisible slot: it auto-advances, the respondent never sees it, and its answer — an image `FileStore` — is available to later questions. Show the image to the respondent by piping `{{ q_name.answer }}` into a visible question's text. That makes a generate-then-react flow possible in a web survey: take an input from the respondent, generate an image from it, then ask them about the result.

```python
visual = QuestionImageGeneration(
    question_name="dream_kitchen",
    question_text="A kitchen renovated in this style: {{ style_choice.answer }}. Photorealistic.",
)
reaction = QuestionFreeText(
    question_name="reaction",
    question_text="Here's that kitchen: {{ dream_kitchen.answer }} — what would you change?",
)
```

- **Referenced images are input images.** If the prompt pipes a scenario image or a respondent's `QuestionFileUpload` answer, that file is sent to the provider as an actual image, so the generation edits or extends it. Constructor and provider details → `skill:edsl-surveys`.
- **Cover the wait.** Set a `submitting_indicator` on the visible question *before* it (see "Submitting indicator") — image generation is slow enough that the respondent will notice, and a call that runs past ~3 minutes fails their page.
- **Billed to the survey owner** per response, like thinking questions — the owner needs a positive balance. See `skill:edsl-surveys-cost`.

## AI agents

A deployed human survey can also let AI agents take it through an agent link, with the
researcher choosing who produces the answers (the participant through their agent, or
the agent alone) and what guidance agents get. Agent responses are marked in the
results. See `skill:edsl-human-survey-agent-access`.

## Using humanize for validation

Humanize is also the primary mechanism for collecting a human comparison sample to validate LLM results. Deploy the same EDSL survey to real respondents, retrieve results as a standard `Results` object, and compare distributions to the LLM run using the methods in `skill:methods-response-validation`.

Key point: if you plan to validate, design the LLM survey with comparability in mind — same question order, same response scales, and the same piping (not survey memory APIs) that humanize uses. See "Memory and piping" above.

## Quick reference

| Task | Code |
|------|------|
| Humanize a survey | `survey.humanize(human_survey_name="...")` |
| Humanize with an agent list (one link per person) | `survey.by(agents).humanize(agent_list_description="...")` |
| Pipe an agent trait into a question | `{{ agent.first_name }}` in `question_text`, `interview_guide`, etc. |
| Get per-respondent links + traits as CSV | `Coop().get_human_survey_respondent_links(uuid, save_path="links.csv", include_preview_urls=True)` |
| Email the links | deploy with `delivery_map=DeliveryMap(email=ChannelConfig(col_name="email_address"))`, then `skill:edsl-human-survey-notifications` |
| Preview a draft (no live survey) | `runway render survey.ep --schema humanize_schema.json` — see `skill:edsl-human-survey-preview` |
| Test the live survey without adding a response to results | `info["preview_url"]` (returned by `.humanize()` / `get_human_survey`) |
| Pipe a prior answer into a later question | `{{ q_name.answer }}` in `question_text` or `interview_guide` — not survey memory APIs |
| Humanize with scenarios | `survey.by(scenarios).humanize(scenario_list_method="randomize")` |
| Style with CSS | see `skill:edsl-human-survey-css` |
| Add JavaScript to a question, or log events | see `skill:edsl-human-survey-javascript` |
| Make a question optional | `humanize_schema={"questions": {"q_name": {"optional": True}}}` |
| Use slider for numerical | `humanize_schema={"questions": {"q_name": {"format": {"type": "slider", "min": 0, "max": 100}}}}` |
| Matrix carousel | `{"questions": {"matrix_q": {"format": {"type": "carousel", "advance_on_select": true}}}}` |
| Preselect a matrix column | `{"questions": {"matrix_q": {"preselection": {"rules": [{"match": {"type": "all"}, "option": {"type": "text", "value": "Neutral"}}]}}}}` |
| Survey progress | `{"survey": {"progress": {"type": "bar", "label": {"type": "percent"}}}}` — also `hidden` or `steps` |
| Attention check | `humanize_schema={"questions": {"q": {"custom_validation": {"select_exact_answer": "Blue"}}}}` |
| Add a logo | `Coop().upload_human_survey_asset("logo.png")`, then `{"survey": {"branding": {"logo": {"source": {"type": "asset", "asset_uuid": logo.uuid}, "alt": "Acme Research logo"}}}}` |
| Time-limit a question | `{"questions": {"q": {"time_limit": {"duration": {"type": "fixed", "seconds": 300}}}}}` — ignored under group presentation |
| Show a wait indicator while the next background question runs (thinking or image generation) | `humanize_schema={"questions": {"q": {"submitting_indicator": {"type": "callout", "title": "Analyzing…"}}}}` |
| Show images inside a text interview | attach `FileStore` values to a scenario, name the keys in `interview_guide` |
| Custom interview intro screen | `humanize_schema={"questions": {"q": {"intro_screen": {"type": "default", "instruction": "..."}}}}` |
| Change a deployed survey (patch or redeploy) | read `references/editing-live-surveys.md` first |
| Pull a deployed survey's survey, scenarios, agents, and schema | see "Pulling a deployed survey" in `references/editing-live-surveys.md` |
| Invisible AI step piped into next question | see "Invisible thinking questions" → `references/background-questions.md` |
| Generate an image mid-survey and show it back | `QuestionImageGeneration(...)`, then pipe `{{ q_name.answer }}` into a later question |
| Debug a thinking or image question (respondents stuck, "can't continue") | `ep humanize background summary <uuid>`, then `runs <uuid> --failed`, then `run <uuid> <run-uuid>` → "When a background question fails" in `references/background-questions.md` |
| Get respondent link | `info["respondent_url"]` |
| List all human surveys | `ep humanize list --query "..."` |
| Check response count | `ep humanize status <uuid>` |
| Fetch results | `ep humanize responses <uuid> --output data/human_responses.ep` (`--include-partial` adds in-progress; see `references/in-progress-responses.md`) |
| Download file upload answers | `FileStoreList.from_file_upload_answers(results[0]["answer"]["q_name"])` |
| Get QR code | `ep humanize qr <uuid> --output writeup/human_survey_qr.png` |
| Check Prolific account and participant limit | `Coop().get_prolific_study_settings()` — see `skill:edsl-prolific-study` |
| Launch Prolific study | `Coop().create_prolific_study(uuid, ...)` |
| List Prolific studies for a survey | `Coop().list_prolific_studies(uuid)` |
| Check a Prolific draft before publishing | `Coop().preflight_prolific_study(uuid, study_id, expected_survey=survey, required_credits=credits)` — see `skill:edsl-prolific-study` |
| Publish Prolific study (make live) | `Coop().publish_prolific_study(uuid, study_id, expected_survey=survey, required_credits=credits)` |
| Fetch Prolific results | `Coop().get_prolific_study_responses(uuid, study_id)` |
| List Prolific filters | `Coop().list_prolific_filters()` |
| Reset scenario ordering | `Coop().reset_scenario_sampling_state(uuid)` |
| Update CSS on live survey | see `skill:edsl-human-survey-css` |
| Fetch events logged by a survey's scripts | `ep humanize events <uuid> --all --output events.jsonl` — see `skill:edsl-human-survey-javascript` |
| Add an AI chat assistant, or fetch what respondents did with it | see `skill:edsl-human-survey-assistant` |
| Let AI agents take the survey | `Coop().patch_human_survey_agent_access(uuid, {"enabled": True})` — see `skill:edsl-human-survey-agent-access` |
