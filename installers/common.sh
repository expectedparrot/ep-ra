#!/usr/bin/env bash

set -euo pipefail

EP_AGENT_ROOT=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
EP_AGENT_MARKER=".ep-agent-managed-skill"

ep_agent_setup_runtime() {
    local install_runtime=1
    local arg

    for arg in "$@"; do
        case "$arg" in
            --help)
                cat <<'EOF'
Usage: install-<harness>.sh

Installs the locked EP Python/EDSL environment, requires a working EP API key,
and installs the selected harness adapter.
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
    fi
}

ep_agent_require_api_key() {
    if [[ -z "${EXPECTED_PARROT_API_KEY:-}" ]] && (cd "$EP_AGENT_ROOT" && uv run --frozen --no-dev ep check >/dev/null 2>&1); then
        printf 'An existing Expected Parrot API key was verified.\n'
        return
    fi

    if [[ -z "${EXPECTED_PARROT_API_KEY:-}" ]]; then
        cat <<'EOF'

An Expected Parrot API key is required to use EP Agent.
Get or create one in your account, then follow the EDSL login prompts:
https://www.expectedparrot.com/getting-started/edsl-api-keys
EOF
        if [[ ! -t 0 ]]; then
            printf 'Run this installer in a terminal to complete the EDSL login flow.\n' >&2
            return 2
        fi
        (cd "$EP_AGENT_ROOT" && uv run --frozen --no-dev ep auth login)
    else
        printf 'Configuring Expected Parrot authentication from EXPECTED_PARROT_API_KEY.\n'
        (cd "$EP_AGENT_ROOT" && uv run --frozen --no-dev ep auth login --api_key "$EXPECTED_PARROT_API_KEY")
    fi

    (cd "$EP_AGENT_ROOT" && uv run --frozen --no-dev ep check)
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
