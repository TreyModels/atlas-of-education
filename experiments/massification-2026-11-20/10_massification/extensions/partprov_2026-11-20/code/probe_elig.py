import csv
from pathlib import Path
A10 = Path("../synthetic_2026-11-20/generator_v1_6_repair/results/panel_A10_repaired.csv").resolve()
V13 = Path("../synthetic_2026-11-20/generator_v1_3/results/synthetic_panel_v1_3.csv").resolve()
def grab(path):
    d = {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["country"] != "SYN00_PHL_LIKE": continue
            y = int(float(r["year"]))
            if y < 2010: continue
            d[(r["level"], y)] = (float(r["eligibility_pool"])/float(r["cohort"]),
                                  float(r["demand_share"]), float(r["demand_official"])/float(r["cohort"]))
    return d
a, v = grab(A10), grab(V13)
for lv in ("primary","lower_secondary","upper_secondary"):
    print("==", lv)
    for y in range(2010, 2025):
        ea = a[(lv,y)]; ev = v[(lv,y)]
        print(y, "P0 elig %.4f ds %.4f d/c %.4f | v13 elig %.4f ds %.4f d/c %.4f" % (ea[0],ea[1],ea[2],ev[0],ev[1],ev[2]))
