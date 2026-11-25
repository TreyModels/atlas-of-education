import json, math, sys
import numpy as np
sys.path.insert(0, "/root/work/contest/papers/shadow-education-contest/code")
from run_hk_korea_comparative import build_arms, _run_single

def canon(o):
    if isinstance(o, dict):
        return {str(k): canon(v) for k, v in sorted(o.items())}
    if isinstance(o, (list, tuple)):
        return [canon(v) for v in o]
    if isinstance(o, np.ndarray):
        return [canon(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)):
        f = float(o)
        if math.isnan(f):
            return "nan"
        if math.isinf(f):
            return "inf" if f > 0 else "-inf"
        return f.hex()
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o

out = {}
for jur in ("HK", "KR"):
    arm = [s for s in build_arms() if s[0] == jur and s[1] == "Baseline"][0]
    out[jur] = canon(_run_single((arm[0], arm[1], 0, arm[3])))
json.dump(out, open(sys.argv[1], "w"), indent=1, sort_keys=True)
print("wrote", sys.argv[1], "jurisdictions", list(out))
