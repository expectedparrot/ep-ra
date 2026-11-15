#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

ep_agent_setup_runtime "$@"
ep_agent_require_api_key

ep_agent_install_skills \
    "$HOME/.gemini/config/skills" \
    "$EP_AGENT_ROOT/research_agent/skills" \
    "$EP_AGENT_ROOT/harnesses/antigravity/skills"

printf '\nEP Agent is ready in Google Antigravity.\n'
printf 'Next: restart Antigravity or reload skills, then start a research project and describe your question.\n'
