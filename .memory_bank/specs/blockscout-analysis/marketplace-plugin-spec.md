# Claude Code Marketplace Plugin Entry — Specification

## Purpose

Declare the `blockscout-analysis` skill as a plugin entry in the Claude Code marketplace manifest (`.claude-plugin/marketplace.json`), bundling the Blockscout MCP server so that Claude Code users can discover, install, and immediately use the skill with a pre-configured MCP connection.

## Reference

- [Claude Code plugin marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces.md)
- [Claude Code plugins reference — plugin manifest schema](https://code.claude.com/docs/en/plugins-reference.md)
- [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp.md)
- [Anthropic skills marketplace.json](https://github.com/anthropics/skills/blob/main/.claude-plugin/marketplace.json) — reference for the monorepo pattern

## Design Decisions

### Monorepo pattern

The marketplace uses the same pattern as the [Anthropic skills repository](https://github.com/anthropics/skills): a single `marketplace.json` defines all plugins without per-plugin `plugin.json` files. This is achieved through:

| Field | Value | Rationale |
|-------|-------|-----------|
| `strict` | `false` | The marketplace entry is the entire plugin definition; no `plugin.json` is needed in the skill directory |
| `source` | `"./blockscout-analysis/"` | Points directly to the skill directory — only this directory is copied to the plugin cache, minimizing footprint |
| `skills` | `["./"]` | The plugin root (i.e., the skill directory itself) is the skill — it contains `SKILL.md` at its root |

### Inline MCP server configuration

The Blockscout MCP server is declared inline in the plugin entry rather than in a separate `.mcp.json` file. This keeps the plugin self-contained with no extra config files.

| Field | Value | Rationale |
|-------|-------|-----------|
| `type` | `"http"` | Required by the Claude Code schema for HTTP-based MCP servers |
| `url` | `"https://mcp.blockscout.com/mcp"` | The native MCP endpoint; must match the URL documented in `SKILL.md` |

## Plugin Entry Fields

| Field | Value | Rationale |
|-------|-------|-----------|
| `name` | `"blockscout-analysis"` | Matches the skill directory name and `SKILL.md` frontmatter `name` |
| `description` | `"Rules, execution strategies, and conventions for ad-hoc blockchain data analysis and building tools, scripts, and applications that query the Blockscout API."` | Human-facing marketplace description; focuses on what the plugin provides rather than agent invocation directives |
| `source` | `"./blockscout-analysis/"` | Relative path within the monorepo |
| `strict` | `false` | No per-plugin `plugin.json` |
| `version` | `"0.2.0"` | Must track the skill version in `SKILL.md` frontmatter `metadata.version` |
| `author.name` | `"Blockscout"` | Publisher identity |
| `homepage` | `"https://blockscout.com"` | Blockscout project homepage |
| `repository` | `"https://github.com/blockscout/agent-skills"` | Source code repository |
| `license` | `"MIT"` | Must match `SKILL.md` frontmatter `license` |
| `keywords` | `["blockchain", "data", "evm", "contract", "address", "wallet", "web3", "defi", "blockscout", "transaction", "ens", "token", "analysis", "development", "api"]` | Discovery keywords for marketplace search |
| `category` | `"data"` | Custom category distinguishing data-focused plugins from general development tooling |
| `skills` | `["./"]` | Single skill at the plugin root |
| `mcpServers` | See [inline MCP server configuration](#inline-mcp-server-configuration) | Bundled Blockscout MCP server |

## Expected Output

The plugin entry in `.claude-plugin/marketplace.json`:

```json
{
  "name": "blockscout-analysis",
  "description": "Rules, execution strategies, and conventions for ad-hoc blockchain data analysis and building tools, scripts, and applications that query the Blockscout API.",
  "source": "./blockscout-analysis/",
  "strict": false,
  "version": "0.2.0",
  "author": {
    "name": "Blockscout"
  },
  "homepage": "https://blockscout.com",
  "repository": "https://github.com/blockscout/agent-skills",
  "license": "MIT",
  "keywords": ["blockchain", "data", "evm", "contract", "address", "wallet", "web3", "defi", "blockscout", "transaction", "ens", "token", "analysis", "development", "api"],
  "category": "data",
  "skills": ["./"],
  "mcpServers": {
    "blockscout": {
      "type": "http",
      "url": "https://mcp.blockscout.com/mcp"
    }
  }
}
```
