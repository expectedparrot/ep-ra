# Claude Code

## Install

Install Claude Code and sign in to your model provider. From the EP Agent
checkout, run the universal installer and choose Claude Code:

```bash
./install.sh
```

The installer requires and verifies an Expected Parrot API key, installs the
locked Python and EDSL runtime, and adds the checkout as a Claude Code plugin
marketplace. Start a new Claude Code session after installation. Rerun the
installer after updating the checkout.

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

The installer guides you through creating an Expected Parrot key if needed and
stores it with the EDSL CLI. The GitHub plugin installation provides skills
and specialist instructions, but does not configure the local EDSL runtime or
API key.
