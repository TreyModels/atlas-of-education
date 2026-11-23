"""Consolidate the scaling evidence (task-19): local massification tables + new tests.

Inputs (read-only):
  /root/work/local_data/10_massification/relations/data/scaling_laws.csv   (within vs between)
  /root/work/local_data/10_massification/model2/runs/scaling_classification.csv
  /root/work/scaling/results/scaling_results.json                          (new tests: Heaps, collapse, urban)
  /root/work/data/*.json                                                   (panel for the collapse levels-vs-changes test)

Output: results/consolidated_verdicts.json and results/consolidated_verdicts.csv
Rule applied (from lit/SCALING_LAWS.md): a *law* needs a stable exponent across samples and
estimators; a *regularity* is a stable pattern without that; a *threshold* is a cut-point.
Extended rule for this task: an exponent also has to survive the within-vs-between contrast —
a between-country cross-section that vanishes inside countries is a between-country regularity,
not a law about how a country changes as it grows.
"""
import csv, json, math, os
import numpy as np

LOCAL = "/root/work/local_data/10_massification"
WD = "/root/work/scaling"
OUT = os.path.join(WD, "results")
DATA = "/root/work/data"
os.makedirs(OUT, exist_ok=True)


def rows(path):
    with open(path, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def f(x):
    try:
        return float(x)
    except Exception:
        return None


# ---------------------------------------------------------------- 1. within vs between table
sl = rows(os.path.join(LOCAL, "relations/data/scaling_laws.csv"))
pairs = {}
for r in sl:
    base = r["id"].split("-")[0]
    pairs.setdefault(base, {})[r["id"].split("-")[1]] = r
wb = []
for base, d in pairs.items():
    w, b = d.get("within"), d.get("between")
    if not w or not b:
        continue
    cw, sw, cb, sb = f(w["coef"]), f(w["se"]), f(b["coef"]), f(b["se"])
    if None in (cw, sw, cb, sb):
        continue
    se_d = math.sqrt(sw ** 2 + sb ** 2)
    z = (cw - cb) / se_d if se_d > 0 else float("nan")
    tw = cw / sw if sw > 0 else float("nan")
    tb = cb / sb if sb > 0 else float("nan")
    ratio = cw / cb if cb not in (0, None) else float("nan")
    wb.append(dict(
        relation=w["relation"], outcome=w["outcome"], driver=w["driver"],
        form=w["functional_form"], n=int(w["n"]), n_cty=int(w["n_cty"]), period=w["period"],
        between_coef=cb, between_se=sb, between_t=tb,
        within_coef=cw, within_se=sw, within_t=tw,
        within_over_between=ratio, diff_z=z,
        within_r2=f(w.get("within_r2")),
        classification_local=w["classification"],
        identification=w["identification_grade"],
    ))


def verdict(w):
    """Extended stability rule."""
    bw_sig = abs(w["between_t"]) >= 1.96
    wi_sig = abs(w["within_t"]) >= 1.96
    ratio = w["within_over_between"]
    same_sign = (w["within_coef"] * w["between_coef"]) > 0
    if not bw_sig and not wi_sig:
        return "unidentified"
    if bw_sig and not wi_sig:
        return "between-country regularity (not a law about change)"
    if wi_sig and not bw_sig:
        return "within-country regularity only"
    if bw_sig and wi_sig and same_sign and 0.67 <= ratio <= 1.5:
        return "stable across within/between: law-like candidate"
    return "unstable across within/between: regularity"


for w in wb:
    w["verdict_extended"] = verdict(w)

# ---------------------------------------------------------------- 2. local stability classification
cl = rows(os.path.join(LOCAL, "model2/runs/scaling_classification.csv"))
cls = []
for r in cl:
    if r["part"] != "classification":
        continue
    cls.append(dict(pair=r["pair"], sample=r["sample"], n_estimators_significant=int(r["n_sig"]),
                    sign_stable=r["sign_stable"] == "True",
                    magnitude_ratio=f(r["magnitude_ratio"]),
                    local_classification=r["classification"]))
for c in cls:
    if c["local_classification"].startswith("scaling law"):
        c["verdict_local_rule"] = "law-like under local rule (stable across estimators)"
    elif c["local_classification"] == "unidentified":
        c["verdict_local_rule"] = "unidentified"
    else:
        c["verdict_local_rule"] = "regularity"

# ---------------------------------------------------------------- 3. new tests from this task
new = json.load(open(os.path.join(WD, "results", "scaling_results.json")))["sections"]
tests = []
h = new["heaps"]
tests.append(dict(relation="occupational categories vs sample size (Heaps, rarefied)",
                  estimate=h["heaps_exponent"], se=h["se"], n=h["npoints"], n_countries=h["ncountries"],
                  benchmark="Heaps literature 0.4-0.6",
                  verdict="sublinear; below literature band",
                  note="ISCO-08 1-digit (10 categories) only; 2-/3-digit deprecated in ILOSTAT API. "
                       "Raw category counts vs workforce give exponent %.3f (sampling-effort trap)." %
                       h["raw_count_vs_workforce_exponent"]))
u = new["urban_income"]
tests.append(dict(relation="urban share vs income (logistic vs power law)",
                  estimate=u["logistic"]["b"], se=u["logistic"]["b_se"], n=u["nobs"],
                  n_countries=u["ncountries"],
                  benchmark="Bettencourt is a city-output law, not this; S-curve benchmark is qualitative",
                  verdict="logistic beats power law out of sample (RMSE %.4f vs %.4f); regularity, not a scaling law" %
                          (u["out_of_sample_rmse_share"]["logistic"], u["out_of_sample_rmse_share"]["power"]),
                  note="logistic steepness %.3f (SE %.3f), midpoint income $%.0f" %
                       (u["logistic"]["b"], u["logistic"]["b_se"], u["logistic"]["midpoint_income_levels"])))
fi = new["fertility_income"]
tests.append(dict(relation="fertility vs income (power law)",
                  estimate=fi["power_law"]["exponent"], se=fi["power_law"]["se"], n=fi["n"],
                  n_countries=fi["ncountries"], benchmark="no canonical exponent",
                  verdict="power law with mild curvature",
                  note="squared term %.4f (SE %.4f); out-of-sample RMSE power %.4f vs quadratic %.4f" %
                       (fi["quadratic"]["squared"], fi["quadratic"]["squared_se"],
                        fi["oos_rmse_logtfr"]["power_law"], fi["oos_rmse_logtfr"]["quadratic"])))
c = new["collapse"]
q = c["collapse_quality"]
tests.append(dict(relation="fertility vs female attainment across countries and cohorts (collapse)",
                  estimate=c["fits"]["exponential"]["decay"], se=c["fits"]["exponential"]["decay_se"],
                  n=c["n"], n_countries=c["ncountries"],
                  benchmark="single common curve (data collapse)",
                  verdict="NOT a single curve: country structure remains",
                  note="pooled R2 %.3f; R2 with country intercepts %.3f, country slopes %.3f; "
                       "slope-heterogeneity F = %.1f; residual SD %.3f (%.1f%% of the fertility range); "
                       "after a country-level rescaling residual SD %.3f (R2 %.3f); low-income residual "
                       "+%.2f vs high-income %.2f; early cohorts +%.2f vs 1970s cohorts %.2f" %
                       (q["r2_pooled"], q["r2_country_intercepts"], q["r2_country_slopes"],
                        q["F_country_slopes_vs_pooled"]["F"], q["residual_sd"],
                        100 * q["residual_sd_over_range"], q["residual_sd_rescaled"],
                        q["r2_country_mult_rescale"],
                        c["residual_structure"]["by_income_group"]["Low income"]["mean_resid"],
                        c["residual_structure"]["by_income_group"]["High income"]["mean_resid"],
                        c["residual_structure"]["by_cohort_band"]["1950"]["mean_resid"],
                        c["residual_structure"]["by_cohort_band"]["1970"]["mean_resid"])))
t = new["wagner"]
tests.append(dict(relation="tax share vs income (Wagner)", estimate=t["elasticity"], se=t["se"],
                  n=t["n"], n_countries=t["ncountries"], benchmark="Wagner: elasticity > 1",
                  verdict="fails Wagner (elasticity far below 1); indicator definition undocumented",
                  note=t["caveat"]))
mn = new["schooling_income"]
tests.append(dict(relation="schooling vs income (weak Mincer proxy)", estimate=mn["slope"],
                  se=mn["slope_se"], n=mn["n"], n_countries=mn["ncountries"],
                  benchmark="individual Mincer return 0.05-0.15 — NOT comparable",
                  verdict="country-level association only; unidentified as a Mincer return",
                  note=mn["caveat"]))

# ---------------------------------------------------------------- 4. levels vs changes on the collapse panel
META = json.load(open(os.path.join(DATA, "meta.json")))


def panel(name):
    d = {}
    for r in json.load(open(os.path.join(DATA, name + ".json"))):
        try:
            d[(r[0], int(r[1]))] = float(r[2])
        except Exception:
            pass
    return d


FERT, SEC, GPI = panel("fertility"), panel("sec"), panel("gpi_sec")
coh = []
for iso, m in META.items():
    if m.get("region") == "Aggregates":
        continue
    for cc in range(1950, 1997):
        s, g, t = SEC.get((iso, cc + 20)), GPI.get((iso, cc + 20)), FERT.get((iso, cc + 28))
        if s and g and t and t > 0 and 0.2 <= g <= 2.0:
            att = s * 2 * g / (1 + g)
            if att > 0:
                coh.append((iso, cc, att, t))
CISO = np.array([r[0] for r in coh]); CCOH = np.array([r[1] for r in coh])
CA = np.array([r[2] for r in coh]); CT = np.array([r[3] for r in coh])
ly, lx = np.log(CT), np.log(CA)
# between: country means; within: country-demeaned
cmeans_x = {c: lx[CISO == c].mean() for c in set(CISO)}
cmeans_y = {c: ly[CISO == c].mean() for c in set(CISO)}
mb = np.polyfit(np.array([cmeans_x[c] for c in sorted(cmeans_x)]),
                np.array([cmeans_y[c] for c in sorted(cmeans_x)]), 1)
between_slope = float(mb[0])
dmx = lx - np.array([cmeans_x[c] for c in CISO])
dmy = ly - np.array([cmeans_y[c] for c in CISO])
within_slope = float(np.sum(dmx * dmy) / np.sum(dmx ** 2))
r_within = dmy - within_slope * dmx
lib = np.unique(CISO)
se_w = math.sqrt(sum((dmx[CISO == c] * r_within[CISO == c]).sum() ** 2 for c in lib) / np.sum(dmx ** 2) ** 2)
# changes: 10-year differences within country
idx = {(CISO[i], int(CCOH[i])): i for i in range(len(coh))}
ch = []
for c in lib:
    for i in range(len(coh)):
        if CISO[i] != c:
            continue
        j = idx.get((c, int(CCOH[i]) + 10))
        if j is not None:
            ch.append((c, math.log(CT[j]) - math.log(CT[i]), math.log(CA[j]) - math.log(CA[i])))
ch = np.array([(r[1], r[2]) for r in ch])
change_slope = float(np.polyfit(ch[:, 1], ch[:, 0], 1)[0])
levels_vs_changes = dict(
    relation="fertility vs female attainment: levels vs changes",
    between_country_slope=between_slope, within_country_levels_slope=within_slope, within_se=se_w,
    within_t=within_slope / se_w if se_w > 0 else None,
    ten_year_change_slope=change_slope, n_levels=int(len(CT)), n_changes=int(len(ch)),
    ncountries=int(len(lib)),
    verdict="between-country relation is strong and negative; the within-country level slope and the "
            "ten-year change slope are the test of whether it is a law about change",
)

# ---------------------------------------------------------------- 5. unified verdict table
unified = []
for w in wb:
    unified.append(dict(
        relation=w["relation"], source="local scaling_laws.csv (within vs between)",
        estimate=w["between_coef"], se=w["between_se"], n=w["n"], n_countries=w["n_cty"],
        within_estimate=w["within_coef"], within_se=w["within_se"],
        local_classification=w["classification_local"], verdict=w["verdict_extended"]))
for c in cls:
    unified.append(dict(
        relation=c["pair"], source="local scaling_classification.csv (5 estimators)",
        estimate=None, se=None, n=None, n_countries=None,
        within_estimate=None, within_se=None,
        local_classification=c["local_classification"], verdict=c["verdict_local_rule"]))
for t in tests:
    unified.append(dict(
        relation=t["relation"], source="this task (new tests)",
        estimate=t["estimate"], se=t["se"], n=t["n"], n_countries=t["n_countries"],
        within_estimate=None, within_se=None,
        local_classification=t["benchmark"], verdict=t["verdict"]))
out = dict(within_between=wb, local_classification=cls, new_tests=tests,
           levels_vs_changes=levels_vs_changes, unified_verdicts=unified,
           rule="law = stable exponent across samples/estimators AND credible within-vs-between; "
                "a between-country cross-section that vanishes inside countries is a regularity")
json.dump(out, open(os.path.join(OUT, "consolidated_verdicts.json"), "w"), indent=1)
with open(os.path.join(OUT, "consolidated_verdicts.csv"), "w", newline="") as fh:
    wtr = csv.writer(fh)
    wtr.writerow(["relation", "source", "estimate", "se", "n", "n_countries",
                  "within_estimate", "within_se", "local_classification", "verdict"])
    for r in unified:
        wtr.writerow([r["relation"], r["source"], r["estimate"], r["se"], r["n"], r["n_countries"],
                      r["within_estimate"], r["within_se"], r["local_classification"], r["verdict"]])
print("WROTE", os.path.join(OUT, "consolidated_verdicts.json"))
print("levels-vs-changes:", json.dumps(levels_vs_changes, indent=1))
print("law-like (extended):", [r["relation"] for r in wb if r["verdict_extended"].startswith("stable")])
print("between-only:", [r["relation"] for r in wb if r["verdict_extended"].startswith("between")])
print("local law-like:", [c["pair"] for c in cls if c["local_classification"].startswith("scaling law")])
