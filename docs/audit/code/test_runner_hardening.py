#!/usr/bin/env python3
"""Tests for the hardened HK/Korea runner (Gate-2 precondition #3).

Run with:
    PYTHONPATH="$PWD/engine" python -m pytest docs/audit/code/test_runner_hardening.py -q
or standalone:
    PYTHONPATH="$PWD/engine" python docs/audit/code/test_runner_hardening.py

Engine cost: each seed is a real engine simulation (~10-15 s), so tests use tiny
1-arm-per-jurisdiction x 1-2-seed matrices. They prove the *orchestration*
properties required by task-13:
  * model layer numerically frozen (AST source hashes);
  * stalled worker -> watchdog -> process-GROUP SIGTERM/SIGKILL -> non-zero exit,
    run_failure.json, stall evidence, no final JSON, checkpoints preserved;
  * completion/aggregation stall -> same, with all seed checkpoints preserved;
  * resume after either failure -> success, manifest marks resume, final JSON
    numerically identical to a straight run;
  * completed rows are never recomputed; corrupt checkpoints are recomputed;
  * fingerprint mismatch refuses to reuse checkpoints unless --fresh.
"""
import ast
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RUNNER = os.path.join(REPO, "papers", "shadow-education-contest", "code",
                      "run_hk_korea_comparative.py")
ENGINE = os.path.join(REPO, "engine")

# sha256 of the AST source segment of each MODEL-layer function (from the
# pre-hardening file sha256 dd0b1d8d...). Any numeric change fails the build.
MODEL_FUNCTION_SHA256 = {
    "_with_g12_share": "1077a1800fa593602653b614dd096c0f8f50682281f0eb31baf00c3b683655e9",
    "_with_dv_scale": "c8f8f2c22caa582b848766cb9bd21384f21f66e71b49eadb4e47bbfdb45b3fe4",
    "build_arms": "85ef8878ec21b7f6df8d8e614515b5b6e03e7b64178c9fec87f2b4e66e165e1e",
    "_run_single": "f5fea9d60b24a367fc31e0acc2dd12751978e132689021aeb0573e8bd4719912",
    "_stats": "8cc0c8c24dfd41b6e19b177a1147a95cf62acab5b78972a259693b09f8209644",
}


def _import_runner():
    spec = importlib.util.spec_from_file_location("hk_runner_under_test", RUNNER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _env(extra=None):
    env = dict(os.environ)
    env["PYTHONPATH"] = ENGINE
    env.setdefault("OPENBLAS_NUM_THREADS", "1")
    env.setdefault("MKL_NUM_THREADS", "1")
    env.setdefault("OMP_NUM_THREADS", "1")
    env.pop("HK_HARDENED_TEST_MODE", None)
    env.pop("HK_HARDENED_TEST_STALL_AFTER", None)
    env.pop("HK_HARDENED_ALLOW_TEST_HOOKS", None)
    if extra:
        env.update(extra)
    return env


def run_driver(ckpt, out, extra_args=(), env_extra=None, timeout=600):
    cmd = [sys.executable, RUNNER, "--checkpoint-dir", ckpt, "--out", out,
           "--smoke-arms", "1", "--smoke-seeds", "2",
           "--workers", "2", "--stall-timeout", "120", "--kill-grace", "5"]
    cmd.extend(extra_args)
    proc = subprocess.run(cmd, cwd=REPO, env=_env(env_extra), capture_output=True, text=True,
                          timeout=timeout)
    return proc


def _strip_elapsed(path):
    d = json.load(open(path, encoding="utf-8"))
    d["metadata"].pop("elapsed_seconds", None)
    return d


def _pgid_alive(pgid):
    out = subprocess.run(["ps", "-o", "pid=", "-g", str(pgid)], capture_output=True, text=True)
    return bool(out.stdout.strip())


def _seed_files(ckpt):
    sd = os.path.join(ckpt, "seeds")
    return sorted(f for f in os.listdir(sd) if f.endswith(".json")) if os.path.isdir(sd) else []


# ---------------------------------------------------------------------------
# 1. Model layer frozen
# ---------------------------------------------------------------------------
def test_model_layer_numerically_frozen():
    mod = _import_runner()
    import hashlib

    src = open(RUNNER, encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {n.name: ast.get_source_segment(src, n) for n in tree.body if isinstance(n, ast.FunctionDef)}
    for name, expected in MODEL_FUNCTION_SHA256.items():
        got = hashlib.sha256(funcs[name].encode()).hexdigest()
        assert got == expected, f"MODEL LAYER CHANGED: {name}"
    assert mod.N_SEEDS == 30


# ---------------------------------------------------------------------------
# 2. Dry-run + fingerprint
# ---------------------------------------------------------------------------
def test_dry_run_writes_fingerprint(tmp_path):
    ckpt = str(tmp_path / "ckpt")
    out = str(tmp_path / "out.json")
    proc = run_driver(ckpt, out, extra_args=["--dry-run"])
    assert proc.returncode == 0, proc.stderr
    assert os.path.isfile(os.path.join(ckpt, "fingerprint.json"))
    assert not os.path.exists(out)


# ---------------------------------------------------------------------------
# 3. Stalled worker -> watchdog -> group kill -> resume
# ---------------------------------------------------------------------------
def test_stalled_worker_group_kill_then_resume(tmp_path):
    ref_ckpt, ref_out = str(tmp_path / "ref_ckpt"), str(tmp_path / "ref.json")
    proc = run_driver(ref_ckpt, ref_out)
    assert proc.returncode == 0, proc.stderr
    assert os.path.isfile(ref_out)

    ckpt, out = str(tmp_path / "stall_ckpt"), str(tmp_path / "stall.json")
    stall_env = {"HK_HARDENED_TEST_MODE": "stall_worker",
                 "HK_HARDENED_TEST_STALL_AFTER": "1",
                 "HK_HARDENED_ALLOW_TEST_HOOKS": "1"}
    proc = run_driver(ckpt, out, extra_args=["--stall-timeout", "45", "--kill-grace", "3"],
                      env_extra=stall_env, timeout=300)
    assert proc.returncode == 3, f"expected watchdog stall exit 3, got {proc.returncode}\n{proc.stderr}"

    failure = json.load(open(os.path.join(ckpt, "run_failure.json"), encoding="utf-8"))
    assert failure["failure_kind"] == "stall"
    stall_files = [f for f in os.listdir(ckpt) if f.startswith("stall_") and f.endswith(".json")]
    assert len(stall_files) == 1, f"stall evidence missing: {os.listdir(ckpt)}"
    stall = json.load(open(os.path.join(ckpt, stall_files[0]), encoding="utf-8"))
    assert stall["kind"] == "watchdog_stall"
    assert stall["action"].startswith("killpg(SIGTERM)")
    assert failure["kill_signals"], "run_failure.json must record the kill signals sent"
    assert any("killpg" in s and "SIGTERM" in s for s in failure["kill_signals"]), failure["kill_signals"]
    assert not _pgid_alive(stall["host_pgid"]), "host process group still alive after group kill"
    assert not os.path.exists(out), "final JSON must NOT be written on failure"
    done_before = len(_seed_files(ckpt))
    assert 0 < done_before < 4, f"expected partial checkpoints, got {done_before}"

    # resume with the normal worker: must complete, not recompute finished rows
    proc = run_driver(ckpt, out)
    assert proc.returncode == 0, proc.stderr
    assert os.path.isfile(out)
    manifest = json.load(open(os.path.join(ckpt, "run_manifest.json"), encoding="utf-8"))
    assert manifest["status"] == "ok"
    assert manifest["resumed"] is True
    assert manifest["checkpointed_before_run"] == done_before
    assert manifest["computed_this_run"] == 4 - done_before
    assert _strip_elapsed(out) == _strip_elapsed(ref_out), "resume output differs from straight run"


# ---------------------------------------------------------------------------
# 4. Completion/aggregation stall -> watchdog kills host; work preserved; resume
# ---------------------------------------------------------------------------
def test_completion_stall_then_resume(tmp_path):
    ref_ckpt, ref_out = str(tmp_path / "ref_ckpt"), str(tmp_path / "ref.json")
    proc = subprocess.run([sys.executable, RUNNER, "--checkpoint-dir", ref_ckpt, "--out", ref_out,
                           "--smoke-arms", "1", "--smoke-seeds", "1", "--workers", "2"],
                          cwd=REPO, env=_env(), capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, proc.stderr

    ckpt, out = str(tmp_path / "comp_ckpt"), str(tmp_path / "comp.json")
    stall_env = {"HK_HARDENED_TEST_MODE": "stall_completion", "HK_HARDENED_ALLOW_TEST_HOOKS": "1"}
    proc = subprocess.run([sys.executable, RUNNER, "--checkpoint-dir", ckpt, "--out", out,
                           "--smoke-arms", "1", "--smoke-seeds", "1", "--workers", "2",
                           "--stall-timeout", "45", "--kill-grace", "3"],
                          cwd=REPO, env=_env(stall_env), capture_output=True, text=True, timeout=300)
    assert proc.returncode == 3, f"expected completion-stall exit 3, got {proc.returncode}\n{proc.stderr}"
    assert len(_seed_files(ckpt)) == 2, "all seed checkpoints must survive a completion-phase stall"
    assert not os.path.exists(out), "no final JSON on completion stall"
    assert os.path.isfile(os.path.join(ckpt, "run_failure.json"))
    stall = [f for f in os.listdir(ckpt) if f.startswith("stall_")]
    assert stall, "stall evidence missing"

    # resume: nothing to compute, pure aggregation
    proc = subprocess.run([sys.executable, RUNNER, "--checkpoint-dir", ckpt, "--out", out,
                           "--smoke-arms", "1", "--smoke-seeds", "1", "--workers", "2"],
                          cwd=REPO, env=_env(), capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, proc.stderr
    manifest = json.load(open(os.path.join(ckpt, "run_manifest.json"), encoding="utf-8"))
    assert manifest["computed_this_run"] == 0 and manifest["resumed"] is True
    assert _strip_elapsed(out) == _strip_elapsed(ref_out)


# ---------------------------------------------------------------------------
# 5. Corrupt checkpoint is detected and recomputed
# ---------------------------------------------------------------------------
def test_corrupt_checkpoint_recomputed(tmp_path):
    ref_ckpt, ref_out = str(tmp_path / "ref_ckpt"), str(tmp_path / "ref.json")
    assert run_driver(ref_ckpt, ref_out).returncode == 0
    ckpt, out = str(tmp_path / "corrupt_ckpt"), str(tmp_path / "corrupt.json")
    assert run_driver(ckpt, out).returncode == 0
    seed_name = _seed_files(ckpt)[0]
    path = os.path.join(ckpt, "seeds", seed_name)
    payload = json.load(open(path, encoding="utf-8"))
    payload["row"]["k12_spend"] = 123456.789  # corrupt the numeric content
    json.dump(payload, open(path, "w", encoding="utf-8"))
    proc = run_driver(ckpt, out, extra_args=["--stall-timeout", "240"])
    assert proc.returncode == 0, proc.stderr
    manifest = json.load(open(os.path.join(ckpt, "run_manifest.json"), encoding="utf-8"))
    assert manifest["computed_this_run"] == 1, "exactly the corrupted checkpoint must be recomputed"
    assert _strip_elapsed(out) == _strip_elapsed(ref_out)


# ---------------------------------------------------------------------------
# 6. Fingerprint mismatch refuses; --fresh archives and proceeds
# ---------------------------------------------------------------------------
def test_fingerprint_mismatch_refuses_without_fresh(tmp_path):
    ckpt = str(tmp_path / "fp_ckpt")
    out = str(tmp_path / "fp.json")
    assert run_driver(ckpt, out, extra_args=["--dry-run"]).returncode == 0
    fp_path = os.path.join(ckpt, "fingerprint.json")
    fp = json.load(open(fp_path, encoding="utf-8"))
    fp["fingerprint"] = "0" * 64
    json.dump(fp, open(fp_path, "w", encoding="utf-8"))
    proc = run_driver(ckpt, out, extra_args=["--dry-run"])
    assert proc.returncode == 2, f"expected refusal exit 2, got {proc.returncode}\n{proc.stderr}"
    assert "fingerprint mismatch" in proc.stderr
    proc = run_driver(ckpt, out, extra_args=["--dry-run", "--fresh"])
    assert proc.returncode == 0, proc.stderr
    archived = [d for d in os.listdir(str(tmp_path)) if d.startswith("fp_ckpt_archive_")]
    assert archived, "old checkpoint dir must be archived on --fresh"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
