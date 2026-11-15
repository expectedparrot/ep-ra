# Survey review and execution lifecycle

After the saved `survey.ep` is built, give the researcher an inspection path
before publishing it or running respondents. For a web-form preview, load
`skill:edsl-human-survey-preview` and render the saved survey with runway.
Share the HTML file's path and expect to iterate: after each requested change,
rebuild the saved survey and re-render the preview. A draft preview is not a
reason to push the Survey to Expected Parrot.

Once the researcher confirms the survey content, determine the intended next
step if it is not already explicit: human respondents, AI simulation, or both.

- For human respondents, load `skill:edsl-human-survey` and confirm the
  deployment method before creating a live survey.
- For AI simulation, continue through the scaffold's cost and spend-approval
  phases.
- For both, preserve one approved survey source and use the separate human and
  simulation execution paths.

This review step does not override a Builder handoff. Builder editing requires
an explicitly approved remote push because the Builder operates on the linked
Expected Parrot object. Outside that exception, finish preview iterations
before requesting the publication decision owned by
`skill:edsl-object-publishing`.
