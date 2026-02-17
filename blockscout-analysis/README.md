# Blockscout Analysis Skill

A modular Claude Code skill for blockchain activity analysis using the Blockscout infrastructure ecosystem. It guides AI agents through on-chain data retrieval, filtering, and transformation across 270+ EVM-compatible chains.

## Goal

Enable AI agents to answer blockchain questions — about addresses, transactions, tokens, contracts, and chain-specific data — by selecting the right Blockscout instrument, querying it efficiently, and transforming verbose API responses into LLM-friendly output.

## Key Ideas

### Three instruments, one decision framework

The skill orchestrates three complementary data sources:

1. **MCP Server REST API** (`mcp.blockscout.com/v1/`) — 16 LLM-friendly tools covering the most common queries (address info, transactions, tokens, blocks, contracts). Responses are pre-filtered and enriched (e.g., address info includes first transaction timestamp, ENS name, metadata tags). No authentication required. Used by default in scripts.

2. **PRO API** (`api.blockscout.com`) — Full Blockscout REST/RPC API with 100+ endpoints. Returns raw JSON that scripts must filter for LLM consumption. Requires `$BLOCKSCOUT_API_KEY`. Used as a fallback when MCP lacks coverage, or when 50-item pages are needed (vs MCP's 10).

3. **Supporting Services** — Specialized microservices for data not available through the main API: BENS (batch ENS resolution), Metadata (address tags, reputation), Chainscout (chain registry with explorer URLs), Stats (historical counters), Multichain Aggregator (cross-chain search).

A quick decision table in `SKILL.md` maps every data need to the right instrument. The agent reads only the relevant supporting docs on demand.

### Swagger caching with freshness checking

PRO API endpoints are documented in large Swagger/OpenAPI YAML files (10,000+ lines). The skill includes:

- **`swagger-indexer.py`** — a deterministic Python script that parses swagger files into compact index files (`METHOD /path | summary | line_start-line_end`). The agent greps the index to find endpoints, then reads only the relevant line range from the cached swagger for full parameter/response details.

- **`swagger-freshness.sh`** — compares the cached swagger version against the latest Blockscout release on GitHub. Reports `CURRENT` or `STALE` with actionable next steps.

As an alternative to swagger, agents can probe endpoints directly via HTTP and inspect the response structure.

### Modular documentation

The skill follows a hub-and-spoke pattern. `SKILL.md` (~200 lines) contains the decision table and quick references. Seven supporting docs in `docs/` provide deep detail on specific topics — the agent loads only what's needed for the current task.

## Directory Structure

```
blockscout-analysis/
├── SKILL.md                                # Main entry: decision table, quick references, workflow
├── README.md                               # This file
├── .gitignore                              # Ignores cache/
├── docs/
│   ├── infrastructure-overview.md          # Architecture diagram, instrument comparison, swagger repo map
│   ├── mcp-server-guide.md                 # 16 MCP tools with REST URLs, params, pagination, strategies
│   ├── pro-api-guide.md                    # PRO API auth, URL patterns, endpoint discovery, examples
│   ├── services-guide.md                   # BENS, Metadata, Chainscout, Stats, Multichain Aggregator
│   ├── decision-framework.md              # Decision tree, trade-off matrix, when to use what
│   ├── swagger-caching-and-indexing.md     # Fetch, cache, index, freshness-check workflow
│   └── chain-specific-endpoints.md         # Full direct_api_call endpoint catalog by chain family
├── scripts/
│   ├── swagger-indexer.py                  # YAML → index generator (PyYAML or regex-only fallback)
│   └── swagger-freshness.sh               # Checks cached version against latest GitHub release
└── cache/                                  # Created at runtime, gitignored
    ├── swaggers/                           # Cached swagger YAML files
    ├── indexes/                            # Generated .idx index files
    └── .version                            # Tracks cached Blockscout version (e.g. "9.3.5")
```

## Configuration

- **PRO API key**: set `$BLOCKSCOUT_API_KEY` environment variable (`proapi_xxxxxxxx` format)
- **Native MCP server**: for interactive tasks like contract analysis, configure `https://mcp.blockscout.com/mcp` as an MCP server in your agent environment
