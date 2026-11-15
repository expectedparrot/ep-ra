# OpenCode

## Install

Install OpenCode and sign in to your model provider. From the EP Agent
checkout, run the universal installer and choose OpenCode:

```bash
./install.sh
```

The installer launches EDSL's `ep auth login` flow when an Expected Parrot key
is not already configured, prepares the locked Python and EDSL runtime, and
adds EP Agent skills to `~/.config/opencode/skills/`. Start OpenCode in your
research project and describe the task. Rerun the installer after updating the
checkout.

For a release installation, add the EP Agent skills catalog URL to your
OpenCode configuration, replacing `<release-tag>` with the version you want:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": [
    "https://raw.githubusercontent.com/expectedparrot/ep-ra/<release-tag>/research_agent/skills/"
  ]
}
```

For EDSL commands, activate the checkout's `.venv` in the shell that launches
OpenCode. The installer prints the activation command.
