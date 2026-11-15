## Decision checklist

Before launching, confirm these with the user:
1. Survey content is finalized and tested (use a runway preview from `skill:edsl-human-survey-preview`, then the live `preview_url`)
2. Target population defined; each criterion mapped to a filter or in-survey screener (Step 2)
3. Attention check included for studies of meaningful length/payment (Step 2)
4. Sample size is justified for the analysis plan, and adjusted for expected screen-out
   - On Expected Parrot's Prolific account, it is within the current participant limit returned by `get_prolific_study_settings()`. If a higher limit was requested, confirm with `get_prolific_study_settings()` that it has been granted before continuing; never split across studies to fit
5. Payment rate is fair ($12+/hr recommended)
6. Completion time estimate is realistic (estimated from the survey's question count and types)
7. Eligibility filters proposed, explained, and confirmed with the user (Step 4)
8. Prolific `name` and `description` are plain, participant-facing listing copy — confirmed with the user; not Coop/internal labels (Step 5)
9. A small paid pilot is run before the full sample, for any nontrivial study (Step 3)
10. Submission approval stated: automatic (default), or manual review if the researcher asked, with the 21-day automatic approval explained
11. Total cost is acceptable
12. Credits balance is sufficient (recruitment counts only on Expected Parrot's account)
13. No PII requested in the survey unless disclosed and justified
