# Stats Swagger Indexer Script Specification

## 1. Purpose

A utility script that automatically discovers the latest Stats service release, downloads the Stats service swagger file from the [blockscout/swaggers](https://github.com/blockscout/swaggers) repository, and builds a JSON index mapping every API endpoint with its HTTP method, description, and line range within the source file.

## 2. Data Sources

### 2.1 Stats Releases

- **Source:** GitHub Releases API `https://api.github.com/repos/blockscout/blockscout-rs/releases`
- **Key field:** `tag_name` (e.g., `stats/v2.14.0`)
- **Filtering:** Only non-draft, non-prerelease entries whose `tag_name` starts with `stats/` are considered. The first matching entry from the response sorted by recency is the latest release.
- **Version normalization:** The `tag_name` uses a `stats/v` prefix (e.g., `stats/v2.14.0`), which must be stripped to match swagger folder naming (e.g., `2.14.0`).

### 2.2 Swagger File Download

- **URL pattern:** `https://raw.githubusercontent.com/blockscout/swaggers/master/services/stats/{version}/swagger.yaml`
- **Format:** Swagger 2.0, YAML encoding.
- **No variants:** The Stats service swagger has a single file per release (no chain-specific or feature variants).

## 3. Script Behavior

### 3.1 Step 1 — Discover Latest Release Version

1. Send a GET request to `https://api.github.com/repos/blockscout/blockscout-rs/releases` with query parameter `per_page=20`.
2. Iterate through the response entries. Select the first entry where `draft` is `false` AND `prerelease` is `false` AND `tag_name` starts with `stats/`.
3. Strip the leading `stats/v` characters from `tag_name` to obtain the version string (e.g., `stats/v2.14.0` becomes `2.14.0`).
4. Print the discovered version to stdout.

### 3.2 Step 2 — Download Swagger File

1. Download the swagger file from `https://raw.githubusercontent.com/blockscout/swaggers/master/services/stats/{version}/swagger.yaml`.
2. Save the file to `blockscout-analysis/.build/swaggers/stats-service/swagger.yaml`, creating directories as needed.
3. Print a confirmation message to stdout indicating the file was downloaded successfully.

### 3.3 Step 3 — Build Endpoint Index

1. Read and parse the downloaded file `blockscout-analysis/.build/swaggers/stats-service/swagger.yaml` using the **PyYAML** library.
2. Read the raw file as a list of lines (for line number calculation — see Section 4).
3. Iterate over all entries in the top-level `paths` object. For each path:
   - For each HTTP method defined under the path (e.g., `get`, `post`, `put`, `delete`, `patch`):
     - Extract the `description` field from the method object. If `description` is absent, use an empty string. The description value must be stored **in full without any truncation**, regardless of its length.
     - Determine the **start line** and **end line** of the method's definition block within the swagger YAML file (see Section 4).
     - Append a record to the endpoint index (see Section 5 for the index schema).
4. Save the endpoint index to `blockscout-analysis/.build/swaggers/stats-service/endpoints_map.json`.
5. Print a summary message to stdout reporting how many endpoints were indexed.

## 4. Line Number Calculation

The start and end line numbers refer to the position of each **method definition block** within the swagger YAML file.

### Definition of boundaries

- **Start line:** The line number (1-based) where the HTTP method key (e.g., `get:`, `post:`) appears.
- **End line:** The line number (1-based) of the last line belonging to that method's definition block. This is the line immediately before either the next sibling key at the same or higher indentation level, or the end of the file.

### Implementation approach

Since PyYAML's standard `safe_load` does not preserve source line numbers, the script must use the following approach:

**Raw text scanning with YAML-guided structure:**

1. Parse the YAML with `yaml.safe_load()` to extract the structured endpoint data (paths, methods, descriptions).
2. Read the raw YAML file as a list of lines.
3. For each endpoint path and method identified from the parsed data, scan the raw lines to locate the method's start and end positions:
   - Find the line matching the path key (e.g., a line starting with `  /api/v1/lines:`).
   - Within that path block, find the line matching the method key (e.g., `    get:`).
   - The end line is determined by scanning forward until a line with equal or lower indentation is found (indicating the start of the next method, next path, or a top-level key), or the end of file is reached.

Line numbers are **1-based** (first line of file is line 1).

## 5. Endpoint Index Schema (JSON)

The output file is a JSON array where each element is an object representing one endpoint. The fields of each object are:

| Field          | JSON type | Description                                                                                           |
|----------------|-----------|-------------------------------------------------------------------------------------------------------|
| `swagger_file` | string    | Relative path to the swagger file: `swagger.yaml`                                                    |
| `endpoint`     | string    | API path (e.g., `/api/v1/lines/{name}`)                                                               |
| `method`       | string    | HTTP method in uppercase (e.g., `GET`, `POST`)                                                        |
| `description`  | string    | Full, untruncated value of the `description` field from the method definition; empty string if absent |
| `start_line`   | integer   | 1-based line number where the method definition begins in the swagger file                            |
| `end_line`     | integer   | 1-based line number where the method definition ends in the swagger file                              |

### JSON formatting rules

- The root value is a JSON array (`[...]`).
- The file must be written with `indent=2` for human readability.
- Encoding: UTF-8.
- Use Python's built-in `json` module for serialization.
- The `description` field must contain the **complete, untruncated** text of the swagger `description` value. No length limit or ellipsis must ever be applied.

### Example record

```json
{
  "swagger_file": "swagger.yaml",
  "endpoint": "/api/v1/lines/{name}",
  "method": "GET",
  "description": "Gets a specific line chart by name with optional date range and resolution filtering.",
  "start_line": 42,
  "end_line": 89
}
```

### Uniqueness constraint

A record is uniquely identified by the combination of `endpoint` + `method`. Duplicate combinations must not appear in the index.

## 6. File System Layout

```
blockscout-analysis/
  .build/
    swaggers/
      stats-service/
        swagger.yaml          # Downloaded Stats service swagger
        endpoints_map.json    # The endpoint index
```

- The `.build/` directory is a generated artifact directory. The script must create it (and all subdirectories) if it does not exist.
- The script must **overwrite** existing files in `.build/swaggers-stats/` on each run (idempotent operation).

## 7. Dependencies

| Dependency | Version  | Purpose                                   |
|------------|----------|-------------------------------------------|
| Python     | >= 3.9   | Runtime                                   |
| PyYAML     | >= 6.0   | YAML parsing of swagger files             |
| requests   | >= 2.28  | HTTP requests to GitHub API and raw files |

Standard library modules used: `json`, `os`, `pathlib`.

## 8. Script Interface

- **Script location:** `.memory_bank/specs/blockscout-analysis/tools/swagger-stats-indexer.py`
- **Invocation:** `python .memory_bank/specs/blockscout-analysis/tools/swagger-stats-indexer.py`
- **Arguments:** None. The script is fully automatic.
- **Output directory:** `blockscout-analysis/.build/swaggers/stats-service/` (relative to the working directory).
- **Exit code:** `0` on success, non-zero on failure.

## 9. Error Handling

| Scenario                                              | Behavior                                                              |
|-------------------------------------------------------|-----------------------------------------------------------------------|
| GitHub API rate limit exceeded (HTTP 403)             | Print error with rate limit reset time from headers; exit with code 1 |
| No stats release found in blockscout-rs               | Print error; exit with code 1                                         |
| Swagger folder for version not found (HTTP 404)       | Print error naming the version; exit with code 1                      |
| Network error during download                         | Print error with URL and reason; exit with code 1                     |
| Swagger file is not valid YAML                        | Print error naming the file; exit with code 1                         |
| `paths` key is missing from the swagger file          | Print warning; treat as zero endpoints and write empty index array    |

## 10. Console Output

The script must print structured progress messages to stdout. Example:

```
Discovered latest Stats release: 2.14.0
Downloading swagger.yaml ... done

Indexing endpoints: 11 endpoints indexed
Saved endpoints_map.json

Complete. 11 endpoints indexed.
```

## 11. Non-Requirements

- **No tests required.** This is a utility script, not a product component.
- **No CI/CD integration.** The script is run manually.
- **No caching of GitHub API responses.** Each run fetches fresh data.
- **No authentication.** The script uses unauthenticated GitHub API access (60 requests/hour rate limit is sufficient for this use case).
- **No multi-version support.** The script processes only the latest release.
