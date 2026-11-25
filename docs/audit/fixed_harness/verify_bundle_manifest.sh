#!/usr/bin/env bash
# Verify the frozen GPU-bundle snapshot against its canonical MANIFEST.sha256 and
# compute a whole-directory digest (used as a before/after integrity witness).
#
# READ-ONLY: this script never writes inside the bundle.
#
# Usage:
#   verify_bundle_manifest.sh [--bundle DIR] [--out FILE] [--python PY]
# Prints the bundle directory digest on stdout; writes a JSON record when --out is
# given (atomically, tmp+rename); exits 0 iff every MANIFEST entry verifies.
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BUNDLE=${BUNDLE_DIR:-"$HERE/../gpu_abc_bundle"}
OUT=""
PYTHON=${PYTHON:-python3}

while [ $# -gt 0 ]; do
  case "$1" in
    --bundle) BUNDLE=$2; shift 2 ;;
    --out) OUT=$2; shift 2 ;;
    --python) PYTHON=$2; shift 2 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[ -d "$BUNDLE" ] || { echo "FATAL: bundle dir not found: $BUNDLE" >&2; exit 2; }
[ -f "$BUNDLE/MANIFEST.sha256" ] || { echo "FATAL: MANIFEST.sha256 missing in $BUNDLE" >&2; exit 2; }

cd "$BUNDLE"
if command -v sha256sum >/dev/null 2>&1; then
  HASH_CMD=(sha256sum)
elif command -v shasum >/dev/null 2>&1; then
  HASH_CMD=(shasum -a 256)
else
  echo "FATAL: neither sha256sum nor shasum available" >&2; exit 2
fi
CHECK_CMD=("${HASH_CMD[@]}" -c MANIFEST.sha256)

set +e
CHECK_OUTPUT=$("${CHECK_CMD[@]}" 2>&1)
CHECK_RC=$?
set -e

# Whole-directory digest (sorted path order; includes MANIFEST/ORIGINS/README).
DIGEST=$(
  find . -type f -print0 | LC_ALL=C sort -z | xargs -0 "${HASH_CMD[@]}" | "${HASH_CMD[@]}" | awk '{print $1}'
)
FILE_COUNT=$(find . -type f | wc -l | tr -d ' ')

if [ -n "$OUT" ]; then
  mkdir -p "$(dirname "$OUT")"
  BUNDLE="$BUNDLE" OUT="$OUT" DIGEST="$DIGEST" FILE_COUNT="$FILE_COUNT" \
  CHECK_RC="$CHECK_RC" CHECK_OUTPUT="$CHECK_OUTPUT" CHECK_CMD="${CHECK_CMD[*]}" \
  "$PYTHON" - <<'PY'
import json, os, time

payload = {
    "checked_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "bundle_dir": os.path.abspath(os.environ["BUNDLE"]),
    "manifest": "MANIFEST.sha256",
    "check_command": os.environ["CHECK_CMD"],
    "manifest_entries_ok": os.environ["CHECK_RC"] == "0",
    "check_exit_code": int(os.environ["CHECK_RC"]),
    "check_output": os.environ["CHECK_OUTPUT"].splitlines(),
    "bundle_file_count": int(os.environ["FILE_COUNT"]),
    "bundle_dir_digest_sha256": os.environ["DIGEST"],
    "note": "bundle directory digest = sha256 of the sorted sha256sum listing of every file; used as a before/after mutation witness",
}
out = os.environ["OUT"]
tmp = f"{out}.tmp.{os.getpid()}"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, sort_keys=True)
    f.write("\n")
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, out)
PY
fi

echo "bundle_file_count=$FILE_COUNT"
echo "manifest_rc=$CHECK_RC"
echo "bundle_dir_digest_sha256=$DIGEST"
printf '%s\n' "$CHECK_OUTPUT" >&2

if [ "$CHECK_RC" -ne 0 ]; then
  echo "FATAL: canonical MANIFEST.sha256 verification FAILED" >&2
  exit 1
fi
echo "MANIFEST.sha256: OK ($FILE_COUNT files, digest ${DIGEST:0:16}...)"
