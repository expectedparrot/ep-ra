#!/usr/bin/env bash

set -euo pipefail

EP_AGENT_ROOT=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
EP_AGENT_MARKER=".ep-agent-managed-skill"
EP_AGENT_RUNTIME_INSTALLED=0

ep_agent_setup_runtime() {
    local install_runtime=1
    local arg

    for arg in "$@"; do
        case "$arg" in
            --skills-only)
                install_runtime=0
                ;;
            --help)
                cat <<'EOF'
Usage: install-<harness>.sh [--skills-only]

By default, the installer also creates the locked EP Python/EDSL environment.
Pass --skills-only to install the harness adapter without that environment.
EOF
                exit 0
                ;;
            *)
                printf 'Unknown option: %s\n' "$arg" >&2
                return 2
                ;;
        esac
    done

    if ((install_runtime)); then
        if ! command -v uv >/dev/null 2>&1; then
            printf 'Install uv first: https://docs.astral.sh/uv/getting-started/installation/\n' >&2
            return 127
        fi
        (cd "$EP_AGENT_ROOT" && uv sync --frozen --no-dev)
        EP_AGENT_RUNTIME_INSTALLED=1
    fi
}

ep_agent_install_skills() {
    local target_dir="$1"
    shift
    local source_dir
    local skill_dir name target
    local -a skill_dirs=()

    mkdir -p "$target_dir"
    for source_dir in "$@"; do
        for skill_dir in "$source_dir"/*; do
            [[ -f "$skill_dir/SKILL.md" ]] || continue
            skill_dirs+=("$skill_dir")
        done
    done

    if ((${#skill_dirs[@]} == 0)); then
        printf 'No skills found in the provided source directories.\n' >&2
        return 1
    fi

    # Check every target before copying so a name conflict cannot leave a
    # partially installed skill set.
    for skill_dir in "${skill_dirs[@]}"; do
        name=${skill_dir##*/}
        target="$target_dir/$name"
        if [[ -L "$target" ]]; then
            printf 'Refusing to replace symlink at %s\n' "$target" >&2
            return 1
        fi
        if [[ -e "$target" && ! -f "$target/$EP_AGENT_MARKER" ]]; then
            printf 'Skill name conflict at %s; move it before installing EP Agent.\n' "$target" >&2
            return 1
        fi
    done

    for skill_dir in "${skill_dirs[@]}"; do
        name=${skill_dir##*/}
        target="$target_dir/$name"
        if [[ -d "$target" ]]; then
            rm -rf -- "$target"
        fi
        mkdir -p "$target"
        cp -R "$skill_dir"/. "$target/"
        find "$target" -type d -name '__pycache__' -prune -exec rm -rf {} +
        find "$target" -type f \( -name '*.pyc' -o -name '.DS_Store' \) -delete
        : > "$target/$EP_AGENT_MARKER"
    done

    printf 'Installed %d EP Agent skills in %s\n' "${#skill_dirs[@]}" "$target_dir"
}

ep_agent_print_runtime_note() {
    if ((EP_AGENT_RUNTIME_INSTALLED)); then
        printf '\nThe locked EP Python/EDSL runtime was installed in %s/.venv.\n' "$EP_AGENT_ROOT"
    else
        printf '\nThe EP Python/EDSL runtime was skipped (--skills-only).\n'
    fi
    cat <<EOF

The installer does not configure model-provider or Expected Parrot credentials.

For EDSL workflows, install the EP API key with:
  uv run --frozen --no-dev ep auth login --api_key <key>

You can instead set EXPECTED_PARROT_API_KEY in the environment before
launching the harness. Authenticate the selected harness with its model
provider separately. When using Codex, OpenCode, or the Claude plugin from a
different project, activate this checkout's runtime before starting it:
  source "$EP_AGENT_ROOT/.venv/bin/activate"

The ep-cli.sh and ep-pi.sh launchers activate the locked runtime themselves.
EOF
}
