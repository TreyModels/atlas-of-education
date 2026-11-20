# PRE-DECLARATIONS — EXP-6 PIPE-LOO

**`LABEL: OBSERVED` for the observed completion series; `DERIVED` for every ratio, prediction, error, median and
share computed from it.** No synthetic object enters this experiment.
Experiment: **EXP-6 PIPE-LOO** from Council brief 022 (D122 #1), `SYNTHESIS_022.md` §6 EXP-6, rank **#1**.
Worker **PL** · created 2026-11-20 (Asia/Shanghai) · **written before any run**.

This file is frozen on creation: its sha256 is written to `PRE_DECLARATIONS.sha256` **before**
`code/run_pipe_loo.py` executes, and the script refuses to run unless the on-disk file's sha256 equals the constant
embedded in it. **No threshold, bar, pairing rule, country set, LOO construction, share denominator or verdict rule in
this file may be changed after results are seen.** If any declared step cannot be implemented exactly as written, it
is **reported as not implemented**, not silently approximated.

**This is a measurement audit of an observed series. It makes no causal claim and no direction claim.** The
transition ratio is **not asserted to cause anything**; it is tested only as a *predictive* object. **No C1–C4
reopening.** This experiment does **not re-score EXP-1**: it reuses EXP-1's pairing rule but has a different
estimand (**out-of-sample prediction**, not in-band share). D63 remains `UNABLE as to cause` either way.

---

## 0. Scope and question

**Question (first-order).** Is the one-stage transition ratio `upper_t / lower_{t−3}` — the object the batch renamed
"the ceiling-pipeline" (D115/D118) — a **stable, predictive property of a school system**, or an **artefact of eight
Philippine survey pairs**?

**Operational form.** Purely out-of-sample and within-country: for each pair, predict the observed upper-secondary
completion rate from the country's *other* pairs' median ratio applied to that pair's own lower-secondary completion
rate. A system object must predict **its own held-out years** from a ratio estimated on its **other years**. Nothing
is estimated across countries, so nothing about country similarity is assumed.

**Data used.** `10_massification/data/UNIVERSALIZATION_SERIES.csv`, indicators
`completion_upper_secondary` and `completion_lower_secondary`, `status=observed`, for **PHL, KOR, KHM, CHN**.
**No web, no external data, no writes outside this directory, no DATA ASK.**

**Declared non-entrants (recorded, never imputed).** **HKG and JPN have zero completion pairs** — the frozen file
carries **no** `completion_lower_secondary` or `completion_upper_secondary` rows for either ISO3 (all their rows are
GER/NER/OOS/gross-intake/population indicators). They **cannot enter** and are reported as `NON-ENTRANT` with
`n_pairs = 0`. No proxy numerator, no substitution of GER for completion (D118: exactly one admissible numerator),
no imputation, no interpolation.

---

## 1. Frozen extract from `SYNTHESIS_022.md` §6 EXP-6 — **verbatim**

Quoted from `08_council/brief_022/SYNTHESIS_022.md`, §6 "EXP-6 — **PIPE-LOO**", heading and items 1–7,
character-for-character (line breaks preserved as in the source):

> ### EXP-6 — **PIPE-LOO**: is the lower→upper transition ratio a system object? (rank **#1**)
>
> 1. **First-order link (schooling + cohort flows, with measurement).** Whether the thing the batch renamed "the ceiling"
>    — the one-stage transition ratio — is a stable, predictive property of a school system or an artefact of eight
>    Philippine survey pairs.
> 2. **What changes if positive vs negative.** **Positive** (ratio predictive in ≥3/4 systems) → the transition ratio is
>    the object; the model carries it as a declared link with a **system input** (κ per system, declared, never fitted);
>    the ceiling question becomes "what sets κ?". **Negative** (≤2/4) → the ratio is not an object; the pipeline
>    reclassification is downgraded to a description of PHL's pairs; D63 returns to `UNABLE` **with no object**, and the
>    programme's next model line has no target.
> 3. **Why it is not a niche.** D63 is the phase's single open object and D115 is this batch's headline. A reader of the
>    first-order question is entitled to know whether "the ceiling is a pipeline" is a statement about systems or about
>    8 pairs — and the answer decides what the model is built to reproduce.
> 4. **Data on disk.** `10_massification/data/UNIVERSALIZATION_SERIES.csv` (`completion_upper_secondary`,
>    `completion_lower_secondary`, `status=observed`) for PHL/KOR/KHM/CHN — **43 pairs** (8/19/11/5), pairing rule as
>    EXP-1 (t−3 exact, else nearest within ±1 y, else drop). **No DATA ASK.** Declared limitation: **HKG and JPN have zero
>    completion pairs** and cannot enter.
> 5. **Threshold + falsifier (re-derived before freeze).** Per country, predictive iff **median |LOO error| ≤ 3.0 pp**
>    **and** **≥75%** of pairs within **±5 pp** (LOO: predict `upper_t` as the median of the *other* pairs × `lower_{t−3}`).
>    `PREDICTIVE` iff **≥3/4** countries pass; `NOT PREDICTIVE` if **≤2/4**. Re-derived structure (**pre-freeze calibration
>    of the bars, not a result** — the run must report all 43 pairs): PHL 1.50 (7/8), KOR 0.48
>    (17/19), KHM 2.17 (10/11), CHN 14.48 (0/5). **Falsifier:** ≤2/4 → the object fails and no κ is declared anywhere.
>    Secondary leg (declared, non-verdict-bearing): per-country pair count and annualised-change screen (PHL lower
>    annualised deltas 6.17 / 0.26 / 0.47 / 1.57 / 0.06 / 2.50 / −0.09 / 3.27 / 4.28 / 3.97, mean 2.25, SD 2.04) so the
>    Lead can see how much of the object rests on three 2022–2024 observations.
> 6. **Closed-claim check.** No C1–C4 reopening. Does **not** re-score EXP-1: same pairing rule, different estimand
>    (out-of-sample prediction, not in-band share). No direction claim (the ratio is not asserted to cause anything).
> 7. **Cost / rank.** **Small** (one deterministic script, read-only). **Rank #1.**

**Frozen status of the calibration figures in item 5.** The parenthetical `PHL 1.50 (7/8), KOR 0.48 (17/19), KHM 2.17
(10/11), CHN 14.48 (0/5)` is labelled by the brief itself as **pre-freeze calibration of the bars, not a result**. This
run recomputes it from disk and reports both the recomputed value and the brief's value side by side in
`results/PIPE_LOO_RESULTS.csv` (`brief_calibration` column, recorded as text). **Agreement is reported, never used to
choose a rule.** If they disagree, the disagreement is reported and the recomputed value stands, with the cause stated.

---

## 2. Pairing rule (as EXP-1, re-declared exactly)

For each country with upper/lower series `upper[t]` and `lower[y]` (`status=observed` only, no interpolation):

1. For every observed **upper** year `t`, set `target = t − 3`.
2. If `lower[target]` exists → **exact pair** at `t−3` (flag `EXACT`).
3. Else candidates = observed **lower** years within `±1 y` of `target`. If none → **drop the upper year** and record
   it in `PAIRING_LOG` as `DROPPED_NO_LOWER_WITHIN_1Y`.
4. Else use the nearest candidate; **ties are broken toward the earlier year** — `min(cands, key=(|y − target|, y))`,
   the exact convention implemented in EXP-1's `build_pairs()` (`ceil_attrib_2026-11-20/code/run_ceil_attrib.py`,
   line 216). Flag `NEAREST_1Y` with the realised offset `lower_year − target` in years.
5. The pair's ratio is `ratio = upper[t] / lower[lower_year]`. Both inputs are **pp**-scaled completion percentages
   (`unit = percent`), so ratios are dimensionless and LOO errors are in **percentage points (pp)**.

Pairing is applied **per country and independently**; no pair crosses a country boundary. **Every** upper year is
either paired or logged as dropped, and **all 43 resulting pairs are reported** — no subset is ever substituted for
the full set, and no pair is removed after its error is seen.

---

## 3. LOO construction (leave-one-out, within country)

For country `c` with `n_c` pairs, for each pair `i`:

- **κ̂_(c,−i)** = **median** of the ratios of the **other** `n_c − 1` pairs of country `c` (sample median; for even
  counts the mean of the two central order statistics). **Never fitted**, never cross-country, never shrunk, never
  weighted.
- **prediction_i** = κ̂_(c,−i) × `lower_i`, where `lower_i` is that pair's **own** observed lower-secondary completion
  value at the year actually used by the pairing rule.
- **error_i** = `prediction_i − upper_i` (**signed**, pp) and **abs_error_i** = `|error_i|`.

A country's pairs are **not** removed from any other country's LOO; only same-country pairs are held out. If a country
had `n_c < 2` pairs its LOO would be undefined; that case does not arise here (counts 8/19/11/5) and is declared
`N/A`-by-rule rather than silently dropped.

---

## 4. Thresholds and verdict vocabulary (fixed now, not changed later)

**Per-country `predictive` iff BOTH:**

- **(T1)** `median_c(abs_error) ≤ 3.0 pp`, **and**
- **(T2)** `share_c(|error| ≤ 5.0 pp) ≥ 75.0%` of that country's pairs.

Denominators are the country's **own** pair count `n_c` (8, 19, 11, 5); `within ±5 pp` is inclusive at 5.0
(`abs_error ≤ 5.0`). A country failing **either** bar is `FAIL`.

**Overall verdict (exhaustive over the only possible pass counts with 4 countries):**

| countries passing | verdict |
|---|---|
| **4/4** | `PREDICTIVE` |
| **3/4** | `PREDICTIVE` (the brief's explicit "3/4 pass = PREDICTIVE") |
| **2/4** | `NOT PREDICTIVE` |
| **1/4** | `NOT PREDICTIVE` |
| **0/4** | `NOT PREDICTIVE` |

No other verdict strings exist. There is **no `MIXED`, no `PARTIAL`, no `INCONCLUSIVE`**. **`PREDICTIVE` is not
softened to "suggestive" and `NOT PREDICTIVE` is not softened to "inconclusive"** after the fact. The verdict is
mechanical from the four per-country booleans.

**Consequence mapping (declared before results, taken from the brief verbatim):**

- **`PREDICTIVE`** → the transition ratio **is** the object: per-system **κ = the country's median ratio** becomes a
  **declared input** (never fitted), and the ceiling question becomes "what sets κ?".
- **`NOT PREDICTIVE`** → the ratio **is not** an object: the pipeline reclassification is downgraded to a
  **description of PHL's pairs**; **D63 returns to `UNABLE` with no object** and **no κ is declared anywhere**.

---

## 5. Secondary leg — declared, **non-verdict-bearing**

Computed and reported, but **never** entering the verdict, never re-opening a threshold, never used to re-rank a
country:

- **S1** — per-country pair count `n_c`, and the count of upper years dropped by the pairing rule; plus the two
  declared non-entrants with `n_pairs = 0`.
- **S2** — **PHL annualised lower-secondary completion deltas**: for each consecutive pair of observed PHL lower years
  `(y_from, y_to)`, `delta_annual = (lower[y_to] − lower[y_from]) / (y_to − y_from)` in pp/year; then the **mean** and
  **sample SD (ddof = 1)** over those deltas. This is the brief's "how much rests on three 2022–2024 observations".
- **S3** — **PHL pair-year composition descriptor**: how many of PHL's 8 pairs have upper years in **2022–2024** vs
  **2003–2017**, and the same LOO statistics recomputed on the **2003–2017 subset only**, reported as
  `DESCRIPTIVE-NOT-VERDICT`. **No threshold is applied to S3 and no verdict is derived from it**; it exists so the
  reader can see whether the PHL pass is carried by the three late pairs. Labelling it `DESCRIPTIVE-NOT-VERDICT` is
  part of the declaration, so it cannot be promoted after results.

**κ per country** (the country's median ratio over all its pairs) is reported in the results as `DERIVED`, descriptive,
**not fitted and not causal**. If the verdict is `PREDICTIVE`, these medians are the declared per-system inputs; if the
verdict is `NOT PREDICTIVE`, they are reported as descriptive artefacts and **no κ is declared**.

---

## 6. What this experiment does NOT claim

- **No causal claim.** The ratio is not asserted to cause, constrain or produce anything. "Predictive" is used in the
  narrow out-of-sample sense of §3, not as a claim about mechanism.
- **No direction claim.** No statement about the direction of causation, of policy effect, or of time's arrow.
- **No C1–C4 reopening**, no re-score of EXP-1/EXP-2/EXP-3, no A3-S re-check, no generator re-run, no WT/DT cell
  re-run, no re-fit of any parameter, no tuning of `±1 y`, `3.0 pp`, `±5 pp` or `75%`.
- **No new verdict on D63.** D63 stays exactly where it stands: `UNABLE as to cause`. `PREDICTIVE` does **not** make
  D63 `ANSWERED`; it makes the ratio a **declared input**, which is a modelling convenience, not a finding about
  causes. `NOT PREDICTIVE` returns D63 to `UNABLE` **with no object**.
- **No claim about V1/V2, the phase verdict (D76/D77), `m = 1.10`, or v1.2's scope.** Untouched.
- **No measure substitution.** Completion only; GER is not a substitute numerator (D118).

---

## 7. No-threshold-change rule and closed claims

**The bars in §4 are frozen on creation of this file.** After results are seen, **no threshold, share denominator,
pairing rule, tie-break, LOO definition, country set, verdict string or consequence mapping may be changed**, and **no
pair may be dropped, added, re-weighted or re-flagged**. If the result surprises the worker, the result stands and the
surprise is written in `FINDINGS.md` as an observation **about the result**, never as a licence to re-cut it.

**No re-fit, no re-parameterisation, no second estimand.** A single pass of a single deterministic script produces
every number reported. No RNG anywhere: the script contains no random number generator, no seed and no sampling.

**Closed claims.** This experiment does not reopen C1, C2, C3 or C4; it does not re-score EXP-1 (different estimand:
out-of-sample prediction, not in-band share); it reuses EXP-1's **pairing rule** only, as the brief directs. It does
not re-run CEIL-ATTRIB's ablations and does not re-test the in-band `PIPELINE-CONSISTENT` claim.

---

## 8. Outputs (declared)

1. `results/PIPE_LOO_PAIRS.csv` — **all 43 pairs**, one row each: country, upper year, lower year used, pairing flag,
   realised year offset, both values, ratio, the LOO κ̂ used for that pair, prediction, signed error, absolute error,
   within-±5 pp flag.
2. `results/PIPE_LOO_RESULTS.csv` — per-country: `n_pairs`, `n_within_5pp`, `median abs LOO error`, `% within ±5 pp`,
   the two bar evaluations, `pass/fail`, κ median; plus the **overall row** with `n_countries_pass`,
   `n_countries_total` and the verdict; plus the two `NON-ENTRANT` rows.
3. `results/PIPE_LOO_SECONDARY.csv` — the S1/S2/S3 screens of §5, each labelled non-verdict-bearing.
4. `results/console.txt` — the full console transcript of the run.
5. `results/determinism_run2/` — a byte-identical second run of the same four result files.
6. `FINDINGS.md`, `RUN_MANIFEST.json`, `SHA256SUMS.txt`.

---

## 9. Implementation guards

- The script **refuses to run** if `PRE_DECLARATIONS.md`'s sha256 differs from the embedded constant, or if any frozen
  input's sha256 differs from the value recorded in §1/§2's manifest entry — a changed input is a **reported block**,
  not a silent recomputation.
- Inputs are opened **read-only**; nothing outside this directory is written or modified.
- **Two consecutive runs must be byte-identical**; otherwise determinism is reported as failed.
- No network access, no RNG, no clock-dependent output (the run timestamp is the only non-deterministic field and is
  written to the manifest/comments only, never into a result CSV).
