---
name: bump-skill-version
description: "Bump a skill's version number across all files in this repo (the skill's own frontmatter, the marketplace plugin entry, and any skill-specific occurrences). Pass the skill name and new version as arguments (e.g., 'blockscout-analysis 0.5.0'). Use after content changes are complete and the skill is ready for a new release."
allowed-tools: Read, Edit, Grep
metadata:
  internal: true
---

# Bump Skill Version

Update a skill's version string in every file that references it. This skill works for any skill in the repo: it first applies a shared bump procedure (frontmatter version + marketplace plugin entry), then consults a per-skill reference file for any extra locations specific to that skill.

## Usage

Pass `<skill-name> <new-version>` as `$ARGUMENTS` (e.g., `blockscout-analysis 0.5.0`). If either is missing, ask the user before proceeding.

`<skill-name>` must match a top-level skill directory in the repo root (e.g., `blockscout-analysis/`, `web3-dev/`). Verify the directory and its `SKILL.md` exist before making any edit.

## Shared procedure (applies to every skill)

These three edits are required for every skill bump.

### 1. `<skill-name>/SKILL.md` — frontmatter metadata

The YAML frontmatter contains a single-line JSON `metadata` field with a `"version"` key:

```
metadata: {"author":"blockscout.com","version":"<OLD>","github":...}
```

Replace `"version":"<OLD>"` with `"version":"<NEW>"`. Use exact strings — do not use regex replacements.

### 2. `.claude-plugin/marketplace.json` — plugin entry version

The marketplace manifest has a `plugins` array; each entry has its own `"name"` and `"version"` fields. The bare string `"version": "<OLD>"` may appear in more than one plugin entry when versions happen to coincide, so the `old_string` passed to `Edit` must include the `"name"` line of the target plugin to disambiguate. Match a block like this:

```json
"name": "<skill-name>",
      "description": "...",
      "source": "./<skill-name>/",
      "strict": false,
      "version": "<OLD>",
```

Replace only the `"version": "<OLD>"` line within that block with `"version": "<NEW>"`. Leave the top-level marketplace `metadata.version` untouched — it tracks the marketplace as a whole, not the individual skill.

### 3. `.agents/plugins/<skill-name>/.codex-plugin/plugin.json` — codex plugin descriptor

Each skill that ships as a Codex plugin has its own descriptor at `.agents/plugins/<skill-name>/.codex-plugin/plugin.json`. The descriptor is dedicated to one skill, so the version field is unambiguous — but include the `"name"` line in the `old_string` anyway as a sanity check that the right file is being edited:

```json
{
  "name": "<skill-name>",
  "version": "<OLD>",
```

Replace `"version": "<OLD>"` with `"version": "<NEW>"`. If the file does not exist for a given skill (a skill might not ship as a Codex plugin), skip this edit.

## Skill-specific procedure

After the shared edits, check for `references/<skill-name>.md` next to this `SKILL.md`. If it exists, follow every extra step it lists. If it does not exist, the skill has no additional version sites — skip this step. This is intentional: keeping per-skill quirks in their own file lets `SKILL.md` stay short and lets new skills be onboarded by dropping in a single reference file (or none at all).

## Procedure

1. **Parse arguments**: split `$ARGUMENTS` into `<skill-name>` and `<new-version>`. If either is missing, ask the user.
2. **Validate target**: confirm `<skill-name>/SKILL.md` exists. Abort if not — a typo in the skill name would otherwise bump the wrong file.
3. **Discover current version**: `Grep` for the pattern `"version":"[0-9]+\.[0-9]+\.[0-9]+"` in `<skill-name>/SKILL.md` to read the current version from the frontmatter metadata.
4. **Validate version**: confirm `<new-version>` differs from the current version. Abort if identical.
5. **Apply shared edits**: perform the three edits in "Shared procedure" above. Use exact old/new strings. Skip the codex descriptor edit only if the file does not exist for this skill.
6. **Apply skill-specific edits**: if `references/<skill-name>.md` exists, read it and apply each edit it lists. Otherwise skip.
7. **Verify**: `Grep` for the old version string scoped to `<skill-name>/`, `.claude-plugin/marketplace.json`, and `.agents/plugins/<skill-name>/` and confirm zero remaining occurrences. Other skills' files and `.memory_bank/` may legitimately contain that string and must not be touched.

## Notes

- `.memory_bank/` contains spec documentation with example version strings that do not track live versions; never update them.
- Other skills' `SKILL.md` files may currently sit at the same numeric version as the one being bumped. Do not update them — only the targeted skill changes.
- This skill only updates version strings. It does not modify content — use the appropriate per-skill content-update workflow for that.
