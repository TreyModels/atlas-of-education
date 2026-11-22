#!/usr/bin/env python3
"""Open, close, verify and list run records for the Minis harness.

Standard library only, no network. A run record makes every file change attributable to an
actor, an operator, a model id and a harness version (see HARNESS.md). The manifest is written
before output exists; close hashes what changed; verify re-hashes and refuses to pass on drift.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RECORDS = HERE / "records"
SCHEMA = 1
HARNESS_VERSION = "2026-11-22"
OPERATORS = ("human", "agent", "script", "ci")
HARNESSES = ("minis", "claude-code", "dsh", "hand", "lab.py", "other")
RUN_ID = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{6}Z-[a-z0-9]+-[0-9a-f]{6}$")


def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def sha256(path: Path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args, check=True):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=check).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def source_digest():
    """Hash of the tracked tree as git sees it: HEAD plus any staged/unstaged change names."""
    head = git("rev-parse", "HEAD")
    status = git("status", "--porcelain", "--untracked-files=no") or ""
    blob = json.dumps({"head": head, "status": sorted(status.splitlines())}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def changed_paths(scope):
    """Paths inside scope that differ from HEAD (staged, unstaged or untracked), repo-relative."""
    out = set()
    porcelain = git("status", "--porcelain", "-z", "--untracked-files=all") or ""
    for entry in porcelain.split("\0"):
        if not entry or len(entry) < 4:
            continue
        path = entry[3:].strip()
        if " -> " in path:  # rename: keep the new side
            path = path.split(" -> ", 1)[1]
        if any(path == s.rstrip("/") or path.startswith(s.rstrip("/") + "/") for s in scope):
            if (ROOT / path).is_file():
                out.add(path)
    return sorted(out)


def load(run_dir: Path):
    with open(run_dir / "run.json", encoding="utf-8") as fh:
        return json.load(fh)


def close_run(run_dir: Path):
    rec = load(run_dir)
    if (run_dir / "outputs.json").exists():
        raise SystemExit(f"run {rec['run_id']} is already closed")
    files = []
    for rel in changed_paths(rec["scope"]):
        p = ROOT / rel
        kind = "generated" if rel.endswith(("RUN.md", "outputs.json")) else "authored"
        files.append({"path": rel, "sha256": sha256(p), "bytes": p.stat().st_size, "kind": kind})
    out = {"schema": SCHEMA, "run_id": rec["run_id"], "files": files}
    (run_dir / "outputs.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    # RUN.md is written by make_run_md.py from run.json + outputs.json; no prose is typed here.
    subprocess.run([sys.executable, str(HERE / "make_run_md.py"), rec["run_id"], str(RECORDS)], check=True)
    return out


def verify(run_dirs):
    problems = []
    claims = {}
    for d in run_dirs:
        if not (d / "outputs.json").exists():
            problems.append(f"{d.name}: open, no outputs.json")
            continue
        data = json.loads((d / "outputs.json").read_text(encoding="utf-8"))
        for f in data["files"]:
            p = ROOT / f["path"]
            if not p.is_file():
                problems.append(f"{d.name}: missing {f['path']}")
            elif sha256(p) != f["sha256"]:
                problems.append(f"{d.name}: drift {f['path']}")
            claims.setdefault(f["path"], []).append(d.name)
    for path, runs in claims.items():
        if len(runs) > 1:
            problems.append(f"conflict {path}: claimed by {', '.join(runs)}")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    o = sub.add_parser("open", help="start a run record; refuses if output already exists")
    o.add_argument("--actor", required=True)
    o.add_argument("--operator", required=True, choices=OPERATORS)
    o.add_argument("--model", default="")
    o.add_argument("--harness", default="hand", choices=HARNESSES)
    o.add_argument("--intent", required=True)
    o.add_argument("--scope", action="append", required=True)
    o.add_argument("--session", default=None)
    o.add_argument("--network", action="append", default=[])
    o.add_argument("--notes", default="")

    c = sub.add_parser("close", help="hash changed files and write RUN.md")
    c.add_argument("--run", required=True)

    v = sub.add_parser("verify", help="re-hash closed runs; exit 1 on drift or conflict")
    v.add_argument("--run", default=None)

    l = sub.add_parser("list", help="print run ids and intents")
    l.add_argument("--open", action="store_true", help="only runs without outputs.json")

    a = ap.parse_args(argv)
    RECORDS.mkdir(parents=True, exist_ok=True)

    if a.cmd == "open":
        if a.operator != "human" and not a.model:
            raise SystemExit("a non-human operator must name its model; leave model empty only for human/script")
        if ".." in json.dumps(a.scope) or any(s.startswith("/") for s in a.scope):
            raise SystemExit("scope entries must be repo-relative")
        for s in a.scope:
            # Ignore the harness's own bookkeeping and bytecode: they are not run output.
            extraneous = [q for q in changed_paths([s])
                          if q not in ("research/minis-harness/harness.py", "research/minis-harness/make_run_md.py",
                                       "research/minis-harness/HARNESS.md", "research/minis-harness/test_harness.py")
                          and not q.startswith("research/minis-harness/records/")
                          and "__pycache__" not in q]
            if extraneous:
                raise SystemExit(f"refusing to open: {s} already has uncommitted output ({extraneous[0]}); "
                                 "commit or discard first")
        now = utc_now()
        run_id = f"{now:%Y-%m-%dT%H%M%SZ}-{a.actor.lower()}-{secrets.token_hex(3)}"
        rec = {
            "schema": SCHEMA,
            "run_id": run_id,
            "started_utc": f"{now:%Y-%m-%dT%H:%M:%SZ}",
            "actor": a.actor,
            "operator": a.operator,
            "model": a.model or None,
            "harness": a.harness,
            "harness_version": HARNESS_VERSION,
            "session": a.session,
            "intent": a.intent,
            "scope": a.scope,
            "repo_head": git("rev-parse", "HEAD"),
            "source_digest": source_digest(),
            "network": a.network,
            "notes": a.notes,
        }
        d = RECORDS / run_id
        d.mkdir()
        (d / "run.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"run_id": run_id, "dir": str(d.relative_to(ROOT))}, indent=2))
        return 0

    if a.cmd == "close":
        if not RUN_ID.match(a.run):
            raise SystemExit("not a run id")
        out = close_run(RECORDS / a.run)
        print(json.dumps({"run_id": a.run, "files": len(out["files"])}, indent=2))
        return 0

    if a.cmd == "verify":
        dirs = [RECORDS / a.run] if a.run else sorted(p for p in RECORDS.iterdir() if p.is_dir())
        problems = verify(dirs)
        for p in problems:
            print(p, file=sys.stderr)
        print(json.dumps({"runs": len(dirs), "problems": len(problems)}, indent=2))
        return 1 if problems else 0

    rows = []
    for d in sorted(p for p in RECORDS.iterdir() if p.is_dir()):
        rec = load(d)
        if a.open and (d / "outputs.json").exists():
            continue
        rows.append({"run_id": rec["run_id"], "operator": rec["operator"], "model": rec["model"],
                     "closed": (d / "outputs.json").exists(), "intent": rec["intent"]})
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
