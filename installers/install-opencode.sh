#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

if ! command -v opencode >/dev/null 2>&1; then
    printf 'Install OpenCode first: https://opencode.ai/docs/\n' >&2
    exit 127
fi

ep_agent_setup_runtime "$@"
ep_agent_require_api_key

ep_agent_install_skills \
    "$HOME/.config/opencode/skills" \
    "$EP_AGENT_ROOT/research_agent/skills"

cat <<'EOF'

EP Agent skills are available globally to OpenCode. Start OpenCode in the
project where you want to work and ask your research question. Re-run this
installer after updating the EP Agent checkout to refresh installed skills.
EOF
ep_agent_print_runtime_note
