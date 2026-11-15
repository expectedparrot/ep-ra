# Study Structure for Calibrating Agents

When used in a study project, files are organized as follows:

```
study_x/
  data/
    raw/
      target_distribution.csv      <- user provides this
      trait_space.json              <- agent generates from discussion
    cooked/
      agent_distributions.csv      <- output: per-agent predicted distributions
  computed_objects/
    calibration/
      candidate_grid.ep            <- output: full agent grid
      logprob_results.ep           <- output: EDSL results (logprobs mode)
      sampling_results.ep          <- output: EDSL results (sampling mode)
      calibrated_mixture.ep        <- output: agents with nonzero weight + _weight trait
      mixture_weights.csv          <- output: weights and traits
      calibration_summary.json     <- output: metadata and fit diagnostics
  edsl_jobs/
    job_calibration/
      run_job.py                   <- calls calibrate_agents.py or imports it
  analysis/
    plot_calibration.py            <- visualize mixture fit vs target
  writeup/
    plots/
      calibration_fit.png          <- mixture vs. target distributions
```

The calibrated mixture can be reused by recording the predecessor study path and loading it in place. If portability is required, copy only the mixture into `refs/` and record its provenance:

```python
from edsl import AgentList
mixture = AgentList.git.load("refs/study_x/computed_objects/calibration/calibrated_mixture.ep")
```
