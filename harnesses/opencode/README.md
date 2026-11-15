# OpenCode

## Install

Install OpenCode and sign in to your model provider. From the EP Agent
checkout, run:

```bash
./installers/install-opencode.sh
```

The installer adds EP Agent skills to `~/.config/opencode/skills/` and prepares
the locked Python and EDSL runtime. Add `--skills-only` to skip the runtime.
Start OpenCode in your research project and describe the task. Rerun the
installer after updating the checkout.

For a release installation, add the EP Agent skills catalog URL to your
OpenCode configuration, replacing `<release-tag>` with the version you want:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": [
    "https://raw.githubusercontent.com/expectedparrot/ep-agent/<release-tag>/research_agent/skills/"
  ]
}
```

## Expected Parrot access

EDSL-backed research requires an Expected Parrot API key. Export
`EXPECTED_PARROT_API_KEY` before launching OpenCode, or configure the EDSL CLI
from the checkout:

```bash
uv run --frozen --no-dev ep auth login --api_key <your-key>
```

For EDSL commands, activate the checkout's `.venv` in the shell that launches
OpenCode. The installer prints the activation command.
