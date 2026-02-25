# Blockscout Agent Skills

A collection of AI agent skills for working with the Blockscout ecosystem — blockchain explorers, APIs, and supporting services.

Each skill is a self-contained directory of structured instructions and helper scripts that give an AI agent domain expertise in a specific area. Skills follow the markdown-based format compatible with Claude Code, Codex, Cursor, OpenClaw, Claude Cowork, and other agents that support skill/instruction loading.

## Skills

| Skill | Description |
|-------|-------------|
| [blockscout-analysis](blockscout-analysis/) | Modular skill for blockchain data analysis and scripting using the Blockscout MCP Server. Guides agents to use native tools, REST API scripts, or hybrid flows for multi-chain EVM data. |

## Setup

Each skill is a directory with a `SKILL.md` entry point and supporting docs/scripts. Integration depends on your agent platform.

See each skill's README for required environment variables and configuration.

## Packaging

To create a distributable zip of a skill:

```sh
bash tools/package.sh <skill-directory>
```

This produces `<skill-directory>.zip` containing all tracked files except `.gitignore` and `README.md`.

## License

[MIT](LICENSE)
