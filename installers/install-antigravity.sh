#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

ep_agent_setup_runtime "$@"
ep_agent_require_api_key

ep_agent_install_skills \
    "$HOME/.gemini/config/skills" \
    "$EP_AGENT_ROOT/research_agent/skills" \
    "$EP_AGENT_ROOT/harnesses/antigravity/skills"

printf '\nEP Agent skills are installed for Google Antigravity.\n'
printf 'This setup does not install the Antigravity app.\n'
if command -v agy >/dev/null 2>&1; then
    ep_agent_print_next_command agy
else
    printf 'Install Antigravity from https://antigravity.google/download\n'
    printf 'For terminal use, install its CLI with:\n'
    printf '  curl -fsSL https://antigravity.google/cli/install.sh | bash\n'
    printf 'Then, from the project where you want to work, run:\n'
    printf '  source "%s/.venv/bin/activate" && agy\n' "$EP_AGENT_ROOT"
fi
