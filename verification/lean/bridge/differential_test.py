#!/usr/bin/env python3
"""Lean <-> Python differential-test bridge (exact-arithmetic fixtures only).

Runs the Lean executable witness (`lake env lean bridge/lean_witness.lean`), parses its
JSON lines, and compares each value with `fixtures.json` exactly (no tolerances on the exact
legs). Writes a hashed result JSON and exits 0 only if every fixture matches.

This tests the *reference definitions against their Lean proofs*; it is not a proof that the
Python engine is correct. Engine-level fixtures are added once the engine emits exact encodings
(see docs/audit/LEAN_VERIFICATION_SCOPE.md section 4).
"""
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    fixtures = json.load(open(os.path.join(HERE, "fixtures.json"), encoding="utf-8"))
    env = dict(os.environ)
    # Prefer an elan-managed toolchain if lake/lean are not on PATH.
    tb = os.path.expanduser("~/.elan/toolchains/leanprover--lean4---v4.36.0/bin")
    if os.path.isdir(tb):
        env["PATH"] = tb + os.pathsep + env.get("PATH", "")
    started = time.time()
    proc = subprocess.run(["lake", "env", "lean", "--run", os.path.join(HERE, "lean_witness.lean")],
                          cwd=PROJECT, capture_output=True, text=True, env=env, timeout=600)
    results = []
    values = {}
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        rec = json.loads(line)
        values[rec["key"]] = rec["value"]
    ok = True
    for fx in fixtures["fixtures"]:
        got = values.get(fx["key"])
        match = got == fx["expected"]
        ok = ok and match
        results.append({"key": fx["key"], "expected": fx["expected"], "lean": got,
                        "match": match, "contract": fx["contract"]})
    report = {
        "schema": 1,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lean_exit_code": proc.returncode,
        "lean_stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
        "lean_stderr": proc.stderr.splitlines()[-10:],
        "fixtures_sha256": sha256_file(os.path.join(HERE, "fixtures.json")),
        "witness_sha256": sha256_file(os.path.join(HERE, "lean_witness.lean")),
        "elapsed_sec": round(time.time() - started, 2),
        "comparisons": results,
        "passed": ok and proc.returncode == 0,
    }
    out = os.path.join(HERE, "differential_result.json")
    tmp = out + f".tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, out)
    print(json.dumps(report, indent=2))
    print("DIFFERENTIAL BRIDGE:", "PASS" if report["passed"] else "FAIL")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
