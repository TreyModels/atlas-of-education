"""Country configurations for the push-pull cohort-flow massification model (10_massification/model).

Every value is labelled:
  S = sourced (observed series / named source; series on disk in 04_data unless stated)
  E = estimated (derived from a named series by a stated rule)
  A = assumed (judgement; no direct evidence on disk)
  F = to be fitted under Council brief 013 (LEFT EMPTY HERE - the gate has not landed)
No observed target (GER, completion, sector share) is used as a parameter value anywhere in this file.
The F slots are parameter *ranges*, not target values.
"""
import numpy as np

# --- fertility paths: S from WDI SP.DYN.TFRT.IN where on disk (PHL/KHM/HKG/CHN); KOR/JPN assumed (A)
TFR = {
    'PHL': dict(years=[1990, 2000, 2010, 2020], vals=[4.32, 3.75, 3.31, 2.08], label='S'),
    'KHM': dict(years=[1990, 2000, 2010, 2020], vals=[5.64, 3.79, 2.86, 2.70], label='S'),
    'HKG': dict(years=[1990, 2000, 2010, 2020], vals=[1.27, 1.03, 1.13, 0.88], label='S'),
    'CHN': dict(years=[1990, 2000, 2010, 2020], vals=[2.51, 1.63, 1.69, 1.24], label='S'),
    'KOR': dict(years=[1990, 2000, 2010, 2020], vals=[1.57, 1.47, 1.23, 0.84], label='A (WDI not on disk for KOR here)'),
    'JPN': dict(years=[1990, 2000, 2010, 2020], vals=[1.54, 1.36, 1.39, 1.34], label='A (WDI not on disk for JPN here)'),
}
# --- urban share paths: S from WDI SP.URB.TOTL.IN.ZS where on disk; KOR/JPN assumed
URB = {
    'PHL': dict(years=[1990, 2000, 2010, 2020], vals=[36.0, 39.14, 45.52, 54.11], label='S'),
    'KHM': dict(years=[1990, 2000, 2010, 2020], vals=[15.72, 18.62, 21.12, 39.83], label='S'),
    'HKG': dict(years=[1990, 2000, 2010, 2020], vals=[99.31, 100.0, 100.0, 100.0], label='S'),
    'CHN': dict(years=[1990, 2000, 2010, 2020], vals=[26.2, 36.43, 49.23, 63.52], label='S'),
    'KOR': dict(years=[1990, 2000, 2010, 2020], vals=[73.8, 79.6, 81.9, 81.4], label='A'),
    'JPN': dict(years=[1990, 2000, 2010, 2020], vals=[63.2, 65.2, 67.8, 69.9], label='A'),
}
# --- school-cycle lengths: S from WDI SE.PRM.DURS / SE.SEC.DURS where on disk, else national systems (A/E)
CYCLE = {
    'PHL': dict(primary=6, lower=4, upper=2, tertiary=4, label='S (WDI durations; K-12 from 2016)'),
    'KHM': dict(primary=6, lower=3, upper=3, tertiary=4, label='A (national system)'),
    'HKG': dict(primary=6, lower=3, upper=3, tertiary=4, label='A (national system)'),
    'CHN': dict(primary=6, lower=3, upper=3, tertiary=4, label='A (national system)'),
    'KOR': dict(primary=6, lower=3, upper=3, tertiary=4, label='A (national system)'),
    'JPN': dict(primary=6, lower=3, upper=3, tertiary=4, label='A (national system)'),
}
# --- mortality: simple survival schedule, A (no country life table on disk for this purpose)
SURVIVAL = dict(child=0.995, adult=0.994, old=0.96, label='A: constant age-band survival (declared approximation)')

# --- channel parameter ranges (F: to be fitted under brief 013; ranges are priors, NOT targets)
CHANNEL_PRIORS = {
    'e_s': dict(lo=0.0, hi=0.6, label='F: education->jobs elasticity (educated-labour share -> sector/formal growth)'),
    'e_d': dict(lo=0.0, hi=0.8, label='F: jobs->schooling elasticity (job opportunities -> intake/progression)'),
    'lag_s': dict(lo=1, hi=8, label='F: lag of the education->jobs channel (years)'),
    'lag_d': dict(lo=0, hi=5, label='F: lag of the jobs->schooling channel (years)'),
    'g0': dict(lo=0.0, hi=0.05, label='F: autonomous GDP growth'),
}
# --- exogenous world income growth: S/E from WDI GDP per capita (long-run average, declared)
WORLD_GROWTH = dict(val=0.02, label='E: WDI GDPpc long-run average, rounded')


def get(iso):
    return dict(tfr=TFR[iso], urb=URB[iso], cycle=CYCLE[iso], survival=SURVIVAL,
                channel_priors=CHANNEL_PRIORS, world_growth=WORLD_GROWTH, iso=iso)


COUNTRIES = ['PHL', 'KHM', 'HKG', 'CHN', 'KOR', 'JPN']
