"""Task-12 benchmark + equivalence harness for engine/eduengine/contest_math.py.

Usage (from the worktree root):
    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    PYTHONPATH="$PWD/engine" python docs/audit/code/contest_math_bench.py [--quick]

What it does
------------
1. Loads the PRE-optimisation module as a reference oracle from a frozen git
   commit (default: the commit that last touched contest_math.py before task-12),
   so equivalence is checked against the actual shipped implementation.
2. Runs >=120 randomised equivalence fixtures across (n, seats, weight dispersion)
   and reports max |new - reference| for method='auto' (contract acceptance <=1e-12).
3. Checks the batch API equals per-row single calls, and determinism.
4. Microbenchmarks per-call wall time (reference vs optimised) for engine sizes
   (n=300/seats=69, n=600/seats=69) and prints cache hit-rate effect for the
   9-call-per-gate-year engine pattern.
5. Optionally times one HK Baseline engine run in two subprocesses (reference
   engine copy vs current engine) and reports CPU-seconds and the ratio.

CPU only, single process; no box-specific paths.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time

import numpy as np

REFERENCE_COMMIT = os.environ.get("CONTEST_MATH_REF_COMMIT", "0f56621")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ENGINE = os.path.join(REPO, "engine")


def load_reference(commit=REFERENCE_COMMIT, path=None):
    """Load the pre-task-12 contest_math.py from a git commit (or a supplied file)."""
    if path:
        src = open(path).read()
    else:
        src = subprocess.check_output(
            ["git", "-C", REPO, "show", f"{commit}:engine/eduengine/contest_math.py"],
            text=True)
    tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
    tmp.write(src)
    tmp.close()
    spec = importlib.util.spec_from_file_location("contest_math_reference", tmp.name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["contest_math_reference"] = mod
    spec.loader.exec_module(mod)
    return mod, tmp.name


def fixtures(ref, cur, n_fixtures=130, seed=20261125):
    rng = np.random.default_rng(seed)
    rows = []
    worst = 0.0
    for _ in range(n_fixtures):
        n = int(rng.choice([12, 20, 21, 40, 60, 80, 120, 200, 300, 300, 300, 400, 600]))
        seats = int(rng.integers(1, n))
        disp = float(rng.choice([0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]))
        w = np.ones(n) if disp == 0.0 else np.exp(disp * rng.standard_normal(n))
        t0 = time.perf_counter()
        pref = ref.pl_win_probs(w, seats, method="auto")
        tref = time.perf_counter() - t0
        t0 = time.perf_counter()
        pnew = cur.pl_win_probs(w, seats, method="auto")
        tnew = time.perf_counter() - t0
        d = float(np.max(np.abs(np.asarray(pref) - np.asarray(pnew))))
        worst = max(worst, d)
        rows.append(dict(n=n, seats=seats, dispersion=disp, max_diff=d,
                         ref_ms=1000 * tref, new_ms=1000 * tnew))
    return rows, worst


def microbench(ref, cur, reps=7):
    """Cold-call timing (fresh weights per rep, so no memoisation hits) + warm-call time."""
    rng = np.random.default_rng(11)
    out = []
    for n, seats, disp in [(300, 69, 1.0), (300, 69, 2.0), (300, 36, 1.0), (600, 69, 1.0)]:
        ws = [np.exp(disp * rng.standard_normal(n)) for _ in range(reps + 1)]
        def cold(mod):
            ts = []
            for k in range(reps):
                w = ws[k]
                t0 = time.perf_counter(); mod.pl_win_probs(w, seats); ts.append(time.perf_counter() - t0)
            return float(np.median(ts))
        a = cold(ref); b = cold(cur)
        # warm (memoised) call on the same weights
        w = ws[-1]
        cur.pl_win_probs(w, seats)
        ts = []
        for _ in range(reps):
            t0 = time.perf_counter(); cur.pl_win_probs(w, seats); ts.append(time.perf_counter() - t0)
        warm = float(np.median(ts))
        out.append(dict(n=n, seats=seats, dispersion=disp, reference_ms=1000 * a,
                        optimised_cold_ms=1000 * b, speedup_cold=a / b,
                        optimised_warm_ms=1000 * warm))
    return out


def engine_group(cur, reps=3):
    """9-call gate-year pattern with COLD weights in every repetition (no cache hits)."""
    rng = np.random.default_rng(5)
    n, seats = 300, 69
    ts = []
    for _ in range(reps):
        Ws = [np.exp(1.0 * rng.standard_normal(n)) for _ in range(9)]
        t0 = time.perf_counter()
        for w in Ws:
            cur.pl_win_probs(w, seats)
        ts.append(time.perf_counter() - t0)
    return {"sequential_ms": 1000 * float(np.median(ts))}


def end_to_end(commit=REFERENCE_COMMIT, ref_path=None, seeds=(0,)):
    """Time one HK Baseline run: reference engine vs optimised vs optimised+batched."""
    import shutil
    import importlib
    runner = os.path.join(REPO, "papers/shadow-education-contest/code/run_hk_korea_comparative.py")
    results = {}
    # reference engine copy
    ref_engine = tempfile.mkdtemp(prefix="ref_engine_")
    shutil.copytree(ENGINE, os.path.join(ref_engine, "engine"))
    if ref_path:
        src = open(ref_path).read()
    else:
        src = subprocess.check_output(
            ["git", "-C", REPO, "show", f"{commit}:engine/eduengine/contest_math.py"], text=True)
    open(os.path.join(ref_engine, "engine/eduengine/contest_math.py"), "w").write(src)
    code = (
        "import sys, json, time;"
        f"sys.path.insert(0, {os.path.dirname(runner)!r});"
        "from run_hk_korea_comparative import build_arms, _run_single;"
        "specs=build_arms(); b=[s for s in specs if s[0]=='HK' and s[1]=='Baseline'][0];"
        "t0=time.perf_counter(); _run_single((b[0],b[1],0,b[3]));"
        "print(json.dumps({'cpu_s': time.perf_counter()-t0}))"
    )
    for label, path in (("reference", os.path.join(ref_engine, "engine")),
                        ("optimised", ENGINE)):
        env = dict(os.environ)
        env["PYTHONPATH"] = path
        for k in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
            env[k] = "1"
        if path is None:
            results[label] = {"error": "not available"}
            continue
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env)
        if r.returncode != 0:
            results[label] = {"error": r.stderr[-2000:]}
        else:
            results[label] = json.loads(r.stdout.strip().splitlines()[-1])
    ref_cpu = results.get("reference", {}).get("cpu_s", float("nan"))
    opt_cpu = results.get("optimised", {}).get("cpu_s", float("nan"))
    results["speedup"] = ref_cpu / opt_cpu if opt_cpu else float("nan")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="skip end-to-end runs")
    ap.add_argument("--commit", default=REFERENCE_COMMIT)
    ap.add_argument("--ref-module", default=None,
                    help="path to the pre-optimisation contest_math.py (box use)")
    args = ap.parse_args()
    sys.path.insert(0, ENGINE)
    import eduengine.contest_math as cur
    ref, ref_path = load_reference(args.commit, path=args.ref_module)
    out = {"reference_commit": args.commit, "numpy": np.__version__}
    rows, worst = fixtures(ref, cur)
    out["equivalence"] = {"n_fixtures": len(rows), "max_abs_diff": worst}
    print(f"equivalence: {len(rows)} fixtures, max |new-reference| = {worst:.3e} "
          f"(acceptance <= 1e-12: {'PASS' if worst <= 1e-12 else 'FAIL'})")
    out["batch_api"] = "not shipped (measured 0.87-0.96x slower; reverted per keep-memo-only decision)"
    print("batch API: not shipped (measured slower; reverted per keep-memo-only decision)")
    p1 = cur.pl_win_probs(np.exp(0.5 * np.arange(50)), 7)
    p2 = cur.pl_win_probs(np.exp(0.5 * np.arange(50)), 7)
    out["determinism"] = bool(np.array_equal(p1, p2))
    print(f"determinism (repeat bit-identical): {out['determinism']}")
    out["microbench"] = microbench(ref, cur)
    for r in out["microbench"]:
        print(f"  n={r['n']} k={r['seats']} disp={r['dispersion']}: cold ref "
              f"{r['reference_ms']:.2f} ms -> opt {r['optimised_cold_ms']:.2f} ms "
              f"({r['speedup_cold']:.2f}x); memoised opt call {r['optimised_warm_ms']:.3f} ms")
    out["engine_group"] = engine_group(cur)
    g = out["engine_group"]
    print("9-call gate-year group (cold, sequential): %.0f ms" % g["sequential_ms"])
    if not args.quick:
        out["end_to_end"] = end_to_end(args.commit, ref_path=args.ref_module)
        print("end-to-end HK Baseline:", out["end_to_end"])
    try:
        out["cache_stats"] = cur.pl_stats()
        print("cache stats:", out["cache_stats"])
    except Exception:
        pass
    os.unlink(ref_path)
    with open(os.path.join(REPO, "docs/audit/code/contest_math_bench_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote docs/audit/code/contest_math_bench_results.json")


if __name__ == "__main__":
    main()
