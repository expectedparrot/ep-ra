#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

if ! command -v pi >/dev/null 2>&1; then
    printf 'Install Pi first: https://docs.pi.dev/latest/quickstart\n' >&2
    exit 127
fi

ep_agent_setup_runtime "$@"

pi install "$EP_AGENT_ROOT"

printf 'EP Agent is installed in Pi. Start Pi in the project where you want to work.\n'
printf 'For the full locked local runtime, use %s/ep-pi.sh\n' "$EP_AGENT_ROOT"
ep_agent_print_runtime_note
