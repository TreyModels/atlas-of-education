"""Country configurations for massabm (iteration 2).

Every parameter carries a label: sourced / estimated / fitted / assumed.
Structural mismatches are declared, not hidden:
  - massabm has a 10- or 12-year basic cycle only; KHM/HKG/CHN are approximated with a 10-year
    cycle (4-year secondary), so 6-3-3 and 3-3-4 cannot be represented exactly.
  - massabm's K-12 reform, CCT (4Ps), free-SUC tuition and overseas-registration architecture are
    Philippine/atlas-specific; they are switched OFF for KHM/HKG/CHN unless a source says otherwise.
"""
import copy, json
import numpy as np
from massabm import make_params
from massabm.params import DEFAULTS

FLAT0 = [(1900, 0.0), (2100, 0.0)]
FLAT1 = [(1900, 1.0), (2100, 1.0)]

COUNTRIES = {
    'PHL': dict(
        preset='philippines',
        overrides={},   # filled with the C3 fitted values at run time
        note='baseline institutions: K-12 2013, 4Ps, free SUC tuition, overseas registration architecture'),
    'KHM': dict(
        preset='philippines',
        overrides=dict(
            arch_path=FLAT0, cct_path=FLAT0, reform_rule='never',
            capacity_path=[(1945, .12), (1985, .18), (2009, .28), (2035, .5)],
            urban_path=[(1945, .12), (1980, .15), (2010, .21), (2035, .27)],
            need_share=0.45, rural_cost=0.05, shock_sigma=0.6, cost_col=0.7,
            y_sigma=0.9,
        ),
        note='no K-12 reform, no CCT, no overseas professional architecture; low capacity; higher child-labour need'),
    'HKG': dict(
        preset='korea',
        overrides=dict(
            arch_path=FLAT0, cct_path=FLAT0, reform_rule='never',
            urban_path=[(1945, 1.0), (2035, 1.0)],
            tuition_path=FLAT1,
            capacity_path=[(1945, .55), (1965, .8), (2035, .95)],
            cost_col=0.45, cost_shs=0.05,
            need_share=0.15, rural_cost=0.0,
            y_sigma=0.7,
        ),
        note='city-state: 100% urban, high capacity, no rural cost, no overseas professional channel, no CCT'),
    'CHN': dict(
        preset='korea',
        overrides=dict(
            arch_path=FLAT0, cct_path=FLAT0, reform_rule='never',
            urban_path=[(1945, .12), (1980, .19), (2000, .36), (2010, .50), (2035, .66)],
            capacity_path=[(1945, .25), (1980, .45), (2009, .7), (2035, .92)],
            apex_path=[(1945, .002), (2035, .02)],
            cost_col=0.45, cost_shs=0.04,
            need_share=0.25, rural_cost=0.04,
        ),
        note='high capacity, large formal sector, exam gates; no K-12 reform/CCT/overseas architecture; '
             'hukou and migration are NOT modelled (structural limitation)'),
}

# label + basis for every parameter we document explicitly; everything else defaults to 'assumed'
LABELS = {
    'N': ('assumed', 'cohort scale, no behavioural role'),
    't0': ('assumed', 'model start 1920 to allow 1980 initial stocks'),
    't1': ('assumed', 'horizon; 2040 set for the ledger extensions'),
    'y_sigma': ('estimated', 'lognormal income sd from WDI/APIS-type Gini ~0.4-0.5'),
    'growth': ('estimated', 'real index growth vs subsistence; WDI GDP per capita long-run'),
    'urban_path': ('sourced', 'WDI SP.URB.TOTL.IN.ZS urban share, interpolated 1945-2035'),
    'capacity_path': ('estimated', 'state schooling capacity inferred from observed GER trajectories'),
    'reform_year': ('sourced', 'PHL RA 10533 K-12 (2013); switched off elsewhere'),
    'cct_path': ('sourced', 'PHL 4Ps (2008+); switched off elsewhere'),
    'tuition_path': ('sourced', 'PHL RA 10931 free SUC tuition (2018)'),
    'arch_path': ('sourced', 'PHL/atlas overseas registration architecture (MRAs 2004-2016); off elsewhere'),
    'cost_col': ('fitted', 'fitted in C3/loop2 to observed GER; bounds 0.3-1.0'),
    'cost_shs': ('fitted', 'fitted in C3 to observed GER/completion'),
    'cost_pri': ('assumed', 'direct primary cost; low and stable'),
    'cost_jhs': ('assumed', 'direct lower-secondary cost'),
    'bar_basic': ('fitted', 'fitted in C3 to observed completion'),
    'bar_college': ('fitted', 'fitted in C3 to observed GER/transition'),
    'apex_path': ('fitted', 'apex seat scale fitted (apex_mult) in C3'),
    'hc_school': ('fitted', 'fitted in C3; near zero implies mostly signalling at the aggregate level'),
    'hc_ability': ('assumed', 'ability return inside the gray box'),
    'tut_cost': ('assumed', 'tutoring price per gate-year; no consistent cross-country price series in 04_data'),
    'tut_effect': ('assumed', 'tutoring score effect; literature cards feed this once TARGETS_SHADOW lands'),
    'borrow': ('assumed', 'annual borrowing capacity as share of income; no direct country series'),
    'shock_sigma': ('assumed', 'income shock sd'),
    'need_share': ('estimated', 'direct child-labour opportunity cost share; ILO/EDB employment context'),
    'rural_cost': ('assumed', 'extra post-primary rural cost'),
    'wage_base': ('estimated', 'sector wage relativities, informal = 1.0 (see LITERATURE_LEDGER)'),
    'wage_hc': ('estimated', 'within-sector schooling returns'),
    'vac_paths': ('estimated', 'sector vacancy paths inferred from employment shares (EDB/WDI)'),
    'referral_max': ('assumed', 'kin-referral reach; Philippine evidence suggests high'),
    'r_adjust_p': ('assumed', 'employer floor adjustment probability'),
    'belief_decay': ('assumed', 'memory of observed outcomes; E5 shows it is a structural lever'),
    'tau': ('assumed', 'logit noise in schooling choice'),
    'crra': ('assumed', 'risk preferences'),
    'disc': ('assumed', 'discount factor'),
}


def build(iso, fitted=None):
    c = COUNTRIES[iso]
    ov = copy.deepcopy(c['overrides'])
    if fitted:
        ov.update(fitted)
    p = make_params(preset=c['preset'], **ov)
    return p


def config_table(iso, fitted=None):
    p = build(iso, fitted)
    rows = []
    for k, v in p.items():
        if isinstance(v, dict) or isinstance(v, (list, tuple)):
            val = json.dumps(v)[:70]
        else:
            val = v
        lab, basis = LABELS.get(k, ('assumed', 'not documented individually: judgement/placeholder, no direct evidence'))
        rows.append(dict(parameter=k, value=val, label=lab, basis=basis))
    return rows


def write_markdown(path, fitted_by_country):
    lines = ['# Country configurations — every parameter labelled', '',
             'Labels: **sourced** (observed data / named source) · **estimated** (derived from a named series by a stated rule) ·',
             '**fitted** (calibrated in this package) · **assumed** (judgement, no direct evidence).', '',
             'Structural limitations (declared): massabm has a 10- or 12-year basic cycle only, so KHM/HKG/CHN are',
             'approximated with a 10-year cycle (4-year secondary); 6-3-3 and 3-3-4 cannot be represented exactly.',
             'PHL keeps its K-12/CCT/free-tuition/overseas architecture; KHM/HKG/CHN switch those off.',
             'hukou/migration (CHN) and HKG 3-3-4 are NOT modelled.', '',
             '## Source series used (from 04_data, observed cells only)', '',
             '| series | use |', '|---|---|',
             '| gmr_observed_6countries_1970_2024.csv | GER by level (fit targets C3/loop2) |',
             '| uis_sdg4_4countries_long.csv | completion (fit targets) |',
             '| wdi_4countries_long.csv SP.URB.TOTL.IN.ZS | urban_path (sourced) |',
             '| wdi_4countries_long.csv SE.PRM.DURS / SE.SEC.DURS | structural note on cycle length |',
             '| wdi_4countries_long.csv BX.TRF.PWKR.DT.GD.ZS | PH overseas-channel context (not wired) |', '']
    for iso in ['PHL', 'KHM', 'HKG', 'CHN']:
        lines += [f'## {iso}', '', COUNTRIES[iso]['note'], '',
                  '| parameter | value | label | basis |', '|---|---|---|---|']
        for r in config_table(iso, (fitted_by_country or {}).get(iso)):
            lines.append(f'| `{r["parameter"]}` | {r["value"]} | **{r["label"]}** | {r["basis"]} |')
        lines.append('')
    open(path, 'w').write('\n'.join(lines) + '\n')
    print('wrote', path)
