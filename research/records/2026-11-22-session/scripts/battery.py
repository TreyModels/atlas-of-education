"""Battery: what actually tracks the fall in births?"""
import gzip, json, os
import numpy as np

SRC = "/var/minis/workspace/atlas/research/records/2026-11-22-massification-panel/sources/wdi_sweep"
REG = json.load(open("/var/minis/workspace/wb_regions.json"))
AGG = {"WLD","LMY","MIC","HIC","LMC","UMC","LIC","EAS","EAP","TEA","TEC","ECS","ECA","LCN",
       "LAC","MEA","MNA","SAS","SSF","SSA","ARB","IBT","IBD","EAR","PRE","EMU","OED","CEB",
       "AFE","AFW","TLA","TME","TMN","TSA","TSS","EUU","FCS","HPC","INX","LTE","NAC","PST",
       "SST","CSS"}
CAND = ["ter", "sec", "lsc", "prm_cmp", "gpi_ter", "gpi_sec", "flfp", "wage_emp",
        "emp_ind", "emp_srv", "u5mr", "life_exp", "urban", "gdppc_log", "electricity",
        "lit_adult", "internet", "remit"]
NAME = {"ter": "young people in higher ed", "sec": "secondary completion",
        "lsc": "lower-secondary completion", "prm_cmp": "primary completion",
        "gpi_ter": "women vs men in higher ed", "gpi_sec": "women vs men in secondary",
        "flfp": "women in the labour force", "wage_emp": "share of jobs that are paid",
        "emp_ind": "jobs in industry", "emp_srv": "jobs in services",
        "u5mr": "children dying before 5", "life_exp": "life expectancy",
        "urban": "share living in cities", "gdppc_log": "income per person",
        "electricity": "homes with electricity", "lit_adult": "adult literacy",
        "internet": "internet use", "remit": "money sent home from abroad"}


def load(n):
    p = os.path.join(SRC, n + ".json.gz")
    if not os.path.exists(p):
        p = os.path.join(SRC, n + ".json")
    op = gzip.open(p) if p.endswith(".gz") else open(p)
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


V = {k: load(k) for k in CAND + ["fertility"]}
F = V["fertility"]
real = {i for i in REG if i not in AGG and len(i) == 3}
for k in V:
    V[k] = {kk: vv for kk, vv in V[k].items() if kk[0] in real}


def rows_for(cand):
    out = []
    for (i, t), v in F.items():
        if (i, t + 10) not in F or (i, t) not in V[cand]:
            continue
        out.append((i, t, F[(i, t + 10)] - v, V[cand][(i, t)], v))
    return out


def corr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.std() == 0 or b.std() == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def demean(vals, groups):
    d = {}
    for v, g in zip(vals, groups):
        d.setdefault(g, []).append(v)
    m = {g: np.mean(x) for g, x in d.items()}
    return [v - m[g] for v, g in zip(vals, groups)]


print("=" * 76)
print("TEST 1  What moves with the fall in births?")
print("        between = comparing countries | within = a country against itself")
print("=" * 76)
res = []
for c in CAND:
    r = rows_for(c)
    if len(r) < 300:
        continue
    y = [x[2] for x in r]; x = [x[3] for x in r]
    iso = [x[0] for x in r]; yr = [x[1] for x in r]
    btw = corr(x, y)
    xw = demean(x, iso); yw = demean(y, iso)
    xw = demean(xw, yr); yw = demean(yw, yr)
    res.append((c, btw, corr(xw, yw), len(r)))
for c, b, w, n in sorted(res, key=lambda z: -abs(z[2])):
    print(f"  {NAME[c]:32s} between {b:+.2f}  within {w:+.2f}  (n={n})")

print()
print("=" * 76)
print("TEST 2  All at once, each country against itself")
print("=" * 76)
keys = [c for c, _, _, _ in res]
base = rows_for("ter")
keep = [r for r in base if all((r[0], r[1]) in V[c] for c in keys)]
print(f"  {len(keep)} observations, {len({r[0] for r in keep})} countries")
if len(keep) > 200:
    y = np.array([r[2] for r in keep])
    isos = sorted({r[0] for r in keep}); II = {c: i for i, c in enumerate(isos[1:])}
    years = sorted({r[1] for r in keep})
    cols = [np.ones(len(keep)), np.array([r[4] for r in keep])]
    cols += [np.array([1.0 if r[0] == c else 0.0 for r in keep]) for c in isos[1:]]
    cols += [np.array([1.0 if r[1] == yy else 0.0 for r in keep]) for yy in years[1:]]
    for c in keys:
        v = np.array([V[c][(r[0], r[1])] for r in keep])
        cols.append((v - v.mean()) / (v.std() if v.std() > 0 else 1))
    X = np.column_stack(cols)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    u = y - X @ b
    XtX = X.T @ X
    g = np.array([II.get(r[0], 0) for r in keep])
    meat = np.zeros_like(XtX)
    for cc in set(g.tolist()):
        m = (g == cc); s = X[m].T @ u[m]; meat += np.outer(s, s)
    se = np.sqrt(np.maximum(np.diag(np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)), 0))
    off = X.shape[1] - len(keys)
    out = {c: (b[off + j], se[off + j]) for j, c in enumerate(keys)}
    for c, (bb, ss) in sorted(out.items(), key=lambda z: z[1][0]):
        s = "STRONG" if abs(bb) > 2 * ss else ("some" if abs(bb) > ss else "-")
        print(f"  {NAME[c]:32s} {bb:+6.2f}  (+/-{ss:.2f})  {s}")

print()
print("=" * 76)
print("TEST 3  Which comes first?")
print("=" * 76)
for c in ["ter", "sec", "gpi_ter", "flfp", "wage_emp", "gdppc_log", "u5mr", "electricity"]:
    lead, follow = [], []
    for (i, t), v in F.items():
        if (i, t + 10) not in F or (i, t) not in V[c] or (i, t + 10) not in V[c]:
            continue
        lead.append((V[c][(i, t)], F[(i, t + 10)] - v))
        follow.append((v, V[c][(i, t + 10)] - V[c][(i, t)]))
    if len(lead) < 200:
        continue
    print(f"  {NAME[c]:32s} leads {corr([a for a, _ in lead], [x for _, x in lead]):+.2f}"
          f"   follows {corr([a for a, _ in follow], [x for _, x in follow]):+.2f}")
