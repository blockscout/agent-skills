---
name: upgrade-blockscout-api
description: "Refresh the bundled Blockscout API reference files inside one of this repo's end-user skills. Takes a target argument; each target has its own pipeline because the source artefacts differ (Swagger releases for `blockscout-analysis`, a build-time clone of the `pro-api` repo for `web3-dev`). Run when a target's upstream cuts a new release and the skill's bundled references need to catch up."
disable-model-invocation: true
allowed-tools: Bash(python3 *), Bash(git *), Bash(bash *), Bash(./*), Bash(cp *), Read, Edit, Grep, Glob
metadata:
  internal: true
---

# Upgrade Blockscout API

Refresh the API reference files bundled inside one of this repo's end-user skills.

The two skills published from this repo each carry their own snapshot of the Blockscout API surface, but they're built from completely different upstream artefacts and on independent release cadences. Coupling their refreshes would force spurious diffs on whichever target's upstream hasn't moved, so this skill takes a **target** argument and runs only that target's pipeline.

## Invocation

```
/upgrade-blockscout-api <target>
```

`<target>` must be one of:

| Target | Refreshes | Procedure |
|--------|-----------|-----------|
| `blockscout-analysis` | `blockscout-analysis/references/blockscout-api/*.md` and the master index, from latest Blockscout backend + Stats releases. | [references/blockscout-analysis.md](references/blockscout-analysis.md) |
| `web3-dev` | `web3-dev/references/pro-api.json` and `web3-dev/references/pro-api-index.md`, from a build-time clone of the `pro-api` repo. | [references/web3-dev.md](references/web3-dev.md) |

## Routing rule

1. Read the `<target>` argument from the user's invocation. If it is missing or not in the table above, **stop and ask** which target to upgrade — listing the valid values. Do not guess and do not run both.
2. Read the matching reference file under `references/` and follow it end-to-end. The reference is the canonical, authoritative procedure for that target.
3. Do not mix instructions across targets. The two procedures share no structural steps; lifting a step from one into the other will silently corrupt the bundled output.

## Working directory

Both procedures assume the working directory is the **repository root** (the parent of `blockscout-analysis/` and `web3-dev/`). Confirm this before running any script — the indexers and patch tools resolve paths relative to the repo root and will write to the wrong place otherwise.

## Adding a new target

When a third skill in this repo starts bundling Blockscout API references, add it as a new row in the routing table above and drop a `references/<new-target>.md` file alongside the existing two. Keep this SKILL.md as routing only — every target's procedure lives in its own reference file so the agent loads only what the current run needs.
