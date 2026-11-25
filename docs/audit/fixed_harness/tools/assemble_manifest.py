#!/usr/bin/env python3
"""Assemble a run manifest.json from manifest.jsonl + run_meta.json + configs.

Guarantees:
  * every recorded job maps to a config entry (no silent jobs),
  * every config entry was attempted (no silently skipped experiment),
  * the final file is written atomically (tmp + os.replace),
  * the run is only marked "ok" if every recorded job has exit_code == 0.

Usage:
    assemble_manifest.py --run-dir DIR --manifest-jsonl FILE --config JOBS.json \
        --mode real|dry-run --run-id ID [--bundle DIR]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time


def atomic_write_json(path: str, payload: dict) -> None:
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--manifest-jsonl", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--mode", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--bundle", default="")
    args = ap.parse_args()

    cfg = json.load(open(args.config, encoding="utf-8"))
    cfg_by_id = {j["id"]: j for j in cfg["jobs"]}

    records = []
    with open(args.manifest_jsonl, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    errors = []
    rec_ids = [r["job_id"] for r in records]
    missing = sorted(set(cfg_by_id) - set(rec_ids))
    unknown = sorted(set(rec_ids) - set(cfg_by_id))
    if missing:
        errors.append(f"configured jobs with no attempt record: {missing}")
    if unknown:
        errors.append(f"attempt records with no config entry: {unknown}")
    if len(rec_ids) != len(set(rec_ids)):
        errors.append(f"duplicate job attempt records: {rec_ids}")
    failed = [r["job_id"] for r in records if r.get("exit_code") != 0]
    if failed:
        errors.append(f"jobs with non-zero exit: {failed}")

    # merge config metadata (evidence status / notes / archived provenance)
    jobs = []
    for r in records:
        c = cfg_by_id.get(r["job_id"], {})
        jobs.append({
            "job_id": r["job_id"],
            "evidence_status": c.get("evidence_status"),
            "configuration": r.get("config"),
            "config_sha256": r.get("config_sha256"),
            "script": r.get("script"),
            "script_sha256": r.get("script_sha256"),
            "seed": r.get("seed"),
            "command": r.get("command"),
            "output": r.get("output"),
            "output_sha256": r.get("output_sha256"),
            "exit_code": r.get("exit_code"),
            "wall_time_sec": r.get("wall_time_sec"),
            "worker_count": r.get("worker_count"),
            "started_utc": r.get("started_utc"),
            "ended_utc": r.get("ended_utc"),
            "error": r.get("error"),
        })

    run_meta = {}
    meta_path = os.path.join(args.run_dir, "run_meta.json")
    if os.path.isfile(meta_path):
        run_meta = json.load(open(meta_path, encoding="utf-8"))

    seeds_path = os.path.join(args.run_dir, "seeds.json")
    seeds = json.load(open(seeds_path, encoding="utf-8")) if os.path.isfile(seeds_path) else None

    manifest = {
        "run_id": args.run_id,
        "mode": args.mode,
        "status": "ok" if not errors else "invalid",
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run_dir": os.path.abspath(args.run_dir),
        "bundle_dir": os.path.abspath(args.bundle) if args.bundle else None,
        "jobs_config": os.path.abspath(args.config),
        "jobs_config_sha256": sha256_file(args.config),
        "seeds": seeds,
        "jobs_attempted": len(jobs),
        "jobs_succeeded": len([j for j in jobs if j["exit_code"] == 0]),
        "jobs_failed": len([j for j in jobs if j["exit_code"] != 0]),
        "bundle_digest_before": run_meta.get("bundle_digest_before"),
        "bundle_digest_after": run_meta.get("bundle_digest_after"),
        "bundle_unchanged_during_run": run_meta.get("bundle_digest_before") == run_meta.get("bundle_digest_after"),
        "errors": errors,
        "jobs": jobs,
    }
    out = os.path.join(args.run_dir, "manifest.json")
    atomic_write_json(out, manifest)
    print(f"manifest: {out} status={manifest['status']} attempts={len(jobs)} failed={manifest['jobs_failed']}")
    if errors:
        for e in errors:
            print(f"MANIFEST ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
