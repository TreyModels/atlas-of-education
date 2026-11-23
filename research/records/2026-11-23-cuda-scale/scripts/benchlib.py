"""Shared helpers for the cuda-scale benchmark suite (box2, RTX 2080 Ti).

All runs are the GPU dose engine (kernel.cu + engine.py copied from /root/work/dose_gpu/src,
untouched).  A "run" is 14 cohorts x 2 urban/rural x 5 wealth quintiles x nW=12 women = 1680
woman-records; years 1945..2012 stepped sequentially.  Engine state lives entirely in the
GPUDose object; this module measures it exactly (sum of every device array's nbytes).
"""
import os, sys, json, time, subprocess
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/root/work/cuda_scale")
import cupy as cp
from engine import GPUDose, targets_array, make_spec
import dosecore as dc

RESULTS = "/root/work/cuda_scale/results"
os.makedirs(RESULTS, exist_ok=True)
PANEL_PATH = os.environ.get("DOSE_PANEL", "/root/work/cuda_scale/data/panel.json")
PAN = json.load(open(PANEL_PATH))
FIT = PAN["FIT"]

NW = 12
WPR = 14 * 2 * 5 * NW          # women-records per run = 1680
TMAX = 2012
YEARS = TMAX - 1945 + 1        # 68 calendar years stepped


def log(*a):
    print(*a, flush=True)


def gpu_stat():
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total,utilization.gpu,"
             "temperature.gpu,clocks.sm,power.draw",
             "--format=csv,noheader"], text=True, timeout=10).strip()
    except Exception as e:                       # never let telemetry kill a benchmark
        out = "unavailable: %s" % e
    return out


def build_specs(n, seed=3, scen=0, fc=0.0):
    """n independent runs: random parameter draw (uniform over the prior box) x country.
    Same construction as research/records/2026-11-23-dose-gpu/scripts/bench_scale.py."""
    rng = np.random.default_rng(seed)
    specs = []
    for i in range(n):
        iso = FIT[i % len(FIT)]
        pc = PAN["countries"][iso]
        th = dc.LO + rng.random(dc.D_) * (dc.HI - dc.LO)
        specs.append(make_spec(pc, th, scen, fc, pc["age_gap"], 7, i))
    return specs


def state_bytes(eng):
    """Exact device bytes held by the engine: every cupy array it owns."""
    total, biggest, n_arr = 0, 0, 0
    for v in vars(eng).values():
        if isinstance(v, cp.ndarray):
            total += v.nbytes
            biggest = max(biggest, v.nbytes)
            n_arr += 1
    return total, biggest, n_arr


def mem(free=True):
    f, t = cp.cuda.runtime.memGetInfo()
    return dict(free_bytes=int(f), total_bytes=int(t))


def free_pool():
    cp.get_default_memory_pool().free_all_blocks()
    cp.get_default_pinned_memory_pool().free_all_blocks()


def dump(name, obj):
    path = os.path.join(RESULTS, name)
    json.dump(obj, open(path, "w"), indent=1, default=str)
    log("wrote", path)
    return path


def array_digest(a):
    import hashlib
    a = np.ascontiguousarray(a)
    return hashlib.sha256(a.tobytes()).hexdigest()[:16]


def compare(a, b):
    """Exact comparison, NaNs allowed to match NaNs."""
    a = np.asarray(a); b = np.asarray(b)
    same = bool(np.array_equal(a, b, equal_nan=True))
    with np.errstate(all="ignore"):
        finite = np.isfinite(a) & np.isfinite(b)
        maxdiff = float(np.max(np.abs(a[finite] - b[finite]))) if finite.any() else 0.0
        nan_mismatch = int(np.sum(np.isnan(a) != np.isnan(b)))
    return dict(bitwise_identical=same, max_abs_diff=maxdiff,
                nan_pattern_mismatches=nan_mismatch,
                digest_a=array_digest(a), digest_b=array_digest(b))
