# Blockscout Analysis

AI agent skill for blockchain data analysis and building tools that query on-chain data through the Blockscout MCP Server. Works across all EVM chains indexed by Blockscout.

## What this skill does

The skill gives an agent domain expertise in two areas:

1. **Blockchain activity analysis** — answering questions about wallets, tokens, transactions, contracts, and NFTs using the Blockscout MCP Server.
2. **Building scripts and tools** — writing and executing code that queries blockchain data via the MCP REST API for deterministic, multi-step flows.

## Key ideas

- **Single data source**: All data access goes through the Blockscout MCP Server (native MCP tools or REST API). Chainscout is used only to resolve chain IDs to Blockscout explorer URLs.
- **Data source priority**: Dedicated MCP tools first (enriched, LLM-friendly), then `direct_api_call` for endpoints not covered by dedicated tools.
- **Execution strategy**: The skill guides the agent to choose between direct tool calls, scripts (REST API), hybrid approaches, and LLM reasoning — based on task complexity and whether deterministic logic or semantic understanding is needed.
- **Multichain**: Almost all MCP tools accept a `chain_id` parameter. The agent uses `get_chains_list` to discover supported chains.

## Directory structure

```
blockscout-analysis/
├── SKILL.md                           # Agent entry point — decision framework,
│                                      #   workflow, and all behavioral instructions
├── README.md                          # This file (human overview)
├── artifacts/                         # Runtime: agent-generated ad-hoc scripts
└── references/                        # Lookup data consulted during execution
    ├── blockscout-api-index.md        # Endpoint index for direct_api_call
    ├── blockscout-api/                # Detailed endpoint parameter references
    │   ├── addresses.md
    │   ├── blocks.md
    │   ├── tokens.md
    │   ├── transactions.md
    │   ├── smart-contracts.md
    │   ├── ...                        # + chain-specific files (arbitrum, zksync, etc.)
    │   └── stats.md
    └── chainscout-api.md              # Chain registry endpoint
```

- **`SKILL.md`** is the self-contained agent entry point. An agent that reads only this file has everything it needs to behave correctly.
- **`references/`** contains API endpoint details the agent looks up during execution (e.g., to find parameters for `direct_api_call`).
- **`artifacts/`** is where the agent stores scripts it generates at runtime. Contents are gitignored.

## Setup

Integration depends on your agent platform. For **Claude Code**, symlink the skill directory into `.claude/skills/`:

```bash
ln -s /path/to/blockscout-analysis .claude/skills/blockscout-analysis
```

For optimal results, also configure the Blockscout MCP server (`https://mcp.blockscout.com/mcp`) in your agent's MCP settings. The skill can fall back to the REST API if native MCP is not available.

## License

[MIT](../LICENSE)
