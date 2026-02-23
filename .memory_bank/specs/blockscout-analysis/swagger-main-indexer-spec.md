# Swagger Main Indexer Script Specification

## 1. Purpose

A utility script that automatically discovers the latest Blockscout backend release, downloads all swagger file variants for that release from the [blockscout/swaggers](https://github.com/blockscout/swaggers) repository, and builds a JSON index mapping every API endpoint across all chain-specific variants.

## 2. Data Sources

### 2.1 Blockscout Releases

- **Source:** GitHub Releases API `https://api.github.com/repos/blockscout/blockscout/releases`
- **Key field:** `tag_name` (e.g., `v9.3.5`)
- **Filtering:** Only non-draft, non-prerelease entries are considered. The first matching entry from the response sorted by recency is the latest release.
- **Version normalization:** The `tag_name` uses a `v` prefix (e.g., `v9.3.5`), which must be stripped to match swagger folder naming (e.g., `9.3.5`).

### 2.2 Swagger Variant Discovery

- **Source:** GitHub Contents API `https://api.github.com/repos/blockscout/swaggers/contents/blockscout/{version}`
- **Response:** JSON array of directory entries. Each entry with `"type": "dir"` represents a swagger variant (e.g., `default`, `celo`, `arbitrum`, `ethereum`, `zksync`, etc.).
- **Variant count varies by release.** As of version 9.3.5, there are 16 variants: `arbitrum`, `blackfort`, `default`, `ethereum`, `filecoin`, `neon`, `optimism-celo`, `optimism`, `polygon_zkevm`, `rsk`, `scroll`, `shibarium`, `stability`, `zetachain`, `zilliqa`, `zksync`.

### 2.3 Swagger File Download

- **URL pattern:** `https://raw.githubusercontent.com/blockscout/swaggers/master/blockscout/{version}/{variant}/swagger.yaml`
- **Format:** OpenAPI 3.0.0, YAML encoding.

## 3. Script Behavior

### 3.1 Step 1 — Discover Latest Release Version

1. Send a GET request to `https://api.github.com/repos/blockscout/blockscout/releases` (with query parameter `per_page=10` to limit payload).
2. Iterate through the response entries. Select the first entry where `draft` is `false` AND `prerelease` is `false`.
3. Extract `tag_name` and strip the leading `v` character to obtain the version string (e.g., `v9.3.5` becomes `9.3.5`).
4. Print the discovered version to stdout.

### 3.2 Step 2 — Discover Swagger Variants

1. Send a GET request to `https://api.github.com/repos/blockscout/swaggers/contents/blockscout/{version}`.
2. If the response status is 404, abort with an error message indicating that the swagger folder for the discovered version does not exist.
3. Filter the response to entries with `"type": "dir"`.
4. Collect the `name` field from each directory entry into an ordered list.
5. Reorder the list so that `default` is the first element. All other variants follow in the order returned by the API.

### 3.3 Step 3 — Download Swagger Files

For each variant in the ordered list:

1. Download the swagger file from `https://raw.githubusercontent.com/blockscout/swaggers/master/blockscout/{version}/{variant}/swagger.yaml`.
2. Save the file to `blockscout-analysis/.build/swaggers/main-indexer/{variant}/swagger.yaml`, creating directories as needed.
3. Print a confirmation message to stdout indicating the variant was downloaded successfully.

### 3.4 Step 4 — Build Endpoint Map from Primary Variant

After downloading the `default` variant:

1. Read and parse the downloaded file `blockscout-analysis/.build/swaggers/main-indexer/default/swagger.yaml` using the **PyYAML** library.
2. Iterate over all entries in the top-level `paths` object. For each path:
   - For each HTTP method defined under the path (e.g., `get`, `post`, `put`, `delete`, `patch`):
     - Extract the `description` field from the method object. If `description` is absent, use an empty string. The description value must be stored **in full without any truncation**, regardless of its length.
     - Determine the **start line** and **end line** of the method's definition block within the swagger YAML file (see Section 4 for line number calculation).
     - Append a record to the endpoint map (see Section 5 for the map schema).
3. Save the current endpoint map to `blockscout-analysis/.build/swaggers/main-indexer/endpoints_map.json`.

### 3.5 Step 5 — Extend Map with Variant-Specific Endpoints

For each remaining variant (all variants except `default`), in order:

1. Read and parse the downloaded swagger file using PyYAML.
2. Iterate over all path+method combinations in the variant's `paths`.
3. For each path+method combination:
   - Check if this combination already exists in the endpoint map (match by endpoint path AND HTTP method).
   - If it does **not** exist, append it to the map as a new record with the variant's swagger file path, line numbers from the variant's file, and description from the variant's file.
   - If it already exists, skip it (the `default` variant's entry takes precedence).
4. After processing the variant, overwrite `blockscout-analysis/.build/swaggers/main-indexer/endpoints_map.json` with the current state of the full endpoint map.
5. Print a progress message to stdout indicating the variant was indexed and how many new unique endpoints were added.

## 4. Line Number Calculation

The start and end line numbers refer to the position of each **method definition block** within the swagger YAML file.

### Definition of boundaries

- **Start line:** The line number (1-based) where the HTTP method key (e.g., `get:`, `post:`) appears.
- **End line:** The line number (1-based) of the last line belonging to that method's definition block. This is the line immediately before either the next sibling key at the same or higher indentation level, or the end of the file.

### Implementation approach

Since PyYAML's standard `safe_load` does not preserve source line numbers, the script must use one of the following approaches:

**Recommended approach — raw text scanning with YAML-guided structure:**

1. Parse the YAML with `yaml.safe_load()` to extract the structured endpoint data (paths, methods, descriptions).
2. Read the raw YAML file as a list of lines.
3. For each endpoint path and method identified from the parsed data, scan the raw lines to locate the method's start and end positions:
   - Find the line matching the path key (e.g., a line starting with `  /v2/blocks/...:`).
   - Within that path block, find the line matching the method key (e.g., `    get:`).
   - The end line is determined by scanning forward until a line with equal or lower indentation is found (indicating the start of the next method, next path, or a top-level key), or the end of file is reached.

Line numbers are **1-based** (first line of file is line 1).

## 5. Endpoint Map Schema (JSON)

The output file is a JSON array where each element is an object representing one endpoint. The fields of each object are:

| Field           | JSON type | Description                                                                                           |
|-----------------|-----------|-------------------------------------------------------------------------------------------------------|
| `swagger_file`  | string    | Relative path to the swagger file (e.g., `default/swagger.yaml`)                                     |
| `endpoint`      | string    | API path (e.g., `/v2/blocks/{block_hash_or_number_param}`)                                            |
| `method`        | string    | HTTP method in uppercase (e.g., `GET`, `POST`)                                                        |
| `description`   | string    | Full, untruncated value of the `description` field from the method definition; empty string if absent |
| `start_line`    | integer   | 1-based line number where the method definition begins in the swagger file                            |
| `end_line`      | integer   | 1-based line number where the method definition ends in the swagger file                              |

### JSON formatting rules

- The root value is a JSON array (`[...]`).
- The file must be written with `indent=2` for human readability.
- Encoding: UTF-8.
- Use Python's built-in `json` module for serialization.
- The `description` field must contain the **complete, untruncated** text of the swagger `description` value. No length limit or ellipsis must ever be applied.

### Example record

```json
{
  "swagger_file": "default/swagger.yaml",
  "endpoint": "/v2/blocks/{block_hash_or_number_param}/internal-transactions",
  "method": "GET",
  "description": "Retrieves internal transactions included in a specific block.",
  "start_line": 42,
  "end_line": 89
}
```

### Uniqueness constraint

A record is uniquely identified by the combination of `endpoint` + `method`. When processing variants beyond `default`, a new record is only added if no existing record matches both `endpoint` and `method`.

## 6. File System Layout

```
blockscout-analysis/
  .build/
    swaggers/
      main-indexer/
        default/
          swagger.yaml        # Downloaded swagger for default variant
        arbitrum/
          swagger.yaml        # Downloaded swagger for arbitrum variant
        ethereum/
          swagger.yaml        # Downloaded swagger for ethereum variant
        ...                   # One folder per variant
        endpoints_map.json    # The endpoint index (updated after each variant)
```

- The `.build/` directory is a generated artifact directory. The script must create it (and all subdirectories) if it does not exist.
- The script must **overwrite** existing files in `.build/swaggers/main-indexer/` on each run (idempotent operation).

## 7. Dependencies

| Dependency | Version   | Purpose                                   |
|------------|-----------|-------------------------------------------|
| Python     | >= 3.9    | Runtime                                   |
| PyYAML     | >= 6.0    | YAML parsing of swagger files             |
| requests   | >= 2.28   | HTTP requests to GitHub API and raw files |

Standard library modules used: `json`, `os`, `pathlib`.

## 8. Script Interface

- **Script location:** `.memory_bank/specs/blockscout-analysis/tools/swagger-main-indexer.py`
- **Invocation:** `python .memory_bank/specs/blockscout-analysis/tools/swagger-main-indexer.py`
- **Arguments:** None. The script is fully automatic.
- **Output directory:** `blockscout-analysis/.build/swaggers/main-indexer/` (relative to the working directory).
- **Exit code:** `0` on success, non-zero on failure.

## 9. Error Handling

| Scenario                                           | Behavior                                                                |
|----------------------------------------------------|-------------------------------------------------------------------------|
| GitHub API rate limit exceeded (HTTP 403)          | Print error with rate limit reset time from headers; exit with code 1   |
| Release version not found in swagger repo (HTTP 404) | Print error naming the version; exit with code 1                      |
| Network error during download                       | Print error with URL and reason; exit with code 1                      |
| Swagger file is not valid YAML                      | Print error naming the file; skip the variant and continue              |
| A variant folder has no `swagger.yaml`              | Print warning; skip the variant and continue                            |
| `paths` key is missing from a swagger file          | Print warning; treat as zero endpoints and continue                     |

## 10. Console Output

The script must print structured progress messages to stdout. Example:

```
Discovered latest Blockscout release: 9.3.5
Found 16 swagger variants: default, arbitrum, blackfort, ...

[1/16] Downloading default/swagger.yaml ... done
[1/16] Indexing default: 150 endpoints added (150 total)
        Saved endpoints_map.json

[2/16] Downloading arbitrum/swagger.yaml ... done
[2/16] Indexing arbitrum: 3 new endpoints (153 total)
        Saved endpoints_map.json

...

Complete. 165 total endpoints indexed across 16 variants.
```

## 11. Non-Requirements

- **No tests required.** This is a utility script, not a product component.
- **No CI/CD integration.** The script is run manually.
- **No caching of GitHub API responses.** Each run fetches fresh data.
- **No authentication.** The script uses unauthenticated GitHub API access (60 requests/hour rate limit is sufficient for this use case).
- **No support for multiple Blockscout versions in a single run.** The script processes only the latest release.
