# FINDINGS — EXP-6 PIPE-LOO

**Is the lower→upper one-stage transition ratio a system object, or eight Philippine pairs?**

**`LABEL: OBSERVED`** (the completion series) / **`DERIVED`** (every ratio, prediction, error, median, share).
Worker **PL** · 2026-11-20 · Council brief 022 (D122 #1), `SYNTHESIS_022.md` §6 EXP-6, rank #1.
Pre-declared before the run in `PRE_DECLARATIONS.md` (sha256 `97033df0c5693f50…`, sidecar
`PRE_DECLARATIONS.sha256`). **No threshold, bar, pairing rule or verdict string was changed after results.**

---

## 1. Verdict — `PREDICTIVE` (3 of 4 countries pass)

The declared rule is **per country: `PASS` iff median |LOO error| ≤ 3.0 pp AND ≥75% of pairs within ±5 pp**;
**`PREDICTIVE` iff ≥3/4 countries pass, `NOT PREDICTIVE` iff ≤2/4.** Result, on **all 43 pairs**:

| country | n pairs | median \|LOO error\| | % within ±5 pp | bar T1 (≤3.0) | bar T2 (≥75%) | verdict |
|---|---|---|---|---|---|---|
| PHL Philippines | 8 | **1.50 pp** | **87.5%** (7/8) | pass | pass | **PASS** |
| KOR Korea | 19 | **0.48 pp** | **89.5%** (17/19) | pass | pass | **PASS** |
| KHM Cambodia | 11 | **2.17 pp** | **90.9%** (10/11) | pass | pass | **PASS** |
| CHN China | 5 | **14.48 pp** | **0.0%** (0/5) | fail | fail | **FAIL** |
| **overall** | **43** | (1.01 pp pooled, descriptive) | (79.1% pooled, descriptive) | | | **PREDICTIVE** |

**Declared non-entrants, recorded not imputed:** **HKG and JPN have zero completion pairs** — the frozen file carries
no `completion_lower_secondary` or `completion_upper_secondary` rows for either (all their rows are GER/NER/OOS/
gross-intake/population). They cannot enter; no proxy numerator was substituted (D118: exactly one admissible
numerator), nothing interpolated.

**Reproduction of the brief's pre-freeze calibration.** The block's item 5 recorded PHL 1.50 (7/8), KOR 0.48 (17/19),
KHM 2.17 (10/11), CHN 14.48 (0/5) as **calibration of the bars, not a result**. This run recomputes all four from
disk and reproduces them **exactly, to 2 dp and to the pair count**, and builds exactly **43 pairs (8/19/11/5)**.
That is evidence the pairing rule and the LOO construction match the Council's intent — it is **not** evidence for or
against the hypothesis, and it was not used to choose any rule.

---

## 2. What was actually tested

For each country, every observed **upper**-secondary year `t` was paired with lower-secondary completion at `t−3`
(exact), else the nearest observation within **±1 y** (ties → earlier year), else dropped. Then, for each pair, the
country's **other** pairs' median ratio κ̂ was multiplied by **that pair's own** lower value to predict its upper
value. A genuine system object has to predict **its own held-out years** from a ratio estimated on its **other**
years. Nothing is estimated across countries, so nothing about country similarity is assumed; and no pair is ever
scored by a κ that used its own ratio.

**What the pairing rule did with the data** (16 of 59 upper years dropped, all for the declared reason `no lower
observation within ±1 y of t−3`): PHL dropped 3 (1999, 2000, 2022), KOR 5 (2000–2004), KHM 7 (1996, 1997, 2001, 2005,
2015, 2019, 2020), CHN 1 (2010). Because of the ±1 y tolerance, the **realised lag is not always 3 years** — it is 2,
3 or 4 years depending on the pair (recorded per pair in `PIPE_LOO_PAIRS.csv`, column `year_offset_used`). That is the
declared rule working as written, and it is a real source of prediction error in KHM and CHN.

---

## 3. So: is the transition ratio a system object?

**Yes, for three of the four systems — and the exception is the informative one.** Read plainly:

- **PHL, KOR, KHM:** a single number per system — the median of that system's own historical ratios — predicted
  held-out years within a few pp. The ratio is not an artefact of eight PHL pairs; it also holds in a second East
  Asian system (KOR, 19 pairs) and in a low-completion Southeast Asian system (KHM, 11 pairs). That is a genuinely
  out-of-sample result, and it is the first time the "pipeline" object has been tested this way.
- **CHN: the object fails, and fails *systematically*.** All five residuals are large and they change sign in a
  pattern: **+14.5, +8.4, +7.7, −15.6, −22.4 pp**. Under-prediction early, over-prediction late, because CHN's ratio
  **trends upward across its own pairs — 0.645, 0.717, 0.722, 0.908, 0.966** — while its lower-secondary completion
  sits almost flat (82.6–95.7). A constant-κ predictor is the wrong shape for that system: during rapid upper-secondary
  expansion the "transition ratio" is not a constant, it is a **trajectory**.

That pattern, not the 3/4 count, is the finding: **the ratio is a within-system near-constant in systems that are not
in the middle of an upper-secondary expansion, and it is not a constant in the one system that is.** The coefficient
is also **system-specific, not universal**: the four medians are **PHL 0.949, KOR 0.990, KHM 0.595, CHN 0.722** — a
0.395 spread. On a lower value of 40–90 pp that spread is 16–35 pp, so a single pooled κ could not serve these
systems simultaneously. Whatever "the pipeline" is, its coefficient is set per system.

---

## 4. What this does and does not change

**The κ-link.** Under the pre-declared `PREDICTIVE` branch, the ratio becomes a **declared per-system input — never
fitted**: κ = **0.949 PHL, 0.990 KOR, 0.595 KHM, 0.722 CHN** (each the median of that system's own pairs, reported as
`DERIVED`). This confirms the direction of EXP-7's declared link — but it **corrects its scope**: a single global
κ = 0.949 is a PHL number being applied to systems whose own coefficients differ by up to 0.40. The model should carry
**κ per system**, and the ceiling question becomes the brief's own question: **what sets κ?** That question is *not*
answered here and no mechanism is proposed.

**"The ceiling is a pipeline."** The D115 reclassification is **not** downgraded to a description of PHL's pairs — the
`NOT PREDICTIVE` branch did not fire, so that downgrade is not triggered. But the claim has to be stated at its true
strength: the one-stage transition ratio is a **system-specific, approximately stationary coefficient** that predicts
its own system's held-out years in 3 of 4 systems, **and fails in the system undergoing rapid expansion**. It is not a
constant of schooling, it is not universal across systems, and it is not a mechanism.

**D63 stays `UNABLE` as to cause.** The verdict changes the *status of the object*, not the causal question. Nothing
here says what sets the ratio, what moves it, or which way anything runs. No causal claim, no direction claim, no C1–C4
reopening, no re-score of EXP-1 (same pairing rule, different estimand: out-of-sample prediction, not in-band share).
The phase verdict (D76/D77), `m = 1.10` and v1.2's scope are untouched.

---

## 5. Honest limits — read these with the verdict

1. **43 pairs, 4 systems.** This is a small, non-random sample of school systems, and 16 upper years were dropped by
   the declared pairing rule. The verdict rule was declared for exactly this sample and sits at its **exact boundary:
   3/4 with 3 required. One country flipping flips the verdict.** There is no headroom, and `PREDICTIVE` here should
   not be read as robust.
2. **KOR's pass is close to an arithmetic identity at saturation.** KOR's lower series is pinned at 99.90–100.00 and 17
   of its 19 upper values sit in 97.3–99.5, so a wide neighbourhood of κ predicts within ±5 pp. The pass is real under
   the declared bar, but it is weak evidence for a *mechanism*; it mainly shows the ratio is ~1 where both stages are
   full. Its two misses are the only two single-year dips in the series (93.16 in 2006, 83.04 in 2008) — i.e. the
   bar is informative only where the series actually moves. The systems where a ±5 pp band is genuinely informative
   are **PHL and KHM** — and, negatively, **CHN**.
3. **KHM's median is carried by one decisive outlier.** The t=2000 pair (ratio 0.139, error 14.5 pp) uses the 1996
   lower value — a collapse-year observation, at a realised lag of 4 years. KHM still passes (10/11 in band), but its
   median is not comfortable.
4. **PHL's pass is carried by 2003–2017.** Six of PHL's eight pairs have upper years in 2003–2017; the declared
   descriptive screen (S3, `DESCRIPTIVE-NOT-VERDICT`, no threshold applied, no verdict drawn from it) gives that subset
   a median |LOO error| of **1.37 pp, 5/6 within ±5 pp** — not weaker than the full set. The **two** late pairs
   (2023, 2024) are both in band (+4.86, +1.77 pp). But they are **two, not three**: **upper 2022 is dropped by the
   pairing rule** (no lower observation within ±1 y of 2019), and 2022 is the largest single-year move in PHL's upper
   series (76.43 → 68.28). So part of PHL's recent turbulence lies **outside** the test by construction, and the
   PHL verdict rests on pairs that are mostly a decade or more old.
5. **Measurement caveats (D118).** Completion only, one admissible numerator, no GER substitution, no interpolation;
   UIS completion values are survey/model-derived and the PHL lower series' recent annualised deltas
   (**3.27, 4.28, 3.97 pp/yr in 2021–2024**, against a 1999–2017 pace mostly under 2.5) are far above its own history.
   The most recent years are both the least stable part of the measurement and the part any forward claim would lean
   on. The declared S2 screen reports mean **2.25 pp/yr** and sample SD **2.14 pp/yr** (ddof=1). The brief's
   "SD 2.04" is the **population** SD (ddof=0) of the same ten deltas — same data, different denominator convention,
   **non-verdict-bearing either way**; no recomputation was substituted for a threshold.
6. **The two systems with no data are the ones that would test the saturation caveat.** HKG and JPN are high-completion
   systems with **zero** completion pairs; they cannot enter. So the sample speaks to the saturation regime only
   through KOR, which weakens limit 2's converse as much as the pass itself.
7. **The ±1 y tolerance blurs the "one-stage" claim.** Realised lags run 2–4 years, and the pooled error therefore
   mixes genuine ratio instability with lag mismatch. Declared in advance, reported per pair, not adjusted after the
   fact.

---

## 6. What would change the answer (not a commitment)

More systems — especially complete series for high-completion systems, so saturation is tested rather than assumed;
a declared test of **non-stationarity** (a trend in the ratio) as a separate estimand, since CHN shows that the failure
mode is trend, not noise; and pairs at longer, unblurred lags. None of this is proposed as a new experiment here, and
nothing downstream should treat this experiment as a licence beyond §4.

---

## 7. Reproduction

```
python code/run_pipe_loo.py                       # writes results/
python code/run_pipe_loo.py --outdir results/determinism_run2
python code/make_manifest.py
```

Deterministic, no RNG, no network, read-only inputs, nothing written outside this directory. **Two runs are
byte-identical** on all four artifacts:

| file | sha256 (run 1 = run 2) |
|---|---|
| `results/PIPE_LOO_PAIRS.csv` | `692ca7c01b8b3a7105e84339a87f97029b6a50e277681bdcdbe0f02bf027600f` |
| `results/PIPE_LOO_RESULTS.csv` | `7c4faa427f48485393e58a234d1f1cbd2302bbfc11e81d55454cc56b5e5eff6c` |
| `results/PIPE_LOO_SECONDARY.csv` | `0f30229335734987b8feaf61f74675cdc47d4ee0206314a7eed8841d98c1fdb2` |
| `results/console.txt` | `b21706b4218e23243304aba6254dffc5286194c493b853f15b2307fb3a588fe3` |

The script refuses to run if `PRE_DECLARATIONS.md` or either frozen input changes hash. Inputs:
`UNIVERSALIZATION_SERIES.csv` `85bc8693…737ddb`, `SYNTHESIS_022.md` `9508dd55…7c109b`.
