"""Early-warning signals before fertility transitions, and diminishing returns to schooling.

Pre-registration: research/records/2026-11-23-early-warning/PREREGISTRATION.md (committed first).
"""
import json, os
import numpy as np
D = "/root/work/data"; OUT = "/root/work/early_warning"
os.makedirs(OUT, exist_ok=True)
np.random.seed(20261123)

def series(name):
    d = json.load(open(f"{D}/{name}.json"))
    out = {}
    for iso, y, v in d:
        if v is None: continue
        try: out.setdefault(iso, {})[int(y)] = float(v)
        except Exception: pass
    return out

FERT = series("fertility")
LSC = series("lsc")
META = json.load(open(f"{D}/meta.json"))
REGION = {k: (v.get("region", "") if isinstance(v, dict) else "") for k, v in META.items()} if isinstance(META, dict) else {}

def arr(d):
    ys = sorted(d); return np.array(ys), np.array([d[y] for y in ys], float)

# ---------- event detection (pre-registered rule)
EV = {}
for iso, d in FERT.items():
    if len(d) < 35: continue
    ys, v = arr(d)
    best, bt = 0.0, None
    for i in range(len(ys) - 10):
        if ys[i + 10] - ys[i] != 10: continue
        fall = v[i] - v[i + 10]
        if fall > best + 1e-12 or (abs(fall - best) < 1e-12 and bt is not None and ys[i] < bt):
            best, bt = fall, ys[i]
    if bt is not None and best >= 1.0 and (bt - 19) >= int(ys[0]):   # the pre-event window must be observed
        EV[iso] = dict(event=int(bt), fall=float(best), years=ys)
print("countries with an event (10-year fall >= 1.0):", len(EV), flush=True)

def detrend(x):
    t = np.arange(len(x)); X = np.column_stack([np.ones(len(x)), t])
    b = np.linalg.lstsq(X, x, rcond=None)[0]; return x - X @ b

def ews_slopes(vals, t):
    """vals: series values; t: the years. Window = 15 years ending 5 years before the event."""
    out = {}
    if len(vals) < 15: return None
    r = detrend(vals)
    subs = [r[0:10], r[3:13], r[5:15]]
    var = np.array([np.var(s) for s in subs])
    ac = []
    for s in subs:
        s = s - s.mean()
        den = (s * s).sum()
        ac.append(float((s[:-1] * s[1:]).sum() / den) if den > 0 else np.nan)
    ac = np.array(ac)
    sk = np.array([float(((s - s.mean()) ** 3).mean() / (s.std() ** 3 + 1e-12)) for s in subs])
    idx = np.arange(3)
    out["var_slope"] = float(np.polyfit(idx, var, 1)[0] / (var.mean() + 1e-12))
    out["ac_slope"] = float(np.polyfit(idx, ac, 1)[0]) if np.all(np.isfinite(ac)) else np.nan
    out["skew_slope"] = float(np.polyfit(idx, sk, 1)[0]) if np.all(np.isfinite(sk)) else np.nan
    out["ac_level"] = float(ac.mean()) if np.all(np.isfinite(ac)) else np.nan
    return out

def window_at(iso, ev_year):
    """15 years ending 5 before the event. Internal gaps (the WDI series is not annual everywhere) are
    linearly interpolated; a window needs at least 12 of its 15 years observed."""
    d = FERT[iso]; ys = np.arange(ev_year - 19, ev_year - 4)
    have = [y in d for y in ys]
    if sum(have) < 12: return None
    v = np.array([d.get(y, np.nan) for y in ys], float)
    ok = np.isfinite(v)
    v = np.interp(ys, ys[ok], v[ok])
    return ews_slopes(v, ys)

rows = []
rng = np.random.default_rng(20261123)
for iso, e in EV.items():
    w = window_at(iso, e["event"])
    if w is None: continue
    # pseudo-events within country
    ys = e["years"]; cand = [int(y) for y in ys if abs(int(y) - e["event"]) > 10 and
                             all((y - k) in FERT[iso] for k in range(5, 20))]
    ps = [window_at(iso, y) for y in cand]
    ps = [p for p in ps if p is not None]
    rows.append(dict(iso=iso, event=e["event"], fall=e["fall"], real=w,
                     pseudo={k: (float(np.mean([p[k] for p in ps])) if ps else np.nan) for k in w},
                     n_pseudo=len(ps)))
print("countries with a usable pre-event window:", len(rows), flush=True)

def paired(key):
    d = np.array([r["real"][key] - r["pseudo"][key] for r in rows if np.isfinite(r["real"][key]) and np.isfinite(r["pseudo"][key])])
    if len(d) < 10: return None
    se = d.std(ddof=1) / np.sqrt(len(d))
    return dict(n=int(len(d)), mean=float(d.mean()), se=float(se), t=float(d.mean() / se),
                mde80=float(2.802 * se))   # two-sided 5%, 80% power, one-sample
print("\n=== EARLY WARNING: event minus pseudo-event (paired by country)")
res = {}
for k in ("ac_slope", "var_slope", "skew_slope", "ac_level"):
    r = paired(k); res[k] = r
    print("  %-11s %s" % (k, ("n=%d mean %+.4f se %.4f t %+.2f  MDE(80%%) %.4f" % (r["n"], r["mean"], r["se"], r["t"], r["mde80"])) if r else "insufficient"))

# ---------- placebo countries: no real transition
noT = []
for iso, d in FERT.items():
    if len(d) < 35 or iso in EV: continue
    ys, v = arr(d)
    best = max((v[i] - v[i + 10] for i in range(len(ys) - 10) if ys[i + 10] - ys[i] == 10), default=0.0)
    if best < 0.3:
        yv = int(ys[len(ys) // 2]); w = window_at(iso, yv + 7)
        if w is not None: noT.append(w)
print("\n=== PLACEBO COUNTRIES (10-year fall < 0.3): n =", len(noT))
for k in ("ac_slope", "var_slope"):
    a = np.array([r["real"][k] for r in rows if np.isfinite(r["real"][k])])
    b = np.array([w[k] for w in noT if np.isfinite(w[k])])
    if len(b) > 5:
        se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        print("  %-11s events %+.4f (n=%d) vs no-transition %+.4f (n=%d): diff %+.4f se %.4f" % (
            k, a.mean(), len(a), b.mean(), len(b), a.mean() - b.mean(), se))

# ---------- surrogate null on the event windows
print("\n=== SURROGATE NULL (shuffle first differences, re-integrate): p = share of surrogates at least as extreme")
for k in ("ac_slope", "var_slope"):
    hits, tot = 0, 0
    for r in rows[:200]:
        d = FERT[r["iso"]]; ys = np.arange(r["event"] - 19, r["event"] - 4)
        if not all(y in d for y in ys): continue
        x = np.array([d[y] for y in ys], float); dx = np.diff(x)
        real = r["real"][k]
        if not np.isfinite(real): continue
        cnt = 0
        for _ in range(200):
            s = np.concatenate([[x[0]], x[0] + np.cumsum(rng.permutation(dx))])
            w = ews_slopes(s, ys)
            if w is not None and np.isfinite(w[k]) and w[k] >= real: cnt += 1
        hits += cnt; tot += 200
    if tot: print("  %-11s share of surrogates with slope >= observed: %.3f (n=%d surrogates)" % (k, hits / tot, tot))

# ---------- diminishing returns: 10-year fertility change vs schooling completion
print("\n=== DIMINISHING RETURNS: 10-year fertility change on completion and completion^2 (+ region dummies)")
X, y, reg = [], [], []
for iso, d in FERT.items():
    l = LSC.get(iso)
    if not l: continue
    for yy in sorted(l):
        if yy in d and (yy + 10) in d and 0 <= l[yy] <= 100:
            X.append([1.0, l[yy], l[yy] ** 2]); y.append(d[yy + 10] - d[yy]); reg.append(REGION.get(iso, ""))
X = np.array(X); y = np.array(y); reg = np.array(reg)
ok = np.all(np.isfinite(X), 1) & np.isfinite(y)
cmean = X[ok, 1].mean()
X[:, 1] = X[:, 1] - cmean                      # centre completion: b1 = marginal effect at the mean
X[:, 2] = (X[:, 1]) ** 2
X, y, reg = X[ok], y[ok], reg[ok]
regs = [r for r in sorted(set(reg)) if (reg == r).sum() > 50]
Xd = [X]
for r in regs[1:]: Xd.append((reg == r).astype(float)[:, None])
Xf = np.column_stack(Xd)
inv = np.linalg.pinv(Xf.T @ Xf); b = inv @ Xf.T @ y; e = y - Xf @ b
n, k = Xf.shape
cov = inv @ (Xf.T * e ** 2) @ Xf @ inv * (n / (n - k))
se = np.sqrt(np.maximum(np.diag(cov), 0))
print("  n = %d observations, %d countries" % (n, len([iso for iso in FERT if LSC.get(iso)])))
print("  completion coefficient b1 = %+.4f (t %+.2f) | completion^2 (per 100) b2 = %+.4f (t %+.2f)" % (
    b[1], b[1] / se[1], b[2], b[2] / se[2]))
q = np.quantile(X[:, 1], [.1, .5, .9])
print("  completion centred at %.1f; marginal effect of +1 point at p10/p50/p90:" % cmean)
for qq in q:
    print("    at %+6.1f from mean: %+.4f births" % (qq, b[1] + 2 * b[2] * qq))
tp = -b[1] / (2 * b[2]) if abs(b[2]) > 1e-12 else np.nan
print("  turning point of the quadratic: %+.1f from the mean (inside the data range: %s)" % (
    tp, bool(np.nanmin(X[:, 1]) < tp < np.nanmax(X[:, 1]))))
# bootstrap the marginal effects at the deciles
rngb = np.random.default_rng(7); boots = []
for _ in range(400):
    ii = rngb.integers(0, len(y), len(y))
    bb = np.linalg.pinv(Xf[ii].T @ Xf[ii]) @ Xf[ii].T @ y[ii]
    boots.append([bb[1] + 2 * bb[2] * qq for qq in q])
boots = np.array(boots)
for j, qq in enumerate(q):
    print("    bootstrap 95%% interval at %+6.1f: [%+.4f, %+.4f]" % (qq, np.quantile(boots[:, j], .025), np.quantile(boots[:, j], .975)))
json.dump(dict(n_events=len(rows), ews={k: v for k, v in res.items()},
               placebo_countries=len(noT), dim_returns=dict(n=int(n), b1=float(b[1]), se1=float(se[1]),
                                                             b2=float(b[2]), se2=float(se[2]),
                                                             q=[float(x) for x in q],
                                                             marginal=[float(b[1] + 2 * b[2] * x) for x in q],
                                                             turning_point=float(tp))),
          open(f"{OUT}/ews_results.json", "w"), indent=1)
print("\nwrote", f"{OUT}/ews_results.json")
