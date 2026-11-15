# Google Antigravity CLI

## Install

From the EP Agent checkout, run the universal installer and choose Google
Antigravity CLI:

```bash
./install.sh
```

If `agy` is missing, the installer uses Google's official CLI installer. It
also prepares the locked EDSL runtime, verifies the required Expected Parrot
API key (or guides you through login), and installs EP Agent's skills globally
in `~/.gemini/config/skills/`. It adds read-only sandbox access to this
checkout's virtual environment and its Python runtime so EP commands can run
without repeated access prompts. It also allows sandboxed network requests to
`expectedparrot.com` and its subdomains for EP API access. Other Antigravity
sandbox protections remain enabled.

## Start

From the project where you want to work, run:

```bash
source /path/to/ep-ra/.venv/bin/activate && agy
```

On first launch, sign in with your Google account when Antigravity prompts you.
The desktop app is separate; download it from [Google Antigravity](https://antigravity.google/download).

Antigravity does not interpret EDSL's `PRESENT_FILE` marker as an open-file
command. EP Agent validates presented files and returns their project-relative
paths so you can open them in Antigravity's file view.

Google's [Agent Skills documentation](https://antigravity.google/docs/skills)
covers skill discovery. See the [Antigravity IDE side panel guide](https://antigravity.google/docs/agent-side-panel)
for reviewing files and artifacts.
