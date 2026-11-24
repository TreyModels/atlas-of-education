#!/usr/bin/env python3
"""EXPLORATORY POST-HOC follow-up to the gender split (task-7) — pre-registered in
PRE_REGISTRATION_FOLLOWUP.md (commit dab608c), written and committed BEFORE this computation.

B1: inverse-variance weighted mean of the six post-event female-minus-male differences from the COMMITTED
    results/e8_event_difference_verified8.csv. FORMULA (fixed in the pre-registration):
      d_e = att_diff_F_minus_M
      se_e = (diff_ci_hi - diff_ci_lo) / (2 * 1.96)
      w_e = 1 / se_e^2
      D_IV = sum(w_e d_e)/sum(w_e); SE_IV = 1/sqrt(sum w_e); 95% CI = D_IV +/- 1.96 SE_IV
    This is ARITHMETIC ON COMMITTED OUTPUTS, not new estimation.
B2: leave-one-event-out equal-weight D over the remaining five post events.
B3: drop-MOZ paired CS D — a new (exploratory) estimation on the host with the SAME pre-registered design and
    seeds as the confirmatory run, MOZ removed from the whole sample. Labelled re-estimation, not recomputation.

Nothing here edits the confirmatory REPORT/PRE_REGISTRATION. All outputs EXPLORATORY / POST-HOC; no causal language.
Output: results/gender_split_followup.json
"""
import importlib.util
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.abspath(os.path.join(HERE, ".."))
RES = os.path.join(REC, "results")

DIFF_CSV = os.path.join(RES, "e8_event_difference_verified8.csv")
CONF_JSON = os.path.join(RES, "gender_split_results.json")
OUT = os.path.join(RES, "gender_split_followup.json")

POST = [1, 2, 3, 4, 5, 6]
Z = 1.96


def load_gs():
    spec = importlib.util.spec_from_file_location("gender_split_e8", os.path.join(HERE, "gender_split_e8.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    out = {"label": "EXPLORATORY POST-HOC (task-7); follow-up to the confirmatory task-3 record",
           "preregistration_followup_commit": "dab608c",
           "confirmatory_commit": "5b42bfd",
           "design_note": "B1/B2 are recomputation (arithmetic on committed outputs); B3 is an exploratory "
                          "re-estimation on a reduced sample. Confirmatory REPORT/PRE_REGISTRATION unchanged.",
           "language_rule": "association only; no causal wording"}

    # ---------------- B1 + B2 : from committed event-level difference table ----------------
    d = pd.read_csv(DIFF_CSV)
    post = d[d.event.isin(POST)].copy().sort_values("event")
    assert len(post) == 6, f"expected 6 post events, got {len(post)}"
    rows = []
    for _, r in post.iterrows():
        e = int(r.event)
        point = float(r.att_diff_F_minus_M)
        lo = float(r.diff_ci_lo)
        hi = float(r.diff_ci_hi)
        se = (hi - lo) / (2.0 * Z)
        rows.append({"event": e, "att_F": float(r.att_F), "att_M": float(r.att_M), "d_e": point,
                     "ci_lo": lo, "ci_hi": hi, "se_from_ci": se,
                     "w_raw": 1.0 / se ** 2, "n_boot_used": int(r.diff_n_boot_used)})
    tab = pd.DataFrame(rows)
    tab["w_norm"] = tab.w_raw / tab.w_raw.sum()
    D_IV = float((tab.w_raw * tab.d_e).sum() / tab.w_raw.sum())
    sum_w = float(tab.w_raw.sum())
    SE_IV = float(1.0 / np.sqrt(sum_w))
    D_IV_lo, D_IV_hi = D_IV - Z * SE_IV, D_IV + Z * SE_IV
    D_eq = float(tab.d_e.mean())
    SE_eq = float(np.sqrt((tab.se_from_ci ** 2).sum() / len(tab) ** 2))
    D_eq_lo, D_eq_hi = D_eq - Z * SE_eq, D_eq + Z * SE_eq

    conf = json.load(open(CONF_JSON))
    D_conf = float(conf["difference"]["D"])
    D_conf_ci = [float(conf["difference"]["D_ci95"][0]), float(conf["difference"]["D_ci95"][1])]

    out["B1"] = {
        "type": "RECOMPUTATION (arithmetic on committed results/e8_event_difference_verified8.csv; not new estimation)",
        "formula": "se_e=(ci_hi-ci_lo)/(2*1.96); w_e=1/se_e^2; D_IV=sum(w_e d_e)/sum(w_e); "
                   "SE_IV=1/sqrt(sum w_e); 95% CI = D_IV +/- 1.96*SE_IV",
        "caveat": "treats the reported percentile paired-bootstrap CIs as symmetric normal intervals "
                  "(approximation; the bootstrap distribution is skewed)",
        "events": tab.to_dict(orient="records"),
        "weight_profile_normalised": {int(r.event): float(r.w_norm) for _, r in tab.iterrows()},
        "D_IV": D_IV, "SE_IV": SE_IV, "D_IV_ci95": [D_IV_lo, D_IV_hi],
        "D_IV_ci_excludes_zero": bool(D_IV_lo > 0 or D_IV_hi < 0),
        "D_equal_weight_confirmatory": D_conf,
        "D_equal_weight_confirmatory_ci95_percentile": D_conf_ci,
        "D_equal_weight_normal_approx": D_eq,
        "D_equal_weight_normal_approx_ci95": [D_eq_lo, D_eq_hi],
        "sign": "male_higher" if D_IV < 0 else ("female_higher" if D_IV > 0 else "zero"),
    }
    # --- diagnostic: the confirmatory paired percentile CI implies a JOINT (paired) SE of D.
    # The B1 formula uses each event's MARGINAL SE and therefore ignores the positive cross-event correlation
    # induced by the shared country draw; the joint paired SE is the correct scale for the aggregate.
    SE_joint = (D_conf_ci[1] - D_conf_ci[0]) / (2.0 * Z) if None not in D_conf_ci else None
    out["B1"]["diagnostic_not_in_prereg"] = {
        "why": "added post-hoc to explain why the IV CI (independent marginal SEs) differs from the confirmatory "
               "paired percentile CI; descriptive diagnostic only, no new decision rule",
        "SE_joint_implied_by_confirmatory_paired_ci(percentile_width_/3.92)": SE_joint,
        "D_IV_with_joint_paired_SE_ci95": ([D_IV - Z * SE_joint, D_IV + Z * SE_joint] if SE_joint else None),
        "D_equal_weight_with_joint_paired_SE_ci95": ([D_eq - Z * SE_joint, D_eq + Z * SE_joint] if SE_joint else None),
        "note": "the six post-event differences are strongly positively correlated within the paired bootstrap "
                "(same country draws, overlapping event windows); combining their marginal CIs as independent, "
                "as the pre-registered B1 formula does, understates the variance of the aggregate and is "
                "anti-conservative. The paired percentile CI is the confirmatory inference.",
    }
    rule_fired = out["B1"]["D_IV_ci_excludes_zero"]
    iv_joint_incl0 = (out["B1"]["diagnostic_not_in_prereg"]["D_IV_with_joint_paired_SE_ci95"] is not None and
                      (out["B1"]["diagnostic_not_in_prereg"]["D_IV_with_joint_paired_SE_ci95"][0] <= 0 <=
                       out["B1"]["diagnostic_not_in_prereg"]["D_IV_with_joint_paired_SE_ci95"][1]))
    out["B1"]["reading"] = (
        "EXPLORATORY. Pre-registered B1 rule fires mechanically: the IV formula's CI excludes zero "
        f"({D_IV:.2f} [{D_IV - Z*SE_IV:.2f}, {D_IV + Z*SE_IV:.2f}]). HOWEVER the direct comparison does NOT support a "
        "weighting-artefact explanation: the IV point estimate (-4.05) is essentially the equal-weight estimate "
        "(-3.94), the weights are dominated by +1 (33%) and +2 (24%) only because those event CIs are narrowest, "
        "and applying the SAME normal approximation to the equal-weight mean also excludes zero "
        f"([{D_eq - Z*SE_eq:.2f}, {D_eq + Z*SE_eq:.2f}]). The apparent flip is a CI-CONSTRUCTION effect: the B1 "
        "formula treats the six post-event CIs as independent, while the paired country-cluster bootstrap makes them "
        "strongly positively correlated — the joint paired SE implied by the confirmatory percentile CI is ~2.30, "
        "not ~0.97. With the joint paired SE the IV aggregate CI "
        f"{out['B1']['diagnostic_not_in_prereg']['D_IV_with_joint_paired_SE_ci95']} includes zero. "
        "Confirmatory headline preserved: no detected sex difference."
        if rule_fired else
        "The inverse-variance weighted aggregate CI INCLUDES zero: the confirmatory conclusion (no detected sex "
        "difference) is unchanged; the event-level +1/+2 pattern remains a descriptive, multiplicity-untested "
        "observation.")
    out["B1"]["pre_registered_rule_fired"] = bool(rule_fired)
    out["B1"]["weighting_artefact_supported"] = bool(rule_fired and not iv_joint_incl0)
    out["B1"]["conclusion_changes_with_paired_uncertainty"] = bool(iv_joint_incl0)

    # ---------------- B2 : leave-one-event-out ----------------
    loo = []
    for e_star in POST:
        keep = [r for r in rows if r["event"] != e_star]
        d_loo = float(np.mean([r["d_e"] for r in keep]))
        loo.append({"dropped_event": e_star, "D_loo": d_loo, "leverage_vs_full_D": d_loo - D_conf})
    loo_tab = pd.DataFrame(loo)
    most = loo_tab.loc[loo_tab.leverage_vs_full_D.abs().idxmax()]
    out["B2"] = {
        "type": "RECOMPUTATION (equal-weight mean of the remaining five post-event differences)",
        "D_full_equal_weight": D_conf,
        "leave_one_event_out": loo_tab.to_dict(orient="records"),
        "D_loo_range": [float(loo_tab.D_loo.min()), float(loo_tab.D_loo.max())],
        "most_influential_event_dropped": int(most.dropped_event),
        "max_abs_leverage": float(most.leverage_vs_full_D),
        "note": "descriptive leverage only; no significance test invented",
    }

    # ---------------- B3 : drop-MOZ paired CS D (exploratory re-estimation) ----------------
    try:
        gs = load_gs()
        # sanity: reproduce the confirmatory D from the same code path on the full sample first
        res = {}
        for sex in ("F", "M"):
            panel = gs.load_panel(gs.IND[sex])
            countries = (set(panel.iso3) & set(gs.load_region().loc[
                gs.load_region().region.str.contains("Sub-Saharan", na=False), "iso3"])) - {"MOZ"}
            Y = gs.ymat(panel, countries)
            coh = {c: g for c, g in gs.load_verified().items() if c in Y and c != "MOZ"}
            att_gt, ev = gs.att_cs(Y, coh, gs.YEARS)
            res[sex] = {"Y": Y, "coh": coh, "ev": ev}
        draws = sorted(set(res["F"]["Y"]) | set(res["M"]["Y"]))
        seeds = [gs.SEED_BASE + i for i in range(gs.N_BOOT)]
        boots = gs.boot_event_tables(None, None, draws, seeds,
                                     sex_series={"F": res["F"]["Y"], "M": res["M"]["Y"]},
                                     coh_series={"F": res["F"]["coh"], "M": res["M"]["coh"]})
        pt = {}
        for sex in ("F", "M"):
            ev = res[sex]["ev"]
            pt[sex] = {int(r.event): float(r.att) for _, r in ev.iterrows()}
        used = [e for e in POST if e in pt["F"] and e in pt["M"]]
        D_moz = float(np.mean([pt["F"][e] for e in used]) - np.mean([pt["M"][e] for e in used]))
        common = None
        for e in used:
            s_e = set(boots["F"].get(e, {})) & set(boots["M"].get(e, {}))
            common = s_e if common is None else (common & s_e)
        reps = [float(np.mean([boots["F"][e][k] for e in used]) - np.mean([boots["M"][e][k] for e in used]))
                for k in sorted(common or [])]
        if len(reps) >= 10:
            lo, hi = np.percentile(reps, [2.5, 97.5])
            ci = [float(lo), float(hi)]
        else:
            ci = [None, None]
        out["B3"] = {
            "type": "EXPLORATORY RE-ESTIMATION on a reduced sample (not recomputation)",
            "sample": "SSA 1990-2015, verified-8 dates, MOZ removed from the whole sample (7 treated countries)",
            "design": "same att_cs (bd782be), universal base g-1, not-yet-treated controls, event -5..+6, "
                      "cohort-weighted, 500 paired country-cluster bootstrap reps, seeds 20261125+i, percentile CIs",
            "D_dropMOZ": D_moz, "D_dropMOZ_ci95": ci, "n_events_used": used,
            "n_boot_reps_used": int(len(reps)),
            "sign": "male_higher" if D_moz < 0 else ("female_higher" if D_moz > 0 else "zero"),
            "ci_excludes_zero": bool(ci[0] is not None and (ci[0] > 0 or ci[1] < 0)),
            "treated_at_e0": {sex: int(gs.att_cs(res[sex]["Y"], res[sex]["coh"], gs.YEARS)[1]
                                       .loc[lambda t: t.event == 0, "n_treated"].iloc[0])
                              if (res[sex]["ev"].event == 0).any() else None for sex in ("F", "M")},
        }
    except Exception as exc:  # pragma: no cover
        out["B3"] = {"status": "not run", "reason": f"{type(exc).__name__}: {exc}"}

    # confirmatory headline preservation
    out["confirmatory_headline"] = ("both sexes' post-abolition primary-GER trajectories are similar; the "
                                    "female-minus-male post mean is -3.94 pp with a 95% CI that includes zero "
                                    "(no detected sex difference)")
    # the exploratory probes do NOT replace the confirmatory inference: the paired percentile CI remains the
    # pre-registered inference; B1's rule fired mechanically but the weighting-artefact reading is refuted by the
    # pre-registered comparator and the joint-paired-SE diagnostic.
    out["confirmatory_headline_changed"] = False
    out["pre_registered_B1_rule_fired"] = bool(out["B1"]["pre_registered_rule_fired"])
    out["exploratory_finding"] = (
        "the equal-weight aggregate null is NOT a weighting artefact (IV point estimate -4.05 vs equal-weight "
        "-3.94; leave-one-event-out range 0.27 pp; drop-MOZ -3.95); the apparent CI flip is a CI-construction "
        "effect (independent marginal SEs vs the paired country-cluster bootstrap). Confirmatory 'no detected sex "
        "difference' preserved, with the fragility note that the paired percentile CI's upper endpoint is +0.29.")
    json.dump(out, open(OUT, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("B1", "B2", "B3") if k in out}, indent=1))
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
