#!/usr/bin/env python3
"""Smoke + checkpoint/resume equivalence check for the hardened HK/Korea runner.

Runs a small real-engine matrix (default 3 arms per jurisdiction x 2 seeds = 6
arms x 2 seeds = 12 real simulations) three times:

  1. STRAIGHT   fresh checkpoints, normal run          -> reference JSON
  2. INTERRUPT  fresh checkpoints; the TEST-ONLY stall hook makes half the
                seeds hang -> driver watchdog kills the host process GROUP
                (non-zero exit, run_failure.json, checkpoints preserved)
  3. RESUME     same checkpoint dir, normal run         -> final JSON
  4. AGGREGATE  same checkpoint dir again (0 tasks)     -> final JSON, pure aggregation

Then it compares the JSON values (metadata.elapsed_seconds stripped):
RESUME == STRAIGHT and AGGREGATE == STRAIGHT, i.e. checkpoint/resume is value-
equivalent to a straight run and completed rows are never recomputed.

This script is the Gate-2 precondition evidence; it is safe on CPU (no GPU).
Writes a JSON report (--report) and exits 0 only if every equivalence holds.

Usage:
  PYTHONPATH="$PWD/engine" python docs/audit/code/smoke_checkpoint_resume.py \
      [--python-executable PATH] [--workers 2] [--arms-per-jur 3] [--seeds 2] \
      [--stall-timeout 45] [--report docs/audit/results/SMOKE_...json]
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RUNNER = os.path.join(REPO, "papers", "shadow-education-contest", "code", "run_hk_korea_comparative.py")
ENGINE = os.path.join(REPO, "engine")


def env_for(extra=None):
    env = dict(os.environ)
    env["PYTHONPATH"] = ENGINE
    env.setdefault("OPENBLAS_NUM_THREADS", "1")
    env.setdefault("MKL_NUM_THREADS", "1")
    env.setdefault("OMP_NUM_THREADS", "1")
    for key in ("HK_HARDENED_TEST_MODE", "HK_HARDENED_TEST_STALL_AFTER", "HK_HARDENED_ALLOW_TEST_HOOKS"):
        env.pop(key, None)
    if extra:
        env.update(extra)
    return env


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_elapsed(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    d["metadata"].pop("elapsed_seconds", None)
    return d


def run(py, ckpt, out, args, env_extra=None, timeout=1800):
    cmd = [py, RUNNER, "--checkpoint-dir", ckpt, "--out", out] + args
    started = time.time()
    proc = subprocess.run(cmd, cwd=REPO, env=env_for(env_extra), capture_output=True, text=True,
                          timeout=timeout)
    return {
        "cmd": cmd,
        "exit_code": proc.returncode,
        "wall_sec": round(time.time() - started, 2),
        "stdout_tail": proc.stdout.splitlines()[-8:],
        "stderr_tail": proc.stderr.splitlines()[-8:],
    }


def count_seeds(ckpt):
    d = os.path.join(ckpt, "seeds")
    return len([f for f in os.listdir(d) if f.endswith(".json")]) if os.path.isdir(d) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--python-executable", default=sys.executable)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--arms-per-jur", type=int, default=3, help="N arms per jurisdiction (3 -> 6 arms)")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--stall-timeout", type=float, default=45.0)
    ap.add_argument("--report", default="")
    ap.add_argument("--workdir", default="")
    args = ap.parse_args()

    py = args.python_executable
    workdir = args.workdir or tempfile.mkdtemp(prefix="hk_hardened_smoke_")
    os.makedirs(workdir, exist_ok=True)
    matrix = ["--smoke-arms", str(args.arms_per_jur), "--smoke-seeds", str(args.seeds),
              "--workers", str(args.workers)]
    expected = 2 * args.arms_per_jur * args.seeds
    print(f"smoke workdir: {workdir}")
    print(f"matrix: {args.arms_per_jur} arms/jur x {args.seeds} seeds = {expected} runs, "
          f"python={py}, workers={args.workers}")

    ref_ckpt, ref_out = os.path.join(workdir, "ckpt_ref"), os.path.join(workdir, "ref.json")
    straight = run(py, ref_ckpt, ref_out, matrix + ["--stall-timeout", "180"])
    straight["checkpointed"] = count_seeds(ref_ckpt)
    straight["out_sha256"] = sha256_file(ref_out) if os.path.isfile(ref_out) else None
    straight["manifest"] = json.load(open(os.path.join(ref_ckpt, "run_manifest.json"))) \
        if os.path.isfile(os.path.join(ref_ckpt, "run_manifest.json")) else None
    ok_straight = straight["exit_code"] == 0 and straight["out_sha256"] is not None
    print(f"[1/4] straight: rc={straight['exit_code']} wall={straight['wall_sec']}s rows={straight['checkpointed']}")

    int_ckpt, int_out = os.path.join(workdir, "ckpt_int"), os.path.join(workdir, "int.json")
    interrupted = run(py, int_ckpt, int_out, matrix + ["--stall-timeout", str(args.stall_timeout)],
                      env_extra={"HK_HARDENED_TEST_MODE": "stall_worker",
                                 "HK_HARDENED_TEST_STALL_AFTER": "1",
                                 "HK_HARDENED_ALLOW_TEST_HOOKS": "1"})
    interrupted["checkpointed"] = count_seeds(int_ckpt)
    interrupted["final_json_written"] = os.path.isfile(int_out)
    interrupted["failure"] = json.load(open(os.path.join(int_ckpt, "run_failure.json"))) \
        if os.path.isfile(os.path.join(int_ckpt, "run_failure.json")) else None
    interrupted["stall_evidence"] = [f for f in os.listdir(int_ckpt) if f.startswith("stall_")] if os.path.isdir(int_ckpt) else []
    ok_interrupt = (interrupted["exit_code"] != 0 and not interrupted["final_json_written"]
                    and 0 < interrupted["checkpointed"] < expected
                    and interrupted["failure"] is not None and interrupted["stall_evidence"])
    print(f"[2/4] interrupt: rc={interrupted['exit_code']} wall={interrupted['wall_sec']}s "
          f"checkpointed={interrupted['checkpointed']}/{expected} final_json={interrupted['final_json_written']}")

    resumed = run(py, int_ckpt, int_out, matrix + ["--stall-timeout", "180"])
    resumed["checkpointed"] = count_seeds(int_ckpt)
    resumed["out_sha256"] = sha256_file(int_out) if os.path.isfile(int_out) else None
    resumed["manifest"] = json.load(open(os.path.join(int_ckpt, "run_manifest.json"))) \
        if os.path.isfile(os.path.join(int_ckpt, "run_manifest.json")) else None
    equivalent = False
    if os.path.isfile(ref_out) and os.path.isfile(int_out):
        equivalent = strip_elapsed(ref_out) == strip_elapsed(int_out)
    ok_resume = resumed["exit_code"] == 0 and equivalent and resumed["manifest"] and resumed["manifest"]["resumed"]
    print(f"[3/4] resume: rc={resumed['exit_code']} wall={resumed['wall_sec']}s "
          f"computed={resumed['manifest']['computed_this_run'] if resumed['manifest'] else '?'} "
          f"value_equal={equivalent}")

    agg_out = os.path.join(workdir, "agg.json")
    aggregate = run(py, int_ckpt, agg_out, matrix + ["--stall-timeout", "180"])
    aggregate["out_sha256"] = sha256_file(agg_out) if os.path.isfile(agg_out) else None
    aggregate["manifest"] = json.load(open(os.path.join(int_ckpt, "run_manifest.json"))) \
        if os.path.isfile(os.path.join(int_ckpt, "run_manifest.json")) else None
    eq_agg = False
    if os.path.isfile(ref_out) and os.path.isfile(agg_out):
        eq_agg = strip_elapsed(ref_out) == strip_elapsed(agg_out)
    ok_aggregate = (aggregate["exit_code"] == 0 and eq_agg
                    and aggregate["manifest"]["computed_this_run"] == 0)
    print(f"[4/4] aggregate-only: rc={aggregate['exit_code']} wall={aggregate['wall_sec']}s "
          f"value_equal={eq_agg} computed={aggregate['manifest']['computed_this_run'] if aggregate['manifest'] else '?'}")

    report = {
        "schema": 1,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runner": RUNNER,
        "runner_sha256": sha256_file(RUNNER),
        "engine_dir": ENGINE,
        "python": py,
        "python_version": sys.version.split()[0],
        "numpy_version": __import__("numpy").__version__ if "numpy" in sys.modules else
                         subprocess.run([py, "-c", "import numpy;print(numpy.__version__)"],
                                        capture_output=True, text=True).stdout.strip(),
        "workers": args.workers,
        "matrix": {"arms_per_jurisdiction": args.arms_per_jur, "seeds": args.seeds,
                   "expected_runs": expected},
        "workdir": workdir,
        "cases": {"straight": straight, "interrupted": interrupted,
                  "resumed": resumed, "aggregate_only": aggregate},
        "assertions": {
            "straight_ok": ok_straight,
            "interrupted_nonzero_no_final_json_checkpoints_preserved": ok_interrupt,
            "resume_success_resumed_flag_value_equal_to_straight": bool(ok_resume),
            "aggregate_only_zero_compute_value_equal_to_straight": bool(ok_aggregate),
        },
        "passed": bool(ok_straight and ok_interrupt and ok_resume and ok_aggregate),
    }
    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        tmp = args.report + f".tmp.{os.getpid()}"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, args.report)
        print(f"report: {args.report}")
    print("RESULT:", "PASS" if report["passed"] else "FAIL")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
