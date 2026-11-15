#!/usr/bin/env bash

set -euo pipefail

# Resolve project files relative to this script, regardless of the caller's cwd.
EP_AGENT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$EP_AGENT_DIR"

# Load project-local environment variables (API keys, etc.) when available.
if [[ -f "$EP_AGENT_DIR/.env" ]]; then
    set -a
    # shellcheck disable=SC1091
    source "$EP_AGENT_DIR/.env"
    set +a
fi

# Give this session a dedicated transcript and debug-log location.
TRANSCRIPT_DIR="$EP_AGENT_DIR/session-transcripts"
mkdir -p "$TRANSCRIPT_DIR"
SESSION_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
printf '%s\n' "$SESSION_ID" >> "$TRANSCRIPT_DIR/.ep-sessions"

# Use Claude Code's stable alias so the launcher follows the Opus version the
# installed CLI and account currently support. Version-like shorthand such as
# "opus-4.6" is not a recognized Claude Code model identifier.
EP_CLI_MODEL="${EP_CLI_MODEL:-opus}"
DEBUG_DIR="$TRANSCRIPT_DIR/debug"
DEBUG_LOG="$DEBUG_DIR/$SESSION_ID.log"
mkdir -p "$DEBUG_DIR"

# Share the harness-neutral role and user-outcome guidance with the detailed
# Claude Code workflow instructions.
SYSTEM_PROMPT_FILE=$(mktemp "$TRANSCRIPT_DIR/system-prompt.XXXXXX")
trap 'rm -f "$SYSTEM_PROMPT_FILE"' EXIT
cat \
    "$EP_AGENT_DIR/research_agent/skills/workflow-session-start/references/agent-core.md" \
    "$EP_AGENT_DIR/research_agent/system_prompt.md" \
    > "$SYSTEM_PROMPT_FILE"

if ! command -v uv >/dev/null 2>&1; then
    printf '%s\n' "ep-cli.sh requires uv: https://docs.astral.sh/uv/" >&2
    exit 127
fi

# --frozen makes uv.lock the executable environment contract. Claude inherits
# this environment, so every `ep` or Python invocation uses the pinned EDSL.
uv run --frozen --no-dev -- claude \
    --session-id "$SESSION_ID" \
    --model "$EP_CLI_MODEL" \
    --dangerously-skip-permissions \
    --debug-file "$DEBUG_LOG" \
    --system-prompt-file "$SYSTEM_PROMPT_FILE" \
    --plugin-dir "$EP_AGENT_DIR/research_agent" \
    "$@"
