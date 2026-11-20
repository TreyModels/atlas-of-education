# Cluster 3 — Geography & Size Scaling (X7, X8, X9)

All numbers below are quoted directly from `results/X7_size_ger.csv`,
`results/X8_citystate_pairwise.csv`, `results/X9_markets_ger.csv`, and
`CLUSTER_RESULTS.csv`. Estimator: OLS with country-clustered (CR1) SEs. No
imputation; complete cases per specification. All claims are descriptive
associations; no causal or directional claims are made.

**Proxy caveat (applies throughout):** MARKETS = (SP.URB.TOTL.IN.ZS/100 ×
SP.POP.TOTL)/1,000,000 = urban population in millions. It is a **derived
proxy, NOT a count of real markets**. SIZE = log(SP.POP.TOTL).

## X7 — Size and TER/SEC (30 countries, 1995–2024). Verdict: NOT SUPPORTED

SIZE coefficient on SE.TER.ENRR (primary):

| Spec | Estimate | SE | 95% CI | n | clusters |
|---|---|---|---|---|---|
| (a) between (country means) | −1.7386 | 1.8565 | [−5.3774, 1.9002] | 30 | 30 |
| (b) within (demeaned) | −5.6424 | 14.5399 | [−34.1406, 22.8558] | 656 | 30 |
| (c) pooled with country FE | −5.6424 | 14.5399 | [−34.1406, 22.8558] | 656 | 30 |
| (d) pooled without controls | −2.6115 | 2.3306 | [−7.1794, 1.9564] | 656 | 30 |

SIZE coefficient on SE.SEC.ENRR.UP (secondary):

| Spec | Estimate | SE | 95% CI | n | clusters |
|---|---|---|---|---|---|
| (a) between | 0.0187 | 2.9242 | [−5.7127, 5.7501] | 29 | 29 |
| (b) within | 29.4717 | 19.4236 | [−8.5985, 67.5419] | 504 | 29 |
| (c) pooled with country FE | 29.4717 | 19.4236 | [−8.5985, 67.5419] | 504 | 29 |
| (d) pooled without controls | −1.7590 | 2.3493 | [−6.3636, 2.8456] | 504 | 29 |

**Verdict: NOT SUPPORTED.** Every CI includes 0 in both the between and
within specifications for both dependent variables (between sign negative
for TER, within sign negative for TER but CI spans zero; SEC within sign
positive but CI spans zero). Threshold: min 10 countries met (n=30, 29).

## X8 — City-state (HKG) vs large systems (CHN/PHL/KHM). Verdict: NOT SUPPORTED

DESCRIPTIVE ONLY — n ≤ 4 per side (1 HKG vs 3 large systems). No
scaling-law claim is warranted or made.

Duration tertiary-15 → tertiary-50 (band midpoints from
UNIVERSALIZATION_TIMING, observed rows):

| Pair | Duration HKG | Duration other | Ratio | Status |
|---|---|---|---|---|
| CHN | 19.5 | 13.0 | 0.6667 | observed (censoring HKG: none/none, CHN: none/none) |
| PHL | 19.5 | — | — | UNABLE (PHL tertiary-15 crossing is left-censored) |
| KHM | 19.5 | — | — | UNABLE (KHM tertiary-50 crossing is right-censored) |

Volatility (SD of annual changes in ger_tertiary, UNIVERSALIZATION_SERIES):

| Pair | SD HKG | SD other | Ratio |
|---|---|---|---|
| CHN | 3.9746 | 1.9750 | 0.4969 |
| PHL | 3.9746 | 2.0115 | 0.5061 |
| KHM | 3.9746 | 1.0516 | 0.2646 |

**Verdict: NOT SUPPORTED.** The single uncensored duration ratio (0.6667)
and all three volatility ratios (0.4969, 0.5061, 0.2646) are below the 1.2
NOT-SUPPORTED floor; no ratio reaches FASTER (≥1.5) or SMOOTHER (≥2.0).
Censored pairs are reported UNABLE individually. Small-n caveat: each
"ratio" rests on one country per side; HKG duration uses band midpoints
(19.5 = 2007.5 − 1988.0).

## X9 — Number-of-markets proxy and TER. Verdict: PARTIAL

TER = SE.TER.ENRR. NOTE: JOBS_AND_MARKETS_PANEL.csv contains no
SE.TER.ENRR, so TER for the 6-system sample (KHM/CHN/HKG/JPN/KOR/PHL,
1995–2024) was taken from panel_wdi_long.csv. MARKETS is a derived proxy
(urban population in millions), not a count of real markets.

6-system sample (within spec, with LGDP): estimate 0.0560, SE 0.0330,
CI [−0.0087, 0.1207], n=139, clusters=6 — CI includes 0.

30-country sample (within spec, with LGDP): estimate 0.0353, SE 0.0177,
CI [0.0005, 0.0700], n=656, clusters=30 — CI excludes 0.

Other MARKETS specs (all from results/X9_markets_ger.csv): 6-system
between with LGDP −0.0072 [−0.0278, 0.0134] (n=6); 6-system within no LGDP
0.1209 [0.1174, 0.1244] (n=139); 30-country between with LGDP −0.0013
[−0.0151, 0.0126] (n=30); 30-country within no LGDP 0.1449 [0.0959,
0.1938] (n=656).

URBAN-only specs: 6-system within 1.3184 [0.4361, 2.2007] (n=139);
30-country within 1.4303 [0.6591, 2.2016] (n=656); between 6-systems
0.9197 [0.5014, 1.3380]; between 30-country 0.8536 [0.6389, 1.0683].

**Verdict: PARTIAL.** The within CI excludes 0 in the 30-country sample
only; the 6-system sample's CI includes 0 (threshold: association requires
both samples). Signs do not flip across samples (positive in both within
specs), and MARKETS and URBAN-only specs agree in sign, so the market-count
NOT-SUPPORTED override does not trigger. Given the proxy caveat, this is
evidence about urban population size, not about the number of markets.

## Reproducibility

- Run: `python code/run.py`, exit 0.
- Re-run produced byte-identical CSVs (SHA-256):
  - results/X7_size_ger.csv `c0f948de2aa62824716d25470ffbd3e2e61284cd993a90d6d7af8cf6f67a2b7c`
  - results/X8_citystate_pairwise.csv `5d75ad49f28bf90132f37ff99475abadbc166c7f0677ab6e9ac6c0d15d212bf5`
  - results/X9_markets_ger.csv `90d36e14bc96b663402e01118d5c5cecb0b376b79f31f3571d56e9fa66ab36f7`
  - CLUSTER_RESULTS.csv `980b77590a6146d26c13b1677880e906bd7f9cf7e06773ca8bc3db2ace9c4ce5`
- Details in RUN_MANIFEST.json.
