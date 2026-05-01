# Codex Plugins Publisher — Specification

## Purpose

Publish this repository's plugins to a dedicated branch in a layout the [Codex plugin marketplace](https://github.com/blockscout/agent-skills/blob/main/.agents/plugins/marketplace.json) can consume directly. Codex requires plugins to be self-contained directory trees with no symlinks, while this repo keeps each skill as a single source-of-truth directory at the project root and reuses it via symlinks under `.agents/plugins/<plugin>/skills/<skill>`. The publisher script bridges the two layouts without restructuring the source tree.

## Background

- The Codex marketplace manifest (`.agents/plugins/marketplace.json`) supports `git-subdir` plugin sources with an explicit `ref`, so the install-time content can come from a branch other than `main`.
- The branch dedicated to that content is `codex-plugins`. Codex first reads `marketplace.json` from `main`, then fetches each plugin's directory from `codex-plugins`.
- The same skill directories also serve as Claude Code plugins from `main`, so the source layout cannot change.

## Reference

- [Codex plugin marketplace manifest](https://developers.openai.com/codex/plugins/marketplaces/) — schema for `marketplace.json`, including `git-subdir` source with `ref`.

## Inputs

| Input | Default | Notes |
|-------|---------|-------|
| `<source-ref>` (positional) | `main` | Branch or tag (e.g. `vX.Y.Z`) to publish from |
| `<target-branch>` (positional) | `codex-plugins` | Branch to write the published layout to |
| `REMOTE` (env) | `origin` | Git remote to push to |

## Source Layout (read from `<source-ref>`)

```
.agents/plugins/
├── marketplace.json
├── <plugin>/
│   ├── .codex-plugin/plugin.json
│   ├── .mcp.json                   (optional)
│   └── skills/
│       └── <skill> -> ../../../../<skill>     (symlink to repo-root skill dir)
```

Every immediate subdirectory of `.agents/plugins/` is a plugin. `marketplace.json` is the only non-directory entry and is reserved.

## Target Layout (written to `<target-branch>`)

```
.agents/plugins/marketplace.json   (verbatim copy from source)
plugins/<plugin>/
├── .codex-plugin/plugin.json
├── .mcp.json                      (if present in source)
└── skills/<skill>/                (real directory with dereferenced content)
README.md                          (short, generated)
```

Constraints:

- No symlinks anywhere under `plugins/`.
- The target branch root contains only the three managed paths above; nothing else from the source ref bleeds through.

## Behavior

### Source enumeration

Read committed entries only — never the working tree. Use `git ls-tree`/`git cat-file` against `<source-ref>` so:

- gitignored files cannot leak into the published branch
- uncommitted local edits cannot leak in
- the script is reproducible from a fresh clone

### Symlink dereferencing

For every committed entry under a plugin tree:

| Mode | Action |
|------|--------|
| `100644` / `100755` | Write blob content to the destination path; preserve executable bit |
| `120000` (symlink) | Read link target via `git cat-file blob`, resolve relative to the symlink's parent directory, normalize `.`/`..`, then recurse on the resolved path |
| `160000` (submodule) | Fail loudly — submodules are not supported in plugin trees |
| anything else | Fail loudly |

The recursion produces a real directory at the symlink's location populated with the committed contents of the resolved target. Resolution must stay within the repo root; an absolute symlink target or one that escapes the root via `..` is a fatal error.

### Failure modes

The script exits non-zero with a clear message on:

- unknown source ref
- missing `.agents/plugins/marketplace.json` at the source ref
- empty `.agents/plugins/` at the source ref
- a symlink whose resolved target has no committed content (broken symlink)
- absolute symlink target, or one that escapes the repo root
- submodule entry inside a plugin tree
- any tree mode other than the four listed above

### Target branch sync

1. Determine whether `<target-branch>` exists locally and/or on the remote.
2. Set up a temp git worktree:
   - exists locally → check out the existing branch
   - exists only on remote → fetch into a local branch, then check out
   - does not exist → create as an **orphan branch** (no shared history with `main`)
3. Force the worktree's tree to exactly match the staged content: remove every top-level entry except `.git`, then copy the staged tree over. Stale files from prior runs are removed; any branch content not produced by this script is removed.
4. `git add -A`. If the index is unchanged, exit 0 without committing.
5. Otherwise commit with message `Sync codex plugins from <source-ref> (<short-sha>)` where `<short-sha>` is the 7-char abbreviation of `<source-ref>^{commit}`.
6. Push the target branch to `<remote>` (`-u` on first publish, plain push thereafter).

### Generated `README.md`

Short and identical across runs except for the source ref:

```
# Blockscout AI — Codex Plugins

This branch holds the packaged Codex plugins for the Blockscout AI marketplace.
It is generated from `<source-ref>`. Do not edit by hand.

Install in Codex:

` ` `
codex plugin marketplace add blockscout/agent-skills
` ` `
```

(Backticks shown spaced for display; the real file uses a fenced code block.)

## Cleanup

The script registers a trap that removes the temp staging directory and the temp worktree on any exit path, then runs `git worktree prune` to keep the repo's worktree list clean.

## Portability

Must run on macOS's stock `bash` 3.2 — no `mapfile`, no `${var,,}`/`${var^^}`, no associative arrays. The shebang is `#!/usr/bin/env bash` and the script uses `set -euo pipefail`.

## Out of Scope

- Tag creation or version bumping (handled separately by the `bump-skill-version` skill).
- Validation of plugin manifest contents (`plugin.json`, `marketplace.json`) beyond confirming the files exist and are committed.
- Resolving symlinks that point through other symlinks across plugin boundaries — currently every plugin links only to its single root skill directory.

## Install Flow Enabled by This Script

1. User runs `codex plugin marketplace add blockscout/agent-skills` — Codex clones the default branch and reads `.agents/plugins/marketplace.json`.
2. User opens `/plugins` in Codex and discovers the plugins from the manifest.
3. User installs a plugin — Codex fetches `plugins/<plugin>/` from the `codex-plugins` ref declared in the manifest.
4. The skill (and any inline MCP server) becomes available in the working project.
