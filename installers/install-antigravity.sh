#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

ep_agent_setup_runtime "$@"

if ! command -v agy >/dev/null 2>&1 && [[ ! -x "$HOME/.local/bin/agy" ]]; then
    if ! command -v curl >/dev/null 2>&1; then
        printf 'Install curl before installing Google Antigravity CLI.\n' >&2
        exit 127
    fi
    printf 'Installing Google Antigravity CLI...\n'
    curl -fsSL https://antigravity.google/cli/install.sh | bash
fi

if command -v agy >/dev/null 2>&1; then
    agy_command=agy
elif [[ -x "$HOME/.local/bin/agy" ]]; then
    agy_command="\"$HOME/.local/bin/agy\""
else
    printf 'Google Antigravity CLI installation did not provide the agy command.\n' >&2
    exit 1
fi

ep_agent_require_api_key

ep_agent_install_skills \
    "$HOME/.gemini/config/skills" \
    "$EP_AGENT_ROOT/research_agent/skills" \
    "$EP_AGENT_ROOT/harnesses/antigravity/skills"

printf '\nGoogle Antigravity CLI and EP Agent skills are ready.\n'
printf 'Next: from the project where you want to work, run:\n'
printf '  source "%s/.venv/bin/activate" && %s\n' "$EP_AGENT_ROOT" "$agy_command"
