#!/usr/bin/env bash
set -euo pipefail

# Publish Codex plugins to a dedicated branch.
#
# Usage: publish-codex-plugins.sh [<source-ref>] [<target-branch>]
#   source-ref     defaults to "main" (also accepts tags like vX.Y.Z)
#   target-branch  defaults to "codex-plugins"
#
# Env:
#   REMOTE         git remote to push to (default: origin)

SOURCE_REF="${1:-main}"
TARGET_BRANCH="${2:-codex-plugins}"
REMOTE="${REMOTE:-origin}"

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

git rev-parse --verify "$SOURCE_REF^{commit}" >/dev/null 2>&1 \
  || { echo "Error: source ref '$SOURCE_REF' not found" >&2; exit 1; }

STAGE_DIR="$(mktemp -d -t codex-plugins-stage.XXXXXX)"
WORKTREE_DIR="$(mktemp -d -t codex-plugins-wt.XXXXXX)"
# mktemp -d created an empty dir; remove it so `git worktree add` can use the path
rmdir "$WORKTREE_DIR"

cleanup() {
  rm -rf "$STAGE_DIR"
  if [[ -e "$WORKTREE_DIR" ]]; then
    git worktree remove -f "$WORKTREE_DIR" 2>/dev/null || rm -rf "$WORKTREE_DIR"
  fi
  git worktree prune >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Resolve a relative symlink target against a base directory (both repo-relative),
# normalizing '.' and '..'. Fails if the path escapes the repo root or is absolute.
resolve_path() {
  local base="$1" target="$2"
  if [[ "$target" = /* ]]; then
    echo "Error: absolute symlink target '$target' is not allowed" >&2
    exit 1
  fi
  local combined="$base/$target"
  local IFS='/'
  read -ra parts <<< "$combined"
  local stack=()
  local p
  for p in "${parts[@]}"; do
    case "$p" in
      ''|'.') ;;
      '..')
        if [[ ${#stack[@]} -eq 0 ]]; then
          echo "Error: symlink target '$target' from '$base' escapes repo root" >&2
          exit 1
        fi
        unset 'stack[${#stack[@]}-1]'
        ;;
      *) stack+=("$p") ;;
    esac
  done
  local out=""
  for p in "${stack[@]}"; do
    out+="/$p"
  done
  printf '%s\n' "${out#/}"
}

# Recursively copy committed content from a path within SOURCE_REF to a destination
# directory on disk, dereferencing symlinks. Fails on broken symlinks, submodules,
# absolute symlinks, or anything outside the committed tree.
copy_committed() {
  local src_path="$1" dst_path="$2"
  src_path="${src_path#./}"
  src_path="${src_path%/}"

  local entries
  entries="$(git ls-tree -r "$SOURCE_REF" -- "$src_path" 2>/dev/null || true)"

  if [[ -z "$entries" ]]; then
    echo "Error: '$src_path' has no committed content at $SOURCE_REF (broken symlink target?)" >&2
    exit 1
  fi

  local line meta path mode hash rel out link_target link_dir resolved
  while IFS=$'\t' read -r meta path; do
    mode="${meta%% *}"
    hash="${meta##* }"

    if [[ "$path" == "$src_path" ]]; then
      rel=""
    else
      rel="${path#"$src_path"/}"
    fi
    if [[ -z "$rel" ]]; then
      out="$dst_path"
    else
      out="$dst_path/$rel"
    fi

    case "$mode" in
      100644|100755)
        mkdir -p "$(dirname "$out")"
        git cat-file blob "$hash" > "$out"
        if [[ "$mode" == "100755" ]]; then chmod +x "$out"; fi
        ;;
      120000)
        link_target="$(git cat-file blob "$hash")"
        link_dir="$(dirname "$path")"
        resolved="$(resolve_path "$link_dir" "$link_target")"
        copy_committed "$resolved" "$out"
        ;;
      160000)
        echo "Error: submodule at '$path' is not supported in plugin trees" >&2
        exit 1
        ;;
      *)
        echo "Error: unsupported tree entry mode $mode at '$path'" >&2
        exit 1
        ;;
    esac
  done <<< "$entries"
}

echo "Assembling plugins from $SOURCE_REF..."

mkdir -p "$STAGE_DIR/plugins" "$STAGE_DIR/.agents/plugins"

# Discover plugin directories (immediate trees under .agents/plugins/ at SOURCE_REF)
PLUGIN_PATHS=()
while IFS= read -r p; do
  PLUGIN_PATHS+=("$p")
done < <(
  git ls-tree "$SOURCE_REF" -- ".agents/plugins/" \
    | awk -F'\t' '{ split($1, a, " "); if (a[2]=="tree") print $2 }'
)

if [[ ${#PLUGIN_PATHS[@]} -eq 0 ]]; then
  echo "Error: no plugin directories found under .agents/plugins/ at $SOURCE_REF" >&2
  exit 1
fi

for plugin_path in "${PLUGIN_PATHS[@]}"; do
  plugin_name="$(basename "$plugin_path")"
  echo "  - $plugin_name"
  copy_committed "$plugin_path" "$STAGE_DIR/plugins/$plugin_name"
done

# Copy .agents/plugins/marketplace.json verbatim
marketplace_hash="$(git ls-tree "$SOURCE_REF" -- ".agents/plugins/marketplace.json" | awk '{print $3}')"
[[ -n "$marketplace_hash" ]] \
  || { echo "Error: .agents/plugins/marketplace.json not committed at $SOURCE_REF" >&2; exit 1; }
git cat-file blob "$marketplace_hash" > "$STAGE_DIR/.agents/plugins/marketplace.json"

# README
cat > "$STAGE_DIR/README.md" <<EOF
# Blockscout AI — Codex Plugins

This branch holds the packaged Codex plugins for the Blockscout AI marketplace.
It is generated from \`$SOURCE_REF\`. Do not edit by hand.

Install in Codex:

\`\`\`
codex plugin marketplace add blockscout/agent-skills
\`\`\`
EOF

# Determine target branch state
local_exists=false
remote_exists=false
git show-ref --verify --quiet "refs/heads/$TARGET_BRANCH" && local_exists=true
git ls-remote --exit-code --heads "$REMOTE" "$TARGET_BRANCH" >/dev/null 2>&1 && remote_exists=true

if $local_exists; then
  echo "Checking out existing local branch $TARGET_BRANCH..."
  git worktree add "$WORKTREE_DIR" "$TARGET_BRANCH"
elif $remote_exists; then
  echo "Fetching $REMOTE/$TARGET_BRANCH..."
  git fetch "$REMOTE" "$TARGET_BRANCH:$TARGET_BRANCH"
  git worktree add "$WORKTREE_DIR" "$TARGET_BRANCH"
else
  echo "Creating new orphan branch $TARGET_BRANCH..."
  git worktree add --detach "$WORKTREE_DIR" "$SOURCE_REF"
  git -C "$WORKTREE_DIR" checkout --orphan "$TARGET_BRANCH"
  git -C "$WORKTREE_DIR" rm -rf . >/dev/null 2>&1 || true
fi

# Force the worktree tree to exactly match the staged content
find "$WORKTREE_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cp -R "$STAGE_DIR/." "$WORKTREE_DIR/"

git -C "$WORKTREE_DIR" add -A

if git -C "$WORKTREE_DIR" diff --cached --quiet; then
  echo "No changes — $TARGET_BRANCH is already up to date with $SOURCE_REF."
  exit 0
fi

SOURCE_SHA="$(git rev-parse --short=7 "$SOURCE_REF^{commit}")"
commit_msg="Sync codex plugins from $SOURCE_REF ($SOURCE_SHA)"
git -C "$WORKTREE_DIR" -c user.useConfigOnly=false commit -m "$commit_msg"

echo "Pushing $TARGET_BRANCH to $REMOTE..."
if $remote_exists; then
  git -C "$WORKTREE_DIR" push "$REMOTE" "$TARGET_BRANCH"
else
  git -C "$WORKTREE_DIR" push -u "$REMOTE" "$TARGET_BRANCH"
fi

echo "Done. $TARGET_BRANCH updated from $SOURCE_REF."
