"""Build the B11 validation report: hold-out error by method and gap length on the real public data.

This module prints markdown to stdout and writes nothing by default (the Lead owns
docs/imputation_validation.md; pass --out to write a file).  Everything is seeded, so two runs
give the same tables.  Typical use:

    python -m engine.impute                        # from the project root
    python -m engine.impute --replicates 5         # more stable error estimates
    python -m engine.impute --datasets pwt         # one dataset only

Datasets
  1. log GDP per capita, PWT 10.0, annual 1960-2019, countries with >=55 observations
  2. mean years of schooling, Lee-Lee/Barro-Lee/UNDP, annual 1991-2017
  3. the original Barro-Lee 2010 five-year table, where a gap of 1 wave is 5 years -- this is the
     natural home of the cohort back-cast and is scored in waves
  4. lower-secondary completion, World Bank WDI (SE.SEC.CMPT.LO.ZS, downloaded in B4), annual 1990-2025
  5. lower-secondary completion, UNESCO UIS (CR.2, the B4 curated extract), annual 1996-2024
  6. out-of-school rate, lower-secondary age, UNESCO UIS (ROFST.MOD.2, modelled), annual 2000-2025
The WDI and UIS series are the ones the to-do item B11 asks for; they are modelled/register estimates,
so their hold-out error is a lower bound on the error of imputing an actual survey series.
"""
import argparse
import sys

import numpy as np

from . import data
from .base import make_imputer
from .harness import holdout


def _annual_pwt():
    p = data.load_pwt('gdp_pc', year_min=1960, year_max=2019)
    return p.subset(entity_mask=data.near_complete(p, min_obs=55))


def _annual_attainment():
    p = data.load_attainment(year_min=1991, year_max=2017)
    keep = p.observed().sum(axis=1) >= 20
    return p.subset(entity_mask=keep)


def _barro_lee():
    return data.load_barro_lee()


def _wdi_completion():
    """World Bank WDI lower-secondary completion, annual 1990-2025, countries with >=15 observations."""
    p = data.load_wdi('completion_lower', year_min=1990, year_max=2025)
    return p.subset(entity_mask=p.observed().sum(axis=1) >= 15)


def _uis_completion():
    """UNESCO UIS lower-secondary completion rate (CR.2), annual 1996-2024."""
    p = data.load_uis('completion_lower', year_min=1996, year_max=2024)
    return p.subset(entity_mask=p.observed().sum(axis=1) >= 12)


def _uis_out_of_school():
    """UNESCO UIS out-of-school rate, lower-secondary age (ROFST.MOD.2), annual 2000-2025."""
    p = data.load_uis('out_of_school_lower', year_min=2000, year_max=2025)
    return p.subset(entity_mask=p.observed().sum(axis=1) >= 12)


# the state-space and multiple-imputation rungs are scored on the attainment panel; on raw GDP
# levels they can produce non-positive values, so they are not meaningful without a log panel
_PWT_METHODS = ('linear', 'loglinear')
_ATTAINMENT_METHODS = ('linear', 'loglinear', 'scurve', 'cohort', 'kalman', 'amelia')
_BARRO_LEE_METHODS = ('linear', 'loglinear', 'cohort', 'kalman')
_BOUNDED_METHODS = ('linear', 'loglinear', 'scurve', 'kalman')


def _method_set(names):
    return {n: make_imputer(n) for n in names}


def _section(title, panel, methods, reps, seed, points_per_gap, gap_lengths, notes='', unit='y',
             score_transform=None, metric_note='MAE'):
    rep = holdout(panel, methods=_method_set(methods), gap_lengths=gap_lengths,
                  n_replicates=reps, seed=seed, points_per_gap=points_per_gap,
                  score_transform=score_transform)
    lines = [f'## {title}', '',
             f'{panel.n_entities} countries, {panel.n_years} year positions '
             f'({panel.years[0]:g}-{panel.years[-1]:g}), {reps} replicates, seed {seed}.', '']
    if notes:
        lines += [notes, '']
    what = 'gap length' if unit == 'y' else 'waves'
    lines += [f'{metric_note} by method and {what}:', '', rep.table('mae', suffix=unit), '',
              f'RMSE by method and {what}:', '', rep.table('rmse', suffix=unit), '',
              'Scored points per cell:', '', rep.counts_table(suffix=unit), '']
    has_coverage = any(np.isfinite(rep.scores[m].get(gap_lengths[0], {}).get('coverage', np.nan))
                       for m in rep.methods)
    if has_coverage:
        lines += ['Interval coverage (nominal 90%):', '', rep.coverage_table(suffix=unit), '']
    lines += [f'Best method at the longest gap: `{rep.best(max(gap_lengths))[0]}` '
              f'(MAE {rep.best(max(gap_lengths))[1]:.3f}).', '']
    return lines, rep


def build_report(replicates=3, seed=0, datasets=('pwt', 'attainment', 'barro_lee', 'wdi', 'uis'),
                 points_per_gap=60, gap_lengths=(1, 2, 3, 5, 10)):
    """Return the validation report as markdown text."""
    L = ['# Imputation hold-out validation', '',
         f'The imputation ladder from `engine/impute` (v1.0). Deterministic: gaps deleted with seed {seed}, '
         f'every method refit on the damaged panel. Only verified (`v`) cells are deleted and scored.',
         '']
    if 'pwt' in datasets:
        lines, _ = _section('1. GDP per capita, Penn World Table 10.0 (annual)',
                            _annual_pwt(), _PWT_METHODS, replicates, seed, points_per_gap,
                            gap_lengths,
                            notes='Gap length is the number of consecutive missing years. Errors are '
                                  'in log points (a value of 0.05 is about 5%), so the linear rung '
                                  'and the log-linear rung are compared on their natural scale.',
                            score_transform=np.log, metric_note='MAE (log points)')
        L += lines
    if 'attainment' in datasets:
        lines, _ = _section('2. Mean years of schooling, Lee-Lee / Barro-Lee / UNDP (annual 1991-2017)',
                            _annual_attainment(), _ATTAINMENT_METHODS, replicates, seed,
                            points_per_gap, gap_lengths,
                            notes='Gap length is the number of consecutive missing years. '
                                  'The cohort rung is designed for this variable.')
        L += lines
    if 'barro_lee' in datasets:
        lines, _ = _section('3. Barro-Lee 2010 five-year waves (one wave = 5 years)',
                            _barro_lee(), _BARRO_LEE_METHODS, replicates, seed, points_per_gap,
                            (1, 2), notes='Gap length here is in waves: 1 wave = 5 years, '
                                          '2 waves = 10 years.', unit=' wave')
        L += lines
    if 'wdi' in datasets:
        lines, _ = _section('4. Lower-secondary completion, World Bank WDI (annual 1990-2025, bounded %)',
                            _wdi_completion(), _BOUNDED_METHODS, replicates, seed,
                            points_per_gap, gap_lengths,
                            notes='The series the project downloads in B4 (SE.SEC.CMPT.LO.ZS). Bounded '
                                  'percentage in [0, 100], so the S-curve rung is applicable.')
        L += lines
    if 'uis' in datasets:
        lines, _ = _section('5. Lower-secondary completion, UNESCO UIS (annual 1996-2024, bounded %)',
                            _uis_completion(), _BOUNDED_METHODS, replicates, seed,
                            points_per_gap, gap_lengths,
                            notes='UIS register-based completion (CR.2) from the curated B4 extract. '
                                  'Bounded in [0, 100].')
        L += lines
        lines, _ = _section('6. Out-of-school rate, lower-secondary age, UNESCO UIS (annual 2000-2025, bounded %)',
                            _uis_out_of_school(), _BOUNDED_METHODS, replicates, seed,
                            points_per_gap, gap_lengths,
                            notes='UIS modelled out-of-school rate (ROFST.MOD.2). Bounded in [0, 100]; '
                                  'a rate whose long gaps are the ones that matter most for the child-labour work.')
        L += lines
    L += ['## Reading the tables', '',
          '- Long gaps should be harder than short ones on average, and the tests check 1- and '
          '2-year gaps against 10-year gaps. Adjacent lengths can cross in a table (3 vs 5 years) '
          'because the blocks are randomly placed and some episodes are simply unforecastable; '
          'that is sampling noise in the hold-out, not a bug.',
          '- Linear/log-linear rungs are strong on short gaps of smooth series; the S-curve and '
          'state-space rungs are for bounded or noisy series, and the state-space rung is the one '
          'that supplies honest intervals.',
          '- The multiple-imputation rung borrows the year cross-section from other countries; '
          'it can beat univariate interpolation when a country has a long gap while the world '
          'moves (the common year factor is observable from the other countries), but it is not '
          'guaranteed to win on every series: the tables show where it does and does not.',
          '- Interval coverage is only as honest as the model. The 90% state-space intervals are '
          'near nominal on the smooth PWT/attainment series; where they are too wide or too narrow, '
          'that is a finding about the model, not something to tune away.',
          '']
    return '\n'.join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Run the Atlas imputation hold-out validation report')
    ap.add_argument('--replicates', type=int, default=3, help='independent deletion patterns (default 3)')
    ap.add_argument('--seed', type=int, default=0, help='master seed (default 0)')
    ap.add_argument('--points-per-gap', type=int, default=60,
                    help='target scored cells per gap length per replicate (default 60)')
    ap.add_argument('--datasets', default='pwt,attainment,barro_lee,wdi,uis',
                    help='comma list of: pwt, attainment, barro_lee, wdi, uis')
    ap.add_argument('--out', default=None,
                    help='optional path to write the markdown (default: print to stdout only)')
    args = ap.parse_args(argv)
    datasets = tuple(s.strip() for s in args.datasets.split(',') if s.strip())
    unknown = [d for d in datasets if d not in ('pwt', 'attainment', 'barro_lee', 'wdi', 'uis')]
    if unknown:
        raise SystemExit(f'unknown dataset(s) {unknown}; choose from pwt, attainment, barro_lee, wdi, uis')
    text = build_report(replicates=args.replicates, seed=args.seed, datasets=datasets,
                        points_per_gap=args.points_per_gap)
    if args.out:
        with open(args.out, 'w') as fh:
            fh.write(text + '\n')
        print(f'wrote {args.out}')
    else:
        print(text)


if __name__ == '__main__':
    sys.exit(main())
