#!/usr/bin/env python3
"""Deliberately failing CPU-only stub for the harness failure-propagation proof.

Behaviour: it creates a *partial* temp file in the staging dir and then exits
non-zero (default 7) without renaming it into a result.  That lets the proof
check all three properties the archived runner lacked:
  * a non-zero job rc propagates to the whole run (harness aborts, run rc != 0),
  * the exact failing rc is preserved in run_failure.json,
  * no partial JSON can be mistaken for a result (atomic-rename discipline).
"""
from __future__ import annotations

import argparse
import os
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--job-id", default="stub_fail")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--exit-code", type=int, default=7)
    a = ap.parse_args()

    os.makedirs(a.out_dir, exist_ok=True)
    partial = os.path.join(a.out_dir, "result.json.tmp.partial")
    with open(partial, "w", encoding="utf-8") as f:
        f.write('{"stub": "fail", "partial": true}\n')
    print(f"stub_job_fail: simulating a crashed job (partial file {partial})", file=sys.stderr)
    print(f"stub_job_fail: intentional exit code {a.exit_code}", file=sys.stderr)
    return a.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
