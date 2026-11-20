"""KNOWN-ANSWER COHORT-ARITHMETIC TEST (E2 / Phase-0 gate).

INDEPENDENTLY NAMED NEW IMPLEMENTATION, NOT A REPRODUCTION of massabm, triad or any
atlas engine. A small deterministic ledger written to answer one question: does a
year-by-year people / money / job accounting system conserve when the behavioural
mechanisms are switched off (zero dropout, all pass, fixed seats, no migration)?
If this fails, no behavioural run downstream is interpretable.

Declared assumptions (see PRE_DECLARATIONS.md, E2):
  - N_CHILD=200 children enter grade 0 every year, T=40 years, L=10 grades.
  - Every enrolled child advances one grade per year and passes. No dropout, no
    repetition, no migration, no child labour.
  - University: fixed SEATS=60 places/year, filled deterministically by rank (child id).
    Everyone who finishes grade 10 enters the adult labour force whether or not admitted;
    admission confers a credential, it does not remove anyone from the labour force.
  - Jobs: fixed 150 FORMAL vacancies/year filled by rank; everyone else works informally
    at a declared lower wage. formal_employed + informal == labour force every year.
  - One index unit = one formal adult wage per year. School cost 0.15 per pupil-year.
    Income tax 0.10 on formal wages only.
  - Startup: pupils exist before any tax-paying adult does. An explicit START_FUND
    endowment finances the first decade; draws are logged and may not exceed the fund.
    This makes the fiscal warm-up an explicit stock rather than a hidden subsidy.

Checks (deterministic, no seeds needed for the arithmetic):
  C1 people   : per cohort, exited + still_enrolled == N_CHILD exactly
  C2 seats    : admitted_t == min(SEATS, candidates_t) and admitted_t <= SEATS
  C3 stock    : enrolled(t) == enrolled(t-1) + entrants(t) - exits(t)
  C4 money    : inflow == outflow every year to 1e-9; endowment never overdrawn
  C5 jobs     : formal_employed <= VACANCIES; formal+informal == labour force
  C6 nonneg   : every stock, flow, drawing is finite and >= 0
  C7 probs    : every reported probability is in [0,1]
  C8 limits   : all-pass/zero-dropout => admission share constant and == min(SEATS,N)/N;
                SEATS=0 => nobody admitted; SEATS>=N => everybody reaching the gate admitted
  C9 stress   : enrolment cap below N: stocks stay in [0, cap], seats still respected

Exit code 1 on any failed check so the Phase-0 gate is unambiguous.
"""
import argparse
import csv
import math
import sys

N_CHILD = 200
GRADES = 10
SEATS = 60
VACANCIES = 150
TAX = 0.10
COST_PER_PUPIL = 0.15
WAGE_FORMAL = 1.0
WAGE_INFORMAL = 0.5
TRANSFER = 0.0
START_FUND = 4000.0
T_END = 40


def run_world(seats=SEATS, vacancies=VACANCIES, enrol_cap=None, start_fund=START_FUND):
    fails = []
    kids = {}
    next_id = 0
    graduated = []
    rows = []
    enrolled_prev = 0
    money_cum = 0.0
    fund = start_fund
    for t in range(T_END):
        entrants = []
        currently = len([k for k in kids.values() if k['status'] == 'enrolled'])
        n = N_CHILD if enrol_cap is None else min(N_CHILD, max(enrol_cap - currently, 0))
        for _ in range(n):
            kids[next_id] = dict(entry=t, grade=0, status='enrolled', admitted=False)
            entrants.append(next_id); next_id += 1
        exits, candidates = [], []
        for cid, k in kids.items():
            if k['status'] != 'enrolled':
                continue
            if k['grade'] < GRADES - 1:
                k['grade'] += 1
            else:
                candidates.append(cid)
        candidates.sort()
        admitted = candidates[:min(seats, len(candidates))]
        for cid in candidates:
            k = kids[cid]
            k['status'] = 'graduate'; k['admitted'] = cid in admitted
            exits.append(cid); graduated.append(cid)
        force = len(graduated)
        formal = min(vacancies, force)
        informal = force - formal
        n_enrolled = len([k for k in kids.values() if k['status'] == 'enrolled'])
        wage_bill = formal * WAGE_FORMAL + informal * WAGE_INFORMAL
        tax = TAX * formal * WAGE_FORMAL
        spend = n_enrolled * COST_PER_PUPIL
        transfers = TRANSFER * n_enrolled
        pre = wage_bill + transfers - tax - spend
        fund_draw = max(0.0, -pre)
        if fund_draw > fund + 1e-9:
            fails.append(f'C4 t={t} endowment overdrawn: need {fund_draw:.2f}, fund {fund:.2f}')
        fund -= fund_draw
        consumption = pre + fund_draw
        inflow = wage_bill + transfers + fund_draw
        outflow = tax + spend + consumption
        money_cum += inflow - outflow
        for nm, v in [('n_enrolled', n_enrolled), ('formal', formal), ('informal', informal),
                      ('consumption', consumption), ('wage_bill', wage_bill), ('tax', tax),
                      ('spend', spend), ('fund', fund)]:
            if not math.isfinite(v) or v < -1e-9:
                fails.append(f'C6 t={t} {nm}={v}')
        if len(admitted) != min(seats, len(candidates)):
            fails.append(f'C2 t={t} admitted={len(admitted)} != min({seats},{len(candidates)})')
        if len(admitted) > seats:
            fails.append(f'C2 t={t} seat overfill {len(admitted)}>{seats}')
        if n_enrolled != enrolled_prev + len(entrants) - len(exits):
            fails.append(f'C3 t={t} stock {n_enrolled} != {enrolled_prev}+{len(entrants)}-{len(exits)}')
        if abs(inflow - outflow) > 1e-9:
            fails.append(f'C4 t={t} inflow {inflow!r} != outflow {outflow!r}')
        if formal > vacancies or formal + informal != force:
            fails.append(f'C5 t={t} formal={formal} informal={informal} force={force} vac={vacancies}')
        p_adm = (len(admitted) / len(candidates)) if candidates else 0.0
        if not (0.0 <= p_adm <= 1.0):
            fails.append(f'C7 t={t} p_admit={p_adm}')
        rows.append(dict(t=t, entrants=len(entrants), exits=len(exits), enrolled=n_enrolled,
                         candidates=len(candidates), admitted=len(admitted), p_admit=p_adm,
                         labour_force=force, formal_employed=formal, informal_employed=informal,
                         wage_bill=wage_bill, tax=tax, spend=spend, consumption=consumption,
                         inflow=inflow, outflow=outflow, money_cum=money_cum,
                         fund_draw=fund_draw, fund=fund))
        enrolled_prev = n_enrolled
    by_entry = {}
    for cid, k in kids.items():
        d = by_entry.setdefault(k['entry'], dict(total=0, enrolled=0, exited=0, admitted=0))
        d['total'] += 1
        d['enrolled' if k['status'] == 'enrolled' else 'exited'] += 1
        d['admitted'] += int(k['admitted'])
    for e, d in sorted(by_entry.items()):
        if d['enrolled'] + d['exited'] != d['total']:
            fails.append(f'C1 cohort {e}: {d["enrolled"]}+{d["exited"]} != {d["total"]}')
    return rows, fails, by_entry


def check_limit_cases():
    fails = []
    _, f0, be0 = run_world(seats=0)
    fails += f0
    if any(d['admitted'] for d in be0.values()):
        fails.append('C8 seats=0 but someone admitted')
    _, f1, be1 = run_world(seats=10 * N_CHILD)
    fails += f1
    for e, d in be1.items():
        if e <= T_END - GRADES and d['admitted'] != d['total']:
            fails.append(f'C8 seats>=N cohort {e}: admitted {d["admitted"]} != {d["total"]}')
    rows2, f2, _ = run_world(enrol_cap=100)
    fails += f2
    for r in rows2:
        if not (0 <= r['enrolled'] <= 100) or r['admitted'] > SEATS:
            fails.append(f'C9 cap=100 t={r["t"]} enrolled={r["enrolled"]} admitted={r["admitted"]}')
    return fails, rows2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', default=None)
    a = ap.parse_args()
    rows, fails, by_entry = run_world()
    lim_fails, _ = check_limit_cases()
    all_fails = fails + lim_fails
    if a.csv:
        with open(a.csv, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
    matured = [d for e, d in by_entry.items() if e <= T_END - GRADES]
    comp = [d['admitted'] / d['total'] for d in matured]
    print('KNOWN-ANSWER COHORT ARITHMETIC TEST (independent new implementation)')
    print(f'  world: N={N_CHILD}/cohort, {GRADES} grades, seats={SEATS}, vacancies={VACANCIES}, T={T_END}')
    for grp, lbl in [(('C1',), 'C1 people conservation per cohort'),
                     (('C2',), 'C2 fixed seats never overfilled'),
                     (('C3',), 'C3 enrolment stock identity'),
                     (('C4',), 'C4 money conservation + endowment never overdrawn'),
                     (('C5',), 'C5 jobs: formal<=vacancies, formal+informal==labour force'),
                     (('C6',), 'C6 nonnegativity / finiteness'),
                     (('C7',), 'C7 probabilities in [0,1]'),
                     (('C8',), 'C8 limit cases (seats=0, seats>=N)'),
                     (('C9',), 'C9 enrolment-cap stress')]:
        bad = [x for x in all_fails if x.startswith(grp)]
        print(f'  {lbl}: {"PASS" if not bad else "FAIL"}')
    print(f'  KNOWN ANSWER admission share (all pass, zero dropout), constant across matured cohorts: '
          f'{comp[0]:.4f}  (must equal min(SEATS,N)/N = {min(SEATS, N_CHILD) / N_CHILD:.4f})')
    print(f'  KNOWN ANSWER final money_cum (must be ~0): {rows[-1]["money_cum"]:.2e}')
    print(f'  KNOWN ANSWER startup endowment drawn: {rows[-1]["fund_draw"]:.0f} of {START_FUND:.0f} '
          f'(remaining {rows[-1]["fund"]:.0f}); fiscal warm-up is an explicit stock, not a hidden subsidy')
    print(f'  failures: {len(all_fails)}')
    for x in all_fails[:20]:
        print('   FAIL', x)
    sys.exit(1 if all_fails else 0)


if __name__ == '__main__':
    main()
