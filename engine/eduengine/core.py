"""eduengine core: children, ladder, household choice, learning, gates, beliefs, and the module loop.

Units: money in multiples of the informal adult wage (= 1). Learning in grade-equivalents (one year of
full-quality schooling for an average child adds 1). See SPEC.md for the phase order and LITERATURE.md for sources.

Gate-1 repair (see docs/audit/ENGINE_INTERFACE_CONTRACT.md and docs/audit/ENGINE_CORE_AUDIT.md):
* explicit gate kinds ``open | fixed_bar | quota | contest`` (``'bar'`` is a deprecated alias of ``fixed_bar``;
  an unknown/missing kind raises ``ValueError`` at construction and after every calendar gate replacement);
* separate events: credential completion, track placement (persistent ``k['track']``), university admission
  (gate ``admit``), elite status (persistent ``k['elite']``/``k['elite_prize']``);
* expected contest probabilities are the Plackett-Luce top-seat probabilities from
  ``eduengine.contest_math.pl_win_probs`` (the old ``1-exp(-lam x^r)`` path is deleted); the realised gate is
  ``pl_realize`` on event-keyed uniforms;
* persistent per-person preparation stock ``k['prep_stock'][:, m]`` replaces the undepreciated ``k['contest_e']``
  stock (``k['contest_e']`` survives only as the current-year effort flow for reporting);
* exogenous draws are event-keyed by immutable ``k['pid']`` (``eduengine.rng.EventRNG``), so policy arms share
  exogenous draws for every person.
"""
import warnings

import numpy as np
from scipy.special import ndtr

from .contest_math import pl_win_probs, pl_realize
from .rng import EventRNG

CORE_DEFAULTS = dict(
    seed=0, N=1500, T=70, measure_from=35,          # children per cohort; years simulated; cohorts entering >= measure_from are scored
    levels=[('primary', 6), ('lower', 3), ('upper', 3), ('tertiary', 4)],
    gates=[dict(kind='fixed_bar', bar=3.0), dict(kind='fixed_bar', bar=5.5),
           dict(kind='fixed_bar', bar=8.0), dict(kind='fixed_bar', bar=11.5)],
    exam_sd=1.0,                 # noise in gate scores (grade-equivalents)
    entry_age=6, max_entry_age=9,
    # households
    y_median=1.0, y_sigma=0.75, y_growth=0.0, urban_share=0.4, urban_income=1.6,
    subsist=0.55, shock_sigma=0.3, borrow=0.15,
    child_wage=((8, 0.0), (11, 0.10), (14, 0.35), (17, 0.70), (20, 0.95)),
    need_share=0.5,              # need_mode='constant': share of a child's potential earnings the household must replace
    need_mode='luxury',          # 'luxury' (Basu & Van 1998): a household needs a child's earnings only when poor
    need_max=1.0, poverty_line=1.0, need_width=0.35,   # need = need_max x logistic((poverty_line - y) / (need_width x poverty_line))
    # grade repetition and exam retakes (v0.4)
    promote_bar=0.0,             # promoted if learning >= promote_bar x grade (+ noise); 0 = automatic promotion
    gate_retakes=0,              # times a child who fails a gate exam may repeat the final grade and resit
    voc_quality=0.85,            # learning per year on a vocational track (gates with fail='track' send failers there)
    # anchored enrolment (v0.3): HOW MANY continue follows observed completion (UIS), the mechanism decides WHO
    enrol_targets={},            # {level: [(year, completion), ...]}; levels without targets stay fully modelled
    anchor_stop=None,            # year from which anchoring ends: the implied wedge is frozen at its recent mean and the
                                 # mechanism decides (policy experiments; cf. Chari, Kehoe & McGrattan 2007)
    entry_share=0.97,            # share of a cohort that ever enrols (anchor for the first level)
    rural_cost=0.03,             # extra yearly cost of schooling beyond primary for rural children (distance)
    delta=0.93, kappa=12.0,      # discount factor; weight on the child's future log income (altruism x working-life annuity)
    tau=0.25,                    # logit noise in the continue decision (utility units)
    # learning
    q0=1.0, beta_a=0.25, home_effect=0.15, ses_home=0.6,   # base quality; ability; home input per year; corr(income, home capital)
    learn_noise=0.15,
    # beliefs
    prior_logw=[0.0, 0.05, 0.15, 0.35, 0.8], belief_decay=0.85,
    # measurement anchors (assumed scale; see SDG4 module)
    mpl_primary=4.5, mpl_lower=7.0,
    # calendar, paths and interventions (v0.2)
    start_year=0,                # calendar year of t = 0
    paths={},                    # {param: [(year, value), ...]} interpolated every year (e.g. income growth, budgets)
    events=[],                   # [{'year': Y, 'set': {param: value}, 'label': str}] step changes = interventions
    level_open=None,             # per level: [(year, 0/1), ...] or None; a closed level is skipped (e.g. no Senior High before 2016)
    # street state (v0.2): urban children who leave school young and whom no kin network absorbs (Tilly's trust networks)
    kin_support=0.7, street_age=15,
    # struts that can be switched off for strut-removal tests (see struts.py)
    belief_floor=True,
    # Tullock contest gate (vertical-tier positional race): expected and realised probabilities are Plackett-Luce
    elite_logw=0.0,              # log-wage premium for winning a contest gate (gate-level elite_logw overrides)
    contest_r=1.5,               # contest discrimination exponent (Plackett-Luce / Gumbel-max)
    contest_alpha=1.0,           # effectiveness of contest tutoring effort in effective contest input
    contest_price=0.05,          # unit price of contest tutoring effort (wage units, pre-tax resource cost)
    contest_x0=1.0,              # baseline contest input (free schooling / zero-tutoring floor)
    contest_max_e=10.0,          # regulatory cap on annual contest tutoring effort
    # expected-contest-probability module (engine/eduengine/contest_math.py; contract §10)
    contest_prob_method='auto',  # 'auto' (deterministic: exact for small n) | 'exact'
    contest_prob_mc=20000,       # Monte-Carlo draws for the validation-only 'mc' path
    contest_prob_seed_offset=0,  # seed offset for validation-only MC draws
)

# ---------------------------------------------------------------------------------------------- gate schema
GATE_KINDS = ('open', 'fixed_bar', 'quota', 'contest')
_GATE_ALIAS = {'bar': 'fixed_bar'}
_GATE_NUMERIC_FIELDS = ('bar', 'share', 'cut0', 'elite_logw', 'r', 'alpha', 'x0', 'track_bonus', 'lam0')
_TRACK_PRIZE_KEYS = ('quality_mult', 'earnings_logw', 'g12_track_bonus')

#: Canonical Korea Gate-9 specs (contract §3). Data, not fitting: the three track_prize magnitudes are
#: PRE-REGISTERED STRUCTURAL PLACEHOLDERS, not estimates. ``earnings_logw=0.15`` reuses the old phantom G9
#: ``elite_logw`` value so the repair converts an unpriced prize into a delivered one; ``quality_mult`` and
#: ``g12_track_bonus`` are placeholders whose sensitivity is a wave-2 task. Runners deepcopy one entry into
#: ``gates=``; the two specs differ only at level index 1 (Grade 9).
GATE_SPECS = {
    'KR-SINGLE': [
        dict(kind='fixed_bar', bar=2.0, spec=dict(id='KR-G6', label='primary completion')),
        dict(kind='open', spec=dict(id='KR-G9-open', label='regular grade-9 transition')),
        dict(kind='contest', share=0.12, fail='track',
             spec=dict(id='KR-G12', label='CSAT-style university gate')),
        dict(kind='fixed_bar', bar=10.0, spec=dict(id='KR-TER', label='tertiary completion')),
    ],
    'KR-TRACKED': [
        dict(kind='fixed_bar', bar=2.0, spec=dict(id='KR-G6', label='primary completion')),
        dict(kind='contest', share=0.35, fail='track', track_consequence=True,
             track_prize=dict(quality_mult=1.10, earnings_logw=0.15, g12_track_bonus=1.25),
             spec=dict(id='KR-G9-track', label='selective grade-9 placement')),
        dict(kind='contest', share=0.12, fail='track', track_bonus=1.25,
             spec=dict(id='KR-G12', label='CSAT-style gate with track bonus')),
        dict(kind='fixed_bar', bar=10.0, spec=dict(id='KR-TER', label='tertiary completion')),
    ],
}


def _is_num(x):
    return isinstance(x, (int, float, np.integer, np.floating)) and not isinstance(x, bool)


def normalise_gates(gates, nlev):
    """Validate and normalise a gate list (contract §1). Returns ``(gates, used_alias)``.

    ``'bar'`` is rewritten to ``fixed_bar`` and reported through ``used_alias`` so the Engine can emit one
    ``DeprecationWarning``. Unknown/missing kinds and malformed fields raise ``ValueError`` -- a gate list may
    never silently fall through to another kind.
    """
    if not isinstance(gates, (list, tuple)):
        raise ValueError(f'gates must be a list of dicts, got {type(gates).__name__}')
    if len(gates) != nlev:
        raise ValueError(f'gates must have one entry per level: got {len(gates)}, expected {nlev}')
    out = []
    used_alias = False
    track_seen = None
    for m, raw in enumerate(gates):
        if not isinstance(raw, dict):
            raise ValueError(f'gate at level {m} must be a dict, got {type(raw).__name__}')
        g = dict(raw)
        kind = g.get('kind', None)
        if kind in _GATE_ALIAS:
            kind = _GATE_ALIAS[kind]
            g['kind'] = kind
            used_alias = True
        if kind not in GATE_KINDS:
            raise ValueError(
                f"unknown gate kind {raw.get('kind')!r} at level {m}; "
                f"expected one of {GATE_KINDS} ('bar' is accepted as a deprecated alias of 'fixed_bar')")
        spec = g.get('spec', None)
        if spec is not None:
            if not isinstance(spec, dict):
                raise ValueError(f'gate {m}: spec must be a dict or None')
            bad = [k for k in spec if k in _GATE_NUMERIC_FIELDS]
            if bad:
                raise ValueError(f'gate {m}: spec may not carry numeric fields {bad}')
        fail = g.get('fail', 'stop')
        g['fail'] = 'track' if fail == 'track' else 'stop'
        g['academic_only'] = bool(g.get('academic_only', False))
        if kind == 'open':
            for key in ('share', 'bar', 'elite_logw', 'track_prize', 'set_voc'):
                if key in g and g[key] is not None:
                    raise ValueError(f"gate {m}: kind='open' may not carry {key!r}")
            g['track_consequence'] = False
        if kind == 'fixed_bar':
            if not _is_num(g.get('bar')):
                raise ValueError(f"gate {m}: kind='fixed_bar' requires a numeric 'bar'")
        if kind in ('quota', 'contest'):
            if not _is_num(g.get('share')):
                raise ValueError(f"gate {m}: kind={kind!r} requires a numeric 'share'")
            if not (0.0 < float(g['share']) <= 1.0):
                raise ValueError(f"gate {m}: share must be in (0, 1], got {g['share']!r}")
            g['share'] = float(g['share'])
            share_of = g.get('share_of', 'cohort')
            if share_of not in ('cohort', 'applicants'):
                raise ValueError(f"gate {m}: share_of must be 'cohort' or 'applicants', got {share_of!r}")
            g['share_of'] = share_of
        if kind == 'quota':
            if not _is_num(g.get('cut0', 0.0)):
                raise ValueError(f'gate {m}: cut0 must be numeric')
            g['cut0'] = float(g.get('cut0', 0.0))
        if kind == 'contest':
            for key in ('r', 'alpha', 'x0'):
                if g.get(key, None) is not None and not _is_num(g[key]):
                    raise ValueError(f'gate {m}: {key} must be numeric or None')
            if g.get('elite_logw', None) is not None and not _is_num(g['elite_logw']):
                raise ValueError(f'gate {m}: elite_logw must be numeric or None')
            g['set_voc'] = bool(g.get('set_voc', True))
            g['track_bonus'] = float(g.get('track_bonus', 1.0) or 1.0)
        tc = bool(g.get('track_consequence', False))
        if kind != 'contest':
            tc = False
        g['track_consequence'] = tc
        if tc:
            if g['fail'] != 'track':
                raise ValueError(f'gate {m}: a track_consequence gate requires fail=\'track\'')
            if g.get('elite_logw', None) is not None:
                raise ValueError('a tracking gate may not pay a direct elite_logw; use track_prize')
            if 'set_voc' in raw:
                raise ValueError('a tracking gate may not set set_voc (losers are placed on the non-elite track)')
            g.pop('set_voc', None)
            tp = g.get('track_prize', None)
            if not isinstance(tp, dict):
                raise ValueError(f'gate {m}: track_consequence requires a track_prize dict')
            if set(tp.keys()) != set(_TRACK_PRIZE_KEYS):
                raise ValueError(f'gate {m}: track_prize keys must be exactly {_TRACK_PRIZE_KEYS}, got {sorted(tp)}')
            for key in _TRACK_PRIZE_KEYS:
                if not _is_num(tp[key]):
                    raise ValueError(f'gate {m}: track_prize[{key!r}] must be numeric')
            if (float(tp['quality_mult']) == 1.0 and float(tp['earnings_logw']) == 0.0
                    and float(tp['g12_track_bonus']) == 1.0):
                raise ValueError(f'gate {m}: track_prize is neutral; a tracking gate must deliver something')
            g['track_prize'] = {key: float(tp[key]) for key in _TRACK_PRIZE_KEYS}
            if track_seen is not None:
                raise ValueError(f'at most one track_consequence gate is allowed (levels {track_seen} and {m})')
            track_seen = m
        adm = g.get('admit', None)
        if adm is not None:
            if not isinstance(adm, dict):
                raise ValueError(f'gate {m}: admit must be a dict or None')
            adm = dict(adm)
            if not _is_num(adm.get('share')):
                raise ValueError(f'gate {m}: admit requires a numeric share')
            if not (0.0 < float(adm['share']) <= 1.0):
                raise ValueError(f"gate {m}: admit.share must be in (0, 1]")
            adm['share'] = float(adm['share'])
            adm_kind = adm.get('kind', 'quota')
            if adm_kind not in ('quota', 'open'):
                raise ValueError(f"gate {m}: admit.kind must be 'quota' or 'open', got {adm_kind!r}")
            adm['kind'] = adm_kind
            adm['cut0'] = float(adm.get('cut0', 0.0))
            adm['academic_only'] = bool(adm.get('academic_only', False))
            adm['share_of'] = adm.get('share_of', 'cohort')
            if adm['share_of'] not in ('cohort', 'applicants'):
                raise ValueError(f"gate {m}: admit.share_of must be 'cohort' or 'applicants'")
            g['admit'] = adm
        out.append(g)
    return out, used_alias


def interp_path(path, x):
    xs, ys = zip(*path)
    return float(np.interp(x, xs, ys))


class Module:
    """Base class. A module declares defaults and fills in any of the phase hooks."""
    name = 'module'
    defaults = {}

    def setup(self, E): pass
    def supply(self, E, t): pass
    def sector(self, E, t): pass
    def extras(self, E, t): pass
    def labour(self, E, t, ex): return None     # only a labour module returns incomes
    def after(self, E, t): pass
    def measure(self, E, t): pass
    def summary(self, E): return {}


class Engine:
    def __init__(self, modules, **params):
        self.modules = list(modules)
        p = dict(CORE_DEFAULTS)
        for m in self.modules:
            p.update(m.defaults)
        unknown = [k for k in params if k not in p]
        if unknown:
            raise KeyError(f'unknown parameters: {unknown}')
        p.update(params)
        if p['measure_from'] >= p['T'] - 1:              # short runs: score the second half instead of crashing
            p['measure_from'] = p['T'] // 2
        self.p = p
        lv = [n for _, n in p['levels']]
        self.ends = np.cumsum(lv)                     # grade at which each level ends
        self.nlev = len(lv)
        self._alias_warned = False
        self._install_gates(p['gates'], initial=True)
        self.rng = EventRNG(p['seed'], replicate=p['seed'])
        self.t_now = -1
        self._pool_map_cache = {}
        self.B = np.array(p['prior_logw'], float)     # beliefs: expected log income by credential 0..nlev
        self.Bn = np.zeros(self.nlev + 1)
        self.lrate = p['q0']                          # believed mean learning per school year
        self.kids = None
        self.labour_module = [m for m in self.modules if m.labour.__func__ is not Module.labour]
        if len(self.labour_module) > 1:
            raise ValueError('use one labour module')
        self.R = dict(year=[])                        # time series, filled by record()
        self.exits = []                               # exited children (dicts of arrays), for cohort tables
        self.census = {}                              # (cohort, age) -> [enrolled, population]
        self.cw = np.array([interp_path(p['child_wage'], a) for a in range(0, 41)])
        self.modules_by_name = {m.name: m for m in self.modules}
        self.event_log = []
        self.closed = [False] * self.nlev
        self.wedge = np.zeros(self.nlev)              # completion wedges (Anchor module; strut S0)
        self.frozen = None                            # frozen implied wedge after anchor_stop
        self.pass_rate = np.ones(self.nlev)           # recent gate pass rates (used by anchored enrolment)
        self.comp_count = {}                          # cohort -> completions by level (for anchoring)
        for m in self.modules:
            m.setup(self)

    # ------------------------------------------------------------------ gate schema
    def _install_gates(self, gates, initial=False):
        """Normalise a gate list and carry initialised cut/belief state over for unchanged indices (contract §1)."""
        normalised, used_alias = normalise_gates(gates, self.nlev)
        if used_alias and not getattr(self, '_alias_warned', False):
            warnings.warn(
                "gate kind 'bar' is a deprecated alias of 'fixed_bar'; update the config (fixed in a future release)",
                DeprecationWarning, stacklevel=2)
            self._alias_warned = True
        old = getattr(self, 'gates', None)
        old_cut = getattr(self, 'cut', None)
        old_adm = getattr(self, 'cut_adm', None)
        old_lam = getattr(self, 'lam_contest', None)
        self.gates = normalised
        self.p['gates'] = normalised
        self.gate_kinds = [g['kind'] for g in normalised]
        self.contest_indices = [m for m, g in enumerate(normalised) if g['kind'] == 'contest']
        self.track_gate_index = next((m for m, g in enumerate(normalised) if g.get('track_consequence')),
                                     None)
        self.track_effect = (dict(normalised[self.track_gate_index]['track_prize'])
                             if self.track_gate_index is not None else None)
        self.track_earnings_logw = float(self.track_effect['earnings_logw']) if self.track_effect else 0.0
        cut, cut_adm, lam = [], [], []
        for m, g in enumerate(normalised):
            same = old is not None and m < len(old) and old[m]['kind'] == g['kind']
            cut.append((old_cut[m] if same and old_cut is not None else g.get('cut0', 0.0)))
            cut_adm.append((old_adm[m] if same and old_adm is not None
                            else g.get('admit', {}).get('cut0', 0.0) if g.get('admit') else 0.0))
            lam.append((old_lam[m] if same and old_lam is not None else g.get('lam0', 0.5)))
        self.cut = [float(x) for x in cut]
        self.cut_adm = [float(x) for x in cut_adm]
        # kept only for backward import compatibility; it must not feed any probability after the repair
        self.lam_contest = [float(x) for x in lam]

    def set_gates(self, gates):
        """Replace the gate list at runtime (calendar events); re-validates immediately."""
        self._install_gates(gates)
        return self.gates

    def gate_kind(self, m):
        return self.gate_kinds[m]

    @property
    def contest_gates(self):
        return [(m, self.gates[m]) for m in self.contest_indices]

    # ------------------------------------------------------------------ contest API (contract §6)
    def _contest_pool_mask(self, m):
        """The children who will sit gate ``m`` next: the cohort currently in the last grade of level ``m``.

        A gate at the end of level ``m`` is sat by children with ``cred == m`` and ``g == ends[m] - 1`` (they are
        promoted to ``ends[m]`` and sit the gate in the same year).  Using the *sitting cohort* (not every child
        with ``cred <= m`` across several cohorts) is what makes the expected probability of §1.3 the same object
        as the realised draw: both are top-``seats`` Plackett-Luce among ~N same-year applicants.
        """
        k = self.kids
        cand = (k['cred'] == m) & (k['g'] == self.ends[m] - 1)
        if not cand.any():
            cand = k['cred'] == m
        return cand

    def contest_candidates(self, m):
        """Boolean mask of the children who compete for gate ``m`` (contract §6; sitting-cohort definition).

        ``academic_only`` excludes the vocational track; a ``track_consequence`` gate excludes children already
        placed.  (Wording clarification vs contract §1.3: the competing pool is the same-year sitters, which is
        required for the expected and realised probabilities to be the same object; flagged to the Commander.)
        """
        k = self.kids
        g = self.gates[m]
        cand = self._contest_pool_mask(m)
        if g.get('academic_only'):
            cand = cand & ~k['voc']
        if g.get('track_consequence'):
            cand = cand & (k['track'] == -1)
        return cand

    def contest_seats(self, m):
        """Planned seats for gate ``m``: ``max(round(share * denominator), 1)`` with the D3 denominator."""
        g = self.gates[m]
        if g['kind'] != 'contest':
            raise ValueError(f'gate {m} is not a contest gate')
        if g.get('share_of', 'cohort') == 'applicants':
            denom = int(self.contest_candidates(m).sum())
        else:
            denom = int(self.p['N'])
        return max(int(round(float(g['share']) * denom)), 1)

    def _contest_exponents(self, m):
        g = self.gates[m]
        r = g.get('r', None)
        alpha = g.get('alpha', None)
        x0 = g.get('x0', None)
        return (float(self.p['contest_r'] if r is None else r),
                float(self.p['contest_alpha'] if alpha is None else alpha),
                float(self.p['contest_x0'] if x0 is None else x0))

    def _contest_w(self, m, L, stock, track):
        """Contest weights ``w = x_eff**r`` (with the later-gate ``track_bonus`` where applicable)."""
        r, alpha, x0 = self._contest_exponents(m)
        g = self.gates[m]
        ends = max(int(self.ends[m]), 1)
        x = np.maximum(x0 * np.maximum(np.asarray(L, float), 0.1) / ends + alpha * np.asarray(stock, float), 1e-6)
        w = x ** r
        bonus = float(g.get('track_bonus', 1.0) or 1.0)
        if bonus != 1.0 and track is not None:
            w = np.where(np.asarray(track) == 1, w * bonus, w)
        return w

    def _map_positions(self, cand, idx):
        """Positions of global child indices ``idx`` inside the sorted candidate array ``cand``."""
        idx = np.asarray(idx, int)
        if len(cand) == 0 or len(idx) == 0:
            return idx, np.zeros(len(idx), bool)
        pos = np.searchsorted(cand, idx)
        inside = (pos < len(cand)) & (cand[np.clip(pos, 0, len(cand) - 1)] == idx)
        return pos, inside

    def contest_weights(self, m, idx=None, stock_override=None):
        """Return ``(pids, w)`` for the children competing for gate ``m`` (contract §6; weight definition owned here)."""
        k = self.kids
        cand = np.flatnonzero(self.contest_candidates(m))
        L = k['L'][cand]
        stock = k['prep_stock'][cand, m].copy()
        if stock_override is not None:
            if idx is None:
                raise ValueError('stock_override requires idx')
            so = np.asarray(stock_override, float)
            iv = np.asarray(idx, int)
            if so.shape != iv.shape:
                raise ValueError(f'stock_override shape {so.shape} != idx shape {iv.shape}')
            pos, inside = self._map_positions(cand, iv)
            stock[pos[inside]] = so[inside]
        w = self._contest_w(m, L, stock, k['track'][cand])
        if idx is not None:
            iv = np.asarray(idx, int)
            pos, inside = self._map_positions(cand, iv)
            return k['pid'][iv[inside]], w[pos[inside]]
        return k['pid'][cand], w

    def _pl_probs(self, w, seats):
        """Expected top-``seats`` Plackett-Luce win probabilities, with the contract seat-sum invariant."""
        w = np.asarray(w, float)
        n = len(w)
        seats = int(min(max(int(seats), 0), n))
        if n == 0:
            return np.zeros(0)
        method = self.p['contest_prob_method']
        rng = None
        if method == 'mc':                      # validation-only path (never the default decision path)
            rng = self.rng.mc_rng(self.p['contest_prob_seed_offset'])
        P = np.asarray(pl_win_probs(w, seats, method=method, rng=rng,
                                    n_mc=int(self.p['contest_prob_mc'])), float)
        if P.shape != (n,):
            raise ValueError(f'contest probability module returned shape {P.shape}, expected ({n},)')
        if seats > 0:
            total = float(P.sum())
            dev = abs(total - seats)
            if dev > 1e-3 and method != 'mc':
                raise ValueError(
                    'contest probability module violates the seat-sum invariant: '
                    f'sum(P)={total:.6g}, seats={seats} (deviation {dev:.3g} > 1e-3); '
                    "it must implement the deterministic method='auto' path of contract amendment A5")
            if total > 0:
                P = P * (seats / total)
        return P

    def contest_expected_probs(self, m, idx=None):
        """``(idx_or_pids, P)``: expected top-seat win probabilities of the gate-``m`` candidates (contract §6)."""
        pid, w = self.contest_weights(m, idx=None)
        seats = min(self.contest_seats(m), len(w))
        P = self._pl_probs(w, seats)
        if idx is None:
            return np.arange(len(w)), P
        iv = np.asarray(idx, int)
        cand = np.flatnonzero(self.contest_candidates(m))
        pos, inside = self._map_positions(cand, iv)
        out = np.zeros(len(iv))
        out[inside] = P[pos[inside]]
        return iv, out

    def _effective_elite_logw(self, m):
        """Effective log-wage prize of a non-tracking contest gate (``None`` inherits ``p['elite_logw']``)."""
        g = self.gates[m]
        if g.get('track_consequence'):
            return 0.0
        elw = g.get('elite_logw', None)
        return float(self.p['elite_logw'] if elw is None else elw)

    def _gate_expected_P(self, m, gidx, Lend, track_state):
        """Expected win probability for the children ``gidx`` at gate ``m`` (contract §1.3).

        The competitor pool is the *sitting cohort* of gate ``m`` (one year group, ``cred==m`` and
        ``g==ends[m]-1``).  ``pl_win_probs`` is evaluated once on that pool; the resulting probability curve
        as a function of own contest weight is then used for every valued child (exactly for pool members,
        by monotone interpolation of the official probabilities for children valued at a future gate -- a
        documented approximation, since the future cohort's weight distribution is approximated by the current
        sitting cohort's).  The pool probability map is cached per (year, gate, pool weights), so repeated
        household-problem evaluations in one year do not repeat the PL computation.

        ``track_state`` overrides the children's own track state (used for the counterfactual in
        :meth:`gate_prize_dv` and by the value recursion); it never changes the competitor pool.
        """
        k = self.kids
        gate = self.gates[m]
        if gate['kind'] != 'contest':
            raise ValueError(f'gate {m} is not a contest gate')
        gidx = np.atleast_1d(np.asarray(gidx, int))
        pool = np.flatnonzero(self.contest_candidates(m))
        w_pool = self._contest_w(m, k['L'][pool], k['prep_stock'][pool, m], k['track'][pool])
        if gate.get('share_of', 'cohort') == 'applicants':
            denom = len(pool)
        else:
            denom = int(self.p['N'])
        seats = max(int(round(float(gate['share']) * denom)), 1)
        seats = min(seats, len(pool)) if len(pool) else 0
        cache = self._pool_map_cache
        key = (m, w_pool.tobytes())
        if key not in cache:
            if len(w_pool) == 0:
                cache[key] = (np.zeros(0), np.zeros(0), np.zeros(0), np.zeros(0), np.zeros(0))
            else:
                P_pool = self._pl_probs(w_pool, seats)
                lw = np.log(w_pool)
                order = np.argsort(lw)
                cache[key] = (order, lw[order], P_pool[order], pool, P_pool)
        order, lw_sorted, P_sorted, pool_cand, P_pool = cache[key]
        if len(gidx) == 0:
            return np.zeros(0)
        stock = k['prep_stock'][gidx, m]
        state = track_state if track_state is not None else k['track'][gidx]
        w_own = self._contest_w(m, Lend, stock, state)
        if len(w_pool) == 0:
            return np.zeros(len(gidx))
        Pown = np.interp(np.log(w_own), lw_sorted, P_sorted,
                         left=float(P_sorted[0]), right=float(P_sorted[-1]))
        pos, inside = self._map_positions(pool_cand, gidx)
        Pown[inside] = P_pool[pos[inside]]                 # exact for the sitting cohort
        return Pown

    # ------------------------------------------------------------------ population
    def add_cohort(self, t):
        p, r, N = self.p, self.rng, self.p['N']
        pid = t * N + np.arange(N, dtype=np.int64)        # immutable person ids (contract §2)
        z = r.normal(t, 'cohort_z', pid)
        urban = r.uniform(t, 'cohort_urban', pid) < p['urban_share']
        y = p['y_median'] * np.exp(p['y_sigma'] * z) * (1 + p['y_growth']) ** t * np.where(urban, p['urban_income'], 1.0)
        home = ndtr(p['ses_home'] * z + np.sqrt(1 - p['ses_home'] ** 2) * r.normal(t, 'cohort_home', pid))
        new = dict(cohort=np.full(N, t), y=y, z=z, a=r.normal(t, 'cohort_ability', pid), home=home, urban=urban,
                   L=np.zeros(N), g=np.zeros(N, int), cred=np.zeros(N, int), started=np.zeros(N, bool),
                   sector=np.zeros(N, int), att=np.zeros(N, bool), reason=np.full(N, -1),
                   L6=np.full(N, np.nan), L9=np.full(N, np.nan), spend=np.zeros(N), pub_years=np.zeros(N),
                   comp_age=np.full((N, self.nlev), np.nan),
                   q=np.searchsorted(np.quantile(z, [0.2, 0.4, 0.6, 0.8]), z), street=np.zeros(N, bool),
                   gtimes=np.zeros(N, int), repeats=np.zeros(N, int), retakes=np.zeros(N, int), voc=np.zeros(N, bool),
                   contest_e=np.zeros(N), tut_k12=np.zeros(N),
                   pid=pid, track=np.full(N, -1, np.int8), elite=np.zeros(N, bool), elite_prize=np.zeros(N),
                   prep_stock=np.zeros((N, self.nlev)))
        if self.kids is None:
            self.kids = new
        else:
            self.kids = {k: np.concatenate([self.kids[k], v]) for k, v in new.items()}

    def age(self, t):
        return t - self.kids['cohort'] + self.p['entry_age']

    def level_of(self, g):
        """Index of the level a child with g completed grades is in (nlev if finished)."""
        return np.searchsorted(self.ends, g, side='right')

    # ------------------------------------------------------------------ household valuation
    def values(self, t, L=None, idx=None, track_state=None):
        """Backward induction over remaining levels. Returns (V_stop, V_continue) per child.

        ``track_state`` (contract amendment A4) overrides ``k['track']`` for a counterfactual evaluation: it is
        used by :meth:`gate_prize_dv` to price the actual track continuation value.
        """
        out = self._value_recursion(t, L=L, idx=idx, track_state=track_state, want_aux=False)
        return out['V_stop'], out['V_cont']

    def _value_recursion(self, t, L=None, idx=None, track_state=None, want_aux=False):
        p, k = self.p, self.kids
        if idx is None:
            gi = np.arange(len(k['y']))
        else:
            gi = np.atleast_1d(np.asarray(idx, int))
        n = len(gi)
        if n == 0:
            return dict(V_stop=np.zeros(0), V_cont=np.zeros(0), aux={})
        L = k['L'][gi] if L is None else np.asarray(L, float)
        g, cred, y = k['g'][gi], k['cred'][gi], k['y'][gi]
        age_now = self.age(t)[gi]
        ycost = self.yr['cost'][gi] if hasattr(self, 'yr') else np.zeros(n)
        d = p['delta']
        need_frac = self.need_frac(y)
        voc = k['voc'][gi]
        lam = self.lrate * np.exp(p['beta_a'] * k['a'][gi])
        te = self.track_effect
        earn = float(te['earnings_logw']) if te else 0.0
        qmult = float(te['quality_mult']) if te else 1.0
        lam1 = lam * qmult
        if track_state is None:
            tr = np.asarray(k['track'][gi], int)
        else:
            tr = np.broadcast_to(np.asarray(track_state, int), (n,)).copy()
        Vc0 = p['kappa'] * self.B
        Vc1 = p['kappa'] * (self.B + earn) if te else Vc0
        mt = self.track_gate_index
        U1 = np.full(n, Vc1[self.nlev])
        U0 = np.full(n, Vc0[self.nlev])
        Us = np.full(n, Vc0[self.nlev])
        Vcont = np.full(n, -np.inf)
        cont0_by_cred = np.full(n, -np.inf)
        cont1_by_cred = np.full(n, -np.inf)
        aux = {}
        for m in range(self.nlev - 1, -1, -1):
            closed = self.closed[m]
            above = (mt is not None) and (m > mt)
            tracking = (mt is not None) and (m == mt)
            if closed:                                  # a level that does not exist: entering m = entering m+1
                if above:
                    c0, c1 = U0 - Vc0[m], U1 - Vc1[m]
                    cont0_by_cred = np.where(cred == m, c0, cont0_by_cred)
                    cont1_by_cred = np.where(cred == m, c1, cont1_by_cred)
                else:
                    c0 = Us - Vc0[m]
                    Vcont = np.where(cred == m, c0, Vcont)
                continue
            gate = self.gates[m]
            kind = gate['kind']
            start_g = 0 if m == 0 else self.ends[m - 1]
            yrs_left = np.where(cred == m, self.ends[m] - g, self.ends[m] - start_g)
            yrs_left = np.maximum(yrs_left, 0)
            pv = np.zeros(n)
            for j in range(int(yrs_left.max()) + 1 if n else 0):
                a_ = np.clip(age_now + np.maximum(start_g - g, 0) + j, 0, 40)
                c = ycost + need_frac * self.cw[a_.astype(int)]
                pv += np.where(j < yrs_left, d ** j * c / np.maximum(y, 0.05), 0.0)
            elw = self._effective_elite_logw(m) if kind == 'contest' else 0.0
            adm = gate.get('admit')

            def _gate_branch(Lend, P, s):
                if above:
                    Uc = U1 if s == 1 else U0
                    Vc_ = Vc1 if s == 1 else Vc0
                else:
                    Uc = Us
                    Vc_ = Vc0
                Upass = Uc + p['kappa'] * elw
                Vfail = Uc if gate['fail'] == 'track' else Vc_[m]
                if adm is not None and m + 1 < self.nlev:
                    if adm['kind'] == 'open':
                        Pa = np.ones(n)
                    else:
                        Pa = ndtr((Lend - self.cut_adm[m]) / p['exam_sd'])
                        if adm.get('academic_only'):
                            Pa = np.where(voc, 0.0, Pa)
                    Upass = Pa * Uc + (1 - Pa) * Vc_[m + 1]
                return d ** yrs_left * (P * Upass + (1 - P) * Vfail) - pv + self.wedge[m]

            def _expected(kind_, Lend, s):
                if kind_ == 'contest':
                    return self._gate_expected_P(m, gi, Lend, np.full(n, s) if above else None)
                if kind_ == 'open':
                    return np.ones(n)
                ref = gate['bar'] if kind_ == 'fixed_bar' else self.cut[m]
                P = ndtr((Lend - ref) / p['exam_sd'])
                if gate.get('academic_only'):
                    P = np.where(voc, 0.0, P)
                return P

            if tracking:
                # the gate that places the child on a persistent track: passing -> state 1, failing -> state 0
                P = _expected('contest', L + lam * np.maximum(self.ends[m] - g, 0), 0)
                cont = d ** yrs_left * (P * U1 + (1 - P) * U0) - pv + self.wedge[m]
                Um = np.maximum(Vc0[m], cont)
                Vcont = np.where(cred == m, cont, Vcont)
                Us = np.where(cred <= m, Um, Us)
            elif above:
                for s in (0, 1):
                    Lend = L + (lam1 if s == 1 else lam) * np.maximum(self.ends[m] - g, 0)
                    P = _expected(kind, Lend, s)
                    cont = _gate_branch(Lend, P, s)
                    Um = np.maximum(Vc1[m] if s == 1 else Vc0[m], cont)
                    if s == 1:
                        cont1_by_cred = np.where(cred == m, cont, cont1_by_cred)
                        U1 = np.where(cred <= m, Um, U1)
                    else:
                        cont0_by_cred = np.where(cred == m, cont, cont0_by_cred)
                        U0 = np.where(cred <= m, Um, U0)
                aux[(0, m)] = U0.copy()
                aux[(1, m)] = U1.copy()
            else:
                Lend = L + lam * np.maximum(self.ends[m] - g, 0)
                P = _expected(kind, Lend, 0)
                cont = _gate_branch(Lend, P, 0)
                Um = np.maximum(Vc0[m], cont)
                Vcont = np.where(cred == m, cont, Vcont)
                Us = np.where(cred <= m, Um, Us)
                aux[(0, m)] = Us.copy()
        V_stop = np.where(tr == 1, Vc1[np.minimum(cred, self.nlev)], Vc0[np.minimum(cred, self.nlev)])
        if mt is not None:
            placed = cred > mt
            V = Vcont.copy()
            V = np.where(placed & (tr == 1), cont1_by_cred, V)
            V = np.where(placed & (tr != 1), cont0_by_cred, V)
        else:
            V = Vcont
        V = np.where(cred >= self.nlev, -np.inf, V)
        return dict(V_stop=V_stop, V_cont=V, aux=aux)

    def gate_prize_dv(self, m, idx=None):
        """Utility value of passing gate ``m`` (contract §6): the only prize tutoring may price.

        Tracking gate: ``d**yrs_left * (V(track=1 continuation) - V(track=0 continuation))`` from the same
        :meth:`_value_recursion` as the household problem. Non-tracking elite gate: ``kappa * effective_elite_logw``.
        """
        k = self.kids
        iv = np.arange(len(k['y'])) if idx is None else np.atleast_1d(np.asarray(idx, int))
        g = self.gates[m]
        if not g.get('track_consequence'):
            dv = np.full(len(iv), float(self.p['kappa']) * self._effective_elite_logw(m))
            return iv, dv
        t = self.t_now if self.t_now >= 0 else 0
        res = self._value_recursion(t, idx=iv, track_state=1, want_aux=True)
        U1 = res['aux'].get((1, m + 1))
        U0 = res['aux'].get((0, m + 1))
        if U1 is None or U0 is None:                    # tracking gate at the top level
            U1 = np.full(len(iv), self.p['kappa'] * (self.B[self.nlev] + self.track_effect['earnings_logw']))
            U0 = np.full(len(iv), self.p['kappa'] * self.B[self.nlev])
        yrs = np.maximum(self.ends[m] - k['g'][iv], 0)
        return iv, (self.p['delta'] ** yrs) * (U1 - U0)

    def _target(self, m, Y):
        T = self.p['enrol_targets']
        if m not in T and str(m) not in T:
            return None
        return interp_path(T.get(m, T.get(str(m))), Y)

    def anchored_choice(self, t, idx, net, go):
        """Quantity from data, selection from the mechanism. For each targeted level, the share of started pupils who
        continue this year is the per-year survival implied by the observed completion series (adjusted for gate pass
        rates); the pupils who continue are those with the highest net value among those who can pay this year."""
        p, k = self.p, self.kids
        Y = self.year(t)
        lev = k['cred'][idx]; g = k['g'][idx]
        started = k['started'][idx]
        age = self.age(t)[idx]
        cash = np.maximum(k['y'][idx] * np.exp(p['shock_sigma'] * self._shock_now[idx]) - p['subsist'], 0) + p['borrow'] * k['y'][idx] + self.yr['cct'][idx]
        need = self.yr['cost'][idx] + self.need_frac(k['y'][idx]) * self.cw[np.clip(age, 0, 40)]
        afford = need <= cash
        wedges = np.full(self.nlev, np.nan)
        for m in range(self.nlev):
            if self.closed[m]:
                continue
            grp = np.flatnonzero(started & (lev == m))
            if len(grp) == 0:
                continue
            Ym = Y + int(np.median(self.ends[m] - g[grp])) + 4          # when this group's completion will be measured
            Cm = self._target(m, Ym)
            if Cm is None:
                continue
            Cprev = p['entry_share'] if m == 0 else self._target(m - 1, Ym - self.p['levels'][m][1])
            if Cprev is None:
                Cprev = p['entry_share']
            n_m = self.p['levels'][m][1]
            q = min(1.0, (max(Cm, 1e-4) / max(Cprev, 1e-4)) ** (1 / n_m) / max(self.pass_rate[m], 0.05) ** (1 / n_m))
            n_go = int(round(q * len(grp)))
            score = net[grp] + p['tau'] * self.rng.logistic(Y, 'anchor', k['pid'][idx[grp]])
            score = np.where(afford[grp], score, -np.inf)               # cash first: who cannot pay cannot stay
            order = np.argsort(score)[::-1]
            chosen = order[:n_go]
            chosen = chosen[np.isfinite(score[chosen])]
            go[grp] = False
            go[grp[chosen]] = True
            if 0 < len(chosen) < len(grp):
                wedges[m] = -float(score[order[len(chosen) - 1]])          # implied wedge: value the marginal stayer needed
        self.note(implied_wedge=wedges)
        return go

    def need_frac(self, y):
        """Share of a child's potential earnings the household must replace if the child stays in school."""
        p = self.p
        if p['need_mode'] == 'constant':
            return np.full(np.shape(y), p['need_share'])
        z = (p['poverty_line'] - y) / (p['need_width'] * p['poverty_line'])
        return p['need_max'] / (1 + np.exp(-np.clip(z, -30, 30)))

    def mvl_all(self, t):
        """Marginal value of learning for every child attending this year (cached per year)."""
        if 'mvl' not in self.yr:
            k = self.kids
            m = np.zeros(len(k['y']))
            idx = np.flatnonzero(k['att'])
            if len(idx):
                m[idx] = self.mvl(t, idx)
            self.yr['mvl'] = m
        return self.yr['mvl']

    def mvl(self, t, idx):
        """Marginal value of one grade-equivalent of learning (finite difference through the gates)."""
        k = self.kids
        _, c0 = self.values(t, idx=idx)
        _, c1 = self.values(t, L=k['L'][idx] + 0.5, idx=idx)
        return np.maximum((c1 - c0) / 0.5, 0.0)

    # ------------------------------------------------------------------ one year
    def year(self, t):
        return self.p['start_year'] + t

    def apply_calendar(self, t):
        p, Y = self.p, self.year(t)
        for name, path in p['paths'].items():
            p[name] = interp_path(path, Y)
        for ev in p['events']:
            if ev['year'] == Y:
                p.update(ev['set'])
                if 'gates' in ev['set']:
                    self.set_gates(p['gates'])
                self.event_log.append((Y, ev.get('label', ''), dict(ev['set'])))
        if p['level_open']:
            self.closed = [bool(lo is not None and interp_path(lo, Y) < 0.5) for lo in p['level_open']]

    # ------------------------------------------------------------------ gates
    def _seats_for(self, gate, n_cand):
        denom = n_cand if gate.get('share_of', 'cohort') == 'applicants' else int(self.p['N'])
        return max(int(round(float(gate['share']) * denom)), 1)

    def _q_means(self, values, q):
        values = np.asarray(values, float)
        out = []
        for j in range(5):
            msk = q == j
            out.append(float(values[msk].mean()) if msk.any() else np.nan)
        return out

    def step(self, t):
        p = self.p
        self.t_now = t
        self._pool_map_cache = {}
        self.apply_calendar(t)
        self.add_cohort(t)
        k = self.kids
        n = len(k['y'])
        self.yr = dict(cost=np.zeros(n), quality=np.full(n, p['q0']), withheld=np.zeros(n), tut_gain=np.zeros(n),
                       buyback=np.zeros(n, bool), extra_spend=np.zeros(n), cct=np.zeros(n), tut_kind=np.zeros(n, int),
                       res_cost=np.zeros(n), tut_tax=np.zeros(n), tut_outlay=np.zeros(n), gov_tut_tax=np.zeros(n))
        for m in self.modules:
            m.supply(self, t)
        age = self.age(t)
        # rural distance cost beyond primary
        self.yr['cost'] += np.where(~k['urban'] & (k['g'] >= 6), p['rural_cost'], 0.0)
        # ---- continue / enter
        alive = k['reason'] < 0
        eligible = alive & (k['started'] | (age >= p['entry_age']))
        idx = np.flatnonzero(eligible)
        V_stop, V_cont = self.values(t, idx=idx)
        net = V_cont - V_stop
        anchoring = bool(p['enrol_targets']) and (p['anchor_stop'] is None or self.year(t) < p['anchor_stop'])
        if p['enrol_targets'] and not anchoring:
            if self.frozen is None:                   # the wedge the data needed in the last 5 anchored years, held fixed
                W = np.array(self.R.get('implied_wedge', [])[-5:], float)
                self.frozen = np.nan_to_num(np.nanmean(W, 0)) if len(W) else np.zeros(self.nlev)
            net = net + self.frozen[np.minimum(k['cred'][idx], self.nlev - 1)]
            self.note(implied_wedge=self.frozen.copy())
        pr = 1 / (1 + np.exp(-np.clip(net / p['tau'], -30, 30)))
        go = self.rng.uniform(Y_ := self.year(t), 'continuation', k['pid'][idx]) < pr
        self._shock_now = np.zeros(n)
        self._shock_now[idx] = self.rng.normal(Y_, 'income_shock', k['pid'][idx])
        if anchoring:
            go = self.anchored_choice(t, idx, net, go)
        # liquidity: this year's cost must be payable from this year's cash
        cash = np.maximum(k['y'][idx] * np.exp(p['shock_sigma'] * self._shock_now[idx]) - p['subsist'], 0) \
            + p['borrow'] * k['y'][idx] + self.yr['cct'][idx]
        need = self.yr['cost'][idx] + self.need_frac(k['y'][idx]) * self.cw[np.clip(age[idx], 0, 40)]
        broke = go & (need > cash)
        att = np.zeros(n, bool)
        att[idx[go & ~broke]] = True
        # exits: started children who stop; never-starters past max entry age
        started = k['started']
        stop = np.zeros(n, bool)
        stop[idx[~go & started[idx]]] = True
        stop[idx[broke & started[idx]]] = True
        k['reason'][idx[broke & started[idx]]] = 1          # liquidity
        k['reason'][idx[~go & started[idx]]] = 0            # choice
        never = alive & ~k['started'] & ~att & (age >= p['max_entry_age'])
        k['reason'][never] = 4
        k['reason'][stop & (k['reason'] < 0)] = 0
        k['started'] |= att
        k['att'] = att
        self._cash = np.zeros(n)
        self._cash[idx] = cash - np.where(go, need, 0)
        # ---- sector choice and rationing, extras (tutoring)
        for m in self.modules:
            m.sector(self, t)
        att = k['att']
        k['contest_e'] = np.zeros(n)                        # current-year effort flow only (contract §5)
        for m in self.modules:
            m.extras(self, t)
        # ---- learning (track=1 children learn at quality * quality_mult once placed)
        y = self.yr
        qmult_arr = np.where(k['track'] == 1, self.track_effect['quality_mult'], 1.0) if self.track_effect else 1.0
        eff = y['quality'] * qmult_arr * (1 - np.where(y['buyback'], 0.0, y['withheld'])) \
            * np.where(k['voc'], p['voc_quality'], 1.0)
        dL = eff * np.exp(p['beta_a'] * k['a']) + y['tut_gain'] + p['home_effect'] * (k['home'] - 0.5) \
            + p['learn_noise'] * self.rng.normal(t, 'learning', k['pid'])
        dL = np.where(att, np.maximum(dL, 0.0), 0.0)
        k['L'] += dL
        if att.any():
            self.lrate = 0.8 * self.lrate + 0.2 * float(np.mean((dL[att]) / np.exp(p['beta_a'] * k['a'][att])))
        k['spend'] += np.where(att, y['cost'] + y['extra_spend'], 0.0)
        # ---- progression: promotion (repetition if learning lags the grade), then gates
        new_in_grade = att & (k['gtimes'] == 0)        # first year in this grade (for gross intake ratios)
        self.R.setdefault('new_by_grade', []).append(np.bincount(k['g'][new_in_grade], minlength=self.ends[-1] + 2)[:self.ends[-1] + 1])
        # attendance by grade, indexed like tutoring and private counts: index j = pupils studying grade j+1 this year
        self.R.setdefault('att_by_grade', []).append(np.bincount(k['g'][att], minlength=self.ends[-1] + 2)[:self.ends[-1] + 1])
        if p['promote_bar'] > 0:
            promote = att & ((k['L'] + 0.5 * self.rng.normal(t, 'promote', k['pid'])) >= p['promote_bar'] * (k['g'] + 1))
        else:
            promote = att.copy()
        k['repeats'][att & ~promote] += 1
        k['gtimes'][att & ~promote] += 1
        k['gtimes'][promote] = 0
        k['g'][promote] += 1
        gate_diag = self._empty_gate_diag()
        gated = np.zeros(n, bool)                        # each child meets at most one gate per year
        for m_ in range(self.nlev):
            at_gate = promote & ~gated & (k['g'] == self.ends[m_])
            gated |= at_gate
            if not at_gate.any():
                continue
            if self.ends[m_] == 6: k['L6'][at_gate] = k['L'][at_gate]
            if self.ends[m_] == 9: k['L9'][at_gate] = k['L'][at_gate]
            gate = self.gates[m_]
            kind = gate['kind']
            score = k['L'] + p['exam_sd'] * self.rng.normal(t, f'gate_exam_{m_}', k['pid'])
            ok = np.zeros(n, bool)
            if kind == 'open':                           # non-selective transition: nobody is refused
                ok = at_gate.copy()
            elif kind == 'fixed_bar':
                ok = at_gate & (score >= gate['bar'])
            elif kind == 'quota':
                want = at_gate & (~k['voc'] if gate.get('academic_only') else True)
                wi = np.flatnonzero(want)
                seats = self._seats_for(gate, len(wi))
                if len(wi):
                    order = wi[np.argsort(score[wi], kind='stable')][::-1]
                    n_adm = min(seats, len(order))
                    ok[order[:n_adm]] = True
                    cutv = float(score[order[n_adm - 1]])
                    self.cut[m_] = 0.7 * self.cut[m_] + 0.3 * cutv
            elif kind == 'contest':
                cand = at_gate.copy()
                if gate.get('academic_only'):
                    cand = cand & ~k['voc']
                if gate.get('track_consequence'):
                    cand = cand & (k['track'] == -1)
                ci = np.flatnonzero(cand)
                seats = self._seats_for(gate, len(ci))
                seats_eff = min(seats, len(ci))
                if len(ci):
                    w = self._contest_w(m_, k['L'][ci], k['prep_stock'][ci, m_], k['track'][ci])
                    P = self._pl_probs(w, seats_eff)
                    Y = self.year(t)
                    u = self.rng.uniform(Y, f'contest_pl_{m_}', k['pid'][ci])
                    won = pl_realize(w, seats_eff, u)
                    ok[ci[won]] = True
                    elw = self._effective_elite_logw(m_)
                    if elw > 0.0 and not gate.get('track_consequence'):
                        win = ci[won]
                        k['elite'][win] = True
                        k['elite_prize'][win] = np.maximum(k['elite_prize'][win], elw)
                    if gate.get('track_consequence'):
                        k['track'][at_gate] = 0
                        k['track'][ci[won]] = 1
                    self._record_contest(m_, ci, seats, seats_eff, w, P, won, gate_diag)
                else:
                    if gate.get('track_consequence'):
                        k['track'][at_gate] = 0
                    self._record_contest_empty(m_, seats, gate_diag)
                # the preparation stock is consumed by sitting this gate
                k['prep_stock'][at_gate, m_] = 0.0
            else:                                        # unreachable: normalisation guarantees a kind
                raise ValueError(f'unknown gate kind {kind!r} at level {m_}')
            if gate.get('academic_only') and kind != 'contest':
                ok = ok & ~k['voc']
            if gate.get('fail') == 'track':              # failers continue on a vocational / non-elite track
                tracked = at_gate & ~ok
                if kind == 'contest':
                    if gate.get('set_voc', True) and not gate.get('track_consequence'):
                        k['voc'][tracked] = True
                else:
                    k['voc'][tracked] = True
                ok = ok | tracked
            passed = at_gate & ok
            self.pass_rate[m_] = 0.8 * self.pass_rate[m_] + 0.2 * passed.sum() / max(at_gate.sum(), 1)
            k['cred'][passed] = m_ + 1
            k['comp_age'][passed, m_] = age[passed]
            for c_, nn in zip(*np.unique(k['cohort'][passed], return_counts=True)):
                self.comp_count.setdefault(int(c_), np.zeros(self.nlev))[m_] += nn
            nxt = m_ + 1
            while nxt < self.nlev and self.closed[nxt] and passed.any():   # skipped stage: awarded on passing the one below
                k['cred'][passed] = nxt + 1
                k['comp_age'][passed, nxt] = age[passed]
                k['g'][passed] = self.ends[nxt]
                for c_, nn in zip(*np.unique(k['cohort'][passed], return_counts=True)):
                    self.comp_count.setdefault(int(c_), np.zeros(self.nlev))[nxt] += nn
                nxt += 1
            adm = gate.get('admit')
            if adm is not None and passed.any() and m_ + 1 < self.nlev:   # admission quota to the next level
                if adm['kind'] == 'open':
                    admitted = passed
                else:
                    cand_adm = passed & (~k['voc'] if adm.get('academic_only') else True)
                    ai = np.flatnonzero(cand_adm)
                    if adm.get('share_of', 'cohort') == 'applicants':
                        denom = len(ai)
                    else:
                        denom = int(p['N'])
                    seats_adm = max(int(round(float(adm['share']) * denom)), 1)
                    admitted = np.zeros(n, bool)
                    if len(ai):
                        order = ai[np.argsort(score[ai], kind='stable')][::-1]
                        n_adm = min(seats_adm, len(order))
                        admitted[order[:n_adm]] = True
                        self.cut_adm[m_] = 0.7 * self.cut_adm[m_] + 0.3 * float(score[order[n_adm - 1]])
                refused = passed & ~admitted
                k['reason'][refused & (k['reason'] < 0)] = 6  # leave with the credential just earned
            failed = at_gate & ~ok
            retake = failed & (k['retakes'] < p['gate_retakes'])
            k['retakes'][retake] += 1
            k['repeats'][retake] += 1
            k['g'][retake] -= 1                          # repeat the final grade and sit the exam again next year
            k['gtimes'][retake] = 1
            k['reason'][failed & ~retake] = 2
        finished = att & (k['cred'] >= self.nlev)
        k['reason'][finished & (k['reason'] < 0)] = 3
        # ---- census for out-of-school rates (all children of a cohort, enrolled or not)
        for c_ in np.unique(k['cohort']):
            sel = k['cohort'] == c_
            a_ = t - c_ + p['entry_age']
            self.census[(c_, a_)] = int(att[sel].sum())
        # ---- labour market for leavers
        ex = np.flatnonzero(k['reason'] >= 0)
        if len(ex):   # street state: urban, young, poor leavers without a kin network to absorb them
            young = (age[ex] < p['street_age']) & k['urban'][ex] & (k['y'][ex] < p['y_median'] * p['urban_income'])
            k['street'][ex] = young & (self.rng.uniform(t, 'street', k['pid'][ex]) >= p['kin_support'])
        inc = None
        if self.labour_module:
            inc = self.labour_module[0].labour(self, t, ex)
        if inc is None:          # no labour module: Mincer-style fixed returns, prizes applied multiplicatively last
            inc = np.exp(0.08 * k['g'][ex] + 0.05 * (k['L'][ex] - k['g'][ex]))
            mult = np.exp(k['elite_prize'][ex])
            if self.track_effect:
                mult = mult * np.where(k['track'][ex] == 1, np.exp(self.track_earnings_logw), 1.0)
            inc = inc * mult
        self.update_beliefs(ex, inc)
        self.leaver_income = inc
        self.note(**gate_diag)
        for m in self.modules:
            m.after(self, t)
        for m in self.modules:
            m.measure(self, t)
        self.record(t, ex, inc)
        if len(ex):
            self.exits.append({kk: (v[ex] if v.ndim == 1 else v[ex]) for kk, v in k.items()})
            self.exits[-1]['inc'] = inc
            self.exits[-1]['exit_year'] = np.full(len(ex), t)
            keep = k['reason'] < 0
            self.kids = {kk: v[keep] for kk, v in k.items()}

    # ------------------------------------------------------------------ contest diagnostics (contract §1.4)
    def _empty_gate_diag(self):
        nan5 = lambda: [np.nan] * 5
        nll = lambda: [np.nan] * self.nlev
        return dict(contest_candidates=nll(), contest_seats=nll(), contest_expected_seats=nll(),
                    contest_admitted=nll(), contest_applicant_seat_ratio=nll(), contest_admit_rate=nll(),
                    contest_expected_p_mean=nll(), contest_expected_p_by_q=[nan5() for _ in range(self.nlev)],
                    contest_realized_by_q=[nan5() for _ in range(self.nlev)],
                    contest_prep_stock_mean_by_q=[nan5() for _ in range(self.nlev)])

    def _record_contest(self, m, ci, seats, seats_eff, w, P, won, diag):
        k = self.kids
        q = k['q'][ci]
        admitted = float(won.sum())
        diag['contest_candidates'][m] = int(len(ci))
        diag['contest_seats'][m] = int(seats)
        diag['contest_expected_seats'][m] = float(P.sum())
        diag['contest_admitted'][m] = admitted
        diag['contest_applicant_seat_ratio'][m] = len(ci) / max(seats, 1)
        diag['contest_admit_rate'][m] = admitted / max(len(ci), 1)
        diag['contest_expected_p_mean'][m] = float(P.mean())
        diag['contest_expected_p_by_q'][m] = self._q_means(P, q)
        diag['contest_realized_by_q'][m] = self._q_means(won.astype(float), q)
        diag['contest_prep_stock_mean_by_q'][m] = self._q_means(k['prep_stock'][ci, m], q)

    def _record_contest_empty(self, m, seats, diag):
        diag['contest_candidates'][m] = 0
        diag['contest_seats'][m] = int(seats)
        diag['contest_expected_seats'][m] = 0.0
        diag['contest_admitted'][m] = 0.0
        diag['contest_applicant_seat_ratio'][m] = 0.0
        diag['contest_admit_rate'][m] = 0.0
        diag['contest_expected_p_mean'][m] = 0.0
        diag['contest_expected_p_by_q'][m] = [0.0] * 5
        diag['contest_realized_by_q'][m] = [0.0] * 5
        diag['contest_prep_stock_mean_by_q'][m] = [0.0] * 5

    def contest_summary(self):
        """Additive Gate-1 contest diagnostics summary (contract §1.4); merged by :meth:`run`."""
        R = self.R
        if not self.contest_indices:
            return {}
        m0 = int(self.p['measure_from'])

        def series(key, m):
            if key not in R:
                return np.nan
            arr = np.array(R[key][m0:], float)
            col = arr[:, m] if arr.ndim == 2 else arr
            with np.errstate(invalid='ignore'):
                return float(np.nanmean(col)) if np.isfinite(col).any() else np.nan

        out = dict(
            contest_seats_by_gate=[series('contest_seats', m) for m in self.contest_indices],
            contest_candidates_by_gate=[series('contest_candidates', m) for m in self.contest_indices],
            contest_applicant_seat_ratio_by_gate=[series('contest_applicant_seat_ratio', m) for m in self.contest_indices],
            contest_admit_rate_by_gate=[series('contest_admit_rate', m) for m in self.contest_indices],
            contest_expected_seats_by_gate=[series('contest_expected_seats', m) for m in self.contest_indices],
        )
        gaps = []
        for m in self.contest_indices:
            a = series('contest_admit_rate', m)
            e = series('contest_expected_p_mean', m)
            if np.isfinite(a) and np.isfinite(e):
                gaps.append(abs(a - e))
        out['contest_expected_vs_realized_gap'] = float(np.mean(gaps)) if gaps else np.nan
        return out

    def update_beliefs(self, ex, inc):
        if len(ex) == 0:
            return
        self.observe(self.kids['cred'][ex], inc)

    def observe(self, c, inc):
        """Update beliefs from realised incomes (NaN = not yet working, e.g. queuing graduates)."""
        ok = np.isfinite(inc)
        c, inc = c[ok], inc[ok]
        if len(c) == 0:
            return
        lw = np.log(np.maximum(inc, 1e-3))
        d = self.p['belief_decay']
        for j in range(self.nlev + 1):
            s = c == j
            if s.sum() >= 5:
                w = s.sum()
                self.B[j] = (d * self.Bn[j] * self.B[j] + w * lw[s].mean()) / (d * self.Bn[j] + w)
                self.Bn[j] = d * self.Bn[j] + w
        # credentials with few recent holders are valued at the prior premium over the next credential down (fixed 1 Nov:
        # otherwise a never-observed level looks worthless and nobody ever tries it - the cold-start trap the triad model hit)
        prior = np.array(self.p['prior_logw'], float)
        for j in range(1, self.nlev + 1):
            if self.p['belief_floor'] and self.Bn[j] < 20:
                self.B[j] = max(self.B[j], self.B[j - 1] + prior[j] - prior[j - 1])

    def record(self, t, ex, inc):
        R, k = self.R, self.kids
        R['year'].append(t)
        att = k['att']
        R.setdefault('enrolled', []).append(int(att.sum()))
        R.setdefault('beliefs', []).append(self.B.copy())
        R.setdefault('lrate', []).append(self.lrate)
        # every yearly series stays aligned with R['year']: a module that has nothing to report in a year (e.g. the
        # labour market before the first leavers) gets a NaN of the right shape, so R[key][t] is always calendar year t.
        # (Fixed 1 Nov 2026: unpadded series were shifted, e.g. China's labour series ran 3 years ahead.)
        n = len(R['year'])
        nanlike = lambda v: np.full(np.shape(v), np.nan) if np.ndim(v) else np.nan
        rec = getattr(self, 'yr_record', {})
        for key, v in rec.items():
            lst = R.setdefault(key, [])
            while len(lst) < n - 1:
                lst.append(nanlike(v))
            lst.append(v)
        for key, lst in R.items():
            if key not in rec and key not in ('year', 'enrolled', 'beliefs', 'lrate') and len(lst) < n:
                lst.append(nanlike(lst[-1]))
        self.yr_record = {}

    def note(self, **kv):
        """Modules call this to add yearly series."""
        if not hasattr(self, 'yr_record'):
            self.yr_record = {}
        self.yr_record.update(kv)

    def run(self):
        for t in range(self.p['T']):
            self.step(t)
        self.X = {kk: np.concatenate([e[kk] for e in self.exits]) for kk in self.exits[0]} if self.exits else {}
        # everyone ever born in the run (exited + still in school), for calendar-year indicator series
        k = self.kids
        rest = {kk: v for kk, v in k.items()}
        rest['inc'] = np.full(len(k['y']), np.nan); rest['exit_year'] = np.full(len(k['y']), -1)
        self.ALL = {kk: np.concatenate([self.X[kk], rest[kk]]) for kk in self.X} if self.X else rest
        out = {}
        for m in self.modules:
            out.update(m.summary(self))
        out.update(self.contest_summary())            # additive Gate-1 diagnostics
        return out
