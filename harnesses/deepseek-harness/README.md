# DeepSeek Harness

DeepSeek Harness is experimental developer-preview software. Its maintainers
say it has not had a security audit. It can run model-generated commands and
access files, credentials, processes, and network resources available to it.
Read the [official safety guidance](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md)
and use it only in a workspace you are comfortable exposing to the harness.

## Install EP Agent

From the EP Agent checkout, run the universal installer and choose DeepSeek
Harness:

```bash
./install.sh
```

The installer requires Node.js/npm, prepares the locked EDSL runtime, verifies
the required Expected Parrot API key, and installs EP Agent skills in
`~/.dsh/skills/`.

## Start

From the project where you want to work, run:

```bash
source /path/to/ep-ra/.venv/bin/activate && npx @deepseek-ai/dsh web
```

The command starts DeepSeek Harness's local web app. Select a workspace there,
then configure a model provider in **Settings > Models**. This provider key is
separate from the Expected Parrot key configured during EP Agent installation.
