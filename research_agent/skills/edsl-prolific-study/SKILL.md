---
name: edsl-prolific-study
description: >
  Launch and manage a paid Prolific study for an EDSL human survey: sample
  size, payment, cost estimation, demographic and quality filters, publishing,
  monitoring, and submission review. Use when the user wants to recruit paid
  human participants on Prolific, target respondents with filters, or manage
  an existing Prolific study.
tags: [edsl, workflow, data-collection, external-tool]
---

# Skill: edsl-prolific-study

Launch and manage a Prolific study for an EDSL survey with human participants.

## When to use

Use this skill when the user wants to:
- Launch a survey with human participants on Prolific
- Set up a human study with appropriate sample size and payment
- Manage an existing Prolific study (publish, pause, stop, collect responses)

## Verify capability before reporting a limitation

The Expected Parrot integration owns Prolific creation, live filters, costing,
publication, monitoring, and response retrieval. Never tell the researcher
that no Prolific API is available, or route them to manual Prolific setup,
without first checking this skill's documented Coop methods and current runtime
connectivity. Account balance, Prolific login state, institutional settings,
and ethics requirements may affect whether a particular study can proceed;
they do not prove that the integration itself is absent. Report the concrete
failed capability check and its error, not a guessed platform limitation.

## Workflow

**These steps are interdependent, not strictly linear.** The numbering is a
default reading order, but real conversations loop between them:
- *Who* you can reach (Step 2) affects *how many* you need and what you pay
  (Step 3): if the target is a subgroup defined by filters, the sample size is
  derived from those segments; if some participants will screen out, you must
  over-recruit.
- *How many / how much* (Step 3) affects whether the study is affordable, which
  can send you back to loosen filters or narrow the population.

The only firm rules: **confirm the final filter set and finalize cost before
you create the study (Step 5)**, and **never publish without explicit user
sign-off (Step 6)** — that is when money is charged.

### Step 1: Humanize the survey

The user should already have an EDSL `Survey` object. If they don't, use the appropriate EDSL skill to help them create one first.

Call `survey.humanize()` to create a web-based version and get a project UUID:

```python
human_survey = survey.humanize(
    human_survey_name="My Study",              # internal, researcher-facing name (NOT shown to participants)
    survey_description="Study about X, run 2026-07.",  # set this — see note below
    survey_alias="my-study-slug",               # optional, creates a friendly URL
    survey_visibility="private",                # "private" or "public"
)

human_survey_uuid = human_survey["uuid"]
# human_survey also contains admin_url and respondent_url
```

`human_survey_name` and `survey_description` are **researcher-facing** — they
label the survey on your Coop content page, not on anything participants see.
Treat them as effectively required: give each a clear, specific name and
description so you can find the survey later and trace which humanize call it
came from (e.g. include the topic and date). A page full of "My Study" entries
is impossible to navigate.

### Step 2: Define the target population and how to reach it

Before sizing the sample, establish **who** the study is for and **how** you can
reach them. Do this early — it drives both the sample size (Step 3) and the
filter confirmation (Step 4), and it can reveal that the survey instrument
itself needs to change.

**Start with the research goal, not a number.** Ask who the user wants to hear
from and what decision the study informs. Many users don't know Prolific
targeting exists, or assume it can screen on anything. Surface what's possible
early — it often reshapes their plan.

**Fetch the available filters now** (see Step 4 for the API) so you can tell the
user what can be targeted directly:

```python
from edsl import Coop
coop = Coop()

filters = coop.list_prolific_filters()
filters.table()
```

**Decide how each targeting criterion will be enforced.** For every "we only
want people who..." requirement, it is one of:

1. **A Prolific filter** — the attribute is one Prolific already collects (age,
   country, employment, education, etc.). Cheapest and cleanest: ineligible
   people never enter the study. Confirm and apply in Step 4.
2. **An in-survey screening question** — the attribute is *not* something
   Prolific tracks (e.g. "uses a competitor product weekly", "holds opinion X",
   "manages a team"). No filter can express it. You must screen inside the
   survey with a question plus early-termination logic:
   ```python
   from edsl.surveys import EndOfSurvey
   survey = survey.add_rule(
       "screener", "{{ screener.answer }} == 'No'", EndOfSurvey
   )
   # or survey.add_stop_rule("screener", "{{ screener.answer }} == 'No'")
   ```
   This is a **change to the survey instrument** — go back to the survey object
   and add it before humanizing (Step 1) if not already present.
3. **Both** — a filter to narrow the pool cheaply, then an in-survey screener
   for the part no filter covers.

**Screening has cost and sizing consequences — flag them:**
- Participants who screen out still consume recruitment (and, depending on
  Prolific's screen-out handling, may still be paid). So you must
  **over-recruit**: if you need 100 qualified responses and expect ~30% to
  screen out, recruit ~145 (`100 / (1 - 0.30)`).
- Prefer Prolific filters over in-survey screening whenever an equivalent filter
  exists — it avoids paying for ineligible participants entirely.

**Summarize the population plan for the user before moving on**, e.g.:
```
Target: US adults 25-54 who manage a team of 5+ people.
- Age 25-54, US residence  -> Prolific filters (Step 4)
- Manages a team of 5+      -> no filter exists; in-survey screening question
                               (expect ~40% screen-out -> over-recruit)
```

**Consider an attention check while you're in the instrument.** A strong
data-quality lever is an instructed-response or attention-check item in the
survey itself (e.g. "Select 'Somewhat agree' to show you're reading"), which
uses the same navigation machinery as screening. It gives you a clear signal
for spotting low-effort responses when you analyze the data. Propose one for any
study of meaningful length or payment.

### Step 3: Determine sample size and payment

Help the user think through these decisions. Note the dependencies from Step 2:
if the population is defined by filter segments, the sample size is *derived*
from those segments; if the survey screens people out, size the recruit to the
**screen-out-adjusted** number.

**If the user doesn't know how many to survey**, don't wait for a number — help
them derive one. Ask what analysis or decision the study feeds, then propose an
N from the rules of thumb below and explain the tradeoff. For AI-simulation
users migrating to human studies, note that human samples need real N for
statistical power (unlike AI personas).

**Pilot before you scale.** For any study of meaningful size or cost, strongly
recommend a small paid pilot first (e.g. 5-10 participants) to validate that the
survey is clear, timing is realistic, and screening/attention checks behave as
intended — *then* launch the full sample. Spending the full budget before
confirming the instrument works is the most common expensive mistake. This
mirrors the pilot-then-scale approach used throughout EDSL studies.

**Check the account and participant limit before proposing an N.**

```python
settings = coop.get_prolific_study_settings()
# settings["key_source"]: "ep" (Expected Parrot's Prolific account) or "user_key" (their own key)
# settings["participant_limit"] applies only if settings["participant_limit_applies"]
```

- **Expected Parrot's account** (`participant_limit_applies` is true): recruitment
  is paid in credits, and each study can recruit at most `participant_limit`
  participants. Tell the researcher both up front.
- **Their own Prolific key:** Prolific bills them directly, so recruitment costs
  no credits, and there is no participant limit. AI-interviewer runtime is
  still paid in credits.
- If the design needs more participants than the limit (after the scenario and
  screen-out adjustments below), say so before drafting anything. Offer two
  options: reduce the sample, or email info@expectedparrot.com to request a
  higher limit. A request isn't a raise: before creating the study, call
  `get_prolific_study_settings()` again and go ahead only once it shows the
  higher limit. **Never split one sample across several studies to get around
  the limit.**

**Sample size (`num_participants`)**
- Ask the user what kind of analysis they plan to do.
- For pilot testing or qualitative exploration: 10-30 participants.
- For detecting moderate effect sizes in simple comparisons: 50-100 per group.
- For surveys with many subgroups or small effects: 200+ per group.
- If the survey uses `Scenario` lists to show different stimuli, participants are randomly assigned across scenarios. Factor this into the total count: `num_participants = participants_per_scenario * num_scenarios`.
- Expect some attrition (~5-15%). Over-recruit slightly to compensate.

**Estimated completion time (`estimated_completion_time_minutes`)**
- Estimate from the survey's structure using the rules of thumb below — count
  the questions by type and add reading/orienting time.
- Rule of thumb: ~30 seconds per simple multiple-choice question, ~1-2 minutes per free-text question.
- Add 1-2 minutes for reading instructions and orienting.
- Round up to be generous - underestimating means participants are underpaid for
  their time, which hurts participant experience.

**Payment (`participant_payment_cents`)**
- Prolific enforces a **minimum of $8.00 USD/hour**. The system will reject studies below this.
- The validation formula: `(participant_payment_cents / 100) / (estimated_completion_time_minutes / 60) >= 8.0`
- **Recommended rate: $12-15 USD/hour** for good data quality and fast recruitment.
- Quick calculation to help the user:
  - 5-minute study at $12/hr = 100 cents ($1.00)
  - 10-minute study at $12/hr = 200 cents ($2.00)
  - 15-minute study at $12/hr = 300 cents ($3.00)
  - 20-minute study at $12/hr = 400 cents ($4.00)
- Formula: `payment_cents = round(estimated_minutes * (hourly_rate / 60) * 100)`
- The total study cost includes Prolific's platform fee on top of participant payments. Use `calculate_prolific_study_cost` (below) to get the actual amount that will be charged before spending anything.

**Calculate and present the actual cost** before proceeding. Use `calculate_prolific_study_cost` to get the real total (including Prolific's platform fee) before any money is spent:

```python
from edsl import Coop
coop = Coop()

cost = coop.calculate_prolific_study_cost(
    participant_payment_cents=200,
    num_participants=100,
    estimated_completion_time_minutes=10,
)
# cost["cost_cents"]   — total charge in cents (participants + platform fee)
# cost["cost_credits"] — same amount in EP credits
# cost["is_underpayment"] — True if below $8.00/hr minimum
# cost["underpayment_warning"] — warning message if is_underpayment is True

print(f"Total cost: ${cost['cost_cents'] / 100:.2f} ({cost['cost_credits']} EP credits)")
if cost["underpayment_warning"]:
    print(cost["underpayment_warning"])
```

### Add AI-interviewer runtime cost when applicable

`calculate_prolific_study_cost(...)` calculates recruitment and participant
payment only. It does not accept a human-survey UUID and cannot detect whether
the survey contains a `QuestionInterview`. Before calling its result the total,
inspect the deployed instrument and determine whether each participant will
complete an AI-led interview.

For an interview study, obtain the **current authoritative AI-interviewer rate
in credits per participant-minute** from the live product pricing or deployment
cost surface. Never hard-code or recall this rate from memory. Calculate:

```text
AI-interviewer credits = current credits/minute x estimated interview minutes x participants
Combined credits = Prolific recruitment credits + AI-interviewer credits
```

Use the expected interview duration, not the total survey duration, unless the
entire study is the interview. For multiple interviews, sum their expected
minutes per participant. If routing means only a fraction of respondents enter
an interview, state and apply that assumption explicitly.

Present three separate lines: Prolific recruitment subtotal, AI-interviewer
runtime estimate, and combined expected credits. If an authoritative current
interviewer rate is not available, state that the recruitment subtotal is **not
an all-in estimate** and stop before draft creation or publication until the
runtime price can be confirmed. Never silently report recruitment cost alone
as the total for an AI-interview study.

Keep the all-in estimate in `required_credits` for the later publication gate:

```python
recruitment_credits = cost["cost_credits"]
interviewer_credits = (
    current_credits_per_minute
    * estimated_interview_minutes
    * num_participants
)
required_credits = recruitment_credits + interviewer_credits
```

For a study without an AI interview, set
`required_credits = cost["cost_credits"]`. On the researcher's own Prolific key,
leave recruitment out: `required_credits` is the AI-interviewer credits only (0
without an interview), and present recruitment as billed by Prolific.

Present a cost summary like:
```
Sample size:        100 participants
Est. completion:    10 minutes
Payment per person: $2.00 (= $12.00/hr)
Total cost:         $XX.XX (including Prolific platform fee)
AI interviewer:     XXXX credits (rate x interview minutes x participants)
Combined expected:  XXXX credits
EP credits needed:  XXXX
```

### Step 4: Propose, explain, and confirm filters (before creating the study)

Filters control **who is eligible** to take the study. This is a required
collaborative step, not a silent one. **Always propose the filters you intend
to use, explain in plain language what each one does, and get the user's
explicit confirmation before creating the study.** Assume the user may not be
familiar with Prolific — err on the side of explaining.

This turns the population plan from Step 2 into concrete filter objects. Do it
**before** Step 5 so the confirmed filters can be passed directly into
`create_prolific_study(..., filters=[...])`. If the study has no eligibility
requirements, confirm that with the user ("open to all Prolific participants?")
and skip to Step 5.

#### 4a. Always fetch the live filter list first

The live `list_prolific_filters()` output is the **source of truth** for what is
available. This documentation is never guaranteed to be exhaustive, and the
filter set may change from time to time, so do not rely on a hardcoded list.
Always call `list_prolific_filters()` and inspect what is actually available
before proposing anything:

```python
from edsl import Coop
coop = Coop()

filters = coop.list_prolific_filters()
filters.table()                 # display all currently-available filters

# Inspect one filter to see its type and valid options/range
filters.find("age")                             # range filter (min/max)
filters.find("employment-status")               # select filter (option labels)
```

Each filter is one of two types:
- **range** — takes `min=` and `max=` integers (e.g. `age`, `approval_rate`).
- **select** — takes `values=[...]` as a list of the option **labels** exactly
  as shown in `select_filter_options` (EDSL maps labels to Prolific's internal
  indices for you).

#### 4b. Filter categories (illustrative, NOT exhaustive)

The catalogue is large (dozens of filters). The groups below show the *kinds* of
targeting available so you know what to reach for — they are **not the source of
truth** and are not guaranteed to be complete. The live `list_prolific_filters()`
output is authoritative and may contain filters (or options per filter) not
listed here. Always verify exact ids and option labels against it.

Some ids are irregular — they are slugs derived from Prolific's own filter
titles and are sometimes malformed (e.g. `relationshipmarital-status`, from
"Relationship/Marital status", has no hyphen where you'd expect one). **Copy
ids verbatim from `list_prolific_filters()`; never normalize, correct, or guess
them.** A "tidied-up" id will not match and the filter will fail at runtime.

Almost all filters are **select** type. Only three are **range**: `age`,
`approval_rate`, `approval_numbers`.

- **Data quality (range):** `approval_rate`, `approval_numbers` — see below.
- **Core demographics:** `age`, `sex`, `gender`, `ethnicity` /
  `ethnicity-simplified`, `sexual-orientation`, `cisgender-and-transgender`,
  `lgbtq`, `gender-identity-non-binary-only`, `religious-affiliation`.
- **Geography & nationality:** `current-country-of-residence`, `nationality`,
  `country-of-birth`, `current-us-state-of-residence`,
  `current-uk-area-of-residence`, `nationality-uk`.
- **Language:** `first-language`, `primary-language`, `fluent-languages`.
- **Education:** `highest-education-level-completed`, `student-status`,
  `undergraduate-year-of-study`, `degree-subject`, `international-students`,
  `studying-abroad`, `further-educational-study`.
- **Work & industry:** `employment-status`, `employment-sector`, `industry`,
  `industry-role`, `company-type`, `work-function`, `work-role`,
  `employment-role`, `years-of-work-experience`.
- **Household & socioeconomic:** `household-income-usd-us-participants-only`,
  `household-income-gbp`, `socioeconomic-status`, `household-size`,
  `number-of-children`, `relationshipmarital-status`, `property-type`,
  `car-ownership`, `pets`.
- **Lifestyle & interests:** `diet`, `diet-restriction`, `physical-activity`,
  `weekly-exercise`, `video-games`, `online-shopping-frequency`,
  `team-sports`, `experience-with-musical-instruments`, etc.
- **Identity & service:** `military-veteran`, `active-military-service-member`,
  `us-political-affiliation`, `vision`, `mixed-ethnic-background`.
- **Targeting a known set:** `custom_allowlist` — restrict to a specific list of
  participant IDs.

**Quality filters worth proposing proactively.** Beyond demographics, Prolific
offers filters that protect data quality. Unless the user has a reason not to,
consider proposing:
- `approval_rate` with a floor (e.g. `min=95`, often `min=98` or `99`) so you
  only recruit reliable participants. Explain it simply: "This only lets in
  people whose past submissions were approved at least 95% of the time — it
  filters out low-effort respondents."
- `approval_numbers` with a small `min` (e.g. `min=10`) to avoid brand-new
  accounts, if that matters for the study.

#### 4c. Present a proposal and confirm

Show the user a short, plain-language summary before building anything, e.g.:

```
Proposed eligibility filters:
- Age 25-45           -> only participants aged 25 to 45
- Lives in US or UK   -> current country of residence is United States or United Kingdom
- Approval rate >= 95 -> only reliable participants (>=95% of past studies approved)

More restrictive filters = a smaller eligible pool and slower recruitment.
Do these look right, or would you like to adjust?
```

Wait for confirmation. Only after the user agrees, build the filter objects.
Hold them for Step 5, where they are passed into `create_prolific_study`:

```python
age_filter = filters.create_study_filter("age", min=25, max=45)
country_filter = filters.create_study_filter(
    "current-country-of-residence",
    values=["United States", "United Kingdom"],   # exact option labels
)
quality_filter = filters.create_study_filter("approval_rate", min=95, max=100)

confirmed_filters = [age_filter, country_filter, quality_filter]
```

Note: More restrictive filters = slower recruitment and a smaller eligible pool.
If recruitment stalls, loosening a filter is the first thing to try.

### Step 5: Create the Prolific study

Create the study, passing the filters confirmed in Step 4. This creates the
study in **draft** mode — no money is charged until you publish (Step 6).

**Participant-facing title and description (required care).**
`create_prolific_study`'s `name` and `description` are what Prolific
**participants** see when deciding whether to take the study. They are **not**
the Coop/humanize labels from Step 1.

| Field | Audience | Purpose |
|-------|----------|---------|
| `humanize(... human_survey_name=..., survey_description=...)` | Researcher (Coop) | Find the deploy later |
| `create_prolific_study(... name=..., description=...)` | Prolific participants | Listing copy on Prolific |

**Do:**
- Write a short, plain title that says what the task *feels like* to a participant (topic + format), e.g. "Share your recent online shopping experience".
- Keep the description concrete: roughly how long, what they'll do (survey / chat interview / voice interview), any special requirements (mic, desktop).
- Propose `name` and `description` to the user and get a quick OK before creating the study.
- In the same proposal, state the selected submission approval policy. If the researcher asked for manual review (or already has), state **"Submission approval: manual review"**: participants are paid when the researcher approves their submissions, or when Prolific automatically approves them 21 days after completion. Otherwise, state **"Submission approval: automatic (default)"**: submissions are approved and participants paid as soon as they enter the completion code. Add one line on the alternative policy. Don't ask a separate question. Pass `approval_mode="manual"` only if the researcher asks for manual review (or already has); otherwise leave it out.

**Do not:**
- Reuse `human_survey_name`, topic folder names (`topic_customer-churn-...`), job ids (`job_a`), internal codes, or dates as the Prolific title.
- Use placeholders like `"Study Title Shown to Participants"`, `"My Study"`, or the research hypothesis / brand strategy jargon.
- Spoil the study (don't put the experimental manipulation or the "real" research question in the public title if that would bias answers).

```python
from edsl import Coop
coop = Coop()

study = coop.create_prolific_study(
    human_survey_uuid=human_survey_uuid,
    # Participant-facing — NOT the Coop human_survey_name
    name="Share your recent online shopping experience",
    description=(
        "A short survey about how you shop online. "
        "About 10 minutes. Desktop or mobile is fine."
    ),
    num_participants=100,
    estimated_completion_time_minutes=10,
    participant_payment_cents=200,
    filters=confirmed_filters,   # from Step 4; omit or use [] if none
    # Optional:
    # device_compatibility=["desktop", "mobile", "tablet"],  # default: all three
    # peripheral_requirements=["audio"],  # options: audio, camera, download, microphone
    # approval_mode="manual",  # only if the researcher asked for manual review
)

study_id = study["study_id"]
# study["total_cost_cents"] shows the total cost including Prolific fees
```

After creation, share the total cost with the user:
```python
print(f"Total study cost: ${study['total_cost_cents'] / 100:.2f}")
```

The response also includes an `admin_url` you can share with the user to view
and manage the study:
```python
print(study["admin_url"])
```

**If creation is refused:**
- *Over the participant limit:* the error names the limit. Offer the options from
  Step 3; never split the sample across studies.
- *The survey's Prolific key was deleted:* ask the researcher to add a key for the
  same Prolific workspace on the Keys page, then click Reconnect on the survey's
  Prolific studies page, and try again.

**Changed your mind on filters after creation?** While the study is still a
draft you can revise them with `update_prolific_study(human_survey_uuid,
study_id, filters=[...])`. Re-confirm with the user first, as in Step 4. The
same goes for the approval policy: `update_prolific_study(human_survey_uuid,
study_id, approval_mode="manual")` (or `"automatic"`) switches it while the
study is a draft. It can't change after publishing.

### Step 6: Publish the study

Publishing is a separate, irreversible spending decision. **Do not publish in
the same turn or command batch that creates or updates the draft.** First show
the researcher the exact draft they are authorizing, including its
participant-facing name, participant count, payment per participant, estimated
completion time, filters, submission approval (`get_prolific_study(...)["approval_mode"]`),
and exact total cost.

Then use `AskUserQuestion` to ask one decision only: whether to publish this
specific Prolific study at the displayed total cost. Include options such as
`Publish Prolific study` and `Keep as draft`. **Stop and wait for the answer.**
Do not call `publish_prolific_study` unless the researcher gives a fresh,
affirmative confirmation after seeing that exact summary and cost.

Authorization to create the draft, approve filters, approve survey content,
run inference, publish a report or Coop object, or take any other action does
not authorize Prolific publication. Ambiguous instructions such as "publish
it" do not count, even if Prolific publication was discussed earlier. Ask the
scoped `AskUserQuestion` and wait. If the draft's cost, sample, payment,
duration, filters, approval policy, or participant-facing copy changes after confirmation,
display the revised summary and obtain a new confirmation.

First run the preflight check. It confirms the study is still an unpublished
draft, the deployed survey matches `survey` (the Survey you humanized in Step
1), the payment meets Prolific's minimum, and the balance covers
`required_credits` from Step 3. For an AI interview study, pass the all-in
estimate; without `required_credits` the check costs recruitment only:
```python
check = coop.preflight_prolific_study(
    human_survey_uuid,
    study_id,
    expected_survey=survey,
    required_credits=required_credits,
)
print(check["ready"], check["blockers"])
print(f"Need {check['required_credits']} credits, have {check['balance_credits']}")
```

If `check["ready"]` is false, show the researcher each blocker and stop; do not
publish. A passing check neither reserves funds nor authorizes spending. On the
researcher's own key, the check doesn't cost recruitment in credits
(`check["key_source"] == "user_key"`).

If publication is refused for exceeding the participant limit (the error names
the limit), offer the options from Step 3; never split the sample across
studies.

Only after the preflight passes and the researcher explicitly selects the
publication option may you run the publication call in a new command. Pass the
same arguments: publication reruns the preflight and raises `CoopValueError`
instead of publishing if any blocker appears.

```python
# This makes the study live and charges credits
coop.publish_prolific_study(
    human_survey_uuid,
    study_id,
    expected_survey=survey,
    required_credits=required_credits,
)
```

### Step 7: Monitor and manage

**If you don't have a `study_id`** — the user is returning to a study from an
earlier session, or several studies were created against the same survey — list
everything attached to the human survey and pick from there:

```python
studies = coop.list_prolific_studies(human_survey_uuid)
for s in studies:
    print(
        f"{s['study_id']}  {s['status']:<12} {s['name']}  "
        f"n={s['num_participants']}  ${s['total_cost_cents'] / 100:.2f}"
    )
```

Each dict has `study_id`, `name`, `status` (e.g. `"UNPUBLISHED"`, `"ACTIVE"`),
`num_participants`, `participant_payment_cents`,
`estimated_completion_time_minutes`, and `total_cost_cents` — enough to tell the
studies apart and confirm with the user which one they mean.

Once you know which study you're working on, call
`get_prolific_study(human_survey_uuid, study_id)` for the full record.

```python
# Check study status and details
coop.get_prolific_study(human_survey_uuid, study_id)

# Pause/resume/stop as needed
coop.pause_prolific_study(human_survey_uuid, study_id)
coop.resume_prolific_study(human_survey_uuid, study_id)
coop.stop_prolific_study(human_survey_uuid, study_id)

# Delete a draft study (only works for unpublished studies)
coop.delete_prolific_study(human_survey_uuid, study_id)
```

**If recruitment stalls or fills only partially** — common with tight filters:
- Check progress with `get_prolific_study(...)` (how many places are filled vs.
  outstanding). A study that hasn't moved in a while usually has too small an
  eligible pool.
- **Loosen the constraints.** The most restrictive filter is the usual culprit
  — widen an age range, add a country, or drop a non-essential criterion.
  Re-confirm changes with the user (as in Step 4), then apply with
  `update_prolific_study(..., filters=[...])`.
- **Adjust the target count.** `update_prolific_study(..., num_participants=...)`
  can raise or lower the sample. Lowering to what you can realistically fill is
  a valid way to close out a partially-filled study. On Expected Parrot's
  account, raising it is subject to the participant limit from Step 3.
- **Pause vs. stop.** `pause` halts new submissions but keeps the study open to
  resume later (use while you decide or edit). `stop` ends recruitment
  permanently — use only when you're done. Prefer pause when unsure.

```python
# Get responses from the Prolific study specifically
responses = coop.get_prolific_study_responses(human_survey_uuid, study_id)

# Or get ALL human responses (Prolific + direct link respondents)
all_human = coop.get_human_survey_responses(human_survey_uuid)
```

**Approving or rejecting submissions** depends on the study's approval mode.
With automatic approval (the default), submissions are approved and paid as
participants finish, and the researcher needs to do nothing. With manual review,
the researcher approves or rejects on the Prolific admin page (from
`study["admin_url"]`); anything left unreviewed is approved automatically 21 days
after completion. You do not need to walk the user through this — just point them
to the admin page if they ask.

## Key constraints and gotchas

Read [the constraints and gotchas reference](references/constraints.md) before creating or publishing a study.

## Decision checklist

Use [the Prolific decision checklist](references/decision-checklist.md) before creating or publishing a study.
