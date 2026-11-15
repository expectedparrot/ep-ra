#!/usr/bin/env bash

set -euo pipefail

EP_AGENT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$EP_AGENT_DIR"

if [[ -f "$EP_AGENT_DIR/.env" ]]; then
    set -a
    # shellcheck disable=SC1091
    source "$EP_AGENT_DIR/.env"
    set +a
fi

if ! command -v uv >/dev/null 2>&1; then
    printf '%s\n' "ep-pi.sh requires uv: https://docs.astral.sh/uv/" >&2
    exit 127
fi

if ! command -v pi >/dev/null 2>&1; then
    printf '%s\n' "ep-pi.sh requires the Pi CLI on PATH (Node.js 22.19 or newer)." >&2
    exit 127
fi

SESSION_DIR="$EP_AGENT_DIR/session-transcripts/pi"
mkdir -p "$SESSION_DIR"
SESSION_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')

exec uv run --frozen --no-dev -- pi \
    --session-dir "$SESSION_DIR" \
    --session-id "$SESSION_ID" \
    --approve \
    --no-context-files \
    "$@"
