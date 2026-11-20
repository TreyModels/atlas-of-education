# FINDINGS — SYNTHETIC generator v1.3: shadow education at the gates

**`LABEL: SYNTHETIC.`** Every number in this file was produced by a declared-assumption simulator. None of
it is evidence about the world, none of it is an estimate or a forecast, and none of it licenses a causal or
direction claim. No real country is modelled. The three "country types" are synthetic parameterisations named
for the cases that informed them; they are **not** Hong Kong, the Philippines or Cambodia.

Files: [`code/sim_v1_3.py`](code/sim_v1_3.py) · [`PARAMS.md`](PARAMS.md) · [`PRE_DECLARATIONS.md`](PRE_DECLARATIONS.md)
(verbatim copy of the frozen spec + S1 note) · [`IMPLEMENTATION_NOTE.md`](IMPLEMENTATION_NOTE.md) +
[`IMPLEMENTATION_NOTE_N1.md`](IMPLEMENTATION_NOTE_N1.md) (pre-run spec-gap resolutions) · [`TUNE_LOG.md`](TUNE_LOG.md) ·
[`results/`](results/) · [`RUN_MANIFEST.json`](RUN_MANIFEST.json)

**Spec implemented:** `shadow_module/PRE_DECLARATIONS.md`, sha256
`cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2`, plus the binding controller note
`PRE_DECLARATIONS_S1_NOTE.md`, sha256 `af49a616a7b57c4ef23a693c155d022cd17817f66f5acafba4dc6798dedb65eb`.
Both are re-hashed at start-up; the run refuses on mismatch.

---

## In plain English

I bolted a **household tutoring decision** onto the frozen v1.2 generator, at its own gates. A family buys
tutoring when the queue in front of it is crowded, the credential behind the gate is worth something, tutoring
would actually raise the chance of getting through, and the fee is affordable relative to its income — and for
no other reason. The same behavioural coefficients are used for every country; countries differ only through
four declared inputs (`φ`, the fee share, income dispersion, and how much of the cohort is in school at each
gate).

The block works. Demand rises with gate pressure and with the credential's value, it is essentially zero at the
primary "pre-gate", every accounting identity holds, and — the check that matters most for honesty — with the
block switched **off** the panel is **byte-for-byte identical** to the frozen v1.2 panel (sha256 match). That
means v1.2 was not re-fitted, not even by one float.

**Four findings matter, and two of them are failures:**

1. **The HKG anchor is not reproduced (c4a FAIL).** The declared rule puts HKG-like demand at the
   upper-secondary gate at **34.0 %** in 2020, against a declared band of **75–95 %**. The reason is visible in
   the generator's own state: in v1.2 the upper-secondary gate is **not crowded** (queue ≈ 0.47 places per
   applicant, advance rate ≈ 0.90, rank factor 1.00, so `R ≈ 1.21`). To reach 75 % the same rule would need
   `R ≈ 2.98`, i.e. **2.46× the gate pressure this generator actually produces at that gate**. The pressure in
   this synthetic world sits at the *job* gate and, for poor systems, the *tertiary* gate — not at upper-secondary
   entry, which is where the 85 % figure was measured.
2. **The country ordering is not reproduced either (c4b FAIL), and it misses narrowly.** On the declared
   cohort-incidence statistic `D*`: HKG **0.329**, PHL **0.232**, KHM **0.120**. The PHL−KHM gap clears its
   threshold (+0.112 vs ≥0.05); the HKG−PHL gap is **+0.0967 vs the required ≥0.10** — a 3.3 % shortfall on the
   statistic. I did not widen the band, drop a country, or raise a coefficient to close it. It fails.
3. **One rule, no country-specific behaviour (c4c PASS).** Zero country-specific behavioural coefficients exist
   in the code; the audit that decides this is mechanical, and every country-varying quantity is in the declared
   input table and in `results/shadow_country_inputs_audit.csv`.
4. **The exposure channel, not the demand channel, is doing the ordering work — exactly as pre-declared.** KHM's
   *gate-conditional* rate at the tertiary gate (72 %) is far **above** PHL's (53 %) and HKG's (36 %), while KHM's
   *cohort incidence* is the lowest. That is the pattern `PRE_DECLARATIONS.md` §8 flagged as the ex-ante risk: "the
   ordering is carried mainly by cohort exposure `ν`, not by gate-conditional demand."

`c1`, `c2`, `c3`, `c5`, `c6` pass. `c4` fails as a whole, through `c4a` and `c4b`. **Both failures are findings
about this generator, not about any country.**

---

## 1. The frozen check table (scored exactly as `§8` states)

| check | verdict | key numbers |
|---|---|---|
| **c1** gate pressure | **PASS** | ∂D/∂lnR ≥ 0 in **619 scored cells** (min **+0.312**; 53 saturated cells NOT-SCORED, §6). R→2R at g2 in 2020: **+32.67 pp** HKG, **+30.93 pp** PHL, **+30.10 pp** KHM (threshold ≥ +10.0 pp). Numeric vs analytic max error **1.5e-09**. |
| **c2** expected returns | **PASS** | ∂D/∂ln(1+V) ≥ 0 in **619 scored cells** (min **+0.156**). V→1.25V (+25 % on φ) at g2 in 2020: **+4.26 pp** HKG, **+3.43 pp** PHL, **+2.90 pp** KHM (threshold ≥ +2.0 pp). |
| **c3** near-zero pre-gate (structural) | **PASS** | max D(g0) = **0.020503** (HKG 1979) ≤ 0.025; max D(g0)/D(g1) = **0.081622** (KHM 1975) ≤ 0.20; 168 country-years checked. |
| **c4a** HKG level anchor | **FAIL** | D(HKG,g2,2020) = **0.340215**, band **[0.75, 0.95]**; full 1970–2025 path **[0.3058, 0.4463]**. |
| **c4b** ordering on `D*` | **FAIL** | D*(2020): HKG **0.328708**, PHL **0.231984**, KHM **0.120131**. Gaps: HKG−PHL **+0.096724** (needs ≥ 0.10) **FAIL**; PHL−KHM **+0.111853** (needs ≥ 0.05) PASS. |
| **c4c** one rule, no country behaviour | **PASS** | 16 behavioural keys, all gate-indexed; **0** country-specific behavioural keys; **0** forbidden tokens in the behavioural functions; country inputs = `{phi, s, sigma, nu, oos_upper}` only. |
| **c4** (aggregate) | **FAIL** | c4a FAIL · c4b FAIL · c4c PASS → **FAIL** (not VOID: no country-specific behaviour exists). |
| **c5** identities | **PASS** | **0** violations in **840 country-gate-years**. p ∈ [0.005907, 0.9979]; D ∈ [0.012650, 0.995811]; π⁰,π¹,Π ∈ [0.01, 1]; Π ≥ π⁰ (min slack −1.1e−16, float round-off); S ≥ 0; max D*/exposure **0.4282**; max tutored/source-cohort at g1–g3 **0.4652**; max tutored/candidates at g4 **0.9958**; no NaN/inf; D(g0) < D(g1) in every year (max D(g0)−D(g1) = **−0.1993**). |
| **c6** no re-fit guard | **PASS** | Ablation sha256 **`14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac`** = frozen v1.2 panel sha256. Byte-identical. |

Row counts: panel **6 720** rows (30 countries × 56 years × 4 levels) and 89 columns; gate panel **840** rows
(3 types × 56 years × 5 gates); decomposition **840** rows; sensitivity **31** cells; country-input audit **32**
rows; checks 9 rows; detail 39 rows.

`PASS` means "this declared parameterisation can produce this pattern through the declared mechanism" —
nothing more.

---

## 2. `c4` in detail — the check that failed, and why

### 2.1 c4a: the level anchor is out of reach at the gate where it was measured

| quantity (HKG-like, g2, 2020) | value |
|---|---|
| `R` realised | **1.213963** (Q = 0.466, π⁰ = 0.903, κ = 1.000) |
| `D` realised | **0.340215** |
| `R` that would be needed for D = 0.75, all else fixed | **2.983275** |
| required / realised `R` | **2.457×** (required Δln R = **0.899**) |

This is a `NOT-SCORED` diagnostic computed **after** the scored run (`results/shadow_diagnostics_v1_3.json`,
`c4a_gap_diagnostic`), dated 2026-11-20; it explains the FAIL, it does not change it. `D` is strictly
increasing in `ln R`, so the "required R" is exact by bisection.

The mechanism is visible in §3: v1.2's upper-secondary gate has spare capacity (`Q ≈ 0.5`, `π⁰ ≈ 0.9`,
`κ = 1`), so the gate-pressure term contributes only `2.0 × 0.194 ≈ 0.39` logit. Demand at g2 is carried by the
credential-value term (`ln(1+V) ≈ 1.78` logit) and held down by the fee. **In this generator the horse race is
not at upper-secondary entry.** It is at the job gate (g4) and, for poor systems, at tertiary entry (g3).

That is a statement about the generator's gate machinery — the exact risk `DRY_RUN_PLAN.md` §7.1 flagged before
the run ("`R` is inert … report it — do not raise `b_Z` to fix it"). `b_Z` was not raised. In the pre-declared
sensitivity grid, **no cell reaches the band**: the maximum D(g2) anywhere on the grid is **0.551** (at
`b_V = 1.5`), still 20 pp below the floor of the band.

### 2.2 c4b: the ordering misses by 0.0033 on the first gap

| type | D(g1) 2020 | D(g2) 2020 | D(g3) 2020 | ν (g1,g2,g3) | `D*` 2020 |
|---|---|---|---|---|---|
| SYN_HKG_LIKE | 0.380988 | 0.340215 | 0.362164 | 0.10 / 0.62 / 0.22 | **0.328708** |
| SYN_PHL_LIKE | 0.292560 | 0.260596 | 0.530077 | 0.30 / 0.35 / 0.10 | **0.231984** |
| SYN_KHM_LIKE | 0.271987 | 0.227558 | 0.719620 | 0.28 / 0.13 / 0.02 | **0.120131** |

Read the middle of that table: **KHM's gate-conditional demand is the highest in the set at g3 (0.72)** — its
tertiary gate is genuinely tight (`R = 2.87`) and its fees are cheap — **yet its cohort incidence is the
lowest**, because only 43 % of its cohort is in school at gate age. PHL's g3 rate (0.53) also exceeds HKG's
(0.36). The ordering is produced by **who reaches the gate**, not by different demand intensity, which is the
module's declared design claim and the S1 note's stated risk.

The HKG−PHL gap of **0.0967** vs the required **0.10** is the closest call in the whole battery. It fails. It
passes in only **3 of the 31** pre-declared sensitivity cells (`b_V = 1.5`: 0.1766; `H = 30`: 0.1214;
`s_PHL = 0.07`: 0.1012) and fails in the other 28, including the central cell. The central-value result is the
scored result and it is a FAIL.

### 2.3 c4c: the rule really is one rule

The audit is mechanical (`shadow_code_audit()` in the code, output in `results/shadow_country_inputs_audit.csv`):
it scans the source of the five behavioural functions for country identifiers, checks that every behavioural key
in `SHADOW_BEHAV` is gate-indexed (`delta` keys are exactly `{0,1,2,3,4}`), and checks that the only country
input keys are `{phi, s, sigma, nu, oos_upper}`. All three conditions hold. **c4 is therefore FAIL, not VOID.**

### 2.4 The S1-note caveats, restated because they are part of the result

- **c4a is the only empirical anchor in the module**, and it is deliberately wide (±10 pp) because the 85 %
  figure is *senior-secondary only*, second-hand, and the source's own reporters say the surveys "should not be
  considered statistically robust". A FAIL against it is a statement that the declared rule cannot reproduce a
  weakly-measured level through the declared mechanism.
- **c4b is a DECLARED SYNTHETIC-REPRODUCTION CHECK on the model's own `D*`**, not a claim that the on-disk rates
  order the countries that way. The on-disk headline rates — HKG 85 % (senior secondary, second-hand), PHL 46.5 %
  (all basic education, single select sample), KHM 68.4 % (two-school Grade-9 case study) — are from different
  stages and sampling frames, and at face value they would put KHM **above** PHL. No country ordering is
  identifiable from them. This FAIL is about the generator's arithmetic, not about Cambodia or the Philippines.
- **c3 is structural, not an empirical prediction.** Observed primary-stage tutoring (PHL 23.8 %, KHM 41.3 %) is
  real in the record and is **out of this module's scope**; the module does not explain it and does not try to.

---

## 3. Where the gate pressure actually is (the generator's own state)

2020 values, `results/shadow_gates_v1_3.csv`:

| type | g1 R | g2 R | g3 R | g4 R | D(g1) | D(g2) | D(g3) | D(g4) |
|---|---|---|---|---|---|---|---|---|
| HKG-like | 1.352 | **1.214** | 1.161 | 1.027 | 0.381 | 0.340 | 0.362 | 0.575 |
| PHL-like | 1.319 | **1.214** | 1.769 | 1.034 | 0.293 | 0.261 | 0.530 | 0.480 |
| KHM-like | 1.385 | **1.254** | 2.871 | 8.040 | 0.272 | 0.228 | 0.720 | 0.984 |

Over 1970–2025 the ranges are: g1 `R` ∈ [1.216, 1.478]; g2 ∈ [1.152, 1.434]; g3 ∈ [1.137, 2.871];
g4 ∈ [1.009, 16.465]. Two consequences a reader should not miss:

1. **Upper-secondary entry (g2) is the *least* congested gate in the whole system** — it is the gate the HKG
   anchor is measured at, and the one where the model's own pressure is weakest. That is the single sentence
   that explains c4a.
2. **The job gate (g4) is where pressure concentrates**, and for the poor system it saturates (D = 0.996). The
   module reports g4 but `g4` never enters `D*` and its `Π` has no feedback hook (it is a labour gate, not a
   school gate).

---

## 4. Load-bearing parameters, and the one that looks load-bearing but is not

Pre-declared one-at-a-time grid, central values scored (`results/shadow_sensitivity_v1_3.csv`):

| parameter | range | D(HKG,g2,2020) | HKG−PHL gap | c4b |
|---|---|---|---|---|
| `b_V` credential return | 0.5 / **1.0** / 1.5 | 0.177 / **0.340** / 0.551 | 0.035 / **0.097** / 0.177 | FAIL / **FAIL** / PASS |
| `H` horizon | 10 / **20** / 30 | 0.234 / **0.340** / 0.420 | 0.061 / **0.097** / 0.121 | FAIL / **FAIL** / PASS |
| `b_Z` gate pressure | 1.2 / **2.0** / 2.8 | 0.307 / **0.340** / 0.375 | 0.098 / **0.097** / 0.095 | FAIL / **FAIL** / FAIL |
| `b_y` income | 0.3 / **0.6** / 0.9 | 0.346 / **0.340** / 0.337 | 0.095 / **0.097** / 0.097 | FAIL everywhere |
| `b_F` fee burden | 0.4 / **0.8** / 1.2 | 0.343 / **0.340** / 0.337 | 0.097 / **0.097** / 0.097 | FAIL everywhere |
| `b_Δ` lift coefficient | 1 / **2** / 3 | 0.334 / **0.340** / 0.347 | 0.095 / **0.097** / 0.098 | FAIL everywhere |
| `δ_g` lift fraction | 0.15 / **0.30** / 0.45 (uniform) | 0.334 / **0.340** / 0.346 | 0.095 / **0.096** / 0.097 | FAIL everywhere |
| `s_PHL` | 0.02 / **0.04** / 0.07 | 0.340 / **0.340** / 0.340 | 0.094 / **0.097** / 0.101 | FAIL / **FAIL** / PASS |
| `σ_c` (all three together) | low / **central** / high | 0.346 / **0.340** / 0.333 | 0.095 / **0.097** / 0.099 | FAIL everywhere |

**The level is carried by `b_V` and `H`, i.e. by the *credential-value* channel, not by the gate-pressure
channel.** Going from the low to the high end of the declared `b_V` range moves D(HKG,g2) by **+37 pp**; the
whole declared `b_Z` range moves it by **+7 pp**. That is the quantitative content of §2.1: in *this* generator,
gate pressure is not what makes tutoring demand large at the upper-secondary gate; the credential's value is.
`b_y`, `b_F`, `b_Δ` and `σ_c` are nearly inert on the level (≤ 1.5 pp across their full declared ranges).

**`δ_g` — the most exposed declared parameter — is nearly inert on the scored level and dominant for the
loop.** It has no on-disk anchor at all (`PARAMETERS.csv` B08). Across its full declared range (0.15 → 0.45):

- D(HKG,g2,2020) moves from **0.3342** to **0.3461** — **+1.19 pp**, i.e. the tutoring lift enters through
  `b_Δ·ln(1+Δπ) ≤ 0.4` logit and barely moves the level;
- the realised feedback multiplier `Π/π⁰` (g1–g3) moves from **1.506** to **2.686** — the loop scales almost
  linearly with `δ_g`.

So the parameter the module can least defend is the one that matters least for the scored demand levels and most
for the credential-inflation loop's magnitude. That ordering of exposures is itself worth knowing before anyone
uses the loop for anything.

Two sensitivity cells also flip *other* checks, reported as-is: `b_V = 0.5` and `H = 10` make **c2 FAIL** (the
+25 % φ experiment then moves D by less than 2 pp); `b_Z = 2.8` makes **c3 FAIL** (max D(g0) = 0.0300 > 0.025,
because a stronger pressure channel also inflates the pre-gate). No cell makes c4a pass.

---

## 5. The feedback loop is present, bounded, and small

`Π = (1−D)π⁰ + Dπ¹` replaces `π⁰` as the realised advance rate in the **next** year's pool at the level above
(`g1→lower-secondary`, `g2→upper-secondary`, `g3→tertiary`), and touches nothing else. The multiplier
`Π/π⁰` realised over 1970–2025 is at most **1.061** (HKG), **1.395** (PHL) and **1.878** (KHM) on the
hook-bearing gates; at 2020 the g1–g3 means are **1.005 / 1.043 / 1.295**. The hard bound
`|Π − π⁰| ≤ δ_g(1 − π⁰)` holds in every cell (c5).

The macro consequence is visible but tiny, because v1.2 caps eligibility pools at `1.05 × cohort`:

| host | 2020 GDPpc, block off → on | upper-secondary enrolment | tertiary enrolment |
|---|---|---|---|
| SYN28 (HKG-like) | 48 270.8 → 48 289.9 (**+0.040 %**) | +0.203 % | +0.372 % |
| SYN00 (PHL-like) | 6 993.9 → 7 002.2 (**+0.119 %**) | 0.000 % | +0.051 % |
| SYN18 (KHM-like) | 890.85 → 890.87 (**+0.002 %**) | 0.000 % | +0.001 % |

So the credential-inflation loop **does not bite hard in this generator**: the gate-pass channel is real but the
pipeline caps absorb it. A reader should treat "shadow education ratchets the queue" as *implemented and
bounded*, not as *demonstrated to matter* in v1.3. (These are `NOT-SCORED` diagnostics; they are also why the
scored panel's v1.2 columns differ slightly from the frozen v1.2 panel for the three host countries — the block
is on. With the block off they are identical, which is c6.)

---

## 6. Saturation, and what was not scored

- **53 of the 672** gate-year cells (7.9 %) fall outside the pre-declared "informative" range `D ∈ [0.05, 0.90]`
  and are `NOT-SCORED`, exactly as `DRY_RUN_PLAN.md` §7.2 pre-declares. **All 53 are KHM-like at the job gate
  (g4)**, where D ranges 0.606 → 0.996. No g1–g3 cell is saturated, so every cell that feeds `D*` is scored.
- `g0` is never scored as a gate (§2): its demand is the structural control for c3 only.
- `g4` is reported but enters neither `D*` nor the feedback.
- The KHM Grade-9 68.4 % case study, the PHL 46.5 % all-basic figure and the PHL 23.8 % / KHM 41.3 % primary
  figures are **`NOT-SCORED`** and out of scope. Observed primary-stage tutoring in particular is *not*
  explained by this module.

---

## 7. What this cannot claim (frozen, `PRE_DECLARATIONS.md` §13, copied verbatim)

> No evidence about Hong Kong, the Philippines, Cambodia or any country. No causal claim about returns, tutoring
> effects, or welfare. No identification of cross-country shadow incidence (LOOP_CLOSEOUT exclusion 3). No
> provider/fee/rent claim (exclusion 6). No claim that gate pressure and expected returns are separately
> identified — in the feedback loop they are collinear by construction (a tighter gate mechanically lowers `π⁰`
> and raises both `R` and `Δπ`), so the module reports their **joint** contribution and cannot attribute shares.
> No policy claim. A PASS means "this declared parameterisation can produce this pattern through the declared
> mechanism" — nothing more.

And, specifically for the two FAILs: they are **findings about the generator**, not about any school system.
A FAIL means "this declared rule, run on this generator's state, does not produce the pre-declared pattern". It
does **not** mean the pattern is false in the world, and it does **not** license a claim that shadow education
is absent, low, or mis-measured anywhere.

**Nothing about primary-stage tutoring.** c3 is a structural consistency check (no gate ⇒ no positional good),
not a prediction; observed primary tutoring is out of scope.

**Nothing about providers, hours, fees or rents.** `S` is a declared share of mean monthly household income — no
currency conversion, no provider block, no entry cost.

---

## 8. Reproducibility

- One `PCG64` stream, seed **20261120**, v1.2 draw order, shadow block draws nothing, floats `%.10g`.
- **Two clean runs into separate directories are byte-identical** (9/9 result files plus the manifest), recorded
  in [`results/determinism_note.md`](results/determinism_note.md).
- **c6**: with the block off, the ablation panel's sha256 is `14729c51…`, identical to the frozen v1.2 panel.
- The run re-hashes the frozen shadow predeclaration, the S1 note, the inherited v1.2 predeclaration, the local
  verbatim copy and `PARAMS.md`, and refuses to run on any mismatch.
- Re-run: `python code/sim_v1_3.py --out results --manifest RUN_MANIFEST.json` (≈ 8 s; `--smoke` for the
  ablation + distributions only, `--no-sensitivity` to skip the grid).
