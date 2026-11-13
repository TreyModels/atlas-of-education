"""Unit tests for engine features (beyond the accounting checks). Run: python tests.py"""
import os, sys, warnings; warnings.filterwarnings('ignore')
import numpy as np
import eduengine as ee
import worlds as W
from eduengine import measure as M

R = []
def t(name, ok, detail=''):
    R.append(ok); print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")

def small(world='low_pay', **kw):
    E = W.make(world, N=600, T=50, measure_from=20, **kw); o = E.run(); return E, o

print('TESTS')
# closed stage: nobody holds the closed credential alone; skipped stage completed at the same age as the one below
E, o = small(level_open=[None, None, [(0, 0), (100, 0)], None])
X = E.ALL; c2 = (X['cred'] == 2).sum(); same = np.isfinite(X['comp_age'][:, 2]) & np.isfinite(X['comp_age'][:, 1])
t('closed stage: no one ends with only the skipped credential', c2 == 0, f'holders of credential 2: {c2}')
t('closed stage: skipped level completed at same age as the level below',
  bool(np.all(X['comp_age'][same, 2] == X['comp_age'][same, 1])) and same.sum() > 0, f'{same.sum()} children')
t('closed stage: no one fails the closed gate', not np.any((X['reason'] == 2) & (X['g'] == 12) & (X['cred'] == 3)))
# events fire once
E = W.make('low_pay', N=300, T=30, events=[dict(year=10, set=dict(pay_ratio=0.9), label='x')]); E.run()
t('event fires once and changes the parameter', len(E.event_log) == 1 and E.p['pay_ratio'] == 0.9)
# paths interpolate
E = W.make('low_pay', N=300, T=30, paths=dict(pay_ratio=[(0, 0.5), (29, 1.0)])); E.run()
t('path interpolates to its end value', abs(E.p['pay_ratio'] - 1.0) < 1e-9)
# repetition
E0, _ = small(promote_bar=0.0); E1, _ = small(promote_bar=0.75)
t('no repetition when promote_bar = 0', int(E0.ALL['repeats'].sum()) == 0)
t('repetition appears when learning lags', int(E1.ALL['repeats'].sum()) > 0, f"{int(E1.ALL['repeats'].sum())} repeated years")
oa0 = M.oos_admin(E0, 12, 14, 2045 - 2045 + 40); oa1 = M.oos_admin(E1, 12, 14, 40)
print(f'  [INFO] repetition and lower-secondary OOS: {oa0:.3f} -> {oa1:.3f} (diagnostic only)')
# retakes
Ea, oa = small(gate_retakes=0, promote_bar=0.0); Eb, ob = small(gate_retakes=1, promote_bar=0.0)
t('retakes reduce gate-failure exits', ob['exit_reasons']['gate_fail'] <= oa['exit_reasons']['gate_fail'] and int(Eb.ALL['retakes'].sum()) > 0,
  f"{oa['exit_reasons']['gate_fail']:.3f} -> {ob['exit_reasons']['gate_fail']:.3f}")
# queue
_, q0 = small('exam_race', queue_on=False); _, q1 = small('exam_race', queue_on=True)
t('graduate queue off -> no graduate unemployment', q0['grad_unemp'] == 0)
t('graduate queue on -> some graduate unemployment', q1['grad_unemp'] > 0, f"{q1['grad_unemp']:.3f}")
# competitive labour now values degrees
_, oc = small('exam_race', mods=dict(labour='competitive'))
t('competitive labour: tertiary completion > 0 (skill = degree)', oc['completion_tertiary'] > 0.05, f"{oc['completion_tertiary']:.3f}")
# luxury axiom
E = ee.build([], N=10, T=1); y = np.array([0.2, 0.6, 1.0, 1.6, 3.0]); nf = E.need_frac(y)
t('child-labour need falls with household income', bool(np.all(np.diff(nf) < 0)), str(np.round(nf, 2)))
# gross intake ratio responds to an understated population
E, _ = small()
t('gross intake ratio rises when the population is understated', M.gross_intake_last(E, 0, 40, -0.2) > M.gross_intake_last(E, 0, 40))
# v0.3.1: yearly series stay aligned with the calendar even when a module skips early years
E, _ = small('exam_race', queue_on=True)
n = len(E.R['year'])
t('every yearly series has one entry per year', all(len(v) == n for v in E.R.values()),
  str({k: len(v) for k, v in E.R.items() if len(v) != n}))
# anchoring stops on request; the frozen wedge then carries enrolment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from countries import cambodia as KH
Ea = KH.make(N=300, T=46); Ea.run()
Eb = KH.make(N=300, T=46, anchor_stop=2020); Eb.run()
ca, cb = M.completion_cohort(Ea, 0, 2019), M.completion_cohort(Eb, 0, 2019)
t('anchor_stop: identical before the stop year', abs(ca - cb) < 1e-12, f'{ca:.3f} vs {cb:.3f}')
t('anchor_stop: a frozen wedge is used after it', Eb.frozen is not None and Ea.frozen is None)
# tutoring firms employ graduates; a full commercial ban removes those jobs
from countries import china as CN
Ec = CN.make(N=300, T=46); Ec.run()
tj = Ec.R['tutor_jobs']; y0 = Ec.p['start_year']
t('tutoring jobs exist before Double Reduction and shrink after it', tj[2019 - y0] > 2 * tj[2023 - y0] > 0,
  f'{tj[2019 - y0]:.3f} -> {tj[2023 - y0]:.3f}')
# planning core: the reconstructed-cohort identity closes exactly on the agents; staffing default is unchanged
from eduengine import planning as PL
t('planning identity closes on the agents (Cambodia)', max(PL.closure(Ea)) < 1e-9, f'{max(PL.closure(Ea)):.2e}')
Ef = KH.make(N=300, T=46, staffing='budget'); Ef.run()
t('staffing="budget" is the default and reproduces it', np.allclose(np.nan_to_num(Ef.R['ptr']), np.nan_to_num(Ea.R['ptr'])))
En = KH.make(N=300, T=46, staffing='norm'); En.run()
t('staffing="norm" holds pupil-teacher ratio near target', abs(np.nanmean(En.R['ptr'][-10:]) - En.p.get('ptr_target', 35)) < 8, f"{np.nanmean(En.R['ptr'][-10:]):.1f}")
t('degree-holder queue is recorded and never exceeds the all-graduate queue', 'deg_queue' in Ec.R and all(a <= b + 1e-9 for a, b in zip(np.nan_to_num(Ec.R['deg_queue']), np.nan_to_num(np.array(Ec.R['queue'], float) / Ec.p['N']))))
import atlas_coverage as COV
from eduengine import ledger as LGR
_cv = COV.build()
t('coverage page counts match the scoring ledger', _cv['observations'] + _cv['other_observations'] == len(LGR.OBS) and sum(_cv['by_country'].values()) == _cv['observations'], f"{_cv['observations']} observations")
print('ALL PASS' if all(R) else f'{R.count(False)} FAILED')
sys.exit(0 if all(R) else 1)
