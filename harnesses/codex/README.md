# Codex

## Install

Install Codex and sign in. From the EP Agent checkout, run the universal
installer and choose Codex:

```bash
./install.sh
```

The installer launches EDSL's `ep auth login` flow when an Expected Parrot key
is not already configured, prepares the locked Python and EDSL runtime, and
adds EP Agent skills to `~/.agents/skills/`. Start Codex in the project where
you want to work and describe your research task. Rerun the installer after
updating the checkout.

You can also install the plugin through the Codex desktop app. Add the
Expected Parrot marketplace, select EP Agent, and follow its setup steps.

For research commands that use EDSL, activate the checkout's `.venv` in the
shell that launches Codex:

```bash
source /path/to/ep-ra/.venv/bin/activate
```
