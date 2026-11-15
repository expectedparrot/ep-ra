#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

ep_agent_setup_runtime "$@"

if ! command -v opencode >/dev/null 2>&1 && [[ ! -x "$HOME/.opencode/bin/opencode" ]]; then
    if ! command -v curl >/dev/null 2>&1; then
        printf 'Install curl before installing OpenCode.\n' >&2
        exit 127
    fi
    printf 'Installing OpenCode CLI...\n'
    curl -fsSL https://opencode.ai/v2/install | bash
fi

if command -v opencode >/dev/null 2>&1; then
    opencode_command=opencode
elif [[ -x "$HOME/.opencode/bin/opencode" ]]; then
    opencode_command="\"$HOME/.opencode/bin/opencode\""
else
    printf 'OpenCode CLI installation did not provide the opencode command.\n' >&2
    exit 1
fi

ep_agent_require_api_key

ep_agent_install_skills \
    "$HOME/.config/opencode/skills" \
    "$EP_AGENT_ROOT/research_agent/skills"

printf '\nEP Agent is ready in OpenCode.\n'
ep_agent_print_next_command "$opencode_command"
