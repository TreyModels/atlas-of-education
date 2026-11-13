"""Load the packaged public cross-country data as ProvenancePanels.

The files live in `analysis/public_data/data/`, downloaded from the Our World in Data archive
copies of the underlying releases (Penn World Table 10.0, Barro-Lee / Lee-Lee attainment,
Altinok-Angrist-Patrinos education quality, ILOSTAT unemployment by education, UN series).
Rows read from these documented release files are flagged 'v' (verified against the named file);
a cell absent from the file is '' (missing).  Loaders return a fresh copy, so callers can mutate.

Notes on the year grids, which matter for gap lengths:

  * PWT is annual 1950-2019 for ~213 entities (114 with at least 55 annual observations in
    1960-2019).  Use load_pwt(...) and subset to a complete window for the hold-out.
  * The Lee-Lee / Barro-Lee / UNDP years-of-schooling file is 5-yearly to 1990 and annual
    1991-2017.  load_attainment(year_min=1991) gives the annual adult-attainment panel used for
    the annual hold-out; load_barro_lee() gives the original 13-wave 1950-2010 Barro-Lee table.
  * ILOSTAT unemployment by education is a sparse survey panel (survey years only, 1990-2017);
    use it for bounded-rate behaviour, not for contiguous-gap scoring.

If pandas is unavailable the module raises a clear ImportError at call time; the core imputation
code is numpy/scipy only.
"""
import functools
from pathlib import Path

import numpy as np

from .panel import ProvenancePanel

DATA_DIR = Path(__file__).resolve().parents[2] / 'analysis' / 'public_data' / 'data'
DATA_FLAG = 'v'

PWT_FILE = 'Penn World Table version 10.0.csv'
ATTAINMENT_FILE = 'Years of Schooling - based on Lee-Lee (2016), Barro-Lee (2018) and UNDP (2018).csv'
BARRO_LEE_FILE = 'Educational Attainment - Barro Lee Education Dataset (2010) .csv'
ILOSTAT_FILE = 'Unemployment rate, ages 25-54, by education - ILOSTAT (2017).csv'
QUALITY_FILE = 'Global Data Set on Education Quality (1965-2015) - Altinok, Angrist, and Patrinos (2018).csv'

PWT_FIELDS = {
    'gdp_pc': 'GDP per capita (output, multiple price benchmarks)',
    'gdp_pc_exp': 'GDP per capita (expenditure, multiple price benchmarks)',
    'gdp': 'GDP (output, multiple price benchmarks)',
    'population': 'Population',
    'productivity': 'Productivity: output per hour worked',
    'labour_share': 'Share of labour compensation in GDP',
}

ILOSTAT_FIELDS = {
    'all': 'Unemployment rate, ages 25-54,  all levels of education',
    'advanced': 'Unemployment rate, ages 25-54,  advanced education',
    'basic': 'Unemployment rate, ages 25-54,  basic education',
    'intermediate': 'Unemployment rate, ages 25-54,  intermediate education',
    'less_than_basic': 'Unemployment rate, ages 25-54,  less than basic education',
}


def data_available():
    """True if the packaged data directory is present."""
    return DATA_DIR.is_dir()


def _read_csv(filename, usecols=None):
    try:
        import pandas as pd
    except ImportError as ex:                              # pragma: no cover - pandas is a project dep
        raise ImportError('engine.impute.data needs pandas to read the packaged CSVs') from ex
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f'packaged public data not found: {path}')
    return pd.read_csv(path, usecols=usecols)


def _panel_from_long(df, value_column, name, flag=DATA_FLAG, year_min=None, year_max=None):
    """Pivot an OWID-style long frame (Entity, Year, value column) into a ProvenancePanel."""
    import pandas as pd
    if value_column not in df.columns:
        raise KeyError(f'column {value_column!r} not in {list(df.columns)}')
    d = df[['Entity', 'Year', value_column]].copy()
    d['Entity'] = d['Entity'].astype(str)
    d['Year'] = d['Year'].astype(float)
    if year_min is not None:
        d = d[d.Year >= float(year_min)]
    if year_max is not None:
        d = d[d.Year <= float(year_max)]
    d = d.dropna(subset=[value_column])
    if d.empty:
        raise ValueError(f'{name}: no observations in the requested window')
    if d.duplicated(['Entity', 'Year']).any():
        raise ValueError(f'{name}: duplicate (Entity, Year) rows')
    entities = sorted(d.Entity.unique())
    # keep the complete year grid of the requested window, not just years that survived dropna,
    # so that a country with a missing year gets a proper empty cell
    all_years = df['Year'].astype(float)
    lo = float(year_min) if year_min is not None else float(d.Year.min())
    hi = float(year_max) if year_max is not None else float(d.Year.max())
    year_values = sorted(all_years[(all_years >= lo) & (all_years <= hi)].unique())
    if not year_values:
        year_values = sorted(d.Year.unique())
    years = np.asarray(year_values, dtype=float)
    values = np.full((len(entities), len(years)), np.nan)
    flags = np.full((len(entities), len(years)), '', dtype='<U1')
    ei = {e: i for i, e in enumerate(entities)}
    yi = {y: j for j, y in enumerate(years)}
    for e, y, v in d[['Entity', 'Year', value_column]].itertuples(index=False):
        j = yi.get(float(y))
        if j is None:
            continue
        values[ei[e], j] = float(v)
        flags[ei[e], j] = flag
    return ProvenancePanel(entities, years, values, flags, name=name)


# ---------------------------------------------------------------- Penn World Table
@functools.lru_cache(maxsize=None)
def _pwt_cached(field, year_min, year_max):
    col = PWT_FIELDS[field]
    df = _read_csv(PWT_FILE, usecols=['Entity', 'Year', col])
    return _panel_from_long(df, col, name=f'Penn World Table 10.0: {col}',
                            year_min=year_min, year_max=year_max)


def load_pwt(field='gdp_pc', year_min=None, year_max=None):
    """Panel of a PWT 10.0 series (annual).  field: see PWT_FIELDS."""
    if field not in PWT_FIELDS:
        raise KeyError(f'unknown PWT field {field!r}; known: {sorted(PWT_FIELDS)}')
    return _pwt_cached(field, year_min, year_max).copy()


# ---------------------------------------------------------------- attainment
@functools.lru_cache(maxsize=None)
def _attainment_cached(year_min, year_max):
    df = _read_csv(ATTAINMENT_FILE)
    df.columns = ['Entity', 'Year', 'value']
    return _panel_from_long(df, 'value', name='Mean years of schooling (Lee-Lee 2016 / Barro-Lee 2018 / UNDP 2018)',
                            year_min=year_min, year_max=year_max)


def load_attainment(year_min=None, year_max=None):
    """Adult mean years of schooling (annual 1991-2017; 5-yearly before 1991)."""
    return _attainment_cached(year_min, year_max).copy()


@functools.lru_cache(maxsize=None)
def _barro_lee_cached():
    df = _read_csv(BARRO_LEE_FILE)
    df.columns = ['Entity', 'Year', 'value']
    return _panel_from_long(df, 'value', name='Barro-Lee 2010: average years of total education (5-year waves)')


def load_barro_lee():
    """The original Barro-Lee 2010 table: 146 countries x 13 five-year waves, 1950-2010."""
    return _barro_lee_cached().copy()


# ---------------------------------------------------------------- ILOSTAT (bounded rates)
@functools.lru_cache(maxsize=None)
def _ilostat_cached(field):
    col = ILOSTAT_FIELDS[field]
    df = _read_csv(ILOSTAT_FILE)
    return _panel_from_long(df, col, name=f'ILOSTAT: {col} (survey years)')


def load_ilostat(field='all'):
    """Unemployment rate 25-54 by education, a bounded percentage in [0, 100]."""
    if field not in ILOSTAT_FIELDS:
        raise KeyError(f'unknown ILOSTAT field {field!r}; known: {sorted(ILOSTAT_FIELDS)}')
    return _ilostat_cached(field).copy()


# ---------------------------------------------------------------- education quality (bounded scores)
@functools.lru_cache(maxsize=None)
def _quality_cached():
    df = _read_csv(QUALITY_FILE)
    df = df.iloc[:, :4]
    df.columns = ['Entity', 'Year', 'hlo', 'min_share']
    return _panel_from_long(df, 'hlo', name='Harmonised learning outcome score (Altinok, Angrist, Patrinos 2018)')


def load_learning_scores():
    """Average harmonised learning outcome score, 5-year points 1965-2015 (bounded ~100-700)."""
    return _quality_cached().copy()


# ---------------------------------------------------------------- World Bank WDI (downloaded, to-do item B4)
# analysis/public_data/data/wdi/<code>.csv, tidy long format (country_iso3, country, year, value), 1990-2025.
WDI_DIR = 'wdi'
UIS_FILE = 'uis/uis_sdg4_national.csv'          # curated UNESCO UIS SDG-4 national extract (B4)

WDI_FIELDS = {
    'completion_lower': 'SE.SEC.CMPT.LO.ZS',     # lower-secondary completion, % of relevant age group (bounded)
    'tertiary_enrolment': 'SE.TER.ENRR',         # gross tertiary enrolment, % (can exceed 100)
    'wage_share': 'SL.EMP.WORK.ZS',              # wage and salaried workers, % of employment (bounded)
    'youth_unemployment': 'SL.UEM.1524.ZS',      # youth unemployment, % (bounded)
    'education_spending': 'SE.XPD.TOTL.GD.ZS',   # government education spending, % of GDP
}

# UIS indicator IDs (the curated extract keeps 50 SDG-4 indicators; these are the base "both sexes" series).
UIS_FIELDS = {
    'completion_lower': 'CR.2',                  # lower-secondary completion rate, both sexes (%)
    'completion_primary': 'CR.1',
    'completion_upper': 'CR.3',
    'out_of_school_lower': 'ROFST.MOD.2',        # out-of-school rate, lower-secondary age, both sexes (%)
    'out_of_school_primary': 'ROFST.MOD.1',
    'tertiary_enrolment': 'GER.5T8',             # gross tertiary enrolment ratio, both sexes (%)
    'spending_gdp': 'XGDP.FSGOV',                # government education spending, % of GDP
}


@functools.lru_cache(maxsize=None)
def _wdi_cached(code, year_min, year_max):
    df = _read_csv(f'{WDI_DIR}/{code}.csv')
    df = df.rename(columns={'country': 'Entity', 'year': 'Year'})
    return _panel_from_long(df, 'value', name=f'World Bank WDI: {code}',
                            year_min=year_min, year_max=year_max)


def load_wdi(field='completion_lower', year_min=None, year_max=None):
    """Panel of a downloaded World Bank WDI series (annual).  field: see WDI_FIELDS."""
    if field not in WDI_FIELDS:
        raise KeyError(f'unknown WDI field {field!r}; known: {sorted(WDI_FIELDS)}')
    return _wdi_cached(WDI_FIELDS[field], year_min, year_max).copy()


@functools.lru_cache(maxsize=None)
def _uis_cached(indicator, year_min, year_max):
    df = _read_csv(UIS_FILE)
    df = df[df.INDICATOR_ID == indicator].rename(columns={'COUNTRY_ID': 'Entity', 'YEAR': 'Year'})
    if df.empty:
        raise ValueError(f'UIS indicator {indicator!r} is not in the curated extract')
    return _panel_from_long(df, 'VALUE', name=f'UNESCO UIS: {indicator}',
                            year_min=year_min, year_max=year_max)


def load_uis(field='completion_lower', year_min=None, year_max=None):
    """Panel of a UNESCO UIS SDG-4 series (annual, national, both sexes).  field: see UIS_FIELDS."""
    if field not in UIS_FIELDS:
        raise KeyError(f'unknown UIS field {field!r}; known: {sorted(UIS_FIELDS)}')
    return _uis_cached(UIS_FIELDS[field], year_min, year_max).copy()


# ---------------------------------------------------------------- helpers for the harness
def near_complete(pwt, min_obs=55):
    """Boolean entity mask for PWT entities with at least min_obs observed years.

    Useful to cut the ragged PWT panel down to countries whose series are long enough to hold out
    10-year gaps with anchors on both sides.
    """
    return pwt.observed().sum(axis=1) >= int(min_obs)


def log_panel(panel):
    """Log the panel's values, keeping provenance flags (for log-scale hold-outs)."""
    return panel.map(np.log, name=panel.name + ' [log]')
