## Key constraints and gotchas

- **Minimum payment: $8.00/hr.** The `create_prolific_study` and `update_prolific_study` methods will raise `CoopValueError` if below this threshold.
- **Publishing is irreversible** in terms of cost - you cannot delete a published study, only stop it.
- **Submission approval is fixed at publish.** Studies default to automatic approval; `approval_mode` can be changed with `update_prolific_study` only while the study is a draft.
- **Filter IDs** use inconsistent naming (dashes vs underscores). The `find()` method handles both, so `"current_country_of_residence"` and `"current-country-of-residence"` both work.
- **Filters are live-defined.** This doc's filter list is not guaranteed exhaustive and the set may change from time to time — always call `list_prolific_filters()` at runtime rather than trusting a hardcoded list. Select filters take option **labels** (as shown in the filter's `select_filter_options`), not raw indices.
- **Always confirm filters with the user** before creating the study (see Step 4). Explain what each filter does in plain language.
- **Prolific `name` / `description` are participant-facing.** Never copy Coop `human_survey_name` or internal study labels into them (see Step 5).
- **Credits** are required in your Expected Parrot account to publish studies on Expected Parrot's Prolific account. On the researcher's own Prolific key, Prolific bills recruitment directly; only AI-interviewer runtime uses credits.
- **Participant limit.** A study on Expected Parrot's Prolific account can recruit at most the researcher's participant limit, from `get_prolific_study_settings()`. Creating, raising or publishing past it is refused. Never split one sample across several studies to get around it; the researcher can email info@expectedparrot.com to request a higher limit. Studies on their own key have no limit.
- **Account-required surveys.** If the human survey requires sign-in
  (`survey.login_required`), every Prolific participant must sign in to an
  Expected Parrot account, or create one, before answering, and their username
  is recorded with the response. Confirm this with the researcher before
  recruiting: it adds a step for participants and ties responses to accounts.
- **Respect participant anonymity.** Prolific participants are pseudonymous. Do
  not ask for personally identifying information (real name, email, address,
  etc.) in the survey unless there is a specific, disclosed reason — it violates
  participant expectations and platform norms.
- **Longitudinal / multi-wave studies** (re-contacting the same participants
  across sessions) are a distinct Prolific workflow and are **not covered by
  this skill**; setting one up needs Prolific-side configuration beyond these
  methods.
