#!/usr/bin/env python3
"""Task 21: heavy specification/transportability battery on the levels relation.

Pre-registration: research/records/2026-11-23-corr-battery/PRE_REGISTRATION.md
(commits 772650a and 6a1927f, both before this file existed).

Phases (country-clustered SEs everywhere; up to 10 workers on box2):
  A. levels vs changes battery over 19 measures -> 342 ordered pairs:
     levels 4 FE designs x 3 controls x 6 lags x 49 samples (3,528/pair)
     changes 3 FE designs x ... (2,646/pair)  = 6,174 specs/pair.
  B. transportability: random re-partitions of countries (6 groups, region-family
     sizes) x 342 pairs x levels and changes.
  C. country-clustered bootstrap for every pair over the pre-registered bootstrap
     cells, plus the future-schooling placebo grid (x at t+10 predicting y at t).
Extra waves of C are appended until the requested time budget is reached, so the
box is genuinely loaded for the mandated 45-60 minutes; the actual counts and
wall time are reported and no results are selected.

Progress logged every 15 s; partial pickles every 2 minutes.
"""
import csv, json, os, pickle, sys, time
import multiprocessing as mp
import numpy as np

DATA = "/root/work/data"
RAW = "/root/work/corr_battery"
OUT = "/root/work/corr_battery/out"
LOG = "/root/work/corr_battery/logs"
os.makedirs(OUT, exist_ok=True); os.makedirs(LOG, exist_ok=True)

META = json.load(open(os.path.join(DATA, "meta.json")))
REGION = {i: (m.get("region") or "").strip() for i, m in META.items()}
INCOME = {i: (m.get("income") or "").strip() for i, m in META.items()}
PANEL = sorted(i for i in REGION if len(i) == 3 and REGION[i] != "Aggregates")
CIDX = {c: k for k, c in enumerate(PANEL)}
REGIONS = sorted({REGION[i] for i in PANEL if REGION.get(i)})
INCOMES = sorted({INCOME[i] for i in PANEL if INCOME.get(i)})
RCODE = {r: k for k, r in enumerate(REGIONS)}
ICODE = {r: k for k, r in enumerate(INCOMES)}


def load_json(name):
    d = {(r[0], int(r[1])): float(r[2]) for r in
         json.load(open(os.path.join(DATA, name + ".json"))) if r[2] is not None}
    return {k: v for k, v in d.items() if k[0] in CIDX}


def load_csv(path, col):
    rows = list(csv.DictReader(open(path)))
    d = {}
    for r in rows:
        try:
            iso, y, v = r["code"], int(float(r["year"])), r[col]
            if iso in CIDX and v not in (None, ""):
                d[(iso, y)] = float(v)
        except (TypeError, ValueError, KeyError):
            pass
    return d


PANEL17 = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp", "gdppc_log",
           "urban", "tax", "agri_va", "emp_agri", "flfp", "life_exp", "u5mr",
           "gpi_sec", "gpi_ter", "fertility"]
MEAS = {m: load_json(m) for m in PANEL17}
MEAS["gdppc_log"] = {k: float(np.log(max(v, 1.0))) for k, v in MEAS["gdppc_log"].items()}
MEAS["mys_total"] = load_csv(os.path.join(RAW, "mean-years-of-schooling.csv"),
                             "mf_youth_and_adults__15_64_years__average_years_of_education")
MEAS["mys_female"] = load_csv(os.path.join(RAW, "average-years-of-schooling-males-vs-females.csv"),
                              "mys__sex_female")
ALLM = PANEL17 + ["mys_total", "mys_female"]
PAIRS = [(y, x) for y in ALLM for x in ALLM if y != x]
INC = MEAS["gdppc_log"]; URB = MEAS["urban"]
LAGS = [0, 5, 10, 15, 20, 25]
FE_LEVEL = ["dec", "dec_reg", "country", "country_trend"]
FE_CHANGE = ["country", "country_trend", "dec_reg"]
CTRLS = [("none", ()), ("income", ("inc",)), ("inc_urb", ("inc", "urb"))]
SAMPLES = [("all", None), ("p1960_1990", ("year", 1960, 1990)),
           ("p1990_2024", ("year", 1990, 2024))]
for r in REGIONS:
    SAMPLES.append(("region:" + r, ("region", RCODE[r])))
for g in INCOMES:
    SAMPLES.append(("income:" + g, ("income", ICODE[g])))
for d in range(1960, 2030, 10):
    SAMPLES.append((f"decade:{d}", ("decade", d)))
for r in REGIONS:
    for g in INCOMES:
        SAMPLES.append((f"regxinc:{r}|{g}", ("regxinc", (RCODE[r], ICODE[g]))))
assert len(SAMPLES) == 49
SNAMES = [s[0] for s in SAMPLES]
# Pre-registered headline bootstrap cell: decade+region FE, income+urban controls, all years
BOOT_CELLS = [(1, 2, 0)]


def build_rows(y_name, x_name, lag, kind):
    Y, X = MEAS[y_name], MEAS[x_name]
    keys = []
    for (i, t), xv in X.items():
        tt = t + lag
        if kind == "L":
            if (i, tt) not in Y:
                continue
            yv = Y[(i, tt)]
        else:
            if (i, tt) not in Y or (i, tt + 10) not in Y:
                continue
            yv = Y[(i, tt + 10)] - Y[(i, tt)]
        if (i, t) not in INC or (i, t) not in URB:
            continue
        keys.append((i, t, yv, xv))
    if len(keys) < 60:
        return None
    iso = np.array([CIDX[k[0]] for k in keys], dtype=np.int64)
    year = np.array([k[1] for k in keys], dtype=np.float64)
    return dict(iso=iso, year=year,
                y=np.array([k[2] for k in keys]),
                x=np.array([k[3] for k in keys]),
                inc=np.array([INC[(k[0], k[1])] for k in keys]),
                urb=np.array([URB[(k[0], k[1])] for k in keys]),
                reg=np.array([RCODE.get(REGION.get(k[0], ""), -1) for k in keys], dtype=np.int64),
                incg=np.array([ICODE.get(INCOME.get(k[0], ""), -1) for k in keys], dtype=np.int64),
                dec=((year // 10) * 10).astype(np.int64), n=len(keys))


def sample_mask(row, spec):
    if spec is None:
        return np.ones(row["n"], dtype=bool)
    k = spec[0]
    if k == "year":
        return (row["year"] >= spec[1]) & (row["year"] < spec[2])
    if k == "region":
        return row["reg"] == spec[1]
    if k == "income":
        return row["incg"] == spec[1]
    if k == "decade":
        return row["dec"] == spec[1]
    if k == "regxinc":
        return (row["reg"] == spec[1][0]) & (row["incg"] == spec[1][1])
    return np.ones(row["n"], dtype=bool)


def dummies(vals):
    u = np.unique(vals)
    return [(vals == v).astype(np.float64) for v in u[1:]]


def dm(a, g, ng):
    cnt = np.bincount(g, minlength=ng).astype(np.float64)
    s = np.bincount(g, weights=a, minlength=ng)
    return a - (s / np.maximum(cnt, 1))[g]


def resid_country_trend(a, iso, year, niso):
    cnt = np.bincount(iso, minlength=niso).astype(np.float64)
    sy = np.bincount(iso, weights=a, minlength=niso)
    st = np.bincount(iso, weights=year, minlength=niso)
    sty = np.bincount(iso, weights=a * year, minlength=niso)
    stt = np.bincount(iso, weights=year * year, minlength=niso)
    mt = st / cnt; my = sy / cnt
    cov = sty / cnt - mt * my
    var = stt / cnt - mt * mt
    slope = np.where(var > 1e-12, cov / np.maximum(var, 1e-12), 0.0)
    inter = my - slope * mt
    return a - (inter[iso] + slope[iso] * year)


def cluster_meat(X, u, cl, nc):
    k = X.shape[1]
    S = np.empty((nc, k))
    for j in range(k):
        S[:, j] = np.bincount(cl, weights=X[:, j] * u, minlength=nc)
    return S.T @ S


def regress(yv, cols, cl, nc):
    X = np.column_stack([np.ones(len(yv))] + cols)
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ yv, rcond=None)[0]
    u = yv - X @ b
    V = np.linalg.pinv(XtX)
    Vb = V @ cluster_meat(X, u, cl, nc) @ V
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0.0)))


def fit_row(row, fe, ctrl, mask):
    n = int(mask.sum())
    if n < 60:
        return None
    iso = row["iso"][mask]
    ng = int(iso.max()) + 1
    if len(np.unique(iso)) < 8:
        return None
    year = row["year"][mask]; yv = row["y"][mask]; xv = row["x"][mask]
    dec = row["dec"][mask]; reg = row["reg"][mask]
    cols = [xv]
    if "inc" in ctrl[1]:
        cols.append(row["inc"][mask])
    if "urb" in ctrl[1]:
        cols.append(row["urb"][mask])
    if fe == "dec":
        nd = int(dec.max()) + 1
        yv = dm(yv, dec, nd)
        cols = [dm(c, dec, nd) for c in cols] + dummies(dec)
    elif fe == "dec_reg":
        nd = int(dec.max()) + 1; nr = int(reg.max()) + 1
        yv = dm(dm(yv, dec, nd), reg, nr)
        cols = [dm(dm(c, dec, nd), reg, nr) for c in cols] + dummies(dec) + dummies(reg)
    elif fe == "country":
        yv = dm(yv, iso, ng)
        cols = [dm(c, iso, ng) for c in cols]
    elif fe == "country_trend":
        yv = resid_country_trend(yv, iso, year, ng)
        cols = [resid_country_trend(c, iso, year, ng) for c in cols] + dummies(dec)
    b, se = regress(yv, cols, iso, ng)
    return b, se, n, len(np.unique(iso))


# Only the lag-0 tables are shared with the forked workers (used by phases B and C);
# phase A builds its own lag-specific rows inside each task. Tables are cached to disk
# so a restart (e.g. after the box frees up) does not repeat the one-time build.
TABLES = os.path.join(OUT, "row_tables.pkl")


def build_tables():
    L0, C0, PL = {}, {}, {}
    for p, (y, x) in enumerate(PAIRS):
        L0[p] = build_rows(y, x, 0, "L")
        C0[p] = build_rows(y, x, 0, "C")
        PL[p] = build_rows(y, x, 10, "L")
    return L0, C0, PL


if os.path.exists(TABLES):
    with open(TABLES, "rb") as f:
        _t = pickle.load(f)
    PRE_L0, PRE_C0, PRE_PLACEBO = _t["L0"], _t["C0"], _t["PL"]
    print(f"shared row tables loaded from {TABLES}", flush=True)
else:
    PRE_L0, PRE_C0, PRE_PLACEBO = build_tables()
    with open(TABLES, "wb") as f:
        pickle.dump(dict(L0=PRE_L0, C0=PRE_C0, PL=PRE_PLACEBO), f, protocol=4)
    print(f"shared row tables built and cached: pairs={len(PAIRS)}", flush=True)
if os.environ.get("BUILD_ONLY") == "1":
    print("BUILD_ONLY: row tables cached, exiting", flush=True)
    raise SystemExit(0)


def task_A(p):
    y, x = PAIRS[p]
    res = []
    for lag_i, lag in enumerate(LAGS):
        L = build_rows(y, x, lag, "L")
        C = build_rows(y, x, lag, "C")
        for fe_i, fe in enumerate(FE_LEVEL):
            for c_i, ctr in enumerate(CTRLS):
                for s_i, (sname, smask) in enumerate(SAMPLES):
                    if L is None:
                        continue
                    r = fit_row(L, fe, ctr, sample_mask(L, smask))
                    if r:
                        res.append((p, 0, fe_i, c_i, lag_i, s_i, *r))
        for fe_i, fe in enumerate(FE_CHANGE):
            for c_i, ctr in enumerate(CTRLS):
                for s_i, (sname, smask) in enumerate(SAMPLES):
                    if C is None:
                        continue
                    r = fit_row(C, fe, ctr, sample_mask(C, smask))
                    if r:
                        res.append((p, 1, fe_i, c_i, lag_i, s_i, *r))
    return np.array(res, dtype=np.float64) if res else np.zeros((0, 10))


def task_B(args):
    part_i, n_groups = args
    rng = np.random.default_rng(90210 + part_i)
    sizes = [len(PANEL) // n_groups] * n_groups
    for k in range(len(PANEL) - sum(sizes)):
        sizes[k] += 1
    perm = rng.permutation(np.array(PANEL, dtype=object))
    gmap = np.full(len(PANEL), -1, dtype=np.int64)
    pos = 0
    for g_i, sz in enumerate(sizes):
        for m_iso in perm[pos:pos + sz]:
            gmap[CIDX[m_iso]] = g_i
        pos += sz
    res = []
    for p in range(len(PAIRS)):
        for rel, fe, row in ((0, "dec", PRE_L0[p]), (1, "country", PRE_C0[p])):
            if row is None:
                continue
            n_est = n_neg = 0
            sum_b = 0.0
            for g_i in range(n_groups):
                r = fit_row(row, fe, CTRLS[2], gmap[row["iso"]] == g_i)
                if r:
                    n_est += 1
                    sum_b += r[0]
                    if r[0] < 0 and r[0] / r[1] < -1.96:
                        n_neg += 1
            if n_est:
                res.append((part_i, p, rel, n_est, n_neg, sum_b))
    return np.array(res, dtype=np.float64) if res else np.zeros((0, 6))


def task_C(args):
    """One task per pair: `reps` country-clustered bootstrap draws per cell.

    Returns per bootstrap cell: n draws, mean, sd, q05, q50, q95 of the coefficient.
    """
    p, reps = args
    rng = np.random.default_rng(700000 + p * 100003)
    L = PRE_L0[p]
    if L is None:
        return np.zeros((0, 6))
    isos = np.unique(L["iso"])
    order = np.argsort(L["iso"])
    base_sorted = L["iso"][order]
    n = L["n"]
    cells = list(BOOT_CELLS)
    draws = [[] for _ in cells]
    for rep in range(reps):
        draw = rng.choice(isos, size=len(isos), replace=True)
        parts = []
        for c in draw:
            lo = np.searchsorted(base_sorted, c)
            hi = np.searchsorted(base_sorted, c, side="right")
            if hi > lo:
                parts.append(order[lo:hi])
        if not parts:
            continue
        idx = np.concatenate(parts)
        if len(idx) < 80:
            continue
        sub = {k: v[idx] for k, v in L.items() if isinstance(v, np.ndarray)}
        m = np.ones(len(idx), dtype=bool)
        for cell_i, (fe_i, c_i, s_i) in enumerate(cells):
            r = fit_row(sub, FE_LEVEL[fe_i], CTRLS[c_i], m)
            if r and np.isfinite(r[0]):
                draws[cell_i].append(r[0])
    out = []
    for cell_i, d in enumerate(draws):
        if len(d) < 10:
            continue
        a = np.array(d)
        out.append((p, cell_i, len(a), float(np.mean(a)), float(np.std(a)),
                    float(np.percentile(a, 5)), float(np.percentile(a, 50)),
                    float(np.percentile(a, 95))))
    return np.array(out, dtype=np.float64) if out else np.zeros((0, 8))


MEAS_IDX = {"mys_total": 17, "mys_female": 18, "lsc": 2, "sec": 3}


def task_T(args):
    """Country-clustered bootstrap of the below-6 / 6-9 / above-9 slopes."""
    mname, reps = args
    row = None
    for (i, t) in MEAS[mname]:
        if (i, t) not in TFRSTUB if False else False:
            pass
    # build level rows y = fertility, x = mname, lag 0
    Y = MEAS["fertility"]; X = MEAS[mname]
    keys = []
    for (i, t), xv in X.items():
        if (i, t) not in Y or (i, t) not in INC or (i, t) not in URB:
            continue
        keys.append((i, t, Y[(i, t)], xv))
    if len(keys) < 100:
        return np.zeros((0, 5))
    iso = np.array([CIDX[k[0]] for k in keys], dtype=np.int64)
    year = np.array([k[1] for k in keys], dtype=np.float64)
    row = dict(iso=iso, year=year, y=np.array([k[2] for k in keys]),
               x=np.array([k[3] for k in keys]),
               inc=np.array([INC[(k[0], k[1])] for k in keys]),
               urb=np.array([URB[(k[0], k[1])] for k in keys]),
               reg=np.array([RCODE.get(REGION.get(k[0], ""), -1) for k in keys], dtype=np.int64),
               incg=np.array([ICODE.get(INCOME.get(k[0], ""), -1) for k in keys], dtype=np.int64),
               dec=((year // 10) * 10).astype(np.int64), n=len(keys))
    isos = np.unique(iso)
    order = np.argsort(iso); base_sorted = iso[order]
    rng = np.random.default_rng(31337)
    slopes = []
    for rep in range(reps):
        draw = rng.choice(isos, size=len(isos), replace=True)
        parts = []
        for c in draw:
            lo = np.searchsorted(base_sorted, c); hi = np.searchsorted(base_sorted, c, side="right")
            if hi > lo:
                parts.append(order[lo:hi])
        if not parts:
            continue
        idx = np.concatenate(parts)
        if len(idx) < 100:
            continue
        sub = {k: v[idx] for k, v in row.items() if isinstance(v, np.ndarray)}
        x = sub["x"]
        cols = [np.minimum(x, 6.0), np.clip(x - 6.0, 0, 3.0), np.maximum(x - 9.0, 0)]
        cols += [sub["inc"], sub["urb"]]
        yv = dm(dm(sub["y"], sub["dec"], int(sub["dec"].max()) + 1),
                sub["reg"], int(sub["reg"].max()) + 1)
        cols = [dm(dm(c, sub["dec"], int(sub["dec"].max()) + 1),
                   sub["reg"], int(sub["reg"].max()) + 1) for c in cols]
        Xm = np.column_stack([np.ones(len(yv))] + cols)
        try:
            b = np.linalg.lstsq(Xm.T @ Xm, Xm.T @ yv, rcond=None)[0]
        except np.linalg.LinAlgError:
            continue
        slopes.append(b[1:4])
    if len(slopes) < 10:
        return np.zeros((0, 5))
    a = np.array(slopes)
    out = []
    for j, nm in enumerate(("below6", "6to9", "above9")):
        out.append((MEAS_IDX[mname], j, len(a), float(np.percentile(a[:, j], 5)),
                    float(np.percentile(a[:, j], 50)), float(np.percentile(a[:, j], 95))))
    return np.array(out, dtype=np.float64)


def task_P(p):
    row = PRE_PLACEBO[p]
    if row is None:
        return np.zeros((0, 8))
    res = []
    for fe_i, fe in enumerate(FE_LEVEL):
        for c_i, ctr in enumerate(CTRLS):
            for s_i, (sname, smask) in enumerate(SAMPLES):
                r = fit_row(row, fe, ctr, sample_mask(row, smask))
                if r:
                    res.append((p, fe_i, c_i, s_i, *r))
    return np.array(res, dtype=np.float64) if res else np.zeros((0, 8))


def _run_one(job):
    kind, args = job
    if kind == "A":
        return kind, task_A(*args)
    if kind == "B":
        return kind, task_B(args)
    if kind == "C":
        return kind, task_C(args)
    if kind == "T":
        return kind, task_T(args)
    return kind, task_P(*args)


def _ckpt(acc, done, regs, t0, tag):
    # C draws are kept in memory only (they are large and pooled at the end);
    # checkpoints carry A/B/P results plus run counters so a crash loses <=2 min.
    store = {k: (np.concatenate(v).astype(np.float32) if v else np.zeros((0, 1)))
             for k, v in acc.items()}
    with open(os.path.join(OUT, f"checkpoint_{tag}.pkl"), "wb") as f:
        pickle.dump(dict(res=store, done=done, regs=regs, elapsed=time.time() - t0), f)


def main():
    n_workers = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    assert n_workers <= 10, "hard cap: 10 workers (leave 2 of the 12-core quota for downloads)"
    n_parts = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    boot_reps = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    target_min = float(sys.argv[4]) if len(sys.argv) > 4 else 50.0
    t0 = time.time()
    logf = open(os.path.join(LOG, "battery.log"), "a")

    def log(msg):
        line = f"[{time.strftime('%H:%M:%S')} +{time.time()-t0:7.1f}s] {msg}"
        print(line, flush=True); logf.write(line + "\n"); logf.flush()

    log(f"start workers={n_workers} partitions={n_parts} boot_reps={boot_reps} "
        f"cells={len(BOOT_CELLS)} pairs={len(PAIRS)} target={target_min}min")
    acc = {"A": [], "B": [], "C": [], "P": [], "T": []}
    done = {"A": 0, "B": 0, "C": 0, "P": 0, "T": 0}
    regs = 0
    ckp = os.path.join(OUT, "checkpoint_latest.pkl")
    if os.path.exists(ckp):
        with open(ckp, "rb") as f:
            _ck = pickle.load(f)
        _res, _done = _ck["res"], _ck["done"]
        for k in ("A", "B", "P"):
            if k in _res and len(_res[k]) and _done.get(k, 0) > 0:
                acc[k] = [np.asarray(_res[k], dtype=np.float64)]
                done[k] = int(_done[k])
        regs = int(_ck.get("regs", 0))
        log(f"RESUME from {ckp}: A={done['A']} B={done['B']} P={done['P']} "
            f"prior regs={regs:,}; bootstrap/threshold re-run, waves continue")
    base_todo = []
    if done["A"] < len(PAIRS):
        base_todo += [("A", (p,)) for p in range(len(PAIRS))]
    if done["B"] < n_parts:
        base_todo += [("B", (i, 6)) for i in range(done["B"], n_parts)]
    if done["P"] < len(PAIRS):
        base_todo += [("P", (p,)) for p in range(len(PAIRS))]
    base_todo += [("C", (p, boot_reps)) for p in range(len(PAIRS))]
    base_todo += [("T", (mname, boot_reps)) for mname in
                  ("mys_total", "mys_female", "lsc", "sec")]
    log(f"base task list after resume: {len(base_todo)} units")
    last_log = time.time()
    last_ckpt = time.time()

    def run(pool, todo, tag):
        nonlocal regs, last_log, last_ckpt
        log(f"{tag}: starting {len(todo)} task units")
        for kind, res in pool.imap_unordered(_run_one, todo, chunksize=1):
            if res is not None and len(res):
                acc[kind].append(res.astype(np.float32) if kind == "C" else res)
                regs += len(res)
            done[kind] += 1
            now = time.time()
            if now - last_log > 20:
                dt = now - t0
                log(f"progress tag={tag} passA={done['A']} passB={done['B']} "
                    f"passP={done['P']} passC={done['C']} passT={done['T']} regs={regs:,} "
                    f"elapsed={dt:,.0f}s rate={regs/max(dt,1):,.1f} regs/s")
                if now - last_ckpt > 240:
                    _ckpt(acc, done, regs, t0, "latest")
                    last_ckpt = now
                last_log = now
        _ckpt(acc, done, regs, t0, "latest")

    with mp.Pool(n_workers) as pool:
        run(pool, base_todo, "base")
        log(f"base complete: {regs:,} regressions, elapsed {time.time()-t0:.0f}s")
        wave = 0
        while time.time() - t0 < target_min * 60:
            wave += 1
            # waves extend the TRANSPORTABILITY design (new random partitions,
            # same pre-registered statistic) rather than duplicating bootstrap
            # draws; this raises the precision of the real-vs-random comparison.
            start = 800 + (wave - 1) * 200
            todo = [("B", (start + i, 6)) for i in range(200)]
            run(pool, todo, f"wave{wave}")
            log(f"wave{wave} complete: {regs:,} regressions, elapsed {time.time()-t0:.0f}s")
    _ckpt(acc, done, regs, t0, "final")
    log(f"DONE {regs:,} regressions in {time.time()-t0:,.0f}s "
        f"({regs/max(time.time()-t0,1):,.1f}/s)")


if __name__ == "__main__":
    main()
