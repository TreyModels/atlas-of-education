#!/usr/bin/env python3
"""Run the ten equation-suite scripts: smoke pass first, then the full pass.

Records per-script status, wall time, stdout/stderr tails and sha256 of script + output JSON in
results/run_all.json and results/run_all_manifest.csv. No server shutdown, no destructive action.
"""
import argparse, json, multiprocessing as mp, os, platform, subprocess, sys, time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)
SCRIPTS = [
    "eq01_family_demand.py", "eq02_supply_finance.py", "eq03_learning_quality.py",
    "eq04_transitions_gates.py", "eq05_returns_credentials.py",
    "eq06_migration_rural_urban.py", "eq07_inequality_dashboard.py",
    "eq08_growth.py", "eq09_identification.py", "eq10_tutoring_shadow.py",
]


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_one(script, smoke, outdir):
    cmd = [sys.executable, os.path.join(HERE, script), "--outdir", outdir]
    if smoke:
        cmd.append("--smoke")
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                                MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1"))
    dt = time.time() - t0
    name = script[:-3]
    outp = os.path.join(outdir, name + ".json")
    return {
        "script": script, "phase": "smoke" if smoke else "full",
        "status": "PASS" if p.returncode == 0 else "FAIL",
        "returncode": p.returncode, "wall_s": round(dt, 2),
        "stdout_tail": p.stdout.strip().splitlines()[-3:],
        "stderr_tail": p.stderr.strip().splitlines()[-5:],
        "output_json": outp, "output_sha256": sha256(outp) if os.path.exists(outp) else None,
        "script_sha256": sha256(os.path.join(HERE, script)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-only", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--outdir", default=os.path.join(REC, "results"))
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    start = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    t0 = time.time()
    manifest = {"label": "SIMULATION/known-truth equation suite (no causal claims)",
                "host": platform.node(), "python": sys.version.split()[0],
                "numpy": __import__("numpy").__version__, "nproc": os.cpu_count(),
                "workers": args.workers, "start_utc": start,
                "command": " ".join(sys.argv), "smoke": [], "full": []}

    smoke = [run_one(s, True, args.outdir) for s in SCRIPTS]
    manifest["smoke"] = smoke

    if not args.smoke_only:
        ctx = mp.get_context("fork") if hasattr(mp, "get_context") else mp
        try:
            with ctx.Pool(processes=min(args.workers, len(SCRIPTS))) as pool:
                full = pool.starmap(run_one, [(s, False, args.outdir) for s in SCRIPTS])
        except Exception as exc:  # fall back to sequential; record it
            manifest["pool_error"] = repr(exc)
            full = [run_one(s, False, args.outdir) for s in SCRIPTS]
        manifest["full"] = full

    manifest["wall_s"] = round(time.time() - t0, 2)
    manifest["end_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest["failures"] = [r["script"] for r in manifest["smoke"] + manifest["full"]
                            if r["status"] != "PASS"]
    with open(os.path.join(args.outdir, "run_all.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    with open(os.path.join(args.outdir, "run_all_manifest.csv"), "w") as f:
        f.write("phase,script,status,returncode,wall_s,script_sha256,output_sha256\n")
        for r in manifest["smoke"] + manifest["full"]:
            f.write("%s,%s,%s,%s,%s,%s,%s\n" % (r["phase"], r["script"], r["status"],
                    r["returncode"], r["wall_s"], r["script_sha256"], r["output_sha256"]))
    print(json.dumps({"wall_s": manifest["wall_s"], "failures": manifest["failures"],
                      "smoke_fail": [r["script"] for r in manifest["smoke"] if r["status"] != "PASS"],
                      "full_fail": [r["script"] for r in manifest["full"] if r["status"] != "PASS"]}, indent=1))
    return 0 if not manifest["failures"] else 1


if __name__ == "__main__":
    sys.exit(main())
