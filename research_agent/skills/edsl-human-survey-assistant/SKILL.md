---
name: edsl-human-survey-assistant
description: >
  Adds an AI chat assistant to an EDSL human survey: choosing its role, which
  questions it may fill, hiding it on attention checks and condition pages,
  testing it, changing it on a live survey, and downloading what respondents
  did with it. Use when the researcher wants respondents to have an AI helper
  beside the form, is studying the effect of AI assistance, or wants the
  assistant's conversations or interaction data.
tags: [edsl, data-collection]
---

# Human Survey Assistant

The survey assistant is an AI chat beside a human survey. Respondents can ask it
what a question means, or tell it their answer in their own words and have it fill
in the form. Each answer it fills is shown in the chat with an **Undo** button, and
the respondent still presses **Next**: it can't submit a page. It is configured in
the humanize schema under `survey.assistant`.

## 1. Decide with the researcher first

Before writing the schema, settle these with the researcher. Each changes what the
data means.

- **Role.** `express_intent` (default) helps respondents say what *they* think: it
  explains neutrally and fills answers from what they say, but won't recommend one.
  `advise` may recommend answers when asked, so answers can reflect its advice. Use
  `advise` only when the effect of AI advice is what's being studied. Roles are
  carried out by the model and aren't guaranteed; a respondent who insists may still
  get an opinion, which shows in the conversation.
- **Filling answers.** On by default for most question types. Set
  `can_fill_answers: False` for an assistant that only explains, or
  `fillable: False` on single questions.
- **Pages it must not see.** For attention checks, knowledge tests and pages that
  differ between conditions, set both `chat: False` (no chat on that page) and
  `context: False` (left out of what it knows on later pages). Otherwise it can name
  the right answer to an attention check.
- **Comparing with and without the assistant.** Use separate surveys, one per
  condition, and assign respondents between them. Don't switch the assistant on and
  off mid-fielding to make arms.
- **Cost.** Each reply is charged to the survey owner's account in credits. If the
  balance runs out, the assistant becomes unavailable and respondents carry on
  without it. Chats on a preview link are charged too.

## 2. Add it

```python
humanize_schema = {
    "survey": {
        "assistant": {
            "enabled": True,
            "presentation": {"type": "sidebar"},  # or "modal"
            "system_prompt": "Respondents are adults shopping for a used car.",
            "question_overrides": {
                "consent": {"chat": False},
                "attention_check": {"chat": False, "context": False},
                "priorities": {
                    "instructions": "Fuel economy means the cost of fuel, not emissions.",
                },
            },
        }
    }
}
info = survey.humanize(human_survey_name="...", humanize_schema=humanize_schema)
```

- `presentation` is required, even with `enabled: False`.
- `system_prompt` adds to the role's built-in rules; it doesn't replace them. It and
  each question's `instructions` are never sent to respondents.
- Leave `model` out: the default is the only model accepted, and any other value is
  refused.
- Every field, its limits and which question types it can fill:
  `references/config.md`.

## 3. Test it

- **Runway previews and `survey.preview()` don't show the chat.** Use them for the
  form's layout only (see `skill:edsl-human-survey-preview`).
- After deploying, have the researcher open `info["preview_url"]` and chat with it:
  ask about a question, give an answer in their own words, press **Undo**, and visit
  any page set to `chat: False`. Each reply there is charged.
- Preview chats don't appear in results or downloads unless asked for
  (`include_previews=True`), but they do appear among the conversations, with a
  **Preview** badge (§5).

## 4. Change it on a live survey

Never patch without the researcher's confirmation, as for any change to a live
survey ("Confirm before applying" in `skill:edsl-human-survey`'s editing live surveys
reference). Before patching, check how many responses exist
(`ep humanize status <uuid>`) and tell the researcher:

- what respondents will get differently. A change of `role` changes how they arrive at
  their answers: under `advise` the assistant may recommend answers when asked, so
  answers can reflect its advice.
- that respondents part way through will have answered under both settings, and those
  already finished under the old ones. If the change is a new condition, use a new
  survey instead (§1).

Wait for their go-ahead, then patch only what changes:

```python
from edsl import Coop

Coop().patch_human_survey_humanize_schema(
    "<human-survey-uuid>", {"survey": {"assistant": {"role": "advise"}}}
)
```

```bash
ep humanize schema patch <human-survey-uuid> --schema assistant_patch.json
```

- Changes apply from the next page each respondent is shown. A page already on
  screen keeps its settings. `enabled: False` is the exception: it stops replies
  straight away.
- Record when the patch was applied and what changed, so the analysis can split
  respondents at that point. `settings_versions` in the summary and `configs` show
  it too (§5).
- A patch merges key by key and can't remove a key. To drop an override, patch
  `survey.assistant` to `None`, then write the whole block back without it.

## 5. Reading the data

Start with the summary, `Coop().get_human_survey_assistant_summary(uuid)` (or
`ep humanize assistant summary <uuid>`): respondents offered the assistant and who
chatted, turns by status, the assistant's edits by outcome, the trace's size, and cost.
It says whether there's anything to fetch, and how big the rest is: if no one chatted,
stop there. If `turns.pending` is above zero or `last_activity_at` is recent, fielding
is still live and the numbers will move.

Most questions about the assistant come down to the same few things: what each
respondent asked, what the assistant said and filled in, whether those answers
stuck, and whether it worked as designed. For those, fetch the results
(`skill:edsl-human-survey`) and the conversations, to a file:
`Coop().get_all_human_survey_assistant_conversations(uuid)`, or
`ep humanize assistant conversations <uuid> --output conversations.jsonl`. Each
respondent's survey comes in the order it happened, one row per thing: their messages
and the replies, the answers the assistant filled, had refused or had undone, and each
save of an answer they typed themselves. `references/data.md` has every download, how
they join (on `response_uuid`, `turn` and `edit`), and every field.

The conversations also show where the assistant didn't work: a `reply` whose `status`
is `failed` (with the `notice` the respondent saw) or `interrupted`, and a `message`
with no reply after it. A respondent whose replies failed didn't get the assistant as
designed: count them before comparing conditions. A reply's `ended` tells a
respondent who pressed Stop (`stopped`) from a connection that dropped (`dropped`).

Report counts before going further: respondents who chatted out of those offered the
assistant, turns per respondent, edits by question and outcome, and failed or stopped
replies. Add a few example conversations, or offer them, rather than every
one. Each condition is its own survey, so repeat this per survey. If
`settings_versions` is above 1, the assistant's settings changed during fielding: say
so, and check `configs` before comparing respondents.

Fetch another download only when the summary or the conversations raise a question
they can't answer:

- **`turns`:** when the summary shows failed replies and the researcher needs to know
  why (`error`); or when asked how fast the assistant replied or what a reply cost
  (`sent_at`, `first_text_at`, `credits`).
- **`edits`:** when the report needs the assistant's edits by question across
  respondents, each with its final outcome (which questions it filled most, which it
  was refused on, which were undone), or the summary's `edits.rejected` is above 0
  and the researcher wants to know why.
- **`threads`:** when comparing respondents who chatted with those who didn't, or
  joining assistant use to the results. It's the only list that includes
  respondents offered the assistant who never chatted.
- **`configs` and `pages`:** when `settings_versions` is above 1 (to see which
  respondents got which settings); when asked what the assistant was told; or when
  the chat didn't appear for someone or couldn't fill a question
  (`hidden_by`, `not_fillable`).
- **The interaction trace:** only for what conversations leave out: whether a
  session is `truncated`, when typing began (`first_change_at`), when a reply's first
  words appeared (`first_text_at`), or when a row reached the server. Check
  `trace.rows` in the summary first, and fetch it per response or to a file.
- **`messages`:** almost never. Only for one turn's conversation (`turn=`) without
  fetching a whole response.

Every download takes `response_uuid` for one respondent. `messages` and `edits` also
take `turn` for a single message and its reply. To read conversations in the browser,
open `Coop().get_human_survey_assistant_url(uuid)`.

Every download leaves out previews unless `include_previews=True`. Tell the researcher
what's missing:

- Turns from the last few seconds may not be listed yet.
- Trace sessions marked `truncated` are incomplete.
- Respondents who were offered the assistant but never chatted have no messages or
  replies in their conversation: they're in `threads` with `turns` 0.
- Rows placed by their turn (`placed` other than `trace`), null text or status, and
  `sent` edits each have a cause to check: "Gaps and odd rows" in
  `references/data.md`.
