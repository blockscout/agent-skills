# Blockscout Agent Skills

A collection of AI agent skills for working with the Blockscout ecosystem — blockchain explorers, APIs, and supporting services.

Each skill is a self-contained directory of structured instructions and helper scripts that give an AI agent domain expertise in a specific area. Skills follow the markdown-based format compatible with Claude Code, Codex, Cursor, OpenClaw, Claude Cowork, and other agents that support skill/instruction loading.

## Skills

| Skill | Description |
|-------|-------------|
| [blockscout-analysis](blockscout-analysis/) | On-chain data retrieval and analysis across EVM chains where Blockscout is deployed via MCP server, PRO API, and supporting services (BENS, Metadata, Chainscout, Stats) |

## Setup

Each skill is a directory with a `SKILL.md` entry point and supporting docs/scripts. Integration depends on your agent: e.g. for **Claude Code**, symlink the skill directory into `.claude/skills/`

See each skill's README for required environment variables and configuration.

## License

[MIT](LICENSE)
