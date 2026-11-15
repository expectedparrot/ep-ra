#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

if ! command -v claude >/dev/null 2>&1; then
    printf 'Install Claude Code first: https://code.claude.com/docs/en/overview\n' >&2
    exit 127
fi

ep_agent_setup_runtime "$@"
ep_agent_require_api_key

if ! claude plugin marketplace list 2>/dev/null | grep -Fq 'expected-parrot'; then
    claude plugin marketplace add "$EP_AGENT_ROOT"
fi

if ! claude plugin list 2>/dev/null | grep -Fq 'ep-agent@expected-parrot'; then
    claude plugin install ep-agent@expected-parrot
fi

printf '\nEP Agent is ready in Claude Code.\n'
printf 'Next: start Claude Code in your research folder and describe your question.\n'
