# Extra version sites — blockscout-analysis

The `blockscout-analysis` skill embeds its own version into a `User-Agent` header that ad-hoc scripts are instructed to send. This is in addition to the shared frontmatter + marketplace edits handled by the parent `SKILL.md`.

## `blockscout-analysis/SKILL.md` — User-Agent header instruction

In the body of the skill (currently around line 121, in the Ad-hoc Scripts / MCP REST API access section), the instructions tell agents to send:

```
User-Agent: Blockscout-SkillGuidedScript/<OLD>
```

Replace `Blockscout-SkillGuidedScript/<OLD>` with `Blockscout-SkillGuidedScript/<NEW>`. Use exact strings — do not use regex replacements.

The version embedded in this header must always match the frontmatter version, which is why it is bumped together. Server-side request logging keys off this header to attribute traffic to the skill version that produced it.
