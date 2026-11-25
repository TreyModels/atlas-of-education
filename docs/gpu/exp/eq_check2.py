import json, sys, time
import numpy as np
sys.path.insert(0, '/root/work/gpuport/e2e/engine')
from eduengine import contest_math as cm

rng = np.random.default_rng(20261125)
fx = []
for _ in range(130):
    n = int(rng.choice([12, 20, 21, 40, 60, 80, 120, 200, 300, 300, 300, 400, 600]))
    seats = int(rng.integers(1, n))
    disp = float(rng.choice([0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]))
    w = np.ones(n) if disp == 0.0 else np.exp(disp * rng.standard_normal(n))
    fx.append((n, seats, disp, w))

cm.set_pl_backend('cpu')
t0 = time.perf_counter()
ref = [np.asarray(cm.pl_win_probs(w, s), float) for (n, s, disp, w) in fx]
t_cpu = time.perf_counter() - t0

cm.set_pl_backend('gpu')
rows = []
t0 = time.perf_counter()
for k, (n, s, disp, w) in enumerate(fx):
    p = np.asarray(cm.pl_win_probs_batch(np.asarray([w]), s)[0], float)
    d = float(np.max(np.abs(p - ref[k])))
    rows.append(dict(n=n, seats=s, disp=disp, d=d))
t_gpu = time.perf_counter() - t0
worst = max(rows, key=lambda r: r['d'])
print("EQ2_JSON " + json.dumps(dict(
    n=len(rows), max_abs_diff=worst['d'], worst=worst,
    mean_abs_diff=float(np.mean([r['d'] for r in rows])),
    n_gt_1e7=int(sum(r['d'] > 1e-7 for r in rows)),
    n_gt_1e6=int(sum(r['d'] > 1e-6 for r in rows)),
    t_cpu_s=round(t_cpu, 3), t_gpu_batch_s=round(t_gpu, 3), rows=rows)))
