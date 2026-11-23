"""Pre-registered tests for the care-work loop and credential inflation (see PREREGISTRATION.md)."""
import csv, json, os
import numpy as np
OUT = "/root/work/care_cred"

def load(path):
    return list(csv.DictReader(open(path)))
def num(x):
    try:
        v = float(x)
        return v if np.isfinite(v) else np.nan
    except Exception:
        return np.nan

def ols(y, X, names):
    """OLS with HC1 robust standard errors, returns dict."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    ok = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    y, X = y[ok], X[ok]
    n, k = X.shape
    if n <= k + 2: return None
    XtX = X.T @ X
    try: inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError: inv = np.linalg.pinv(XtX)
    b = inv @ X.T @ y
    e = y - X @ b
    s2 = (e @ e) / (n - k)
    cov = s2 * inv
    # HC1
    S = X.T * e ** 2 @ X * (n / (n - k))
    covh = inv @ (X.T * e ** 2) @ X @ inv * (n / (n - k))
    seh = np.sqrt(np.maximum(np.diag(covh), 0))
    r2 = 1 - (e @ e) / max(((y - y.mean()) ** 2).sum(), 1e-12)
    return dict(n=int(n), b=[float(x) for x in b], se=[float(x) for x in seh],
                t=[float(b[i] / seh[i]) if seh[i] > 0 else np.nan for i in range(k)],
                r2=float(r2), names=names)

def z(v):
    v = np.asarray(v, float)
    s = np.nanstd(v)
    return (v - np.nanmean(v)) / (s if s > 0 else 1.0)

def design(*cols, const=True):
    cols = list(cols)
    X = np.column_stack(cols) if cols else np.zeros((len(cols[0]), 0))
    if const: X = np.column_stack([np.ones(X.shape[0]), X])
    return X

res = {}
cs = load(f"{OUT}/panel_cross_section.csv")
allr = load(f"{OUT}/panel_all.csv")
def get(r, k): return num(r.get(k, ""))
print("cross-section n =", len(cs), flush=True)
for r in cs:
    r["log_gdp"] = np.log(max(get(r, "gdp_pc"), 1.0)) if np.isfinite(get(r, "gdp_pc")) else np.nan
    r["gap"] = get(r, "edu_ter_f") - get(r, "isco12_f") if np.isfinite(get(r, "isco12_f")) else np.nan
S = dict(
    tfr=[get(r, "tfr") for r in cs], upsec=[get(r, "edu_upsec_f") for r in cs],
    ter=[get(r, "edu_ter_f") for r in cs], care=[get(r, "care_f") for r in cs],
    carem=[get(r, "care_m") for r in cs], manuf=[get(r, "manuf_f") for r in cs],
    isco=[get(r, "isco12_f") for r in cs], gap=[get(r, "gap") for r in cs],
    lgdpg=[get(r, "log_gdp") for r in cs], urb=[get(r, "urban") for r in cs])
S = {k: np.asarray(v, float) for k, v in S.items()}
n_countries = int(np.isfinite(S["care"]).sum() + np.isfinite(S["isco"]).sum())  # for the availability table

# ---------- A1: care share rises with attainment
for lab, att in (("upper secondary", "upsec"), ("tertiary", "ter")):
    a1 = ols(z(S["care"]), design(z(S[att]), z(S["lgdpg"])), ["attainment", "log gdp"])
    res[f"A1_care_vs_{att}"] = a1
    a1b = ols(z(S["care"]), design(z(S[att]), z(S["lgdpg"]), z(S["urb"])), ["attainment", "log gdp", "urban"])
    res[f"A1_care_vs_{att}_with_urban"] = a1b

# ---------- A3: attainment x care interaction on fertility
for lab, att in (("upper secondary", "upsec"), ("tertiary", "ter")):
    A = z(S[att]); C = z(S["care"]); inter = A * C
    res[f"A3_tfr_{att}_interaction"] = ols(z(S["tfr"]), design(A, C, inter), ["attainment", "care", "attainment x care"])
    res[f"A3_tfr_{att}_interaction_controls"] = ols(z(S["tfr"]), design(A, C, inter, z(S["lgdpg"]), z(S["urb"])),
                                                    ["attainment", "care", "interaction", "log gdp", "urban"])
    # placebos: male care, manufacturing
    AM = z(S[att]); CM = z(S["carem"]); res[f"A3_placebo_male_{att}"] = ols(
        z(S["tfr"]), design(AM, CM, AM * CM, z(S["lgdpg"])), ["attainment", "male care", "male care interaction", "log gdp"])
    MU = z(S["manuf"]); res[f"A3_placebo_manuf_{att}"] = ols(
        z(S["tfr"]), design(AM, MU, AM * MU, z(S["lgdpg"])), ["attainment", "manufacturing", "manufacturing interaction", "log gdp"])

# ---------- B1: horse race, attainment vs credential-occupation gap
G = z(S["gap"]); T = z(S["ter"])
res["B1_attainment_only"] = ols(z(S["tfr"]), design(T), ["tertiary attainment"])
res["B1_gap_only"] = ols(z(S["tfr"]), design(G), ["credential-occupation gap"])
res["B1_horse_race"] = ols(z(S["tfr"]), design(T, G), ["tertiary attainment", "credential-occupation gap"])
res["B1_horse_race_controls"] = ols(z(S["tfr"]), design(T, G, z(S["lgdpg"]), z(S["urb"])),
                                    ["tertiary attainment", "gap", "log gdp", "urban"])
# ---------- B2: saturation split
att = S["ter"]; finite = np.isfinite(att) & np.isfinite(S["gap"]) & np.isfinite(S["tfr"])
if finite.sum() >= 12:
    med = np.nanmedian(att[finite])
    for lab, m in (("high_attainment", finite & (att >= med)), ("low_attainment", finite & (att < med))):
        idx = np.where(m)[0]
        sub = dict((k, np.array(v)[idx]) for k, v in S.items())
        res[f"B2_{lab}_gap"] = ols(z(sub["tfr"]), design(z(sub["gap"])), ["gap"])
        res[f"B2_{lab}_att"] = ols(z(sub["tfr"]), design(z(sub["ter"])), ["tertiary attainment"])
        res[f"B2_{lab}_both"] = ols(z(sub["tfr"]), design(z(sub["ter"]), z(sub["gap"])), ["tertiary", "gap"])

# ---------- A2: change, more care share -> bigger fertility fall
by = {}
for r in allr:
    by.setdefault(r["iso"], []).append(r)
pairs = []
for iso, rs in by.items():
    rs = sorted(rs, key=lambda r: int(r["year"]))
    if len(rs) >= 2:
        y0, y1 = rs[0], rs[-1]
        if np.isfinite(get(y0, "care_f")) and np.isfinite(get(y0, "tfr")) and np.isfinite(get(y1, "tfr")):
            pairs.append(dict(iso=iso, care0=get(y0, "care_f"), dtfr=get(y1, "tfr") - get(y0, "tfr"),
                              y0=int(y0["year"]), y1=int(y1["year"]), tfr1=get(y1, "tfr")))
print("change pairs:", len(pairs), flush=True)
if len(pairs) >= 10:
    res["A2_change"] = ols(z([p["dtfr"] for p in pairs]), design(z([p["care0"] for p in pairs])),
                           ["care share (early)"])
    res["A2_change_lvl1"] = ols(z([p["dtfr"] for p in pairs]),
                                design(z([p["care0"] for p in pairs]), z([p["tfr1"] for p in pairs])),
                                ["care share (early)", "fertility (late)"])
# ---------- specification curve (pre-registered): all combinations, reported in full
def panel_design(dat, ykey, xkeys, fe, controls):
    rows = [r for r in dat if np.isfinite(num(r.get(ykey, "")))]
    y = np.array([num(r[ykey]) for r in allr], float)
    cols = [np.array([num(r[k]) for r in allr], float) for k in xkeys]
    if controls:
        cols.append(np.array([np.log(max(num(r.get("gdp_pc", "")), 1.0))
                              if np.isfinite(num(r.get("gdp_pc", ""))) else np.nan for r in allr]))
    if controls == "full":
        cols.append(np.array([num(r.get("urban", "")) for r in allr], float))
    X = list(cols)
    if fe in ("country_year", "year"):
        yrs = sorted({int(r["year"]) for r in rows})
        for yy in yrs[1:]: X.append(np.array([1.0 if int(r["year"]) == yy else 0.0 for r in allr]))
    if fe == "country_year":
        isos = sorted({r["iso"] for r in rows})
        for ii in isos[1:]: X.append(np.array([1.0 if r["iso"] == ii else 0.0 for r in allr]))
    return ols(z(y), design(*[z(c) for c in cols], *X), xkeys + ["..."])

spec = []
for att_key in ("edu_upsec_f", "edu_ter_f"):
    sub = [r for r in allr if np.isfinite(num(r.get(att_key, ""))) and np.isfinite(num(r.get("care_f", "")))]
    for ctrl in (None, "gdp", "full"):
        for sample, datum in (("all", sub),
                              ("30+ countries", sub),
                              ("2010_2016", [r for r in sub if int(r["year"]) <= 2016])):
            for fe in ("none", "year", "country_year"):
                if len(datum) < 20: continue
                spec.append(dict(dynamic="A", measure=att_key, controls=str(ctrl), sample=sample, fe=fe,
                                 fit=panel_design(datum, "tfr", ["care_f", att_key], fe, ctrl)))
for meas in ("gap", "isco12_f"):
    sub = [r for r in cs if np.isfinite(num(r.get(meas, ""))) and np.isfinite(num(r.get("tfr", "")))]
    for ctrl in (None, "gdp", "full"):
        if len(sub) < 20: continue
        rows2 = [dict(r, resp=num(r.get("tfr", ""))) for r in sub]
        X = [z([num(r.get(meas, "")) for r in rows2]), z([num(r.get("edu_ter_f", "")) for r in rows2])]
        if ctrl: X.append(z([np.log(max(num(r.get("gdp_pc", "")), 1.0)) for r in rows2]))
        if ctrl == "full": X.append(z([num(r.get("urban", "")) for r in rows2]))
        spec.append(dict(dynamic="B", measure=meas, controls=str(ctrl), sample="cross-section", fe="none",
                         fit=ols(z([r["resp"] for r in rows2]), design(*X), [meas, "attainment", "..."])
                         if all(len(x) == len(rows2) for x in X) else None))
b_ok = [s for s in spec if s["fit"] is not None]
res["spec_curve"] = dict(n_specs=len(b_ok),
                         A_signs=[(1 if s["fit"]["b"][1] > 0 else -1) for s in b_ok if s["dynamic"] == "A"],
                         A_sig=[bool(abs(s["fit"]["t"][1]) > 1.96) for s in b_ok if s["dynamic"] == "A"],
                         B_first_signs=[(1 if s["fit"]["b"][1] < 0 else -1) for s in b_ok if s["dynamic"] == "B"],
                         B_first_sig=[bool(abs(s["fit"]["t"][1]) > 1.96) for s in b_ok if s["dynamic"] == "B"],
                         specs=[dict(dynamic=s["dynamic"], measure=s["measure"], controls=s["controls"],
                                     sample=s["sample"], fe=s["fe"], coef=s["fit"]["b"][1],
                                     t=s["fit"]["t"][1], n=s["fit"]["n"]) for s in b_ok])
print("\n=== SPEC CURVE: A care-share coefficient (pre-registered sign +), B gap/isco coefficient (sign -)")
for s_ in res["spec_curve"]["specs"]:
    print("  %s %-12s ctrl=%-5s samp=%-12s fe=%-12s coef %+.3f t %+.2f n=%d" % (
        s_["dynamic"], s_["measure"], s_["controls"], s_["sample"], s_["fe"], s_["coef"], s_["t"], s_["n"]))
json.dump(dict(cross_section_n=len(cs), change_pairs=len(pairs), results=res),
          open(f"{OUT}/results_care_cred.json", "w"), indent=1, default=float)

def show(key, lab):
    d = res.get(key)
    if not d: print(f"{lab}: insufficient data"); return
    s = "  ".join(f"{n}={b:+.3f} (t={t:+.2f})" % () if False else f"{n} {b:+.3f} [t {t:+.2f}]"
                  for n, b, t in zip(d["names"], d["b"], d["t"]))
    print(f"{lab}: n={d['n']} R2={d['r2']:.3f} | {s}")
print("\n=== CARE ===")
for k in ("A1_care_vs_upsec", "A1_care_vs_upsec_with_urban", "A3_tfr_upsec_interaction",
          "A3_tfr_upsec_interaction_controls", "A3_placebo_male_upsec", "A3_placebo_manuf_upsec", "A2_change"):
    show(k, k)
print("\n=== CREDENTIALS ===")
for k in ("B1_attainment_only", "B1_gap_only", "B1_horse_race", "B1_horse_race_controls",
          "B2_high_attainment_both", "B2_low_attainment_both", "B2_high_attainment_gap", "B2_low_attainment_gap"):
    show(k, k)
