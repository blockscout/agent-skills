## Chainscout API

Base URL: `https://chains.blockscout.com/api`

### Chain Registry

#### /chains/{chain_id}

Returns the descriptor for the specified chain, including the Blockscout explorer URL in the `explorers` array. Use `explorers[].url` where `explorers[].hostedBy` is `"blockscout"` to obtain the Blockscout instance URL.

- **Parameters**

  | Name | Type | Required | Description |
  | ---- | ---- | -------- | ----------- |
  | `chain_id` | `string` | Yes | Numeric chain ID of the target network (e.g. `42161` for Arbitrum One). Obtain valid IDs from the `get_chains_list` MCP tool. |
