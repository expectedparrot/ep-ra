# Environment & runtime

`uxtest` is pinned as an ep-agent project dependency. Run it through the locked
project environment; do not install or upgrade it during a study:

```
uv run --frozen --no-dev uxtest --version
uv run --frozen --no-dev uxtest doctor
```

Everything below is runtime configuration, not setup.

## doctor

```
uv run --frozen --no-dev uxtest doctor
```
Checks: `uxtest` importable, `edsl` importable, Playwright Chromium launches,
`pandoc` available. If `doctor` reports something broken, surface that to the
user rather than trying to reinstall.

## Store location & initialization

The store is `uxtest_store/` — in the study layout, under `data/`
(`data/uxtest_store/`). `init` creates it with a default `config.yaml`, a
`seniors.yaml` persona, and the store's subdirs.

uxtest finds the store by walking up the tree from the study root (checking each
directory and its `data/` subdir, like `.git`). Later commands reuse the store and
never touch your edited `config.yaml` — `init` only writes config for a brand-new
store or with `--force`.
A store whose `config.yaml` is missing raises `FileNotFoundError`; fix with
`uxtest init --force`, which (re)writes `config.yaml` and the default
`seniors.yaml` without deleting custom personas.

## Model configuration

<!-- lint-allow-model: illustrative example, not a model recommendation -->
`config.yaml` holds the **store-wide default** `model` (default `gpt-4o`; any
model id EDSL recognizes works). Pin the model **per study in the fixture** — an
`overrides: {model: ...}` block — rather than editing `config.yaml`. The fixture
is the source of truth; a per-variant `overrides:` can even set a different model
per device. The
store default applies only when a fixture sets no override.
