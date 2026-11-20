#!/usr/bin/env python3
"""Reproducibility check for code/run.py.

Runs `run.py` twice, hashes every file in `results/*.csv` after each run, and
asserts the two hash maps are identical (byte-identical CSVs). Writes
`stats/REPRO_CHECK.json` with both runs' hashes and the verdict.

The two runs necessarily differ in `RUN_MANIFEST.json`'s `run_utc` and in the
`run_utc` line of `FINDINGS.md`; that is expected and is recorded, not treated
as a failure. Only the numbered result CSVs must be byte-identical.

Usage:  python code/verify_repro.py
Exit code 0 iff the two runs are byte-identical on results/*.csv.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATS_DIR = Path(
    "/Users/treymenefee/massification_live/experiments/massification-2026-11-20/"
    "10_massification/extensions/longitudinal_2026-11-20/stats"
)
RUN = STATS_DIR / "code" / "run.py"
RESULTS = STATS_DIR / "results"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def snapshot() -> dict[str, str]:
    return {p.name: sha256(p) for p in sorted(RESULTS.glob("*.csv"))}


def one_run(tag: str) -> dict[str, str]:
    print(f"[{tag}] running {RUN} ...", flush=True)
    subprocess.run([sys.executable, str(RUN)], check=True, cwd=str(STATS_DIR))
    snap = snapshot()
    print(f"[{tag}] {len(snap)} result files hashed", flush=True)
    return snap


def main() -> int:
    run1 = one_run("run1")
    run2 = one_run("run2")
    identical = run1 == run2
    differing = sorted(k for k in set(run1) | set(run2)
                       if run1.get(k) != run2.get(k))
    out = {
        "script": str(RUN),
        "run.py_sha256": sha256(RUN),
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_result_files": len(run1),
        "identical": bool(identical),
        "differing_files": differing,
        "run1": run1,
        "run2": run2,
        "note": (
            "Both runs executed code/run.py in this directory with the same Python "
            "interpreter. Every results/*.csv was hashed after each run. `run_utc` in "
            "RUN_MANIFEST.json and FINDINGS.md differs between runs by design and is not "
            "part of this comparison."
        ),
    }
    (STATS_DIR / "REPRO_CHECK.json").write_text(
        json.dumps(out, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"identical={identical} differing={differing}")
    return 0 if identical else 1


if __name__ == "__main__":
    sys.exit(main())
