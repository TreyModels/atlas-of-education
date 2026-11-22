"""Country data loading. Every series used by the model comes from countries/<ISO3>/wdi_series.json
(World Bank WDI, sourced) or countries/<ISO3>/config.json (dated policy facts, declared costs, other targets)."""
import json
import math
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Series:
    """A yearly series with linear interpolation and flat extrapolation (or log-linear back-extrapolation
    for population-type series when `back_growth` is given)."""

    def __init__(self, points, back_growth=None):
        pts = sorted((int(k), float(v)) for k, v in points.items() if not str(k).startswith('_') and v is not None)
        if not pts:
            raise ValueError('empty series')
        self.years = np.array([p[0] for p in pts], float)
        self.values = np.array([p[1] for p in pts], float)
        self.back_growth = back_growth

    def __call__(self, year):
        y0 = self.years[0]
        if year < y0 and self.back_growth is not None:
            return self.values[0] * (1 + self.back_growth) ** (year - y0)
        return float(np.interp(year, self.years, self.values))

    def observed(self, lo=-math.inf, hi=math.inf):
        m = (self.years >= lo) & (self.years <= hi)
        return dict(zip(self.years[m].astype(int).tolist(), self.values[m].tolist()))


class Country:
    def __init__(self, iso3):
        base = os.path.join(ROOT, 'countries', iso3)
        self.iso3 = iso3
        self.config = json.load(open(os.path.join(base, 'config.json')))
        self.wdi_raw = json.load(open(os.path.join(base, 'wdi_series.json')))
        w = self.wdi_raw
        # declared data repairs (e.g. series breaks): drop observations before a year, hold the first kept value
        for code, rule in self.config.get('wdi_repairs', {}).items():
            if code.startswith('_'):
                continue
            w[code] = {k: v for k, v in w[code].items() if k.startswith('_') or int(k) >= rule['drop_before']}
        g = self.config.get('demography', {}).get('pre_data_pop_growth', 0.03)
        self.gdppc = Series(w['NY.GDP.PCAP.KD'])
        self.pop = Series(w['SP.POP.TOTL'], back_growth=g)
        self.cbr = Series(w['SP.DYN.CBRT.IN'])
        u5 = w.get('SH.DYN.MORT')
        if u5:
            self.u5mr = Series(u5)
        else:
            u5_def = self.config.get('demography', {}).get('u5mr_default', 3.0)
            self.u5mr = Series({1950: u5_def, 2025: u5_def})
        gini = w.get('SI.POV.GINI')
        self.gini = Series(gini) if gini else None
        # v5: extra WDI series gathered by the data agents (sources/*.json 'worldbank' blocks) and driver series
        import glob
        for f in sorted(glob.glob(os.path.join(base, 'sources', '*.json'))):
            try:
                blk = json.load(open(f)).get('worldbank', {})
            except Exception:
                continue
            for code, pts in blk.items():
                if not code.startswith('_') and isinstance(pts, dict) and code not in w:
                    clean = {k: v for k, v in pts.items() if not str(k).startswith('_') and isinstance(v, (int, float))}
                    if code == 'SE.XPD.TOTL.GB.ZS':
                        clean = {k: v for k, v in clean.items() if v > 0}     # zeros are artefacts (agent note)
                    if clean:
                        w[code] = clean
        self.drivers = {}
        dpath = os.path.join(base, 'drivers_v5.json')
        if os.path.exists(dpath):
            for name, spec in json.load(open(dpath)).get('series', {}).items():
                pts = {k: v for k, v in spec.get('points', {}).items() if isinstance(v, (int, float))}
                if pts:
                    self.drivers[name] = Series(pts)

    def wdi(self, code):
        return Series(self.wdi_raw[code]) if code in self.wdi_raw else None

    def births(self, year):
        """Births in calendar year = crude birth rate x population (WDI). Before the first WDI year the
        population is back-extrapolated at the declared pre-data growth rate and the earliest CBR is held."""
        return self.cbr(year) / 1000.0 * self.pop(year)

    def survivors(self, birth_year):
        """Members of a birth cohort alive at school age: births x (1 - under-five mortality at birth year).
        Mortality between ages 5 and 29 and net migration are ignored (declared)."""
        return self.births(birth_year) * (1 - self.u5mr(birth_year) / 1000.0)


def decile_income_multipliers(gini):
    """Mean income of each decile relative to the national mean, assuming a lognormal distribution with the
    given Gini (0-1). sigma = sqrt(2) * Phi^-1((G+1)/2). Decile means computed by numerical integration."""
    from scipy.stats import norm
    sigma = math.sqrt(2) * norm.ppf((gini + 1) / 2)
    out = []
    for d in range(10):
        lo, hi = d / 10, (d + 1) / 10
        # share of total income held by the decile of a lognormal = Phi(z_hi - sigma) - Phi(z_lo - sigma)
        zl = norm.ppf(lo) if lo > 0 else -np.inf
        zh = norm.ppf(hi) if hi < 1 else np.inf
        share = norm.cdf(zh - sigma) - norm.cdf(zl - sigma)
        out.append(share * 10)
    return np.array(out)
