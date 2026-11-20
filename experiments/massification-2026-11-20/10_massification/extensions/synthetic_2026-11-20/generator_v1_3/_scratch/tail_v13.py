# ======================================================================================
# 9. V1.3 RUN, FROZEN CHECKS c1-c6, AND OUTPUTS
#    Scored exactly as shadow_module/PRE_DECLARATIONS.md sec.8 says. A FAIL is reported
#    as a FAIL; no threshold or parameter is ever adjusted to rescue one.
# ======================================================================================
C1_GAP = 0.10          # sec.8 c1: R doubling at g2 must raise D by >= +10.0 pp
C2_GAP = 0.02          # sec.8 c2: +25% on phi at g2 must raise D by >= +2.0 pp
C3_MAX_D0 = 0.025      # sec.8 c3(i)
C3_RATIO = 0.20        # sec.8 c3(ii)
C4A_LO, C4A_HI = 0.75, 0.95   # sec.8 c4a
C4B_GAP1, C4B_GAP2 = 0.10, 0.05  # sec.8 c4b
SAT_LO, SAT_HI = 0.05, 0.90      # DRY_RUN_PLAN.md sec.7.2 (pre-declared informative range)
DERIV_H = 1e-4                    # numerical step for the derivative components


def run_all(seed=SEED, beh=None, shadow=True, inputs=None, hosts=None):
    """v1.2 run with the shadow block layered on the gate/queue machinery.

    The RNG draws are unchanged from v1.2 (same stream, same order, same count), so the
    30 synthetic countries and their shocks are identical to the frozen v1.2 run.
    """
    beh = SHADOW_BEHAV if beh is None else beh
    inputs = shadow_inputs_named() if inputs is None else inputs
    S_phl, P_phl, coh_obs, ptr_obs, spend_obs = load_observed_phl_paths()
    rng = np.random.default_rng(seed)
    cps = apply_declared(draw_countries(rng))
    gnoise = rng.normal(0.0, P["g_noise_sd"], (T, N_C))
    hhnoise = rng.normal(0.0, P["hh_noise_sd"], (T, N_C))
    # Declared controlled comparisons (unchanged from v1.2).
    for j in (2,):
        gnoise[:, j] = gnoise[:, 1]; hhnoise[:, j] = hhnoise[:, 1]
    for j in (11, 12):
        gnoise[:, j] = gnoise[:, 10]; hhnoise[:, j] = hhnoise[:, 10]
    by_host = {}
    if shadow and hosts:
        for tname, hname in hosts.items():
            by_host[hname] = tname
    results = []
    for i, cp in enumerate(cps):
        S = cohort_path(cp, S_phl)
        Pop = pop_path(cp, P_phl)
        sh_in = None
        if cp["name"] in by_host:
            tname = by_host[cp["name"]]
            sh_in = dict(inputs[tname], type=tname)
        results.append(simulate_country(cp, gnoise[:, i], hhnoise[:, i], S, Pop,
                                        sh_in=sh_in, beh=beh))
    return results, ptr_obs, spend_obs, S_phl, P_phl


def required_R_for_D(beh, ci, g, V, dpi, target, lo_lnR=0.0, hi_lnR=6.0):
    """NOT-SCORED diagnostic: the gate pressure a target demand would need, all else fixed.

    D is strictly increasing in ln R (b_Z > 0), so bisection is exact to machine precision.
    """
    for _ in range(200):
        mid = 0.5 * (lo_lnR + hi_lnR)
        D, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"],
                                   math.exp(mid), V, dpi, g)
        if D < target:
            lo_lnR = mid
        else:
            hi_lnR = mid
    return math.exp(0.5 * (lo_lnR + hi_lnR))


def shadow_world(res, hosts, inputs, beh):
    """Per-type view of the stored run: demand, R, D* and the declared inputs."""
    by = {r["cp"]["name"]: r for r in res}
    w = {}
    for tname in TYPE_ORDER:
        r = by[hosts[tname]]
        ci = dict(inputs[tname])
        D = r["D_sh"]
        dstar = np.array([sum(ci["nu"][g] * D[g, t] for g in (1, 2, 3)) for t in range(T)])
        w[tname] = dict(r=r, ci=ci, host=hosts[tname], D=D, Dstar=dstar,
                        R=r["R_sh"], V=r["V_sh"], dpi=r["dpi_sh"], pi0=r["pi0_sh"],
                        pi1=r["pi1_sh"], Pi=r["Pi_sh"], p=r["p_sh"], Q=r["Q_sh"],
                        kappa=r["kappa_sh"], ratio=r["ratio_sh"], S=r["S_sh"],
                        cand=r["cand_sh"], cap=r["cap_sh"], adv=r["adv_sh"],
                        exposure=float(sum(ci["nu"].values())))
    return w


def build_panel_v13(results, hosts, inputs):
    """v1.2 panel rows (identical objects) + shadow columns for the designated types."""
    rows = build_panel(results)
    by = {r["cp"]["name"]: r for r in results}
    host_of = {h: t for t, h in hosts.items()}
    gate_of_level = {0: 0, 1: 1, 2: 2, 3: 3}
    for row in rows:
        cname = row["country"]
        trow = int(row["year"]) - YEAR_START
        L = LEVELS.index(row["level"])
        g = gate_of_level[L]
        row["shadow_type"] = host_of.get(cname, "")
        row["shadow_gate_status"] = "designated" if cname in host_of else "not_designated"
        row["shadow_gate"] = GATE_NAMES[g]
        r = by[cname]
        if cname in host_of:
            tname = host_of[cname]
            ci = inputs[tname]
            row["D_gate"] = float(r["D_sh"][g, trow])
            row["D_cohort"] = float(sum(ci["nu"][gg] * r["D_sh"][gg, trow]
                                        for gg in (1, 2, 3)))
            row["cohort_exposure"] = float(sum(ci["nu"].values()))
            row["R"] = float(r["R_sh"][g, trow])
            row["ln_R"] = float(math.log(max(r["R_sh"][g, trow], 1e-12)))
            row["Q_gate"] = float(r["Q_sh"][g, trow])
            row["pi0"] = float(r["pi0_sh"][g, trow])
            row["pi1"] = float(r["pi1_sh"][g, trow])
            row["Pi"] = float(r["Pi_sh"][g, trow])
            row["kappa"] = float(r["kappa_sh"][g, trow])
            row["V"] = float(r["V_sh"][g, trow])
            row["s_g"] = float(ci["s"])
            row["spend_share"] = float(r["S_sh"][g, trow])
            row["Pi_over_pi0"] = float(r["ratio_sh"][g, trow])
            for q in range(5):
                row["p_q%d" % (q + 1)] = float(r["p_sh"][g, q, trow])
        else:
            for k in ("D_gate", "D_cohort", "cohort_exposure", "R", "ln_R", "Q_gate",
                      "pi0", "pi1", "Pi", "kappa", "V", "s_g", "spend_share",
                      "Pi_over_pi0", "p_q1", "p_q2", "p_q3", "p_q4", "p_q5"):
                row[k] = ""
    return rows


def write_panel_v13(rows, path):
    cols = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v)
                        for k, v in row.items()})


# --------------------------------------------------------------------------------------
# check helpers
# --------------------------------------------------------------------------------------
def _f(x):
    return f"{x:.10g}" if isinstance(x, float) else str(x)


def _verdict_fail(cond):
    return "PASS" if cond else "FAIL"


def check_c1(w, beh):
    """c1 gate pressure: sign in every scored cell + R-doubling at g2 >= +10 pp."""
    fails = []
    n_scored = n_sat = 0
    min_deriv = float("inf")
    max_abs_err = 0.0
    for tname in TYPE_ORDER:
        d = w[tname]; ci = d["ci"]
        for g in (1, 2, 3, 4):
            for t in range(T):
                D = float(d["D"][g, t])
                if not (SAT_LO <= D <= SAT_HI):
                    n_sat += 1
                    continue
                n_scored += 1
                R = float(d["R"][g, t]); V = float(d["V"][g, t]); dpi = float(d["dpi"][g, t])
                Dp, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g,
                                            lnR_shift=+DERIV_H)
                Dm, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g,
                                            lnR_shift=-DERIV_H)
                der = (Dp - Dm) / (2.0 * DERIV_H)
                ana = beh["b_Z"] * sum(wq * pq * (1.0 - pq)
                                       for wq, pq in zip(beh["omega"], d["p"][g, :, t]))
                max_abs_err = max(max_abs_err, abs(der - ana))
                if der < 0.0:
                    fails.append((tname, g, int(YEARS[t]), der))
                min_deriv = min(min_deriv, der)
    gaps = {}
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    for tname in TYPE_ORDER:
        d = w[tname]; ci = d["ci"]
        R = float(d["R"][2, i20]); V = float(d["V"][2, i20]); dpi = float(d["dpi"][2, i20])
        D2, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], 2.0 * R, V, dpi, 2)
        gaps[tname] = float(D2 - d["D"][2, i20])
    gap_ok = all(v >= C1_GAP for v in gaps.values())
    sign_ok = (len(fails) == 0) and n_scored > 0
    sub = {
        "c1_i_sign_nonneg_all_scored_cells": (sign_ok, f"{n_scored} scored, {n_sat} saturated/NOT-SCORED, "
                                                         f"min dD/dlnR = {_f(min_deriv)}"),
        "c1_i_cells_scored": (None, n_scored),
        "c1_i_cells_saturated_not_scored": (None, n_sat),
        "c1_i_max_abs_numeric_minus_analytic": (None, max_abs_err),
    }
    for tname in TYPE_ORDER:
        sub["c1_ii_R_doubled_g2_gap_" + tname] = (gaps[tname] >= C1_GAP, gaps[tname])
    ok = sign_ok and gap_ok
    return dict(
        check_id="c1",
        expected_pattern=("dD/dlnR >= 0 in every scored (c,g,t) cell AND R->2R at g2 (t*=2020) raises D "
                          "by >= +10.0 pp in all three country types."),
        synthetic_value=(f"sign: {n_scored} scored cells, min dD/dlnR {min_deriv:+.4g} "
                         f"({n_sat} saturated cells NOT-SCORED per DRY_RUN_PLAN 7.2); "
                         f"R-doubling gap at g2: " +
                         ", ".join(f"{k} {v*100:+.2f} pp" for k, v in gaps.items())),
        verdict=_verdict_fail(ok), note=(
            "Numerical central difference in ln R (h=1e-4); the analytic value b_Z*sum(w p(1-p)) is "
            "reported beside it (max |numeric-analytic| = %.3g). Saturated cells (D outside [0.05,0.90]) "
            "are NOT-SCORED as pre-declared in DRY_RUN_PLAN sec.7.2, not counted as passes." % max_abs_err),
        sub=sub, fails=fails, gaps=gaps, n_scored=n_scored, n_sat=n_sat)


def check_c2(w, beh):
    """c2 expected returns: sign in every scored cell + V->1.25V at g2 >= +2.0 pp."""
    fails = []
    n_scored = n_sat = 0
    min_deriv = float("inf")
    max_abs_err = 0.0
    for tname in TYPE_ORDER:
        d = w[tname]; ci = d["ci"]
        for g in (1, 2, 3, 4):
            for t in range(T):
                D = float(d["D"][g, t])
                if not (SAT_LO <= D <= SAT_HI):
                    n_sat += 1
                    continue
                n_scored += 1
                V = float(d["V"][g, t])
                u = math.log1p(max(V, 0.0))
                R = float(d["R"][g, t]); dpi = float(d["dpi"][g, t])
                if u <= 1e-12:
                    continue
                Vp = math.expm1((1.0 + DERIV_H) * u)
                Vm = math.expm1(max(1e-12, (1.0 - DERIV_H)) * u)
                Dp, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g,
                                            V_mult=Vp / V)
                Dm, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, g,
                                            V_mult=Vm / V)
                # the perturbation is +-(h*u) in u = ln(1+V); divide by the actual shift
                der = (Dp - Dm) / (2.0 * DERIV_H * u)
                ana = beh["b_V"] * sum(wq * pq * (1.0 - pq)
                                       for wq, pq in zip(beh["omega"], d["p"][g, :, t]))
                max_abs_err = max(max_abs_err, abs(der - ana))
                if der < 0.0:
                    fails.append((tname, g, int(YEARS[t]), der))
                min_deriv = min(min_deriv, der)
    gaps = {}
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    for tname in TYPE_ORDER:
        d = w[tname]; ci = d["ci"]
        R = float(d["R"][2, i20]); V = float(d["V"][2, i20]); dpi = float(d["dpi"][2, i20])
        D25, _, _, _ = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"], R, V, dpi, 2,
                                     V_mult=1.25)
        gaps[tname] = float(D25 - d["D"][2, i20])
    gap_ok = all(v >= C2_GAP for v in gaps.values())
    sign_ok = (len(fails) == 0) and n_scored > 0
    sub = {
        "c2_i_sign_nonneg_all_scored_cells": (sign_ok, f"{n_scored} scored, {n_sat} saturated/NOT-SCORED, "
                                                         f"min dD/dln(1+V) = {_f(min_deriv)}"),
        "c2_i_cells_scored": (None, n_scored),
        "c2_i_cells_saturated_not_scored": (None, n_sat),
        "c2_i_max_abs_numeric_minus_analytic": (None, max_abs_err),
    }
    for tname in TYPE_ORDER:
        sub["c2_ii_V_plus25pct_g2_gap_" + tname] = (gaps[tname] >= C2_GAP, gaps[tname])
    ok = sign_ok and gap_ok
    return dict(
        check_id="c2",
        expected_pattern=("dD/dln(1+V) >= 0 in every scored cell AND V->1.25V (+25% on phi) at g2 "
                          "(t*=2020) raises D by >= +2.0 pp in all three country types."),
        synthetic_value=(f"sign: {n_scored} scored cells, min dD/dln(1+V) {min_deriv:+.4g} "
                         f"({n_sat} saturated NOT-SCORED); +25% phi gap at g2: " +
                         ", ".join(f"{k} {v*100:+.2f} pp" for k, v in gaps.items())),
        verdict=_verdict_fail(ok), note=(
            "Numerical central difference in ln(1+V) (h=1e-4); analytic b_V*sum(w p(1-p)) beside it "
            "(max |numeric-analytic| = %.3g). The return channel is a declared prior (PARAMETERS.csv B04); "
            "this is a comparative static, not an estimate." % max_abs_err),
        sub=sub, fails=fails, gaps=gaps, n_scored=n_scored, n_sat=n_sat)


def check_c3(w, beh):
    """c3 near-zero pre-gate demand (STRUCTURAL consistency check, not a prediction)."""
    d0 = []; ratios = []
    worst_d0 = (-1.0, "", 0); worst_ratio = (-1.0, "", 0)
    for tname in TYPE_ORDER:
        d = w[tname]
        for t in range(T):
            v = float(d["D"][0, t]); d0.append(v)
            if v > worst_d0[0]:
                worst_d0 = (v, tname, int(YEARS[t]))
            d1 = float(d["D"][1, t])
            if d1 > 1e-12:
                rt = v / d1
                ratios.append(rt)
                if rt > worst_ratio[0]:
                    worst_ratio = (rt, tname, int(YEARS[t]))
    c1ok = worst_d0[0] <= C3_MAX_D0
    c2ok = (len(ratios) == len(d0)) and worst_ratio[0] <= C3_RATIO
    sub = {
        "c3_i_max_D_g0_le_0.025": (c1ok, f"{worst_d0[0]:.6f} at {worst_d0[1]} {worst_d0[2]}"),
        "c3_ii_max_Dg0_over_Dg1_le_0.20": (c2ok, f"{worst_ratio[0]:.6f} at {worst_ratio[1]} {worst_ratio[2]}"),
        "c3_country_years_checked": (None, len(d0)),
    }
    ok = c1ok and c2ok
    return dict(
        check_id="c3",
        expected_pattern=("D(g0) <= 0.025 in every country-year AND D(g0) <= 0.20*D(g1) in every "
                          "country-year. DECLARED STRUCTURAL / CONSISTENCY CHECK, not an empirical "
                          "prediction (PRE_DECLARATIONS.md sec.8 c3 + S1 note item 3)."),
        synthetic_value=(f"max D(g0) = {worst_d0[0]:.6f} at {worst_d0[1]} {worst_d0[2]} (<= 0.025); "
                         f"max D(g0)/D(g1) = {worst_ratio[0]:.6f} at {worst_ratio[1]} "
                         f"{worst_ratio[2]} (<= 0.20)"),
        verdict=_verdict_fail(ok), note=(
            "Structural, not empirical: V(g0)=0 by definition, delta_0=0.02, kappa(g0)=1, and the "
            "pre-gate state is the primary seat/admission ratio. Observed primary-stage tutoring "
            "(PHL 23.8%, KHM 41.3%) is OUT OF THIS MODULE'S SCOPE and is not explained here."),
        sub=sub)


def check_c4a(w, beh):
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    v = float(w["SYN_HKG_LIKE"]["D"][2, i20])
    ok = (C4A_LO <= v <= C4A_HI)
    path = [float(w["SYN_HKG_LIKE"]["D"][2, t]) for t in range(T)]
    return dict(
        check_id="c4a",
        expected_pattern="D_HKG_like(g2, t*=2020) in [0.75, 0.95] (85% +/- 10 pp, widened for source caveats).",
        synthetic_value=f"D_HKG_like(g2, 2020) = {v:.6f} (band [0.75, 0.95]); 1970-2025 range "
                        f"[{min(path):.4f}, {max(path):.4f}]",
        verdict=_verdict_fail(ok), note=(
            "The 85% anchor is senior-secondary-only, second-hand and of low survey robustness "
            "(PRE_DECLARATIONS.md sec.7); the band is wide on purpose. This is a reproduction of a "
            "declared level, not a validation."),
        sub={"c4a_D_HKG_g2_2020_in_band": (ok, v),
             "c4a_D_HKG_g2_path_min": (None, min(path)),
             "c4a_D_HKG_g2_path_max": (None, max(path))})


def check_c4b(w, beh):
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    ds = {k: float(w[k]["Dstar"][i20]) for k in TYPE_ORDER}
    g1 = ds["SYN_HKG_LIKE"] - ds["SYN_PHL_LIKE"]
    g2 = ds["SYN_PHL_LIKE"] - ds["SYN_KHM_LIKE"]
    ok = (g1 >= C4B_GAP1) and (g2 >= C4B_GAP2)
    i20_ = DECLARED_COMPARISON_YEAR - YEAR_START
    gd = "; ".join("%s g1..g3 = %.4f/%.4f/%.4f, nu = %.2f/%.2f/%.2f, D* = %.4f" % (
        k.replace("SYN_", "").replace("_LIKE", ""),
        float(w[k]["D"][1, i20_]), float(w[k]["D"][2, i20_]), float(w[k]["D"][3, i20_]),
        w[k]["ci"]["nu"][1], w[k]["ci"]["nu"][2], w[k]["ci"]["nu"][3],
        float(w[k]["Dstar"][i20_])) for k in TYPE_ORDER)
    sub = {
        "c4b_channel_decomposition_2020": (None, gd),
        "c4b_gap_Dstar_HKG_minus_PHL_ge_0.10": (g1 >= C4B_GAP1, g1),
        "c4b_gap_Dstar_PHL_minus_KHM_ge_0.05": (g2 >= C4B_GAP2, g2),
        "c4b_Dstar_HKG_2020": (None, ds["SYN_HKG_LIKE"]),
        "c4b_Dstar_PHL_2020": (None, ds["SYN_PHL_LIKE"]),
        "c4b_Dstar_KHM_2020": (None, ds["SYN_KHM_LIKE"]),
    }
    return dict(
        check_id="c4b",
        expected_pattern=("D*_HKG - D*_PHL >= 0.10 AND D*_PHL - D*_KHM >= 0.05 at t*=2020, on the "
                          "cohort-incidence statistic D* = sum_g nu_g D_g (g1-g3)."),
        synthetic_value=(f"D*(2020): HKG {ds['SYN_HKG_LIKE']:.4f}, PHL {ds['SYN_PHL_LIKE']:.4f}, "
                         f"KHM {ds['SYN_KHM_LIKE']:.4f}; gaps {g1:+.4f} and {g2:+.4f}"),
        verdict=_verdict_fail(ok), note=(
            "DECLARED SYNTHETIC-REPRODUCTION CHECK (S1 note item 2): the on-disk headline rates "
            "(HKG 85% senior-secondary, PHL 46.5% all-basic, KHM 68.4% two-school Grade-9) do NOT "
            "establish this ordering; they are different stages and sampling frames. D* is driven by "
            "observed out-of-school exposure (nu), so a PASS would say the declared exposure weights "
            "reproduce the ordering, not that any country's incidence orders that way."),
        sub=sub, ds=ds, gaps=(g1, g2))


def shadow_code_audit():
    """c4c: code inspection for any country-specific behavioural parameter."""
    fns = [shadow_demand, credential_value, gate_state, gate_numbers,
           shadow_quintile_income, shadow_block]
    src = "".join(inspect.getsource(f) for f in fns)
    forbidden = ["SYN_HKG_LIKE", "SYN_PHL_LIKE", "SYN_KHM_LIKE", "SYN00", "HKG", "PHL",
                 "KHM", "cp[", "country ==", "name ==", "phi_dict", "delta_HKG"]
    found = [t for t in forbidden if t in src]
    beh_keys = set(SHADOW_BEHAV.keys())
    country_keys = [k for k in beh_keys
                    if k in ("SYN_HKG_LIKE", "SYN_PHL_LIKE", "SYN_KHM_LIKE", "HKG", "PHL", "KHM")]
    delta_keys = sorted(SHADOW_BEHAV["delta"].keys())
    input_keys = sorted({kk for v in SHADOW_COUNTRY_INPUTS.values() for kk in v})
    behavioural = {"a_0", "a_g", "b_Z", "b_V", "b_D", "b_y", "b_F", "delta", "w_Q", "w_pi",
                   "w_kappa", "r_EAP", "H", "dS", "omega", "zq"}
    extra_beh = sorted(beh_keys - behavioural)
    info = dict(functions_audited=[f.__name__ for f in fns],
                source_lines=len(src.strip().splitlines()),
                forbidden_tokens_found=found,
                behavioural_keys=sorted(beh_keys),
                behavioural_keys_not_declared=extra_beh,
                country_specific_behavioural_keys=country_keys,
                delta_keys=delta_keys,
                country_input_keys=input_keys,
                country_types=sorted(SHADOW_COUNTRY_INPUTS.keys()))
    ok = (not found and not country_keys and not extra_beh
          and delta_keys == [0, 1, 2, 3, 4]
          and info["country_input_keys"] == ["nu", "oos_upper", "phi", "s", "sigma"])
    return ok, info


def check_c4c(w, beh):
    ok, info = shadow_code_audit()
    return dict(
        check_id="c4c",
        expected_pattern=("Code inspection: NO country-specific value of a_g, b_Z, b_V, b_D, b_y, b_F, "
                          "delta_g. Every country-varying quantity is in the declared input table and in "
                          "results/shadow_country_inputs_audit.csv. If any exists, c4 is VOID."),
        synthetic_value=(f"behavioural keys {len(info['behavioural_keys'])} (gate-indexed only), "
                         f"country-specific behavioural keys: {len(info['country_specific_behavioural_keys'])}, "
                         f"forbidden tokens in behavioural functions: {len(info['forbidden_tokens_found'])}, "
                         f"declared country inputs: {info['country_input_keys']}"),
        verdict="PASS" if ok else "FAIL",
        note=("VOID rule (sec.8 c4c): a single country-specific behavioural parameter makes the whole of "
              "c4 VOID. The host-country assignment (which v1.2 country carries which declared bundle) is "
              "DATA, is recorded in the audit CSV, and is not a behavioural coefficient."),
        sub={"c4c_no_country_specific_behavioural_coefficient": (ok, "none") if ok else (
            False, ",".join(info["forbidden_tokens_found"] + info["country_specific_behavioural_keys"]))},
        info=info)


def check_c5(w, beh):
    """c5 identities on every scored row (all 3 types x 5 gates x 56 years)."""
    fail = []
    worst = dict(p_lo=1.0, p_hi=0.0, D_lo=1.0, D_hi=0.0, omega=abs(sum(beh["omega"]) - 1.0),
                 pi_lo=1.0, pi_Pi_lo=1.0, Pi_minus_pi0=1e18, S_lo=1e18, dstar_over_expo=0.0,
                 tut_over_cohort_g13=0.0, tut_over_cand_g4=0.0, d0_minus_d1=-1e18, nan=0)
    for tname in TYPE_ORDER:
        d = w[tname]
        for g in GATES:
            for t in range(T):
                for q in range(5):
                    pq = float(d["p"][g, q, t])
                    worst["p_lo"] = min(worst["p_lo"], pq); worst["p_hi"] = max(worst["p_hi"], pq)
                    if not (0.0 <= pq <= 1.0) or pq != pq or pq in (float("inf"), float("-inf")):
                        fail.append((tname, g, int(YEARS[t]), "p_q", pq))
                D = float(d["D"][g, t]); pi0 = float(d["pi0"][g, t])
                pi1 = float(d["pi1"][g, t]); Pi = float(d["Pi"][g, t])
                S = float(d["S"][g, t]); R = float(d["R"][g, t]); Q = float(d["Q"][g, t])
                worst["D_lo"] = min(worst["D_lo"], D); worst["D_hi"] = max(worst["D_hi"], D)
                worst["pi_lo"] = min(worst["pi_lo"], pi0, pi1)
                worst["pi_Pi_lo"] = min(worst["pi_Pi_lo"], Pi)
                worst["Pi_minus_pi0"] = min(worst["Pi_minus_pi0"], Pi - pi0)
                worst["S_lo"] = min(worst["S_lo"], S)
                if not (0.0 <= D <= 1.0):
                    fail.append((tname, g, int(YEARS[t]), "D", D))
                if not (0.01 <= pi0 <= 1.0 and 0.01 <= pi1 <= 1.0 and 0.01 <= Pi <= 1.0):
                    fail.append((tname, g, int(YEARS[t]), "pi_bounds", (pi0, pi1, Pi)))
                if Pi < pi0 - 1e-12:
                    fail.append((tname, g, int(YEARS[t]), "Pi_lt_pi0", (Pi, pi0)))
                if S < 0.0:
                    fail.append((tname, g, int(YEARS[t]), "S_neg", S))
                if not all(np.isfinite([D, pi0, pi1, Pi, S, R, Q])):
                    worst["nan"] += 1
                    fail.append((tname, g, int(YEARS[t]), "nonfinite", None))
    # D* <= exposure, and the tutored-headcount bound
    for tname in TYPE_ORDER:
        d = w[tname]
        for t in range(T):
            ds = float(d["Dstar"][t])
            worst["dstar_over_expo"] = max(worst["dstar_over_expo"], ds / max(d["exposure"], 1e-12))
            if ds > d["exposure"] + 1e-12:
                fail.append((tname, 0, int(YEARS[t]), "Dstar_gt_exposure", ds))
            for g, srcL in ((1, 0), (2, 1), (3, 2)):
                tut = float(d["D"][g, t]) * float(d["cand"][g, t])
                bnd = float(d["r"]["C"][srcL, t])
                rt = tut / max(bnd, 1e-9)
                worst["tut_over_cohort_g13"] = max(worst["tut_over_cohort_g13"], rt)
                if tut > bnd * (1.0 + 1e-12):
                    fail.append((tname, g, int(YEARS[t]), "tutored_gt_cohort", rt))
            tut4 = float(d["D"][4, t]) * float(d["cand"][4, t])
            rt4 = tut4 / max(float(d["cand"][4, t]), 1e-9)
            worst["tut_over_cand_g4"] = max(worst["tut_over_cand_g4"], rt4)
            if tut4 > float(d["cand"][4, t]) * (1.0 + 1e-12):
                fail.append((tname, 4, int(YEARS[t]), "tutored_gt_candidates", rt4))
            worst["d0_minus_d1"] = max(worst["d0_minus_d1"],
                                       float(d["D"][0, t]) - float(d["D"][1, t]))
            if not float(d["D"][0, t]) < float(d["D"][1, t]):
                fail.append((tname, 0, int(YEARS[t]), "Dg0_ge_Dg1", float(d["D"][0, t])))
    omega_ok = abs(sum(beh["omega"]) - 1.0) <= 1e-12
    ok = (len(fail) == 0) and omega_ok
    sub = {
        "c5_p_and_D_in_0_1": (all(f[3] not in ("p_q", "D") for f in fail),
                              f"p in [{worst['p_lo']:.4g},{worst['p_hi']:.4g}], "
                              f"D in [{worst['D_lo']:.4g},{worst['D_hi']:.4g}]"),
        "c5_sum_omega_eq_1": (omega_ok, sum(beh["omega"])),
        "c5_pi0_pi1_Pi_in_bounds": (all(f[3] != "pi_bounds" for f in fail),
                                    f"min pi = {worst['pi_lo']:.6g}"),
        "c5_Pi_ge_pi0": (all(f[3] != "Pi_lt_pi0" for f in fail), worst["Pi_minus_pi0"]),
        "c5_S_ge_0": (worst["S_lo"] >= 0.0, worst["S_lo"]),
        "c5_Dstar_le_exposure": (worst["dstar_over_expo"] <= 1.0 + 1e-12, worst["dstar_over_expo"]),
        "c5_tutored_le_source_cohort_g1_g3": (worst["tut_over_cohort_g13"] <= 1.0 + 1e-12,
                                              worst["tut_over_cohort_g13"]),
        "c5_tutored_le_candidates_g4": (worst["tut_over_cand_g4"] <= 1.0 + 1e-12,
                                        worst["tut_over_cand_g4"]),
        "c5_no_nan_or_inf": (worst["nan"] == 0, worst["nan"]),
        "c5_Dg0_lt_Dg1_every_year": (all(f[3] != "Dg0_ge_Dg1" for f in fail),
                                     worst["d0_minus_d1"]),
    }
    return dict(
        check_id="c5",
        expected_pattern=("Every scored row: p,D in [0,1]; sum omega = 1; pi0,pi1,Pi in [0.01,1] and "
                          "Pi >= pi0; S >= 0; D* <= sum nu; tutored head-count <= cohort at gate; no "
                          "NaN/inf; D(g0) < D(g1)."),
        synthetic_value=(f"{len(fail)} identity violations over {len(TYPE_ORDER) * len(GATES) * T} "
                         f"country-gate-years; p in [{worst['p_lo']:.4g},{worst['p_hi']:.4g}], "
                         f"D in [{worst['D_lo']:.4g},{worst['D_hi']:.4g}], max D*/exposure "
                         f"{worst['dstar_over_expo']:.4g}"),
        verdict=_verdict_fail(ok),
        note=("The tutored-headcount bound uses the source-level cohort C[src] for g1-g3 and the "
              "candidate pool for g4 (no cohort exists at the labour gate); see IMPLEMENTATION_NOTE_N1.md."),
        sub=sub, fails=fail)


def check_c6(ablation_path, v12_path):
    if not Path(v12_path).exists():
        return dict(check_id="c6", expected_pattern="shadow OFF -> v1.3 panel byte-identical to v1.2 panel",
                    synthetic_value="v1.2 panel absent", verdict="VOID",
                    note="c6 is VOID when the frozen v1.2 panel is absent (sec.8).", sub={})
    a = sha256_file(ablation_path)
    b = sha256_file(v12_path)
    ok = (a == b)
    return dict(
        check_id="c6",
        expected_pattern=("With the shadow block switched off the v1.3 panel reproduces "
                          "generator_v1_2/results/synthetic_panel_v1_2.csv byte-for-byte (sha256 equality)."),
        synthetic_value=f"ablation sha256 {a} vs v1.2 sha256 {b}; match={ok}",
        verdict=_verdict_fail(ok),
        note=("The ablation artifact is written with exactly v1.2's 67 columns, row order and %.10g "
              "formatting; a mismatch would mean the shadow block leaked into v1.2 arithmetic."),
        sub={"c6_sha256_byte_identical": (ok, a)}, shas=(a, b))


# --------------------------------------------------------------------------------------
# outputs
# --------------------------------------------------------------------------------------
def write_checks(checks, outdir):
    cols = ["check_id", "expected_pattern", "synthetic_value", "verdict", "note"]
    with open(Path(outdir) / "shadow_checks_v1_3.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols + ["label"], lineterminator="\n")
        w.writeheader()
        for c in checks:
            row = {k: c.get(k, "") for k in cols}
            row["label"] = LABEL
            w.writerow(row)
    # detail
    with open(Path(outdir) / "shadow_checks_detail_v1_3.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["check_id", "component", "value", "component_verdict", "label"])
        for c in checks:
            for k, v in c.get("sub", {}).items():
                val = v[1]
                if isinstance(val, float):
                    val = f"{val:.10g}"
                cv = "INFO" if v[0] is None else ("PASS" if v[0] else "FAIL")
                w.writerow([c["check_id"], k, val, cv, LABEL])
            for f in c.get("fails", []):
                w.writerow([c["check_id"] + "_cell_fail",
                            f"{f[0]}|{f[2]}|g{f[1]}|{f[3]}",
                            (f"{f[4]:.10g}" if isinstance(f[4], float) else f[4]),
                            "FAIL", LABEL])
        w.writerow(["c6_ablation", "artifact", "results/_ablation/synthetic_panel_v1_3_shadow_off.csv",
                    "INFO", LABEL])


def write_gates(w, outdir):
    path = Path(outdir) / "shadow_gates_v1_3.csv"
    cols = ["label", "country_type", "host_country", "year", "gate", "gate_name", "Q", "pi0", "pi1",
            "dpi", "Pi", "kappa", "R", "ln_R", "V", "s_g", "D_gate", "spend_share", "D_cohort",
            "cohort_exposure", "Pi_over_pi0", "candidates", "capacity", "advances",
            "p_q1", "p_q2", "p_q3", "p_q4", "p_q5"]
    with open(path, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        for tname in TYPE_ORDER:
            d = w[tname]
            for t in range(T):
                for g in GATES:
                    row = dict(label=LABEL, country_type=tname, host_country=d["host"],
                               year=int(YEARS[t]), gate="g%d" % g, gate_name=GATE_NAMES[g],
                               Q=float(d["Q"][g, t]), pi0=float(d["pi0"][g, t]),
                               pi1=float(d["pi1"][g, t]), dpi=float(d["dpi"][g, t]),
                               Pi=float(d["Pi"][g, t]), kappa=float(d["kappa"][g, t]),
                               R=float(d["R"][g, t]), ln_R=float(math.log(max(d["R"][g, t], 1e-12))),
                               V=float(d["V"][g, t]), s_g=float(d["ci"]["s"]),
                               D_gate=float(d["D"][g, t]), spend_share=float(d["S"][g, t]),
                               D_cohort=float(d["Dstar"][t]), cohort_exposure=d["exposure"],
                               Pi_over_pi0=float(d["ratio"][g, t]),
                               candidates=float(d["cand"][g, t]), capacity=float(d["cap"][g, t]),
                               advances=float(d["adv"][g, t]))
                    for q in range(5):
                        row["p_q%d" % (q + 1)] = float(d["p"][g, q, t])
                    wr.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v)
                                 for k, v in row.items()})


def write_decomposition(w, beh, outdir):
    path = Path(outdir) / "shadow_decomposition_v1_3.csv"
    cols = ["label", "country_type", "host_country", "year", "gate", "a_g", "bZ_lnR", "bV_ln1pV",
            "bD_ln1pdpi", "by_ln_y", "minus_bF_fee", "Theta_median_q", "D_gate",
            "share_lnR", "share_ln1pV", "share_ln1pdpi", "income_median_rel"]
    with open(path, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        for tname in TYPE_ORDER:
            d = w[tname]; ci = d["ci"]
            ys = shadow_quintile_income(beh, ci["sigma"])
            ymed = ys[2]
            for t in range(T):
                for g in GATES:
                    V = max(0.0, float(d["V"][g, t]))
                    lnR = math.log(max(float(d["R"][g, t]), 1e-12))
                    ln1pV = math.log1p(V)
                    ln1pd = math.log1p(max(float(d["dpi"][g, t]), 0.0))
                    a = beh["a_0"] if g == 0 else beh["a_g"]
                    t_lnR = beh["b_Z"] * lnR
                    t_V = beh["b_V"] * ln1pV
                    t_d = beh["b_D"] * ln1pd
                    t_y = beh["b_y"] * math.log(ymed)
                    t_f = -beh["b_F"] * math.log1p(float(ci["s"]) / ymed)
                    th = a + t_lnR + t_V + t_d + t_y + t_f
                    tot = abs(t_lnR) + abs(t_V) + abs(t_d) + abs(t_y) + abs(t_f)
                    wr.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in dict(
                        label=LABEL, country_type=tname, host_country=d["host"],
                        year=int(YEARS[t]), gate="g%d" % g, a_g=a, bZ_lnR=t_lnR, bV_ln1pV=t_V,
                        bD_ln1pdpi=t_d, by_ln_y=t_y, minus_bF_fee=t_f, Theta_median_q=th,
                        D_gate=float(d["D"][g, t]),
                        share_lnR=(t_lnR / tot if tot > 1e-12 else 0.0),
                        share_ln1pV=(t_V / tot if tot > 1e-12 else 0.0),
                        share_ln1pdpi=(t_d / tot if tot > 1e-12 else 0.0),
                        income_median_rel=ymed).items()})


def write_country_inputs_audit(w, hosts, beh, outdir):
    path = Path(outdir) / "shadow_country_inputs_audit.csv"
    cols = ["label", "country_type", "host_country", "quantity", "value", "unit", "provenance",
            "enters", "is_behavioural"]
    prov = {
        "phi": ("OBSERVED (WDI/ILO 2019, 1 - vulnerable-employment share; declared interpretation)", "V = phi*..."),
        "s": ("DERIVED / DECLARED fee share of mean monthly household income (PARAMETERS.csv C04-C06)", "-b_F ln(1+s/y)"),
        "sigma": ("DECLARED income dispersion; no Gini series on disk (C07-C09)", "y_q/ybar lay-out"),
        "nu": ("DERIVED from observed UIS out-of-school rates + DECLARED split (C10-C12)", "D* = sum_g nu_g D_g"),
        "oos_upper": ("OBSERVED UIS SDG4 2020 (C13)", "constrains nu"),
    }
    with open(path, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        for tname in TYPE_ORDER:
            ci = SHADOW_COUNTRY_INPUTS[tname]
            for q in ("phi", "s", "sigma", "nu", "oos_upper"):
                val = ci[q]
                if isinstance(val, dict):
                    val = "; ".join("g%d=%.2f" % (k, v) for k, v in sorted(val.items()))
                wr.writerow(dict(label=LABEL, country_type=tname, host_country=hosts[tname],
                                 quantity=q, value=(f"{val:.10g}" if isinstance(val, float) else val),
                                 unit={"phi": "probability", "s": "share of mean monthly income",
                                       "sigma": "log units", "nu": "share of cohort",
                                       "oos_upper": "percent"}[q],
                                 provenance=prov[q][0], enters=prov[q][1], is_behavioural="no"))
        for k in ("a_0", "a_g", "b_Z", "b_V", "b_D", "b_y", "b_F", "delta", "w_Q", "w_pi",
                  "w_kappa", "r_EAP", "H", "dS", "omega", "zq"):
            wr.writerow(dict(label=LABEL, country_type="ALL THREE (shared rule)", host_country="",
                             quantity=k, value=_f(SHADOW_BEHAV[k]), unit="logit / declared",
                             provenance="DECLARED, frozen (PARAMETERS.csv B01-B23)",
                             enters="Theta / R / V / D*", is_behavioural="YES-shared-gate-indexed"))
        wr.writerow(dict(label=LABEL, country_type="HOST-MAPPING RULE", host_country="",
                         quantity="host_assignment",
                         value="HKG=highest 2020 gdppc; PHL=SYN00_PHL_LIKE; KHM=lowest 2020 gdppc",
                         unit="rule", provenance="IMPLEMENTATION_NOTE.md sec.1 (shadow-blind income rule)",
                         enters="gate state source only (not a demand-equation term)",
                         is_behavioural="no"))


def sensitivity_cells():
    """Pre-declared one-at-a-time grid (PRE_DECLARATIONS.md sec.6, PARAMETERS.csv B03-B17, C05-C09).

    Each cell is (cell_id, parameter, value, beh_variant, inputs_variant_or_None).
    """
    cells = [("central", "central", "central", shadow_beh_variant(), None)]
    for v in (1.2, 2.0, 2.8):
        cells.append((f"b_Z={v:g}", "b_Z", v, shadow_beh_variant(b_Z=v), None))
    for v in (0.5, 1.0, 1.5):
        cells.append((f"b_V={v:g}", "b_V", v, shadow_beh_variant(b_V=v), None))
    for v in (1.0, 2.0, 3.0):
        cells.append((f"b_D={v:g}", "b_D", v, shadow_beh_variant(b_D=v), None))
    for v in (0.3, 0.6, 0.9):
        cells.append((f"b_y={v:g}", "b_y", v, shadow_beh_variant(b_y=v), None))
    for v in (0.4, 0.8, 1.2):
        cells.append((f"b_F={v:g}", "b_F", v, shadow_beh_variant(b_F=v), None))
    for v in (0.15, 0.30, 0.45):
        cells.append((f"delta_g={v:g}", "delta_g", v,
                      shadow_beh_variant(delta={1: v, 2: v, 3: v, 4: v}), None))
    for v in (10.0, 20.0, 30.0):
        cells.append((f"H={v:g}", "H", v, shadow_beh_variant(H=v), None))
    sig = [("low", (0.40, 0.60, 0.55)), ("central", (0.55, 0.80, 0.75)),
           ("high", (0.70, 1.00, 0.95))]
    for lab, trip in sig:
        cells.append((f"sigma={lab}", "sigma", trip, None, ("sigma", trip)))
    for v in (0.02, 0.04, 0.07):
        cells.append((f"s_PHL={v:g}", "s_PHL", v, None, ("s", "SYN_PHL_LIKE", v)))
    for v in (0.01, 0.021, 0.04):
        cells.append((f"s_KHM={v:g}", "s_KHM", v, None, ("s", "SYN_KHM_LIKE", v)))
    return cells


def run_sensitivity(hosts, outdir):
    rows = []
    for cell in sensitivity_cells():
        cid, par, val, beh, inp = cell
        beh = SHADOW_BEHAV if beh is None else beh
        inputs = shadow_inputs_named()
        if inp is not None:
            if inp[0] == "sigma":
                _, trip = inp
                for k, v in zip(TYPE_ORDER, trip):
                    inputs[k]["sigma"] = float(v)
            elif inp[0] == "s":
                col, k, v = inp
                inputs[k]["s"] = float(v)
        res, *_ = run_all(beh=beh, shadow=True, inputs=inputs, hosts=hosts)
        w = shadow_world(res, hosts, inputs, beh)
        c1 = check_c1(w, beh); c2 = check_c2(w, beh); c3 = check_c3(w, beh)
        c4a = check_c4a(w, beh); c4b = check_c4b(w, beh); c5 = check_c5(w, beh)
        c4c_ok, _ = shadow_code_audit()
        i20 = DECLARED_COMPARISON_YEAR - YEAR_START
        rows.append(dict(
            label=LABEL, cell_id=cid, parameter=par, value=(val if isinstance(val, str) else _f(val)),
            D_HKG_g2_2020=float(w["SYN_HKG_LIKE"]["D"][2, i20]),
            Dstar_HKG=float(w["SYN_HKG_LIKE"]["Dstar"][i20]),
            Dstar_PHL=float(w["SYN_PHL_LIKE"]["Dstar"][i20]),
            Dstar_KHM=float(w["SYN_KHM_LIKE"]["Dstar"][i20]),
            c1=c1["verdict"], c2=c2["verdict"], c3=c3["verdict"], c4a=c4a["verdict"],
            c4b=c4b["verdict"], c4c=("PASS" if c4c_ok else "FAIL"), c5=c5["verdict"],
            c1_gap_min_pp=min(c1["gaps"].values()) * 100.0,
            c2_gap_min_pp=min(c2["gaps"].values()) * 100.0,
            max_D_g0=max(float(w[k]["D"][0, :].max()) for k in TYPE_ORDER),
            gap_HKG_PHL=float(c4b["gaps"][0]),
            gap_PHL_KHM=float(c4b["gaps"][1]),
            max_Pi_over_pi0_g1_g3=float(max(w[k]["ratio"][1:4, :].max() for k in TYPE_ORDER)),
        ))
    with open(Path(outdir) / "shadow_sensitivity_v1_3.csv", "w", newline="") as fh:
        cols = list(rows[0].keys())
        wr = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        for r in rows:
            wr.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in r.items()})
    return rows


def guard_hashes(require_params=True):
    """Frozen-hash guard: refuse to run on any mismatch (sec.10 rule 3)."""
    problems = []
    if not SHADOW_PREDECL.exists():
        problems.append("frozen shadow predeclaration not found: %s" % SHADOW_PREDECL)
    elif sha256_file(SHADOW_PREDECL) != EXPECTED_SHADOW_PREDECL_SHA:
        problems.append("shadow PRE_DECLARATIONS.md sha256 changed: %s" % sha256_file(SHADOW_PREDECL))
    if not SHADOW_S1.exists():
        problems.append("S1 note not found: %s" % SHADOW_S1)
    elif sha256_file(SHADOW_S1) != EXPECTED_SHADOW_S1_SHA:
        problems.append("S1 NOTE sha256 changed: %s" % sha256_file(SHADOW_S1))
    if not PREDECL.exists():
        problems.append("frozen v1.2 predeclaration not found: %s" % PREDECL)
    elif sha256_file(PREDECL) != EXPECTED_PREDECL_SHA:
        problems.append("v1.2 PRE_DECLARATIONS.md sha256 changed: %s" % sha256_file(PREDECL))
    if not LOCAL_PREDECL.exists():
        problems.append("local PRE_DECLARATIONS.md copy not found")
    else:
        txt = LOCAL_PREDECL.read_text()
        for p in (SHADOW_PREDECL, SHADOW_S1):
            if p.read_text() not in txt:
                problems.append("local copy does not contain %s verbatim" % p.name)
    if require_params:
        if not PARAMS_MD.exists():
            problems.append("PARAMS.md not found")
        elif sha256_file(PARAMS_MD) != EXPECTED_PARAMS_SHA:
            problems.append("PARAMS.md sha256 changed: %s" % sha256_file(PARAMS_MD))
    if problems:
        raise SystemExit("REFUSING TO RUN:\n  " + "\n  ".join(problems))
    return True


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "results"))
    ap.add_argument("--manifest", default=str(ROOT / "RUN_MANIFEST.json"))
    ap.add_argument("--smoke", action="store_true", help="smoke test: stop after the ablation + distributions")
    ap.add_argument("--no-sensitivity", action="store_true")
    args = ap.parse_args(argv)
    t0 = time.time()
    guard_hashes()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    inputs = shadow_inputs_named()

    # ---- 1. shadow-OFF run: byte-identity guard (c6) and the host mapping rule ------
    res_off, *_ = run_all(shadow=False)
    rows_off = build_panel(res_off)
    abl_dir = outdir / "_ablation"; abl_dir.mkdir(parents=True, exist_ok=True)
    abl_path = abl_dir / "synthetic_panel_v1_3_shadow_off.csv"
    write_panel(rows_off, abl_path)
    hosts, gdp = resolve_hosts(res_off)
    print("[v1.3] hosts: " + ", ".join("%s<-%s" % (k, v) for k, v in hosts.items()))

    # ---- 2. scored (shadow ON) run --------------------------------------------------
    res, ptr_obs, spend_obs, S_phl, P_phl = run_all(beh=SHADOW_BEHAV, shadow=True,
                                                    inputs=inputs, hosts=hosts)
    hosts_on, gdp_on = resolve_hosts(res)
    host_map_stable = (hosts_on == hosts)
    if not host_map_stable:
        # Disclosed, not fatal: the declared rule reads the v1.2 (shadow-off) state. The block's
        # feedback can move a host's 2020 GDPpc enough to change an income ranking; that is a
        # property of the feedback loop and is reported as a diagnostic, not used to re-map.
        print("[v1.3] NOTE: host ranking under feedback differs: %r (declared %r)" % (hosts_on, hosts))
    rows = build_panel_v13(res, hosts, inputs)
    write_panel_v13(rows, outdir / "synthetic_panel_v1_3.csv")
    w = shadow_world(res, hosts, inputs, SHADOW_BEHAV)
    write_gates(w, outdir)
    write_decomposition(w, SHADOW_BEHAV, outdir)
    write_country_inputs_audit(w, hosts, SHADOW_BEHAV, outdir)

    if args.smoke:
        for tname in TYPE_ORDER:
            d = w[tname]
            print("[smoke] %-13s host=%-18s D(g0..g4) 2020 = %s | R(g1..g4) 2020 = %s" % (
                tname, d["host"],
                " ".join("%.4f" % d["D"][g, DECLARED_COMPARISON_YEAR - YEAR_START] for g in GATES),
                " ".join("%.3f" % d["R"][g, DECLARED_COMPARISON_YEAR - YEAR_START] for g in (1, 2, 3, 4))))
            print("            R range over 1970-2025 g1..g4: %s" % (
                " | ".join("g%d [%.3f,%.3f]" % (g, d["R"][g, :].min(), d["R"][g, :].max()) for g in (1, 2, 3, 4))))
        print("[smoke] c6 ablation sha %s vs v1.2 %s match=%s" % (
            sha256_file(abl_path), sha256_file(V12_PANEL) if V12_PANEL.exists() else "absent",
            sha256_file(abl_path) == (sha256_file(V12_PANEL) if V12_PANEL.exists() else None)))
        print("[smoke] %.1fs" % (time.time() - t0))
        return None

    # ---- 3. checks -------------------------------------------------------------------
    c1 = check_c1(w, SHADOW_BEHAV)
    c2 = check_c2(w, SHADOW_BEHAV)
    c3 = check_c3(w, SHADOW_BEHAV)
    c4a = check_c4a(w, SHADOW_BEHAV)
    c4b = check_c4b(w, SHADOW_BEHAV)
    c4c = check_c4c(w, SHADOW_BEHAV)
    c5 = check_c5(w, SHADOW_BEHAV)
    c6 = check_c6(abl_path, V12_PANEL)
    if c4c["verdict"] != "PASS":
        c4_verdict = "VOID"
    elif c4a["verdict"] == "PASS" and c4b["verdict"] == "PASS":
        c4_verdict = "PASS"
    elif c4a["verdict"] == "VOID" or c4b["verdict"] == "VOID":
        c4_verdict = "VOID"
    else:
        c4_verdict = "FAIL"
    c4 = dict(check_id="c4", expected_pattern="c4a AND c4b AND c4c (VOID if c4c fails; sec.8).",
              synthetic_value="c4a %s; c4b %s; c4c %s -> c4 %s" % (
                  c4a["verdict"], c4b["verdict"], c4c["verdict"], c4_verdict),
              verdict=c4_verdict,
              note="Aggregate row only; the components below are the scored objects.", sub={})
    checks = [c1, c2, c3, c4, c4a, c4b, c4c, c5, c6]
    write_checks(checks, outdir)

    # ---- 4. sensitivity ---------------------------------------------------------------
    sens = None if args.no_sensitivity else run_sensitivity(hosts, outdir)

    # ---- 5. diagnostics (NOT-SCORED) --------------------------------------------------
    i20 = DECLARED_COMPARISON_YEAR - YEAR_START
    # feedback-loop magnitude: scored (with Pi) vs a run with the substitution disabled?
    # The substitution cannot be disabled without touching v1.2 arithmetic, so the loop's
    # realised size is reported directly from the stored ratios.
    loop = {}
    for tname in TYPE_ORDER:
        d = w[tname]
        # only g1-g3 carry the pool hook; g4 has NO hook (labour gate) and is excluded
        loop[tname] = dict(max_ratio_g1_g3=float(d["ratio"][1:4, :].max()),
                           mean_ratio_g1_g3_2020=float(d["ratio"][1:4, i20].mean()),
                           ratio_g4_2020_not_used=float(d["ratio"][4, i20]))
    # twin comparison (NOT-SCORED): impossible for g1..g3 without declared inputs for the twins.
    sat_by = {}
    for t in TYPE_ORDER:
        for g in (1, 2, 3, 4):
            Dv = w[t]["D"][g, :]
            sat_by["%s|g%d" % (t, g)] = dict(
                cells_scored=int(((Dv >= SAT_LO) & (Dv <= SAT_HI)).sum()),
                cells_below_lo=int((Dv < SAT_LO).sum()),
                cells_above_hi=int((Dv > SAT_HI).sum()),
                D_min=float(Dv.min()), D_median=float(np.median(Dv)), D_max=float(Dv.max()))
    d_hkg = w["SYN_HKG_LIKE"]
    i20_ = DECLARED_COMPARISON_YEAR - YEAR_START
    R_req = required_R_for_D(SHADOW_BEHAV, d_hkg["ci"], 2, float(d_hkg["V"][2, i20_]),
                             float(d_hkg["dpi"][2, i20_]), C4A_LO)
    c4a_gap = dict(target_D=C4A_LO,
                   realised_D=float(d_hkg["D"][2, i20_]),
                   realised_R=float(d_hkg["R"][2, i20_]),
                   realised_lnR=float(math.log(d_hkg["R"][2, i20_])),
                   required_R=R_req, required_lnR=float(math.log(R_req)),
                   required_over_realised=float(R_req / d_hkg["R"][2, i20_]),
                   required_dlnR=float(math.log(R_req / d_hkg["R"][2, i20_])))
    off_by = {r["cp"]["name"]: r for r in res_off}
    host_delta = {}
    for t in TYPE_ORDER:
        nm = hosts[t]
        a = off_by[nm]; b = by_name_on[nm] if False else [x for x in res if x["cp"]["name"] == nm][0]
        host_delta[t] = dict(host=nm,
                             gdppc_2020_off=float(a["Y"][i20_]),
                             gdppc_2020_on=float(b["Y"][i20_]),
                             gdppc_ratio=float(b["Y"][i20_] / a["Y"][i20_]),
                             enrol_upper_2020_off=float(a["enrol"][2, i20_]),
                             enrol_upper_2020_on=float(b["enrol"][2, i20_]),
                             enrol_upper_ratio=float(b["enrol"][2, i20_] / max(a["enrol"][2, i20_], 1e-12)),
                             completion_upper_2020_off=float(a["comp_coh"][2, i20_]),
                             completion_upper_2020_on=float(b["comp_coh"][2, i20_]),
                             enrolment_primary_2020_off=float(a["enrol"][0, i20_]),
                             enrolment_primary_2020_on=float(b["enrol"][0, i20_]),
                             enrol_tertiary_2020_off=float(a["enrol"][3, i20_]),
                             enrol_tertiary_2020_on=float(b["enrol"][3, i20_]),
                             enrol_tertiary_ratio=float(b["enrol"][3, i20_] / max(a["enrol"][3, i20_], 1e-12)))
    sm = dict(loop=loop)
    Path(outdir / "shadow_diagnostics_v1_3.json").write_text(
        json.dumps(dict(label=LABEL, scored=False, note=(
            "NOT-SCORED diagnostics. Not part of the frozen c1-c6 set."),
            feedback_loop=loop,
            saturation=dict(c1_cells_saturated=c1["n_sat"], c2_cells_saturated=c2["n_sat"],
                            by_type_gate=sat_by),
            d_gate_2020={t: {("g%d" % g): float(w[t]["D"][g, i20]) for g in GATES} for t in TYPE_ORDER},
            R_2020={t: {("g%d" % g): float(w[t]["R"][g, i20]) for g in GATES} for t in TYPE_ORDER},
            exposure={t: w[t]["exposure"] for t in TYPE_ORDER},
            Dstar_2020={t: float(w[t]["Dstar"][i20]) for t in TYPE_ORDER},
            c4a_gap_diagnostic=c4a_gap,
            host_v1_2_columns_2020=host_delta,
            hosts=hosts, hosts_under_feedback=hosts_on, host_map_stable=host_map_stable,
            gdp_2020_shadow_off={t: float(gdp[hosts[t]]) for t in TYPE_ORDER},
            gdp_2020_shadow_on={t: float(gdp_on[hosts[t]]) for t in TYPE_ORDER},
            gdp_2020_ratio={t: float(gdp_on[hosts[t]] / gdp[hosts[t]]) for t in TYPE_ORDER},
            D_ratio_gates_2020={t: {("g%d" % g): float(w[t]["ratio"][g, i20]) for g in GATES}
                                for t in TYPE_ORDER}), indent=2, sort_keys=True) + "\n")

    # ---- 6. manifest -------------------------------------------------------------------
    sha = lambda p: sha256_file(p) if Path(p).exists() else None
    manifest = dict(
        label=LABEL,
        statement=("Synthetic data from declared assumptions only. Not evidence, not an estimate, not a "
                   "forecast, no causal or direction claim, no real country modelled. The shadow block is a "
                   "declared household demand rule evaluated on this generator's own gate/queue state."),
        generator="code/sim_v1_3.py",
        spec=dict(
            frozen_shadow_predeclaration="shadow_module/PRE_DECLARATIONS.md",
            frozen_shadow_predeclaration_sha256=EXPECTED_SHADOW_PREDECL_SHA,
            s1_note="shadow_module/PRE_DECLARATIONS_S1_NOTE.md",
            s1_note_sha256=EXPECTED_SHADOW_S1_SHA,
            local_copy="PRE_DECLARATIONS.md",
            local_copy_sha256=sha(LOCAL_PREDECL),
            inherited_v1_2_predeclaration_sha256=EXPECTED_PREDECL_SHA,
            implementation_note="IMPLEMENTATION_NOTE.md",
            implementation_note_sha256=sha(ROOT / "IMPLEMENTATION_NOTE.md"),
            implementation_note_n1="IMPLEMENTATION_NOTE_N1.md",
            implementation_note_n1_sha256=sha(ROOT / "IMPLEMENTATION_NOTE_N1.md"),
        ),
        seed=SEED,
        rng="numpy PCG64 (np.random.default_rng), single stream, v1.2 draw order, shadow block draws nothing",
        panel=dict(countries=N_C, years=[YEAR_START, YEAR_END], levels=list(LEVELS), rows=len(rows)),
        host_mapping=hosts,
        host_mapping_rule="HKG=highest 2020 gdppc; PHL=SYN00_PHL_LIKE; KHM=lowest 2020 gdppc (shadow-blind)",
        host_gdp_2020={k: float(v) for k, v in gdp.items() if k in hosts.values()},
        host_mapping_stable_under_feedback=bool(host_map_stable),
        host_mapping_under_feedback=hosts_on,
        python=platform.python_version(), numpy=np.__version__,
        hashes=dict(
            code_sha256=sha(CODE),
            params_md_sha256=sha(PARAMS_MD),
            frozen_parameters_csv_sha256=sha(SHADOW_DIR / "PARAMETERS.csv"),
            v1_2_code_sha256=sha(V12_DIR / "code" / "sim_v1_2.py"),
            v1_2_panel_sha256=sha(V12_PANEL),
            results={p.name: sha(p) for p in sorted(outdir.glob("*.csv"))},
            ablation={"_ablation/synthetic_panel_v1_3_shadow_off.csv":
                      sha(outdir / "_ablation" / "synthetic_panel_v1_3_shadow_off.csv")},
        ),
        checks_summary={c["check_id"]: c["verdict"] for c in checks},
        sensitivity=dict(cells=len(sens) if sens else 0,
                         file="results/shadow_sensitivity_v1_3.csv"),
        determinism=dict(method="two clean runs into separate output directories, cmp on every results CSV",
                         floats="%.10g", wall_clock_in_outputs=False),
    )
    Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    dt = time.time() - t0
    print(f"[sim_v1_3] {LABEL}: {len(rows)} rows, {dt:.1f}s, seed {SEED}")
    for c in checks:
        print(f"  {c['check_id']}: {c['verdict']}  {c['synthetic_value'][:200]}")
    return checks


if __name__ == "__main__":
    main()
