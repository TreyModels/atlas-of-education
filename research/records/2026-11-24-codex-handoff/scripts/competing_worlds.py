#!/usr/bin/env python3
"""Illustrative known-truth benchmark. Entirely synthetic; not the Atlas CUDA model.

Three worlds share schooling proportions and expected fertility in every cell.
A: schooling causes a fertility reduction. B: common trends alone. C: selection
on a latent type creates A's observational micro-pattern, without any schooling
effect. A and C are deliberately observationally indistinguishable.

Cell totals are Poisson under each world because exact schooling counts are fixed.
No parameters are fitted: the model predictions are oracle-known by construction.
Output compares macro and subgroup likelihoods on newly generated independent data.
"""
import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

WORLDS = ('effect', 'common_trend', 'selection')


def cells():
    # p changes across time, and means decline; values are hypothetical.
    return [(c, t, 0.15 + 0.13*t + 0.04*c, 5.0 - 0.46*t - 0.12*c)
            for c in range(3) for t in range(5)]


def rates(p, mu, contrast):
    # E[Y] is exactly mu in both rival observational models.
    return mu + p*contrast, mu - (1-p)*contrast


def experiment(n, contrast, rng):
    macro_ll = np.zeros(3)
    micro_ll = np.zeros(3)
    macro, observed = [], []
    for country, time, p, mu in cells():
        n1 = int(round(n*p)); n0 = n-n1; p_actual = n1/n
        lo, hi = rates(p_actual, mu, contrast)
        # Independent Poisson counts suffice: only sufficient statistics are used.
        # Selection assigns schooling exactly by latent type, so its observational
        # probabilities equal those of effect, but its interventions are different.
        for truth in WORLDS:
            mu0, mu1 = (mu, mu) if truth == 'common_trend' else (lo, hi)
            y0 = int(rng.poisson(n0*mu0)); y1 = int(rng.poisson(n1*mu1))
            # Log-likelihood omits terms constant across rival models.
            totals = y0 + y1
            macro_score = totals*math.log(n*mu) - n*mu
            score1 = y0*math.log(lo)-n0*lo + y1*math.log(hi)-n1*hi
            score0 = totals*math.log(mu)-n*mu
            macro.append((truth, country, time, n0, n1, totals, mu))
            observed.append((truth, country, time, y0/n0, y1/n1))
            i = WORLDS.index(truth)
            # All three models share the same macro likelihood, exactly.
            macro_ll[i] += macro_score
            # Accumulate evidence for structured micro-pattern vs common trend.
            micro_ll[i] += score1-score0
    return macro_ll, micro_ll, macro, observed


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--seed', type=int, default=71201)
    a.add_argument('--reps', type=int, default=200)
    a.add_argument('--n-per-cell', type=int, default=400)
    a.add_argument('--contrast', type=float, default=0.65)
    a.add_argument('--out', type=Path, default=Path('competing_worlds_output'))
    args=a.parse_args()
    if args.reps < 1 or args.n_per_cell < 10 or not 0 < args.contrast < 1:
        a.error('reps >= 1, n-per-cell >= 10 and 0 < contrast < 1 required')
    args.out.mkdir(parents=True, exist_ok=True)
    rng=np.random.default_rng(args.seed)
    wins={w:0 for w in WORLDS}; sums={w:[] for w in WORLDS}
    first_macro=first_observed=None
    for r in range(args.reps):
        _, micro, macro, observed=experiment(args.n_per_cell,args.contrast,rng)
        if r == 0: first_macro, first_observed = macro, observed
        for i,w in enumerate(WORLDS):
            sums[w].append(float(micro[i])); wins[w]+=int(micro[i]>0)
    summary={
        'disclaimer':'Synthetic illustration, not real-world causal evidence or the Atlas CUDA engine.',
        'oracle_design':'Cell means and subgroup rates are known by construction, not estimated. Scores are evaluated on fresh simulated observations.',
        'seed':args.seed,'replicates':args.reps,'countries':3,'periods':5,
        'individuals_per_cell':args.n_per_cell,'conditional_birth_difference':args.contrast,
        'macro_mean_targets': 'Identical for effect, common_trend and selection in every country-period by construction.',
        'micro_observational_distributions': 'effect and selection are identical by construction; common_trend has no within-cell schooling gradient.',
        'intervention_mean_difference_do_school_minus_do_no_school': {'effect':-args.contrast,'common_trend':0.0,'selection':0.0},
        'structured_micro_model_wins':{w:{'count':wins[w],'fraction':wins[w]/args.reps,
            'mean_log_likelihood_advantage':float(np.mean(sums[w]))} for w in WORLDS},
        'interpretation':'Macro likelihoods tie exactly for each dataset. Fresh micro outcomes can separate the specified common-trend model from the gradient models but cannot separate effect from selection; experimental or other credible identifying information is needed.',
    }
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    for name, header, rows in [('first_macro.csv',['truth','country','period','n0','n1','births','target_mean'],first_macro),
                                ('first_micro.csv',['truth','country','period','mean_births_uneducated','mean_births_educated'],first_observed)]:
        with (args.out/name).open('w',newline='') as f:
            w=csv.writer(f);w.writerow(header);w.writerows(rows)
    print(json.dumps(summary,indent=2))

if __name__ == '__main__': main()
