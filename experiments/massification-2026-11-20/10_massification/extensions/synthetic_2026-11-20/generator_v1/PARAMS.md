# PARAMS — every parameter of the SYNTHETIC generator v1, with value, unit and source

**`LABEL: SYNTHETIC.`** This file documents a declared-assumption simulator. Nothing here is estimated,
nothing here is evidence about any country, and no number below licenses a causal claim. The observed
numbers that appear are *targets voluntarily encoded for the PHL-like synthetic country*, listed in §2 so a
reader can subtract them from any claim of reproduction.

Files: [`code/sim_v1.py`](code/sim_v1.py) · [`RUN_MANIFEST.json`](RUN_MANIFEST.json) ·
[`TUNE_LOG.md`](TUNE_LOG.md) · [`FINDINGS.md`](FINDINGS.md)

> **Authoritative source.** `RUN_MANIFEST.json → params` is written by the generator from the module-level
> block in `code/sim_v1.py`. This file is the human-readable mirror plus the material the manifest cannot
> carry: units, sources, anchors and the predeclared scoring rules.

Source vocabulary (one token per row):

| token | meaning |
|---|---|
| `literature` | the value is *anchored* on a number that exists in the programme's literature layer (cited) — the form it enters is still a declared choice |
| `declared` | invented for v1 by design; no estimate exists anywhere. **This is the majority.** |
| `observed target` | a PHL number taken from the fact register and encoded on purpose (see §2) |
| `convention` | accounting identity or definitional constant |

---

## 1. Panel and seed

| item | value | unit | source |
|---|---|---|---|
| seed | `20261120` | — | declared (fixed; single PCG64 stream) |
| countries | 30 synthetic (`SYN00_PHL_LIKE`, `SYN01_TWIN_MFG`, `SYN02_TWIN_OFFICE`, `SYN03`…`SYN29`) | count | declared |
| years | 1970–2025 | year | declared |
| levels | primary, lower_secondary, upper_secondary, tertiary | — | declared |
| panel rows | 30 × 56 × 4 = 6 720 | rows | convention |
| run time | ≈1 s (plus 3 internal counterfactual runs for the B/C/D checks) | s | measured |
| label column | `SYNTHETIC` in every row and every file | — | convention |

**No real country is modelled.** The labels are synthetic identifiers; `SYN00_PHL_LIKE` is a *declared
parameterisation intended to resemble a published signature*, not the Philippines.

---

## 2. Observed numbers encoded — the exact and complete list

These are the only observed numbers that enter the code. §2a enter **numerically**; §2b are recorded
**for rationale only** and enter no computation.

### 2a. Used numerically (all for `SYN00_PHL_LIKE` only)

| fact id | number | where it enters |
|---|---|---|
| PHL-01 | primary completion 83.16 (1999), 87.45 (2013), 91.918 (2017), 95.40 (2021), 98.305 (2024) | shapes the declared `surv_pri` anchor path: 1970 .700 / 1999 .795 / 2013 .835 / 2017 .872 / 2021 .931 / 2024 .971 |
| PHL-01 | first year ≥90 = **2017** | the anchor that pins the primary crossing |
| PHL-02 | lower-secondary completion 58.86 (1999), 71.27 (2013), 81.255 (2017), 92.414 (2024); 2023 = 88.442 | `surv_low` and `seat_low` anchor paths; crossing year 2024 |
| PHL-03 | upper-secondary 76.433 (2017, series max), 75.025 (2024), never ≥90 | `seat_up` anchor (0.845 at 2017, 0.875 at 2024) and `surv_up` |
| PHL-04 | tertiary GER **16.336** (1971) | `ger0[tertiary] = 0.163` |
| PHL-04 | tertiary GER 38.345 (2016) → 28.117 (2018) → 47.414 (2024) → **51.072** (2025) | **diagnostic only** — used to judge the dip, never to set anything |
| PHL-05 | primary GER 99.54 (1971), 106.47 (1990), 103.41 (2015), 99.37 (2017), 94.55 (2018), 88.83 (2021), 94.03 (2024) | shapes the declared `overage` (over-age margin) path: +1.5 / +6.5 / +4.0 / +1.0 / −2.5 / −6.0 pp at the anchor years |
| PHL-05 | primary NER 96.79 (1976) | **not used** (v1 has no NER object) |

### 2b. Rationale only — present in this document, absent from the arithmetic

| fact id | number | why it does not enter |
|---|---|---|
| CAP-03 | primary PTR 35.074 (2005) → 29.084 (2017); education spending 2.328 → 3.964 %GDP | the declared *reason* the floor capacity path rises. The capacity→survival map was replaced by direct anchor interpolation (§4.4), so these numbers are context, not inputs. |
| CAP-04 | "capacity buys the floor, not the ceiling" | a **stipulation** encoded as the ceiling seat cap, not a number |
| NEG-07 | ceiling residual 14.975 pp | a *check*, never an input |

The K-12-style pipeline break at upper secondary (§4.4) is a **declared mechanism**, not an observed
number: 2018 0.93, 2019 0.90, 2020 0.91, 2021 0.95 completion multipliers. It is **not cohort-conserving** —
it destroys ≈8 % of upper-secondary completions in those four years. Declared, not fitted.

---

## 3. Layer 0 — economy states

| parameter | value | unit | source |
|---|---|---|---|
| `lf_share_of_pop` | 0.52 | labour force, share of population | declared |
| `age_share_base` | 0.160 | school-age (6–22) share of pop at TFR 1.4 | declared |
| `age_share_tfr_slope` | 0.045 | +share per +1 TFR | declared |
| `age_share_min`, `age_share_max` | 0.130, 0.420 | share | declared |
| `band_share` | (0.42, 0.21, 0.20, 0.17) | split of the school-age population by level band | declared |
| `x_income_coef` | 0.55 | dX per d ln(GDPpc/1000) | declared |
| `x_urban_coef` | 0.55 | dX per d urban share | declared |
| `x_urban_ref` | 0.40 | urban reference point | declared |
| `x_min`, `x_max` | 0.0, 1.80 | complexity index bounds | declared |
| `takeoff_lit` | 0.60 | adult literacy threshold, pre → industrializing | declared |
| `takeoff_income` | 1500.0 | synthetic USD precondition | declared |
| `div_x`, `div_income` | 0.95, 6000.0 | industrializing → diversified thresholds | declared |
| `lit_learn` | 0.05 | annual closing fraction of the literacy gap | declared |
| `lit_lag` | 12 | years from primary completion to adult literacy | declared |
| `sec_ag_base` / `sec_ag_x` | 0.500 / −0.450 | ag share at X = 0.6 / slope on (X−0.6) | declared (no literature functional form exists; `SIMULABILITY` §4) |
| `sec_inf_base` / `sec_inf_x` | 0.240 / −0.080 | informal share | declared |
| `sec_man_base` / `sec_man_x` | 0.130 / 0.090 | industry share | declared |
| `sec_floors` | (0.02, 0.05, 0.03, 0.05) | minimum shares; services is the residual, water-filled so shares sum to 1 | convention |

Sector-share **directions** follow SCA-04 (agriculture falls steeply, industry rises); the magnitudes are
invented. SCA-04's within/between split is *not* reproduced — that would need an estimated model.

Takeoff is an absorbing switch, not a continuous variable: `pre → industrializing` iff literacy ≥ 0.60 and
GDPpc ≥ 1500; `industrializing → diversified` iff X ≥ 0.95 and GDPpc ≥ 6000.

---

## 4. Layers 1–3

### 4.1 Job ladder (Layer 0/2)

| parameter | value | unit | source |
|---|---|---|---|
| `rung_a` | (0.90, 0.40, −0.30, −1.30) | softmax intercept by rung | declared |
| `rung_b` | (−0.65, 0.20, 1.00, 2.20) | softmax slope on (X−0.6) | declared |
| `x_open` | (0.00, 0.08, 0.26, 0.48) | rung exists only if X ≥ x_open[r] | declared — the "ECI gating" of check D |
| `office_u_coef` | (0.0, 0.35, 0.0, −0.20) | office-bias loading on rung utility | declared |
| `mfg_u_coef` | (0.0, −0.10, 0.30, 0.10) | manufacturing-bias loading | declared |
| `phi_formal` | 0.82 | formal share of industry + services employment | declared |
| `sep` | (0.10, 0.07, 0.05, 0.04) | annual separation rate by rung | declared |
| `seek` | (0.15, 0.35, 0.60, 0.80) | share of graduates who seek a formal rung | declared |
| `queue_retain` | 0.50 | share of unmatched formal-seekers still queued next year | declared |
| `queue_max_lf` | 0.20 | queue cap, share of the labour force | declared |
| `rank_gain` | 0.20 | rank premium when a rung's queue is rationed | declared |

Rung requirement = the graduate's level index (rung 1 elementary ← primary; rung 2 clerical ← lower-sec;
rung 3 technical ← upper-sec; rung 4 professional ← tertiary). Matching runs **highest rung first**, and
inside a rung **highest level first** (the credential queue). Unmatched formal-seekers queue (50 % annual
decay) or fall into the informal block, the residual absorber.

### 4.2 Wages

| parameter | value | unit | source |
|---|---|---|---|
| `rung_mult` | (2.20, 3.20, 4.60, 6.40) | rung wage ladder × GDPpc/1000 | declared |
| `cred_prem` | 0.10 | credential premium per completed level | declared; *order of magnitude* of the Mincer 0.088/yr price (`HC-01`, Psacharopoulos & Patrinos 2018) — **not** that estimate, and not used as an elasticity |
| `psi_pre` / `psi_ind` / `psi_div` | 0.02 / 0.22 / 0.12 | informal-wage literacy slope by regime | declared (architecture: literacy pays ~0 pre-industrial, positive after takeoff) |
| rank factor | `1 + 0.20·(1 − tightness)` for rungs 2–4; **exactly 1.0 for rung 1** | multiplier | declared — the rung-1 restriction is what makes check C's primary-margin flatness structural |

Formal wage = `(GDPpc/1000) · rung_mult[r] · (1 + 0.10·r) · rank_factor[r]`.
Informal wage = `(GDPpc/1000) · (1 + psi(T)·literacy)`.
No earnings microdata, no returns regression, no place premium is used anywhere.

### 4.3 Growth (Layer 3)

| parameter | value | unit | source |
|---|---|---|---|
| `gp` | (0.012, 0.008, 0.030, 0.022) | sector productivity growth: ag, informal, industry, services | declared |
| `accel_ind` | (1.0, 1.0, 1.6, 1.3) | sector growth multipliers once industrializing | declared |
| `accel_div` | (1.0, 1.0, 1.3, 1.5) | … once diversified | declared |
| `comp_step` | (0.10, 0.18, 0.32, 0.50) | growth step per unit of Δ(employment/LF), by rung | declared |
| `lit_ag_growth` | 0.010 | extra ag/informal productivity growth × literacy, **only when T ≥ industrializing** | declared (architecture: literacy pays off by raising informal/agri productivity) |
| `g_floor`, `g_cap` | 0.0, 0.090 | growth clip | declared |
| `g_noise_sd` | 0.006 | sd of annual growth noise | declared |

Growth has **no term in graduates**. Extra graduates with no rung add queue and informal labour, not
output. The only schooling→growth channels are (i) composition — a worker moving into a rung adds a finite
step, larger for higher rungs — and (ii) `lit_ag_growth`, active only after takeoff. GDPpc(t+1) =
GDPpc(t)·(1+g(t)); the income path is endogenous, so nothing pins a country's growth to an assumed rate.

### 4.4 Schooling supply (Layer 1)

| parameter | value | unit | source |
|---|---|---|---|
| `dur` | (6, 3, 3, 4) | years per level | convention |
| annual cohort `C_L` | `band_share_L · S / dur_L` | persons/yr | convention |
| `ger_cap` | 105.0 | hard cap on GER | convention (the Z1 gate) |
| `overage_cap` | 1.05 | intake may exceed the annual cohort by 5 % | convention |
| `star_c1` | (0.30, 1.60, 1.45, 0.90) | logit income elasticity of demand, by level | declared |
| `star_c3` | (0.25, 1.10, 1.10, 0.70) | logit complexity slope, by level | declared |
| `adj_speed` | (0.50, 0.50, 0.35, 0.35) | annual adjustment of GER toward target | declared |
| `surv_min` | (0.62, 0.55, 0.60, 0.70) | survival floor at zero capacity (29 non-PHL countries) | declared |
| `seat_lo` / `seat_hi` | (1.02, 0.28, 0.14, 0.05) / (1.05, 0.985, 0.80, 0.78) | seat capacity start / end (29 non-PHL countries) | declared |
| `ter_pool_retain`, `ter_trans_cap` | 0.35, 0.65 | tertiary eligible-pool memory and transition cap | declared |
| `meas_completion_factor` | (1.0, 1.0, 1.0, 1.0) | completion denominator adjustment | convention — kept at 1.0 deliberately; see FINDINGS on why the observed completion > GER ratios are then unreachable |

**The cohort-flow identity actually implemented:**

```
C_L(t)          = band_share_L · S(t) / dur_L                     annual cohort
intake_L(t)     = GER_L(t)/100 · C_L(t)                           new entrants (≤ 1.05·C_L)
GER_L(t)        = clip(GER_L(t−1) + adj_L·(target − GER_L(t−1)), 0, 105)
target          = min(star_L(Y,X)·push, 100·seat_L(t)·push, 100·elig_L(t), 105)
elig_L(t)       = last year's completers of level L−1 / C_L(t)    pipeline gate
graduates_L(t)  = intake_L(t−dur_L) · surv_L(t) · pipe_L(t)
completion_L(t) = 100 · graduates_L(t) / C_L(t−dur_L)             share of the ENTERING cohort
intake + out_of_school = cohort + over_age_intake                 exact, by construction
```

Completion is a **cohort-flow object** — never a product of fitted probabilities, and never a monotone
transform of the *current* GER (it is a transform of the *entering* GER, which is why the two can diverge in
both directions). `push` is 1.0 in every reported run except the check-D counterfactual (1.10).

**PHL-like declared supply paths** (`surv_override`, `seat_override`) are interpolated through the §2a
anchor years. The PHL `overage` path adds ±pp to primary GER. The `pipe` path cuts upper-secondary
completions in 2018–2021. All three are declared design objects, not estimates.

### 4.5 The three labelled parameterisations

| | `SYN00_PHL_LIKE` | `SYN01_TWIN_MFG` | `SYN02_TWIN_OFFICE` |
|---|---|---|---|
| y0 (1970 GDPpc) | 2000 | 2600 | 2600 |
| pop0 / pop growth | 36e6 / 1.65 % | 20e6 / 1.4 % | 20e6 / 1.4 % |
| TFR 1970 / decline | 5.6 / 0.052 | 4.0 / 0.030 | 4.0 / 0.030 |
| urban 1970 / growth | 0.33 / 0.0045 | 0.42 / 0.004 | 0.42 / 0.004 |
| literacy 1970 | 0.83 | 0.72 | 0.72 |
| initial GER (p, l, u, t) | .995 / .58 / .32 / .163 | .90 / .62 / .44 / .22 | identical |
| ag / inf / man offsets | −.03 / +.08 / −.03 | 0 / −.03 / **+.07** | 0 / +.02 / **−.06** |
| office bias / mfg bias | **−1.20** / −0.80 | −0.30 / **+0.80** | **+0.80** / −0.30 |
| credentialist flag | yes | no | no |
| delivery pace | 1.10 | 1.15 | 1.15 |

The twins differ **only** in the last two rows (sector mix and its rung loadings). That is the controlled
comparison behind check E.

### 4.6 Drawn heterogeneity (the other 27 countries)

`y0 ~ LN(ln 2500, 0.85)`; `pop0 ~ LN(ln 15e6, 1.0)`; population growth `N(0.015, 0.005)` clipped
[0.002, 0.032]; `TFR0 ~ U(2.2, 6.2)`, decline `U(0.010, 0.060)`; urban `U(0.12, 0.78)`, growth
`U(0.001, 0.007)`; literacy `0.10 + 0.60·ln(y0/800)/1.6 + N(0, 0.08)` clipped [0.05, 0.96]; complexity
offset `N(0, 0.16)`; sector offsets `N(0, 0.06/0.05/0.04)`; office and mfg bias `N(0, 0.55)`; delivery pace
`N(1.0, 0.28)` clipped [0.35, 1.9]; initial GER by level from a logit in income and literacy with
`N(0, 0.55)` shocks, forced non-increasing down the ladder; 20 % of countries flagged "credentialist"
(upper/tertiary demand ×1.35/×1.60 — the declared over-expansion heterogeneity that generalises the user's
PHL point).

---

## 5. Predeclared scoring rules for checks A–F

Frozen before the final run; the design-phase history is in `TUNE_LOG.md`. `p` values are two-sided normal
approximations from classical OLS standard errors.

| check | pass rule |
|---|---|
| **A** | (A1) primary completion first ≥90 in **2017**; (A2) lower-sec first ≥90 in **2024** with 2023 < 90; (A3) upper-sec never ≥90 for years ≤2024, max ≤ 77.0, 2024 ∈ [73.5, 76.5]; (A4) tertiary GER 1971 ∈ [14.3, 18.3] **and** 2025 ∈ [48.1, 54.1]; (A5) floor→middle gap ∈ [5, 9] y; (A6) ceiling residual 90 − upper-sec(2024) ∈ [13, 17] pp. All six. |
| **B** | Decade panel (30 countries × 6 decades, decade FE), growth in pp. (B1) `b_lit` > 0 with p < 0.05; (B2) `b_yos` insignificant at 10 % **or** \|`b_yos`\| < 0.5·\|`b_lit`\|; (B3) the takeoff-regime ablation (all countries forced pre-industrial, same seed) reduces \|`b_lit`\| by ≥50 % or makes it ≤ 0. |
| **C** | Country-year panel, 1975–2025. (C1) `ln(w_rung1/w_informal)` on queue pressure **with a literacy control and regime FE**: coefficient ≤ +0.05 (no *positive* rank premium at the primary margin); (C2) `ln(w_rung2/w_rung1)` on the same: coefficient > 0.30 with p < 0.01. |
| **D** | Counterfactual: +10 % to every level's demand **and seat** target in every country, same seed. Δg = pushed − baseline, mean 1980–2025. (D1) regression of Δg on X(1980) has slope > 0 with p < 0.05; (D2) mean Δg in the high-X tercile > 2× the low-X tercile and > 0. |
| **E** | Twins with identical schooling parameters; the longest window from 1970 in which cumulative graduates differ by < 2 % must last ≥ 5 years, and inside it \|Δ mean growth\| ≥ 0.20 pp **and** relative \|Δ queue pressure\| ≥ 20 %. |
| **F** | GER ∈ [0, 105]; completion ∈ [0, 105]; shares sum to 1 (1e−9); cohort conservation exact (1e−9) *including* the over-age term; no negative stocks; out-of-school ≥ 0. |

---

## 6. What v1 does **not** contain

- No estimated coefficient anywhere. No calibration to the observed PHL panel beyond §2a.
- No direction-of-causation claim, no "capacity explains timing" claim, no single-number scaling target.
- No returns→enrolment response (`HC-03` is not found; `SIMULABILITY` §4), no enforcement series, no
  world-society block, no requirement ratchet.
- No regional (17-region) layer: `REG-01…REG-05` are out of scope; they need a within-country structure
  this generator does not have.
- No fertility→completion channel of the SCA-05 kind: cohort size affects the denominator only.
- No NER object, no PTR/spending series inside the model (they are rationale, not inputs).
