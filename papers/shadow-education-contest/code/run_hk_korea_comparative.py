"""Hong Kong (HKDSE) vs South Korea (CSAT) Comparative Tullock Contest Experiment.

Runs all 18 policy arms x 30 matched seeds (540 runs total) against
atlas-of-education branch `research/binding-gate-2026-11-25` (HEAD `68da16e`)
patched with `contest_gate.patch`.

Uses the exact `Engine(modules, **params)` constructor (core.py L73-74) and
`E.R` yearly history dict populated via `E.note(...)`, plus `E.ALL` for cohort
elite-tier tracking.

HARDENED ORCHESTRATION (Gate-2 precondition #3; no model-numeric changes)
--------------------------------------------------------------------------
The model code (_run_single / build_arms / _stats) is UNCHANGED. Only the
execution/orchestration layer changed, to survive the observed
ProcessPoolExecutor completion-phase hang (GATE1_POOL_HANG_INCIDENT.md):

  * per-(arm, seed) checkpoint written atomically by the worker that computed it,
    so no computed row can be lost by a completion/aggregation hang;
  * per-arm checkpoint assembled atomically as soon as all of an arm's seeds are
    present, so a later failure loses at most one arm;
  * resumable driver: validates every checkpoint (row hash, params hash, engine
    fingerprint), skips completed work, runs only missing tasks;
  * per-arm and per-seed watchdog timeouts; a stall triggers process-GROUP kill
    (SIGTERM to -pgid, then SIGKILL after a grace period) plus stall evidence;
  * memory-aware worker cap; results are written to disk and never accumulated
    in the parent (only tiny status tuples cross process boundaries);
  * on any failure: loud non-zero exit, run_failure.json, NO final JSON,
    checkpoints preserved for resume.

Output schema of the final JSON is unchanged, so numbers remain comparable.
Checkpoints/manifests live under --checkpoint-dir (default ./hk_korea_540_ckpt).

Usage:
  PYTHONPATH="$PWD/engine" python papers/shadow-education-contest/code/run_hk_korea_comparative.py
  ... --workers 6 --stall-timeout 240 --resume
  ... --smoke-arms 6 --smoke-seeds 2          # smoke / campaign dry run
  ... --fresh                                  # archive old checkpoints, start over
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import traceback
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures import TimeoutError as FuturesTimeoutError

warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(ROOT, "engine")
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

import multiprocessing

import numpy as np
from eduengine.core import Engine
from eduengine.modules.labour import QueueLabour
from eduengine.modules.schools import PrivateSchools, PublicSchools
from eduengine.modules.sdg4 import SDG4
from eduengine.modules.tutoring import TutoringMarket

N_SEEDS = 30
SEEDS = list(range(N_SEEDS))

HARDENING_VERSION = "hardened-1"
CHECKPOINT_SCHEMA = 1
DEFAULT_OUT = os.path.join(ROOT, "hk_korea_comparative_with_cf4.json")
DEFAULT_CKPT = os.path.join(ROOT, "hk_korea_540_ckpt")

# Exit codes (documented in RUNNER_HARDENING.md).
EXIT_OK = 0
EXIT_CONFIG = 2          # fingerprint mismatch / bad configuration (no run)
EXIT_STALL = 3           # watchdog detected a stall; process group killed
EXIT_HOST_ERROR = 4      # host process reported an error
EXIT_INCOMPLETE = 5      # host exited 0 but checkpoints are incomplete/invalid

# TEST-ONLY fault injection (documented; inert unless explicitly set).
TEST_MODE_ENV = "HK_HARDENED_TEST_MODE"
TEST_STALL_AFTER_ENV = "HK_HARDENED_TEST_STALL_AFTER"


# ===========================================================================
# Model layer — UNCHANGED (must stay numerically identical to dd0b1d8d)
# ===========================================================================
def _with_g12_share(params, share):
    p = dict(params)
    gates = [dict(g) for g in p["gates"]]
    gates[2]["share"] = share
    p["gates"] = gates
    return p


def _with_dv_scale(params, mult):
    p = dict(params)
    p["elite_logw"] = p["elite_logw"] * mult
    gates = [dict(g) for g in p["gates"]]
    for g in gates:
        if "elite_logw" in g:
            g["elite_logw"] = g["elite_logw"] * mult
    p["gates"] = gates
    return p


def build_arms():
    """Return ordered list of (jurisdiction, arm_id, label, params) for all 18 arms."""
    hk_base = dict(
        N=300,
        T=46,
        measure_from=18,
        y_median=2.2,
        y_sigma=0.65,
        urban_share=1.0,
        subsist=0.35,
        borrow=0.25,
        pay_ratio=1.2,
        monitoring=0.9,
        budget_per_child=0.14,
        fee_public=0.0,
        fee_tertiary=0.25,
        vac0=0.30,
        vac_growth=0.005,
        own_ban=0.95,
        r0=0.04,
        elite_logw=0.50,
        contest_r=1.5,
        contest_alpha=0.25,
        contest_price=0.16,
        contest_x0=1.0,
        contest_max_e=6.0,
        gates=[
            dict(kind="bar", bar=2.0),
            dict(kind="bar", bar=4.0),
            dict(kind="contest", share=0.23, fail="track"),
            dict(kind="bar", bar=10.0),
        ],
    )

    kr_base = dict(
        N=300,
        T=46,
        measure_from=18,
        y_median=2.0,
        y_sigma=0.55,
        urban_share=0.85,
        subsist=0.35,
        borrow=0.25,
        pay_ratio=1.2,
        monitoring=0.9,
        budget_per_child=0.14,
        fee_public=0.0,
        fee_tertiary=0.25,
        vac0=0.28,
        vac_growth=0.005,
        own_ban=0.95,
        r0=0.04,
        elite_logw=0.60,
        contest_r=1.6,
        contest_alpha=0.25,
        contest_price=0.16,
        contest_x0=1.0,
        contest_max_e=6.0,
        gates=[
            dict(kind="bar", bar=2.0),
            dict(kind="contest", share=0.35, fail="track", elite_logw=0.15, set_voc=False),
            dict(kind="contest", share=0.12, fail="track"),
            dict(kind="bar", bar=10.0),
        ],
    )

    specs = []
    for jur, base, s_mod, s_maj, s_label_mod, s_label_maj in [
        ("HK", hk_base, 0.28, 0.50, "S=0.28", "S=0.50"),
        ("KR", kr_base, 0.16, 0.40, "S12=0.16", "S12=0.40"),
    ]:
        arms = [
            ("Baseline", f"Baseline ({'S=0.23' if jur == 'HK' else 'S12=0.12'})", base),
            ("CF1a", "CF1a (+50% tax)", dict(base, contest_price=base["contest_price"] * 1.5)),
            ("CF1b", "CF1b (-50% cap)", dict(base, contest_max_e=base["contest_max_e"] * 0.5)),
            ("CF2a", f"CF2a ({s_label_mod})", _with_g12_share(base, s_mod)),
            ("CF2b", f"CF2b ({s_label_maj})", _with_g12_share(base, s_maj)),
            ("CF3a", "CF3a (dV -30%)", _with_dv_scale(base, 0.70)),
            ("CF3b", "CF3b (dV -50%)", _with_dv_scale(base, 0.50)),
            (
                "CF4a",
                "CF4a (Win-Win: dV -50% + Cap -50%)",
                dict(_with_dv_scale(base, 0.50), contest_max_e=base["contest_max_e"] * 0.5),
            ),
            (
                "CF4b",
                f"CF4b (Win-Win: dV -50% + Seats {s_label_maj})",
                _with_g12_share(_with_dv_scale(base, 0.50), s_maj),
            ),
        ]
        for arm_id, label, prm in arms:
            specs.append((jur, arm_id, label, prm))
    return specs


def _run_single(task):
    jur, arm_id, seed, params = task
    mods = [PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]
    E = Engine(mods, **dict(params, seed=seed))
    E.run()

    m = E.p["measure_from"]
    R = E.R
    k12_spend = float(np.mean(R["tut_k12_spend"][m:]))
    k12_rate = float(np.mean(R["tut_k12_rate"][m:]))
    g12_rate = float(np.mean(R["tut_g12_rate"][m:]))
    rq = np.mean(np.array(R["tut_k12_rate_by_q"][m:], float), 0)
    sq = np.mean(np.array(R["tut_k12_spend_by_q"][m:], float), 0)
    contest_e_mean = float(np.mean(R["contest_e_mean"][m:]))

    X = E.ALL
    sel = (X["cohort"] >= m) & (X["cohort"] <= E.p["T"] - 14) & (X["g"] >= 12)
    el = X["elite"][sel]
    qq = X["q"][sel]
    elite_q5_share = float(np.mean(qq[el] == 4)) if el.any() else float("nan")

    return dict(
        jurisdiction=jur,
        arm_id=arm_id,
        seed=seed,
        k12_spend=k12_spend,
        k12_rate_pct=100.0 * k12_rate,
        g12_pct=100.0 * g12_rate,
        q5_q1_gap_pp=100.0 * float(rq[4] - rq[0]),
        q5_q1_spend_ratio=float(sq[4] / max(sq[0], 1e-9)),
        elite_q5_share_pct=100.0 * elite_q5_share,
        k12_rate_by_q=[float(100.0 * v) for v in rq],
        k12_spend_by_q=[float(v) for v in sq],
        contest_e_mean=contest_e_mean,
    )


def _stats(vals):
    arr = np.array(vals, float)
    mean = float(np.nanmean(arr))
    sd = float(np.nanstd(arr, ddof=1)) if len(arr) > 1 else 0.0
    se = sd / np.sqrt(max(len(arr), 1))
    return dict(mean=mean, sd=sd, ci95_lo=mean - 1.96 * se, ci95_hi=mean + 1.96 * se)


# ===========================================================================
# Hardening layer — checkpointing, fingerprinting, watchdog, resume
# ===========================================================================
def _utcnow():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _atomic_write_json(path, payload):
    """Write JSON atomically: tmp in the same directory, fsync, os.replace."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _safe_token(value):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value))


def _arm_stem(jur, arm_id):
    return f"{jur}__{_safe_token(arm_id)}"


def seed_ckpt_path(ckpt_dir, jur, arm_id, seed):
    return os.path.join(ckpt_dir, "seeds", f"{_arm_stem(jur, arm_id)}__seed{int(seed):02d}.json")


def arm_ckpt_path(ckpt_dir, jur, arm_id):
    return os.path.join(ckpt_dir, "arms", f"{_arm_stem(jur, arm_id)}.json")


def _params_sha(params):
    return _sha256_bytes(_canonical_json(params))


def _engine_fingerprint():
    """Content hash of every eduengine source file that can affect the numbers."""
    import eduengine

    pkg_dir = os.path.dirname(os.path.abspath(eduengine.__file__))
    files = {}
    for dirpath, _dirnames, filenames in os.walk(pkg_dir):
        for name in sorted(filenames):
            if not name.endswith(".py"):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, pkg_dir)
            files[rel] = _sha256_file(full)
    return _sha256_bytes(_canonical_json({"eduengine": files, "n_seeds": N_SEEDS, "seeds": SEEDS})), files


def _run_fingerprint(specs):
    """Fingerprint of the whole run definition (engine code + arms + seed grid)."""
    engine_fp, engine_files = _engine_fingerprint()
    arms = [
        {"jurisdiction": jur, "arm_id": arm_id, "label": label, "params_sha256": _params_sha(params)}
        for jur, arm_id, label, params in specs
    ]
    fp = _sha256_bytes(_canonical_json({"engine": engine_fp, "arms": arms, "hardening_version": HARDENING_VERSION}))
    return fp, {"engine_fingerprint": engine_fp, "engine_files": engine_files, "arms": arms,
                "hardening_version": HARDENING_VERSION, "n_seeds": N_SEEDS, "seeds": SEEDS}


def _total_memory_bytes():
    try:
        return os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE")
    except (ValueError, OSError, AttributeError):
        pass
    try:
        out = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip()
        return int(out)
    except Exception:
        return 8 * 1024 ** 3  # conservative fallback


def _available_memory_bytes():
    try:
        return os.sysconf("SC_AVPHYS_PAGES") * os.sysconf("SC_PAGE_SIZE")
    except (ValueError, OSError, AttributeError):
        pass
    total = _total_memory_bytes()
    # macOS: no portable free-page sysconf; assume ~50 % free (memory-aware cap is
    # intentionally conservative; env HK_MAX_WORKERS overrides).
    return total // 2


def default_workers():
    """Memory-aware worker cap (Gate-1 incident had 8 GiB host under memory pressure)."""
    env = os.environ.get("HK_MAX_WORKERS")
    if env:
        return max(1, int(env))
    cpus = os.cpu_count() or 2
    avail = _available_memory_bytes()
    reserve = int(2.5 * 1024 ** 3) if avail > int(6 * 1024 ** 3) else int(1.5 * 1024 ** 3)
    per_worker = int(700 * 1024 ** 2)  # engine + numpy + interpreter, conservative
    by_mem = max(1, (avail - reserve) // max(per_worker, 1))
    return max(1, min(cpus - 2, 6, by_mem))


def _scan_checkpoints(ckpt_dir, specs, seeds, fingerprint):
    """Return (valid_rows, done_keys, invalid_keys) after validating every file."""
    valid_rows = {}
    invalid = []
    arm_params = {(jur, arm_id): _params_sha(params) for jur, arm_id, _label, params in specs}
    for jur, arm_id, _label, _params in specs:
        for seed in seeds:
            path = seed_ckpt_path(ckpt_dir, jur, arm_id, seed)
            if not os.path.isfile(path):
                continue
            try:
                payload = json.load(open(path, encoding="utf-8"))
                row = payload["row"]
                ok = (
                    payload.get("schema") == CHECKPOINT_SCHEMA
                    and payload.get("fingerprint") == fingerprint
                    and payload.get("params_sha256") == arm_params[(jur, arm_id)]
                    and payload.get("jurisdiction") == jur
                    and payload.get("arm_id") == arm_id
                    and payload.get("seed") == seed
                    and payload.get("row_sha256") == _sha256_bytes(_canonical_json(row))
                )
            except Exception:
                ok = False
            if ok:
                valid_rows[(jur, arm_id, seed)] = row
            else:
                invalid.append((jur, arm_id, seed))
    return valid_rows, invalid


def _write_progress(ckpt_dir, done, expected, last_key):
    _atomic_write_json(os.path.join(ckpt_dir, "progress.json"), {
        "schema": CHECKPOINT_SCHEMA,
        "done": done,
        "expected": expected,
        "last_key": list(last_key) if last_key else None,
        "updated_utc": _utcnow(),
    })


def _write_arm_checkpoint(ckpt_dir, fingerprint, jur, arm_id, label, params, rows):
    ordered = sorted(rows, key=lambda r: r["seed"])
    payload = {
        "schema": CHECKPOINT_SCHEMA,
        "hardening_version": HARDENING_VERSION,
        "fingerprint": fingerprint,
        "jurisdiction": jur,
        "arm_id": arm_id,
        "label": label,
        "params_sha256": _params_sha(params),
        "n_seeds": len(ordered),
        "seeds": [r["seed"] for r in ordered],
        "content_sha256": _sha256_bytes(_canonical_json(ordered)),
        "rows": ordered,
        "created_utc": _utcnow(),
    }
    _atomic_write_json(arm_ckpt_path(ckpt_dir, jur, arm_id), payload)


def _scan_arm_states(ckpt_dir, specs, seeds):
    """Count per-arm completed seed checkpoints (unvalidated; fast progress counter)."""
    states = {}
    for jur, arm_id, _label, _params in specs:
        stem = _arm_stem(jur, arm_id)
        states[(jur, arm_id)] = sum(
            1 for seed in seeds if os.path.isfile(seed_ckpt_path(ckpt_dir, jur, arm_id, seed))
        )
    return states


def _progress_token(ckpt_dir):
    """Monotonic-ish progress witness: progress.json identity (content changes per result)."""
    path = os.path.join(ckpt_dir, "progress.json")
    try:
        st = os.stat(path)
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return None


def _count_seed_files(ckpt_dir):
    seeds_dir = os.path.join(ckpt_dir, "seeds")
    if not os.path.isdir(seeds_dir):
        return 0
    try:
        return sum(1 for name in os.listdir(seeds_dir) if name.endswith(".json") and ".tmp." not in name)
    except OSError:
        return 0


# ---------------------------------------------------------------------------
# Worker functions (run inside pool processes)
# ---------------------------------------------------------------------------
def _run_and_checkpoint(bundle):
    """Compute one seed and write its checkpoint IN THE WORKER (bounded IPC: status only)."""
    jur, arm_id, seed, params, ckpt_path, params_sha, fingerprint = bundle
    row = _run_single((jur, arm_id, seed, params))
    _atomic_write_json(ckpt_path, {
        "schema": CHECKPOINT_SCHEMA,
        "hardening_version": HARDENING_VERSION,
        "fingerprint": fingerprint,
        "jurisdiction": jur,
        "arm_id": arm_id,
        "seed": seed,
        "params_sha256": params_sha,
        "row_sha256": _sha256_bytes(_canonical_json(row)),
        "row": row,
        "created_utc": _utcnow(),
    })
    return [jur, arm_id, int(seed), True]


def _test_stall_worker(bundle):
    """TEST-ONLY: simulate a worker that never returns (watchdog/group-kill test)."""
    jur, arm_id, seed, params, ckpt_path, params_sha, fingerprint = bundle
    stall_after = int(os.environ.get(TEST_STALL_AFTER_ENV, "0"))
    if int(seed) >= stall_after:
        time.sleep(3600)  # never returns; driver/host watchdog must kill the group
    return _run_and_checkpoint(bundle)


# ---------------------------------------------------------------------------
# Host role: run the pool, write checkpoints + arm files, never aggregate
# ---------------------------------------------------------------------------
def _host_fail(ckpt_dir, kind, message, extra=None):
    payload = {"schema": CHECKPOINT_SCHEMA, "status": "failed", "kind": kind,
               "message": message, "updated_utc": _utcnow()}
    if extra:
        payload.update(extra)
    _atomic_write_json(os.path.join(ckpt_dir, "host_failure.json"), payload)


def host_main(args):
    tasks = json.load(open(args.task_manifest, encoding="utf-8"))
    ckpt_dir = args.checkpoint_dir
    specs = build_arms()
    by_arm = {(jur, arm_id): (label, params) for jur, arm_id, label, params in specs}
    seed_timeout = args.seed_timeout
    arm_timeout = args.arm_timeout
    fingerprint = args.fingerprint
    test_mode = os.environ.get(TEST_MODE_ENV, "")
    worker = _test_stall_worker if test_mode == "stall_worker" and _test_allowed() else _run_and_checkpoint
    if test_mode == "stall_worker" and not _test_allowed():
        print("WARNING: test mode ignored (set HK_HARDENED_ALLOW_TEST_HOOKS=1)", file=sys.stderr)

    expected = len(tasks)
    arm_start = {}
    arm_done = {}
    done = 0
    os.makedirs(os.path.join(ckpt_dir, "seeds"), exist_ok=True)
    os.makedirs(os.path.join(ckpt_dir, "arms"), exist_ok=True)
    ctx = multiprocessing.get_context("spawn")
    workers = max(1, min(args.workers, expected))
    try:
        with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as ex:
            futures = {}
            for bundle in tasks:
                jur, arm_id, seed = bundle[0], bundle[1], bundle[2]
                arm_start.setdefault((jur, arm_id), time.time())
                futures[ex.submit(worker, tuple(bundle))] = (jur, arm_id, seed)
            while futures:
                try:
                    for fut in as_completed(list(futures), timeout=min(seed_timeout, 15.0)):
                        jur, arm_id, seed = futures.pop(fut)
                        try:
                            status = fut.result()
                        except Exception as exc:  # worker raised
                            _host_fail(ckpt_dir, "worker_exception",
                                       f"worker for {jur}/{arm_id}/seed{seed} raised: {exc!r}",
                                       {"traceback": traceback.format_exc()})
                            os._exit(EXIT_HOST_ERROR)
                        done += 1
                        arm_done[(jur, arm_id)] = arm_done.get((jur, arm_id), 0) + 1
                        _write_progress(ckpt_dir, done, expected, status[:3])
                        label, params = by_arm[(jur, arm_id)]
                        if arm_done[(jur, arm_id)] >= len(SEEDS):
                            rows = []
                            for s in SEEDS:
                                p = seed_ckpt_path(ckpt_dir, jur, arm_id, s)
                                if os.path.isfile(p):
                                    rows.append(json.load(open(p, encoding="utf-8"))["row"])
                            if len(rows) == len(SEEDS):
                                _write_arm_checkpoint(ckpt_dir, fingerprint, jur, arm_id, label, params, rows)
                        now = time.time()
                        for key, started in list(arm_start.items()):
                            if arm_done.get(key, 0) < len(SEEDS) and now - started > arm_timeout:
                                _host_fail(ckpt_dir, "arm_timeout",
                                           f"arm {key[0]}/{key[1]} exceeded arm_timeout={arm_timeout}s "
                                           f"({arm_done.get(key, 0)}/{len(SEEDS)} seeds done)")
                                os._exit(EXIT_STALL)
                        continue  # re-enter as_completed with remaining futures
                except FuturesTimeoutError:
                    continue  # no completion within slice; outer loop re-checks
        if done != expected:
            _host_fail(ckpt_dir, "incomplete", f"host finished with {done}/{expected} results")
            os._exit(EXIT_INCOMPLETE)
        if test_mode == "stall_completion" and _test_allowed():
            # TEST-ONLY: all work is checkpointed, but the host never returns —
            # simulates the observed completion-phase hang.
            _atomic_write_json(os.path.join(ckpt_dir, "test_stall_completion.json"),
                               {"updated_utc": _utcnow(), "note": "TEST-ONLY completion stall active"})
            time.sleep(3600)
        return EXIT_OK
    except SystemExit:
        raise
    except Exception as exc:
        _host_fail(ckpt_dir, "host_exception", f"host crashed: {exc!r}",
                   {"traceback": traceback.format_exc()})
        os._exit(EXIT_HOST_ERROR)


# ---------------------------------------------------------------------------
# Driver role: resume, supervise host, watchdog, aggregate, final assembly
# ---------------------------------------------------------------------------
def _test_allowed():
    return os.environ.get("HK_HARDENED_ALLOW_TEST_HOOKS", "") == "1"


def _ps_snapshot(pgid):
    for cmd in (["ps", "-o", "pid,ppid,pgid,etime,stat,pcpu,rss,comm", "-g", str(pgid)],
                ["ps", "-o", "pid,ppid,pgid,etime,stat,pcpu,comm", "-g", str(pgid)]):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if out.returncode == 0:
                return out.stdout.splitlines()
        except Exception:
            continue
    return []


def _write_stall_evidence(ckpt_dir, reason, host_pid, host_pgid, done, expected, last_progress_utc,
                          stall_timeout, host_log_tail):
    evidence = {
        "schema": CHECKPOINT_SCHEMA,
        "kind": "watchdog_stall",
        "reason": reason,
        "detected_utc": _utcnow(),
        "host_pid": host_pid,
        "host_pgid": host_pgid,
        "checkpoint_done": done,
        "expected": expected,
        "last_progress_utc": last_progress_utc,
        "stall_timeout_sec": stall_timeout,
        "action": "killpg(SIGTERM); killpg(SIGKILL) after grace period",
        "host_log_tail": host_log_tail,
        "process_snapshot": _ps_snapshot(host_pgid),
    }
    path = os.path.join(ckpt_dir, f"stall_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json")
    _atomic_write_json(path, evidence)
    return path


def _kill_group(pid, pgid, grace_sec=10.0):
    """SIGTERM the process GROUP, then SIGKILL after grace. Returns signal log."""
    log = []
    for sig, label in ((signal.SIGTERM, "TERM"), (signal.SIGKILL, "KILL")):
        try:
            os.killpg(pgid, sig)
            log.append(f"killpg({pgid}, SIG{label}) ok")
        except ProcessLookupError:
            log.append(f"killpg({pgid}, SIG{label}) -> no such process group")
            break
        except PermissionError as exc:
            log.append(f"killpg({pgid}, SIG{label}) -> permission error: {exc}")
            break
        if sig == signal.SIGTERM:
            deadline = time.time() + grace_sec
            while time.time() < deadline:
                if not _pgid_alive(pgid):
                    log.append("group empty after SIGTERM")
                    return log
                time.sleep(0.2)
    return log


def _pgid_alive(pgid):
    try:
        out = subprocess.run(["ps", "-o", "pid=", "-g", str(pgid)], capture_output=True, text=True, timeout=5)
        return bool(out.stdout.strip())
    except Exception:
        return False


def _driver_failure(ckpt_dir, payload):
    payload = dict(payload, schema=CHECKPOINT_SCHEMA, status="failed", updated_utc=_utcnow(),
                   final_json_written=False)
    _atomic_write_json(os.path.join(ckpt_dir, "run_failure.json"), payload)


def _build_payload(specs, rows_by_seed, elapsed, seeds):
    """Reproduce the original aggregation EXACTLY from checkpoint rows."""
    grouped = {}
    for jur, arm_id, _label, _params in specs:
        for seed in seeds:
            row = rows_by_seed[(jur, arm_id, seed)]
            grouped.setdefault((jur, arm_id), []).append(row)
    for key in grouped:
        grouped[key].sort(key=lambda r: r["seed"])

    jurs = [j for j in ("HK", "KR") if any(sp[0] == j for sp in specs)]
    summary = {j: {} for j in jurs}
    for jur in jurs:
        base_rows = grouped[(jur, "Baseline")]
        base_spend_mean = float(np.mean([r["k12_spend"] for r in base_rows]))
        base_by_seed = {r["seed"]: r for r in base_rows}

        for _, arm_id, label, _ in [s for s in specs if s[0] == jur]:
            rows = grouped[(jur, arm_id)]
            spend_idx_seeds = [100.0 * r["k12_spend"] / base_by_seed[r["seed"]]["k12_spend"] for r in rows]
            spend_idx_agg = 100.0 * float(np.mean([r["k12_spend"] for r in rows])) / base_spend_mean
            g12_vals = [r["g12_pct"] for r in rows]
            gap_vals = [r["q5_q1_gap_pp"] for r in rows]
            ratio_vals = [r["q5_q1_spend_ratio"] for r in rows]
            elite_vals = [r["elite_q5_share_pct"] for r in rows]
            k12_rate_vals = [r["k12_rate_pct"] for r in rows]
            k12_spend_vals = [r["k12_spend"] for r in rows]

            summary[jur][arm_id] = dict(
                label=label,
                n_seeds=len(rows),
                total_spend_index=round(spend_idx_agg, 2),
                total_spend_index_seed_stats=_stats(spend_idx_seeds),
                g12_pct=_stats(g12_vals),
                q5_q1_gap_pp=_stats(gap_vals),
                q5_q1_spend_ratio=_stats(ratio_vals),
                elite_q5_share_pct=_stats(elite_vals),
                k12_rate_pct=_stats(k12_rate_vals),
                k12_spend_raw=_stats(k12_spend_vals),
                delta_vs_baseline=dict(
                    total_spend_index_pts=round(spend_idx_agg - 100.0, 2),
                    g12_pp=_stats([r["g12_pct"] - base_by_seed[r["seed"]]["g12_pct"] for r in rows]),
                    q5_q1_gap_pp=_stats([r["q5_q1_gap_pp"] - base_by_seed[r["seed"]]["q5_q1_gap_pp"] for r in rows]),
                    q5_q1_spend_ratio=_stats(
                        [r["q5_q1_spend_ratio"] - base_by_seed[r["seed"]]["q5_q1_spend_ratio"] for r in rows]
                    ),
                    elite_q5_share_pp=_stats(
                        [r["elite_q5_share_pct"] - base_by_seed[r["seed"]]["elite_q5_share_pct"] for r in rows]
                    ),
                ),
            )

    raw_results = [rows_by_seed[(jur, arm_id, seed)]
                   for jur, arm_id, _label, _params in specs for seed in seeds]
    return dict(
        metadata=dict(
            repo="https://github.com/TreyModels/atlas-of-education.git",
            branch="research/binding-gate-2026-11-25",
            base_commit="68da16e",
            n_arms=len(specs),
            n_seeds=len(seeds),
            total_runs=len(raw_results),
            elapsed_seconds=round(elapsed, 2),
            history_api="E.R (core.py L99; populated via E.note(...))",
        ),
        summary=summary,
        seeds=raw_results,
    )


def _print_summary(payload, n_runs, elapsed, out_path, n_seeds):
    print(f"\nCompleted {n_runs} runs in {elapsed:.1f}s -> {out_path}\n")
    for jur in [j for j in ("HK", "KR") if j in payload["summary"]]:
        print(f"=== {jur} ({n_seeds} matched seeds) ===")
        print(f"{'Arm':6s} | {'Label':38s} | {'SpendIdx':8s} | {'G12 %':7s} | {'Q5-Q1 Gap':9s} | {'Q5/Q1 Ratio':11s} | {'Elite Q5 %':10s}")
        print("-" * 105)
        for arm_id, d in payload["summary"][jur].items():
            print(
                f"{arm_id:6s} | {d['label']:38s} | {d['total_spend_index']:8.1f} | "
                f"{d['g12_pct']['mean']:6.1f}% | {d['q5_q1_gap_pp']['mean']:7.1f}pp | "
                f"{d['q5_q1_spend_ratio']['mean']:10.2f}x | {d['elite_q5_share_pct']['mean']:9.1f}%"
            )
        print()


def driver_main(args):
    t_driver = time.time()
    specs_all = build_arms()
    seeds = SEEDS[: args.smoke_seeds] if args.smoke_seeds else list(SEEDS)
    if args.smoke_arms:
        specs = []
        for jur in ("HK", "KR"):
            specs.extend([sp for sp in specs_all if sp[0] == jur][: args.smoke_arms])
    else:
        specs = specs_all
    ckpt_dir = os.path.abspath(args.checkpoint_dir)
    out_path = os.path.abspath(args.out)
    os.makedirs(ckpt_dir, exist_ok=True)

    fingerprint, fingerprint_payload = _run_fingerprint(specs_all)
    fp_path = os.path.join(ckpt_dir, "fingerprint.json")
    if os.path.isfile(fp_path):
        stored = json.load(open(fp_path, encoding="utf-8"))
        if stored.get("fingerprint") != fingerprint:
            if args.fresh:
                archive = f"{ckpt_dir}_archive_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
                shutil.move(ckpt_dir, archive)
                os.makedirs(ckpt_dir, exist_ok=True)
                print(f"checkpoint fingerprint changed; archived old checkpoints to {archive}")
            else:
                print(
                    "ERROR: checkpoint fingerprint mismatch (engine/arms/seed grid changed since these "
                    "checkpoints were made). Refusing to reuse them.\n"
                    f"  checkpoint dir: {ckpt_dir}\n"
                    f"  re-run with --fresh to archive them and start over.",
                    file=sys.stderr,
                )
                return EXIT_CONFIG
    _atomic_write_json(fp_path, {"schema": CHECKPOINT_SCHEMA, "created_utc": _utcnow(),
                                 "hardening_version": HARDENING_VERSION, "fingerprint": fingerprint,
                                 **fingerprint_payload})

    expected = len(specs) * len(seeds)
    valid_rows, invalid = _scan_checkpoints(ckpt_dir, specs, seeds, fingerprint)
    if invalid:
        print(f"WARNING: {len(invalid)} invalid checkpoint file(s) discarded and will be recomputed")
        for jur, arm_id, seed in invalid:
            try:
                os.remove(seed_ckpt_path(ckpt_dir, jur, arm_id, seed))
            except OSError:
                pass
    done0 = len(valid_rows)
    print(f"checkpoint dir: {ckpt_dir}")
    print(f"fingerprint: {fingerprint[:16]}…  checkpointed: {done0}/{expected}  "
          f"arms={len(specs)} seeds={len(seeds)}")
    resumed = done0 > 0
    _write_progress(ckpt_dir, done0, expected, None)

    missing_tasks = []
    for jur, arm_id, _label, params in specs:
        for seed in seeds:
            if (jur, arm_id, seed) in valid_rows:
                continue
            missing_tasks.append([jur, arm_id, seed, params,
                                  seed_ckpt_path(ckpt_dir, jur, arm_id, seed),
                                  _params_sha(params), fingerprint])

    host_pid = None
    host_log_path = os.path.join(ckpt_dir, "host.log")
    if missing_tasks:
        workers = args.workers if args.workers else default_workers()
        workers = max(1, min(workers, len(missing_tasks)))
        if args.dry_run:
            print(f"DRY-RUN: would run {len(missing_tasks)} tasks on {workers} workers; "
                  f"{done0}/{expected} already checkpointed")
            return EXIT_OK
        task_manifest = os.path.join(ckpt_dir, "pending_tasks.json")
        _atomic_write_json(task_manifest, missing_tasks)
        cmd = [sys.executable, os.path.abspath(__file__), "--role", "host",
               "--task-manifest", task_manifest, "--checkpoint-dir", ckpt_dir,
               "--workers", str(workers), "--seed-timeout", str(args.seed_timeout),
               "--arm-timeout", str(args.arm_timeout), "--fingerprint", fingerprint]
        print(f"spawning host: {len(missing_tasks)} tasks on {workers} workers "
              f"(seed_timeout={args.seed_timeout}s, stall_timeout={args.stall_timeout}s, "
              f"arm_timeout={args.arm_timeout}s)")
        with open(host_log_path, "w", encoding="utf-8") as host_log:
            host_proc = subprocess.Popen(cmd, stdout=host_log, stderr=subprocess.STDOUT,
                                         start_new_session=True)  # own process GROUP
        host_pid = host_proc.pid
        try:
            host_pgid = os.getpgid(host_pid)
        except ProcessLookupError:
            host_pgid = host_pid
        print(f"host pid={host_pid} pgid={host_pgid} started {_utcnow()}")
        last_count = _count_seed_files(ckpt_dir)
        last_token = _progress_token(ckpt_dir)
        last_progress = time.time()
        last_progress_utc = _utcnow()
        stall_reason = None
        while host_proc.poll() is None:
            time.sleep(1.0)
            count = _count_seed_files(ckpt_dir)
            token = _progress_token(ckpt_dir)
            if count > last_count or token != last_token:
                last_count = max(count, last_count)
                last_token = token
                last_progress = time.time()
                last_progress_utc = _utcnow()
                continue
            if time.time() - last_progress > args.stall_timeout:
                stall_reason = f"no checkpoint progress for {args.stall_timeout}s while host alive"
                break
            if time.time() - t_driver > args.arm_timeout and count == 0:
                stall_reason = f"no checkpoint progress at all within arm_timeout={args.arm_timeout}s"
                break
        if stall_reason is None:
            host_rc = host_proc.wait()
        else:
            log_tail = []
            try:
                log_tail = open(host_log_path, encoding="utf-8", errors="replace").read().splitlines()[-40:]
            except OSError:
                pass
            evidence_path = _write_stall_evidence(
                ckpt_dir, stall_reason, host_pid, host_pgid, count, expected,
                last_progress_utc, args.stall_timeout, log_tail)
            print(f"WATCHDOG: {stall_reason}. Killing process group {host_pgid} "
                  f"(SIGTERM -> SIGKILL). evidence: {evidence_path}", file=sys.stderr)
            signals_log = _kill_group(host_pid, host_pgid, grace_sec=args.kill_grace)
            try:
                host_rc = host_proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                host_rc = -9
            _driver_failure(ckpt_dir, {
                "failure_kind": "stall",
                "reason": stall_reason,
                "stall_evidence": evidence_path,
                "host_pid": host_pid,
                "host_pgid": host_pgid,
                "kill_signals": signals_log,
                "checkpoint_done": _count_seed_files(ckpt_dir),
                "expected": expected,
                "host_log": host_log_path,
                "host_exit_code": host_rc,
            })
            print(f"FAILED: run aborted by watchdog; checkpoints preserved in {ckpt_dir}. "
                  f"Re-run the SAME command to resume.", file=sys.stderr)
            return EXIT_STALL
        # host exited on its own: clean up any stragglers in its group (e.g. crash path)
        if host_rc != 0 or _pgid_alive(host_pgid):
            _kill_group(host_pid, host_pgid, grace_sec=args.kill_grace)
        if host_rc != EXIT_OK:
            log_tail = []
            try:
                log_tail = open(host_log_path, encoding="utf-8", errors="replace").read().splitlines()[-40:]
            except OSError:
                pass
            _driver_failure(ckpt_dir, {
                "failure_kind": "host_error",
                "reason": f"host exited rc={host_rc}",
                "host_pid": host_pid,
                "host_pgid": host_pgid,
                "checkpoint_done": _count_seed_files(ckpt_dir),
                "expected": expected,
                "host_log": host_log_path,
                "host_log_tail": log_tail,
            })
            print(f"FAILED: host exited rc={host_rc}; checkpoints preserved in {ckpt_dir}.", file=sys.stderr)
            return EXIT_HOST_ERROR
        # re-validate everything the host wrote (a host rc=0 is not trusted blindly)
        valid_rows, invalid = _scan_checkpoints(ckpt_dir, specs, seeds, fingerprint)
        if invalid or len(valid_rows) != expected:
            _driver_failure(ckpt_dir, {
                "failure_kind": "incomplete",
                "reason": f"after host rc=0: {len(valid_rows)}/{expected} valid checkpoints, "
                          f"{len(invalid)} invalid",
                "invalid": invalid,
                "checkpoint_dir": ckpt_dir,
            })
            print(f"FAILED: incomplete/invalid checkpoints after host rc=0 "
                  f"({len(valid_rows)}/{expected}); no final JSON written.", file=sys.stderr)
            return EXIT_INCOMPLETE

    # ---------------------------------------------------------------
    # Aggregation phase (small: JSON files only; cannot hang on pipes)
    # ---------------------------------------------------------------
    valid_rows, invalid = _scan_checkpoints(ckpt_dir, specs, seeds, fingerprint)
    if invalid or len(valid_rows) != expected:
        _driver_failure(ckpt_dir, {"failure_kind": "incomplete",
                                   "reason": f"{len(valid_rows)}/{expected} valid checkpoints before aggregation",
                                   "invalid": invalid})
        print(f"FAILED: {len(valid_rows)}/{expected} checkpoints before aggregation; no final JSON.",
              file=sys.stderr)
        return EXIT_INCOMPLETE
    # Publish each complete arm JSON atomically (already written by host; ensure it).
    for jur, arm_id, label, params in specs:
        rows = [valid_rows[(jur, arm_id, s)] for s in seeds]
        _write_arm_checkpoint(ckpt_dir, fingerprint, jur, arm_id, label, params, rows)
    elapsed = time.time() - t_driver
    payload = _build_payload(specs, valid_rows, elapsed, seeds)
    _atomic_write_json(out_path, payload)
    _atomic_write_json(os.path.join(ckpt_dir, "run_manifest.json"), {
        "schema": CHECKPOINT_SCHEMA,
        "status": "ok",
        "hardening_version": HARDENING_VERSION,
        "fingerprint": fingerprint,
        "out": out_path,
        "out_sha256": _sha256_file(out_path),
        "n_arms": len(specs),
        "n_seeds": len(seeds),
        "total_runs": len(payload["seeds"]),
        "workers": args.workers or default_workers(),
        "resumed": resumed,
        "checkpointed_before_run": done0,
        "computed_this_run": len(missing_tasks),
        "elapsed_seconds": round(elapsed, 3),
        "checkpoint_dir": ckpt_dir,
        "completed_utc": _utcnow(),
        "final_json_written": True,
    })
    _print_summary(payload, len(payload["seeds"]), elapsed, out_path, len(seeds))
    print(f"manifest: {os.path.join(ckpt_dir, 'run_manifest.json')} status=ok "
          f"resumed={resumed} computed={len(missing_tasks)}")
    return EXIT_OK


# ===========================================================================
# CLI
# ===========================================================================
def build_arg_parser():
    ap = argparse.ArgumentParser(description="Hardened HK/Korea 540-run contest experiment (Gate-2 precondition #3)")
    ap.add_argument("--role", choices=["driver", "host"], default="driver", help=argparse.SUPPRESS)
    ap.add_argument("--task-manifest", default="", help=argparse.SUPPRESS)
    ap.add_argument("--fingerprint", default="", help=argparse.SUPPRESS)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--checkpoint-dir", default=DEFAULT_CKPT)
    ap.add_argument("--workers", type=int, default=0, help="0 = memory-aware auto cap")
    ap.add_argument("--seed-timeout", type=float, default=600.0,
                    help="max seconds for a single seed result to arrive (host watchdog)")
    ap.add_argument("--arm-timeout", type=float, default=1800.0,
                    help="max seconds for one arm to complete (host watchdog)")
    ap.add_argument("--stall-timeout", type=float, default=180.0,
                    help="max seconds with no checkpoint progress (driver watchdog -> group kill)")
    ap.add_argument("--kill-grace", type=float, default=10.0,
                    help="seconds between SIGTERM and SIGKILL for the process group")
    ap.add_argument("--smoke-arms", type=int, default=0, help="only first N arms PER JURISDICTION (smoke runs; N=3 -> 6 arms)")
    ap.add_argument("--smoke-seeds", type=int, default=0, help="only first N seeds (smoke runs)")
    ap.add_argument("--fresh", action="store_true", help="archive checkpoint dir if fingerprint changed")
    ap.add_argument("--dry-run", action="store_true", help="report missing tasks without running")
    return ap


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    if args.role == "host":
        return host_main(args)
    return driver_main(args)


if __name__ == "__main__":
    sys.exit(main())
