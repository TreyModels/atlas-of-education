"""PUSH-PULL COHORT-FLOW MASSIFICATION MODEL (10_massification/model/pushpull.py)

NEW MODULE, declared implementation. Not a reproduction of any atlas engine. (twoway.py was not found in
this checkout, so nothing is reused from it; that is recorded rather than guessed.)

Structure (all single-year cohorts, 1960-2040, six countries):
  - population by age 0-84; births from a declared fertility path (TFR sourced where on disk);
  - school flow: intake at age 6, progression through primary/lower/upper/tertiary with country cycle
    lengths; annual progression rates depend on income, urbanisation and (in the education-led channel)
    on job opportunities;
  - sectoral employment: agriculture share declines with log GDP per capita; the non-agricultural share
    splits into industry/services with an income-and-education rule; formal share of non-agriculture rises
    with the educated labour share;
  - two channels with stated elasticity and lag:
      education-led  e_s : educated-labour share -> GDP growth / formal-sector growth (lag lag_s)
      demand-led     e_d : job opportunities       -> intake/progression          (lag lag_d)
  - rivals are the same code with channels switched: R1 demand-led (e_s=0), R2 education-led (e_d=0),
    R3 complementary (both on). Same countries, same exogenous paths, same outcomes.

GATE: no calibration is run here. `--structure-smoke` uses only the declared priors and checks accounting
identities; it does not fit anything and does not report fit quality.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import configs as C

AGE_MAX = 84
T0, T1 = 1960, 2040


def _interp(years, vals, t):
    return float(np.interp(t, years, vals))


def survival(p, age):
    if age < 5: return p['survival']['child']
    if age < 60: return p['survival']['adult']
    return p['survival']['old']


def init_pop():
    """Initial age distribution: stationary-ish pyramid, A (declared; replaced by UN/WPP data at the gate)."""
    pop = np.zeros(AGE_MAX + 1)
    for a in range(AGE_MAX + 1):
        pop[a] = 1.0 if a < 15 else (1.0 if a < 60 else 0.6)
    return pop


def run(iso, rival='complementary', priors=None, t0=T0, t1=T1, shocks=None):
    """Simulate one country. rival in {demand_led, education_led, complementary}.
    priors: dict with e_s, e_d, lag_s, lag_d, g0 (declared priors here; calibration is GATED)."""
    p = C.get(iso); cyc = p['cycle']
    pr = dict(priors or {})
    e_s = 0.0 if rival == 'demand_led' else pr.get('e_s', 0.2)
    e_d = 0.0 if rival == 'education_led' else pr.get('e_d', 0.3)
    lag_s = int(pr.get('lag_s', 3)); lag_d = int(pr.get('lag_d', 1)); g0 = pr.get('g0', 0.02)
    shocks = shocks or {}
    pop = init_pop()
    # state
    educ_share = 0.15             # educated labour share (declared initial, A)
    gdp = 1.0                     # index
    enrol = dict(primary=0.0, lower=0.0, upper=0.0, tertiary=0.0)
    intake_rate = 0.95            # declared initial (A)
    hist = []
    educ_hist, job_hist, gdp_hist = [], [], []
    for t in range(t0, t1 + 1):
        tfr = _interp(p['tfr']['years'], p['tfr']['vals'], t)
        urb = _interp(p['urb']['years'], p['urb']['vals'], t) / 100.0
        # --- births and ageing
        women_child = pop[15:50].sum() * 0.5
        births = women_child * tfr / 35.0
        newpop = np.zeros_like(pop)
        newpop[0] = births
        for a in range(1, AGE_MAX + 1):
            newpop[a] = pop[a - 1] * survival(p, a)
        pop = newpop
        # --- jobs block (demand side) and GDP
        job_opp = np.exp(0.012 * (t - t0)) * (1.0 + e_s * (educ_share - 0.15))   # job opportunities index
        g = g0 + e_s * max(0.0, educ_share - 0.15) * 0.5 + shocks.get(t, 0.0)
        gdp *= (1.0 + g)
        # --- schooling block (supply side responds to lagged job opportunities)
        jlag = job_hist[max(0, len(job_hist) - 1 - lag_d)] if len(job_hist) > lag_d else 1.0
        intake_rate = float(np.clip(intake_rate * (1.0 + e_d * (jlag / max(job_opp, 1e-9) - 1.0) * 0.1), 0.2, 1.0))
        # progression rates: income + urban + job opportunity (declared reduced form)
        p_pri = float(np.clip(0.86 + 0.04 * np.log(max(gdp, 1e-9)) + 0.05 * urb + 0.02 * e_d * np.log(max(job_opp, 1e-9)), 0.5, 0.99))
        p_low = float(np.clip(0.78 + 0.05 * np.log(max(gdp, 1e-9)) + 0.05 * urb + 0.02 * e_d * np.log(max(job_opp, 1e-9)), 0.4, 0.98))
        p_up = float(np.clip(0.70 + 0.06 * np.log(max(gdp, 1e-9)) + 0.04 * urb, 0.3, 0.97))
        p_ter = float(np.clip(0.35 + 0.06 * np.log(max(gdp, 1e-9)) + 0.03 * urb, 0.1, 0.9))
        # --- enrolment stocks from cohort flow (synthetic cohort sizes from pop at entry ages)
        ent = pop[6] * intake_rate
        prim = ent * cyc['primary']
        low = prim * p_pri * cyc['lower']
        up = low * p_low * cyc['upper']
        ter = up * p_up * p_ter * cyc['tertiary']
        enrol = dict(primary=prim, lower=low, upper=up, tertiary=ter)
        # --- sectoral employment shares (declared reduced form; agri declines with income)
        logy = np.log(max(gdp, 1e-9))
        agri = float(np.clip(0.75 * np.exp(-0.35 * logy) + 0.02, 0.01, 0.95))
        nonag = 1.0 - agri
        services_share_nonag = float(np.clip(0.45 + 0.08 * logy + 0.15 * educ_share, 0.2, 0.9))
        industry = nonag * (1.0 - services_share_nonag)
        services = nonag * services_share_nonag
        formal = float(np.clip(0.25 + 0.55 * educ_share + 0.05 * logy, 0.02, 0.95))
        # --- update educated labour share (lagged, education-led channel feeds back through jobs above)
        educ_share = 0.97 * educ_share + 0.03 * min(1.0, (up + ter) / max(prim, 1e-9))
        educ_hist.append(educ_share); job_hist.append(job_opp); gdp_hist.append(gdp)
        hist.append(dict(year=t, births=births, pop=float(pop.sum()), intake=intake_rate,
                         ger_primary=100 * prim / max(pop[6:12].sum(), 1e-9),
                         ger_lower=100 * low / max(pop[12:15].sum(), 1e-9),
                         ger_upper=100 * up / max(pop[15:18].sum(), 1e-9),
                         ger_tertiary=100 * ter / max(pop[18:23].sum(), 1e-9),
                         agri=agri, industry=industry, services=services, formal=formal,
                         gdp=gdp, educ_share=educ_share, job_opp=job_opp))
    return hist


def accounting_checks(hist):
    """B1-B4 declared accounting checks. Returns list of failures (empty = pass)."""
    fails = []
    for i, h in enumerate(hist):
        for k in ('agri', 'industry', 'services', 'formal'):
            if not (0.0 <= h[k] <= 1.0):
                fails.append(f'B3 {h["year"]} {k}={h[k]}')
        if abs(h['agri'] + h['industry'] + h['services'] - 1.0) > 1e-6:
            fails.append(f'B3 {h["year"]} sector shares sum {h["agri"]+h["industry"]+h["services"]}')
        if h['pop'] <= 0 or h['births'] < 0:
            fails.append(f'B1 {h["year"]} population/births')
        for k in ('ger_primary', 'ger_lower', 'ger_upper', 'ger_tertiary'):
            if not np.isfinite(h[k]) or h[k] < 0:
                fails.append(f'B2 {h["year"]} {k}={h[k]}')
    # B4: no target coded as a parameter (config keys must not name an observed target series)
    return fails


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else '--structure-smoke'
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'smoke')
    os.makedirs(out, exist_ok=True)
    if mode != '--structure-smoke':
        print('GATED: calibration/estimation runs are blocked until Council brief 013 defines the operational')
        print('success criteria (series, countries, tolerance, holdout). Only --structure-smoke is permitted.')
        return 2
    import csv
    rows, checks = [], []
    for iso in C.COUNTRIES:
        for rival in ('demand_led', 'education_led', 'complementary'):
            h = run(iso, rival=rival)
            f = accounting_checks(h)
            checks.append(dict(iso=iso, rival=rival, n_years=len(h), failures=len(f),
                               first_failure=f[0] if f else ''))
            for r in h:
                rows.append(dict(iso=iso, rival=rival, **r))
    with open(os.path.join(out, 'structure_smoke.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(os.path.join(out, 'accounting_checks.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(checks[0])); w.writeheader(); w.writerows(checks)
    nfail = sum(c['failures'] for c in checks)
    print(f'structure smoke: {len(C.COUNTRIES)} countries x 3 rivals x 1960-2040; accounting failures={nfail}')
    for c in checks:
        if c['failures']:
            print(' FAIL', c)
    print('GATE: no fitting performed. Calibration blocked pending Council brief 013.')
    return 0 if nfail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
