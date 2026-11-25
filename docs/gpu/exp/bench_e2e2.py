import json, sys, time
sys.path.insert(0, "/root/work/contest/papers/shadow-education-contest/code")
import eduengine  # noqa: F401  (registers the GPU backend when ATLAS_PL_BACKEND=gpu)
from eduengine import contest_math as cm
from run_hk_korea_comparative import build_arms, _run_single

arm_of = {(s[0], s[1]): s for s in build_arms()}
out = {"backend": cm.pl_backend(), "runs": []}
for jur in ("HK", "KR"):
    arm = arm_of[(jur, "Baseline")]
    for rep in (1, 2):
        t_cpu = time.process_time(); t_wall = time.perf_counter()
        res = _run_single((arm[0], arm[1], 0, arm[3]))
        out["runs"].append(dict(jur=jur, rep=rep,
                                cpu_s=round(time.process_time() - t_cpu, 3),
                                wall_s=round(time.perf_counter() - t_wall, 3),
                                k12_spend=float(res.get("k12_spend", float("nan"))),
                                g12_rate=float(res.get("g12_rate", float("nan")))))
out["stats"] = cm.pl_stats()
print("E2E2_JSON " + json.dumps(out))
