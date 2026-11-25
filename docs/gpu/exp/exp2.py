"""
Decisive experiment, part 2: CUDA-graph replay of the 405-call chain.

Same float32 arithmetic as exp1 (sequential scan, float64 exp preprocessing on CPU,
reference renormalisation), but the ~3000-op DP for a batch is captured once per
(n, d, M1) shape and replayed, which removes the per-op Python dispatch cost that
dominates the 14.9 ms/call in exp1.
"""
import argparse, json, math, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import exp1  # noqa: E402  (sets up sys.path for ref/)
import contest_math as cm  # noqa: E402
import torch  # noqa: E402

DEV = "cuda"
B_MAX = 9


class BatchedQuad:
    def __init__(self, n, d, below, sign, offc, M1, B=B_MAX):
        self.n, self.d, self.B, self.M1 = n, d, B, M1
        self.sign, self.offc = sign, offc
        z64 = lambda *s: torch.zeros(s, dtype=torch.float64, device=DEV)
        z32 = lambda *s: torch.zeros(s, dtype=torch.float32, device=DEV)
        self.WN = z64(B, n)
        self.T = z64(B, M1)
        self.SW = z64(B, M1)
        self.PB = z32(B, n, M1)
        self.QA = torch.ones((B, n, M1), dtype=torch.float32, device=DEV)
        self.Suf = z32(B, n + 1, d + 1, M1)
        self.PreA = z32(B, d + 1, M1)
        self.PreB = z32(B, d + 1, M1)
        self.out = torch.empty((B, n), dtype=torch.float64, device=DEV)
        self.f_stay, self.f_inc = (self.QA, self.PB) if below else (self.PB, self.QA)
        self.g = torch.cuda.CUDAGraph()
        s = torch.cuda.Stream()
        s.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(s):
            for _ in range(2):
                self._run()
        torch.cuda.current_stream().wait_stream(s)
        torch.cuda.synchronize()
        with torch.cuda.graph(self.g):
            self._run()

    def _run(self):
        n, d, B, M1 = self.n, self.d, self.B, self.M1
        f_stay, f_inc = self.f_stay, self.f_inc
        Suf = self.Suf
        Suf.zero_()
        Suf[:, n, 0, :] = 1.0
        for i in range(n - 1, -1, -1):
            cur = Suf[:, i + 1]
            nxt = Suf[:, i]
            torch.mul(cur, f_stay[:, i, None, :], out=nxt)
            nxt[:, 1:, :] += f_inc[:, i, None, :] * cur[:, :-1, :]
        for a in range(1, d + 1):                       # sequential scan == reference order
            Suf[:, :, a, :] += Suf[:, :, a - 1, :]
        Pre = self.PreA
        tmp = self.PreB
        Pre.zero_()
        Pre[:, 0, :] = 1.0
        out = self.out
        for i in range(n):
            tail = (Pre * Suf[:, i + 1, :, :].flip(1)).sum(dim=1)          # float32
            G = torch.clamp(self.offc + self.sign * tail.double(), 0.0, 1.0)
            kernel = self.WN[:, i:i + 1] * self.T * self.QA[:, i, :].double()
            out[:, i] = (self.SW * kernel * G).sum(dim=1)
            torch.mul(Pre, f_stay[:, i, None, :], out=tmp)
            tmp[:, 1:, :] += f_inc[:, i, None, :] * Pre[:, :-1, :]
            Pre, tmp = tmp, Pre
        return out

    def feed(self, calls):
        """calls: list of <=B prep dicts (all same n/d/below). Pads by repeating the last."""
        B = self.B
        idx = list(range(len(calls))) + [len(calls) - 1] * (B - len(calls))
        WN = np.stack([calls[j]["wn"] for j in idx])
        T = np.zeros((B, self.M1), dtype=np.float64)
        SW = np.zeros((B, self.M1), dtype=np.float64)
        PB = np.zeros((B, self.n, self.M1), dtype=np.float32)
        QA = np.ones((B, self.n, self.M1), dtype=np.float32)
        for b, j in enumerate(idx):
            c = calls[j]
            m1 = c["m"] + 1
            T[b, :m1] = c["t"]
            SW[b, :m1] = c["sw"]
            PB[b, :, :m1] = c["PB"]
            QA[b, :, :m1] = c["QA"]
        self.WN.copy_(torch.from_numpy(np.ascontiguousarray(WN)))
        self.T.copy_(torch.from_numpy(T))
        self.SW.copy_(torch.from_numpy(SW))
        self.PB.copy_(torch.from_numpy(PB))
        self.QA.copy_(torch.from_numpy(QA))

    def replay(self):
        self.g.replay()
        return self.out


def run(mode):
    meta = json.load(open(os.path.join(HERE, "perf_calls.json")))
    rng = np.random.default_rng(20261125)
    ws = [exp1.make_w(c["n"], c["wmin"], c["wmax"], rng) for c in meta]
    seats = [c["seats"] for c in meta]

    # ---- CPU reference (cold caches), same process ----
    cm._RESULT_CACHE.clear()
    cm._GRID_CACHE.clear()
    t0 = time.perf_counter()
    cpu_p = [np.asarray(cm.pl_win_probs(w, s), float) for w, s in zip(ws, seats)]
    t_cpu = time.perf_counter() - t0

    # ---- CPU-side preprocessing (same as reference; unavoidable in the real path) ----
    t0 = time.perf_counter()
    calls = [exp1.prep_call(w, s) for w, s in zip(ws, seats)]
    t_prep = time.perf_counter() - t0

    M1 = max(c["m"] + 1 for c in calls)
    engines = {}
    for c in calls:
        key = (c["n"], c["d"], c["below"])
        if key not in engines:
            engines[key] = BatchedQuad(c["n"], c["d"], c["below"], c["sign"], c["offc"], M1)

    # batch arbitrary same-(n,below) calls in chunks of B_MAX
    buckets = {}
    for k, c in enumerate(calls):
        buckets.setdefault((c["n"], c["d"], c["below"]), []).append(k)

    t0 = time.perf_counter()
    gpu_p = [None] * len(calls)
    n_batches = 0
    for key, idxs in buckets.items():
        eng = engines[key]
        for s in range(0, len(idxs), B_MAX):
            chunk = idxs[s:s + B_MAX]
            eng.feed([calls[k] for k in chunk])
            out = eng.replay().cpu().numpy()
            n_batches += 1
            for b, k in enumerate(chunk):
                gpu_p[k] = cm._renormalize_to_seats(out[b], calls[k]["seats"])
    t_replay = time.perf_counter() - t0

    diffs = [float(np.max(np.abs(np.asarray(cpu_p[k]) - gpu_p[k]))) for k in range(len(calls))]
    t_gpu_total = t_prep + t_replay
    return dict(mode="bench_graphs", n_calls=len(calls), n_batches=n_batches, M1=M1,
                t_cpu_s=round(t_cpu, 4), t_prep_s=round(t_prep, 4),
                t_replay_s=round(t_replay, 4), t_gpu_total_s=round(t_gpu_total, 4),
                pl_speedup=round(t_cpu / t_gpu_total, 2),
                e2e_cpu_s=round(t_cpu + 1.93, 3), e2e_gpu_s=round(t_gpu_total + 1.93, 3),
                e2e_speedup=round((t_cpu + 1.93) / (t_gpu_total + 1.93), 2),
                max_abs_diff=float(max(diffs)), mean_abs_diff=float(np.mean(diffs)),
                pass_dev=bool(max(diffs) <= 1e-7),
                pass_pl_3x=bool(t_cpu / t_gpu_total >= 3.0),
                pass_e2e_3x=bool((t_cpu + 1.93) / (t_gpu_total + 1.93) >= 3.0))


if __name__ == "__main__":
    torch.cuda.init()
    res = run("bench")
    print("RESULT_JSON " + json.dumps([res]))
