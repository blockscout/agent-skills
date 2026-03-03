---
name: bump-skill-version
description: "Bump the blockscout-analysis skill version number across all files. Use after the API reference files have been updated and you are ready to tag a new release. Pass the new version as an argument (e.g., '0.4.0')."
allowed-tools: Read, Edit, Grep
---

# Bump Skill Version

Update the `blockscout-analysis` skill version string in every file that contains it. Run this after content changes (e.g., API reference updates) are complete and the skill is ready for a new release.

## Usage

Pass the new version as `$ARGUMENTS` (e.g., `0.4.0`). If no argument is provided, ask the user for the target version before proceeding.

## Files and locations

All edits are simple string replacements of the old version with the new version. There are exactly **3 occurrences** across **2 files**:

### 1. `blockscout-analysis/SKILL.md` — frontmatter metadata (line ~5)

The YAML frontmatter contains a single-line JSON `metadata` field with a `"version"` key:

```
metadata: {"author":"blockscout.com","version":"<OLD>","github":...}
```

Replace `"version":"<OLD>"` with `"version":"<NEW>"`.

### 2. `blockscout-analysis/SKILL.md` — User-Agent header instruction (line ~121)

The Ad-hoc Scripts section instructs agents to set a User-Agent header:

```
User-Agent: Blockscout-SkillGuidedScript/<OLD>
```

Replace `Blockscout-SkillGuidedScript/<OLD>` with `Blockscout-SkillGuidedScript/<NEW>`.

### 3. `.claude-plugin/marketplace.json` — plugin version (line ~16)

The marketplace manifest lists the skill version:

```json
"version": "<OLD>",
```

Replace `"version": "<OLD>"` with `"version": "<NEW>"`.

## Procedure

1. **Discover the current version**: Run `Grep` for the pattern `"version":"[0-9]+\.[0-9]+\.[0-9]+"` in `blockscout-analysis/SKILL.md` to read the current version from the frontmatter metadata.
2. **Validate**: Confirm the new version (`$ARGUMENTS`) differs from the current version. Abort if they are identical.
3. **Apply edits**: Use the `Edit` tool for each of the 3 locations listed above. Use exact old/new strings — do not use regex replacements.
4. **Verify**: Run `Grep` for the old version string across the repository to confirm zero remaining occurrences (excluding `.memory_bank/` which contains spec documentation with example version strings that do not track the live version).

## Notes

- The file `.memory_bank/specs/blockscout-analysis/spec.md` contains `0.3.0` as a prose example illustrating the JSON format. This is **not** a live version reference and must **not** be updated.
- This skill only updates version strings. It does not modify API reference content — use the `upgrade-blockscout-api` skill for that.
