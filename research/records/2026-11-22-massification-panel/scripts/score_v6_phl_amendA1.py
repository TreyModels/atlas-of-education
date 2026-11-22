"""Score Amendment A1 runs (P0h_con, P0h_unc) on the same held-out rows. Reported separately from the registered winner."""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import run_v6_phl_amendA1  # registers specs
import masseng.engine_v6_phl as E
from masseng.data import Country
from masseng import calibrate5 as C5
OUT = Path("outputs/PHL/v6_phl")
c = Country("PHL"); rows = C5.build_rows(c)
test = [r for r in rows if r["role"] == "test"]
ger = [r for r in test if r["series"] in ("ger_primary", "ger_secondary", "ger_tertiary")]
obs = np.array([r["value"] for r in ger])
out = {}
for spec in ("P0h_con", "P0h_unc"):
    f = json.loads((OUT / f"fit_{spec}.json").read_text())
    res, table = E.score_v6_phl(c, f, rows)
    p = np.asarray(C5._pred(res, ger), float); m = np.isfinite(p)
    yrs = list(res.years)
    out[spec] = dict(
        status="Amendment A1 run (post-inspection); not eligible as registered winner",
        train_cost=f["cost"], at_bounds=f["at_bounds"], dials_at_bounds=f["dials_at_bounds"],
        b_h=f["params"]["b_h"], eta=f["params"]["eta"],
        three_ger_rmse=float(np.sqrt(np.mean((p[m] - obs[m]) ** 2))),
        per_ger={g: table[g]["model"] for g in ("ger_primary", "ger_secondary", "ger_tertiary")},
        private_share_rmse={s: table[s]["model"] for s in table if s.startswith("priv_")},
        tertiary_ger_2013=float(res.ind["ger_tertiary"][yrs.index(2013)]),
        tertiary_ger_2024=float(res.ind["ger_tertiary"][yrs.index(2024)]),
    )
    print(spec, round(out[spec]["three_ger_rmse"], 3), out[spec]["dials_at_bounds"], "b_h", round(out[spec]["b_h"], 3), "ter2024", round(out[spec]["tertiary_ger_2024"], 1))
(OUT / "scores_amendA1.json").write_text(json.dumps(out, indent=2) + "\n")
