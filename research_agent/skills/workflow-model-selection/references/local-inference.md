# User-owned OpenAI-compatible endpoints

Use when the user explicitly wants local/self-hosted inference through Ollama,
LM Studio, llama.cpp, vLLM, SGLang, or another OpenAI-compatible server. Confirm
the endpoint and exact model identifier from the user or that server's model
listing; the Expected Parrot remote catalog does not list arbitrary local aliases.
Do not silently substitute a hosted model if connection or inference fails.

Create a portable model list with the supported CLI:

```bash
ep models create --service openai_compatible --model <server-model-id> \
  --base-url http://127.0.0.1:8000/v1 --output local-models.ep
```

For authentication, add `--api-key-env LOCAL_MODEL_API_KEY`; the package stores
the variable name, not its secret value. Use the actual server URL and keep the
model list as the effective run configuration.

```bash
ep run --jobs jobs.ep --model_list local-models.ep --local \
  --max-concurrency 4 --api-timeout 300 --output data/local-results.ep
```

This is an execution example after the study plan authorizes the endpoint and
scope. `--model_list` replaces embedded models. Configure the study's run target
with these options before using its phase command; do not run both this example
and the target. `--local` disables Expected Parrot inference, not the external
server's own billing. Account for any endpoint charges and local capacity.
Match concurrency to server slots; `--api-timeout` bounds individual local API
requests and differs from a remote per-interview `--task-timeout`.

If a connection check is needed, inspect the endpoint's `/models` first. A
one-question smoke still performs inference; include it in the approved scope.
Keep the model, URL, parameter settings, and saved Results provenance. Inspect
completion counts and partial-result warnings before claiming a complete run.

## Different providers or parameters in one model list

For a hosted comparison whose entries require different services or parameters,
repeat `--model-spec` with catalog-confirmed values:

```bash
ep models create \
  --model-spec '{"model":"<first-model>","service":"<first-service>"}' \
  --model-spec '{"model":"<second-model>","service":"<second-service>","parameters":{"temperature":0.5}}' \
  --output model-list.ep
```

Use only parameters supported by the chosen models. This avoids writing Python
solely to construct a heterogeneous list. Validate requested provider/model
pairs through [requested-models.md](requested-models.md) before costing.

Source: EDSL `docs/en/latest/local_openai_compatible.mdx` and CLI model specs.
