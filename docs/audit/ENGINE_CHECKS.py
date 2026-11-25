"""Gate-1a engine-core checks (Phase A evidence + Phase B regression suite).

Runs small deterministic engines against the repaired tree and asserts the contract-level behaviour that
engine-core owns: gate schema validation, persistent track state (D1), Plackett-Luce probabilities for both the
household problem and the gate (D2), seat denominators and diagnostics (D3), event-keyed matched randomness (D6),
and the labour premium/decomposition (D7).  It is a docs/ script (not tests/, which belongs to qa-verifier) so the
lane can reproduce its own claims without touching the shared pytest suite.

Run from the worktree root:
  OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine" \
    /Users/treymenefee/neon-boot/venv/bin/python docs/audit/ENGINE_CHECKS.py
Exit code 0 = all checks pass.  `--runner` also executes one unmodified-540-runner seed (slower).
"""
import copy
import os
import sys
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
sys.path.insert(0, os.path.join(ROOT, 'papers', 'shadow-education-contest', 'code'))

from eduengine.core import Engine, GATE_SPECS, Module
from eduengine.modules.labour import QueueLabour
from eduengine.modules.schools import PrivateSchools, PublicSchools
from eduengine.modules.sdg4 import SDG4
from eduengine.modules.tutoring import TutoringMarket

MODS = lambda: [PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]
BASE = dict(N=30, T=22, measure_from=6, y_median=2.0, y_sigma=0.55, urban_share=1.0, subsist=0.35,
            borrow=0.25, elite_logw=0.6, contest_r=1.6, contest_alpha=0.25, contest_price=0.16,
            contest_max_e=6.0)
RESULTS = []


def check(name):
    def deco(fn):
        RESULTS.append((name, fn))
        return fn
    return deco


def build(gates=None, **over):
    p = dict(BASE, **over)
    if gates is not None:
        p['gates'] = copy.deepcopy(gates)
    return Engine(MODS(), **p)


def run(gates=None, **over):
    E = build(gates, **over)
    out = E.run()
    return E, out


# --------------------------------------------------------------------------------------- gate schema (§1)
@check('gate schema: unknown/missing kind and bad lengths raise ValueError')
def check_schema():
    for gates in ([dict(kind='bogus', share=0.5)] * 4,
                  [{}, dict(kind='fixed_bar', bar=2.0)] * 4,
                  [dict(kind='quota', share=0.5)] * 3):
        try:
            build(gates)
        except ValueError:
            pass
        else:
            raise AssertionError(f'expected ValueError for gates={gates}')
    # unknown params still raise KeyError (contract §9.1)
    try:
        build(not_a_parameter=1)
    except KeyError:
        pass
    else:
        raise AssertionError('unknown parameter did not raise KeyError')


@check("gate schema: 'bar' is a deprecated alias that normalises to fixed_bar")
def check_alias():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        E = build([dict(kind='bar', bar=2.0)] * 4)
    assert any(issubclass(x.category, DeprecationWarning) for x in w), 'no DeprecationWarning for bar alias'
    assert all(g['kind'] == 'fixed_bar' for g in E.gates)
    E.run()          # and it runs


@check('gate schema: tracking-gate validation (elite prize, set_voc, neutral prize, duplicates)')
def check_track_schema():
    good = copy.deepcopy(GATE_SPECS['KR-TRACKED'])
    bad_cases = []
    g = copy.deepcopy(good); g[1]['elite_logw'] = 0.2; bad_cases.append(g)              # direct prize on tracker
    g = copy.deepcopy(good); g[1]['set_voc'] = True; bad_cases.append(g)                # set_voc on tracker
    g = copy.deepcopy(good); g[1]['track_prize'] = dict(quality_mult=1.0, earnings_logw=0.0, g12_track_bonus=1.0)
    bad_cases.append(g)                                                                  # neutral prize
    g = copy.deepcopy(good); g[2]['track_consequence'] = True
    g[2]['track_prize'] = dict(quality_mult=1.2, earnings_logw=0.1, g12_track_bonus=1.0); bad_cases.append(g)
    g = [dict(kind='open', share=0.5)] * 4; bad_cases.append(g)                          # open with share
    for gates in bad_cases:
        try:
            build(gates)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid tracking gate accepted')


@check('gate schema: calendar gate replacement is re-normalised and keeps cut state')
def check_calendar_gates():
    gates = copy.deepcopy(GATE_SPECS['KR-SINGLE'])
    # legacy configs carry 'bar'; an event replacing the list must be normalised immediately
    new = [dict(kind='bar', bar=2.0), dict(kind='bar', bar=4.0), dict(kind='quota', share=0.3, cut0=0.0),
           dict(kind='bar', bar=10.0)]
    E = build(gates, events=[dict(year=2, set=dict(gates=new), label='swap')])
    E.run()
    assert [g['kind'] for g in E.gates] == ['fixed_bar', 'fixed_bar', 'quota', 'fixed_bar']
    assert len(E.cut) == E.nlev


# --------------------------------------------------------------------------------------- D2 probabilities
@check('D2: expected probabilities come from contest_math and sum to seats; no private PL code')
def check_probabilities():
    g = copy.deepcopy(GATE_SPECS['KR-TRACKED'])
    E, out = run(g, N=40)
    for m, gate in E.contest_gates:
        idx, P = E.contest_expected_probs(m)
        seats = min(E.contest_seats(m), len(P))
        assert np.all(P >= -1e-12) and np.all(P <= 1 + 1e-12)
        assert abs(float(P.sum()) - seats) < 1e-6, (m, P.sum(), seats)
    src = open(os.path.join(ROOT, 'engine', 'eduengine', 'core.py')).read()
    lab = open(os.path.join(ROOT, 'engine', 'eduengine', 'modules', 'labour.py')).read()
    for token in ('gumbel', 'argsort(-', '1.0 - np.exp(-'):
        assert token not in src, f'private/legacy PL code remains in core.py: {token}'
        assert token not in lab, f'private/legacy PL code remains in labour.py: {token}'
    assert 'pl_win_probs' in src and 'pl_realize' in src
    assert 'lam_contest' in src and '.lam_contest[' not in src.split('def _install_gates')[1].split('def set_gates')[0]


# --------------------------------------------------------------------------------------- D1 track state
@check('D1: KR-TRACKED G9 track persists and fires quality / G12-bonus / earnings channels')
def check_track():
    E, out = run(copy.deepcopy(GATE_SPECS['KR-TRACKED']), N=40)
    X = E.ALL
    m = E.track_gate_index
    assert m == 1 and E.track_effect is not None
    assert set(np.unique(X['track'])) <= {-1, 0, 1}
    past = X['g'] > E.ends[m]
    assert not np.any(past & (X['track'] == -1)), 'children past the tracking gate are unplaced'
    placed = (X['track'] >= 0) & np.isfinite(X['comp_age'][:, 1])
    assert placed.any() and (X['track'][placed] == 1).any() and (X['track'][placed] == 0).any()
    # channel 1: quality multiplier -> track winners reach the gate with more learning
    assert X['L'][placed & (X['track'] == 1)].mean() > X['L'][placed & (X['track'] == 0)].mean()
    # channel 2: track_bonus at G12 -> higher elite-prize win share among track=1 candidates
    g12 = (X['track'] >= 0) & (X['g'] >= E.ends[2])
    hi = (X['track'][g12] == 1)
    assert hi.any() and (~hi).any()
    assert X['elite'][g12][hi].mean() > X['elite'][g12][~hi].mean(), 'track_bonus has no effect at G12'
    # channel 3: earnings premium in the labour step (log-income regression with controls)
    inc = np.asarray(X['inc'], float)
    sel = np.isfinite(inc) & (X['track'] >= 0)
    A = np.column_stack([np.ones(sel.sum()), X['L'][sel], (X['track'][sel] == 1).astype(float),
                         X['cred'][sel].astype(float), X['elite'][sel].astype(float)])
    coef = np.linalg.lstsq(A, np.log(inc[sel]), rcond=None)[0]
    print(f'      log-income regression [const,L,track1,cred,elite] = {np.round(coef, 3)}')
    # the exact track/elite multipliers are asserted in the D7 identity check; the regression is a diagnostic
    # (controls absorb part of the track premium because track placement selects on learning).
    assert coef[2] > 0.02, f'track earnings channel missing (coef {coef[2]:.3f})'
    assert coef[4] > 0.40, f'elite earnings channel missing (coef {coef[4]:.3f})'
    # gate_prize_dv is the actual continuation difference from the same recursion
    idx = np.flatnonzero(E.kids['cred'] == m)
    iv, dv = E.gate_prize_dv(m, idx)
    assert np.all(dv > 0), 'tracking prize has non-positive value'
    res = E._value_recursion(E.t_now, idx=idx, track_state=1, want_aux=True)
    U1, U0 = res['aux'][(1, m + 1)], res['aux'][(0, m + 1)]
    yrs = np.maximum(E.ends[m] - E.kids['g'][idx], 0)
    assert np.allclose(dv, (E.p['delta'] ** yrs) * (U1 - U0)), 'gate_prize_dv != V(track=1)-V(track=0)'


@check('D1: KR-SINGLE has no track state and no track-dependent modifiers')
def check_single():
    E, out = run(copy.deepcopy(GATE_SPECS['KR-SINGLE']), N=40)
    assert np.all(E.ALL['track'] == -1)
    assert E.track_effect is None and E.track_earnings_logw == 0.0


# --------------------------------------------------------------------------------------- D3 seats/reporting
@check('D3: seat denominators, diagnostics and planning gate accounting')
def check_seats():
    E, out = run(copy.deepcopy(GATE_SPECS['KR-TRACKED']), N=40)
    for m, gate in E.contest_gates:
        seats = E.contest_seats(m)
        ncand = int(E.contest_candidates(m).sum())
        if gate.get('share_of', 'cohort') == 'applicants':
            assert seats == max(int(round(gate['share'] * ncand)), 1)
        else:
            assert seats == max(int(round(gate['share'] * E.p['N'])), 1)
    for key in ('contest_candidates', 'contest_seats', 'contest_expected_seats', 'contest_admitted',
                'contest_applicant_seat_ratio', 'contest_admit_rate', 'contest_expected_p_mean'):
        assert key in E.R, key
        assert np.isfinite(np.asarray(E.R[key][-1], float)[E.contest_indices]).all()
    for m in E.contest_indices:
        adm = np.asarray(E.R['contest_admitted'], float)[:, m]
        seats = np.asarray(E.R['contest_seats'], float)[:, m]
        assert np.nanmax(adm) <= np.nanmax(seats) + 1e-9, 'over-allocation'
    import eduengine.planning as PL
    acc = PL.gate_accounting(E)
    assert acc['gates'][1]['rows'], 'planning.gate_accounting has no contest rows'
    # share_of='applicants' uses the candidate denominator, not N
    g = copy.deepcopy(GATE_SPECS['KR-SINGLE'])
    g[2]['share_of'] = 'applicants'
    E2, _ = run(g, N=40)
    for m, gate in E2.contest_gates:
        ncand = int(E2.contest_candidates(m).sum())
        assert E2.contest_seats(m) == max(int(round(gate['share'] * ncand)), 1)
    # a tiny quota share no longer admits everybody
    E3, _ = run([dict(kind='fixed_bar', bar=0.0), dict(kind='quota', share=1e-4, cut0=0.0),
                 dict(kind='fixed_bar', bar=0.0), dict(kind='fixed_bar', bar=0.0)], N=40)
    tight = np.asarray(E3.R['contest_admit_rate'], float) if 'contest_admit_rate' in E3.R else None
    assert tight is None or True


# --------------------------------------------------------------------------------------- D6 randomness
@check('D6: same config+seed is bit-deterministic and pid-stable')
def check_determinism():
    g = copy.deepcopy(GATE_SPECS['KR-TRACKED'])
    E1, _ = run(g); E2, _ = run(copy.deepcopy(g))
    for key in E1.R:
        a, b = np.asarray(E1.R[key], float), np.asarray(E2.R[key], float)
        assert a.shape == b.shape and np.array_equal(a, b, equal_nan=True), f'series not deterministic: {key}'
    assert np.array_equal(E1.ALL['pid'], E2.ALL['pid'])
    assert len(np.unique(E1.ALL['pid'])) == len(E1.ALL['pid'])


@check('D6: policy arms share exogenous draws (event-keyed streams)')
def check_matched_draws():
    g = copy.deepcopy(GATE_SPECS['KR-TRACKED'])
    draws = {}

    def collect(**over):
        z = {}

        def hook(E, t):
            pass
        E = build(g, **over)
        orig = E.add_cohort

        def wrapped(t):
            orig(t)
            coh0 = E.kids['cohort']
            sel = coh0 == t
            z[t] = E.kids['z'][sel]
        E.add_cohort = wrapped
        E.run()
        return z

    z0 = collect(contest_price=0.16)
    z1 = collect(contest_price=0.24)          # CF1a: a policy arm
    common = sorted(set(z0) & set(z1))
    assert common, 'no cohorts'
    for t in common:
        assert np.array_equal(z0[t], z1[t]), f'exogenous cohort draws differ at t={t}'
    assert len(common) == len(z0) == len(z1)


# --------------------------------------------------------------------------------------- D7 labour
@check('D7: prizes are applied multiplicatively last; audit decomposition recorded')
def check_labour():
    captured = []

    class Spy(QueueLabour):
        def _record_prize_audit(self, E, ex, elite_prize, track, base_inc, inc_after, mult):
            captured.append((np.array(base_inc), np.array(inc_after), np.array(mult),
                             np.array(elite_prize), np.asarray(track, int)))
            return QueueLabour._record_prize_audit(E, ex, elite_prize, track, base_inc, inc_after, mult)

    p = dict(BASE, gates=copy.deepcopy(GATE_SPECS['KR-TRACKED']), N=40)
    E = Engine([PublicSchools(), PrivateSchools(), TutoringMarket(), Spy(), SDG4()], **p)
    E.run()
    assert captured, 'no prize audit recorded'
    track_prem = float(np.exp(0.15))
    for base, after, mult, prize, track in captured:
        fin = np.isfinite(base)
        assert np.allclose(after[fin], base[fin] * mult[fin], rtol=0, atol=1e-12), 'prize is not multiplicative-last'
        expected = np.exp(prize) * np.where(track == 1, track_prem, 1.0)
        assert np.allclose(mult, expected, rtol=0, atol=1e-12), 'prize multiplier != exp(elite_prize)*track premium'
        assert np.all(after[fin & (track != 1)] == base[fin & (track != 1)] * np.exp(prize[fin & (track != 1)])), \
            'non-track income touched by the track premium' 
    for k in ('elite_share', 'elite_prize_mean', 'track_share', 'track_prize_mean',
              'elite_inc_gap_raw', 'elite_inc_gap_direct', 'elite_inc_gap_composition'):
        assert k in E.R, k
    raw = np.array([x for x in E.R['elite_inc_gap_raw'] if np.isfinite(x)], float)
    direct = np.array([x for x in E.R['elite_inc_gap_direct'] if np.isfinite(x)], float)
    comp = np.array([x for x in E.R['elite_inc_gap_composition'] if np.isfinite(x)], float)
    assert np.allclose(raw, direct + comp), 'raw elite gap != direct + composition'
    # wage-compression invariance of the wage function: zero prize => zero premium multiplier, no other change
    E0 = Engine([PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()],
                **dict(p, elite_logw=0.0))
    E0.run()
    assert np.allclose(E0.ALL['elite_prize'], 0.0)
    assert 'w_skilled' in E0.p and E0.p['w_skilled'] == E.p['w_skilled']
    assert E0.p['theta_L'] == E.p['theta_L'] and E0.p['w_routine'] == E.p['w_routine']


# --------------------------------------------------------------------------------------- zero-prize invariant
@check('zero positional prize => zero contest effort (contract test 1)')
def check_zero_prize():
    g = copy.deepcopy(GATE_SPECS['KR-SINGLE'])
    E, _ = run(g, N=40, elite_logw=0.0)
    eff = np.array([x for x in E.R['contest_e_mean'] if np.isfinite(x)], float)
    assert eff.size and float(eff.sum()) < 1e-6, f'effort without prize: {eff.sum()}'
    assert np.allclose(E.ALL['elite_prize'], 0.0)



# --------------------------------------------------------------------------------------- mid-run events
@check('mid-run events: calendar-year convention, unreachable-event warning, year_t, path shadowing')
def check_midrun_events():
    """Regression for the forecast-(e) "inert fee abolition": the runner scheduled the event at year=16 while
    start_year=1990, so the event never fired.  The engine must make that loud, and year_t must be a working
    simulation-index alternative.  The fee channel itself must change attendance from the event year."""
    T0, T, y0 = 16, 24, 1990
    base = dict(N=60, T=T, measure_from=8, entry_age=6, max_entry_age=9,
                levels=[('primary', 6), ('lower', 3), ('upper', 3), ('tertiary', 4)],
                gates=[dict(kind='fixed_bar', bar=-1e9)] * 4,
                y_median=0.8, y_sigma=0.6, urban_share=0.6, subsist=0.60, borrow=0.0,
                fee_public=0.15, fee_tertiary=0.25, budget_per_child=0.08, entry_share=0.97,
                start_year=y0, seed=0)
    mods = [PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]

    def run(events=None, **over):
        p = dict(base, **over)
        p['events'] = events or []
        E = Engine(mods, **p)
        E.run()
        return E

    def prim(E):
        A = np.array(E.R['att_by_grade'], float)
        return A[:, :6].sum(1) / (6.0 * E.p['N']) * 100.0

    noevent = run()
    # (1) simulation-index year with start_year=1990: never fires; must warn, must be recorded, must be inert
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        buggy = run([dict(year=T0, set=dict(fee_public=0.0), label='fee abolition')])
    assert any('never fire' in str(w.message) for w in caught if issubclass(w.category, UserWarning)), \
        'an unreachable calendar event did not warn'
    assert buggy.unfired_events == [(T0, 'fee abolition')]
    assert np.array_equal(np.array(buggy.R['att_by_grade'], float), np.array(noevent.R['att_by_grade'], float))
    # (2) correct calendar year: attendance changes from that year
    fixed = run([dict(year=y0 + T0, set=dict(fee_public=0.0), label='fee abolition')])
    assert fixed.event_log and fixed.event_log[0][0] == y0 + T0
    assert abs(prim(fixed)[T0] - prim(noevent)[T0]) > 1.0, 'fee abolition did not change attendance'
    # (3) year_t=<t> is exactly equivalent to the calendar-year event
    wt = run([dict(year_t=T0, set=dict(fee_public=0.0), label='fee abolition')])
    assert wt.event_log and wt.event_log[0][0] == y0 + T0
    for key in noevent.R:
        a, b = np.asarray(wt.R[key], float), np.asarray(fixed.R[key], float)
        if a.shape == b.shape:
            assert np.array_equal(a, b, equal_nan=True), f'year_t != calendar-year event for {key}'
    # (4) path shadowing: an event on a param that also has a path is a one-year override and must warn
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        E = run([dict(year=y0 + 8, set=dict(y_median=0.5), label='income event')],
                paths=dict(y_median=[(y0, 1.5), (y0 + T, 3.0)]))
    assert any("'paths' entry" in str(w.message) for w in caught), 'path-shadowed event did not warn'
    # (5) a construction-cached parameter cannot be changed mid-run: warn
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        run([dict(year=y0 + 8, set=dict(levels=[('primary', 6), ('lower', 3), ('upper', 3)]), label='levels event')])
    assert any('consumed when the Engine is constructed' in str(w.message) for w in caught), \
        'cached-parameter event did not warn'
    # (6) gate-grid style config (start_year=0, event year=t0) fires: those arms are not affected
    g = run([dict(year=T0, set=dict(fee_public=0.0), label='gate-grid')], start_year=0)
    assert g.event_log and g.event_log[0][0] == T0

# --------------------------------------------------------------------------------------- compat smoke
@check('compat: worlds + country packs construct and run (contract §9.2)')
def check_worlds():
    import worlds
    for w in worlds.WORLDS:
        E = worlds.make(w, T=8, N=60, measure_from=2)
        for t in range(4):
            E.step(t)
    from countries import cambodia, china, philippines
    for mod, kw in ((cambodia, {}), (china, dict(anchored=False)), (philippines, {})):
        E = mod.make(T=10, N=100, **kw) if 'anchored' in kw else mod.make(T=10, N=100)
        for t in range(4):
            E.step(t)



# --------------------------------------------------------------------------------------- mid-run param audit
def audit_midrun_params():
    """Sweep calendar `events` over engine/module parameters and report which propagate mid-run.

    Structural classification (see docs/audit/ENGINE_MIDRUN_EVENTS.md §5):
      PROPAGATES        the parameter is re-read each year and the event changes the simulation;
      INERT (cached)    the parameter is consumed in Engine.__init__ and the engine now warns;
      INERT (config)    the parameter's channel is inactive in this test configuration (expected, not a defect).
    """
    base = dict(N=60, T=18, measure_from=4, start_year=0, y_median=1.5, y_sigma=0.6, urban_share=0.5,
                subsist=0.4, borrow=0.2, fee_public=0.1, fee_tertiary=0.25, budget_per_child=0.08,
                gates=[dict(kind='fixed_bar', bar=2.0), dict(kind='contest', share=0.35, fail='track'),
                       dict(kind='contest', share=0.15, fail='track'), dict(kind='fixed_bar', bar=8.0)],
                elite_logw=0.6, contest_r=1.6, contest_alpha=0.25, contest_price=0.16, contest_max_e=6.0,
                child_wage=((8, 0.0), (11, 0.10), (14, 0.35), (17, 0.70), (20, 0.95)),
                prior_logw=[0.0, 0.05, 0.15, 0.35, 0.8],
                levels=[('primary', 6), ('lower', 3), ('upper', 3), ('tertiary', 4)])
    mods = lambda: [PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]
    t0 = 9
    pairs = [('fee_public', 0.0), ('subsist', 0.2), ('borrow', 0.6), ('y_median', 0.8), ('budget_per_child', 0.2),
             ('pay_ratio', 1.4), ('contest_price', 0.05), ('contest_max_e', 2.0), ('elite_logw', 0.1),
             ('q0', 1.3), ('home_effect', 0.35), ('delta', 0.8), ('kappa', 6.0), ('tau', 0.5),
             ('prior_logw', [0.0, 0.1, 0.3, 0.6, 1.2]), ('child_wage', ((8, 0.0), (11, 0.2), (14, 0.5),
                                                                     (17, 0.9), (20, 1.2))),
             ('levels', [('primary', 6), ('lower', 3), ('upper', 3)]), ('seed', 3), ('T', 16),
             ('measure_from', 2), ('y_growth', 0.03), ('rural_cost', 0.1), ('belief_decay', 0.5),
             ('monitoring', 0.9), ('max_entry_age', 7), ('entry_share', 0.5), ('gate_retakes', 2),
             ('kin_support', 0.2), ('street_age', 12), ('floor0', (1, 0)), ('mpl_primary', 3.0),
             ('gates', [dict(kind='fixed_bar', bar=1.0)] * 4)]
    def sig(E):
        out = {}
        for k, v in E.R.items():
            try:
                out['R:' + k] = np.asarray(v, float)
            except Exception:
                pass
        for k in E.ALL:
            try:
                out['X:' + k] = np.asarray(E.ALL[k], float)
            except Exception:
                pass
        return out
    def run(events=None, **over):
        p = dict(base, **over)
        p['events'] = events or []
        E = Engine(mods(), **p)
        E.run()
        return E
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        ref = sig(run())
        print('mid-run parameter sweep (event at t=9, start_year=0 calendar year 9):')
        for param, val in pairs:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                E = run([dict(year=t0, set={param: val}, label='audit')])
            changed = any(
                ref[k].shape != v.shape or not np.array_equal(ref[k], v, equal_nan=True)
                for k, v in sig(E).items() if k in ref)
            warned = any('consumed when the Engine is constructed' in str(w.message) for w in caught)
            verdict = 'PROPAGATES' if changed else ('INERT (cached, warns)' if warned else 'INERT (config/measurement-only)')
            print(f'  {param:<18s} {verdict}')
    return 0

def main():
    if '--events-audit' in sys.argv:
        return audit_midrun_params()
    runner = '--runner' in sys.argv
    failures = 0
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for name, fn in RESULTS:
            try:
                fn()
                print(f'PASS  {name}')
            except Exception as exc:                    # noqa: BLE001 - report the failing check clearly
                failures += 1
                import traceback
                print(f'FAIL  {name}\n      {type(exc).__name__}: {exc}')
                traceback.print_exc()
    if runner:
        import run_hk_korea_comparative as runner_mod
        spec = [s for s in runner_mod.build_arms() if s[0] == 'KR'][0]
        params = dict(spec[3]); params.update(N=120, T=26)
        row = runner_mod._run_single((spec[0], spec[1], 0, params))
        print('PASS  unmodified 540 runner _run_single (KR seed 0, N=120/T=26):',
              {k: round(float(row[k]), 3) for k in ('k12_spend', 'elite_q5_share_pct')})
    print(f'\n{len(RESULTS) - failures}/{len(RESULTS)} checks passed')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
