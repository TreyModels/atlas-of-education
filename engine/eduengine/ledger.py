"""Observation registry and discrepancy ledger: every gap between the model and a historical observation becomes a row,
compared instrument-to-instrument, with a tolerance set by data quality. Open rows are the bounty tickets.

Tolerance: within 10% of the observed value or 0.03 absolute, whichever is larger, widened for low-quality data.
"""
import numpy as np
from . import measure as M

# status -> extra tolerance (absolute)
STATUS_TOL = {'UIS': 0.0, 'UIS-volatile': 0.10, 'GEM': 0.05, 'survey': 0.05, 'unverified': 0.10, 'stylised': 0.08}

UIS = 'UNESCO UIS release May 2026, via measuredworld.com (re-check in the UIS data browser)'

# (country, indicator, instrument, args, year, value, status, source)
OBS = []


def _add(country, ind, instr, args, series, status, source):
    for y, v in series.items():
        OBS.append(dict(country=country, indicator=ind, instrument=instr, args=args, year=y, value=v, status=status, source=source))


_add('cambodia', 'completion_primary', 'completion_cohort', dict(level=0),
     {2000: .3434, 2005: .5895, 2008: .6145, 2010: .7107, 2014: .7228, 2019: .7817, 2021: .8232}, 'UIS', UIS)
_add('cambodia', 'completion_lower', 'completion_cohort', dict(level=1),
     {2000: .1739, 2005: .2676, 2008: .3183, 2010: .3668, 2014: .4052, 2019: .4587, 2021: .5604}, 'UIS', UIS)
_add('cambodia', 'completion_upper', 'completion_cohort', dict(level=2),
     {2000: .0436, 2005: .1039, 2008: .1307, 2010: .1698, 2014: .2123, 2019: .2178, 2021: .2665}, 'UIS', UIS)
_add('cambodia', 'oos_primary', 'oos_admin', dict(a0=6, a1=11),
     {2015: .0829, 2018: .1092, 2020: .0943, 2021: .1105, 2024: .0369}, 'UIS-volatile', UIS)
_add('cambodia', 'oos_lower', 'oos_admin', dict(a0=12, a1=14), {2015: .1342, 2020: .2029, 2021: .2255, 2024: .1759}, 'UIS-volatile', UIS)
_add('cambodia', 'tutoring_g56', 'tutoring_narrow', dict(grades=[5, 6]), {2004: .20, 2015: .28}, 'GEM',
     'CSES via Marshall & Fukao 2019, cited in GEM Report 2026 Cambodia case study')
_add('cambodia', 'tutoring_primary_broad', 'tutoring_broad', dict(grades=[1, 2, 3, 4, 5, 6]), {2008: .62}, 'unverified',
     'Bray & Bunly 2005; Dawson 2009 (range 0.525-0.71), via Brehm 2016')

_add('philippines', 'completion_primary', 'completion_cohort', dict(level=0),
     {2000: .8351, 2004: .8556, 2008: .8473, 2010: .8677, 2013: .8745, 2017: .9192, 2022: .9585}, 'UIS', UIS)
_add('philippines', 'completion_lower', 'completion_cohort', dict(level=1),
     {2000: .6503, 2004: .6608, 2008: .6796, 2010: .7110, 2013: .7127, 2017: .8125, 2022: .8416}, 'UIS', UIS)
_add('philippines', 'completion_upper', 'completion_cohort', dict(level=2),
     {2000: .6013, 2004: .6036, 2008: .6409, 2010: .6612, 2013: .6747, 2017: .7643, 2022: .6701}, 'UIS', UIS)

_add('china', 'completion_primary', 'completion_cohort', dict(level=0), {2010: .9669, 2014: .9721, 2018: .9776, 2020: .9919}, 'UIS', UIS)
_add('china', 'completion_lower', 'completion_cohort', dict(level=1), {2010: .8494, 2014: .8256, 2018: .9027, 2020: .9574}, 'UIS', UIS)
_add('china', 'completion_upper', 'completion_cohort', dict(level=2), {2010: .4397, 2014: .6087, 2018: .7499, 2020: .8752}, 'UIS', UIS)

_add('kenya', 'completion_primary', 'completion_cohort', dict(level=0),
     {2003: .5518, 2008: .7843, 2014: .8414, 2019: .8043, 2022: .8532, 2024: .9078}, 'UIS', UIS)


WB = 'UIS via World Bank WDI, via indexmundi.com'
P1, P2, P3 = list(range(1, 7)), list(range(7, 10)), list(range(10, 13))
_add('cambodia', 'private_primary', 'private_share', dict(grades=P1), {2019: .0568}, 'UIS', WB)
_add('cambodia', 'tutoring_lower_broad', 'tutoring_broad', dict(grades=P2), {2019: .57}, 'unverified', 'UNESCO PEER profile via ChatGPT (2019 study, not checked)')
_add('philippines', 'tutoring_grade6', 'tutoring_broad', dict(grades=[6]), {2010: .407}, 'survey', 'ADB/CERC 2012 via GMA News')
_add('philippines', 'tutoring_grade10', 'tutoring_broad', dict(grades=[10]), {2010: .465}, 'survey', 'ADB/CERC 2012 via GMA News (level unspecified)')
_add('philippines', 'private_primary', 'private_share', dict(grades=list(range(1, 7))), {2019: .0934}, 'UIS', WB)
_add('philippines', 'private_secondary', 'private_share', dict(grades=list(range(7, 13))), {2019: .2434}, 'UIS', WB)
_add('china', 'tutoring_k12', 'tutoring_broad', dict(grades=list(range(1, 13))), {2017: .37, 2023: .136}, 'survey',
     'CIEFR household surveys 2017 and 2023 (Wei 2024)')
_add('china', 'private_primary', 'private_share', dict(grades=P1), {2020: .0889}, 'UIS', WB)
_add('china', 'private_secondary', 'private_share', dict(grades=P2 + P3), {2020: .1439}, 'UIS', WB)
_add('china', 'youth_unemployment', 'youth_unemployment', {}, {2019: .12, 2023: .19}, 'stylised',
     'NBS urban 16-24 rate, approx. (about 12% in 2019; 21.3% peak June 2023; series revised 2024); the model measures graduates queuing, not the NBS definition')


def model_value(E, ob):
    i, a, Y = ob['instrument'], ob['args'], ob['year']
    if i == 'completion_cohort': return M.completion_cohort(E, a['level'], Y)
    if i == 'oos_admin': return M.oos_admin(E, a['a0'], a['a1'], Y)
    if i == 'oos_household': return M.oos_household(E, a['a0'], a['a1'], Y)
    if i == 'tutoring_broad': return M.tutoring(E, Y, a['grades'], 'broad')
    if i == 'tutoring_narrow': return M.tutoring(E, Y, a['grades'], 'narrow')
    if i == 'private_share': return M.private_share(E, Y, a['grades'])
    if i == 'youth_unemployment': return M.youth_unemployment(E, Y)
    raise ValueError(i)


def ledger(E, country, train_until=2015):
    rows = []
    for ob in [o for o in OBS if o['country'] == country]:
        v = model_value(E, ob)
        tol = max(0.10 * ob['value'], 0.03) + STATUS_TOL[ob['status']]
        gap = v - ob['value'] if np.isfinite(v) else np.nan
        rows.append(dict(ob, model=v, gap=gap, tol=tol, within=bool(np.isfinite(gap) and abs(gap) <= tol),
                         split='train' if ob['year'] <= train_until else 'test'))
    return rows


def score(rows):
    out = {}
    for split in ('train', 'test'):
        r = [x for x in rows if x['split'] == split]
        out[split] = (sum(x['within'] for x in r), len(r))
    return out


def fmt(rows):
    L = [f"{'indicator':24s} {'instrument':18s} {'year':>5s} {'observed':>9s} {'model':>7s} {'gap':>7s} {'tol':>5s}  status       split  verdict"]
    for x in sorted(rows, key=lambda x: (x['indicator'], x['year'])):
        L.append(f"{x['indicator']:24s} {x['instrument']:18s} {x['year']:5d} {x['value']:9.3f} {x['model']:7.3f} {x['gap']:+7.3f} "
                 f"{x['tol']:5.2f}  {x['status']:12s} {x['split']:5s}  {'ok' if x['within'] else 'OPEN TICKET'}")
    return '\n'.join(L)
