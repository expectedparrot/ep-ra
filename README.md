# EP Agent

EP Agent provides research skills and specialist workflows for Claude Code,
Codex, OpenCode, and Pi. It helps plan and carry out studies with EDSL and
create evidence-based reports.

## Requirements

- macOS, Linux, or WSL
- One supported AI harness, installed and signed in
- [uv](https://docs.astral.sh/uv/getting-started/installation/) to install the
  locked EDSL runtime (unless you choose a skills-only installation)
- An Expected Parrot API key for EDSL-backed research
- A model provider account configured in your chosen harness

## Install

Clone this repository, then run the installer for your harness from the
checkout root:

```bash
git clone https://github.com/expectedparrot/ep-agent.git
cd ep-agent
./installers/install-codex.sh
```

Choose one installer:

| Harness | Installer | Guide |
|---|---|---|
| Claude Code | `./installers/install-claude-code.sh` | [Claude Code](harnesses/claude-code/README.md) |
| Codex | `./installers/install-codex.sh` | [Codex](harnesses/codex/README.md) |
| OpenCode | `./installers/install-opencode.sh` | [OpenCode](harnesses/opencode/README.md) |
| Pi | `./installers/install-pi.sh` | [Pi](harnesses/pi/README.md) |

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

By default, the installer also prepares the locked Python and EDSL runtime in
`.venv`. To install only the harness skills or plugin, use `--skills-only`:

```bash
./installers/install-codex.sh --skills-only
```

The installer does not install the AI harness or configure model-provider
sign-in. Authenticate with your selected provider using that harness's normal
sign-in flow.

## Configure Expected Parrot access

Provide your API key through the environment:

```bash
export EXPECTED_PARROT_API_KEY="<your-key>"
```

Alternatively, configure the EDSL CLI once from the checkout:

```bash
uv run --frozen --no-dev ep auth login --api_key <your-key>
```

Keep API keys in your environment or secret manager. Do not put them in this
repository or in a shared project configuration.

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
installing the skills. EDSL-backed workflows need the checkout's `.venv` on
`PATH`; the installer prints the activation command.

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
