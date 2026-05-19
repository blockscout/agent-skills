# Specifications

This directory contains specifications for the agent skills and supporting tooling in this repository. Each skill has its own subdirectory with a `spec.md` file capturing the original requirements and design constraints, along with supporting specs and tools used during the skill preparation phase. Repo-level tooling specs live as standalone files at the root of this directory.

## Structure

```
specs/
├── publish-codex-plugins-spec.md           # Spec for tools/publish-codex-plugins.sh — publishes plugins to the codex-plugins branch
├── blockscout-analysis/
│   ├── spec.md                             # Main skill spec (start here)
│   ├── api-file-generator-spec.md          # API reference file generator tool spec
│   ├── api-format-spec.md                  # API reference file format spec
│   ├── blockscout-api-composition-spec.md  # Pipeline to produce Blockscout API reference files
│   ├── chainscout-api-spec.md              # Specification for Chainscout API reference file
│   ├── api-extras-applier-spec.md          # Specification for patching Blockscout API reference files from the frozen extras catalog (originally snapshotted from unlock_blockchain_analysis)
│   ├── api-extras-applier-data.yaml        # Frozen catalog of direct_api_call endpoints applied by api-extras-applier.py
│   ├── mcp-duplicate-removal-spec.md       # Specification for removing MCP tool duplicate endpoints from API reference files
│   ├── marketplace-plugin-spec.md          # Specification for Claude Code marketplace plugin entry
│   ├── rpc-api-patch-spec.md               # Specification for patching Blockscout API reference files with JSON-RPC endpoints
│   ├── swagger-main-indexer-spec.md        # Specification for indexing the main Blockscout swagger
│   ├── swagger-stats-indexer-spec.md       # Specification for indexing the stats Blockscout swagger
│   └── tools/                              # Supporting scripts used during skill preparation
│       ├── common.py                       # Shared utilities for the tools
│       ├── api-file-generator.py           # Generates API reference files from indexed data
│       ├── api-extras-applier.py           # Patches Blockscout API reference files from the frozen extras catalog
│       ├── swagger-main-indexer.py         # Indexes the main Blockscout swagger
│       └── swagger-stats-indexer.py        # Indexes the Stats service swagger
└── web3-dev/
    ├── spec.md                             # Main skill spec (start here)
    ├── pro-api-indexer-spec.md             # Specification for the PRO API endpoint indexer
    └── tools/                              # Supporting scripts used during skill preparation
        └── pro-api-indexer.py              # Generates the PRO API endpoint markdown index from pro-api.json
```
