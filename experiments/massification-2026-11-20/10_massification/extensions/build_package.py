#!/usr/bin/env python3
"""Build a package RUN_MANIFEST.json + SHA256SUMS.txt for a workbench directory (Lead tool).

Usage: python build_package.py <package_dir> [--status "..."]

Writes <package_dir>/RUN_MANIFEST.json first, then <package_dir>/SHA256SUMS.txt over every file
(manifest included, SHA256SUMS itself excluded) so `shasum -a 256 -c SHA256SUMS.txt` verifies.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    pkg = Path(sys.argv[1]).resolve()
    status = sys.argv[2] if len(sys.argv) > 2 else ""
    pre = pkg / "PRE_DECLARATIONS.md"
    try:
        head = subprocess.run(["git", "-C", str(pkg), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:  # noqa
        head = ""
    subs = {}
    for child in sorted(pkg.iterdir()):
        if child.is_dir() and not child.name.startswith(".") and child.name != "__pycache__":
            subs[child.name] = sorted(str(p.relative_to(pkg)) for p in child.rglob("*") if p.is_file())[:80]
    manifest = {
        "package": pkg.name,
        "status": status or "DESCRIPTIVE / SYNTHETIC — see FINDINGS.md; no causal claims",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_head": head,
        "predeclarations_sha256": sha256(pre) if pre.exists() else None,
        "files": {},
        "subdirectories": subs,
        "notes": "SHA256SUMS.txt covers every file in this package (including this manifest); it excludes only itself.",
    }
    for p in sorted(pkg.rglob("*")):
        if p.is_file() and "SHA256SUMS.txt" not in p.name:
            manifest["files"][str(p.relative_to(pkg))] = sha256(p)
    (pkg / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    # recompute manifest hash after writing it, then write sums including the manifest
    lines = []
    for p in sorted(pkg.rglob("*")):
        if not p.is_file() or p.name == "SHA256SUMS.txt":
            continue
        lines.append(f"{sha256(p)}  {p.relative_to(pkg)}")
    (pkg / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n")
    print(f"wrote {pkg/'RUN_MANIFEST.json'} and {pkg/'SHA256SUMS.txt'} ({len(lines)} entries)")


if __name__ == "__main__":
    main()
