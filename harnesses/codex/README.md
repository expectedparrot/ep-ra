# Codex

## Install

Install Codex and sign in. From the EP Agent checkout, run:

```bash
./installers/install-codex.sh
```

The installer adds EP Agent skills to `~/.agents/skills/` and prepares the
locked Python and EDSL runtime. Add `--skills-only` to skip the runtime. Start
Codex in the project where you want to work and describe your research task.
Rerun the installer after updating the checkout.

You can also install the plugin through the Codex desktop app. Add the
Expected Parrot marketplace, select EP Agent, and follow its setup steps.

## Expected Parrot access

EDSL-backed research requires an Expected Parrot API key. Export
`EXPECTED_PARROT_API_KEY` before launching Codex, or configure the EDSL CLI from
the checkout:

```bash
uv run --frozen --no-dev ep auth login --api_key <your-key>
```

For research commands that use EDSL, activate the checkout's `.venv` in the
shell that launches Codex. The installer prints the activation command.
