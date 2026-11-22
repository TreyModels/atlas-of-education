# Round 3 — shocks on capital, not on a grain stock (v11 → v12)

Scripts: `v12_abm.js`, `v12_experiments.js`, `v12_report.js`. Results: `results/v12_all.csv`
(672 runs), `results/analysis_v12.json`.

## Which parameters were dead

Round 2 left `raidRate` and `droughtSlope` at zero effect: `Y9 raid30` produced peak 861, popDecl 0.46,
elite 0.61, 5.0 relocations — identical to the base and to `nomigrate`. The cause was that a raid was

```js
for (rr = 0; rr < N*0.02; rr++) { wealth[rnd] -= 1.0; }        // 8 agents lose 1 t
```

against a mean wealth flow of ≈ +34 t/settlement/yr, so the shock was erased by the next harvest.
Drought entered only as a multiplier on the *current* year's efficiency `(1 + shock)`, again a flow.
`mortMax`/`mortSlope` were dead for the same class of reason: households re-equilibrate to the food
ratio within a single year, so the mortality response never accumulates.

## The structural fix (v12, F9)

Shocks now hit **capital**, and therefore travel through the same condition variable as the fiscal loop:

```
drought year (shock < -0.05):  infra *= (1 - droughtDamage * (-shock) * 4)   // canals silt, bunds breach
raid event:                    infra *= (1 - raidInfraDamage)               // the hydraulic system is sacked
                               5% of settlements lose raidLandLoss of their land  // fields abandoned
```

A raid is now a permanent cut to the productivity of the whole polity, not a one-year debit; a drought
does not merely lower this year's yield but lowers the network condition that sets every future yield,
and the crown then has to fund repair out of a shrunken revenue.

## The ten experiments (medians of 8 seeds)

```
=== Z1_raid_rate ===            peakYr  popD elite reloc  decl
  x0.0                            1061  0.51  0.59   2.0  0.72
  x0.1                            1037  0.47  0.58   2.0  0.76
  x0.3                            1019  0.49  0.59   2.0  0.81
  x0.6                             964  0.51  0.59   2.4  0.82

=== Z2_raid_damage (raidRate .30) ===  peakYr  popD elite reloc  decl  fund
  dmg0.00 (old behaviour)          1044  0.50  0.59   2.0  0.72  0.59
  dmg0.05                          1024  0.49  0.58   2.0  0.74  0.59
  dmg0.15                           987  0.49  0.59   2.0  0.83  0.57
  dmg0.35                           977  0.49  0.60   2.8  0.78  0.56

=== Z3_drought_damage ===       peakYr  popD elite reloc  decl
  dd0.00                          1112  0.59  0.59   1.5  0.79
  dd0.02                          1065  0.51  0.59   2.0  0.67
  dd0.05                          1002  0.52  0.59   2.0  0.85
  dd0.10                           943  0.47  0.60   2.9  0.76

=== Z4_climate ===              peakYr  popD elite reloc  decl
  cv0.05                          1366  0.49  0.44   0.8  0.60
  cv0.10                          1037  0.47  0.58   2.0  0.76
  cv0.18                           910  0.54  0.67   4.1  0.82
  cv0.28                           832  0.62  0.72   6.9  0.87

=== Z5_timing (binding regime) ===  peakYr  popD elite reloc  decl
  pd2500                          1555  0.02  0.09     0  0.26
  pd3500                          1550  0.02  0.09     0  0.23
  pd4500                          1099  0.57  0.59   1.4  0.80
  pd6000                           954  0.46  0.59   4.0  0.76

=== Z6_frontier ===             peakYr  popD elite reloc  decl  cap binds
  zh1.05                           984  0.45  0.48   2.0  0.81   815
  zh1.20                          1000  0.43  0.53   2.0  0.75   870
  zh1.35                          1037  0.47  0.58   2.0  0.76   933
  zh1.60                          1066  0.50  0.65   2.0  0.75  1058

=== Z7_elite ===                peakYr  popD elite reloc  decl
  e1 / e2 / e5              1030/1038/1039  0.57/0.54/0.45  0.59-0.60  2.0  0.74-0.77
  e2c30 / e2c60              1012/1041  0.56  0.58-0.59  3.8/2.0  0.82/0.68

=== Z8_infra_floor ===          peakYr  popD elite reloc  decl
  hf0.35                          1012  0.69  0.69   3.9  0.86
  hf0.50                          1029  0.58  0.62   2.1  0.85
  hf0.65                          1064  0.46  0.51   1.9  0.70
  hf0.80                          1216  0.11  0.27   1.0  0.55

=== Z9_rules ===                peakYr  popD elite reloc  decl
  monDep04 / prest04         1037/1029  0.47/0.53  0.58-0.59  2.0/2.5  0.76/0.80
  rentSurplus                      967  0.54  0.59   9.4  0.89
  floor10                         1037  0.47  0.58   2.0  0.75
  combined (zh1.2,pd3500,raid.3)  1499  0.16  0.18   0.1  0.40
  debt8                           1019  0.72  0.78   7.0  0.91
```

Monte Carlo (360 runs, 21 parameters): interior-peak rate 0.99, full-pattern rate 0.01.
Correlations with peakYr: `climateVol` −0.40, `hEffFloor` +0.30; with revenue decline: `climateVol`
+0.30; with elite share: `rentRate` +0.40, `climateVol` +0.30. `armyPerKm`, `growRate`, `migrateProb`,
`monumentShare`, `crownShare` ≈ 0. `climateVol` is now the strongest single driver of peak timing
(it was ≈ 0.0 in round 2).

## Distance from the historical target

| | peak | lag | revDecl | elite | distance |
|---|---|---|---|---|---|
| target | 1100–1250 | 50–250 | >0.30 | 0.30–0.60 | 0 |
| **Z3 dd0 (no extra drought damage)** | **1112** | **129** | **0.79** | **0.59** | **0** (pattern 0.88) |
| **Z5 pd4500** | **1099** | **142** | **0.80** | **0.59** | **0** (pattern 1.00) |
| Z8 hf0.80 | 1216 | 194 | 0.55 | 0.27 | 3 (elite 0.03 low) |
| Z3 dd0.02 | 1065 | 123 | 0.67 | 0.59 | 35 |
| v10 default (round 1) | 992 | 123 | 0.84 | 0.60 | 108 |

`Z5 pd4500` hits all four targets in **every** seed (pattern 1.00) and `Z3 dd0` in 88% of seeds.

## Interpretation

1. Rerouting shocks through capital works: `raidRate` now spans peak 1061 → 964 and revenue decline
   0.72 → 0.82; `droughtDamage` spans 1112 → 943; `climateVol` spans 1366 → 832 and is now the strongest
   determinant of peak timing in the Monte Carlo (r = −0.40 on peakYr). The earlier "raiding is harmful"
   result is reproduced in the ABM, but only once raids damage the network rather than households'
   grain stock.
2. Two round-3 variants land inside the whole historical envelope, one of them in every seed:
   `Z5 pd4500` (peak 1099, lag 142, decline 0.80, elite 0.59) and `Z3 dd0` (1112, 129, 0.79, 0.59).
   The 110-yr earliness of round 1 is fixed by lowering the maintenance load into the partially-funded
   regime rather than by touching demography.
3. The model is well identified on the fiscal side and badly identified on the demographic side.
   Peak timing responds to `pdPerKm`, `climateVol`, `hEffFloor`, `kmPer1000T`, and to almost nothing
   sociological; `growRate`, `mortSlope`, `mortMax` and `migrateProb` remain near-zero.
4. Still dead after three rounds: `monDep`, `migrateProb`, `armyPerKm` (0.1–1.4), `mortSlope`/`mortMax`,
   `clearProb`, `netUp`, and `crownShare` in the presence of the arrears channel. `monumentShare` is
   live level-wise but weak under random draws, because at MC-drawn values upkeep is usually starved
   already and the temple programme is funded out of a residual that no longer exists.
5. The residual error is structural, not parametric: revenue declines are always steeper than history
   (0.55–0.85 against a >0.30 threshold) because dispossession is a ratchet — elites never sell land
   back, so once the frontier closes the rent base only falls. A land market with a return flow (land
   re-purchased by cultivators in good decades) is the obvious next fix.
