"""No-refit sensitivity of the headline to lam_g (review 1.3). Holds every other on-disk parameter fixed.
Run: python lam_sensitivity.py -> results/lam_sensitivity.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import K, ENGINE, dump, summarise, START  # noqa: E402
from run_fits import ondisk  # noqa: E402

base = {k: v for k, v in ondisk('full').items()}
out = {}
for lam in (1.0, 0.0561, 0.0156, 0.0124, 0.0025):
    p = dict(base, lam_g=lam)
    s = summarise({k: p[k] for k in START}, {}, 'full')
    out[str(lam)] = dict(rate_change=s['rate_change'], late_rate=s['late_rate'], grad_u_change=s['grad_u_change'],
                         fit_early_mae=s['fit_early']['mae'], whole_record_mae=s['whole_record']['mae'],
                         new_verified_mae=s['new_verified']['mae'])
    print(lam, {k: round(v, 3) for k, v in out[str(lam)].items()})
dump('lam_sensitivity.json', dict(base_params={k: base[k] for k in START}, rows=out))
