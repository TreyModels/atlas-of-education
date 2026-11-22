# Round 1 — closing the fiscal → water → harvest loop (v9 → v10)

Scripts: `v10_abm.js`, `v10_experiments.js`, `v10_report.js`. Results: `results/v10_all.csv`
(672 runs), `results/analysis_v10.json`. 400 settlements, 8 zones, 800–1600 CE.

## The structural fix (one fix, five parts of one mechanism)

The v9 ABM was parameter-deaf: all 664 runs peaked at 1600 and relocated zero times, and
`monumentShare`/`upkeepShare` gave bit-identical output. Diagnosis on the server, run by run:

1. `upkeepNeed` was the constant `(40 + 300*charter)*0.8 ≈ 272 t`, while crown revenue was
   ≈ 5,000–15,000 t (45% of elite rent). `fundedFrac` was therefore pinned at 1.000 every year,
   `infra` saturated at 1.0, and the `(0.55 + 0.45*infra)` factor in the harvest rule never moved.
   Crown revenue and cultivator survival were never in the same equation.
2. `charter` was pinned at 1.0 by `prestige = log(1 + monument/50000)*0.02`: `monument` accumulates
   and never decays, so prestige grew without bound and the `clamp(...,0,1)` held charter at 1 for
   the whole run. Nothing downstream of charter (relocation at charter < 0.25) could ever fire.
3. Mortality `wealth < -6.0 && r() < 0.05` almost never fired: with rent a fixed *share* of
   harvest, a bad year cost the cultivator nothing extra and wealth was monotonically positive
   (mean ≈ +34 t/settlement/yr). Population was a birth process with no death term.
4. `landCap` was inert (see the 400×150 ha = 60,000 ha note) and, once raised, was global.

Fix as implemented in `v10_abm.js`:

- **F1** the network has a length: `netKm → km0 + peakRevEver*kmPer1000T/1000`,
  `upkeepNeed = netKm*pdPerKm*pdToT` (canals, once dug, must be maintained even after revenue falls;
  `netDown` < `netUp` so the bill lags abatement). This makes a fiscal squeeze possible at all.
- **F2** the crown budget is a budget: `discretionary = revenue*(1-armyShare)`, then upkeep and the
  monument programme split it by normalised shares, so raising `monumentShare` starves the network.
- **F3** `hEff = 0.55 + 0.45*infra` enters every agent's `eff` — fiscal decline now reaches households.
- **F4** demography is food-driven: per-capita food ratio drives household growth and excess mortality
  (`growRate`, `mortSlope`, `mortMax`), and a settlement below 3 households is abandoned.
- **F5** per-zone land ceiling: `zoneCap[z] = zoneHeadroom ×` land initially farmed in zone z.
- **F6** rent accrues to the nearest elite (same zone first), not a random one.
- **F7** prestige has diminishing returns and a finite scale, so charter can fall.
- **F8 (added during calibration, kept because it was needed)** rent is *paid* as a share of the actual
  crop (so revenue stays elastic) but *assessed* on a normal-year yield; the shortfall becomes arrears
  and arrears above `debtLimit` force a land sale to the nearest elite. Without this, `eliteShareOfLand`
  was frozen at 0.02–0.08 and revenue decline was an artefact of the infra channel alone.

## Result: the ABM now produces an interior peak. Yes.

| run | peakYr | popDecl | relocs | lag | revDecl | eliteLand | meanFunded |
|---|---|---|---|---|---|---|---|
| v9 baseline (median over 664 runs) | 1600 | 0.00 | 0 | n/a | 0.20 | 0.12 | 1.00 |
| v10 default | **1003** | **0.49** | 2 | **128** | **0.795** | **0.573** | 0.502 |
| X5 `swCouple=0` (fix off) | 1583 | 0.01 | 0 | n/a | 0.42 | 0.07 | 0.53 |
| X5 `swCouple=1` (fix on) | 992 | 0.49 | 2.1 | 123 | 0.84 | 0.60 | 0.48 |

Interior-peak rate 0.99 over 672 runs (was 0.00 in v9). Turn the coupling off and the model reverts
to the v9 pathology (peak at 1583, zero population decline, zero relocations).

## The ten experiments (medians of 8 seeds)

```
=== X1_budget_split ===                       peakYr  popD elite reloc  decl
  u30m05 (monument starved)                     1438  0.24  0.26   0.3  0.45
  u30m18                                        992  0.49  0.60   2.1  0.84
  u30m45                                        891  0.44  0.62   4.1  0.84
  u12m18                                        891  0.44  0.62   4.1  0.84   <-- identical to u30m45

=== X2_fiscal_load ===                        peakYr  popD elite reloc  decl
  pd3000 (bill never binds)                     1534  0.01  0.07     0  0.25
  pd5000                                        992  0.49  0.60   2.1  0.84
  pd8000                                        884  0.52  0.60  10.1  0.80
  pd12000                                       852  0.55  0.61  12.0  0.81

=== X3_network_dyn ===                        peakYr  popD elite reloc  decl
  k10 (slow network growth)                     1534  0.01  0.07     0  0.25
  k30 / k30sticky                               992  0.49  0.60   2.1  0.84
  k60                                           874  0.42  0.60   7.6  0.78

=== X4_demog ===                              peakYr  popD elite reloc  decl
  g0.001 / g0.0025 / g0.005 / g0.008      1003/992/985/978  ~0.5  0.60  2.1 0.84

=== X5_coupling_off ===                       peakYr  popD elite reloc  decl
  nofix                                         1583  0.01  0.07     0  0.42
  fix                                            992  0.49  0.60   2.1  0.84

=== X6_arrears ===                            peakYr  popD elite reloc  decl
  d4s02                                         971  0.72  0.81   9.0  0.93
  d15s05 (default)                              992  0.49  0.60   2.1  0.84
  d40s05                                       1348  0.10  0.08   2.0  0.24
  floor90 (no dispossession below 90 ha)        992  0.43  0.55   2.0  0.79

=== X7_frontier ===                           peakYr  popD elite reloc  decl  cap binds
  zh1.02                                        948  0.42  0.47   2.3  0.80   806
  zh1.35 (default)                              992  0.49  0.60   2.1  0.84   944
  zh2.0 / zh3.0                                 996  0.44  0.72   2.0  0.80/0.40  1222/never

=== X8_infra ===                              peakYr  popD elite reloc  decl
  soft (decay .03 / repair .04)                 1466  0.23  0.26   0.3  0.50
  base                                          992  0.49  0.60   2.1  0.84
  hard                                          900  0.43  0.61   3.3  0.83
  floor30 / floor80                       967 / 1368  0.73/0.09  0.72/0.30  8.9/1  0.93/0.63

=== X9_rules ===                              peakYr  popD elite reloc  decl
  rentGross / rentSurplus                  992 / 937  0.49/0.51  0.60  2.1/10  0.84/0.91
  slowdeath / fastdeath                    995 / 990  0.48/0.51  0.60  2.1  0.84/0.83
  elite1pct / elite8pct                   1001 / 992  0.57/0.30  0.59/0.63  2  0.84/0.83
```

Monte Carlo (360 runs, 16 parameters drawn jointly): **interior-peak rate 0.99, full-pattern rate 0.01**.
Correlations with outcome: `debtLimit` → elite share −0.70 and popDecline −0.60; `hEffFloor` → peakYr
+0.50; `pdPerKm` → peakYr −0.20; `monumentShare` → pattern −0.01 (still dead under random draws);
`migrateProb`, `clearProb`, `netUp`, `crownShare` ≈ 0.

## Distance from the historical target

Target: peak 1100–1250, relocation lag 50–250 yr, revenue decline > 0.30, elite land 0.30–0.60.

| | peak | lag | revDecl | elite | distance |
|---|---|---|---|---|---|
| target | 1100–1250 | 50–250 | >0.30 | 0.30–0.60 | 0 |
| best v10 (multiple variants) | 992 | 123 | 0.84 | 0.60 | 108 (peak 108 yr too early) |
| X4 g0.001 | 1003 | 117 | 0.84 | 0.60 | 97 |

## Interpretation

1. The fiscal coupling is the missing mechanism: switching it off reproduces v9 exactly (peak 1583,
   no decline, no relocation), switching it on gives interior peaks in 99% of runs. The channel is
   crown revenue → upkeep funding → network condition → per-agent harvest → mortality → rent base.
2. Peak timing is not a demographic output; it is the date at which the maintenance bill overtakes the
   crown's allocation. That single parameter (`pdPerKm`, or equivalently the network growth rate
   `kmPer1000T`) moves the peak from 1534 to 852, while `growRate` moves it by 25 years. Demography is
   passive — the next defect.
3. The budget split is degenerate: `(u30,m45)` and `(u12,m18)` are bit-identical, so only the ratio
   `u/(u+m)` is identified, and under Monte Carlo `monumentShare` still has zero effect. The crown
   budget is one degree of freedom dressed as two. Round 2 attacks this.
4. Dispossession (`debtLimit`) is the strongest single control of elite land share (r = −0.70) and of
   how deep the fall goes (r = −0.60), so the land-market rule — not the rent rate — is what sets the
   class composition.
5. The model is still ~110 yr early on the peak: to reach 1100–1250 the fiscal squeeze has to start
   later, which means a smaller/laggier network bill relative to early revenue.
