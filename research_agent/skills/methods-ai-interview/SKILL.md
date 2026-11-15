---
name: methods-ai-interview
description: >
  Design and run AI-led interviews with QuestionInterview — adaptive follow-up
  for depth, stories, and reasoning. Use when a study needs interviews with
  real human respondents (humanize) or simulated AI agents/personas (turn-based
  run), including mixed survey-plus-interview designs, guide piloting, or
  post-simulation depth — even if the user has not asked for an interview.
tags: [methods, qualitative, data-collection, simulation]
---

# AI interviews

`QuestionInterview` is a **multi-turn** conversation — not a single `QuestionFreeText`. Proactively suggest it when depth, stories, reasoning, or "why" matter. Do not wait for the user to say "interview."

Draft guide content with **skill:research-interview-design**.

Use this skill to decide when to suggest an AI interview, how to explain it, how it fits into a survey, and how to run it for either human respondents or simulated agents/personas.

## Choose a path

| | Human respondents | Simulated agents/personas |
|---|---|---|
| **When** | Real people in a browser | Pilot a guide, persona grid, post-simulation depth |
| **Run** | `Survey(...).humanize()` | `Survey(...).by(agents).by(models).run()` |
| **Mechanics** | **skill:edsl-human-survey** | This skill, especially simulation guidance below |

Do not use `.humanize()` for agent simulation. Do not use `.run()` when the user wants real human respondents.

## Decisions and capabilities to surface

For an underspecified interview, perform the bounded review required by
`skill:workflow-session-start` after loading the relevant owner skills. Select
only considerations that affect this interview; do not recite this section.
Infer useful options from the research goal; do not wait for the researcher to
name features. Explain relevant recommendations and tradeoffs before finalizing
the design, while preserving settled choices.

- **Must resolve:** human versus simulated respondents; the interview's goal;
  and, for humans, text, voice, or respondent choice. Ask before enabling a
  human interview or another consequential participant-experience feature.
- **Suggest when relevant:** mix structured questions into the same instrument
  when clean coded outcomes matter; pipe already-collected answers into the
  interviewer so it does not ask for known information again; use image stimuli
  only for text-mode interviews; use a checklist or end policy when topic
  coverage or stopping consistency matters.
- **Evidence boundary:** simulation can pilot a guide, explore persona-linked
  hypotheses, and expose model sensitivity. It cannot establish lived
  experience, prevalence, genuine behavior, or human fatigue. For human
  fielding, surface recruitment, privacy, accessibility, preview, quality, and
  cost only when they affect the stated goal.
- **Fast path:** if the researcher asks for a simple text interview, use text
  with no widgets or feature tour. If they supply a settled guide or request a
  narrow edit, preserve it and make the edit.
- **Phase transition:** when a simulated pilot moves to humans, newly review
  participant mode and experience, recruitment, consent/privacy, live preview,
  response quality, and cost. Do not assume that a simulation-ready artifact is
  field-ready.

For a combined design, assign each phase a role. Usually AI is the bounded
instrument/guide pilot and humans provide evidence about real experience or
behavior. State what must remain comparable, what advances the study to the
human phase, and what human evidence can confirm or overturn; do not create two
unrelated studies.

## When to suggest

Suggest `QuestionInterview` when the user wants:

- **why**, **how**, or **stories** behind attitudes
- qualitative depth or adaptive follow-up
- UX, product, journey, or task-walkthrough research
- screeners routing some respondents to depth
- piloting a guide before fielding
- depth across an agent list
- post-survey or post-simulation explanation
- "talk to people," "qualitative," "open-ended," or "deeper" feedback

Do not silently replace an interview with `QuestionFreeText` when adaptive follow-up would be better.

## When not to suggest

Do not push an AI interview when:

- the study is pure quantitative tracking with no need for depth
- the user needs identical fixed wording for every respondent
- the user explicitly wants a short form with no conversation
- the depth wanted is **structured per-item probing** rather than open-ended conversation — "ask them which tools they use, then the same 3 questions about each tool." That is `Survey.loop_over` (see **skill:edsl-surveys**): fixed wording, one clean column per item per question, no transcript to code. Choose the interview only when the follow-ups must genuinely adapt to what the person says; choose `loop_over` when the follow-ups are known in advance and only the *items* vary.

If useful, mention an interview as an optional follow-up wave, but respect the user's stated preference.

## How to explain the option

Use plain language. Emphasize value, not jargon.

Suggested framing:

> "For the depth you're after, I'd suggest adding an AI interview block to the same survey link — not just a single free-text box. The AI asks follow-ups based on what each person actually says, like a good moderator. We can still keep your multiple-choice, scale, and screener questions in the same instrument, including routing rules that decide who gets the interview."

Ask for confirmation before finalizing a human respondent design that includes an interview.

## Response mode: text, voice, or both

Letting respondents answer an interview by text or voice is a **built-in `QuestionInterview` setting** — `interview_mode` in the humanize schema: `"text"` and `"voice"` force one mode, `"both"` lets the respondent pick text or voice at the intro screen. It needs no custom UI, transcription, or storage work.

**Default behavior: for any human interview design, ask whether respondents should be able to choose text or voice** (`interview_mode: "both"`) — unless the user has already made their preference clear, in which case just apply it. If the user has already said "let them choose" / "either" / "don't require one," map that straight to `"both"` and confirm.

`interview_mode` applies to the `QuestionInterview` only. Don't confuse voice mode with **mic dictation**, which lets a respondent speak their messages into a *text* interview instead of typing them — that is still a text interview, and it is not available on the survey's other questions. Under `"both"`, respondents who pick text can dictate. If the user says "voice," clarify which they mean rather than assuming. See **skill:edsl-human-survey**.

Full schema + `voice_interview_config` / `text_interview_config` → **skill:edsl-human-survey**.

## `QuestionInterview` fields

| Field | Role |
|-------|------|
| `question_text` | Short interview **goal** or topic label — not the full guide |
| `interview_guide` | Full script: topics, probes, stopping guidance. Never empty or placeholder |
| `max_turns` | Cap on interviewer turns in **simulation only**. Use with `.run()` for simulated agents/personas, not humanized deployment |

## Interview guide files

For **human** deployment, write two files in the same `edsl_jobs/job_*` directory:

| File | Contents |
|------|----------|
| `interview_guide.md` | Full AI interviewer script in markdown, readable and editable by the researcher |
| `deploy_interview.py` | Survey + `.humanize()` — loads the guide, no inline guide text |

Required workflow:

1. Write `interview_guide.md` with the complete guide content.
2. Present `interview_guide.md` directly with `ep present`.
3. Write `deploy_interview.py` beside it.
4. Load the guide from disk.

```python
from pathlib import Path

interview_guide = Path(__file__).with_name("interview_guide.md").read_text(encoding="utf-8")
```

Never embed the guide in `deploy_interview.py` as `interview_guide = """..."""`.

Never put the AI guide under `writeup/`.

Never use alternate guide filenames like `interview_guide_ai.md`.

For guide content and quality, use **skill:research-interview-design** (including **skill:research-interview-design** → `references/interviewer-conduct.md` for hard rules and voice turn-taking). For job directory naming, see **skill:workflow-file-layout**.

---

## With human respondents

**Explain it:** an AI interview block in the same survey link asks follow-ups based on what each person says — not just one open-ended box. Confirm before finalizing.

**Resolve identity before finalizing question order.** Ask whether responses should be
anonymous or linked to a respondent name/ID. Explain that anonymity reduces
privacy risk, while an identifier supports follow-up and record linkage. If the
researcher chooses identified responses, add a required free-response name or
ID question after any eligibility screeners but before substantive structured
items and the interview. This avoids retaining identifiers from respondents who
screen out. If there is no screener, the identifier can be the first respondent
question. Do not silently collect identity, infer it from recruitment metadata,
or add both name and ID when one is sufficient.

**Respondent experience:**

1. The respondent sees an intro screen explaining the interview.
2. They start a text chat or voice conversation.
3. The AI asks adaptive follow-ups based on the interview guide.
4. A turn-by-turn transcript is saved automatically.
5. The respondent taps Finish and continues to any remaining survey questions.

Structured questions and interview items can live in the same survey link.

**Decide where structured questions belong.** When the researcher adds
multiple-choice, numeric, scale, file-upload, or other fixed questions to an
interview study, do not assume they belong inside the conversation. Show the
proposed order and ask one explicit placement decision:

- ordinary survey questions before the interview;
- ordinary survey questions after the interview;
- split before and after; or
- supported text-interview widgets asked inside the conversation.

Recommend ordinary before/after questions when clean standalone columns,
non-interview question types, or stable wording matter. Use in-conversation
`structured_questions` only for supported multiple-choice/numerical moments
that benefit from conversational timing, and only after approval.

**Deploy:**

```python
from pathlib import Path

from edsl import QuestionInterview, Survey

interview_guide = Path(__file__).with_name("interview_guide.md").read_text(encoding="utf-8")

q = QuestionInterview(
    question_name="depth_interview",
    question_text="Understanding why customers churned",
    interview_guide=interview_guide,
)

survey = Survey([q])

survey.humanize(
    human_survey_name="Churn depth study",
    humanize_schema={
        "questions": {
            "depth_interview": {"interview_mode": "both"}
        }
    },
)
```

**Text, voice, or both**

Set `interview_mode` per question in `humanize_schema`. Default is `"text"` if omitted.

| Mode | Respondent experience | When to use |
|------|----------------------|-------------|
| `"text"` | Chat-style interface — type answers, read AI follow-ups on screen | Default. Lower friction, async-friendly, easy to skim transcripts. Best when respondents may be in public/noisy settings or prefer writing. |
| `"voice"` | Voice conversation — speak answers, hear AI follow-ups | Richer tone and pacing; good for UX walkthroughs, emotional topics, or users who think out loud. Requires a quiet environment and microphone access. |
| `"both"` | Respondent chooses text or voice before the interview starts | Use when mode preference is unknown or the audience is mixed. Slightly more setup on the intro screen. |

The `question_text` is not shown to respondents — it frames the interview internally. What they experience is driven by the guide and the mode you set.

Ask the user which mode fits their audience before deploying. If unsure, `"both"` is a reasonable default for human studies; `"text"` if you need maximum completion rates or silent environments.

For voice or `"both"` mode, also ask which spoken language respondents should use, and offer a choice of how the AI interviewer should **sound** (different speaking voices). Ask in plain language — "which voice should the interviewer use?" — not schema field names. Set both under `voice_interview_config` in `humanize_schema` (language defaults to English; `"multilingual"` auto-detects; omit the voice setting to keep the deployment default). Allowed voices, schema fields, and live patching → **skill:edsl-human-survey**.

**When language comes from a prior answer:** interview `language` is fixed per `QuestionInterview` in the schema — it cannot branch on `{{ q.answer }}`. Create a separate interview question per language (each with its own guide and `language` config) and use skip logic to route respondents to the matching one. Full pattern → **skill:edsl-human-survey** (`references/interview-languages.md` — "Language chosen by a prior question").

**Checklist and end policy (text mode)**

For text-mode interviews you can also give the interviewer a **checklist** of items to cover and **dictate how the interview ends** — both set under `text_interview_config` in `humanize_schema`.

A checklist turns coverage goals into items the AI marks off as they're met. The respondent can optionally see them.

An `interviewer_gated` end policy hides the End Interview button until those goals are met, so the interview can't be cut short before the required topics are reached. With that gate you can also decide what happens the moment the AI marks the interview complete: leave the chat open for late additions, or lock it so that turn is the clean stopping point.

Separately, `participant_chat_during_reply` decides whether respondents can type while the AI's reply is still generating; leave it open unless the user asks to lock it.

When coverage or stopping consistency matters, recommend checklist and ending options alongside the guide. Keep respondent-controlled ending unless the researcher chooses gating after understanding its effect. They can also be adjusted on an already-deployed interview without re-running `.humanize()` (via `patch_human_survey_humanize_schema`). For the field reference and live-patching, see **skill:edsl-human-survey**.

**Structured questions (text mode)**

A text interview is pure prose by default. `structured_questions` lets the AI pose a **multiple-choice** or **numerical** question mid-conversation as an actual input widget — radio buttons or a number field — so those specific points come back as clean coded answers instead of prose someone has to code later. The rest of the conversation stays conversational.

Never enable this on your own initiative. It changes how the interview behaves, and many users want a purely conversational instrument. You may suggest it when the design calls for coded answers at specific moments, but only add it once the user has agreed.

If they agree, the guide has to do the work: enabling the capability only grants permission — the AI decides when to use it from `interview_guide`. Name the moment, spell out the exact answer options or accepted range, and tell it to render a structured question rather than typing the question into its message. Field reference (`allowed_types`) and guide wording → **skill:edsl-human-survey**.

**Showing images (text mode)**

A text interviewer can display images inline in the chat — a concept or package design to react to, a screenshot to walk through, a diagram to fall back on when a respondent has misunderstood something. Attach the images as `FileStore` values on a scenario and name each key in the `interview_guide` at the point it should appear. Suggest it whenever the topic has visual stimulus the respondent would otherwise only be told about.

This is text-only — a voice interview cannot show anything. So when images carry part of the material, set `interview_mode` to `"text"` rather than offering `"both"`, and tell the user why: whoever picked voice would sit through an interview missing half of it. That overrides the usual "ask whether respondents may choose" default.

The guide must also say when *not* to show each image. Every image on the scenario is available for the whole conversation, so a guide that only names the trigger will get them re-shown. Setup code and the full rules → **skill:edsl-human-survey** — "Showing images mid-interview".

**Other text-mode touches**

`text_interview_config` also carries the written interview `language` (separate from the voice one above), `interviewer_name` for the label above the AI's messages, and `end_interview_message` for the closing screen. The intro screen respondents see before either mode starts is customizable too, via the question-level `intro_screen` — a place to greet respondents, set expectations, or give consent language. Fields → **skill:edsl-human-survey**.

For preview, styling, and other `humanize_schema` options, see **skill:edsl-human-survey**.

Do not use `max_turns` for humanized deployment. For now, treat `max_turns` as simulation-only.

**Memory and piping**

Survey memory modes (`set_full_memory_mode()`, `add_targeted_memory()`, etc.) are for simulated `.run()` jobs only — they have no effect in humanize. For mixed survey + interview designs, pipe screener or demographic answers into `question_text` or `interview_guide` with `{{ q_name.answer }}`. Full rules → **skill:edsl-human-survey** — "Memory and piping".

**Proactively surface answers from earlier questions.** When an interview follows ordinary survey questions, the interviewer has **no automatic knowledge of those answers** — it only sees what you pipe in. Review the prior questions: if their answers are context the interviewer would naturally build on (e.g. limits, preferences, prior selections), pipe them into the `interview_guide` (its natural home — that's the interviewer's brief) so the AI can reference them instead of re-asking. **Suggest this to the user** — an interviewer that ignores answers the respondent just gave reads as broken and redundant.

**Mixed survey + interview pattern:**

```text
[Screener multiple choice]
→ routing / stop rules
→ optional demographics
→ AI interview
```

Example:

- **Screener:** "Have you used [product] in the last 30 days?"
- **If No:** stop or skip to end.
- **If Yes:** route to `QuestionInterview`.
- **Interview:** draft or adapt `interview_guide.md` with **skill:research-interview-design**.

Use **skill:edsl-surveys** for `add_skip_rule`, `add_rule`, `add_stop_rule`, and `EndOfSurvey`.

When presenting the plan, show the question order and routing so the user can see how structured and adaptive parts fit together.

**After fielding** — mention only what applies:

- Transcript email on submission: **skill:edsl-human-survey-notifications**
- Thematic synthesis: **skill:methods-thematic-analysis** or **skill:research-qualitative-data-analysis**
- Transcripts → personas: **skill:methods-transcripts-to-personas**
- Compare to LLM simulation: **skill:methods-response-validation**

Do not promise capabilities outside the relevant skills.

**Draft preview before deployment.** Before `.humanize()`, render the full
survey with runway (**skill:edsl-human-survey-preview**) and wait for the
researcher to confirm it. The live walkthrough below comes after this, not
instead of it.

**Researcher walkthrough before launch.** After humanizing and before sharing,
recruiting, or publishing, give the researcher the live preview URL and
proactively ask them to complete the instrument themselves. Tell them to check
the opening, identity choice, routing, interview behavior, structured-question
placement, ending, and completion path. Wait for their feedback and incorporate
approved corrections before launch. A structural code review is not a
substitute for experiencing the respondent flow.

**Deployment handoff.** Always give the researcher all three clickable Markdown
links together: **Preview interview** (`preview_url`), **Participant link**
(`respondent_url`), and **Survey dashboard** (`admin_url`). For external AI-agent
participation, substitute the agent participation link using
skill:edsl-human-survey-agent-access; retain the browser preview and dashboard.
If both routes are intended, label and provide both participation links. Use
actual returned URLs or the documented agent-link derivation, not bare URLs or code-formatted text. Follow the required deployment
handoff in skill:research-interview-design, including missing-link recovery.
Giving the participant link to the researcher is not permission to distribute
it before the walkthrough. Retrieve responses yourself when requested; never
append retrieval code or assign that work to the researcher.

---

## With simulated agents

`QuestionInterview` runs as a **turn-based conversation**: interviewer and respondent alternate each turn until the guide is covered or `max_turns` is reached. The respondent is the `Agent` on the job.

`max_turns` is currently relevant here: use it to cap interviewer turns during simulated `.run()` workflows.

```python
from pathlib import Path

from edsl import Agent, Model, QuestionInterview, Survey

interview_guide = Path("interview_guide.md").read_text(encoding="utf-8")

q = QuestionInterview(
    question_name="career_choice",
    question_text="Understand why people chose their professional field",
    interview_guide=interview_guide,
    max_turns=10,
)

respondent = Agent(
    name="teacher_34",
    traits={"age": 34, "occupation": "high school teacher"},
    instruction="Answer naturally as this person in a qualitative interview.",
)

results = Survey([q]).by(respondent).by(Model("...")).run()  # confirm model at runtime
```

**Read saved transcripts:** Follow [transcript inspection](references/transcript-inspection.md)
for native turn structure, named-agent selection, and the one-command JSONL or
Markdown exporter. Reuse existing study extraction code before exploring schemas;
do not parse native interview answers as strings or assume the first content block
is text. Use the same exporter for report excerpts and appendices.

For survey structure and memory across prior questions in **simulation**, see **skill:edsl-surveys**. For humanize deployment, use piping instead — see **skill:edsl-human-survey**.

---

## Guide sourcing

```text
No guide
→ Draft one with skill:research-interview-design.

Human moderator script
→ Adapt it for an AI interviewer with skill:research-interview-design.

Prior study findings
→ Ground the guide in those findings.

Repeat design
→ Reuse a saved guide when available.
```

Clarify whether the guide will be drafted or supplied by the user.

Never ship a `QuestionInterview` without a real guide.

## Common mistakes

- `QuestionFreeText` when adaptive follow-up is needed
- Empty or placeholder `interview_guide`
- Guide inlined in Python instead of `interview_guide.md`
- Guide written under `writeup/` or with a non-canonical filename
- Human moderator guide pasted verbatim without adapting it for AI
- Full guide pasted into `question_text`
- `.humanize()` for persona simulation
- `.run()` for real humans
- Simulation without an `Agent` on the job
- Screener without routing into the interview
- Identified study without a first name/ID question, or identity collected
  without the researcher's choice
- Fixed questions silently placed inside the interview instead of resolving
  before/after/inside placement
- Promising analysis features not covered by linked skills
- Enabling `structured_questions` without the user agreeing to it first
- Offering `"both"` when the interview shows images — voice respondents never see them
- Using `max_turns` as if it applies to humanized respondent deployment
- `set_full_memory_mode()` or other survey memory APIs on a humanize deploy

## Checklist

- [ ] Depth/stories/"why" matter → suggest `QuestionInterview`, not single free-text
- [ ] Right path: human (`humanize`) vs simulated (`agents + run`)
- [ ] Non-empty `interview_guide`; `question_text` stays short
- [ ] Human deploy: separate `interview_guide.md` + `deploy_interview.py`
- [ ] Guide loaded from disk, not inlined in Python
- [ ] Screeners route into the interview when applicable
- [ ] Human study: resolve anonymous vs name/ID; if identified, put the chosen
  free-response identifier after eligibility screeners and before substantive items
- [ ] Present question order and routing for mixed survey + interview designs
- [ ] Resolve whether structured questions are before, after, split around, or
  supported widgets inside the interview
- [ ] Clarify whether the guide will be drafted or supplied by the user
- [ ] Use `max_turns` only for simulated agent/persona interviews
- [ ] Guide quality → **skill:research-interview-design** (hard rules + conduct → `references/interviewer-conduct.md`)
- [ ] Interview design: ask whether respondents may choose text or voice (`interview_mode: "both"`) unless the user already specified; voice deploy: confirm spoken language and offer how the interviewer should sound → **skill:edsl-human-survey**
- [ ] If interview language comes from a prior answer: fork one `QuestionInterview` per language + skip rules (not Jinja on `language`)
- [ ] `structured_questions` only after the user has agreed, with the guide instructing when to use it
- [ ] Visual stimulus in the topic → offer inline images (text mode only; force `"text"` if the images are essential)
- [ ] Human deploy: prior answers piped (`{{ q.answer }}`), not survey memory APIs
- [ ] Humanize mechanics → **skill:edsl-human-survey**
- [ ] Runway preview of the full survey confirmed before `.humanize()`
- [ ] Researcher completes the live preview before recruitment/publication
- [ ] Chat handoff includes clickable preview, participant, and survey dashboard links
- [ ] Survey routing → **skill:edsl-surveys**
- [ ] Follow-up analysis → only mention relevant linked skills
