#!/bin/bash
# List available research study types with their trigger descriptions.
# Usage: bash list_study_types.sh

SKILLS_DIR="$(dirname "$0")/skills"

for dir in "$SKILLS_DIR"/research-*/; do
    # Deleted or renamed skills may leave empty local directories behind.
    [ -f "$dir/SKILL.md" ] || continue
    skill_name=$(basename "$dir")
    # Extract description from SKILL.md frontmatter
    desc=$(awk '/^---$/{n++; next} n==1{print} n==2{exit}' "$dir/SKILL.md" \
        | grep -A20 'description:' \
        | sed '1s/^description: *>*//' \
        | sed '/^[a-z]*:/,$d' \
        | tr '\n' ' ' \
        | sed 's/  */ /g; s/^ *//; s/ *$//')
    printf "%-30s  %s\n" "$skill_name" "$desc"
done
