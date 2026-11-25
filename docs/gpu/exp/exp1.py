"""
Decisive Gate-1 experiment: torch float32 batched replica of
engine/eduengine/contest_math.py::_quadrature_win_probs, vs the CPU reference.

Modes:
  bench     -- 405 REAL call shapes from perf_calls.json (one HK Baseline run):
               CPU reference wall, GPU (batched) wall, max|dP| per call.
  fixtures  -- the 130-fixture equivalence sweep (n>20 path), max|dP|.
Writes JSON to stdout.  CPU-only for the reference; 1 process.
"""
import argparse, json, math, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "ref"))
import contest_math as cm  # noqa: E402

import torch  # noqa: E402

DEV = "cuda"
torch.backends.cuda.matmul.allow_tf32 = False
C = cm._QUAD_TAIL_C
PT = cm._QUAD_T_LO
H = cm._QUAD_H
CAP = cm._QUAD_MAX_NODES


def m_of(w_min):
    span = math.log(C / w_min) - math.log(PT)
    m = int(math.ceil(span / H))
    if m < 2:
        m = 2
    if m % 2:
        m += 1
    if m + 1 > CAP:
        m = CAP - 1
        if m % 2:
            m -= 1
    return m


def prep_call(w, seats):
    """Exactly the reference's float64 preprocessing; returns numpy float32 DP inputs."""
    wn = cm._normalized_weights(np.asarray(w, dtype=np.float64))
    wn = np.maximum(wn, cm._QUAD_W_FLOOR)
    n = wn.size
    seats = cm._as_seats(seats, n)
    if 0 < seats < n:
        below = (seats - 1) <= (n - seats - 1)
        d = max((seats - 1) if below else (n - seats - 1), 0)
        t, sw, m = cm._simpson_grid(float(wn.min()))
        PB = (-np.expm1(-(wn[:, None] * t[None, :]))).astype(np.float32)
        QA = np.exp(-(wn[:, None] * t[None, :])).astype(np.float32)
        return dict(wn=wn, t=t, sw=sw, m=m, PB=PB, QA=QA, below=below, d=d,
                    sign=(1.0 if below else -1.0), offc=(0.0 if below else 1.0),
                    n=n, seats=seats)
    return None


def quad_gpu_batch(calls, M1, seq_scan=True):
    """calls: list of dicts from prep_call (same n, seats, below, d, M1 padding)."""
    B = len(calls)
    n = calls[0]["n"]
    d = calls[0]["d"]
    below = calls[0]["below"]
    sign, offc = calls[0]["sign"], calls[0]["offc"]
    WN = torch.from_numpy(np.ascontiguousarray(np.stack([c["wn"] for c in calls]))).to(DEV)
    T = torch.zeros((B, M1), dtype=torch.float64, device=DEV)
    SW = torch.zeros((B, M1), dtype=torch.float64, device=DEV)
    PB = torch.zeros((B, n, M1), dtype=torch.float32, device=DEV)
    QA = torch.ones((B, n, M1), dtype=torch.float32, device=DEV)
    for b, c in enumerate(calls):
        m1 = c["m"] + 1
        T[b, :m1] = torch.from_numpy(c["t"])
        SW[b, :m1] = torch.from_numpy(c["sw"])
        PB[b, :, :m1] = torch.from_numpy(c["PB"])
        QA[b, :, :m1] = torch.from_numpy(c["QA"])
    f_stay, f_inc = (QA, PB) if below else (PB, QA)
    Suf = torch.zeros((B, n + 1, d + 1, M1), dtype=torch.float32, device=DEV)
    Suf[:, n, 0, :] = 1.0
    for i in range(n - 1, -1, -1):
        cur = Suf[:, i + 1]
        nxt = Suf[:, i]
        torch.mul(cur, f_stay[:, i, None, :], out=nxt)
        nxt[:, 1:, :] += f_inc[:, i, None, :] * cur[:, :-1, :]
    if seq_scan:                      # reference is a sequential float32 accumulate
        for a in range(1, d + 1):
            Suf[:, :, a, :] += Suf[:, :, a - 1, :]
    else:
        Suf = torch.cumsum(Suf, dim=2)
    out = torch.empty((B, n), dtype=torch.float64, device=DEV)
    Pre = torch.zeros((B, d + 1, M1), dtype=torch.float32, device=DEV)
    Pre[:, 0, :] = 1.0
    for i in range(n):
        tail = (Pre * Suf[:, i + 1, :, :].flip(1)).sum(dim=1)          # float32
        G = torch.clamp(offc + sign * tail.double(), 0.0, 1.0)          # float64
        kernel = WN[:, i:i + 1] * T * QA[:, i, :].double()
        out[:, i] = (SW * kernel * G).sum(dim=1)
        tmp = Pre * f_stay[:, i, None, :]
        tmp[:, 1:, :] += f_inc[:, i, None, :] * Pre[:, :-1, :]
        Pre = tmp
    return out.cpu().numpy()


def make_w(n, wmin, wmax, rng):
    sig = max(math.log(wmax / wmin) / 6.0, 1e-3)
    w = np.exp(sig * rng.standard_normal(n))
    return w / w.max() * wmax


def bench(seq_scan, batch_cap=9):
    calls_meta = json.load(open(os.path.join(HERE, "perf_calls.json")))
    rng = np.random.default_rng(20261125)
    ws = [make_w(c["n"], c["wmin"], c["wmax"], rng) for c in calls_meta]
    seats = [c["seats"] for c in calls_meta]
    # ---- CPU reference, same process, caches cold ----
    cm._RESULT_CACHE.clear()
    cm._GRID_CACHE.clear()
    t0 = time.perf_counter()
    cpu_p = [np.asarray(cm.pl_win_probs(w, s), float) for w, s in zip(ws, seats)]
    t_cpu = time.perf_counter() - t0
    # ---- prep + group ----
    calls = [prep_call(w, s) for w, s in zip(ws, seats)]
    M1 = max(c["m"] + 1 for c in calls)
    groups = []
    for k, c in enumerate(calls):
        if groups and calls[groups[-1][0]]["n"] == c["n"] and len(groups[-1]) < batch_cap:
            groups[-1].append(k)
        else:
            groups.append([k])
    # ---- GPU ----
    t0 = time.perf_counter()
    gpu_p = [None] * len(calls)
    for gidx in groups:
        P = quad_gpu_batch([calls[k] for k in gidx], M1, seq_scan)
        for b, k in enumerate(gidx):
            gpu_p[k] = cm._renormalize_to_seats(P[b], calls[k]["seats"])
    t_gpu = time.perf_counter() - t0
    diffs = [float(np.max(np.abs(np.asarray(cpu_p[k]) - gpu_p[k]))) for k in range(len(calls))]
    return dict(mode="bench", n_calls=len(calls), n_groups=len(groups), M1=M1,
                seq_scan=seq_scan, t_cpu_s=round(t_cpu, 4), t_gpu_s=round(t_gpu, 4),
                speedup=round(t_cpu / t_gpu, 3),
                max_abs_diff=float(max(diffs)), mean_abs_diff=float(np.mean(diffs)),
                cpu_s_per_call=round(t_cpu / len(calls), 5),
                gpu_s_per_call=round(t_gpu / len(calls), 5))


def fixtures(seq_scan):
    rng = np.random.default_rng(20261125)
    rows = []
    t_cpu = t_gpu = 0.0
    for _ in range(130):
        n = int(rng.choice([12, 20, 21, 40, 60, 80, 120, 200, 300, 300, 300, 400, 600]))
        seats = int(rng.integers(1, n))
        disp = float(rng.choice([0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]))
        w = np.ones(n) if disp == 0.0 else np.exp(disp * rng.standard_normal(n))
        t0 = time.perf_counter()
        p_cpu = np.asarray(cm.pl_win_probs(w, seats), float)
        t_cpu += time.perf_counter() - t0
        if n <= 20:                      # exact-DP path: unchanged, CPU
            rows.append(dict(n=n, seats=seats, disp=disp, path="exact", d=0.0))
            continue
        c = prep_call(w, seats)
        t0 = time.perf_counter()
        P = quad_gpu_batch([c], c["m"] + 1, seq_scan)[0]
        p_gpu = cm._renormalize_to_seats(P, seats)
        t_gpu += time.perf_counter() - t0
        rows.append(dict(n=n, seats=seats, disp=disp, path="quad",
                         d=float(np.max(np.abs(p_cpu - p_gpu)))))
    quad = [r for r in rows if r["path"] == "quad"]
    return dict(mode="fixtures", n=len(rows), n_quad=len(quad),
                seq_scan=seq_scan,
                max_abs_diff=float(max(r["d"] for r in rows)),
                max_abs_diff_quad=float(max(r["d"] for r in quad)),
                mean_abs_diff=float(np.mean([r["d"] for r in rows])),
                t_cpu_s=round(t_cpu, 3), t_gpu_s=round(t_gpu, 3),
                pass_1e7=bool(max(r["d"] for r in rows) <= 1e-7),
                rows=rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="bench", choices=["bench", "fixtures", "both"])
    ap.add_argument("--seq-scan", action="store_true", default=False)
    a = ap.parse_args()
    torch.cuda.init()
    out = []
    if a.mode in ("fixtures", "both"):
        out.append(fixtures(a.seq_scan))
    if a.mode in ("bench", "both"):
        out.append(bench(a.seq_scan))
    print("RESULT_JSON " + json.dumps(out))
