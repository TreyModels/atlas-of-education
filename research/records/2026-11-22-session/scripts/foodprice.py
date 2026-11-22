#!/usr/bin/env python3
"""World food prices x farm dependence: when cheap imports arrive, do farms empty
and births fall?

A global price index has no cross-country variation, so year effects would eat it.
The identifying variation is the INTERACTION with how farm-dependent a country was
before the price moved (a shift-share design).
"""
import json, os, gzip, csv, io, urllib.request
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
UA = {"User-Agent": "Mozilla/5.0"}


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


# ---------- food price index ----------
fp = os.path.join(DATA, "ffpi.json")
if not os.path.exists(fp):
    u = "https://www.fao.org/fileadmin/templates/worldfood/Reports_and_docs/Food_price_indices_data.csv"
    raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read().decode("latin-1")
    rows = list(csv.reader(io.StringIO(raw)))
    start = next(i for i, r in enumerate(rows) if r and r[0] == "Date")
    hdr = rows[start]
    mon = {m: k + 1 for k, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
    out = {}
    for r in rows[start + 1:]:
        if not r or "-" not in r[0]:
            continue
        try:
            m, yy = r[0].split("-")
            y = 1900 + int(yy) if int(yy) > 50 else 2000 + int(yy)
            out.setdefault(y, []).append((mon[m], [float(x) for x in r[1:7]]))
        except Exception:
            continue
    annual = {}
    for y, lst in out.items():
        lst.sort()
        arr = np.array([v for _, v in lst])
        annual[y] = arr.mean(0).tolist()
    json.dump({"cols": hdr[1:7], "annual": annual}, open(fp, "w"))
FF = json.load(open(fp))
FF["annual"] = {int(k): v for k, v in FF["annual"].items()}
COLS = FF["cols"]
years = sorted(int(y) for y in FF["annual"])
print(f"food price index: {years[0]}-{years[-1]}, columns {COLS}")

meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG}
     for k in ["fertility", "emp_agri", "agri_va", "urban", "gdppc_log", "wage_emp"]}


def baseline(k, iso, year=1990):
    for d in range(0, 12):
        for y in (year + d, year - d):
            if (iso, y) in S[k]:
                return S[k][(iso, y)]
    return None


def build(outcome, price_col=1, lag_expo=0):
    """price_col: index into the FAO columns (1=overall food, 4=cereals)"""
    rows = []
    for (i, t), v in S[outcome].items():
        if (i, t + 10) not in S[outcome] or t not in FF["annual"] or (t + 10) not in FF["annual"]:
            continue
        expo = baseline("emp_agri", i)
        if expo is None:
            continue
        p0 = FF["annual"][t][price_col]
        p1 = FF["annual"][t + 10][price_col]
        r = [i, t, S[outcome][(i, t + 10)] - v, v, expo, np.log(p1 / p0) if p0 > 0 else None]
        if r[5] is None:
            continue
        ok = True
        for c in ("gdppc_log", "urban"):
            if (i, t) in S[c]:
                r.append(S[c][(i, t)])
            else:
                ok = False
                break
        if ok:
            rows.append(r)
    return rows


def fit(rows, interact=True, extra=True):
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    gy = np.array([(r[1] // 5) * 5 for r in rows])
    y = np.array([r[2] for r in rows])
    own = np.array([r[3] for r in rows])
    expo = np.array([r[4] for r in rows], float)
    dlogp = np.array([r[5] for r in rows], float)
    ez = (expo - expo.mean()) / expo.std()
    dz = (dlogp - dlogp.mean()) / (dlogp.std() + 1e-9)
    cols = [np.ones(len(y)), own, ez * dz]
    names = ["own level", "farm share x price change"]
    if interact:
        cols.append(ez)
        names.append("farm share (level)")
    if extra:
        cols.append(np.array([r[6] for r in rows], float))
        cols.append(np.array([r[7] for r in rows], float))
        names += ["income", "cities"]
    X = np.column_stack(cols)

    def dm(a, g):
        s = np.bincount(g, weights=a); c = np.bincount(g)
        return a - (s / np.maximum(c, 1))[g]
    X = np.column_stack([dm(X[:, j], gi) for j in range(X.shape[1])])
    X = np.column_stack([dm(X[:, j], gy) for j in range(X.shape[1])])
    Y = dm(dm(y, gi), gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    se = np.sqrt(np.maximum(np.diag(Vb), 0))
    return names, b, se, len(rows), len(ui)


for outcome, lab in (("emp_agri", "FARM EMPLOYMENT SHARE"),
                     ("fertility", "BIRTHS PER WOMAN"),
                     ("wage_emp", "PAID EMPLOYMENT SHARE")):
    for pc, pname in ((1, "overall food price"), (4, "cereal price")):
        rows = build(outcome, pc)
        if len(rows) < 150:
            print(f"\n{lab} / {pname}: too few ({len(rows)})")
            continue
        names, b, se, n, nc = fit(rows)
        print("\n" + "=" * 74)
        print(f"{lab}  vs  {pname} x farm dependence   (n={n}, {nc} countries)")
        print("=" * 74)
        for j, nm in enumerate(names):
            if j == 0:
                continue
            print(f"   {nm:32s} {b[j]:+8.4f}  (±{se[j]:.4f}) "
                  f"{'**' if abs(b[j]/se[j])>1.96 else ''}")
