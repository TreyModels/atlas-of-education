#!/usr/bin/env python3
"""Gender split of the E8 fee-abolition event study (Leg A) — pre-registered in PRE_REGISTRATION.md.

Reuses the estimator logic of
  research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py @ bd782be
(att_cs = Callaway–Sant'Anna ATT(g,t) with universal base g-1 and not-yet-treated controls, event -5..+6,
cohort-size-weighted aggregation; boot_rep = country-cluster bootstrap), imported directly from that file.

Design fixed in PRE_REGISTRATION.md (commit 875ffd8):
  outcomes  WDI/UIS SE.PRM.ENRR.FE (female), SE.PRM.ENRR.MA (male)   [OBSERVED]
  gate      pooled SE.PRM.ENRR ATT(0) must reproduce 12.4436 within 0.50 pp
  primary   D = mean_{e=+1..+6} ATT_F(e) - mean_{e=+1..+6} ATT_M(e), paired country-cluster bootstrap
  bootstrap 500 reps, replicate i uses numpy.random.default_rng(20261125 + i); percentile 95% CI
No causal language. Nulls/failures reported.

Outputs: results/e8_event_<indicator>_verified8.csv, results/e8_event_difference_verified8.csv,
results/pooled_reproduction_gate.json, results/gender_split_results.json
"""
import importlib.util
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(REC, "data")
RES = os.path.join(REC, "results")
os.makedirs(RES, exist_ok=True)

E8_SCRIPT = os.path.abspath(os.path.join(
    REC, "..", "2026-11-25-e6e8-sequencing", "scripts", "e8_fee_event_study.py"))
FEE_DATES = os.path.abspath(os.path.join(
    REC, "..", "2026-11-25-e6e8-sequencing", "data", "fee_dates.csv"))

YEARS = tuple(range(1990, 2016))          # 1990–2015, the E8 window at bd782be
EVENTS = list(range(-5, 7))
POST = [1, 2, 3, 4, 5, 6]                 # pre-registered post window for D
N_BOOT = 500
SEED_BASE = 20261125
GATE_TARGET = 12.4436
GATE_TOL = 0.50

IND = {"F": "SE.PRM.ENRR.FE", "M": "SE.PRM.ENRR.MA", "pooled": "SE.PRM.ENRR"}


def load_e8_module():
    spec = importlib.util.spec_from_file_location("e8_fee_event_study", E8_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E8 = load_e8_module()
att_cs = E8.att_cs


def load_panel(indicator):
    if indicator == IND["pooled"]:
        p = os.path.join(DATA, "wdi_pooled_ger_panel.csv")
    else:
        p = os.path.join(DATA, "wdi_sex_ger_panels.csv")
    d = pd.read_csv(p)
    d = d[d.indicator == indicator]
    d = d[(d.year >= YEARS[0]) & (d.year <= YEARS[-1])]
    return d[["iso3", "year", "value"]]


def load_region():
    m = pd.read_csv(os.path.join(DATA, "wdi_metadata_country.csv"))
    m["region"] = m["region"].fillna("")
    return m


def load_verified():
    fee = pd.read_csv(FEE_DATES)
    fee["preferred_year"] = pd.to_numeric(fee["preferred_year"], errors="coerce")
    v = fee[fee.status == "VERIFIED"].copy()
    return dict(zip(v.iso3, v.preferred_year.astype(int)))


def ymat(panel, countries):
    out = {}
    for iso, g in panel.groupby("iso3"):
        if iso in countries:
            out[iso] = dict(zip(g.year.astype(int), g.value.astype(float)))
    return out


def event_table(ev):
    return ev.sort_values("event").reset_index(drop=True) if len(ev) else ev


def boot_event_tables(Y, coh, draws_universe, seeds, sex_series=None, coh_series=None):
    """Country-cluster bootstrap. If sex_series is None: one series, own universe.

    sex_series: dict sex -> Y dict (F, M); the SAME country draw (from `draws_universe`) is used for both,
    so the same countries enter both sexes (paired bootstrap for the difference).
    Returns {sex: {event: {replicate_index: value}}} (or {"by_event": ...} for the single-series case),
    keyed by replicate index so paired differences use the SAME draw even when some events are undefined in
    some replicates.
    """
    if sex_series is not None:
        out = {"F": {e: {} for e in EVENTS}, "M": {e: {} for e in EVENTS}}
        for i, seed in enumerate(seeds):
            rng = np.random.default_rng(seed)
            draw = rng.choice(draws_universe, size=len(draws_universe), replace=True)
            for sex in ("F", "M"):
                Yb = {}
                for k, c in enumerate(draw):
                    if c in sex_series[sex]:
                        Yb[f"{c}_{k}"] = sex_series[sex][c]
                cohb = {f"{c}_{k}": coh_series[sex][c] for k, c in enumerate(draw)
                        if c in coh_series[sex]}
                _, ev = att_cs(Yb, cohb, YEARS)
                if len(ev):
                    for e, a in zip(ev.event.astype(int), ev.att.astype(float)):
                        if e in out[sex]:
                            out[sex][e][i] = a
        return out
    out = {e: {} for e in EVENTS}
    for i, seed in enumerate(seeds):
        rng = np.random.default_rng(seed)
        draw = rng.choice(draws_universe, size=len(draws_universe), replace=True)
        Yb = {}
        for k, c in enumerate(draw):
            if c in Y:
                Yb[f"{c}_{k}"] = Y[c]
        cohb = {f"{c}_{k}": coh[c] for k, c in enumerate(draw) if c in coh}
        _, ev = att_cs(Yb, cohb, YEARS)
        if len(ev):
            for e, a in zip(ev.event.astype(int), ev.att.astype(float)):
                if e in out:
                    out[e][i] = a
    return {"by_event": out}


def ci(arr):
    a = np.asarray(arr, dtype=float)
    a = a[np.isfinite(a)]
    if len(a) < 10:
        return (np.nan, np.nan, int(len(a)))
    lo, hi = np.percentile(a, [2.5, 97.5])
    return (float(lo), float(hi), int(len(a)))


def main():
    reg = load_region()
    ssa = set(reg.loc[reg.region.str.contains("Sub-Saharan", na=False), "iso3"])
    verified = load_verified()

    results = {"preregistration_commit": "875ffd8", "years": [YEARS[0], YEARS[-1]],
               "events": EVENTS, "n_boot": N_BOOT, "seed_base": SEED_BASE,
               "gate_target": GATE_TARGET, "gate_tolerance": GATE_TOL,
               "indicators": IND, "sample": "Sub-Saharan Africa (WDI metadata), 1990-2015"}

    # ---------- models, point estimates ----------
    panels = {k: load_panel(v) for k, v in IND.items()}
    samples = {}
    for k, panel in panels.items():
        countries = set(panel.iso3) & ssa
        Y = ymat(panel, countries)
        coh = {c: g for c, g in verified.items() if c in Y}
        att_gt, ev = att_cs(Y, coh, YEARS)
        ev = event_table(ev)
        samples[k] = {"Y": Y, "coh": coh, "att_gt": att_gt, "ev": ev,
                      "n_countries": len(Y), "n_treated": len(coh),
                      "treated": sorted(coh), "treated_missing": sorted(set(verified) - set(coh))}

    # ---------- gate: pooled pooled ATT(0) ----------
    ev_p = samples["pooled"]["ev"]
    att0 = float(ev_p.loc[ev_p.event == 0, "att"].iloc[0]) if (ev_p.event == 0).any() else float("nan")
    gate_pass = bool(np.isfinite(att0) and abs(att0 - GATE_TARGET) <= GATE_TOL)
    gate = {"series": IND["pooled"], "sample": "SSA 1990-2015, verified-8 cohorts",
            "att0_reproduced": att0, "att0_reported_at_bd782be": GATE_TARGET,
            "deviation": float(att0 - GATE_TARGET) if np.isfinite(att0) else None,
            "tolerance_pp": GATE_TOL, "gate_pass": gate_pass,
            "n_treated": samples["pooled"]["n_treated"],
            "n_control_countries": int(ev_p.loc[ev_p.event == 0, "n_controls"].iloc[0]) if (ev_p.event == 0).any() else None,
            "wdi_vintage": "2026-11-11 (see data/input_hashes.csv)",
            "reference": "results/e8_event_SE.PRM.ENRR_verified8.csv @ bd782be, event 0 att=12.44362392207772"}
    pd.DataFrame([gate]).to_csv(os.path.join(RES, "pooled_reproduction_gate.csv"), index=False)
    json.dump(gate, open(os.path.join(RES, "pooled_reproduction_gate.json"), "w"), indent=1)

    # ---------- pooled reproduction bootstrap (same pre-registered seeds) ----------
    seeds = [SEED_BASE + i for i in range(N_BOOT)]
    pooled_boot = boot_event_tables(samples["pooled"]["Y"], samples["pooled"]["coh"],
                                    sorted(samples["pooled"]["Y"]), seeds)
    prow = []
    for _, r in samples["pooled"]["ev"].iterrows():
        e = int(r.event)
        lo, hi, nrep = ci(list(pooled_boot["by_event"].get(e, {}).values()))
        prow.append({"event": e, "att": float(r.att), "ci_lo": lo, "ci_hi": hi, "n_boot_used": nrep,
                     "n": int(r.n), "n_treated": int(r.n_treated), "n_controls": int(r.n_controls),
                     "outcome": IND["pooled"], "dates": "verified8", "series_label": "OBSERVED (WDI/UIS)"})
    pooled_tab = pd.DataFrame(prow).sort_values("event")
    pooled_tab.to_csv(os.path.join(RES, "e8_event_SE.PRM.ENRR_verified8_reproduction.csv"), index=False)
    # verify every event matches the committed bd782be table
    ref_csv = os.path.abspath(os.path.join(REC, "..", "2026-11-25-e6e8-sequencing", "results",
                                           "e8_event_SE.PRM.ENRR_verified8.csv"))
    max_dev = None
    event_devs = {}
    if os.path.exists(ref_csv):
        ref = pd.read_csv(ref_csv)
        ref_att = dict(zip(ref.event.astype(int), ref.att.astype(float)))
        for _, r in pooled_tab.iterrows():
            e = int(r.event)
            if e in ref_att:
                dv = float(r.att - ref_att[e])
                event_devs[e] = dv
                max_dev = abs(dv) if max_dev is None else max(max_dev, abs(dv))
    gate["event_by_event_vs_bd782be"] = {"max_abs_deviation": max_dev, "deviations": event_devs,
                                         "reference": "research/records/2026-11-25-e6e8-sequencing/results/"
                                                      "e8_event_SE.PRM.ENRR_verified8.csv @ bd782be",
                                         "bootstrap_note": "this run uses the pre-registered seeds 20261125+i, "
                                                           "so CI endpoints are not expected to equal the E8 "
                                                           "record's (seeds 1000+i); point estimates are the gate"}
    json.dump(gate, open(os.path.join(RES, "pooled_reproduction_gate.json"), "w"), indent=1)

    # ---------- paired bootstrap ----------
    draws_universe = sorted(set(samples["F"]["Y"]) | set(samples["M"]["Y"]))
    seeds = [SEED_BASE + i for i in range(N_BOOT)]
    boots_sex = boot_event_tables(None, None, draws_universe, seeds,
                                  sex_series={"F": samples["F"]["Y"], "M": samples["M"]["Y"]},
                                  coh_series={"F": samples["F"]["coh"], "M": samples["M"]["coh"]})

    # ---------- per-sex event tables ----------
    tables = {}
    for sex in ("F", "M"):
        ev = samples[sex]["ev"].copy()
        rows = []
        b = boots_sex[sex]
        for _, r in ev.iterrows():
            e = int(r.event)
            lo, hi, nrep = ci(list(b[e].values())) if e in b else (np.nan, np.nan, 0)
            rows.append({"event": e, "att": float(r.att), "ci_lo": lo, "ci_hi": hi,
                         "n_boot_used": nrep, "n": int(r.n), "n_treated": int(r.n_treated),
                         "n_controls": int(r.n_controls), "outcome": IND[sex],
                         "dates": "verified8", "series_label": "OBSERVED (WDI/UIS)"})
        t = pd.DataFrame(rows)
        tables[sex] = t
        t.to_csv(os.path.join(RES, f"e8_event_{IND[sex]}_verified8.csv"), index=False)

    # ---------- difference per event + primary D ----------
    def att_at(sex, e):
        t = tables[sex]
        m = t[t.event == e]
        return float(m.att.iloc[0]) if len(m) else float("nan")

    rows = []
    db = []
    used_events = []
    for e in EVENTS:
        f = att_at("F", e)
        m_ = att_at("M", e)
        dif = f - m_ if (np.isfinite(f) and np.isfinite(m_)) else None
        # replicate-level paired difference at this event
        bF, bM = boots_sex["F"], boots_sex["M"]
        common = sorted(set(bF.get(e, {})) & set(bM.get(e, {})))
        if common:
            dd = [bF[e][k] - bM[e][k] for k in common]
            lo, hi, nrep = ci(dd)
        else:
            lo, hi, nrep = (np.nan, np.nan, 0)
        rows.append({"event": e, "att_F": f, "att_M": m_, "att_diff_F_minus_M": dif,
                     "diff_ci_lo": lo, "diff_ci_hi": hi, "diff_n_boot_used": nrep,
                     "n_treated_F": int(tables["F"].loc[tables["F"].event == e, "n_treated"].iloc[0]) if e in set(tables["F"].event) else None,
                     "n_treated_M": int(tables["M"].loc[tables["M"].event == e, "n_treated"].iloc[0]) if e in set(tables["M"].event) else None})
    pd.DataFrame(rows).to_csv(os.path.join(RES, "e8_event_difference_verified8.csv"), index=False)

    for e in POST:
        f = att_at("F", e)
        m_ = att_at("M", e)
        if np.isfinite(f) and np.isfinite(m_):
            used_events.append(e)
            db.append({"event": e, "att_F": f, "att_M": m_})
    if used_events:
        D = float(np.mean([r["att_F"] for r in db]) - np.mean([r["att_M"] for r in db]))
    else:
        D = float("nan")
    # paired bootstrap D
    reps = []
    if used_events:
        common_reps = None
        for e in used_events:
            s_e = set(boots_sex["F"].get(e, {})) & set(boots_sex["M"].get(e, {}))
            common_reps = s_e if common_reps is None else (common_reps & s_e)
        for k in sorted(common_reps or []):
            valsF = [boots_sex["F"][e][k] for e in used_events]
            valsM = [boots_sex["M"][e][k] for e in used_events]
            reps.append(float(np.mean(valsF) - np.mean(valsM)))
    if len(reps) >= 10:
        D_lo, D_hi = np.percentile(reps, [2.5, 97.5])
        D_ci = [float(D_lo), float(D_hi)]
    else:
        D_ci = [None, None]
    ci_excludes_zero = bool(len(reps) >= 10 and (D_ci[0] is not None) and (D_ci[0] > 0 or D_ci[1] < 0))
    # ATT(0) per sex reported separately
    att0F = att_at("F", 0)
    att0M = att_at("M", 0)
    d0_f = tables["F"][tables["F"].event == 0]
    d0_m = tables["M"][tables["M"].event == 0]

    results.update({
        "gate": gate,
        "samples": {k: {"n_countries": v["n_countries"], "n_treated": v["n_treated"],
                        "treated": v["treated"], "treated_missing": v["treated_missing"],
                        "n_controls_at_event0": (int(v["ev"].loc[v["ev"].event == 0, "n_controls"].iloc[0])
                                                 if (v["ev"].event == 0).any() else None)}
                    for k, v in samples.items()},
        "female": {"att0": att0F,
                   "att0_ci": [float(d0_f.ci_lo.iloc[0]), float(d0_f.ci_hi.iloc[0])] if len(d0_f) else [None, None],
                   "n_treated_at_0": int(d0_f.n_treated.iloc[0]) if len(d0_f) else None,
                   "mean_post_1_6": float(np.mean([att_at('F', e) for e in used_events])) if used_events else None,
                   "event_table": tables["F"].to_dict(orient="records")},
        "male": {"att0": att0M,
                 "att0_ci": [float(d0_m.ci_lo.iloc[0]), float(d0_m.ci_hi.iloc[0])] if len(d0_m) else [None, None],
                 "n_treated_at_0": int(d0_m.n_treated.iloc[0]) if len(d0_m) else None,
                 "mean_post_1_6": float(np.mean([att_at('M', e) for e in used_events])) if used_events else None,
                 "event_table": tables["M"].to_dict(orient="records")},
        "difference": {"primary_statistic": "D = mean_{e=+1..+6} ATT_F(e) - mean_{e=+1..+6} ATT_M(e)",
                       "D": D, "D_ci95": D_ci, "n_events_used": used_events,
                       "n_boot_reps_used": len(reps),
                       "ci_excludes_zero": ci_excludes_zero,
                       "sign": (None if not np.isfinite(D) else ("female_higher" if D > 0 else "male_higher" if D < 0 else "zero")),
                       "event_table": pd.DataFrame(rows).to_dict(orient="records")},
        "bootstrap_universe_countries": len(draws_universe),
        "bootstrap_note": ("paired: replicate i draws countries with replacement from the union of F/M country sets "
                           "using numpy.random.default_rng(20261125+i); the same draw builds both sexes' panels"),
        "gate_assessment": ("PASS: sex split interpreted (prereg A5)" if gate_pass
                            else "FAIL: sex-split estimates are diagnostic only and no gender conclusion is drawn (prereg A5)"),
    })
    json.dump(results, open(os.path.join(RES, "gender_split_results.json"), "w"), indent=1, default=str)
    print(json.dumps({k: results[k] for k in ("gate", "difference")}, indent=1, default=str))
    print("\nFEMALE\n", tables["F"].to_string(index=False))
    print("\nMALE\n", tables["M"].to_string(index=False))
    print("\nDIFF\n", pd.DataFrame(rows).to_string(index=False))
    print("\nwrote", RES)


if __name__ == "__main__":
    main()
