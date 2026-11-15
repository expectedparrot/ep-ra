#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

if ! command -v pi >/dev/null 2>&1; then
    printf 'Install Pi first: https://docs.pi.dev/latest/quickstart\n' >&2
    exit 127
fi

ep_agent_setup_runtime "$@"
ep_agent_require_api_key

install_log=$(mktemp)
if ! pi install "$EP_AGENT_ROOT" >"$install_log" 2>&1; then
    cat "$install_log" >&2
    rm "$install_log"
    exit 1
fi
rm "$install_log"

provider_login="skipped"
if [[ -t 0 ]]; then
    printf '\nPi needs a model provider for conversations. You can sign in now or later.\n'
    read -r -p 'Provider ID to sign in now (for example anthropic or openai; Enter to skip): ' provider
    if [[ -n "$provider" ]]; then
        pi auth login "$provider"
        provider_login="complete"
    fi
fi

printf '\nEP Agent is ready in Pi.\n'
if [[ "$provider_login" == "complete" ]]; then
    printf 'Next: run Pi in your research folder and describe your question.\n'
else
    printf 'Next: run Pi, use /login to connect a model provider, then describe your question.\n'
fi
