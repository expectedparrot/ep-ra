#!/usr/bin/env bash

set -euo pipefail

EP_AGENT_ROOT=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

case "${1:-}" in
    --help|-h)
        cat <<'EOF'
Usage: ./install.sh

Choose a supported AI harness, configure and verify your required Expected
Parrot API key, and install EP Agent for that harness. OpenCode and the
Antigravity CLI are installed automatically if they are missing.
EOF
        exit 0
        ;;
    "")
        ;;
    *)
        printf 'Unknown option: %s\nRun ./install.sh --help for usage.\n' "$1" >&2
        exit 2
        ;;
esac

if [[ ! -t 0 ]]; then
    printf 'Run ./install.sh from an interactive terminal.\n' >&2
    exit 2
fi

printf '%s\n' 'EP Agent setup' '' \
    'Choose the AI harness you want to use:' \
    '  1) Claude Code' \
    '  2) Codex' \
    '  3) OpenCode' \
    '  4) Pi' \
    '  5) Google Antigravity CLI' \
    '  q) Quit'

while true; do
    read -r -p 'Harness [1-5]: ' choice
    case "$choice" in
        1) installer="$EP_AGENT_ROOT/installers/install-claude-code.sh"; break ;;
        2) installer="$EP_AGENT_ROOT/installers/install-codex.sh"; break ;;
        3) installer="$EP_AGENT_ROOT/installers/install-opencode.sh"; break ;;
        4) installer="$EP_AGENT_ROOT/installers/install-pi.sh"; break ;;
        5) installer="$EP_AGENT_ROOT/installers/install-antigravity.sh"; break ;;
        q|Q) printf 'Setup cancelled.\n'; exit 0 ;;
        *) printf 'Choose 1, 2, 3, 4, 5, or q.\n' ;;
    esac
done

exec "$installer"
