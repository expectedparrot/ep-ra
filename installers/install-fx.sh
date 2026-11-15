#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

ep_agent_setup_runtime "$@"

if ! command -v fx >/dev/null 2>&1 && [[ ! -x "$HOME/.local/bin/fx" ]]; then
    if ! command -v curl >/dev/null 2>&1; then
        printf 'Install curl before installing Vercel fx.\n' >&2
        exit 127
    fi
    printf 'Installing Vercel fx...\n'
    curl -fsSL https://fx.sh/setup.sh | bash
fi

if command -v fx >/dev/null 2>&1; then
    fx_command=fx
elif [[ -x "$HOME/.local/bin/fx" ]]; then
    fx_command="\"$HOME/.local/bin/fx\""
else
    printf 'Vercel fx installation did not provide the fx command.\n' >&2
    exit 1
fi

ep_agent_require_api_key

ep_agent_install_skills \
    "$HOME/.fx/skills" \
    "$EP_AGENT_ROOT/research_agent/skills"

printf '\nEP Agent is ready in Vercel fx.\n'
printf 'If you have not connected a model provider, fx will guide you through it on first launch.\n'
ep_agent_print_next_command "$fx_command"
