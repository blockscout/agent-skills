# OpenAI Codex Agent Metadata (`agents/openai.yaml`) — Specification

## Purpose

Produce an `agents/openai.yaml` file so that the `blockscout-analysis` skill is compatible with the [OpenAI Codex skill format](https://developers.openai.com/codex/skills.md). The file declares UI metadata and the Blockscout MCP server dependency, enabling Codex to automatically configure the MCP server when the skill is installed.

## Reference

- [OpenAI Codex skills documentation](https://developers.openai.com/codex/skills.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI skills warehouse](https://github.com/openai/skills) — canonical examples under `skills/.curated/*/agents/openai.yaml`

## `interface`

| Field | Value | Rationale |
|-------|-------|-----------|
| `display_name` | `"Blockscout Analysis"` | Human-readable form of skill name |
| `short_description` | `"Analyze blockchain data across EVM chains"` (41 chars) | Within the 25-64 char guideline |
| `default_prompt` | Omitted | User must always specify what to analyze |
| Icons | Omitted | No asset files exist yet; add `icon_small`/`icon_large` when assets are created |

## `dependencies.tools`

Single MCP server dependency for the Blockscout MCP Server.

| Field | Value | Rationale |
|-------|-------|-----------|
| `value` | `"blockscout"` | Canonical identifier for the Blockscout MCP server across all platform configurations |
| `description` | `"Blockscout MCP server"` | Follows the `"<Name> MCP server"` convention |
| `transport` | `"streamable_http"` | Standard for HTTP-based MCP servers |
| `url` | `"https://mcp.blockscout.com/mcp"` | Must match the URL in SKILL.md |

## Expected Output

```yaml
interface:
  display_name: "Blockscout Analysis"
  short_description: "Analyze blockchain data across EVM chains"

dependencies:
  tools:
    - type: "mcp"
      value: "blockscout"
      description: "Blockscout MCP server"
      transport: "streamable_http"
      url: "https://mcp.blockscout.com/mcp"
```
