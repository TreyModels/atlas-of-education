import csv
from pathlib import Path
A10 = Path("../synthetic_2026-11-20/generator_v1_6_repair/results/panel_A10_repaired.csv").resolve()
V13 = Path("../synthetic_2026-11-20/generator_v1_3/results/synthetic_panel_v1_3.csv").resolve()
def rows(path, country="SYN00_PHL_LIKE"):
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["country"] != country: continue
            if int(float(r["year"])) in (2010, 2015, 2020, 2023, 2024):
                yield r
print("== A10 (frozen v1.6 P0) ==")
for lv in ("primary", "lower_secondary", "upper_secondary"):
    for r in rows(A10):
        if r["level"] != lv: continue
        d = float(r["demand_official"]); c = float(r["cohort"])
        print(lv, r["year"], "dem/coh %.10f" % (d/c), "adm/coh %.10f" % (float(r["admitted_official"])/c),
              "seats/coh %.6f" % (float(r["seats"])/c), "K_H %.6f" % (float(r["tier_K_H"])/c),
              "A_H/coh %.6f" % (float(r["tier_A_H"])/c), "T_O/coh %.6f" % (float(r["tier_T_O"])/c),
              "unf %.6f" % float(r["tier_O_unfilled_share"]))
print("== v1.3 frozen block ==")
for lv in ("primary", "lower_secondary", "upper_secondary"):
    for r in rows(V13):
        if r["level"] != lv: continue
        d = float(r["demand_official"]); c = float(r["cohort"])
        print(lv, r["year"], "dem/coh %.10f" % (d/c), "adm/coh %.10f" % (float(r["admitted_official"])/c),
              "dem_share %.10f" % float(r["demand_share"]))
