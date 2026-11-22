"""Diagnostic A2 (2026-11-22, post-inspection, NOT eligible for selection).
Question: are the household-spending rows (FIES 2003/2006, x10 scale) driving the private-share misfit
and the nu_basic/nu_ter bound hits? Refit P2_con with all edu_share_* training rows removed, then score.
"""
import json, sys
from pathlib import Path
import numpy as np
import masseng.engine_v6_phl as E
from masseng.data import Country
from masseng import calibrate5 as C5
OUT = Path("outputs/PHL/v6_phl"); OUT.mkdir(parents=True, exist_ok=True)
c = Country("PHL"); rows = C5.build_rows(c)
train = [r for r in rows if r["role"] == "train" and not r["series"].startswith("edu_share")]
f = E.fit_v6_phl(c, train, spec="P2_con", max_nfev=250, ftol=1e-7)
res, table = E.score_v6_phl(c, f, rows)
test = [r for r in rows if r["role"] == "test"]
ger = [r for r in test if r["series"] in ("ger_primary", "ger_secondary", "ger_tertiary")]
p = np.asarray(C5._pred(res, ger), float); o = np.array([r["value"] for r in ger]); m = np.isfinite(p)
full = [r for r in rows if r["role"] == "train"]
pt = C5._pred(res, full)
out = dict(status="DIAGNOSTIC A2 — post-inspection; not eligible for selection",
           dropped_train_series=["edu_share_hh", "edu_share_bottom30", "edu_share_top70"],
           fit=f, three_ger_rmse=float(np.sqrt(np.mean((p[m]-o[m])**2))),
           per_series={s: table[s]["model"] for s in table},
           fitted_spending_shares={f"{r['series']} {r['year']}": [r["value"], float(v)] for r, v in zip(full, pt) if r["series"].startswith("edu_share")})
(OUT / "diag_A2_no_spending_rows.json").write_text(json.dumps(out, indent=2) + "\n")
print("A2 3GER", round(out["three_ger_rmse"], 3), "at_bounds", f["at_bounds"], "priv_primary", round(table["priv_primary"]["model"], 2), "priv_tertiary", round(table["priv_tertiary"]["model"], 2))
print(out["fitted_spending_shares"])
