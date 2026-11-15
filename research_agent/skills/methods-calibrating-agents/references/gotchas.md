# Gotchas — Calibrating Agent Mixtures

## 1. OpenAI models only for logprobs

Logprobs are an OpenAI-specific API feature. Pass an OpenAI model (`service: openai` in `ep models`) for logprobs mode. Anthropic and other providers do not expose log probabilities through EDSL. For non-OpenAI models, use `--method sampling`.

## 2. Top-5 token limit in logprobs

OpenAI returns logprobs for at most 5 top tokens. If a question has more than 5 options, some options may have no logprob data. Use epsilon smoothing (the script defaults to 1e-10) and be aware that divergence scores will be approximate. For questions with many options, prefer sampling mode.

## 3. Sampling mode cost

With sampling, total API calls = n_agents x n_questions x n_samples. For 100 agents, 2 questions, and 30 samples, that is 6,000 calls. Use `--max-candidates` to subsample the grid, or start with a small `--n-samples` (e.g., 10) for exploration and increase for final calibration.

## 4. Grid size scaling

A grid of 5 dimensions x 5 levels = 3,125 candidates. With logprobs at ~$0.002 per API call (mid-tier OpenAI model, short prompt), that is ~$6.25 for a single question. With sampling at n=30, that is ~$187.50 for one question. Use `--max-candidates` to subsample, or reduce levels.

## 5. Persona construction matters

The persona string is what the model reads. Trait values must be natural-language phrases that compose into a coherent character description. Test a few agents manually before running the full grid.

## 6. Normalization

Logprobs may not sum to 1.0 across only the valid option tokens (probability mass leaks to other tokens). Always renormalize the extracted distribution before computing divergence.

## 7. Temperature must be 1

Lower temperatures sharpen the distribution, making all agents look more similar. `temperature=1` gives the model's natural distribution.

## 8. Target probabilities must sum to 1

The script validates this and raises an error if any question's probabilities are off by more than 0.01.

## 9. Sparse mixtures

In practice, the optimizer produces sparse solutions: out of hundreds of candidates, only 3-10 agents typically get nonzero weight. This is expected and desirable — it means the population can be approximated by a small number of "types."
