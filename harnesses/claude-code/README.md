# Claude Code

## Install

Install Claude Code and sign in to your model provider. From the EP Agent
checkout, run:

```bash
./installers/install-claude-code.sh
```

The installer adds the checkout as a plugin marketplace and installs EP Agent.
Add `--skills-only` to skip the locked Python and EDSL runtime. Start a new
Claude Code session after installation. Rerun the installer after updating the
checkout.

To install from GitHub's plugin marketplace instead, use Claude Code's plugin
commands:

```text
/plugin marketplace add expectedparrot/ep-agent
/plugin install ep-agent@expected-parrot
```

For PDF, DOCX, PPTX, and XLSX support, install Anthropic's official document
skills separately:

```text
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

## Expected Parrot access

EDSL-backed research requires an Expected Parrot API key. Set
`EXPECTED_PARROT_API_KEY` in the environment before starting Claude Code, or
configure the EDSL CLI from the checkout:

```bash
uv run --frozen --no-dev ep auth login --api_key <your-key>
```

Keep the key in your environment or secret manager. The GitHub plugin
installation provides skills and specialist instructions; use the checkout
installer when you also need the locked local runtime.
