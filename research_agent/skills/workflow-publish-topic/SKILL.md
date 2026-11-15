---
name: workflow-publish-topic
description: >
  Push an entire topic (all studies) to the remote server so it is
  shareable. Use when the user wants to publish or share an entire topic
  with all its studies.
tags: [workflow, publishing]
---

# Publish Topic

Push a topic-level repo — which contains all of its studies — to the remote git server.

## Prerequisites

- The user has explicitly asked to publish the topic. Explain that publishing will initialize or modify a local Git repository, create commits, and push to a remote before proceeding.
- The `.env` file at the ep-agent root (`<ep-agent-root>/.env`) must contain `GIT_PUBLISH_URL`.

## Repo Naming

Derive the repo name from the **topic alias** alone:

```
sessions/topic_corn-chips-elasticity  →  corn-chips-elasticity
sessions/topic_ban-the-box            →  ban-the-box
```

Rules:
1. Strip the `topic_` prefix from the topic directory name.
2. The result must be a valid URL path segment (lowercase, hyphens, underscores, no spaces).

## Steps

1. **Read the remote URL base** from the `.env` file:
   ```bash
   source <ep-agent-root>/.env
   echo "$GIT_PUBLISH_URL"
   ```
   If `GIT_PUBLISH_URL` is not set, stop and tell the user to add it to `.env`.

2. **Determine the repo name** from the topic path. For example, if the topic is `sessions/topic_corn-chips-elasticity`:
   ```bash
   REPO_NAME="corn-chips-elasticity"
   ```

3. **Navigate to the topic root** (the directory containing `README.md` and the `study_*` subdirectories).

4. **Prepare the repository at publish time.** Do not assume ordinary study creation initialized Git.
   - If the topic is not already a repository, run `git init --initial-branch=main`, add the topic files, and create the first commit.
   - If it is already a repository, inspect its status and commit only the changes intended for publishing. Determine its current branch with `git branch --show-current`; do not assume it is named `main`.
   - If a commit fails because identity is missing, ask the user for the name and email to configure locally for this repository; do not invent placeholder identity or change global Git configuration.
   - Never remove or replace an existing `.git` directory.

5. **Add the remote and push**:
   ```bash
   cd <topic_root>
   PUBLISH_BRANCH="$(git branch --show-current)"
   test -n "$PUBLISH_BRANCH"  # stop and ask the user if HEAD is detached
   git remote add origin "${GIT_PUBLISH_URL}/${REPO_NAME}.git"
   git push -u origin "$PUBLISH_BRANCH"
   ```
   If the remote `origin` already exists, check whether it points to the correct URL. If it does, just push. If it points elsewhere, ask the user before changing it.

6. **Report the shareable URL** to the user:
   ```
   Published: ${GIT_PUBLISH_URL}/${REPO_NAME}.git
   ```

## Error Handling

- If `git push` fails with a permissions or network error, report to the user.
- If `origin` already exists with a different URL, do not overwrite — ask the user what to do.
- If the topic has no commits, create the first commit as part of this explicitly requested publishing workflow.
- If a commit fails because `user.name` or `user.email` is unset, request those values and set them with `git config --local` only.

## Nested Git Repos

Existing topics may contain user-created nested repositories. Leave them untouched. Before publishing a topic containing nested `.git` directories, explain that Git will not include their working-tree contents normally and ask whether the user wants to publish those repositories separately or explicitly bundle selected artifacts.

## Example

```bash
# Full example for sessions/topic_corn-chips-elasticity
source <ep-agent-root>/.env
cd <ep-agent-root>/sessions/topic_corn-chips-elasticity

REPO_NAME="corn-chips-elasticity"
git init --initial-branch=main  # only if this topic is not already a repository
git add -A
git commit -m "Publish topic: corn chips elasticity"
git remote add origin "${GIT_PUBLISH_URL}/${REPO_NAME}.git"
PUBLISH_BRANCH="$(git branch --show-current)"
git push -u origin "$PUBLISH_BRANCH"
# → Published: https://<server>/git/corn-chips-elasticity.git
```
