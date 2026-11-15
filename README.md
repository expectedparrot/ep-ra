# EP Agent

EP Agent provides research skills and specialist workflows for Claude Code,
Codex, OpenCode, Pi, and Google Antigravity. It helps plan and carry out studies
with EDSL and create evidence-based reports.

## Requirements

- macOS, Linux, or WSL
- One supported AI harness, installed and signed in
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- An Expected Parrot API key (required during installation)
- A model provider account configured in your chosen harness

## Install

Clone this repository and run the universal installer:

```bash
git clone https://github.com/expectedparrot/ep-ra.git
cd ep-ra
./install.sh
```

The installer lets you select Claude Code, Codex, OpenCode, Pi, or Google
Antigravity. It installs the locked EDSL runtime, verifies an existing Expected
Parrot API key or guides you through EDSL's `ep auth login` flow, then installs
the selected harness adapter. The key is required; setup stops if authentication
cannot be verified.
If you need a key, [create one in your Expected Parrot account](https://www.expectedparrot.com/getting-started/edsl-api-keys).

Choose your harness guide:

| Harness | Installer | Guide |
|---|---|---|
| Claude Code | Select it in the installer | [Claude Code](harnesses/claude-code/README.md) |
| Codex | Select it in the installer | [Codex](harnesses/codex/README.md) |
| OpenCode | Select it in the installer | [OpenCode](harnesses/opencode/README.md) |
| Pi | Select it in the installer | [Pi](harnesses/pi/README.md) |
| Google Antigravity | Select it in the installer | [Google Antigravity](harnesses/antigravity/README.md) |

## Optional Anthropic document skills

The PDF, DOCX, PPTX, and XLSX skills are not bundled with EP Agent. Claude
Code users can install Anthropic's official document-skills plugin separately:

```text
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

This installs the skills from Anthropic's marketplace, outside the EP Agent
checkout. See the [official Anthropic skills repository](https://github.com/anthropics/skills)
for other Anthropic-supported ways to use them.

The installer does not install the AI harness or configure model-provider
sign-in. Authenticate with your selected provider using that harness's normal
sign-in flow.

## Start a research session

Start your chosen harness in the project where you want to work, then describe
the research question and the result you need. The installed skills guide study
planning, approval checkpoints, data collection, analysis, and reporting.

For a full local session with the locked runtime, use the launcher for your
harness from this checkout:

```bash
./ep-cli.sh  # Claude Code
./ep-pi.sh   # Pi
```

These launchers set harness permission options so the agent can carry out its
workflow. Use them only in a checkout and workspace you trust. The agent still
uses separate approval checkpoints for paid research and consequential actions.

For Codex and OpenCode, start the harness in your research project after
installing the skills. For EDSL commands, activate the installed runtime in
that shell first with `source /path/to/ep-ra/.venv/bin/activate`.

## Update or uninstall

Pull the latest repository version and rerun the same installer to update the
installed skills or plugin. The installer replaces only EP Agent-managed skill
directories.

To remove the installed skills, delete the EP Agent skill directories from the
location listed by your harness guide. To remove a Claude Code plugin, use its
plugin management commands. To remove Pi, use `pi remove` with the installed
package identifier.

## License

EP Agent is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE).
Commercial use requires separate permission from Expected Parrot.
