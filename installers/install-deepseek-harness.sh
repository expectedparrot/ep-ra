#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

if ! command -v npx >/dev/null 2>&1; then
    printf 'Node.js and npm are required for DeepSeek Harness. Install Node.js from https://nodejs.org/ and rerun this installer.\n' >&2
    exit 127
fi

ep_agent_setup_runtime "$@"
ep_agent_require_api_key
ep_agent_install_skills \
    "$HOME/.dsh/skills" \
    "$EP_AGENT_ROOT/research_agent/skills"

cat <<'EOF'

DeepSeek Harness is experimental developer-preview software. Its authors say
it has not undergone a security audit and may execute generated commands and
access files, credentials, processes, and the network available to it.
Review its safety guidance before use:
https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md

The Expected Parrot key above configures EDSL. DeepSeek Harness separately
needs a model-provider key configured in its web app under Settings > Models.
EOF
ep_agent_print_next_command 'npx @deepseek-ai/dsh web'
