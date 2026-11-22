"""MASSENG v7 Comparative Mechanism Lab.

Unifies Stages 1-3 of the comparative education roadmap:
1. Stage 1 (Sign-constrained, supply-braked steam engine):
   - Parsimonious behavioral core with strict theoretical sign bounds (b_h >= 0, b_p >= 0, kappa > 0).
   - Saturating positional pull g(S) = S / (S + s0) so credential norms level off instead of overshooting.
   - Separate basic vs. tertiary private-sector income slopes (nu_basic, nu_ter).
   - Real supply/capacity brakes via conserved joint admissions.
2. Stage 2 (Flexible grade cycles & multi-destination post-secondary choice):
   - Time-varying grade cycles: Philippines K-12 (2017), Cambodia (6+3+3+4 + 2014 Bac II rerouting),
     and Hong Kong NSS reform (6+7+3 -> 6+6+4 with 2012 double cohort).
   - Multi-destination tertiary clearing: funded local, self-financed/private, vocational/associate
     rerouting, study abroad, and work/deferral — strictly conserving every applicant.
   - Explicit four-bucket bottleneck decomposition: not_qualified, no_demand, priced_out, blocked_by_gate_or_seats.
3. Stage 3 (Zero-sum shadow-education strap-on):
   - Integrates masseng/tutoring.py (Yang 2026 CES exam-vs-skill wedge omega + Kang 2025 rank tournament)
     at rationed gates, feeding tutoring costs into household spending and shifting decile shares of fixed seats.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np
from scipy.optimize import least_squares

from .data import Country, decile_income_multipliers
from .array_admissions import clear_two_sector_array
from .tutoring import TutoringParams, TutoringPolicy, solve_exam_gate_tutoring

PUB, PRIV = 0, 1
LEVEL_NAMES = ["primary", "secondary", "upper_secondary", "tertiary"]

V7_DEFAULTS = dict(
    # Core 4 behavioral dials (sign-constrained)
    b_h=1.2,          # >= 0: wage-premium return sensitivity
    b_p=1.8,          # >= 0: saturating positional/relational pull
    kappa=2.5,        # > 0: household cost sensitivity
    lam=0.35,         # >= 0: cost-dulling under credential saturation
    # Level/sector intercepts (pinned or lightly fitted)
    a_prim=4.8,
    a_sec=3.2,
    a_sec_entry=2.0,
    a_ter=4.5,
    a_ter_entry=0.2,
    # Split private-sector preferences (basic vs. tertiary)
    mu_basic=-2.8,
    nu_basic=0.8,
    mu_ter=0.5,
    nu_ter=1.2,
    # Cross-sectional income & cost scale
    eta_x=0.35,
    c_scale=1.0,
    # Fixed demographic/operational parameters
    s0_sat=0.25,      # Michaelis-Menten half-saturation for positional pull g(S) = S/(S+s0)
    h_def=0.20,
    late=0.15,
    rep_prim=0.04,
    rep_sec=0.02,
    reroute_propensity=0.62,  # share of exam-blocked candidates rerouting to vocational/associate tracks
)

# Strict theoretical sign bounds: no negative human-capital cheats or ceiling-hugging kappa=40
V7_BOUNDS = dict(
    b_h=(0.0, 6.0),
    b_p=(0.0, 6.0),
    kappa=(0.2, 12.0),
    lam=(0.0, 2.5),
    a_prim=(1.0, 10.0),
    a_sec=(0.0, 8.0),
    a_sec_entry=(-2.0, 6.0),
    a_ter=(1.0, 10.0),
    a_ter_entry=(-4.0, 5.0),
    mu_basic=(-6.0, 2.0),
    nu_basic=(-2.0, 4.0),
    mu_ter=(-3.0, 4.0),
    nu_ter=(-2.0, 5.0),
    eta_x=(0.0, 2.5),
    c_scale=(0.4, 2.5),
)


@dataclass
class V7Result:
    years: np.ndarray
    ind: dict
    bottlenecks: dict
    destinations: dict
    tutoring: dict
    extra: dict = field(default_factory=dict)


def _sig(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30.0, 30.0)))


def _interp_dict(d: dict, y: int) -> float:
    pts = sorted((int(k), float(v)) for k, v in d.items() if not str(k).startswith("_"))
    if not pts:
        return 0.0
    return float(np.interp(y, [p[0] for p in pts], [p[1] for p in pts]))


class LabModelV7:
    """Unified comparative cohort engine for Philippines, Cambodia, and Hong Kong."""

    def __init__(
        self,
        country: Country,
        params: dict | None = None,
        mode: str = "steam_braked",   # steam_braked | human_capital_only | steam_unbraked
        tutoring_params: TutoringParams | None = None,
        tutoring_policy: TutoringPolicy | None = None,
    ):
        self.c = country
        self.cfg = country.config
        self.v5 = self.cfg.get("v5", {})
        self.mode = mode
        self.p = dict(V7_DEFAULTS)
        if params:
            self.p.update({k: v for k, v in params.items() if k in V7_DEFAULTS})
        self._apply_mode_constraints()

        self.tut_params = tutoring_params or TutoringParams(enabled=(country.iso3 in ("HKG", "KHM")))
        self.tut_policy = tutoring_policy or TutoringPolicy()

        yrs = self.v5.get("years", self.cfg["years"])
        self.y0, self.y1 = yrs["simulate_from"], yrs["simulate_to"]
        st = self.cfg["structure"]
        self.max_age = st.get("max_age", 29)
        self.shs_from = st.get("upper_secondary_from", 10**6)
        self.n_lower = st.get("lower_secondary_grades", 4)
        self.cycle_reform = st.get("cycle_reform")  # e.g. HKG 2012 NSS 3-3-4 reform
        self.late_max_age = st.get("late_entry_max_age", 8)
        self.late_hazard = st.get("late_entry_hazard", 0.0)
        self.catch_up = self.cfg.get("catch_up_entry")
        self.max_defer_age = self.v5.get("max_defer_age", 25)

        # Exam gate (Cambodia Bac II or Hong Kong HKDSE/HKALE)
        gate = self.cfg.get("tertiary_entry_exam")
        hk_gate = self.v5.get("exam_gate_pass_rate")
        self.exam = None
        if gate:
            pts = sorted((int(k), float(v)) for k, v in gate["pass_rate"].items() if not str(k).startswith("_"))
            self.exam = dict(pts=pts, default=float(gate.get("default_before_data", pts[0][1])))
        elif hk_gate:
            pts = sorted((int(k), float(v)) for k, v in hk_gate.items() if not str(k).startswith("_"))
            self.exam = dict(pts=pts, default=pts[0][1])

        self._prepare()

    def _apply_mode_constraints(self):
        if self.mode == "human_capital_only":
            self.p["b_p"] = 0.0
            self.p["lam"] = 0.0
        # Enforce theoretical sign constraints
        self.p["b_h"] = max(0.0, float(self.p["b_h"]))
        self.p["b_p"] = max(0.0, float(self.p["b_p"]))
        self.p["kappa"] = max(0.05, float(self.p["kappa"]))
        self.p["lam"] = max(0.0, float(self.p["lam"]))

    def set_params(self, params: dict):
        self.p = dict(V7_DEFAULTS)
        self.p.update({k: v for k, v in params.items() if k in V7_DEFAULTS})
        self._apply_mode_constraints()
        return self

    def _driver(self, name: str, default: float = 0.0) -> np.ndarray:
        d = getattr(self.c, "drivers", {}) or {}
        s = d.get(name)
        if s is None:
            return np.full(len(self.years), default, dtype=float)
        return np.array([s(y) for y in self.years], dtype=float)

    def _prepare(self):
        c, cfg, v5 = self.c, self.cfg, self.v5
        Y = np.arange(self.y0, self.y1 + 1)
        self.years = Y
        self.gdp = np.array([c.gdppc(y) for y in Y], dtype=float)
        self.gdp_ref = c.gdppc(1990)
        gdef = cfg.get("demography", {}).get("gini_default", 0.42)
        self.mult = np.array([decile_income_multipliers((c.gini(y) / 100.0) if c.gini else gdef) for y in Y])
        self.lnmult = np.log(self.mult)
        self.lngdp = np.log(self.gdp / self.gdp_ref)

        dm = v5.get("driver_map", {})
        self.prem = np.zeros((len(Y), 4), dtype=float)
        self.prem[:, 1] = self.prem[:, 2] = self._driver(dm.get("premium_secondary", "premium_secondary"), 0.25)
        self.prem[:, 3] = self._driver(dm.get("premium_tertiary", "premium_tertiary"), 0.45)

        dc = v5["direct_costs_share_of_gdppc"]
        fe = v5["forgone_earnings_share_of_gdppc"]
        direct = np.zeros((len(Y), 4, 2), dtype=float)
        forgone = np.zeros((len(Y), 4), dtype=float)
        for li, name in enumerate(LEVEL_NAMES):
            direct[:, li, PUB] = dc[name]["public"]
            direct[:, li, PRIV] = dc[name]["private"]
            forgone[:, li] = fe[name]
        for ev in v5.get("policy_events", cfg.get("policy_events", [])):
            li = LEVEL_NAMES.index(ev["level"])
            si = PUB if ev["sector"] == "public" else PRIV
            delta = ev.get("direct_cost_change", ev.get("cost_change", 0.0))
            direct[Y >= ev["year"], li, si] += delta
        self.direct = np.maximum(direct, 0.002)
        self.forgone = forgone

        self.transfer = np.zeros((len(Y), 10, 4), dtype=float)
        for tr in cfg.get("transfers", []):
            ramp = np.clip((Y - tr["year"] + 1) / max(tr.get("ramp_years", 1), 1), 0.0, 1.0)
            for li in tr["levels"]:
                for d in tr["deciles"]:
                    self.transfer[:, d, LEVEL_NAMES.index(li)] += tr["value"] * ramp

        s6_pts = sorted((int(k), float(v)) for k, v in cfg["entry_age"]["share_at_6"].items() if not str(k).startswith("_"))
        self.s6 = np.array([np.interp(y, [q[0] for q in s6_pts], [q[1] for q in s6_pts]) for y in Y])

        self.b_lo = self.y0 - self.max_age - 2
        self.b_hi = self.y1
        self.cohort = np.array([c.survivors(b) for b in range(self.b_lo, self.b_hi + 1)], dtype=float)

        prm_age, sec_dur, prm_dur = c.wdi("SE.PRM.AGES"), c.wdi("SE.SEC.DURS"), c.wdi("SE.PRM.DURS")
        self.band = {}
        for y in Y:
            a0 = int(round(prm_age(y))) if prm_age else 6
            pd = int(round(prm_dur(y))) if prm_dur else 6
            sd = int(round(sec_dur(y))) if sec_dur else 6
            self.band[y] = dict(primary=(a0, a0 + pd), secondary=(a0 + pd, a0 + pd + sd), tertiary=(a0 + pd + sd, a0 + pd + sd + 5))

        xs = c.wdi("SE.XPD.TOTL.GD.ZS")
        self.pub_xpd = np.array([xs(y) for y in Y], dtype=float) / 100.0 if xs else np.full(len(Y), 0.035)
        self.cons_share = v5.get("household_consumption_share_of_gdp", 0.72)

        # Supply brakes: funded tertiary quota & self-financed capacity
        self.funded_quota_cfg = v5.get("funded_tertiary_quota")
        self.sf_cap_cfg = v5.get("self_financed_capacity")
        self.abroad_cost = float(v5.get("abroad_cost_share_of_gdppc", 0.90))

    def _pass_rate(self, y: int) -> float:
        if self.exam is None:
            return 1.0
        pts = self.exam["pts"]
        if y < pts[0][0]:
            return self.exam["default"] / 100.0
        return float(np.interp(y, [q[0] for q in pts], [q[1] for q in pts])) / 100.0

    def _tertiary_supply_caps(self, yi: int, y: int) -> tuple[float, float]:
        """Return (public_funded_seats, private_or_sf_seats) for new tertiary entrants in year y."""
        if self.mode == "steam_unbraked":
            return (1e12, 1e12)
        if self.funded_quota_cfg is not None:
            # Hong Kong explicit UGC funded quota + self-financed seats
            q_pub = _interp_dict(self.funded_quota_cfg, y)
            q_priv = _interp_dict(self.sf_cap_cfg, y) if self.sf_cap_cfg else 1e12
            return (q_pub, q_priv)
        # Philippines & Cambodia: fiscal-anchored public seat cap + elastic private capacity
        age_pop = self._pop_at_age(y, 18)
        if self.c.iso3 == "PHL":
            # Historical SUC/LUC public intake absorbs ~40-46% of tertiary entrants; private absorbs rest
            pub_share = 0.10 + 0.14 * np.clip((y - 1975) / 45.0, 0.0, 1.0)
            priv_share = 0.34 + 0.16 * np.clip((y - 1975) / 45.0, 0.0, 1.0)
            return (pub_share * age_pop, priv_share * age_pop)
        if self.c.iso3 == "KHM":
            # Cambodia: modest public seats + fee-charging private/public seats
            pub_share = 0.03 + 0.07 * np.clip((y - 1995) / 29.0, 0.0, 1.0)
            priv_share = 0.04 + 0.14 * np.clip((y - 1995) / 29.0, 0.0, 1.0)
            return (pub_share * age_pop, priv_share * age_pop)
        return (1e12, 1e12)

    def _pos_pull(self, s_val: float) -> float:
        """Saturating positional pull g(S) = S / (S + s0) in [0, 1)."""
        s0 = max(self.p["s0_sat"], 0.05)
        return float(s_val / (s_val + s0))

    def _base_u(self, yi: int, li: int, S: np.ndarray) -> np.ndarray:
        p = self.p
        return (
            p["b_h"] * self.prem[yi, li]
            + p["b_p"] * self._pos_pull(S[li])
            + p["eta_x"] * self.lnmult[yi]
        )

    def _sector_v(self, yi: int, li: int, S: np.ndarray) -> np.ndarray:
        p = self.p
        k = p["kappa"] * np.exp(-p["lam"] * self._pos_pull(S[li]))
        cost = p["c_scale"] * self.direct[yi, li, :][None, :] + self.forgone[yi, li]
        burden = np.maximum(cost - self.transfer[yi, :, li][:, None], 0.0) / self.mult[yi][:, None]
        v = -k * np.log1p(burden)
        if li == 3:
            v[:, PRIV] += p["mu_ter"] + p["nu_ter"] * (self.lngdp[yi] + self.lnmult[yi])
        else:
            v[:, PRIV] += p["mu_basic"] + p["nu_basic"] * (self.lngdp[yi] + self.lnmult[yi])
        return v

    def _latent_prob(self, yi: int, li: int, base: np.ndarray, V: np.ndarray, S: np.ndarray) -> np.ndarray:
        """Zero-direct-cost latent demand probability (guaranteed >= actual-cost demand)."""
        p = self.p
        k = p["kappa"] * np.exp(-p["lam"] * self._pos_pull(S[li]))
        free_burden = np.maximum(self.forgone[yi, li] / self.mult[yi], 0.0)
        free = np.repeat((-k * np.log1p(free_burden))[:, None], 2, axis=1)
        if li == 3:
            free[:, PRIV] += p["mu_ter"] + p["nu_ter"] * (self.lngdp[yi] + self.lnmult[yi])
        else:
            free[:, PRIV] += p["mu_basic"] + p["nu_basic"] * (self.lngdp[yi] + self.lnmult[yi])
        best = np.maximum(V, free)
        return _sig(base + np.logaddexp(best[:, PUB], best[:, PRIV]))

    def _pop_at_age(self, y: int, a: int) -> float:
        b = y - 1 - a
        return float(self.cohort[b - self.b_lo]) if self.b_lo <= b <= self.b_hi else 0.0

    def _band_pop(self, y: int, lo: int, hi: int) -> float:
        return sum(self._pop_at_age(y, a) for a in range(lo, hi))

    def run(self) -> V7Result:
        p = self.p
        Y = self.years
        nb = self.b_hi - self.b_lo + 1
        # Grade slots: 0-5 primary (6), 6-12 secondary (up to 7 grades for HK old system!), 13-16 tertiary (up to 4)
        N_G = 17
        E = np.zeros((nb, 10, N_G, 2), dtype=float)
        comp = np.zeros((nb, 10, 4), dtype=float)
        pool = np.zeros((nb, 10), dtype=float)
        notyet = np.full((nb, 10), 0.1, dtype=float)
        bidx = np.arange(self.b_lo, self.b_hi + 1)

        rc = self.cfg.get("repetition", {})
        rep = np.array([rc.get("primary", p["rep_prim"]), rc.get("secondary", p["rep_sec"]), rc.get("secondary", p["rep_sec"]), 0.0])
        a_w = np.array([p["a_prim"], p["a_sec"], p["a_sec"], p["a_ter"]])
        a_e = np.array([p["a_prim"], p["a_sec_entry"], p["a_sec_entry"], p["a_ter_entry"]])

        ind_names = [
            "ger_primary", "ner_primary", "ger_secondary", "ner_secondary", "ger_tertiary",
            "priv_primary", "priv_secondary", "priv_tertiary",
            "enrol_primary", "enrol_secondary", "enrol_tertiary",
            "trans_lsec_usec", "edu_share_hh", "hh_share_total_spending",
            "gradlr_primary", "gradlr_secondary", "gradlr_tertiary",
            "S_secondary", "S_tertiary",
        ]
        out = {k: np.full(len(Y), np.nan) for k in ind_names}

        bottlenecks = {k: np.zeros(len(Y)) for k in ("cohort_18", "qualified", "not_qualified", "no_demand", "priced_out", "blocked_by_gate_or_seats", "realized")}
        destinations = {k: np.zeros(len(Y)) for k in ("funded_local", "self_financed", "vocational_reroute", "abroad", "unmet_or_exit")}
        tutoring_log = {
            "part_overall": np.zeros(len(Y)),
            "part_by_decile": np.zeros((len(Y), 10)),
            "spend_share_hh": np.zeros(len(Y)),
            "funded_share_top20": np.zeros(len(Y)),
            "funded_share_bot20": np.zeros(len(Y)),
            "mean_h_skill": np.zeros(len(Y)),
            "mean_h_exam": np.zeros(len(Y)),
            "tightness": np.zeros(len(Y)),
        }

        S = np.zeros(4, dtype=float)
        is_hk = self.cycle_reform is not None
        hk_reform_yr = self.cycle_reform["year"] if is_hk else 10**6

        for yi, y in enumerate(Y):
            age = y - 1 - bidx
            alive = (age >= 5) & (age <= self.max_age)
            band20 = (age >= 20) & (age <= 29)
            w20 = self.cohort[band20]
            if w20.sum() > 0:
                for li in (0, 2, 3):
                    S[li] = float((comp[band20, :, li].sum(axis=1) * w20).sum() / w20.sum())
                S[1] = S[2]

            base = [self._base_u(yi, li, S) for li in range(4)]
            V = [self._sector_v(yi, li, S) for li in range(4)]
            IV = [np.logaddexp(v[:, PUB], v[:, PRIV]) for v in V]
            sp = [np.exp(v[:, PRIV] - iv) for v, iv in zip(V, IV)]

            newE = np.zeros_like(E)
            t1 = np.zeros((nb, 10), dtype=float)
            trans_num = trans_den = 0.0

            # Active secondary & tertiary terminal grades in year y
            if is_hk:
                sec_last_old = 12   # Form 7 (grade idx 12 = 7th sec year)
                sec_last_new = 11   # S6 (grade idx 11 = 6th sec year)
                ter_last = 15 if y < hk_reform_yr else 16  # 3-yr degree (13,14,15) vs 4-yr degree (13,14,15,16)
            else:
                sec_last_old = 5 + self.n_lower  # e.g. Grade 10 (idx 9) pre-K-12
                sec_last_new = 11                # Grade 12 (idx 11)
                ter_last = 16                    # 4-yr degree (13,14,15,16)

            for g in range(N_G):
                mass = E[:, :, g, :]
                if not mass.any():
                    continue
                if g <= 5:
                    li = 0
                elif g <= 5 + self.n_lower:
                    li = 1
                elif g <= 12:
                    li = 2
                else:
                    li = 3
                stay = mass * rep[li]
                passed = mass - stay
                pc = _sig(a_w[li] + base[li][:, None] + V[li])
                newE[:, :, g, :] += stay * pc[None]

                # Grade transitions
                if g == 5:
                    tot = passed.sum(axis=2)
                    comp[:, :, 0] += tot
                    pe1 = _sig(a_e[1] + base[1] + IV[1])
                    cont = tot * pe1[None]
                    newE[:, :, 6, PUB] += cont * (1.0 - sp[1])[None]
                    newE[:, :, 6, PRIV] += cont * sp[1][None]
                elif is_hk and g == sec_last_new and y >= hk_reform_yr:
                    # NSS S6 completers -> tertiary (includes 2012 double cohort!)
                    tot = passed.sum(axis=2)
                    comp[:, :, 2] += tot
                    t1 += tot
                elif is_hk and g == sec_last_old and y <= hk_reform_yr:
                    # Old system F7 completers -> tertiary (final F7 cohort exits in 2012 alongside first S6!)
                    tot = passed.sum(axis=2)
                    comp[:, :, 2] += tot
                    t1 += tot
                elif (not is_hk) and g == sec_last_old and y < self.shs_from:
                    tot = passed.sum(axis=2)
                    comp[:, :, 2] += tot
                    t1 += tot
                elif (not is_hk) and g == sec_last_old and y >= self.shs_from and sec_last_old < sec_last_new:
                    tot = passed.sum(axis=2)
                    pe2 = _sig(a_e[2] + base[2] + IV[2])
                    cont = tot * pe2[None]
                    newE[:, :, g + 1, PUB] += cont * (1.0 - sp[2])[None]
                    newE[:, :, g + 1, PRIV] += cont * sp[2][None]
                    trans_num += float((cont.sum(axis=1) * self.cohort).sum())
                    trans_den += float((tot.sum(axis=1) * self.cohort).sum())
                elif (not is_hk) and g == sec_last_new:
                    tot = passed.sum(axis=2)
                    comp[:, :, 2] += tot
                    t1 += tot
                elif g >= 13 and g >= ter_last:
                    tot = passed.sum(axis=2)
                    comp[:, :, 3] += tot
                elif g + 1 < N_G:
                    newE[:, :, g + 1, :] += passed * pc[None]

            out["trans_lsec_usec"][yi] = 100.0 * trans_num / trans_den if trans_den > 0 else np.nan

            # ---------------- Tertiary Entry, Multi-Destination & Shadow-Education Gate ----------------
            pe3 = _sig(a_e[3] + base[3] + IV[3])
            pe3_lat = self._latent_prob(yi, 3, a_e[3] + base[3], V[3], S)
            eligible = (age <= self.max_defer_age)[:, None]
            considered_def = pool * p["h_def"] * eligible

            qual_mass = t1 + considered_def  # (nb, 10)
            qual_persons_d = (qual_mass * self.cohort[:, None]).sum(axis=0)  # (10,)
            lat_persons_d = qual_persons_d * pe3_lat
            eff_persons_d = qual_persons_d * pe3

            # Exam gate (e.g., Cambodia Bac II or Hong Kong HKDSE)
            pr_exam = self._pass_rate(y)
            # Effective applicants passing exam gate vs. exam-blocked
            eff_pass_d = eff_persons_d * pr_exam
            exam_blocked_d = eff_persons_d * (1.0 - pr_exam)

            # Supply caps
            q_pub, q_priv = self._tertiary_supply_caps(yi, y)
            pub_e_s = float(self.pub_xpd[yi]) if np.isfinite(self.pub_xpd[yi]) else 0.035

            # Allocate funded public seats: via zero-sum tutoring gate when enabled & rationed, else proportional
            use_tut = self.tut_params.enabled and (self.c.iso3 in ("HKG", "KHM"))
            if use_tut:
                # Tutoring applies to effective applicants competing for funded seats
                tut_res = solve_exam_gate_tutoring(
                    applicants_by_decile=eff_pass_d,
                    funded_seats=q_pub,
                    income_mult=self.mult[yi],
                    public_spend_e_s=max(pub_e_s * 2.5, 0.08),
                    params=self.tut_params,
                    policy=self.tut_policy,
                )
                adm_pub_d = tut_res["admitted_funded"]
                spill_d = tut_res["spillover"]
                tut_spend_d = eff_persons_d * tut_res["tutoring_spend_per_student"]  # GDPpc-person units
                # Record tutoring diagnostics
                w_apps = eff_pass_d.sum()
                if w_apps > 0:
                    tutoring_log["part_overall"][yi] = 100.0 * float((eff_pass_d * tut_res["tutoring_part"]).sum() / w_apps)
                    tutoring_log["part_by_decile"][yi] = 100.0 * tut_res["tutoring_part"]
                    tutoring_log["mean_h_skill"][yi] = float((eff_pass_d * tut_res["h_skill"]).sum() / w_apps)
                    tutoring_log["mean_h_exam"][yi] = float((eff_pass_d * tut_res["h_exam"]).sum() / w_apps)
                    tutoring_log["tightness"][yi] = tut_res["tightness"]
                if adm_pub_d.sum() > 0:
                    tutoring_log["funded_share_top20"][yi] = 100.0 * float(adm_pub_d[8:].sum() / adm_pub_d.sum())
                    tutoring_log["funded_share_bot20"][yi] = 100.0 * float(adm_pub_d[:2].sum() / adm_pub_d.sum())
            else:
                tut_spend_d = np.zeros(10, dtype=float)
                # Standard two-sector conserved clearing
                dem_2 = np.stack([eff_pass_d * (1.0 - sp[3]), eff_pass_d * sp[3]], axis=1)
                adm_2, _ = clear_two_sector_array(dem_2, np.array([q_pub, q_priv]))
                adm_pub_d = adm_2[:, PUB]
                spill_d = np.maximum(eff_pass_d - adm_pub_d, 0.0)

            # Multi-destination spillover clearing for non-funded applicants (self-financed, abroad, vocational)
            if use_tut:
                # Self-financed local degrees / sub-degrees absorb spillover proportionally up to q_priv
                sf_dem_d = spill_d * _sig(0.8 - 1.2 * np.log1p(self.direct[yi, 3, PRIV] / self.mult[yi]))
                sf_tot = float(sf_dem_d.sum())
                sf_scale = min(1.0, q_priv / sf_tot) if sf_tot > 0 else 1.0
                adm_priv_d = sf_dem_d * sf_scale
                rem_after_sf_d = np.maximum(spill_d - adm_priv_d, 0.0)
            else:
                adm_priv_d = adm_2[:, PRIV]
                rem_after_sf_d = np.maximum(eff_pass_d - adm_pub_d - adm_priv_d, 0.0)

            # Study abroad option (prominent in Hong Kong for higher-income deciles)
            if self.c.iso3 == "HKG":
                p_abroad = _sig(-1.6 + 1.8 * self.lnmult[yi] - 1.2 * np.log1p(self.abroad_cost / self.mult[yi]))
                abroad_d = rem_after_sf_d * p_abroad
                rem_after_sf_d = np.maximum(rem_after_sf_d - abroad_d, 0.0)
            else:
                abroad_d = np.zeros(10, dtype=float)

            # Vocational / associate rerouting for exam-blocked candidates (e.g. Cambodia 2014 Bac II)
            voc_reroute_d = exam_blocked_d * p["reroute_propensity"]
            unmet_d = rem_after_sf_d + exam_blocked_d * (1.0 - p["reroute_propensity"])

            # Map realized domestic tertiary admissions (adm_pub_d, adm_priv_d) back onto cohort array proportionally
            total_dom_d = adm_pub_d + adm_priv_d
            # Fraction of each decile's qualified mass admitted to public / private domestic tertiary
            frac_pub = np.divide(adm_pub_d, qual_persons_d, out=np.zeros(10), where=qual_persons_d > 0)
            frac_priv = np.divide(adm_priv_d, qual_persons_d, out=np.zeros(10), where=qual_persons_d > 0)
            frac_tot = np.minimum(frac_pub + frac_priv, 1.0)
            newE[:, :, 13, PUB] += qual_mass * frac_pub[None, :]
            newE[:, :, 13, PRIV] += qual_mass * frac_priv[None, :]

            # Update deferral pool (strict conservation)
            ent_new = t1 * frac_tot[None, :]
            ent_def = considered_def * frac_tot[None, :]
            pool = np.maximum(pool - ent_def + (t1 - ent_new), 0.0)
            pool = pool * eligible

            # Record 4-bucket bottleneck decomposition & destinations
            c18 = self._pop_at_age(y, 18)
            q_tot = float(qual_persons_d.sum())
            l_tot = float(lat_persons_d.sum())
            e_tot = float(eff_persons_d.sum())
            r_tot = float((adm_pub_d + adm_priv_d + abroad_d + voc_reroute_d).sum())
            bottlenecks["cohort_18"][yi] = c18
            bottlenecks["qualified"][yi] = q_tot
            bottlenecks["not_qualified"][yi] = max(c18 - min(q_tot, c18), 0.0)
            bottlenecks["no_demand"][yi] = max(q_tot - l_tot, 0.0)
            bottlenecks["priced_out"][yi] = max(l_tot - e_tot, 0.0)
            bottlenecks["blocked_by_gate_or_seats"][yi] = max(e_tot - r_tot, 0.0)
            bottlenecks["realized"][yi] = r_tot

            destinations["funded_local"][yi] = float(adm_pub_d.sum())
            destinations["self_financed"][yi] = float(adm_priv_d.sum())
            destinations["vocational_reroute"][yi] = float(voc_reroute_d.sum())
            destinations["abroad"][yi] = float(abroad_d.sum())
            destinations["unmet_or_exit"][yi] = float(unmet_d.sum())

            # ---------------- Grade 1 entrants ----------------
            s6n, s61, s62 = self.s6[yi], self.s6[max(yi - 1, 0)], self.s6[max(yi - 2, 0)]
            lam_l = p["late"]
            share_at = {6: s6n * (1.0 - lam_l), 7: (1.0 - s61) * (1.0 - lam_l) + s61 * lam_l, 8: (1.0 - s62) * lam_l}
            pe0 = _sig(a_e[0] + base[0] + IV[0])
            for a, sh in share_at.items():
                m = age == a
                if m.any():
                    e = 0.1 * sh * pe0[None]
                    notyet[m] = np.maximum(notyet[m] - e, 0.0)
                    newE[m, :, 0, PUB] += e * (1.0 - sp[0])[None]
                    newE[m, :, 0, PRIV] += e * sp[0][None]
            hz = np.zeros(nb)
            if self.late_hazard > 0:
                hz[(age >= 9) & (age <= self.late_max_age)] = self.late_hazard
            if self.catch_up and self.catch_up["years"][0] <= y <= self.catch_up["years"][1]:
                mm = (age >= 7) & (age <= self.catch_up["max_age"])
                hz[mm] = np.maximum(hz[mm], self.catch_up["rate"])
            if hz.any():
                e = notyet * hz[:, None] * pe0[None]
                notyet = np.maximum(notyet - e, 0.0)
                newE[:, :, 0, PUB] += e * (1.0 - sp[0])[None]
                newE[:, :, 0, PRIV] += e * sp[0][None]

            pool[~alive] = 0.0
            newE[~alive] = 0.0
            E = newE

            # ---------------- Record indicators ----------------
            persons = E * self.cohort[:, None, None, None]
            bands = self.band[y]
            slices = dict(primary=slice(0, 6), secondary=slice(6, 13), tertiary=slice(13, 17))
            for lev, sl in slices.items():
                lo, hi = bands[lev]
                pop = self._band_pop(y, lo, hi)
                enr = float(persons[:, :, sl, :].sum())
                out[f"ger_{lev}"][yi] = 100.0 * enr / pop if pop > 0 else np.nan
                out[f"enrol_{lev}"][yi] = enr
                if lev != "tertiary":
                    on = (age >= lo) & (age < hi)
                    out[f"ner_{lev}"][yi] = 100.0 * float(persons[on][:, :, sl, :].sum()) / pop if pop > 0 else np.nan
                out[f"priv_{lev}"][yi] = 100.0 * float(persons[:, :, sl, PRIV].sum()) / enr if enr > 0 else np.nan
                pop_d = pop / 10.0
                if pop_d > 0:
                    byd = persons[:, :, sl, :].sum(axis=(0, 2, 3)) / pop_d
                    out[f"gradlr_{lev}"][yi] = 10.0 * np.log(max(byd[9], 1e-12) / max(byd[0], 1e-12))

            out["S_secondary"][yi], out["S_tertiary"][yi] = S[2], S[3]

            # Household spending (formal schooling + shadow-education tutoring)
            cdir = p["c_scale"] * self.direct[yi]
            spend_d = np.zeros(10, dtype=float)
            for g in range(N_G):
                li = 0 if g <= 5 else (1 if g <= 5 + self.n_lower else (2 if g <= 12 else 3))
                spend_d += (persons[:, :, g, :] * cdir[li][None, None, :]).sum(axis=(0, 2))
            spend_d += tut_spend_d
            total_pop = self.c.pop(y)
            cons_d = self.cons_share * self.mult[yi] * total_pop / 10.0
            out["edu_share_hh"][yi] = 100.0 * float(spend_d.sum() / cons_d.sum())
            tutoring_log["spend_share_hh"][yi] = 100.0 * float(tut_spend_d.sum() / cons_d.sum())
            hh_gdp = float(spend_d.sum() / total_pop)
            pub = self.pub_xpd[yi]
            out["hh_share_total_spending"][yi] = 100.0 * hh_gdp / (hh_gdp + pub) if np.isfinite(pub) else np.nan

        return V7Result(Y, out, bottlenecks, destinations, tutoring_log, extra=dict(params=dict(self.p), mode=self.mode))


def fit_v7(country: Country, train_rows: list[dict], fit_names: list[str], mode: str = "steam_braked", start: dict | None = None, max_nfev: int = 120) -> dict:
    """Fit a parsimonious, sign-constrained v7 parameter subset to training rows."""
    base = dict(V7_DEFAULTS)
    if start:
        base.update({k: v for k, v in start.items() if k in base})
    model = LabModelV7(country, base, mode=mode)
    lo = np.array([V7_BOUNDS[n][0] for n in fit_names], dtype=float)
    hi = np.array([V7_BOUNDS[n][1] for n in fit_names], dtype=float)
    x0 = np.array([np.clip(base[n], V7_BOUNDS[n][0], V7_BOUNDS[n][1]) for n in fit_names], dtype=float)
    obs = np.array([r["value"] for r in train_rows], dtype=float)

    counts = {}
    for r in train_rows:
        counts[r["series"]] = counts.get(r["series"], 0) + 1
    scale = np.array([10.0 if r["series"].startswith("edu_share") else 1.0 for r in train_rows], dtype=float)
    w = np.array([1.0 / np.sqrt(counts[r["series"]]) for r in train_rows], dtype=float) * scale

    yrs_list = list(model.years)
    y_idx = [yrs_list.index(r["year"]) for r in train_rows]
    s_names = [r["series"] for r in train_rows]

    def resid(x):
        prm = dict(base)
        prm.update(dict(zip(fit_names, x)))
        res = model.set_params(prm).run()
        pred = np.array([res.ind[s][i] for s, i in zip(s_names, y_idx)], dtype=float)
        return np.nan_to_num((pred - obs) * w, nan=50.0)

    sol = least_squares(resid, x0, bounds=(lo, hi), x_scale="jac", max_nfev=max_nfev, diff_step=2e-3, ftol=1e-6, xtol=1e-6)
    prm = dict(base)
    prm.update(dict(zip(fit_names, sol.x)))
    at_bounds = [n for n, v in zip(fit_names, sol.x) if abs(v - V7_BOUNDS[n][0]) < 1e-3 or abs(v - V7_BOUNDS[n][1]) < 1e-3]
    return dict(params=prm, fitted=fit_names, cost=float(sol.cost), nfev=int(sol.nfev), mode=mode, at_bounds=at_bounds)


def recover_v7(country: Country, train_rows: list[dict], fit_names: list[str], truth: dict, mode: str = "steam_braked", replicates: int = 12, max_nfev: int = 80) -> dict:
    """Honest synthetic parameter recovery: flags boundary-censored parameters instead of calling them identified."""
    model = LabModelV7(country, truth, mode=mode)
    base_res = model.run()
    yrs_list = list(model.years)
    synth = [float(base_res.ind[r["series"]][yrs_list.index(r["year"])]) for r in train_rows]
    rng = np.random.default_rng(7072026)
    fits = []
    for _ in range(replicates):
        pert = []
        for r, val in zip(train_rows, synth):
            sd = 0.1 if r["series"].startswith("edu_share") else 1.0
            q = dict(r)
            q["value"] = float(val + rng.normal(0.0, sd))
            pert.append(q)
        fits.append(fit_v7(country, pert, fit_names, mode=mode, start=truth, max_nfev=max_nfev))

    report = {}
    for n in fit_names:
        vals = np.array([f["params"][n] for f in fits], dtype=float)
        b_val = float(truth[n])
        b_hits = sum(n in f["at_bounds"] for f in fits)
        if b_hits / replicates > 0.25:
            status = "boundary_censored (not cleanly identified)"
            within = float(np.mean(np.abs(vals - b_val) <= 0.25 * max(abs(b_val), 1e-6)))
        elif abs(b_val) < 1e-6:
            status = "not identified (zero truth)"
            within = None
        else:
            within = float(np.mean(np.abs(vals - b_val) <= 0.25 * abs(b_val)))
            status = "identified" if within >= 0.80 else "not identified"
        report[n] = dict(
            truth=b_val,
            median=float(np.median(vals)),
            q05=float(np.quantile(vals, 0.05)),
            q95=float(np.quantile(vals, 0.95)),
            within_25pct=within,
            bound_hits=int(b_hits),
            replicates=replicates,
            status=status,
        )
    return report
