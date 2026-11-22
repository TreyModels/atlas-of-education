"""Is it mass higher education, or mass higher education WITH women equal or ahead?"""
import gzip, json, os
import numpy as np

SRC = "/var/minis/workspace/atlas/research/records/2026-11-22-massification-panel/sources/wdi_sweep"
REG = json.load(open("/var/minis/workspace/wb_regions.json"))
AGG = {"WLD","LMY","MIC","HIC","LMC","UMC","LIC","EAS","EAP","TEA","TEC","ECS","ECA","LCN","LAC","MEA","MNA","SAS","SSF","SSA","ARB","IBT","IBD","EAR","EAR","PRE","EMU","OED","CEB","AFE","AFW","EAP","TLA","TME","TMN","TSA","TSS","EUU","FCS","HPC","INX","LTE","NAC","PST","SST","CSS","LTE"}


def load(n):
    p = os.path.join(SRC, n + ".json.gz")
    if not os.path.exists(p):
        p = os.path.join(SRC, n + ".json")
    op = gzip.open(p) if p.endswith(".gz") else open(p)
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


ter, gpi, tfr = load("ter"), load("gpi_ter"), load("fertility")


def near(v, iso, y, tol=4):
    for d in range(tol + 1):
        for yy in (y - d, y + d):
            if (iso, yy) in v:
                return v[(iso, yy)], yy
    return None, None


def cross(iso, thr=20.0):
    ys = sorted(y for (i, y) in ter if i == iso)
    below = False
    for y in ys:
        v = ter[(iso, y)]
        if v < thr:
            below = True
        elif below and v >= thr:
            return y
    return None


rows = []
for iso in sorted({i for (i, y) in ter}):
    if iso not in REG or iso in AGG or len(iso)!=3:
        continue
    c = cross(iso)
    if c is None or c < 1965:
        continue
    g, _ = near(gpi, iso, c)
    t0, _ = near(tfr, iso, c)
    t20, _ = near(tfr, iso, c + 20, tol=5)
    if g is None or t0 is None or t20 is None:
        continue
    rows.append(dict(iso=iso, reg=REG[iso], c=c, gpi=g, t0=t0, t20=t20, d=t20 - t0))

print(f"{len(rows)} countries usable\n")


def show(name, f):
    g = [r for r in rows if f(r)]
    if not g:
        print(f"{name}: none\n")
        return
    print(f"{name}  (n={len(g)})")
    print(f"   at crossing: {np.mean([r['t0'] for r in g]):.2f} children/woman -> 20y later: {np.mean([r['t20'] for r in g]):.2f}   (change {np.mean([r['d'] for r in g]):+.2f})")
    print("   " + "  ".join(f"{r['iso']} {r['t20']:.1f}" for r in sorted(g, key=lambda r: r["t20"])) + "\n")


show("A. women equal or ahead (GPI >= 1.0)", lambda r: r["gpi"] >= 1.0)
print("--- MATCHED: only countries that started at 2.0-3.2 children ---")
show("A2. women equal/ahead, same start", lambda r: r["gpi"] >= 1.0 and 2.0 <= r["t0"] <= 3.2)
show("B2. women behind, same start", lambda r: r["gpi"] < 0.9 and 2.0 <= r["t0"] <= 3.2)
show("B. women behind (GPI < 0.9)", lambda r: r["gpi"] < 0.9)
show("C. between (0.9 - 1.0)", lambda r: 0.9 <= r["gpi"] < 1.0)
print("--- inside group A, by region ---")
for reg in ["East Asia & Pacific", "Sub-Saharan Africa", "Latin America & Caribbean",
            "Europe & Central Asia", "South Asia", "Middle East & North Africa"]:
    show(reg, lambda r, reg=reg: r["gpi"] >= 1.0 and r["reg"] == reg)
