# Google Antigravity

## Install

Install [Google Antigravity](https://antigravity.google/download) first, then
install uv if it is not already available.

From the EP Agent checkout, run the universal installer and choose Google
Antigravity:

```bash
./install.sh
```

The installer prepares the locked EDSL runtime, verifies the required Expected
Parrot API key (or guides you through login), then installs EP Agent's skills
globally in `~/.gemini/config/skills/`. Restart Antigravity or reload its skills
to see them in the agent's Customizations panel.

Google account sign-in and model selection use Antigravity's normal setup.
Open a project folder in Antigravity, then describe the research task you want
to complete. Keep the EP Agent checkout available for its locked EDSL runtime;
activate its `.venv` in the shell used by Antigravity when running EDSL
commands outside the checkout.

Antigravity does not interpret EDSL's `PRESENT_FILE` marker as an open-file
command. EP Agent validates presented files and returns their project-relative
paths so you can open them in Antigravity's file view.

For EDSL commands, activate the checkout runtime in the shell that launches
Antigravity:

```bash
source /path/to/ep-ra/.venv/bin/activate
```

See Google's official [Agent Skills documentation](https://antigravity.google/docs/skills)
for skill discovery and the [Antigravity IDE side panel guide](https://antigravity.google/docs/agent-side-panel)
for reviewing files and artifacts.
