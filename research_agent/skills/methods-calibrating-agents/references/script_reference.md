# Script Reference: calibrate_agents.py

Located at `research_agent/skills/methods-calibrating-agents/scripts/calibrate_agents.py`.

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--target-csv` | Yes | -- | CSV with columns `question_name, option, probability` |
| `--trait-space-json` | Yes | -- | JSON mapping dimension names to lists of candidate values |
| `--survey-ep` | No | -- | Pre-built EDSL Survey (`.ep`). If omitted, questions are built from the target CSV. |
| `--output-dir` | No | `./calibration_output` | Directory for all outputs |
| `--model` | **Yes** | *(none)* | Model name; confirm a current one via `ep models`. Logprobs mode needs an OpenAI model. |
| `--method` | No | `logprobs` | `logprobs` or `sampling` — how to estimate each agent's distribution |
| `--n-samples` | No | 30 | Samples per agent in sampling mode |
| `--metric` | No | `kl` | Divergence metric for individual agent ranking: `kl`, `tv`, or `chi2` |
| `--top-k` | No | 5 | Number of top individual agents to show in diagnostics |
| `--max-candidates` | No | 0 | Random-subsample the grid if it exceeds this size (0 = no limit) |

## Resume Support

The script checkpoints after each step. If interrupted, re-run the same command and it will skip completed steps:

- Step 1 skipped if `candidate_grid.ep` exists
- Step 2 skipped if `logprob_results.ep` or `sampling_results.ep` exists
- Steps 3-4 always re-run (fast, no API calls)
