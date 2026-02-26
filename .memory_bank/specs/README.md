# Specifications

This directory contains specifications for the agent skills in this repository. Each skill has its own subdirectory with a `spec.md` file capturing the original requirements and design constraints, along with supporting specs and tools used during the skill preparation phase.

## Structure

```
specs/
└── blockscout-analysis/
    ├── spec.md                             # Main skill spec (start here)
    ├── api-file-generator-spec.md          # API reference file generator tool spec
    ├── api-format-spec.md                  # API reference file format spec
    ├── blockscout-api-composition-spec.md  # Pipeline to produce Blockscout API reference files 
    ├── chainscout-api-spec.md              # Specification for Chainscout API reference file
    ├── mcp-duplicate-removal-spec.md       # Specification for removing MCP tool duplicate endpoints from API reference files
    ├── mcp-unlock-patch-spec.md            # Specification for patching Blockscout API reference files from unlock_blockchain_analysis MCP tool
    ├── openai-yaml-spec.md                 # Specification for OpenAI Codex agent metadata (agents/openai.yaml)
    ├── rpc-api-patch-spec.md               # Specification for patching Blockscout API reference files with JSON-RPC endpoints
    ├── swagger-main-indexer-spec.md        # Specification for indexing the main Blockscout swagger
    ├── swagger-stats-indexer-spec.md       # Specification for indexing the stats Blockscout swagger
    └── tools/                              # Supporting scripts used during skill preparation
        ├── common.py                       # Shared utilities for the tools
        ├── api-file-generator.py           # Generates API reference files from indexed data
        ├── mcp-unlock-patch.py             # Patches Blockscout API reference files with unlock_blockchain_analysis MCP tool endpoints
        ├── swagger-main-indexer.py         # Indexes the main Blockscout swagger
        └── swagger-stats-indexer.py        # Indexes the Stats service swagger
```
