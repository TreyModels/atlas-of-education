import csv, sys, math
from pathlib import Path
import numpy as np

CODE = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE / "frozen"))
import sim_v1_6_repair as S

SYNTH = CODE.resolve().parents[1] / "synthetic_2026-11-20"
S.ROOT = SYNTH / "generator_v1_6_repair"; S.SYNTH = SYNTH
S.MASS = SYNTH.parents[1]; S.DATA = S.MASS / "data"
V13 = SYNTH / "generator_v1_3" / "results" / "synthetic_panel_v1_3.csv"
A10 = SYNTH / "generator_v1_6_repair" / "results" / "panel_A10_repaired.csv"

band, pop = {}, {}
with open(V13, newline="") as fh:
    for r in csv.DictReader(fh):
        if r["country"] != "SYN00_PHL_LIKE": continue
        y = int(float(r["year"])); pop[y] = float(r["population"])
        if r["level"] == "primary": band[y] = float(r["band_population"])
Sp = np.array([band[int(y)] / S.P["band_share"][0] for y in S.YEARS])
Pp = np.array([pop[int(y)] for y in S.YEARS])
S.load_observed_phl_paths = lambda: (Sp, Pp, {}, {}, {})

res, hosts = S.run_arm_full(bimodal=True)
print("PHL host:", hosts.get("SYN_PHL_LIKE"))
i = [j for j, r in enumerate(res) if r["cp"]["name"] == "SYN00_PHL_LIKE"][0]
r = res[i]

obs = {}
with open(A10, newline="") as fh:
    for row in csv.DictReader(fh):
        if row["country"] != "SYN00_PHL_LIKE": continue
        obs[(row["level"], int(float(row["year"])))] = row

cols = ["demand_official", "cohort", "admitted_official", "seats", "survival", "completion_uis",
        "demand_share", "admitted_overage", "gdppc", "eligibility_pool"]
worst = {}
for L, lv in enumerate(S.LEVELS):
    for y in range(2010, 2025):
        t = y - S.YEAR_START
        row = obs[(lv, y)]
        for c in cols:
            a = float(row[c])
            if c == "demand_official": b = float(r["demand_off"][L, t])
            elif c == "cohort": b = float(r["C"][L, t])
            elif c == "admitted_official": b = float(r["intake_off"][L, t])
            elif c == "seats": b = float(r["seats"][L, t])
            elif c == "survival": b = float(r["surv"][L, t])
            elif c == "completion_uis": b = float(r["comp_uis"][L, t])
            elif c == "demand_share": b = float(r["demand_share"][L, t])
            elif c == "admitted_overage": b = float(r["intake_oa"][L, t])
            elif c == "gdppc": b = float(r["Y"][t])
            elif c == "eligibility_pool": b = float(r["pool"][L, t])
            rel = abs(a - b) / max(abs(a), 1e-9)
            k = c
            if rel > worst.get(k, (0,))[0]:
                worst[k] = (rel, lv, y, a, b)
for k, v in worst.items():
    print("%-18s maxrel %.3e at %s %d (panel %.10g vs run %.10g)" % (k, v[0], v[1], v[2], v[3], v[4]))
