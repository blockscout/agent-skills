# Claude Code Marketplace Plugin Entry — Specification

## Purpose

Declare the `web3-dev` skill as a plugin entry in the Claude Code marketplace manifest (`.claude-plugin/marketplace.json`) so that Claude Code users can discover and install the skill that teaches the agent how to build software against the Blockscout PRO API over plain HTTP.

The plugin does **not** bundle an MCP server: `web3-dev` is a direct-HTTP integration skill and has no MCP runtime dependency.

## Reference

- [Claude Code plugin marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces.md)
- [Claude Code plugins reference — plugin manifest schema](https://code.claude.com/docs/en/plugins-reference.md)
- [Anthropic skills marketplace.json](https://github.com/anthropics/skills/blob/main/.claude-plugin/marketplace.json) — reference for the monorepo pattern

## Design Decisions

### Monorepo pattern

The marketplace uses the same pattern as the [Anthropic skills repository](https://github.com/anthropics/skills): a single `marketplace.json` defines all plugins without per-plugin `plugin.json` files. This is achieved through:

| Field | Value | Rationale |
|-------|-------|-----------|
| `strict` | `false` | The marketplace entry is the entire plugin definition; no `plugin.json` is needed in the skill directory |
| `source` | `"./web3-dev/"` | Points directly to the skill directory — only this directory is copied to the plugin cache, minimizing footprint |
| `skills` | `["./"]` | The plugin root (i.e., the skill directory itself) is the skill — it contains `SKILL.md` at its root |

### No MCP server

`web3-dev` instructs the agent to call the Blockscout PRO API over HTTP directly (using the user's `BLOCKSCOUT_PRO_API_KEY`), not through an MCP server. Therefore the plugin entry omits the `mcpServers` field entirely.

## Plugin Entry Fields

| Field | Value | Rationale |
|-------|-------|-----------|
| `name` | `"web3-dev"` | Matches the skill directory name and `SKILL.md` frontmatter `name` |
| `description` | `"Build web3 applications, scripts, CLIs, bots, and mobile/desktop clients that read blockchain data through the Blockscout PRO API — a single HTTP API spanning 100+ EVM chains."` | Human-facing marketplace description; focuses on what the plugin enables rather than agent invocation directives. Shorter than the `SKILL.md` `description`, which is tuned for skill triggering |
| `source` | `"./web3-dev/"` | Relative path within the monorepo |
| `strict` | `false` | No per-plugin `plugin.json` |
| `version` | `"0.1.0"` | Must track the skill version in `SKILL.md` frontmatter `metadata.version` |
| `author.name` | `"Blockscout"` | Publisher identity |
| `homepage` | `"https://blockscout.com"` | Blockscout project homepage |
| `repository` | `"https://github.com/blockscout/agent-skills"` | Source code repository |
| `license` | `"MIT"` | Must match `SKILL.md` frontmatter `license` |
| `keywords` | `["blockchain", "evm", "web3", "dapp", "wallet", "blockscout", "pro-api", "api", "http", "rest", "transaction", "token", "nft", "contract", "development"]` | Discovery keywords for marketplace search |
| `category` | `"development"` | Custom category marking the plugin as build-time developer tooling for HTTP-based web3 apps |
| `skills` | `["./"]` | Single skill at the plugin root |

`mcpServers` is intentionally absent — see [No MCP server](#no-mcp-server).

## Expected Output

The plugin entry in `.claude-plugin/marketplace.json`:

```json
{
  "name": "web3-dev",
  "description": "Build web3 applications, scripts, CLIs, bots, and mobile/desktop clients that read blockchain data through the Blockscout PRO API — a single HTTP API spanning 100+ EVM chains.",
  "source": "./web3-dev/",
  "strict": false,
  "version": "0.1.0",
  "author": {
    "name": "Blockscout"
  },
  "homepage": "https://blockscout.com",
  "repository": "https://github.com/blockscout/agent-skills",
  "license": "MIT",
  "keywords": ["blockchain", "evm", "web3", "dapp", "wallet", "blockscout", "pro-api", "api", "http", "rest", "transaction", "token", "nft", "contract", "development"],
  "category": "development",
  "skills": ["./"]
}
```
