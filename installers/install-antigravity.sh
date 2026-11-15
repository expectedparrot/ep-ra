#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$SCRIPT_DIR/common.sh"

ep_agent_setup_runtime "$@"

if ! command -v agy >/dev/null 2>&1 && [[ ! -x "$HOME/.local/bin/agy" ]]; then
    if ! command -v curl >/dev/null 2>&1; then
        printf 'Install curl before installing Google Antigravity CLI.\n' >&2
        exit 127
    fi
    printf 'Installing Google Antigravity CLI...\n'
    curl -fsSL https://antigravity.google/cli/install.sh | bash
fi

if command -v agy >/dev/null 2>&1; then
    agy_command=agy
elif [[ -x "$HOME/.local/bin/agy" ]]; then
    agy_command="\"$HOME/.local/bin/agy\""
else
    printf 'Google Antigravity CLI installation did not provide the agy command.\n' >&2
    exit 1
fi

ep_agent_require_api_key

python_runtime=$(
    "$EP_AGENT_ROOT/.venv/bin/python" -c 'import sys; print(sys.base_prefix)'
)
antigravity_settings="$HOME/.gemini/antigravity-cli/settings.json"
mkdir -p "$(dirname "$antigravity_settings")"
"$EP_AGENT_ROOT/.venv/bin/python" - "$antigravity_settings" \
    "$EP_AGENT_ROOT/.venv" "$python_runtime" <<'PY'
import json
import os
import sys
import tempfile
from pathlib import Path

settings_path = Path(sys.argv[1])
runtime_paths = [Path(path).resolve() for path in sys.argv[2:]]

if settings_path.exists():
    try:
        settings = json.loads(settings_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot update Antigravity settings at {settings_path}: {exc}", file=sys.stderr)
        sys.exit(1)
else:
    settings = {}

if not isinstance(settings, dict):
    print(f"Cannot update Antigravity settings at {settings_path}: expected a JSON object", file=sys.stderr)
    sys.exit(1)

permissions = settings.setdefault("permissions", {})
if not isinstance(permissions, dict):
    print(f"Cannot update Antigravity settings at {settings_path}: permissions must be an object", file=sys.stderr)
    sys.exit(1)

allowed = permissions.setdefault("allow", [])
if not isinstance(allowed, list) or not all(isinstance(rule, str) for rule in allowed):
    print(f"Cannot update Antigravity settings at {settings_path}: permissions.allow must be a string array", file=sys.stderr)
    sys.exit(1)

for runtime_path in runtime_paths:
    rule = f"read_file({runtime_path})"
    if rule not in allowed:
        allowed.append(rule)

settings_path.parent.mkdir(parents=True, exist_ok=True)
mode = settings_path.stat().st_mode & 0o777 if settings_path.exists() else 0o600
fd, temporary_name = tempfile.mkstemp(dir=settings_path.parent, prefix="settings.", suffix=".tmp")
try:
    with os.fdopen(fd, "w") as temporary_file:
        json.dump(settings, temporary_file, indent=2)
        temporary_file.write("\n")
    os.chmod(temporary_name, mode)
    os.replace(temporary_name, settings_path)
except BaseException:
    try:
        os.unlink(temporary_name)
    except FileNotFoundError:
        pass
    raise
PY

ep_agent_install_skills \
    "$HOME/.gemini/config/skills" \
    "$EP_AGENT_ROOT/research_agent/skills" \
    "$EP_AGENT_ROOT/harnesses/antigravity/skills"

printf '\nGoogle Antigravity CLI and EP Agent skills are ready.\n'
printf 'Antigravity can read the EP Agent runtime and its Python interpreter inside its sandbox.\n'
printf 'Next: from the project where you want to work, run:\n'
printf '  source "%s/.venv/bin/activate" && %s\n' "$EP_AGENT_ROOT" "$agy_command"
