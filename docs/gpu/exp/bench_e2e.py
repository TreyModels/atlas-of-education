import json, sys, time
import numpy as np
sys.path.insert(0, "/root/work/contest/papers/shadow-education-contest/code")
import eduengine  # noqa: F401  (registers the GPU backend when ATLAS_PL_BACKEND=gpu)
from eduengine import contest_math as cm
from run_hk_korea_comparative import build_arms, _run_single

arm = [s for s in build_arms() if s[0] == "HK" and s[1] == "Baseline"][0]
t_cpu = time.process_time(); t_wall = time.perf_counter()
res = _run_single((arm[0], arm[1], 0, arm[3]))
out = dict(jur=arm[0], arm=arm[1], seed=0,
           cpu_s=round(time.process_time() - t_cpu, 3),
           wall_s=round(time.perf_counter() - t_wall, 3),
           backend=cm.pl_backend(), stats=cm.pl_stats(),
           k12_spend=float(res.get("k12_spend", float("nan"))),
           k12_rate=float(res.get("k12_rate", float("nan"))))
print("E2E_JSON " + json.dumps(out))
