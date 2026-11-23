#!/usr/bin/env python3
"""DHS aggregated-indicator analysis: women's schooling and children ever born.

Unit of observation: the DHS-published cell (country x survey x education / wealth / residence /
region). Outcome: mean children ever born to women aged 40-49 (completed fertility). Estimator:
weighted least squares with country x survey fixed effects (absorbed by weighted demeaning), every
cell weighted by its unweighted number of women; standard errors clustered by country.

Outputs to /root/work/dhs/results/: model_summary.txt plus csv extracts.
"""
import json, os, sys
import numpy as np
import pandas as pd

D = "/root/work/dhs/data"
R = "/root/work/dhs/results"
os.makedirs(R, exist_ok=True)
L = []
A = L.append


def verdict(b, se):
    if se is None or se <= 0:
        return "n/a"
    t = b / se
    return "sig+" if t > 1.96 else ("sig-" if t < -1.96 else "null")


def wls_fe(dat, ycol, xcols, fe, wcol, cluster):
    """weighted OLS with absorbed FE (fe), cluster-robust SE; returns dict name -> (b, se, t)"""
    d = dat.dropna(subset=[ycol] + xcols + [wcol, fe, cluster]).copy()
    if len(d) < 5:
        return None, d
    g = pd.factorize(d[fe])[0]
    c = pd.factorize(d[cluster])[0]
    w = d[wcol].values.astype(float)
    y = d[ycol].values.astype(float)

    def dm(v):
        sw = np.bincount(g, weights=w)
        sv = np.bincount(g, weights=v * w)
        return v - (sv / np.maximum(sw, 1e-12))[g]

    yd = dm(y)
    X = np.column_stack([np.ones(len(d))] + [dm(d[x].values.astype(float)) for x in xcols])
    XtWX = X.T @ (X * w[:, None])
    b = np.linalg.lstsq(XtWX, X.T @ (w * yd), rcond=None)[0]
    u = yd - X @ b
    meat = np.zeros_like(XtWX)
    for cc in np.unique(c):
        m = c == cc
        s = X[m].T @ (w[m] * u[m])
        meat += np.outer(s, s)
    P = np.linalg.pinv(XtWX)
    V = P @ meat @ P
    out = {}
    for j, name in enumerate(xcols):
        k = j + 1
        out[name] = (float(b[k]), float(np.sqrt(max(V[k, k], 0))), int(len(d)))
    return out, d


def prep(df, indicator, category, require_denom=True):
    d = df[(df.IndicatorId == indicator) & (df.CharacteristicCategory == category)].copy()
    d = d[d.Value.notna()]
    if require_denom:
        d = d[d.DenominatorUnweighted.notna()]
        d = d[d.DenominatorUnweighted >= 20]
    d["survey"] = d.SurveyId.astype(str)
    d["country"] = d.DHS_CountryCode.astype(str)
    d["cohort"] = d.SurveyYear.astype(float) - 44.5
    return d


def main():
    df = pd.read_csv(f"{D}/dhs_extract.csv")
    df["Value"] = pd.to_numeric(df.Value, errors="coerce")
    df["DenominatorUnweighted"] = pd.to_numeric(df.DenominatorUnweighted, errors="coerce")
    A("=== data provenance and shape ===")
    A(f"rows {len(df)}, indicators: " + ", ".join(sorted(df.IndicatorId.unique())))
    A(f"surveys {df.SurveyId.nunique()}, countries {df.DHS_CountryCode.nunique()}, years "
      f"{int(df.SurveyYear.min())}-{int(df.SurveyYear.max())}")

    # ---------- A. main completed-fertility model, 4 education levels ----------
    ed = prep(df, "FE_FRTY_W_MNC", "Education")
    ed = ed[ed.CharacteristicLabel.isin(["No education", "Primary", "Secondary", "Higher"])]
    ed["w"] = ed.DenominatorUnweighted
    for lvl in ["Primary", "Secondary", "Higher"]:
        ed["edu_" + lvl.lower()] = (ed.CharacteristicLabel == lvl).astype(float)
    xcols = ["edu_primary", "edu_secondary", "edu_higher"]
    m, used = wls_fe(ed, "Value", xcols, "survey", "w", "country")
    A("")
    A("=== A. completed fertility (women 40-49) on education, country x survey FE ===")
    A(f"cells {len(used)}, surveys {used.survey.nunique()}, countries {used.country.nunique()}, "
      f"median women per cell {int(used.w.median())}")
    for k in xcols:
        if m and k in m:
            b, se, n = m[k]
            A(f"  {k:14s} {b:+.3f} children (SE {se:.3f}) {verdict(b, se)}")
    if m:
        json.dump({k: m[k][:2] for k in m}, open(f"{R}/model_education.json", "w"))
        ed.to_csv(f"{R}/extract_completed_fertility_education.csv", index=False)

    # per-survey 2-group gradient (Secondary+ minus No education or primary)
    e2 = prep(df, "FE_FRTY_W_MNC", "Education (2 groups)")
    e2 = e2[e2.CharacteristicLabel.isin(["No education or primary", "Secondary or higher"])]
    piv = e2.pivot_table(index=["survey", "country", "SurveyYear"], columns="CharacteristicLabel",
                         values="Value", aggfunc="first").dropna()
    piv.columns = ["none_prim", "sec_plus"]
    piv["gradient"] = piv.sec_plus - piv.none_prim
    piv = piv.reset_index()
    A("")
    A("=== B. per-survey gradient: secondary+ minus none/primary (children ever born) ===")
    A(f"surveys {len(piv)}, countries {piv.country.nunique()}; median {piv.gradient.median():+.3f}, "
      f"IQR {piv.gradient.quantile(.25):+.3f} to {piv.gradient.quantile(.75):+.3f}; "
      f"{100*(piv.gradient<0).mean():.0f}% negative")
    piv.to_csv(f"{R}/survey_gradients.csv", index=False)

    # ---------- C. cohort steepening ----------
    edc = ed.copy()
    edc["cohort_c"] = (edc.cohort - 1990) / 10.0
    for lvl in ["primary", "secondary", "higher"]:
        edc["edu_" + lvl + "_x_cohort"] = edc["edu_" + lvl] * edc.cohort_c
    xc = ["edu_primary", "edu_secondary", "edu_higher",
          "edu_primary_x_cohort", "edu_secondary_x_cohort", "edu_higher_x_cohort"]
    mc, usedc = wls_fe(edc, "Value", xc, "survey", "w", "country")
    A("")
    A("=== C. does the gradient steepen in later cohorts? (cohort = survey year - 44.5) ===")
    A(f"cells {len(usedc)}, cohorts {int(usedc.cohort.min())}-{int(usedc.cohort.max())}")
    if mc:
        for lvl in ["primary", "secondary", "higher"]:
            b, se, n = mc["edu_" + lvl]
            bi, sei, _ = mc["edu_" + lvl + "_x_cohort"]
            A(f"  {lvl:9s}: level {b:+.3f} (SE {se:.3f}); change per decade {bi:+.3f} (SE {sei:.3f}) {verdict(bi, sei)}")
    # split early/late
    med = edc.cohort.median()
    for lab, sub in (("earlier cohorts (<=median)", edc[edc.cohort <= med]), ("later cohorts (>median)", edc[edc.cohort > med])):
        me, ue = wls_fe(sub, "Value", xcols, "survey", "w", "country")
        if me:
            A(f"  {lab}: sec+higher vs none: " +
              ", ".join(f"{k} {me[k][0]:+.3f}({me[k][1]:.3f})" for k in xcols))
    A(f"  (cohort median split at birth year {med:.0f})")

    # ---------- D. pipeline density interaction ----------
    # DHS-own pipeline measure: share of women 15-49 with secondary or higher, built from the age
    # breakdown of ED_EDUC_W_SEH weighted by the number of women (ED_EDUC_W_TOT) in each age group.
    cat = None
    for c in ("Age (10-year groups)", "Age (5-year groups)"):
        if ((df.IndicatorId == "ED_EDUC_W_SEH") & (df.CharacteristicCategory == c)).any():
            cat = c
            break
    pipe = None
    if cat is not None:
        a = df[(df.IndicatorId == "ED_EDUC_W_SEH") & (df.CharacteristicCategory == cat)]
        b = df[(df.IndicatorId == "ED_EDUC_W_TOT") & (df.CharacteristicCategory == cat)]
        a = a.groupby(["SurveyId", "CharacteristicLabel"]).agg(seh=("Value", "first"),
                                                               yr=("SurveyYear", "first"),
                                                               ctry=("DHS_CountryCode", "first")).reset_index()
        b = b.groupby(["SurveyId", "CharacteristicLabel"]).agg(women=("Value", "first")).reset_index()
        mrg = a.merge(b, on=["SurveyId", "CharacteristicLabel"]).dropna()
        mrg = mrg[mrg.women > 0]
        pipe = mrg.groupby("SurveyId").apply(lambda g: pd.Series(dict(
            pipe=float((g.seh * g.women).sum() / g.women.sum()),
            SurveyYear=float(g.yr.iloc[0]), country=str(g.ctry.iloc[0])))).reset_index()
        pipe["survey"] = pipe.SurveyId.astype(str)
    else:
        pipe = pd.DataFrame(columns=["survey", "pipe"])
    edp = ed.merge(pipe[["survey", "pipe"]], on="survey", how="left").dropna(subset=["pipe"])
    edp["pipe_c"] = (edp["pipe"] - 50.0) / 10.0
    for lvl in ["primary", "secondary", "higher"]:
        edp["edu_" + lvl + "_x_pipe"] = edp["edu_" + lvl] * edp.pipe_c
    xp = ["edu_primary", "edu_secondary", "edu_higher",
          "edu_primary_x_pipe", "edu_secondary_x_pipe", "edu_higher_x_pipe"]
    mp, usedp = wls_fe(edp, "Value", xp, "survey", "w", "country")
    A("")
    A("=== D. does the gradient steepen where the schooling pipeline is denser? ===")
    A(f"pipeline = share of women with secondary or higher at the survey (national, ED_EDUC_W_SEH); "
      f"cells {len(usedp)}, surveys {usedp.survey.nunique()}")
    if mp:
        for lvl in ["primary", "secondary", "higher"]:
            b, se, n = mp["edu_" + lvl]
            bi, sei, _ = mp["edu_" + lvl + "_x_pipe"]
            A(f"  {lvl:9s}: level {b:+.3f} (SE {se:.3f}); change per +10pp pipeline {bi:+.3f} (SE {sei:.3f}) {verdict(bi, sei)}")
    # median split pipelines
    for lab, sub in (("low-pipeline surveys", edp[edp["pipe"] <= edp["pipe"].median()]),
                     ("high-pipeline surveys", edp[edp["pipe"] > edp["pipe"].median()])):
        mm, uu = wls_fe(sub, "Value", xcols, "survey", "w", "country")
        if mm:
            A(f"  {lab}: " + ", ".join(f"{k} {mm[k][0]:+.3f}({mm[k][1]:.3f})" for k in xcols))
    A(f"  (pipeline median split at {edp['pipe'].median():.1f}%)")

    # ---------- E. wealth gradient (comparison; aggregates do not cross education x wealth) ----------
    wl = prep(df, "FE_FRTY_W_MNC", "Wealth quintile")
    wl = wl[wl.CharacteristicLabel.isin(["Lowest", "Second", "Middle", "Fourth", "Highest"])]
    wl["w"] = wl.DenominatorUnweighted
    for q in ["Second", "Middle", "Fourth", "Highest"]:
        wl["wq_" + q.lower()] = (wl.CharacteristicLabel == q).astype(float)
    xw = ["wq_second", "wq_middle", "wq_fourth", "wq_highest"]
    mw, usedw = wls_fe(wl, "Value", xw, "survey", "w", "country")
    A("")
    A("=== E. wealth gradient for the same outcome (not a horse race: the API does not cross education x wealth) ===")
    A(f"cells {len(usedw)}, surveys {usedw.survey.nunique()}, countries {usedw.country.nunique()}")
    if mw:
        for k in xw:
            b, se, n = mw[k]
            A(f"  {k:11s} {b:+.3f} (SE {se:.3f}) {verdict(b, se)}")
        json.dump({k: mw[k][:2] for k in mw}, open(f"{R}/model_wealth.json", "w"))

    # ---------- F. tempo: median age at first birth (women 25-29) by education ----------
    af = prep(df, "FE_AAFB_W_M25", "Education", require_denom=False)
    af = af[af.CharacteristicLabel.isin(["No education", "Primary", "Secondary", "Higher"])]
    # medians have no published denominator; weight all cells equally
    af["w"] = 1.0
    for lvl in ["Primary", "Secondary", "Higher"]:
        af["edu_" + lvl.lower()] = (af.CharacteristicLabel == lvl).astype(float)
    ma, useda = wls_fe(af, "Value", xcols, "survey", "w", "country")
    A("")
    A("=== F. tempo: median age at first birth (women 25-29) on education, same FE ===")
    A(f"cells {len(useda)}, surveys {useda.survey.nunique()}, countries {useda.country.nunique()}")
    if ma:
        for k in xcols:
            b, se, n = ma[k]
            A(f"  {k:14s} {b:+.3f} years (SE {se:.3f}) {verdict(b, se)}")
        json.dump({k: ma[k][:2] for k in ma}, open(f"{R}/model_age_first_birth.json", "w"))
        af.to_csv(f"{R}/extract_age_first_birth_education.csv", index=False)

    # ---------- F2. cohort-specific gradients (requested explicitly) ----------
    piv2 = piv.copy()
    piv2["cohort"] = piv2.SurveyYear.astype(float) - 44.5
    piv2["cohort_decade"] = (piv2.cohort // 10 * 10).astype(int)
    A("")
    A("=== F2. cohort-specific per-survey gradient (secondary+ minus none/primary, children) ===")
    A("  cohort  n_surveys  median_gradient  IQR")
    for cd, g in piv2.groupby("cohort_decade"):
        if len(g) < 3:
            continue
        A(f"  {cd}s   {len(g):3d}       {g.gradient.median():+.3f}         {g.gradient.quantile(.25):+.3f} to {g.gradient.quantile(.75):+.3f}")
    piv2.to_csv(f"{R}/cohort_gradients.csv", index=False)

    # ---------- F3. pipeline terciles for the per-survey gradient ----------
    if len(pipe):
        pv = piv.merge(pipe[["survey", "pipe"]], on="survey", how="inner")
        try:
            pv["tercile"] = pd.qcut(pv["pipe"], 3, labels=["low", "middle", "high"])
            A("")
            A("=== F3. per-survey gradient by pipeline tercile (share of women with secondary+) ===")
            for t3, g in pv.groupby("tercile", observed=True):
                A(f"  {str(t3):7s}: n={len(g):3d} median {g.gradient.median():+.3f} "
                  f"IQR {g.gradient.quantile(.25):+.3f} to {g.gradient.quantile(.75):+.3f}; "
                  f"pipeline {g['pipe'].median():.0f}%")
        except Exception as e:
            A("  pipeline terciles not computed: " + str(e))

    # ---------- F4. tempo vs quantum headline ----------
    if ma and isinstance(m, dict):
        A("")
        A("=== F4. tempo vs quantum: same model, two outcomes ===")
        A("  education level      completed fertility (children)   median age at first birth (years)")
        for lvl, key in (("secondary vs none", "edu_secondary"), ("higher vs none", "edu_higher")):
            if key in m and key in ma:
                A(f"  {lvl:18s} {m[key][0]:+.3f} ({m[key][1]:.3f})                {ma[key][0]:+.3f} ({ma[key][1]:.3f})")

    # ---------- G. sanity: children ever born by age group ----------
    ag = prep(df, "FE_CEBA_W_MNC", "Age (5-year groups)")
    order = ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49"]
    agg = ag[ag.CharacteristicLabel.isin(order)].groupby("CharacteristicLabel").Value.median().reindex(order)
    A("")
    A("=== G. sanity check: median children ever born by age group (all women) ===")
    A("  " + ", ".join(f"{k} {v:.2f}" for k, v in agg.items() if pd.notna(v)))

    # ---------- H. education distribution (pipeline) coverage ----------
    A("")
    A("=== H. pipeline indicator coverage ===")
    A(f"pipeline (DHS own, weighted ED_EDUC_W_SEH): {len(pipe)} surveys; range "
      f"{pipe['pipe'].min():.0f}% to {pipe['pipe'].max():.0f}%, median {pipe['pipe'].median():.0f}%")

    open(f"{R}/model_summary.txt", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
