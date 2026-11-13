"""The measurement layer: one simulated world, many instruments ("Seeing Like a State", Scott 1998).

The engine simulates what children actually do. Each function here simulates how one kind of source would REPORT it.
Gaps between instruments are often not model errors but differences in what is being measured. The bounty ledger
(ledger.py) uses the instrument tag of each observation to compare like with like.

Instruments (v0.1)
  completion_cohort     UIS SDG 4.1.2: cohort 3-5 years above the intended age of the last grade, completed it
  gross_intake_last     World Bank 'primary completion rate': entrants to the last grade / population of intended age.
                        Can exceed 100% (late entrants, denominator error) - e.g. Hong Kong 105% in 2020
  oos_admin             administrative out-of-school: 1 - enrolment / projected population (denominator error drifts
                        between censuses -> year-to-year 'yo-yo')
  oos_household         household-survey out-of-school (DHS/MICS): children outside households (street, institutions)
                        are outside the sampling frame, so they vanish from the denominator
  literacy              'true' (learning >= threshold), 'census_proxy' (household head says yes if the person went to
                        school a few years), 'dhs_card' (secondary schooling assumed literate; others read one sentence)
  tutoring              'broad' (any paid tutoring) vs 'narrow' (outside school only - payments to the own teacher
                        inside school are not counted), the likely gap between CSES and small studies in Cambodia
"""
import numpy as np

LIT_THRESHOLD = 4.0      # grade-equivalents: reads a simple passage (assumed anchor, see struts.py S9)


def _ages(E, Y):
    """Age of every person in E.ALL in calendar year Y."""
    return Y - (E.p['start_year'] + E.ALL['cohort']) + E.p['entry_age']


def completion_cohort(E, level, Y):
    m = level
    intended = E.p['entry_age'] + E.ends[m] - 1
    a = _ages(E, Y)
    sel = (a >= intended + 3) & (a <= intended + 5)
    if not sel.any():
        return np.nan
    ca = E.ALL['comp_age'][sel, m]
    return float(np.mean(np.isfinite(ca) & (ca <= a[sel])))


def gross_intake_last(E, level, Y, denom_error=0.0):
    t = Y - E.p['start_year']
    if t < 0 or t >= len(E.R['att_by_grade']):
        return np.nan
    entrants = E.R['new_by_grade'][t][E.ends[level] - 1]    # new entrants to the last grade (repeaters excluded), any age
    return float(entrants / (E.p['N'] * (1 + denom_error)))


def _enrolled_pop(E, a0, a1, Y):
    t = Y - E.p['start_year']
    enr, pop = 0, 0
    for a in range(a0, a1 + 1):
        c = t - (a - E.p['entry_age'])
        if c < 0:
            continue
        enr += E.census.get((c, a), 0); pop += E.p['N']
    return enr, pop


def oos_admin(E, a0, a1, Y, denom_error=0.0):
    enr, pop = _enrolled_pop(E, a0, a1, Y)
    return float(1 - enr / (pop * (1 + denom_error))) if pop else np.nan


def oos_household(E, a0, a1, Y):
    """Street children are outside the household sampling frame."""
    enr, pop = _enrolled_pop(E, a0, a1, Y)
    if not pop:
        return np.nan
    a = _ages(E, Y)
    exit_age = E.ALL['exit_year'] + E.p['start_year'] - (E.p['start_year'] + E.ALL['cohort']) + E.p['entry_age']
    on_street = E.ALL['street'] & (a >= a0) & (a <= a1) & (exit_age <= a)
    return float(1 - enr / max(pop - on_street.sum(), 1))


def street_children(E, a0, a1, Y):
    """True number of street children of these ages per 1,000 children of these ages (what no survey sees)."""
    a = _ages(E, Y)
    exit_age = E.ALL['exit_year'] - E.ALL['cohort'] + E.p['entry_age']
    on = E.ALL['street'] & (a >= a0) & (a <= a1) & (exit_age <= a)
    pop = E.p['N'] * (a1 - a0 + 1)
    return float(1000 * on.sum() / pop)


def literacy(E, Y, instrument='true', a0=15, a1=24, seed=0):
    r = np.random.default_rng(seed)
    a = _ages(E, Y)
    sel = (a >= a0) & (a <= a1)
    L, g, st = E.ALL['L'][sel], E.ALL['g'][sel], E.ALL['street'][sel]
    if instrument == 'true':
        lit = L >= LIT_THRESHOLD
        return float(lit.mean())
    if instrument == 'census_proxy':        # the household head answers for everyone; schooling stands in for skill
        lit = (g >= 4) | ((g >= 1) & (r.random(len(g)) < 0.5))
        keep = ~st | (r.random(len(g)) < 0.5)                  # censuses half-cover people outside households
        return float(lit[keep].mean())
    if instrument == 'dhs_card':            # secondary schooling assumed literate; others read one sentence aloud
        reads = L + 0.8 * r.standard_normal(len(L)) >= LIT_THRESHOLD - 1.0
        lit = (g >= 9) | reads
        return float(lit[~st].mean())                          # household frame: street youth are not sampled
    raise ValueError(instrument)


def tutoring(E, Y, grades, definition='broad'):
    t = Y - E.p['start_year']
    if 'tut_own_by_grade' not in E.R or t < 0 or t >= len(E.R['tut_own_by_grade']):
        return np.nan
    own = np.array(E.R['tut_own_by_grade'][t]); firm = np.array(E.R['tut_firm_by_grade'][t])
    gi = [g - 1 for g in grades]
    weights = np.array(E.R['att_by_grade'][t], float)[gi]
    rates = (own + firm)[gi] if definition == 'broad' else firm[gi]
    return float(np.dot(rates, weights) / weights.sum()) if weights.sum() > 0 else np.nan


INSTRUMENTS = {
    'completion_cohort': 'UIS SDG 4.1.2 completion rate (household surveys + UIS model)',
    'gross_intake_last': 'Gross intake ratio to the last grade (World Bank "completion rate"; administrative)',
    'oos_admin': 'Administrative out-of-school rate (enrolment / projected population)',
    'oos_household': 'Household-survey out-of-school rate (DHS/MICS frame excludes non-household children)',
    'literacy_true': 'Learning at or above the reading threshold (what an assessment would show)',
    'literacy_census_proxy': 'Census: household head reports whether each person can read and write',
    'literacy_dhs_card': 'DHS/MICS: secondary schooling assumed literate; others read one sentence',
    'tutoring_broad': 'Any paid supplementary tutoring (small studies, PEER broad definition)',
    'tutoring_narrow': 'Paid tutoring outside school only (household expenditure surveys such as CSES)',
}


def private_share(E, Y, level_grades):
    """Share of pupils in the given grades enrolled in private schools (UIS 'percentage of enrolment in private institutions')."""
    t = Y - E.p['start_year']
    if 'priv_by_grade' not in E.R or t >= len(E.R['priv_by_grade']) or t < 0:
        return np.nan
    pg, ng = np.array(E.R['priv_by_grade'][t], float), np.array(E.R['att_by_grade'][t], float)
    gi = [g - 1 for g in level_grades]
    return float(pg[gi].sum() / max(ng[gi].sum(), 1))


def youth_unemployment(E, Y):
    t = Y - E.p['start_year']
    if 'youth_unemp' not in E.R or t >= len(E.R['youth_unemp']) or t < 0:
        return np.nan
    return float(E.R['youth_unemp'][t])
