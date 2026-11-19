"""Trial designs for the rigor families, consumed by research/lab.py:make_tasks.

`--draws` sets the number of nuisance draws or chunks per cell, `--replicates` the seed repetitions where they apply.
Budgets for a first substantive run are in research/rigor/README.md. Every structural cell shares the same draw and
seed indices (lab.py omits cell labels from seeds), so contrasts between structures are paired.
"""

PLACEBO_DATES = [None] + [(y, m) for y in range(2019, 2025) for m in (1, 4, 7, 10)] + [(2021, 8)]
ROLLING_ORIGINS = [(2020, 6), (2020, 12), (2021, 6), (2021, 12), (2022, 6), (2022, 12)]


def rigor_tasks(family, smoke, nd, nr):
    if family == 'credential_recovery':
        for structure in ('M_HC', 'M_POS', 'M_REL', 'M_GATE'):
            for liquidity in ('graded', 'hard'):
                for d in range(nd):
                    yield (f'{structure}/{liquidity}', d, 0,
                           dict(structure=structure, liquidity=liquidity, batch=3 if smoke else 250,
                                n=300 if smoke else 1500))
    elif family == 'shadow_recovery':
        for variant in ('thin', 'diversion', 'favour', 'full'):
            for d in range(nd):
                yield (variant, d, 0, dict(variant=variant, batch=2 if smoke else 40, max_sweeps=100))
    elif family == 'youth_placebo':
        dates = PLACEBO_DATES[:3] + PLACEBO_DATES[-1:] if smoke else PLACEBO_DATES
        for date in dates:
            for d in range(1 if smoke else nd):
                yield (f'date{date}', d, 0, dict(date=date, window='full', max_nfev=3 if smoke else 300))
    elif family == 'youth_rolling':
        for origin in (ROLLING_ORIGINS[2:4] if smoke else ROLLING_ORIGINS):
            for d in range(1 if smoke else nd):
                yield (f'origin{origin}', d, 0, dict(origin=origin, max_nfev=3 if smoke else 300))
    elif family == 'fertility_placebo':
        for start in (1961, 1964):
            yield (f'start{start}', 0, 0, dict(start=start, n_sim=50 if smoke else 2000))
    elif family == 'camchild_validation':
        for target in (None, 0.55, 0.65, 0.75):
            for d in range(nd):
                for r in range(nr):
                    yield (f'baseline{target}', d, r,
                           dict(targetBaseline=target, amountsUSD=[45, 60], wageRangeUSD=[350, 700],
                                n=600 if smoke else 6000))
    else:
        raise ValueError(family)
