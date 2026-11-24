"""Shadow-education (private supplementary tutoring) demand attached to MASSENG v5.

Provenance
----------
Ported from the first-pass standalone shadow-education model on branch
``research/shadow-equations-2026-11-25`` (record dir ``research/records/2026-11-25-shadow-equations/``):
``shadow_model.py`` and ``bray_reality_check.py`` at head ``fdc8da0``.  The copies used here live in
``research/records/2026-11-25-masseng-tutoring/ported/``; this module is a PORT, not an import across branches.

What is ported unchanged (household demand block only)
-----------------------------------------------------
The four-option multinomial logit over ``none / own-teacher / other-teacher / commercial`` (inventory equations
23, 57-63; budget 70; spending 64-69), with
    u_none = 0
    u_k    = b0 + level_tilt[L] + b_income * log(household income)
             + b_quality * (1 - q_L)                     # low school quality -> remedial demand
             - price_k * fee + provider_offset_k         # fee exogenous; own-teacher premium
    P      = softmax(u_none, u_own, u_other, u_commercial)
    participation      = 1 - P_none
    provider shares    = P_k / participation
    spending per pupil = fee_ref * fee * sum_k price_k * P_k          (share of GDP per capita)
A ban on own-teacher tutoring removes the option (u_own = -inf), exactly as the standalone ``ban_own`` did.

Declared changes forced by the engine (all stated again in MASSENG_TUTORING_COUPLING.md)
---------------------------------------------------------------------------------------
* ``ability``, the household's individual school-quality draw ``q_i``, ``teacher_q`` and ``urban`` are DROPPED:
  MASSENG v5 holds no individuals, no ability, no school-quality state and no urban/rural dimension.
* ``q_L`` becomes a declared level-specific school-quality PROXY from an external series (see
  ``quality_proxy``); it is a resource proxy, not a measured learning outcome.
* The standalone's grade-9 / grade-12 intercept bonuses become ``level_tilt`` for the engine's four levels.
* Household income is the engine's decile income, ``log(GDPpc_y * decile_multiplier_d)``; the constant
  ``log(GDPpc_1990)`` is absorbed in ``b0``.
* The EXOGENOUS tutoring fee is in the standalone's fee units (standalone reference fee = 1.0); the grid scales
  it 0.5 / 1.0 / 2.0.  A declared reference fee of ``fee_ref`` of GDP per capita converts fee units to money.
* The CES learning-production equations (26, 28, 30-31, 71-75) are NOT ported into the engine: MASSENG v5 has
  no learning production.  Instead the tutoring effect enters the engine's EXISTING linear transition index as a
  declared achievement shift, ``delta_{y,d,L} = participation_{y,d,L} * log(odds_multiplier)`` added to
  ``base[L]`` (the same index that feeds the within-level progression probability ``pc`` and level-entry
  probability ``pe``).  No score equation is invented.  ``odds_multiplier`` is declared, not estimated.

Coupling direction
------------------
tutoring demand -> engine: (i) the declared achievement shift raises the existing progression/entry
probabilities; (ii) expected tutoring outlay enters the engine's existing household cost/burden term
(``-kappa*log(1+burden)``), so financing competes with continuation.  There is NO feedback from engine state
back into tutoring demand, so the demand block is exogenous given the income distribution; that is a declared
first-pass restriction, not an estimated structure.

Accounting and open deviations (Neon audit items, declared here rather than silently changed)
----------------------------------------------------------------------------------------------
* Household spending is reported as two single-counted flows: (i) the fitted direct-cost schedule and (ii) the
  declared tutoring outlay.  In the financing arm (``spend_feedback=True``) the outlay is declared ADDITIONAL to
  the fitted schedule and the reported total is schedule + outlay; in the learning-only arm
  (``spend_feedback=False``) the fitted ``c_scale`` schedule is read as all-in (it was matched to FIES *total*
  household education spending, which already contains shadow-education outlays), so the reported total is the
  schedule only and the outlay is reported separately -- it is not added twice.  ``spend_school_share_gdp``,
  ``spend_total_share_gdp`` and ``edu_share_hh_incl_tut`` expose the decomposition.
* The MNL price/option mapping against the Bray reality check is an OPEN deviation: the port is four-option with
  ``price_other = 0.8`` while the fitted check used three options with a 0.5 price coefficient on the
  other-teacher option, plus a commercial option absent from the fit.  The claim text is unchanged;
  ``bray_mapping_gap()`` measures the gap.

Window labels (Neon audit item "1940-2024 label error")
-------------------------------------------------------
The engine SIMULATES 1940-2024 (85 years); 1940-1959 are back-cast from 1960 WDI levels using the configured
pre-data growth, NOT observed data.  Observed series used by the PHL fit span 1960-2025 (macro) and 1971-2020/2024
(education enrolment/private), Gini 1985-2023; the fit windows are train 1971-1995 and test 1996-2024
(``countries/PHL/config.json``).  Records must say "simulated 1940-2024, observed data 1960-2024" and must not
call 1940-2024 the data window.  ``SIMULATED_WINDOW`` / ``OBSERVED_DATA_WINDOW`` / ``FIT_WINDOWS`` hold the
declared labels; ``tests/test_tutoring_fixes.py`` checks them against the config and the loaded series.

Switch
------
``switches={'tutoring': False}`` (default) must be bit-identical to the untouched ``Model5``.  Every override
here returns ``super()`` unchanged when the switch is off; the test suite checks the identity.
"""
from dataclasses import dataclass, replace
from typing import Dict, Optional

import numpy as np

from .engine5 import Model5, LEVEL_NAMES, PRIV

# Declared window labels (see module docstring, "Window labels"): the engine's simulation window comes from
# v5.years; observed data coverage of the PHL series used by the fit is macro 1960+ / education 1971+; the fit
# windows come from the PHL config years.  The record must not call 1940-2024 the *data* window.
SIMULATED_WINDOW = (1940, 2024)
OBSERVED_DATA_WINDOW = (1960, 2024)
FIT_WINDOWS = {"train": (1971, 1995), "test": (1996, 2024)}

# Declared demand mappings (OPEN deviation, Neon audit item "MNL price/option mismatch vs Bray").  The bray_8k
# parameter vector was FITTED under BRAY_CHECK_MAPPING; the port implements PORT_MAPPING (four options, full
# price_other, plus a commercial option absent from the fit).  The claim text is unchanged; use
# bray_mapping_gap() to measure the difference.
BRAY_CHECK_MAPPING = {
    "options": ("none", "own", "other"),
    "own_price_coef": 1.0,
    "other_price_coef": 0.5,
    "commercial_option": False,
    "source": "research/records/2026-11-25-masseng-tutoring/ported/bray_reality_check.py:87-93",
}
PORT_MAPPING = {
    "options": ("none", "own", "other", "commercial"),
    "own_price_coef": "price_own (default 1.0)",
    "other_price_coef": "price_other (default 0.8)",
    "commercial_option": True,
    "source": "masseng/tutoring.py _level_utilities (four-option shadow_model.py structure)",
}


# ----------------------------------------------------------------------------- parameters
@dataclass
class TutoringParams:
    """Illustrative tutoring-demand parameters.

    Defaults are the closest-to-Bray demand parameter vector from the standalone demand-mix
    check (``bray_reality_check.json`` best draw at branch head ``fdc8da0``): it reproduces the seven
    published Bray et al. (2016, 2018) Siem Reap patterns up to max |z| = 1.14 in 8k prior draws
    (no draw fits all seven within 1.0 tolerance).  These are ILLUSTRATIVE, not estimates, and they are
    Cambodian, not Philippine.  ``b0`` is usually re-calibrated to the PHL survey level in the coupled runs.
    """
    b0: float = 0.9171                 # shared tutoring intercept (bray 8k best draw)
    b_income: float = 0.6002           # log household income (bray 8k best; shadow b_income)
    b_quality: float = 1.3919          # (1 - school quality) remedial term (bray b_school_gap)
    own_premium: float = 0.1485        # own-teacher premium (bray own_premium)
    other_premium: float = 0.6330      # other-provider premium (bray other_premium)
    cost_other: float = 1.2938         # non-price cost of the other-teacher option (bray cost_other)
    cost_commercial: float = 1.0       # shadow_model.py default
    price_own: float = 1.0             # shadow_model.py default (reference fee = 1.0)
    price_other: float = 0.8           # shadow_model.py default
    price_commercial: float = 1.5      # shadow_model.py default
    level_tilt: Dict[str, float] = None    # set in __post_init__ from the bray grade-9/grade-12 bonuses
    fee: float = 1.0                   # fee scale in standalone fee units; grid {0.5, 1.0, 2.0}
    fee_ref: float = 0.03              # declared reference fee: share of GDP per capita per tutored pupil-year
    ban_own: bool = False              # remove the own-teacher option (u_own = -inf)
    learning: bool = True              # switch the declared achievement-shift channel on/off
    odds_multiplier: float = 1.10      # declared odds multiplier on existing transition probabilities
    spend_feedback: bool = True        # tutoring outlay enters the engine's household burden term
    label: str = ''

    def __post_init__(self):
        if self.level_tilt is None:
            # bray 8k best: grade9_bonus 0.1715, grade12_bonus 0.6677; primary=no bonus;
            # tertiary (post-K12 upper secondary gate) uses the grade-12 tilt.
            self.level_tilt = {'primary': 0.0, 'secondary': 0.1715, 'upper_secondary': 0.6677,
                               'tertiary': 0.6677}

    @classmethod
    def from_bray_draw(cls, row, label='bray_50k_best'):
        """Build parameters from one draw of the standalone demand-mix check (the near-fit anchor).

        ``row`` is one record of the ported ``bray_reality_check.py`` result: it carries ``b0``,
        ``b_income``, ``b_school_gap`` (-> our ``b_quality``), ``own_premium``, ``other_premium``,
        ``cost_other``, ``grade9_bonus`` (-> lower-secondary tilt) and ``grade12_bonus``
        (-> upper-secondary/tertiary tilt).  Dropped-by-engine variables (``b_ability``,
        ``teacher_threshold``, ``urban_demand``) are NOT used.
        """
        return cls(
            b0=float(row['b0']), b_income=float(row['b_income']), b_quality=float(row['b_school_gap']),
            own_premium=float(row['own_premium']), other_premium=float(row['other_premium']),
            cost_other=float(row['cost_other']),
            level_tilt={'primary': 0.0, 'secondary': float(row['grade9_bonus']),
                        'upper_secondary': float(row['grade12_bonus']),
                        'tertiary': float(row['grade12_bonus'])},
            label=label)

    def perturbed(self, rng, band=0.20):
        """One declared uncertainty draw: every unestimated demand parameter moves by U(1-band, 1+band).

        MASSENG v5 is deterministic (no random draws), so a "seed" here is a draw from the declared
        parameter-uncertainty band, NOT sampling uncertainty.
        """
        out = replace(self)
        # b0 is the single calibrated intercept and is re-solved inside the model for every draw, so it is not
        # perturbed here; the draw perturbs the unestimated *shape* parameters only.
        for name in ('b_income', 'b_quality', 'own_premium', 'other_premium', 'cost_other'):
            setattr(out, name, float(getattr(self, name) * (1.0 + band * (2.0 * rng.random() - 1.0))))
        return out


def bray_mapping_gap(tut_params=None, fee=None):
    """Utility-term gap between the ported MNL mapping and the mapping the Bray vector was fitted under.

    OPEN deviation (Neon audit item "MNL price/option mismatch vs Bray"): the bray_8k parameter vector comes from
    ``ported/bray_reality_check.py``, whose three-option mapping charged the other-teacher option
    ``0.5 * price_fee`` and had no commercial option.  The port (``_level_utilities``) charges
    ``price_other * fee`` (default 0.8) and adds a commercial option.  This helper measures the difference for the
    own/other price terms; positive values are more expensive than the fit specification.  It does NOT change any
    default behaviour or claim text -- the deviation is left open until the vector is re-fitted in the port
    specification or the claim is amended.
    """
    tp = tut_params if tut_params is not None else TutoringParams()
    f = float(tp.fee if fee is None else fee)
    own_port = -tp.price_own * f
    own_fit = -BRAY_CHECK_MAPPING["own_price_coef"] * f
    other_port = -tp.price_other * f
    other_fit = -BRAY_CHECK_MAPPING["other_price_coef"] * f
    return {
        "fee": f,
        "own_port": own_port, "own_fit": own_fit, "own_gap": own_port - own_fit,
        "other_port": other_port, "other_fit": other_fit, "other_gap": other_port - other_fit,
        "commercial_option_port": PORT_MAPPING["commercial_option"],
        "commercial_option_fit": BRAY_CHECK_MAPPING["commercial_option"],
        "bray_check_mapping": dict(BRAY_CHECK_MAPPING),
        "port_mapping": dict(PORT_MAPPING),
    }


# ----------------------------------------------------------------------------- helpers
def _softmax(V):
    V = np.asarray(V, float)
    V = V - V.max(axis=-1, keepdims=True)
    E = np.exp(V)
    return E / E.sum(axis=-1, keepdims=True)


def _series_values(c, code, years):
    """Exogenous series over the simulation years, flat-extrapolated by the Series object."""
    s = c.wdi(code)
    if s is None:
        return None
    return np.array([float(s(y)) for y in years])


def quality_proxy(c, years, band, pop_fn, kind='spend'):
    """Declared level-specific school-quality PROXY, shape (n_years, 4), values in [0, 1].

    'spend'   : WDI government expenditure per pupil as % of GDP per capita
                (SE.XPD.PRIM/SECO/TERT.PC.ZS, observed 1997-2009, flat outside), q = clip(x/30, 0, 1).
                Upper secondary uses the secondary series (no separate WDI series).
    'teachers': teacher provision, teachers / school-age population in the level's official band
                (SE.PRM.TCHR, SE.SEC.TCHR, 1971-2024), q = clip((r - 0.02) / 0.03, 0, 1).
                Tertiary falls back to the secondary ratio (no WDI tertiary teacher series).
    Both are RESOURCE proxies for school quality; the repo has no PHL learning-outcome series.
    ``pop_fn(y, lo, hi)`` returns the population in the official age band (Model5._band_pop).
    """
    n = len(years)
    q = np.zeros((n, 4))
    if kind == 'spend':
        for li, code in enumerate(('SE.XPD.PRIM.PC.ZS', 'SE.XPD.SECO.PC.ZS', 'SE.XPD.SECO.PC.ZS',
                                   'SE.XPD.TERT.PC.ZS')):
            vals = _series_values(c, code, years)
            if vals is None:
                raise RuntimeError(f'quality proxy series {code} missing')
            q[:, li] = np.clip(vals / 30.0, 0.0, 1.0)
        return q
    if kind == 'teachers':
        tp = _series_values(c, 'SE.PRM.TCHR', years)
        ts = _series_values(c, 'SE.SEC.TCHR', years)
        if tp is None or ts is None:
            raise RuntimeError('teacher count series missing')
        pop_p = np.array([pop_fn(y, *band[y]['primary']) for y in years])
        pop_s = np.array([pop_fn(y, *band[y]['secondary']) for y in years])
        r_p = np.divide(tp, pop_p, out=np.zeros_like(tp), where=pop_p > 0)
        r_s = np.divide(ts, pop_s, out=np.zeros_like(ts), where=pop_s > 0)
        q[:, 0] = np.clip((r_p - 0.02) / 0.03, 0.0, 1.0)
        q[:, 1] = q[:, 2] = np.clip((r_s - 0.02) / 0.03, 0.0, 1.0)
        q[:, 3] = q[:, 1]
        return q
    raise ValueError(kind)


# ----------------------------------------------------------------------------- model subclass
class TutoringModel5(Model5):
    """MASSENG v5 demand engine with a switchable shadow-education demand block.

    ``switches={'tutoring': True}`` turns the block on.  Default is OFF and is required to reproduce
    ``Model5`` bit-identically (checked by ``verify_switch_off.py``).
    """

    def __init__(self, country, params=None, spec='R1', switches=None, tut_params: Optional[TutoringParams] = None,
                 quality='spend', calibrate_b0_to=None):
        """
        Parameters
        ----------
        calibrate_b0_to : (year, target_participation) or None
            If given, solve ``b0`` so that the mean of primary and lower-secondary participation in
            ``year`` equals ``target_participation``.  One parameter, one declared target; the two grades
            are then read as an external check, not as calibration.
        """
        super().__init__(country, params=params, spec=spec, switches=switches)
        self.tutp = tut_params if tut_params is not None else TutoringParams()
        self.tut_on = bool(self.sw.get('tutoring', False))
        self.quality_kind = quality
        self.tut_panel = {}
        self.tut_b0 = None
        if not self.tut_on:
            self.tut_prob = None
            self.tut_part = None
            self.tut_spend = None
            self.tut_delta = None
            return
        q = quality_proxy(self.c, self.years, self.band, self._band_pop, kind=quality)
        self.tut_quality = q
        self._build_demand(calibrate_b0_to)

    # ------------------------------------------------------------------ demand construction
    def _level_utilities(self, b0, tp):
        """Utilities of the four options, shape (n_years, 10, 4, 4), shape[-1] = none/own/other/commercial."""
        n = len(self.years)
        z_inc = self.lngdp[:, None] + self.lnmult                        # (n, 10) log decile income vs 1990
        shared = (tp.b_income * z_inc[:, :, None]
                  + tp.b_quality * (1.0 - self.tut_quality)[:, None, :])  # (n, 10, 4)
        for li, name in enumerate(LEVEL_NAMES):
            shared[:, :, li] += tp.level_tilt[name]
        V = np.zeros((n, 10, 4, 4))
        off_own = tp.own_premium - tp.price_own * tp.fee
        off_other = tp.other_premium - tp.cost_other - tp.price_other * tp.fee
        off_com = -tp.cost_commercial - tp.price_commercial * tp.fee
        V[..., 1] = b0 + shared + off_own
        V[..., 2] = b0 + shared + off_other
        V[..., 3] = b0 + shared + off_com
        if tp.ban_own:
            V[..., 1] = -np.inf
        return V

    def _build_demand(self, calibrate_b0_to):
        tp = self.tutp
        b0 = tp.b0
        if calibrate_b0_to is not None:
            year, target = calibrate_b0_to
            # Calibrate the intercept ONCE under the REFERENCE (no-policy) demand: fee = 1.0, no ban.  Every
            # policy/seed arm then holds the calibrated parameters fixed, so fee and ban are genuine
            # perturbations rather than being absorbed by a re-solved intercept.
            b0 = self._solve_b0(year, target, replace(tp, fee=1.0, ban_own=False))
        V = self._level_utilities(b0, tp)
        probs = _softmax(V)
        part = 1.0 - probs[..., 0]
        spend = tp.fee_ref * tp.fee * (probs[..., 1] * tp.price_own
                                       + probs[..., 2] * tp.price_other
                                       + probs[..., 3] * tp.price_commercial)
        self.tut_b0 = float(b0)
        self.tut_prob = probs
        self.tut_part = part
        self.tut_spend = spend
        self.tut_delta = (np.log(tp.odds_multiplier) * part) if tp.learning else np.zeros_like(part)

    def _solve_b0(self, year, target, tp):
        yi = int(np.searchsorted(self.years, year))
        if yi >= len(self.years) or self.years[yi] != year:
            raise ValueError(f'calibration year {year} not in simulation years')
        lo, hi = -20.0, 20.0

        def mean_part(b0):
            V = self._level_utilities(b0, tp)
            probs = _softmax(V)
            part = 1.0 - probs[yi, :, :, 0]          # (10 deciles, 4 levels)
            return 0.5 * (part[:, 0].mean() + part[:, 1].mean())

        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if mean_part(mid) < target:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    # ------------------------------------------------------------------ engine hooks
    def _base(self, yi, li, S):
        b = super()._base(yi, li, S)
        if self.tut_on and self.tutp.learning:
            return b + self.tut_delta[yi][:, li]
        return b

    def _v(self, yi, li, S):
        if not (self.tut_on and self.tutp.spend_feedback):
            return super()._v(yi, li, S)
        p = self.p
        z = S[li] if self.zsrc == 'S' else (self.R[yi] if self.zsrc == 'R' else 0.0)
        k = p['kappa'] * np.exp(-p['lam'] * z)
        cost = (p['c_scale'] * self.direct[yi, li, :][None, :] + self.forgone[yi, li]
                + self.tut_spend[yi][:, li][:, None])
        burden = (cost - self.transfer[yi, :, li][:, None]).clip(0.0) / self.mult[yi][:, None]
        v = -k * np.log1p(burden)
        v[:, PRIV] += (p['mu_ter'] if li == 3 else p['mu_basic']) + p['nu'] * (self.lngdp[yi] + self.lnmult[yi])
        return v

    # ------------------------------------------------------------------ outputs
    def run(self, record_deciles=False):
        self.tut_panel = {}
        res = super().run(record_deciles=record_deciles)
        res.extra['tutoring'] = dict(
            switch=self.tut_on, params={k: v for k, v in self.tutp.__dict__.items()},
            b0_used=getattr(self, 'tut_b0', None), quality_proxy=self.quality_kind,
            panel=self.tut_panel)
        return res

    def _record(self, out, yi, y, E, age, S, pool, record_deciles, dec_part):
        super()._record(out, yi, y, E, age, S, pool, record_deciles, dec_part)
        if not self.tut_on:
            return
        persons = E * self.cohort[:, None, None, None]
        lvl = self.level_of_grade
        n_years = len(self.years)
        # enrolled persons by decile at each of the engine's four levels
        persons_li = np.zeros((4, 10))
        for li in range(4):
            sel = (lvl == li)
            persons_li[li] = persons[:, :, sel, :].sum(axis=(0, 2, 3)) if sel.any() else 0.0
        part = self.tut_part[yi]                      # (10, 4)
        prob = self.tut_prob[yi]                      # (10, 4, 4)
        # ---- household spending: TWO declared flows, each counted exactly once (Neon audit item
        # "_record() spend double-count").  Flow 1 = fitted direct-cost schedule (public/private fees) x enrolled
        # persons (mirrors Model5._record).  Flow 2 = declared tutoring outlay.
        cdir = self.p['c_scale'] * self.direct[yi]
        spend_school_d = np.zeros(10)
        for g in range(16):
            spend_school_d += (persons[:, :, g, :] * cdir[lvl[g]][None, None, :]).sum(axis=(0, 2))
        # tutoring outlay (GDPpc units) by decile: enrolled pupils x expected spend per pupil at that level
        spend_tut_d = (persons_li * self.tut_spend[yi].T).sum(axis=0)   # sum over levels -> (10,)
        # The fitted c_scale was matched to FIES *total* household education spending, which already contains
        # shadow-education outlays (MASSENG_TUTORING_COUPLING.md section 3.1).  In the learning-only arm
        # (spend_feedback=False) the schedule is read as all-in, so adding the outlay on top would count the same
        # household spending twice: the reported total is the schedule only.  In the financing arm the outlay is a
        # declared ADDITIONAL flow and is added exactly once.
        spend_incl_d = spend_school_d + spend_tut_d       # declared all-in total, always one of each flow
        spend_d = spend_incl_d if (self.tut_on and self.tutp.spend_feedback) else spend_school_d
        total_pop = self.c.pop(y)
        cons_d = self.cons_share * self.mult[yi] * total_pop / 10.0
        out['edu_share_hh'][yi] = 100 * spend_d.sum() / cons_d.sum()
        out['edu_share_bottom30'][yi] = 100 * spend_d[:3].sum() / cons_d[:3].sum()
        out['edu_share_top70'][yi] = 100 * spend_d[3:].sum() / cons_d[3:].sum()
        out['edu_share_d1'][yi] = 100 * spend_d[0] / cons_d[0]
        out['edu_share_d10'][yi] = 100 * spend_d[9] / cons_d[9]
        hh_gdp = spend_d.sum() / total_pop
        pub = self.pub_xpd[yi]
        out['hh_share_total_spending'][yi] = 100 * hh_gdp / (hh_gdp + pub) if pub == pub else np.nan
        # tutoring aggregate indicators (+ the declared single-count decomposition)
        for key in ('tut_participation', 'tut_own_share', 'tut_other_share', 'tut_commercial_share',
                    'tut_spend_share_gdp', 'tut_spend_share_hh_edu', 'tut_participation_gap_q5_q1',
                    'spend_school_share_gdp', 'spend_total_share_gdp', 'spend_incl_share_gdp',
                    'edu_share_hh_incl_tut'):
            if key not in out:
                out[key] = np.full(n_years, np.nan)
        den = float(persons_li.sum())
        num = float((persons_li * part.T).sum())          # tutored person-years (denominator for provider mix)
        out['tut_participation'][yi] = num / den if den > 0 else np.nan
        # provider shares among TUTORED pupils: sum over cells of (enrolled x P(provider)), divided by tutored mass
        out['tut_own_share'][yi] = float((persons_li * prob[..., 1].T).sum() / num) if num > 0 else np.nan
        out['tut_other_share'][yi] = float((persons_li * prob[..., 2].T).sum() / num) if num > 0 else np.nan
        out['tut_commercial_share'][yi] = float((persons_li * prob[..., 3].T).sum() / num) if num > 0 else np.nan
        out['tut_spend_share_gdp'][yi] = 100.0 * spend_tut_d.sum() / total_pop
        out['spend_school_share_gdp'][yi] = 100.0 * spend_school_d.sum() / total_pop
        out['spend_total_share_gdp'][yi] = 100.0 * spend_d.sum() / total_pop
        out['spend_incl_share_gdp'][yi] = 100.0 * spend_incl_d.sum() / total_pop
        out['edu_share_hh_incl_tut'][yi] = 100.0 * spend_incl_d.sum() / cons_d.sum()
        out['tut_spend_share_hh_edu'][yi] = (100.0 * spend_tut_d.sum() / spend_incl_d.sum()
                                             if spend_incl_d.sum() > 0 else np.nan)
        # participation gap richest vs poorest income quintile (enrolled-weighted)
        byd = (persons_li * part.T).sum(axis=0) / np.maximum(persons_li.sum(axis=0), 1e-12)
        w = persons_li.sum(axis=0)
        q1 = float(np.average(byd[:2], weights=w[:2])) if w[:2].sum() > 0 else np.nan
        q5 = float(np.average(byd[-2:], weights=w[-2:])) if w[-2:].sum() > 0 else np.nan
        out['tut_participation_gap_q5_q1'][yi] = q5 - q1
        self.tut_panel[int(y)] = dict(part=part.tolist(), prob=prob.tolist(),
                                      spend=spend_tut_d.tolist(),
                                      participation=float(out['tut_participation'][yi]),
                                      own_share=float(out['tut_own_share'][yi]),
                                      other_share=float(out['tut_other_share'][yi]),
                                      commercial_share=float(out['tut_commercial_share'][yi]))


# ----------------------------------------------------------------------------- convenience
def bray_anchor():
    """The standalone demand-mix anchor as a TutoringParams object (documented in the module docstring)."""
    return TutoringParams()
