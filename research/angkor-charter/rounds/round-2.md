# Round 2 — the crown budget as committed obligations (v10 → v11)

Scripts: `v11_abm.js`, `v11_experiments.js`, `v11_report.js`. Results: `results/v11_all.csv`
(688 runs), `results/analysis_v11.json`.

## Which parameter was dead

Round 1's `X1_budget_split` produced **bit-identical** output for `(upkeepShare 0.30, monumentShare 0.45)`
and `(0.12, 0.18)` — peak 891, popDecl 0.44, elite 0.62, 4.1 relocations, decl 0.84, all identical to
the last digit. The reason was in the code, not in the physics:

```js
var discretionary = crownRevenue * (1 - armyShare);
var shareSum = upkeepShare + monumentShare;
var upkeepBudget = discretionary * upkeepShare / shareSum;      // ratio only
var monBudget = discretionary * monumentShare / shareSum
                + (upkeepBudget - upkeepPaid);                   // residual flows back to monument
```

Both levers entered only through the ratio `u/(u+m)`, and any unpaid upkeep allocation was handed to
the monument programme, so neither level could ever be identified. Under Monte Carlo `monumentShare`
scored −0.01 against the pattern indicator. So the state budget was one degree of freedom dressed as two.

## The structural fix (v11, F8)

The budget became a set of committed obligations, each with its own level:

```
army   = armyPerKm * netKm * (0.6 + 0.4*charter)      // garrison scales with the network it guards
temple = monumentShare * (revenue - army)             // a programme that cannot be deferred
upkeep = upkeepShare   * (revenue - army - temple)    // slack is elite consumption, not canals
```

`armyPerKm` and `monDep` (monument depreciation) are new; `monumentShare` and `upkeepShare` now enter
additively at their own levels.

## The ten experiments (medians of 8 seeds)

```
=== Y1_obligations ===                        peakYr  popD elite reloc  decl fund
  u55                                           920  0.46  0.60   3.1  0.83 0.38
  u85                                          1137  0.59  0.59   1.4  0.82 0.59
  u100                                         1480  0.31  0.30   0.3  0.52 0.73
  u100m0 (no temple programme at all)          1600  0.01  0.11   1.0  0.38 0.87

=== Y2_temple (upkeepShare=1.0) ===           peakYr  popD elite reloc  decl
  m0.00                                        1600  0.01  0.11   1.0  0.38
  m0.12                                        1530  0.15  0.18   0.1  0.47
  m0.25                                        1301  0.52  0.51   0.9  0.68
  m0.40                                        1020  0.50  0.60   2.0  0.80

=== Y3_garrison ===                           peakYr  popD elite reloc  decl  fund
  a0.10 / a0.35 / a0.70 / a1.40           1489/1480/1480/1454  ~0.3  0.27-0.43  0.3-0.5  0.50-0.63  0.73-0.69

=== Y4_timing (upkeepShare=1.0, bill never binds) ===  peakYr  popD elite reloc  decl
  pd1500 / pd2400 / pd3300 / pd4300       1555/1555/1555/1555  0.02  0.08  0  0.28   <-- identical

=== Y5_demog ===                              peakYr  popD elite reloc  decl
  g0.001 / g0.0025 / g0.005 / g0.008     1559/1480/1367/1167  0.26-0.31  0.29  0.3  0.48-0.52

=== Y6_arrears ===                            peakYr  popD elite reloc  decl
  d6 (fast dispossession)                       850  0.73  0.81  11.0  0.92
  d15                                           861  0.45  0.61   4.9  0.81
  d30 (slow)                                   1394  0.03  0.23   2.0  0.54
  d15s12 / d15s02 / floor10                 857/860/861  ~0.45  0.58-0.63  4-5.3  0.82-0.84

=== Y7_frontier ===                           peakYr  popD elite reloc  decl  cap binds
  zh1.02                                       1337  0.40  0.33   0.6  0.62   806
  zh1.35                                       1480  0.31  0.30   0.3  0.52   935
  zh2.0 / zh3.0                                1566/1519  0.02  0.08-0.09  0  0.22/0.24  never

=== Y8_monument_decay ===                     peakYr  popD elite reloc  decl
  dep0 / dep02 / dep05                      861/861/861  0.45-0.46  0.61  4.9-5.0  0.81   <-- identical
  prest4 (prestigeMax .004)                     861  0.42  0.61   2.1  0.83   lag 229
  prest05 (prestigeMax .0005)                   861  0.47  0.61   6.0  0.82   lag 129

=== Y9_rules ===                              peakYr  popD elite reloc  decl
  rentSurplus / elite15p / elite6p          856/860/861  0.49-0.53  0.60-0.61  4.8-11  0.81-0.87
  harddeath / nomigrate / raid30            859/861/861  0.46  0.61   5.0  0.81
```

Monte Carlo (360 runs, 19 parameters): interior-peak rate 0.99, full-pattern rate 0.01.
Correlations with peakYr: `pdPerKm` −0.40, `hEffFloor` +0.40, `kmPer1000T` −0.30, `debtLimit` +0.30;
with elite share: `debtLimit` −0.70, `rentRate` +0.30, `hEffFloor` −0.30; `upkeepShare`, `monDep`,
`raidRate`, `droughtSlope`, `netUp`, `clearProb`, `migrateProb`, `growRate` ≈ 0.

## Distance from the historical target

| | peak | lag | revDecl | elite | distance |
|---|---|---|---|---|---|
| target | 1100–1250 | 50–250 | >0.30 | 0.30–0.60 | 0 |
| **Y1 u85** | **1137** | **135** | **0.82** | **0.59** | **0** |
| Y2 m0.25 | 1301 | 146 | 0.68 | 0.51 | 51 |
| Y2 m0.40 | 1020 | 121 | 0.80 | 0.60 | 80 |
| Y7 zh1.02 | 1337 | 146 | 0.62 | 0.33 | 87 |

`Y1_obligations:u85` hits all four targets simultaneously (peak 1137 CE, relocation 135 yr later,
revenue −82%, elite land 0.59). Full-pattern rate for that variant 0.88.

## Interpretation

1. The budget degeneracy is fixed. `upkeepShare` alone now spans peak 920 → 1600 and `monumentShare`
   alone spans 1600 → 1020, i.e. each level is separately identified. The monotonicity is the expected
   one: a funded network delays the peak, a temple programme brings it forward.
2. One variant now lands inside the historical window on all four criteria (u85: 1137/135/0.82/0.59).
   The regime that does it is *partially* funded — mean fundedFrac 0.59, i.e. the crown pays about
   three-fifths of the maintenance bill for five centuries before the shortfall compounds.
3. `Y4_timing` is bit-identical across pd 1500–4300 for a legitimate reason, not a bug: with
   `upkeepShare = 1.0` the bill is always paid, so its *level* is irrelevant. The fiscal load is only
   identified in the binding regime — that is a conditional identification, and round 3 exploits it
   (Z5: pd4500 → peak 1099, pd6000 → 954).
4. Still dead after this round: `monDep` (0.00/0.02/0.05 bit-identical), `migrateProb`, `mortSlope`
   and `mortMax` (slowdeath/fastdeath within 3 yr of base), `raidRate` (raid30 identical to base),
   `armyPerKm` in the 0.1–1.4 range. `prestigeMax` only moves the relocation lag, not the peak.
5. The peak is still a fiscal event rather than a Malthusian one: `growRate` moves it (1167–1559) but
   only by shifting how fast households fill the fixed food envelope, and mortality parameters do
   nothing because households re-equilibrate to the food ratio within a single year.
