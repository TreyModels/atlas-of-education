#!/usr/bin/env python3
"""Append one job record to a run's manifest.jsonl from environment variables.

Called by run_gpu_jobs_fixed.sh after every job attempt (success or failure).
Kept separate from the bash harness so JSON escaping/typing is done once, in
Python, and so the record schema is explicit.

Environment (all strings; empty -> null):
    JOB_RUN_ID JOB_MODE JOB_ID JOB_SCRIPT JOB_SCRIPT_SHA JOB_CONFIG
    JOB_CONFIG_SHA JOB_SEED JOB_COMMAND JOB_OUTPUT JOB_OUTPUT_SHA
    JOB_EXIT JOB_WALL JOB_WORKERS JOB_STARTED JOB_ENDED JOB_ERROR
"""
from __future__ import annotations

import json
import os
import sys


def get(name: str) -> str | None:
    v = os.environ.get(name, "")
    return v if v != "" else None


def main() -> int:
    path = sys.argv[1]
    rec = {
        "run_id": get("JOB_RUN_ID"),
        "mode": get("JOB_MODE"),
        "job_id": get("JOB_ID"),
        "script": get("JOB_SCRIPT"),
        "script_sha256": get("JOB_SCRIPT_SHA"),
        "config": get("JOB_CONFIG"),
        "config_sha256": get("JOB_CONFIG_SHA"),
        "seed": int(get("JOB_SEED")) if get("JOB_SEED") is not None else None,
        "command": get("JOB_COMMAND"),
        "output": get("JOB_OUTPUT"),
        "output_sha256": get("JOB_OUTPUT_SHA"),
        "exit_code": int(get("JOB_EXIT")) if get("JOB_EXIT") is not None else None,
        "wall_time_sec": float(get("JOB_WALL")) if get("JOB_WALL") is not None else None,
        "worker_count": int(get("JOB_WORKERS")) if get("JOB_WORKERS") is not None else None,
        "started_utc": get("JOB_STARTED"),
        "ended_utc": get("JOB_ENDED"),
        "error": get("JOB_ERROR"),
    }
    line = json.dumps(rec, sort_keys=True) + "\n"
    # Single O_APPEND write: one intact JSON line per attempt.
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, line.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
