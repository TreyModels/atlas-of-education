#!/usr/bin/env python3
"""Run the ten equation-suite scripts: smoke pass first, then the full pass.

A script's PASS/FAIL is the script's OWN decision rule (`decision_rule.PASS` in its output
JSON), not merely `returncode == 0`: a script can execute cleanly and still fail its
pre-declared or implemented rule, and that must be visible here (Neon line audit / task-47
audit: "run_all.py treated returncode 0 as a pass"). Per-script rule flags are recorded too
(e.g. the S10 Tobit flag) so a decision-rule failure can be traced to a sub-test.

Records per-script execution status, decision-rule verdict, wall time, stdout/stderr tails
and sha256 of script + output JSON in results/run_all.json and results/run_all_manifest.csv.
No server shutdown, no destructive action.
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


def read_decision_rule(outp):
    """Read the script's own decision_rule block from its JSON output.

    Returns {"decision_rule_pass": bool|None, "rule_flags": {...}, "rule_error": str|None}.
    The verdict is the script's `decision_rule.PASS`, never the process exit code.
    """
    res = {"decision_rule_pass": None, "rule_flags": {}, "rule_error": None}
    if not os.path.exists(outp):
        res["rule_error"] = "output JSON missing"
        return res
    try:
        with open(outp) as f:
            obj = json.load(f)
    except Exception as exc:  # unreadable / invalid JSON must fail the run, not pass quietly
        res["rule_error"] = "unreadable output JSON: %r" % (exc,)
        return res
    dr = obj.get("decision_rule")
    if not isinstance(dr, dict) or "PASS" not in dr:
        res["rule_error"] = "no decision_rule.PASS in output JSON"
        return res
    res["decision_rule_pass"] = bool(dr["PASS"])
    # sub-test flags (e.g. eq10's tobit flag) so a rule failure is traceable
    res["rule_flags"] = {k: v for k, v in dr.items() if k != "PASS"}
    return res


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
    if p.returncode != 0:
        execution_status = "FAIL"
    else:
        execution_status = "PASS"
    verdict = read_decision_rule(outp) if p.returncode == 0 else {
        "decision_rule_pass": None, "rule_flags": {}, "rule_error": "script did not exit 0"}
    if p.returncode != 0:
        status = "FAIL"
    elif verdict["decision_rule_pass"] is True:
        status = "PASS"
    elif verdict["decision_rule_pass"] is False:
        status = "RULE_FAIL"
    else:
        status = "NO_RULE"
    return {
        "script": script, "phase": "smoke" if smoke else "full",
        "status": status, "execution_status": execution_status,
        "decision_rule_pass": verdict["decision_rule_pass"],
        "rule_flags": verdict["rule_flags"], "rule_error": verdict["rule_error"],
        "returncode": p.returncode, "wall_s": round(dt, 2),
        "stdout_tail": p.stdout.strip().splitlines()[-3:],
        "stderr_tail": p.stderr.strip().splitlines()[-5:],
        "output_json": outp, "output_sha256": sha256(outp) if os.path.exists(outp) else None,
        "script_sha256": sha256(os.path.join(HERE, script)),
    }


def summarise(rows):
    return {
        "execution_failures": [r["script"] for r in rows if r["execution_status"] != "PASS"],
        "decision_rule_failures": [r["script"] for r in rows if r["status"] == "RULE_FAIL"],
        "no_rule_verdict": [r["script"] for r in rows if r["status"] == "NO_RULE"],
        "rule_passes": [r["script"] for r in rows if r["status"] == "PASS"],
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
                "verdict_rule": "status = the script's own decision_rule.PASS (not returncode==0); "
                                "status is PASS / RULE_FAIL / NO_RULE / FAIL(execution)",
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
    manifest["smoke_summary"] = summarise(manifest["smoke"])
    manifest["full_summary"] = summarise(manifest["full"])
    manifest["failures"] = manifest["full_summary"]["execution_failures"]
    manifest["decision_rule_failures"] = manifest["full_summary"]["decision_rule_failures"]
    with open(os.path.join(args.outdir, "run_all.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    with open(os.path.join(args.outdir, "run_all_manifest.csv"), "w") as f:
        f.write("phase,script,status,execution_status,decision_rule_pass,returncode,wall_s,"
                "script_sha256,output_sha256\n")
        for r in manifest["smoke"] + manifest["full"]:
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                r["phase"], r["script"], r["status"], r["execution_status"],
                r["decision_rule_pass"], r["returncode"], r["wall_s"],
                r["script_sha256"], r["output_sha256"]))
    print(json.dumps({"wall_s": manifest["wall_s"],
                      "execution_failures": manifest["failures"],
                      "decision_rule_failures": manifest["decision_rule_failures"],
                      "no_rule_verdict": manifest["full_summary"]["no_rule_verdict"],
                      "smoke": manifest["smoke_summary"],
                      "full": manifest["full_summary"]}, indent=1))
    summary = manifest["smoke_summary"] if args.smoke_only else manifest["full_summary"]
    bad = (summary["execution_failures"] + summary["decision_rule_failures"] +
           summary["no_rule_verdict"])
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
