"""GATE 1b ACCEPTANCE CHECKS — tutoring.py fiscal ledger, prep stock, cap, switches.

Run from the worktree root:

    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine" \
      /Users/treymenefee/neon-boot/venv/bin/python docs/audit/TUTORING_CHECKS.py

`tests/` belongs to qa-verifier; this is the tutoring lane's own local check (contract §10 allows this path).
It runs in two modes:
  * ENGINE mode  — engine-core's §6 API is present (patched core.py): checks run against the real engine.
  * STUB mode    — core.py is not patched yet: a reference stub of the frozen §6 API (weights formula per
                   contract §1.3, exact/MC Plackett-Luce from `eduengine.contest_math`) lets the accounting,
                   prep-stock, cap and switch logic be exercised first. The stub is test scaffolding only.
Exit code 0 iff every check passes.
"""
import os
import sys
import traceback

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "engine"))
sys.path.insert(0, os.path.join(ROOT, "papers", "shadow-education-contest", "code"))

from eduengine.core import CORE_DEFAULTS, Engine                      # noqa: E402
from eduengine.modules.labour import QueueLabour                     # noqa: E402
from eduengine.modules.schools import PrivateSchools, PublicSchools  # noqa: E402
from eduengine.modules.sdg4 import SDG4                              # noqa: E402
from eduengine.modules.tutoring import TutoringMarket                # noqa: E402
import eduengine.contest_math as cm                                  # noqa: E402
from run_hk_korea_comparative import build_arms                      # noqa: E402

TOL = 1e-12


def _core_api_ready():
    need = ('contest_gates', 'contest_candidates', 'contest_seats', 'contest_weights', 'gate_prize_dv')
    return all(hasattr(Engine, n) for n in need)


MODE = 'engine' if _core_api_ready() else 'stub'


# ----------------------------------------------------------------------------------------------- Plackett-Luce
_PL_CALLS = [0]


def _deterministic_test_pl(weights, seats, method='auto', rng=None, n_mc=20000):
    """Test-harness wrapper around contest_math while its large-n `auto` path is still unseeded MC.

    Exact subset DP for n <= 20; otherwise a fixed-seed MC with a call counter, so the harness is
    reproducible and the effort grid is not swamped by unseeded noise. NEVER used by the engine.
    """
    w = np.asarray(weights, dtype=float)
    if w.size <= 20:
        return cm.pl_win_probs_exact(w, seats)
    _PL_CALLS[0] += 1
    r = np.random.default_rng(7919 + _PL_CALLS[0] * 104729)
    return cm.pl_win_probs_mc(w, seats, rng=r, n_mc=6000)[0]


if MODE == 'stub':
    cm.pl_win_probs = _deterministic_test_pl


# ----------------------------------------------------------------------------------------------- stub §6 API
class StubEngine(Engine):
    """Reference stub of ENGINE_INTERFACE_CONTRACT §2/§6 for running tutoring before core.py lands."""

    def add_cohort(self, t):
        old = None if self.kids is None or 'prep_stock' not in self.kids else np.array(self.kids['prep_stock'])
        super().add_cohort(t)
        k = self.kids
        n = len(k['y'])
        if old is None:
            k['prep_stock'] = np.zeros((n, self.nlev), dtype=np.float64)
        else:
            k['prep_stock'] = np.vstack([old, np.zeros((n - old.shape[0], self.nlev), dtype=np.float64)])

    @property
    def contest_gates(self):
        return [(m, g) for m, g in enumerate(self.p['gates']) if g.get('kind') == 'contest']

    def contest_candidates(self, m):
        k, p = self.kids, self.p
        gate = p['gates'][m]
        c = k['att'] & (k['cred'] <= m)
        if gate.get('academic_only'):
            c &= ~k['voc']
        return c

    def contest_seats(self, m):
        return max(int(round(self.p['gates'][m]['share'] * self.p['N'])), 1)

    def _weights(self, m, stock):
        p = self.p
        gate = p['gates'][m]
        r_c = gate.get('r', p['contest_r'])
        alpha = gate.get('alpha', p['contest_alpha'])
        x0 = gate.get('x0', p['contest_x0'])
        L = self.kids['L']
        x = np.maximum(x0 * np.maximum(L, 0.1) / max(self.ends[m], 1) + alpha * stock, 1e-6)
        return x ** r_c

    def contest_weights(self, m, idx=None, stock_override=None):
        cand = self.contest_candidates(m)
        stock = self.kids['prep_stock'][:, m].copy()
        if idx is not None:
            idx = np.asarray(idx, dtype=int)
            if stock_override is not None:
                stock[idx] = np.asarray(stock_override, dtype=float)
            return idx, self._weights(m, stock)[idx]
        cidx = np.flatnonzero(cand)
        return cidx, self._weights(m, stock)[cidx]

    def contest_expected_probs(self, m, idx=None):
        cand = self.contest_candidates(m)
        cidx = np.flatnonzero(cand)
        _pids, w = self.contest_weights(m)
        seats = min(self.contest_seats(m), w.size)
        P = cm.pl_win_probs(w, seats, method=self.p.get('contest_prob_method', 'auto'))
        if idx is None:
            return cidx, P
        idx = np.asarray(idx, dtype=int)
        pos = np.searchsorted(cidx, idx)
        return idx, P[pos]

    def gate_prize_dv(self, m, idx=None):
        p = self.p
        gate = p['gates'][m]
        elw = gate.get('elite_logw', p['elite_logw']) if not gate.get('track_consequence') else 0.0
        dv = np.full(len(self.kids['y']), p['kappa'] * float(elw), dtype=float)
        if idx is not None:
            idx = np.asarray(idx, dtype=int)
            return idx, dv[idx]
        return np.arange(len(self.kids['y'])), dv


ENGINE_CLS = Engine if MODE == 'engine' else StubEngine


# ----------------------------------------------------------------------------------------------- check harness
class CheckTutoring(TutoringMarket):
    """TutoringMarket with per-year assertions at the `measure` hook (pre-compaction, arrays aligned)."""

    def __init__(self, assert_recurrence=False):
        super().__init__()
        self.assert_recurrence = assert_recurrence

    def setup(self, E):
        super().setup(E)
        self.diag = []
        self.legacy_cum = {}
        self.legacy_last = {}

    def measure(self, E, t):
        y, k = E.yr, E.kids
        if 'tut_outlay' not in y:
            return
        att = k['att']
        # §4.1 financial identities
        assert np.array_equal(y['tut_outlay'], y['res_cost'] + y['tut_tax']), "outlay != resource + tax"
        assert abs(float(y['gov_tut_tax'].sum()) - float(y['tut_tax'].sum())) <= 1e-12 * max(1.0, float(y['tut_tax'].sum())), \
            "gov receipts != sum of taxes"
        # §4.2 cash budget: total yearly tutoring outlay may never exceed core's residual liquidity
        assert np.all(y['extra_spend'][att] <= E._cash[att] + 1e-9), "tutoring outlay exceeded E._cash"
        # §4.2 annual cap binds e_t (not the stock)
        eff = y['contest_effort']
        cap = float(E.p['contest_max_e'])
        assert np.all(eff <= cap + 1e-12), "annual contest effort cap violated"
        actual = k['prep_stock']
        # §5 prep-stock recurrence, exactly: att -> (1-rho)*pre + pos_share*e on the assigned column.
        # Only asserted when no gate is reached in the run (core consumes/zeroes the column at the gate).
        if self.assert_recurrence:
            rho = float(E.p['contest_prep_depreciation'])
            ps = self._positional_share(E.p)
            pre = y['prep_stock_pre']
            expected = (1.0 - rho) * pre
            assigned = y['contest_assigned_gate']
            for i in np.flatnonzero(assigned >= 0):
                expected[i, assigned[i]] += ps * eff[i]
            assert np.allclose(actual[att], expected[att], atol=TOL, rtol=0.0), "prep_stock recurrence violated"
            if not att.all():
                assert np.allclose(actual[~att], pre[~att], atol=TOL, rtol=0.0), \
                    "non-attending prep_stock must not change"
        if self.assert_recurrence:
            # exact legacy-equivalence bookkeeping: rho=0 must equal the old cumulative k['contest_e'] sum;
            # rho=1 must equal the memoryless current-year contribution. Keyed by immutable pid.
            pid = np.asarray(k['pid'])
            assigned = y['contest_assigned_gate']
            ps = self._positional_share(E.p)
            for m_ in range(E.nlev):
                for i in np.flatnonzero(att):
                    self.legacy_last[(int(pid[i]), m_)] = 0.0
            for i in np.flatnonzero(assigned >= 0):
                key = (int(pid[i]), int(assigned[i]))
                v = ps * float(eff[i])
                self.legacy_cum[key] = self.legacy_cum.get(key, 0.0) + v
                self.legacy_last[key] = v
        self.diag.append(dict(
            tax=float(y['tut_tax'].sum()), res=float(y['res_cost'].sum()), outlay=float(y['tut_outlay'].sum()),
            gov=float(y['gov_tut_tax'].sum()), effort_sum=float(eff.sum()),
            effort_max=float(eff.max()) if eff.size else 0.0,
            outlay_max=float(y['tut_outlay'].max()), cash_min=float(E._cash[att].min()) if att.any() else 0.0,
            prep_sum=float(actual.sum()), evals=int(y.get('contest_prob_evals', 0)),
            grid_bound=float(y.get('contest_grid_bound', 0.0)), n_att=int(att.sum())))


def _mods(recur=False):
    # no labour module: keeps these checks focused on tutoring (short runs otherwise trip labour.summary)
    return [PublicSchools(), PrivateSchools(), CheckTutoring(recur), SDG4()]


def _known_params(mods):
    known = dict(CORE_DEFAULTS)
    for m in mods:
        known.update(type(m).defaults)
    return known


def run(params, seed=0, engine_cls=None, recur=False):
    mods = _mods(recur)
    known = _known_params(mods)
    accepted = {k: v for k, v in params.items() if k in known}   # runner configs carry unrelated module params
    E = (engine_cls or ENGINE_CLS)(mods, seed=seed, **accepted)
    E.run()
    tutor = E.modules_by_name['tutoring']
    tutor.diag  # keep the per-year diagnostics on the instance for the checks that need them
    return E, tutor.diag


# ----------------------------------------------------------------------------------------------- configs
HK = dict(build_arms()[0][3])          # real 540 HK baseline params


def tiny_params(**over):
    """Single-level N=2 contest economy: candidate count stays <= 20 so PL exact is used (fast, deterministic)."""
    p = dict(HK)
    p.update(N=2, T=14, measure_from=6, levels=[('primary', 6), ('lower', 3)],
             gates=[dict(kind='fixed_bar', bar=2.0), dict(kind='contest', share=0.5, fail='stop')],
             contest_price=0.02, contest_max_e=3.0, contest_alpha=0.25, contest_r=1.5,
             contest_x0=1.0, elite_logw=0.5, contest_prob_method='exact')
    p.update(over)
    return p


def hk_like_params(**over):
    # N small enough that the contest pool (cred==2 children) stays <= 20 -> exact PL, fast and deterministic
    p = dict(HK)
    p.update(N=4, T=14, measure_from=6, contest_price=0.02, contest_max_e=3.0,
             # keep the candidate pool (cred==1 lower-secondary grades) <= 20 for exact, deterministic PL
             gates=[dict(kind='fixed_bar', bar=2.0), dict(kind='contest', share=0.23, fail='track'),
                    dict(kind='fixed_bar', bar=6.0), dict(kind='fixed_bar', bar=10.0)])
    p.update(over)
    return p


RESULTS = []


def check(name):
    def deco(fn):
        try:
            fn()
            RESULTS.append((name, True, ''))
            print(f"PASS  {name}")
        except Exception as exc:                       # noqa: BLE001 - a failed check is data
            RESULTS.append((name, False, f"{type(exc).__name__}: {exc}"))
            print(f"FAIL  {name}: {type(exc).__name__}: {exc}")
            traceback.print_exc(limit=3)
        return fn
    return deco


# ----------------------------------------------------------------------------------------------- checks
@check("mode detected")
def _():
    print(f"      mode={MODE}  core_api_ready={_core_api_ready()}  contest_math={cm.__name__}")


@check("identities + per-quintile reconciliation (tax=0.5, rebate=none)")
def _():
    E, diag = run(tiny_params(contest_tax_rate=0.5))
    R = E.R
    assert len(diag) > 0
    for y in range(len(R['year'])):
        assert abs(R['contest_spend_now'][y] - R['contest_resource_cost'][y] - R['contest_tax_paid'][y]) \
            <= 1e-12 * max(1.0, R['contest_spend_now'][y])
        assert abs(R['gov_tut_receipt'][y] - R['contest_tax_paid'][y]) <= 1e-12 * max(1.0, R['contest_tax_paid'][y])
    tot = float(np.sum(R['contest_spend_now']))
    res_tot = float(np.sum(R['contest_resource_cost']))
    tax_tot = float(np.sum(R['contest_tax_paid']))
    counts = np.array(R['contest_k12_count_by_q'], float)
    rec = sum(float(np.dot(np.array(R['contest_outlay_by_q'][y], float), counts[y]))
              for y in range(len(R['year'])))
    # per-quintile means x counts must reconcile to the aggregate totals (round-trip through means)
    for y in range(len(R['year'])):
        q_out = np.array(R['contest_outlay_by_q'][y], float) * counts[y]
        assert abs(q_out.sum() - R['contest_spend_now'][y]) <= 1e-9 * max(1.0, R['contest_spend_now'][y])
        q_res = np.array(R['contest_res_cost_by_q'][y], float) * counts[y]
        assert abs(q_res.sum() - R['contest_resource_cost'][y]) <= 1e-9 * max(1.0, R['contest_resource_cost'][y])
        q_tax = np.array(R['contest_tax_by_q'][y], float) * counts[y]
        assert abs(q_tax.sum() - R['contest_tax_paid'][y]) <= 1e-9 * max(1.0, R['contest_tax_paid'][y])
    assert tax_tot > 0.0, "tax=0.5 config produced no tax revenue"
    assert tot > res_tot


@check("effort cap binds (contest_max_e=0.05)")
def _():
    E, diag = run(tiny_params(contest_price=0.001, contest_max_e=0.05, contest_tax_rate=0.0))
    assert len(diag) > 0
    assert all(d['effort_max'] <= 0.05 + 1e-12 for d in diag)
    assert max(d['effort_max'] for d in diag) >= 0.05 - 1e-9, "cap never bound"
    # some child must actually sit at the cap
    assert any(d['effort_max'] >= 0.05 - 1e-9 for d in diag)


@check("cash budget never violated (huge cap forces the cash bound)")
def _():
    E, diag = run(tiny_params(contest_price=0.5, contest_max_e=1e6, contest_tax_rate=0.5))
    for d in diag:
        assert d['outlay'] <= d['res'] + d['tax'] + 1e-12
    E2, diag2 = run(tiny_params(contest_price=0.5, contest_max_e=1e6, contest_tax_rate=0.5))
    assert sum(d['outlay'] for d in diag2) > 0.0


@check("tax: household effort falls, government receipts rise (matched seed)")
def _():
    E0, d0 = run(tiny_params(contest_tax_rate=0.0, contest_price=0.02))
    E1, d1 = run(tiny_params(contest_tax_rate=0.5, contest_price=0.02))
    e0 = sum(d['effort_sum'] for d in d0)
    e1 = sum(d['effort_sum'] for d in d1)
    assert e1 <= e0 + 1e-12, f"tax did not reduce effort ({e1} > {e0})"
    tax1 = sum(d['tax'] for d in d1)
    assert tax1 > 0.0, "tax>0 run has no government receipts"
    res0 = sum(d['res'] for d in d0)
    res1 = sum(d['res'] for d in d1)
    assert res1 <= res0 + 1e-12


@check("rebate is credited to households, gov_tax NOT reduced (uniform 0.5)")
def _():
    E, diag = run(tiny_params(contest_tax_rate=0.5, contest_rebate_policy='uniform', contest_rebate_rate=0.5))
    R = E.R
    reb = float(np.sum(R['contest_rebate_total']))
    tax = float(np.sum(R['contest_tax_paid']))
    gov = float(np.sum(R['gov_tut_receipt']))
    assert gov == tax, "rebate must not reduce gross government receipts"
    assert abs(reb - 0.5 * tax) <= 1e-9 * max(1.0, tax)
    assert int(np.max(R['contest_rebate_recipients'])) > 0
    summ = E.modules_by_name['tutoring'].summary(E)
    assert summ['contest_rebate_recipient'] == 'households'


@check("rho=0 = legacy undepreciated accumulation; rho=1 = memoryless (recurrence asserted every year)")
def _():
    # T=5 with a grade-6 gate: no cohort reaches the gate inside the run, so stock is pure accumulation
    for rho in (0.0, 0.5, 1.0):
        # T=8: the grade-9 lower-secondary gate is never reached, so prep stock is pure accumulation
        E, diag = run(tiny_params(T=8, measure_from=4, contest_prep_depreciation=rho), recur=True)
        assert len(diag) >= 4, f"too few years for rho={rho}"
        assert all(np.isfinite(d['prep_sum']) for d in diag)
    E0, d0 = run(tiny_params(T=8, measure_from=4, contest_prep_depreciation=0.0), recur=True)
    E1, d1 = run(tiny_params(T=8, measure_from=4, contest_prep_depreciation=1.0), recur=True)
    # legacy anchor: undepreciated stock exceeds the memoryless endpoint
    assert sum(d['prep_sum'] for d in d0) > sum(d['prep_sum'] for d in d1) - 1e-12


@check("learning switch adds prep to learned skills; positional anchor keeps prep_stock (documented direction)")
def _():
    p_pos = tiny_params(contest_prep_mode='positional', contest_price=0.01)
    p_lrn = tiny_params(contest_prep_mode='learning', contest_prep_learning_gain=0.5, contest_price=0.01)
    p_both = tiny_params(contest_prep_mode='both', contest_prep_learning_gain=0.5,
                         contest_prep_positional_share=1.0, contest_price=0.01)
    Epos, _ = run(p_pos)
    Elrn, _ = run(p_lrn)
    Eboth, _ = run(p_both)
    diag_pos = Epos.modules_by_name['tutoring'].diag
    diag_lrn = Elrn.modules_by_name['tutoring'].diag
    # documented direction: the reported learning channel is OFF in positional mode and ON in both/learning;
    # where it is on, prep raises learned skill among children who reached the contest level.
    def meanL(E):
        X = E.ALL
        sel = np.asarray(X['cred']) >= 1
        return float(np.mean(np.asarray(X['L'])[sel]))
    diag_both = Eboth.modules_by_name['tutoring'].diag
    add_pos = float(np.nansum(np.array(Epos.R['contest_learning_added'], float)))
    add_both = float(np.nansum(np.array(Eboth.R['contest_learning_added'], float)))
    add_lrn = float(np.nansum(np.array(Elrn.R['contest_learning_added'], float)))
    assert add_pos == 0.0, "positional mode must not create a learning channel"
    assert add_both > 0.0, "both mode must create a learning channel"
    assert meanL(Eboth) > meanL(Epos) + 1e-9, f"learning channel did not raise learned skills ({meanL(Eboth)} <= {meanL(Epos)})"
    # the switch is physically distinct: 'learning' accumulates NO positional prep stock; 'positional' does.
    # (compare the peak stock over the run: by the final year the last cohorts may not have reached the gate pool)
    assert max(d['prep_sum'] for d in diag_lrn) <= 1e-12, "learning mode must not accumulate positional prep stock"
    assert max(d['prep_sum'] for d in diag_pos) > 0.0, "positional mode must accumulate prep stock"
    assert max(d['prep_sum'] for d in diag_both) > 0.0, "both mode must accumulate positional prep stock"
    # learning-only effort is nonzero exactly where the learning value beats the private cost (mvl-driven); if the
    # tiny config prices it at zero (mvl==0 at the top level) then no effort is the correct direction.
    assert add_lrn >= 0.0


@check("zero prize => zero positional effort and zero contest outlay (contract §11 test 1)")
def _():
    E, diag = run(tiny_params(elite_logw=0.0))
    assert sum(d['effort_sum'] for d in diag) == 0.0
    assert sum(d['outlay'] for d in diag) == 0.0
    assert np.nansum(np.array(E.R['contest_e_mean'], float)) == 0.0


@check("zero contest effectiveness => effort cannot raise admission, so e_t=0 (contract §11 test 2)")
def _():
    E, diag = run(tiny_params(contest_alpha=0.0))
    assert sum(d['effort_sum'] for d in diag) == 0.0


@check("universal seat => P=1, no positional return, e_t=0 (contract §11 test 3)")
def _():
    p = tiny_params()
    p['gates'] = [dict(kind='fixed_bar', bar=2.0),
                  dict(kind='contest', share=1.0, share_of='applicants', fail='stop')]
    E, diag = run(p)
    assert sum(d['effort_sum'] for d in diag) == 0.0


@check("no double count: firm_rev uses RESOURCE cost, not outlay")
def _():
    E0, _ = run(tiny_params(contest_tax_rate=0.0))
    E1, _ = run(tiny_params(contest_tax_rate=0.5))
    R0, R1 = E0.R, E1.R
    # matched seed: same own/firm tutoring draws, so the differences are exactly the ledger split
    drev = float(np.sum(R1['firm_rev']) - np.sum(R0['firm_rev']))
    dres = float(np.sum(R1['contest_resource_cost']) - np.sum(R0['contest_resource_cost']))
    dout = float(np.sum(R1['contest_spend_now']) - np.sum(R0['contest_spend_now']))
    assert abs(drev - dres) <= 1e-6 * max(1.0, abs(dres)), (drev, dres)
    assert abs(dout - dres) > 0.0, "tax wedge should make outlay differ from resource cost"


@check("540 runner compatibility: required E.R keys + E.ALL fields still produced")
def _():
    E, _ = run(hk_like_params())
    R = E.R
    for key in ('tut_k12_spend', 'tut_k12_rate', 'tut_g12_rate', 'tut_k12_rate_by_q', 'tut_k12_spend_by_q',
                'contest_e_mean', 'contest_spend_now', 'contest_resource_cost', 'contest_tax_paid',
                'gov_tut_receipt'):
        assert key in R, f"missing E.R key {key}"
        arr = np.array(R[key], float)
        assert np.isfinite(arr[E.p['measure_from']:]).any(), f"E.R[{key}] has no finite measured values"
    for key in ('cohort', 'q', 'elite', 'g'):
        assert key in E.ALL, f"missing E.ALL key {key}"
    # legacy K-12 spend path still aggregates the (gross) household outlay exactly once
    assert abs(float(np.sum(R['contest_spend_now'])) - float(np.sum(R['contest_resource_cost']))
               - float(np.sum(R['contest_tax_paid']))) <= 1e-6 * max(1.0, float(np.sum(R['contest_spend_now'])))
    # 540-era local variable `contest_spend_now` is now the household-outlay series with that name
    assert np.all(np.array(R['contest_spend_now'], float) >= 0.0)


@check("non-contest legacy worlds still run unchanged")
def _():
    import worlds
    E = worlds.make('exam_race', N=60, T=14, measure_from=6, seed=2)
    E.run()
    for key in ('tut_k12_spend', 'tut_k12_rate', 'tut_g12_rate', 'firm_rev'):
        assert key in E.R
    assert 'contest_spend_now' not in E.R or float(np.nansum(np.array(E.R['contest_spend_now'], float))) == 0.0


@check("invalid switch/policy parameters fail loudly at Engine construction")
def _():
    for bad in (dict(contest_prep_mode='nonsense'),
                dict(contest_rebate_policy='nonsense'),
                dict(contest_prep_depreciation=1.5),
                dict(contest_tax_rate=-0.1),
                dict(contest_prep_mode='learning', contest_prep_learning_gain=0.0)):
        try:
            mods = _mods()
            ENGINE_CLS(mods, seed=0, **{k: v for k, v in tiny_params(**bad).items()
                                        if k in _known_params(mods)})
        except ValueError:
            continue
        raise AssertionError(f"invalid config accepted: {bad}")


@check("rho=0 equals the legacy cumulative stock; rho=1 equals the memoryless flow (pid-matched)")
def _():
    E0, _ = run(tiny_params(T=8, measure_from=4, contest_prep_depreciation=0.0), recur=True)
    E1, _ = run(tiny_params(T=8, measure_from=4, contest_prep_depreciation=1.0), recur=True)
    for E, rho in ((E0, 0.0), (E1, 1.0)):
        tutor = E.modules_by_name['tutoring']
        k = E.kids
        pid = np.asarray(k['pid'])
        book = tutor.legacy_cum if rho == 0.0 else tutor.legacy_last
        checked = 0
        for i in range(len(pid)):
            key = (int(pid[i]), 1)          # tiny config has one contest gate, at level index 1
            want = float(book.get(key, 0.0))
            got = float(k['prep_stock'][i, 1])
            assert abs(got - want) <= 1e-9 * max(1.0, abs(want)), \
                f"rho={rho}: prep_stock {got} != legacy-equivalent {want} for pid {key[0]}"
            checked += 1
        assert checked > 0
    # documented contrast: the undepreciated anchor keeps strictly more memory than the memoryless endpoint
    peak0 = max(d['prep_sum'] for d in E0.modules_by_name['tutoring'].diag)
    peak1 = max(d['prep_sum'] for d in E1.modules_by_name['tutoring'].diag)
    assert peak0 >= peak1 - 1e-12, (peak0, peak1)   # cumulative memory can only bound memoryless from above


@check("effort grid cost is 9 probability evaluations per gate-year; grid/refinement error is bounded")
def _():
    import eduengine.modules.tutoring as du
    E, diag = run(tiny_params(contest_price=0.02, contest_max_e=50.0))   # cap high -> interior optimum
    evals = [d['evals'] for d in diag]
    assert max(evals) == 9, f"expected 9 batched PL evaluations per active gate-year, got {set(evals)}"
    assert all(e in (0, 9) for e in evals), set(evals)
    assert any(e == 9 for e in evals), "no active gate-year in the test config"
    bounds = [d['grid_bound'] for d in diag if d['evals']]
    assert max(bounds) < 0.25, f"grid/refinement bounding error too large: {max(bounds)}"
    # coarse (9 + analytic quadratic) vs fine (25-point) reference: same qualitative effort level
    old_grid = du._PREP_GRID.copy()
    try:
        E_coarse, _ = run(tiny_params(contest_price=0.02, contest_max_e=50.0))
        du._PREP_GRID = np.linspace(0.0, 1.0, 25)
        E_fine, _ = run(tiny_params(contest_price=0.02, contest_max_e=50.0))
    finally:
        du._PREP_GRID = old_grid
    ec = float(np.nansum(np.array(E_coarse.R['contest_e_mean'], float)))
    ef = float(np.nansum(np.array(E_fine.R['contest_e_mean'], float)))
    assert ef > 0 and ec > 0
    rel = abs(ec - ef) / ef
    assert rel <= 0.25, f"coarse grid effort differs from 25-point reference by {100*rel:.1f}%"
    print(f"      coarse-vs-fine effort: {100*rel:.1f}%  max bound={max(bounds):.3g}  evals/year={set(evals)}")


# ----------------------------------------------------------------------------------------------- main
def main():
    print(f"=== TUTORING_CHECKS === mode={MODE}")
    npass = sum(1 for _, ok, _ in RESULTS if ok)
    nfail = len(RESULTS) - npass
    print(f"\n{npass}/{len(RESULTS)} checks passed" + (f", {nfail} FAILED" if nfail else ""))
    if MODE == 'stub':
        print("NOTE: ENGINE mode did not run — core.py §6 API absent. Re-run this script after engine-core lands;"
              " the stub validates the tutoring ledger/prep-stock logic, not the patched gate path.")
    return 0 if nfail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
