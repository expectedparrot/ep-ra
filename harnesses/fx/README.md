# Vercel fx

## Install

From the EP Agent checkout, run the universal installer and choose Vercel fx:

```bash
./install.sh
```

If `fx` is missing, the installer uses Vercel's official installer. It also
prepares the locked EDSL runtime, verifies the required Expected Parrot API key
(or guides you through login), and installs EP Agent's skills in `~/.fx/skills/`.

## Start

From the project where you want to work, run:

```bash
source /path/to/ep-ra/.venv/bin/activate && fx
```

If you have not connected a model provider, fx guides you through choosing one
and signing in on first launch. This is separate from the Expected Parrot key
configured during EP Agent installation.

For EDSL commands, activate the checkout's `.venv` in the shell that launches
fx:

```bash
source /path/to/ep-ra/.venv/bin/activate
```
