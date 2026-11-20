# ======================================================================================
# 5b. SHADOW-EDUCATION DEMAND AT THE GATES  (v1.3 block)
#     Frozen spec: shadow_module/PRE_DECLARATIONS.md (sha256 cf8c61cb...) + S1 note.
#     LABEL: SYNTHETIC. ONE behavioural rule for every country; country variation enters
#     ONLY through the declared input bundle (phi, s, sigma, nu) from PARAMETERS.csv
#     C01-C12. No country-specific coefficient exists anywhere in this block (c4c audits
#     exactly that).
# ======================================================================================
GATES = (0, 1, 2, 3, 4)
GATE_NAMES = {0: "g0_PRE", 1: "g1_LS", 2: "g2_US", 3: "g3_TER", 4: "g4_JOB"}
GATE_LABEL = {0: "PRE-GATE (control, no positional good)",
              1: "GATE-LS lower-secondary entry",
              2: "GATE-US upper-secondary entry",
              3: "GATE-TER tertiary entry",
              4: "GATE-JOB credential -> formal rung"}
TYPE_ORDER = ("SYN_HKG_LIKE", "SYN_PHL_LIKE", "SYN_KHM_LIKE")
DECLARED_COMPARISON_YEAR = 2020          # t* (PRE_DECLARATIONS.md sec.8 c4a)

# Frozen central values, PRE_DECLARATIONS.md sec.6 / PARAMETERS.csv B01-B23.
# Keys are gates (0-4) only. A country key here would be the c4c violation.
SHADOW_BEHAV = dict(
    a_0=-4.80,
    a_g=-2.80,
    b_Z=2.00, b_V=1.00, b_D=2.00, b_y=0.60, b_F=0.80,
    delta={0: 0.02, 1: 0.30, 2: 0.30, 3: 0.25, 4: 0.20},
    w_Q=0.40, w_pi=0.40, w_kappa=0.20,
    r_EAP=0.087, H=20.0,
    dS={0: 0.0, 1: 3.0, 2: 3.0, 3: 4.0, 4: 0.0},
    omega=(0.20, 0.20, 0.20, 0.20, 0.20),
    zq=(-1.2816, -0.5244, 0.0, 0.5244, 1.2816),
)

# Declared country input bundles, PRE_DECLARATIONS.md sec.7 / PARAMETERS.csv C01-C12.
# These are the ONLY country-varying quantities. Same a, b, delta for every type.
SHADOW_COUNTRY_INPUTS = {
    "SYN_HKG_LIKE": dict(phi=0.940, s=0.0305, sigma=0.55,
                         nu={1: 0.10, 2: 0.62, 3: 0.22}, oos_upper=5.428),
    "SYN_PHL_LIKE": dict(phi=0.677, s=0.0400, sigma=0.80,
                         nu={1: 0.30, 2: 0.35, 3: 0.10}, oos_upper=24.737),
    "SYN_KHM_LIKE": dict(phi=0.464, s=0.0210, sigma=0.75,
                         nu={1: 0.28, 2: 0.13, 3: 0.02}, oos_upper=56.987),
}


def shadow_inputs_named():
    """Deep copy of the declared input bundles (so a sensitivity run cannot mutate them)."""
    return {k: {kk: (dict(vv) if isinstance(vv, dict) else vv) for kk, vv in v.items()}
            for k, v in SHADOW_COUNTRY_INPUTS.items()}


def shadow_beh_variant(**over):
    """One-at-a-time variant of the frozen block (pre-declared sensitivity only)."""
    beh = dict(SHADOW_BEHAV)
    beh["delta"] = dict(SHADOW_BEHAV["delta"])
    beh["dS"] = dict(SHADOW_BEHAV["dS"])
    beh["omega"] = tuple(SHADOW_BEHAV["omega"])
    beh["zq"] = tuple(SHADOW_BEHAV["zq"])
    for k, v in over.items():
        if k == "delta" and isinstance(v, dict):
            beh["delta"].update(v)
        else:
            beh[k] = v
    return beh


def resolve_hosts(results):
    """Declared, shadow-blind host rule (IMPLEMENTATION_NOTE.md sec.1).

    SYN_HKG_LIKE <- the synthetic country with the highest 2020 GDP per capita
    SYN_PHL_LIKE <- v1.2's own declared PHL-informed country (PARAMS.md sec.9)
    SYN_KHM_LIKE <- the synthetic country with the lowest 2020 GDP per capita

    GDP per capita is a v1.2 state variable and is NOT an argument of the demand
    equation (SHADOW_MODULE.md sec.4). The rule never reads D, R or any check value.
    """
    t20 = int(np.where(YEARS == DECLARED_COMPARISON_YEAR)[0][0])
    gdp = [(float(r["Y"][t20]), i, r["cp"]["name"]) for i, r in enumerate(results)]
    hi = max(gdp, key=lambda x: (x[0], -x[1]))
    lo = min(gdp, key=lambda x: (x[0], x[1]))
    hosts = {"SYN_HKG_LIKE": hi[2], "SYN_PHL_LIKE": "SYN00_PHL_LIKE", "SYN_KHM_LIKE": lo[2]}
    if len(set(hosts.values())) != 3:
        raise SystemExit("REFUSING: host rule produced non-distinct countries: %r" % (hosts,))
    return hosts, {n: v for v, _, n in gdp}


def gate_numbers(beh, cand, cap, adv, kappa):
    """Frozen R definition (PRE_DECLARATIONS.md sec.4.1): Q, pi0, kappa, R + components."""
    Q = min(max(float(cand) / max(float(cap), 1e-9), 0.0), 10.0)
    pi0 = min(max(float(adv) / max(float(cand), 1e-9), 0.01), 0.999)
    k = min(max(float(kappa), 1.0), 5.0)
    R = (1.0 + Q) ** beh["w_Q"] * (1.0 / pi0) ** beh["w_pi"] * k ** beh["w_kappa"]
    R = min(max(R, 1.0), 20.0)
    return dict(Q=Q, pi0=pi0, kappa=k, R=R, candidates=float(cand),
                capacity=float(cap), advances=float(adv))


def gate_state(cand_c, cap_c, grads, enrol, rankf, queue_r, vac, hires, beh):
    """Gate-state contract, DRY_RUN_PLAN.md sec.1.3 mapped onto v1.2 state.

    g0 pre-gate : candidates = primary cohort, capacity = primary seats, advances =
                  primary official-age admissions, kappa = 1 (no credential rank).
    g1..g3      : candidates = graduates of the level below, capacity = the model's own
                  physical admission capacity phys = min(phys_cap*seats, overage_cap*C),
                  advances = admissions (enrol), kappa = rank factor at the rung.
    g4 job gate : candidates = queue + hires over rungs 1-3, capacity = vacancies,
                  advances = hires, kappa = hires-weighted mean rank factor.
    """
    gs = {}
    gs[1] = gate_numbers(beh, grads[0], cap_c[1], enrol[1], rankf[0])
    gs[2] = gate_numbers(beh, grads[1], cap_c[2], enrol[2], rankf[1])
    gs[3] = gate_numbers(beh, grads[2], cap_c[3], enrol[3], rankf[2])
    cand4 = sum(float(queue_r[i]) + float(hires[i]) for i in (1, 2, 3))
    cap4 = sum(float(vac[i]) for i in (1, 2, 3))
    adv4 = sum(float(hires[i]) for i in (1, 2, 3))
    wh = sum(float(hires[i]) for i in (1, 2, 3))
    if wh > 1e-12:
        k4 = sum(float(hires[i]) * float(rankf[i]) for i in (1, 2, 3)) / wh
    else:
        k4 = 1.0
    gs[4] = gate_numbers(beh, cand4, cap4, adv4, k4)
    gs[0] = gate_numbers(beh, cand_c[0], cap_c[0], enrol[0], 1.0)
    return gs


def gate_state_from_run(r, t, beh):
    """Convenience wrapper for the checks: gate state of a stored run at year index t."""
    C = r["C"]
    cap_c = [min(P["phys_cap"] * r["seats"][L, t], P["overage_cap"] * C[L, t])
             for L in range(NL)]
    return gate_state(C[:, t], cap_c, r["grads"][:, t], r["enrol"][:, t],
                      r["rankf"][:, t], r["queue_r"][:, t], r["vac"][:, t],
                      r["hires"][:, t], beh)


def credential_value(beh, phi, gate, w_for_t=None, w_inf_t=None):
    """Frozen V (PRE_DECLARATIONS.md sec.4.2): positional value of the credential."""
    if gate == 0:
        return 0.0                      # no gate, no positional good (sec.4.2, c3)
    if gate == 4:
        G = math.log(max(float(w_for_t[1]), 1e-12) / max(float(w_inf_t), 1e-12))
        return phi * G * beh["H"]       # formal-rung wage-gap form (PARAMETERS.csv B21)
    return phi * beh["r_EAP"] * beh["dS"][gate] * beh["H"]


def shadow_quintile_income(beh, sigma):
    """Declared lognormal lay-out at the five quintile midpoints, mean-normalised."""
    raw = [math.exp(sigma * z) for z in beh["zq"]]
    m = sum(raw) / len(raw)
    return [x / m for x in raw]


def shadow_demand(beh, phi, s, sigma, R, V, dpi, gate, lnR_shift=0.0, V_mult=1.0):
    """The FROZEN demand equation (PRE_DECLARATIONS.md sec.4). Pure, no I/O, no RNG.

    p_q = sigma( a_g + b_Z ln R + b_V ln(1+V) + b_D ln(1+dpi) + b_y ln(y_q/ybar)
                 - b_F ln(1 + s/(y_q/ybar)) )
    D   = sum_q omega_q p_q
    """
    a = beh["a_0"] if gate == 0 else beh["a_g"]
    Vv = max(0.0, float(V)) * float(V_mult)
    lnR = math.log(max(float(R), 1e-12)) + float(lnR_shift)
    ln1pV = math.log1p(Vv)
    ln1pd = math.log1p(max(float(dpi), 0.0))
    ys = shadow_quintile_income(beh, sigma)
    ps, ths = [], []
    for yq in ys:
        th = (a + beh["b_Z"] * lnR + beh["b_V"] * ln1pV + beh["b_D"] * ln1pd
              + beh["b_y"] * math.log(yq) - beh["b_F"] * math.log1p(float(s) / yq))
        ths.append(th)
        ps.append(sig(th))
    D = sum(w * p for w, p in zip(beh["omega"], ps))
    return D, ps, ths, ys


def shadow_block(beh, ci, gs, w_for_t, w_inf_t):
    """One country-year of the shadow block: D, S, pi0, pi1, Pi, R, V, s, p_q.

    Pure: reads the gate state and the declared input bundle, returns numbers.
    """
    out = {}
    for g in GATES:
        Vraw = credential_value(beh, ci["phi"], g, w_for_t, w_inf_t)
        V = max(0.0, Vraw)
        pi0 = gs[g]["pi0"]
        pi1 = min(0.999, pi0 + beh["delta"][g] * (1.0 - pi0))
        dpi = pi1 - pi0
        D, ps, ths, ys = shadow_demand(beh, ci["phi"], ci["s"], ci["sigma"],
                                       gs[g]["R"], V, dpi, g)
        Pi = (1.0 - D) * pi0 + D * pi1
        out[g] = dict(D=D, ps=ps, thetas=ths, ys=ys, V=V, V_raw=Vraw,
                      V_clipped=(Vraw < 0.0), pi0=pi0, pi1=pi1, dpi=dpi, Pi=Pi,
                      R=gs[g]["R"], Q=gs[g]["Q"], kappa=gs[g]["kappa"],
                      S=D * ci["s"], ratio=Pi / max(pi0, 1e-12),
                      candidates=gs[g]["candidates"], capacity=gs[g]["capacity"],
                      advances=gs[g]["advances"])
    return out
