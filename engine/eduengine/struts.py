"""The strut registry. A strut is a rule or constant that exists to make the engine run or match history, not a
mechanism we believe. Every strut is declared here with what it stands in for, what it is tuned to, and how it
would be removed. See papers/STRUTS_WHITEPAPER.md.

strut_test() varies each strut and reports which patterns move: a strut whose variation moves nothing is harmless
scaffolding; one that moves a headline pattern is load-bearing and is a priority for replacement.
"""
import numpy as np

STRUTS = [
    dict(id='S0', name='Completion wedge (anchored enrolment)', params=['enrol_targets', 'anchor_stop'], vary=dict(anchored=(False, True)),
         stands_in_for='Everything about how many children continue that the causal variables do not explain',
         tuned_to='UIS completion series, by construction: quantity comes from the data, selection from the mechanism. The '
                  'implied wedge (the value the marginal stayer needed) is reported every year; in the policy lab it is frozen '
                  'at its recent mean from the policy year on',
         removal='Shrink it: better household, supply and labour mechanisms reduce the wedge needed; report its size every run', kind='wedge'),
    dict(id='S1', name='Formal vacancies follow a set path', params=['vac0', 'vac_growth'], vary=dict(vac_growth=(0.0, 0.02)),
         stands_in_for='Labour demand: firms, sectors, growth, the state as employer',
         tuned_to='Rough formal-employment shares', removal='A labour-demand module tied to growth and sector structure '
         '(cf. IFs, MAMS) or vacancies estimated from labour-force surveys', kind='missing sector'),
    dict(id='S2', name='Weight on the child\'s future income (kappa)', params=['kappa'], vary=dict(kappa=(8.0, 16.0)),
         stands_in_for='Altruism, discounting, aspirations', tuned_to='Overall completion levels',
         removal='Estimate from perceived-returns data (Jensen 2010) and enrolment responses to price changes', kind='behavioural constant'),
    dict(id='S3', name='Belief floor for credentials nobody holds yet', params=['belief_floor'], vary=dict(belief_floor=(False, True)),
         stands_in_for='How families learn about jobs they have never seen', tuned_to='Nothing: it prevents a cold-start trap',
         removal='An information module (job ads, migrant networks, school messaging), testable against information experiments', kind='stability'),
    dict(id='S4', name='Poverty line below which a household needs a child\'s earnings (luxury axiom)', params=['poverty_line', 'need_max'],
         vary=dict(poverty_line=(0.6, 1.4)),
         stands_in_for='Child labour and household production (Basu & Van 1998; Edmonds 2007)', tuned_to='Dropout of poorer children',
         removal='Estimate poverty_line and need_max from child-labour rates by household income (DHS/MICS/LFS); '
                 'v0.3 replaced the flat constant need_share with this income-dependent rule', kind='behavioural constant'),
    dict(id='S10', name='Promotion bar (repetition when learning lags the grade)', params=['promote_bar'], vary=dict(promote_bar=(0.3, 0.7)),
         stands_in_for='Teachers\' promotion decisions and repetition policy', tuned_to='Over-age enrolment',
         removal='Promotion rules by country and era from EMIS repetition rates', kind='behavioural rule'),
    dict(id='S5', name='Withholding as a rule h = h_max x gap x (1 - monitoring)', params=['h_max'], vary=dict(h_max=(0.2, 0.6)),
         stands_in_for='Teachers choosing effort against tutoring income', tuned_to='Own-teacher tutoring level',
         removal='Teachers as agents choosing withholding with detection risk and pupil loss (Jayachandran 2014)', kind='behavioural rule'),
    dict(id='S6', name='Employer floor rule (raise at 4x applicants)', params=['screen_kappa'], vary=dict(screen_kappa=(2.5, 6.0)),
         stands_in_for='Employers minimising screening cost', tuned_to='Credential inflation pace',
         removal='Employers choosing screening technology by cost (as in the three-actor model)', kind='behavioural rule'),
    dict(id='S7', name='Graduate-queue family-support cutoff', params=['queue_support'], vary=dict(queue_support=(0.8, 1.6)),
         stands_in_for='Family transfers and reservation wages', tuned_to='Graduate unemployment',
         removal='A search model with household transfers, fitted to youth unemployment by family income', kind='behavioural constant'),
    dict(id='S8', name='Kin-network absorption of young urban leavers', params=['kin_support'], vary=dict(kin_support=(0.5, 0.9)),
         stands_in_for='Trust networks thinning with urbanization (Tilly)', tuned_to='Nothing yet (no street-child data)',
         removal='Kin support as a function of migration and urban tenure, from household panel data', kind='missing mechanism'),
    dict(id='S9', name='Proficiency and literacy thresholds on the learning scale', params=['mpl_primary'], vary=dict(mpl_primary=(3.5, 5.5)),
         stands_in_for='The link from the engine\'s learning scale to SEA-PLM / PASEC / PISA', tuned_to='Assumed',
         removal='Anchor the scale to learning profiles (Kaffenberger & Pritchett 2021) and harmonised scores', kind='measurement anchor'),
    dict(id='S11', name='Tutoring-industry employment rule', params=['tutor_labour_share', 'tutor_turnover'],
         vary=dict(tutor_labour_share=(0.3, 0.9)),
         stands_in_for='How many graduates the commercial tutoring industry employs, and how fast it turns them over',
         tuned_to='Nothing directly; it moves China\'s youth unemployment after Double Reduction',
         removal='Tutoring-firm payrolls and tutor tenure from industry filings (e.g. listed firms\' annual reports) and labour-force surveys',
         kind='behavioural rule'),
]


def strut_test(make, patterns, seeds=(0,), struts=STRUTS):
    """make(**over) -> engine; patterns: {name: fn(engine, summary) -> float}. Returns rows of pattern shifts."""
    base = []
    for s in seeds:
        E = make(seed=s); o = E.run(); base.append({k: f(E, o) for k, f in patterns.items()})
    b = {k: float(np.nanmean([x[k] for x in base])) for k in patterns}
    rows = []
    for st in struts:
        (prm, (lo, hi)), = st['vary'].items()
        res = {}
        for v in (lo, hi):
            vals = []
            for s in seeds:
                E = make(seed=s, **{prm: v}); o = E.run(); vals.append({k: f(E, o) for k, f in patterns.items()})
            res[v] = {k: float(np.nanmean([x[k] for x in vals])) for k in patterns}
        swing = {k: abs(res[hi][k] - res[lo][k]) for k in patterns}
        rows.append(dict(id=st['id'], name=st['name'], param=prm, lo=lo, hi=hi, base=b, low=res[lo], high=res[hi], swing=swing,
                         load_bearing=[k for k, v in swing.items() if v > 0.05]))
    return rows
