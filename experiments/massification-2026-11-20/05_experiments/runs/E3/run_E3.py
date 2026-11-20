"""E3 Japan within-country: which structural variable can drive the grade-6 juku gradient?
Endpoint + elasticity-identification test (only two endpoints are on disk)."""
import json, os, sys
import numpy as np

OBS = dict(mean=41.8, akita=22.1, tokyo=57.9, r_with_achievement=-0.16)
RATIO = OBS['tokyo'] / OBS['akita']
# declared auxiliary Tokyo/Akita ratios (sourced / estimated / assumed - labelled in the output)
DRIVERS = {
    'density_competition': dict(ratio=6363.0 / 89.0, band=(0.1, 0.6),
                                basis='sourced approximate: pop density 6,363 vs 89 per km2 (Statistics Bureau 2020)'),
    'income': dict(ratio=1.6, band=(0.1, 1.0),
                   basis='estimated/assumed: prefectural per-capita income ratio ~1.6 (accounts not on disk)'),
    'gate_stakes': dict(ratio=1.2, band=(0.5, 2.0),
                        basis='assumed: high-school applicants-per-seat ratio ~1.2 (NOT FOUND on disk)'),
}


def main(out):
    os.makedirs(out, exist_ok=True)
    rows = []
    for k, d in DRIVERS.items():
        req = float(np.log(RATIO) / np.log(d['ratio']))
        lo, hi = d['band']
        rows.append(dict(driver=k, auxiliary_ratio=d['ratio'], required_elasticity=req,
                         plausibility_lo=lo, plausibility_hi=hi, passes_T4=(lo <= req <= hi),
                         basis=d['basis']))
    # T5: density model mean consistency with only the two endpoints (no prefecture fitting):
    # a linear-in-log-density model through the two endpoints must predict the unweighted mean
    # once a density distribution is assumed. With no prefecture densities on disk we report the
    # required mean-density position and state the data gap instead of inventing 47 values.
    dens_pass = any(r['driver'] == 'density_competition' and r['passes_T4'] for r in rows)
    t5_possible = False   # full prefecture density table is not on disk -> cannot compute the mean
    L = ['E3 JAPAN WITHIN-COUNTRY IDENTIFICATION (grade-6 juku)',
         f'Observed: prefecture mean {OBS["mean"]}%, range {OBS["akita"]}% (Akita) - {OBS["tokyo"]}% (Tokyo),'
         f' Tokyo/Akita = {RATIO:.3f}; r with achievement = {OBS["r_with_achievement"]:+.2f} (external note only).',
         'Only the two ENDPOINTS and the mean are on disk; the full 47-prefecture table is not.',
         '', 'REQUIRED ELASTICITY to span the observed range, by candidate channel:',
         f'  {"driver":22s} {"ratio T/A":>9s} {"required e":>10s} {"band":>12s} {"verdict":>8s}']
    for r in rows:
        L.append(f'  {r["driver"]:22s} {r["auxiliary_ratio"]:9.2f} {r["required_elasticity"]:10.3f} '
                 f'[{r["plausibility_lo"]:.1f},{r["plausibility_hi"]:.1f}]{r["passes_T4"]:>8}'.replace('True', 'PASS').replace('False', 'FAIL'))
    L += ['', 'BASIS of each auxiliary ratio:'] + [f'  {r["driver"]:22s} {r["basis"]}' for r in rows]
    t4 = [r['driver'] for r in rows if r['passes_T4']]
    L += ['', 'T4 (predeclared): a channel passes only if its required elasticity is inside its plausibility band.',
          f'  channels passing T4: {t4 if t4 else "none"}',
          '', 'T5 (predeclared): density model mean within +/-5 pp of 41.8 with no prefecture fitting.',
          '  NOT COMPUTABLE: the full prefecture density/juku table is not on disk (only Akita and Tokyo),',
          '  so the unweighted mean cannot be predicted without inventing 45 data points. Reported as a data gap.',
          '', 'VERDICT:',
          '  The density/competition channel is the only one that spans the observed range with a plausible',
          '  elasticity (~0.23): Tokyo/Akita density is ~70x while the participation ratio is only 2.6x, so a',
          '  modest density elasticity suffices. The income channel requires e~2.1 and the gate-stakes channel',
          '  e~5.3 to span the same range - both outside their plausibility bands, so both FAIL.',
          '  WHAT FAILS / LIMITS: (i) n=2 endpoints means no rank correlation and no R^2 can be computed, so',
          '  density is "not rejected", not identified; (ii) the r=-0.16 with achievement is an external',
          '  consistency note only - the data needed to test it are not on disk; (iii) income is correlated with',
          '  density across the two endpoints, so without the full table the density channel could be standing',
          '  in for any urban correlate (private-school share, commute costs, provider chain penetration).']
    open(os.path.join(out, 'findings.txt'), 'w').write('\n'.join(L) + '\n')
    import csv
    with open(os.path.join(out, 'e3_channels.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    json.dump(dict(obs=OBS, ratio=RATIO, drivers={k: dict(ratio=v['ratio'], band=v['band']) for k, v in DRIVERS.items()},
                   T4_pass=t4, T5_computable=False),
              open(os.path.join(out, 'run_meta.json'), 'w'), indent=1)
    print('\n'.join(L))


if __name__ == '__main__':
    main(sys.argv[1])
