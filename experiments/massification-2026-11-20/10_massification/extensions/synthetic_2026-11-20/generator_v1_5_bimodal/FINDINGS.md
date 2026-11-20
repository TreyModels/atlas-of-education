# FINDINGS — v1.5 **BIMODAL-GATE** (Amendment A5), built and run to the frozen predeclaration

**`LABEL: SYNTHETIC` for every generator object; `LABEL: OBSERVED` for every PHL series; `LABEL: DECLARED` for every
behavioural assumption. This is a synthetic experiment. It is not evidence about the Philippines or any country, it
licenses no causal claim and no direction claim, it re-opens no C1–C4 claim, and it fits nothing to the known PHL
outcome.**

- **Predeclaration used:** `PRE_DECLARATIONS.md`, sha256
  `7178e3d2ee2e367cd7dbb0619f2031305ff446978a43aab9e1f6caefb07ca97f` — verified before the run and re-verified
  after; byte-identical to the frozen original. `PARAMETERS.csv` (`72327cf7…`), `DESIGN.md` (`db21055b…`) and
  `DRY_RUN_PLAN.md` (`46603905…`) likewise unchanged.
- **Base instrument:** frozen `generator_v1_3` code `70ae8f0e…`, panel `47d4b082…`, copied byte-for-byte to
  `code/base_v1_3_sim.py`; **no file outside `generator_v1_5_bimodal/` was written**.
- **Verdict string:** `a=MIXED; b=FAIL; c=MIXED; d=FAIL; e=MIXED; **ALL=FAIL**`
  with `BASELINE-GUARD-PASS`, `KAPPA-GUARD-FAIL`, `FROZEN-FILE-GUARD-PASS`, `DETERMINISM-PASS`.
- **Scope note carried by every level statement (D119):** v1.3/v1.2 levels are a **2021–2024 placement**, 24–37 pp
  low before 2021, 9/33 within ±5 pp (EXP-7 leg (a) = `ENDPOINT-ONLY`). Every level number below is readable only as
  a **2022–2024 placement** statement.

---

## 1. The answer in two sentences

**Coexistence.** Yes — the declared two-tier structure *can* hold untaken low-cost places and a contested high gate in
the **same synthetic country-year**: for `SYN00_PHL_LIKE` in **all 15** scored years 2010–2024 the upper-secondary
Tier O unfilled share is **0.648–0.932** while the Tier H queue ratio is **1.29–1.93** and the credentialed-job
absorption `p₄` is **≈0.25**, i.e. the model class represents the phenomenon the single-gate stack could not.

**But the same run fails the level pattern and two of its guard formalities.** The declared Tier O quality
(`q_O_mult = 0.55`) drives Tier O survival to **≈0.48–0.51 per level** across 60–85 % of all places, so primary
completion falls to **51.6 pp** (never reaching the 90 pp bar) and upper-secondary to **33.7 pp** — **(b) = FAIL, a
collapse, not the predeclared stall** — and the κ link, while arithmetically exact (20/53 → 0/53 violations), lands
at an upper 2024 of **55.66 pp**, **8.31 pp below** the 63.97 pp κ-implied ceiling, because that ceiling bounds the
*entry cohort* and upper survival is 0.870.

---

## 2. Checks table (frozen thresholds, arm A11 unless stated)

| check | verdict | key numbers | threshold as frozen |
|---|---|---|---|
| **(a)** untaken Tier O places **and** Tier H queues, same country-year | **MIXED** | unfilled ≥ 0.10 in **18/30** cells; queue ratio ≥ 1.10 in **30/30**; both in the **15/15** years; `p₄ ≤ 0.50` in **15/15**; `same_level` = **15** (A11), **15** (A01), **0** (A00) | (a-i) ≥15/30, (a-ii) ≥15/30, (a-iii) ≥8/15 + p₄, (a-iv) A01 = 0 ∧ A11 ≥ 8 |
| **(b)** primary near-universal while upper stalls | **FAIL** | primary first sustained ≥ 90: **never**; primary 2024 **51.63**; upper 2024 **33.68**; upper < 90 in every year ≤ 2024: **true** | (b-i) first ≥90 ∈ [2014,2020] ∧ primary 2024 ≥ 92; (b-ii) upper 2024 ∈ [55,85]; (b-iii) ∈ [73,77] |
| **(c)** shadow demand at the high gates, not the open tier | **MIXED** | `D_H/D_O` min **33.2**; max `D_O` **0.0077**; high-gate R→2R gap **+31.13 pp**; open-tier gap **+2.16 pp** | (c-i) ≥ 5.0; (c-ii) ≤ 0.025; (c-iii) high ≥ +10.0 **and** open ≤ +1.0 pp |
| **(d)** ceiling from quality / outside option / sorting, no free taste | **FAIL** | T-AUD-1/2 hits **0**; `w_work_free = 0`; slack ≥ 0 in **53/53** cells; cap **non-binding 0/53**; child wage +10 % → **+1.081 pp** (wrong sign); Tier O quality −20 % → unfilled **+11.22 pp** | (d-i) 0 hits; (d-ii) slack ∧ non-binding ≥5/53; (d-iii) ≤ −2.0 pp; (d-iv) ≥ +5.0 pp |
| **(e)** no-re-fit guards | **MIXED** | A00 panel sha **`47d4b082…`** (byte-identical, plus an independent cross-check through the frozen base code); κ violations **20/53 → 0/53**; non-upper rows **cell-identical 180/5 040**; upper rows differing **1 620/1 680**; frozen inputs **20/20**; determinism **14/14** byte-identical | (e-i) exact sha; (e-ii) cell identity ∧ upper-diff-only-where-cap-binds ∧ 0/53; (e-iii) frozen files; (e-iv) determinism |

**No frozen branch covers "only the contrast leg fails".** (a-i), (a-ii) and (a-iii) all hold; only the (a-iv) A01 leg
fails (see §5.1). The frozen vocabulary has no branch for that combination, so `MIXED` is reported with the failing leg
named, as §7 requires ("the subset must be named in the report"). The representation claim itself — the thing the user
asked for — holds in every scored year.

---

## 3. The coexistence tabulation (the actual object)

`results/unfilled_vs_queue.csv`, same country (`SYN00_PHL_LIKE`), same year, both levels:

| year | Tier O unfilled share, lower | upper | Tier H queue ratio, lower | upper | `p₄` job gate | both levels coexist |
|---|---|---|---|---|---|---|
| 2010 | 0.000 | 0.907 | 3.98 | 1.29 | 0.237 | no (lower filled) |
| 2015 | 0.000 | 0.892 | 3.41 | 1.32 | 0.252 | no |
| 2019 | 0.008 | 0.832 | 3.20 | 1.49 | 0.255 | no |
| 2022 | **0.102** | **0.709** | 3.39 | 1.75 | 0.251 | **yes** |
| 2023 | **0.138** | **0.692** | 3.30 | 1.61 | 0.250 | **yes** |
| 2024 | **0.178** | **0.648** | 3.19 | 1.93 | 0.250 | **yes** |

At **upper secondary** the two facts hold together in **every** year of the window: 65–93 % of the open-access places
are unfilled *while* 1.3–1.9 candidates queue per high-gate place. At **lower secondary** the open tier fills until
2019 and only begins to leave places untaken from 2022. **This is a representation statement, not an empirical one**:
with `h_share` declared, part of the coexistence is arithmetical (PRE_DECLARATIONS §9), and the diagnostic content is
the magnitude, its monotone response to the `h_share` grid (mean unfilled 0.464 → 0.436 → 0.434 as `h_share` rises by
0.10 steps), and the **exact zero** in the single-gate arm A00.

---

## 4. Where the ceiling actually comes from — and what that costs (d)

The predeclared question was whether the pattern is carried by **tier quality, the outside option and sorting** rather
than by the removed taste parameter. The answer is **tier quality alone**, and it overshoots into a collapse:

- `w_work_free = 0` in both tiers and in the outside option, and the T-AUD-1/2 source audit finds **0** country-specific
  values, **0** level-targeted utility constants and one declared vector per parameter for all 30 countries. The taste
  shim is not doing the work. **(d-i) holds.**
- **Tier quality is doing all of it.** `Q_O = 0.55·Q` and `surv_O = surv_max·Q_O^θ` give `surv_O = 0.508` (primary),
  `0.476` (lower), `0.479` (upper) in 2024, against `surv_H = 0.995`. With 60–85 % of places in Tier O, the
  admission-weighted completion is roughly half the untiered system's:

  | level (2024) | `adm_H/C` | `T_O/C` | `surv_H` | `surv_O` | v1.5 completion | v1.3 completion |
  |---|---|---|---|---|---|---|
  | primary | 0.140 | 0.660 | 0.995 | 0.508 | **51.6** | 100.0 |
  | lower secondary | 0.257 | 0.543 | 0.995 | 0.476 | **51.6** | 85.9 |
  | upper secondary | 0.246 | 0.199 | 0.995 | 0.479 | **33.7** | 76.6 |
  | tertiary | 0.402 | 0.193 | 0.966 | 0.501 | 44.1 | 37.4 |

- **The outside option and sorting are quantitatively inert.** The declared child-wage shock (+10 %) moves upper 2024
  completion by **+1.08 pp** — the wrong sign and below the 2.0 pp bar — because the κ cap fixes the *total* upper entry
  in all 53 cells, so the shock can only shift the H/O *composition* (and therefore the admission-weighted survival),
  not the total. Sorting OFF moves mean unfilled by −1.58 pp. Per the frozen rule this makes the sorting/outside-option
  account **decorative at this parameterisation**, and (d) FAILs on (d-iii) — exactly the outcome §6(d) was written to
  expose ("the level pattern is pipeline-stipulated").
- **(d-iv) passes, but for an indirect reason and this must not be over-read:** Tier O quality −20 % raises mean unfilled
  by **+11.22 pp**. The frozen `U_O` vector contains **no quality term**, so this is *not* a take-up response to quality;
  it runs through the general-equilibrium chain quality → survival → graduates → formal employment → `G_H` → `A_H`.
- **(d-ii) fails its third leg.** The declared cap form (a same-year *rate* comparison, `adm_upper ≤ κ·comp_lower`) is
  strictly tighter than the completion-level statement by the factor `surv_upper ≈ 0.87`, so it binds in **all 53**
  scored anchor cells and the upper level **is** cap-determined in every year. The predeclared expectation of ≥5
  non-binding cells was derived from the 20/53 pattern of the *completion-level* audit, not from the cap itself.
- **The two readings of the cap are mutually exclusive, and this is worth stating plainly.** Read as a *count*
  comparison (`adm_upper_count ≤ κ·comp_lower_count`, the weaker reading because `C_lower/C_upper = 1.05`), the cap
  binds in **0 of 53** cells — i.e. it never acts, A01 collapses back to v1.3, upper 2024 stays at 76.64 and the
  completion-level audit fails with **20/53** violations. Read as a *rate* comparison (the reading §3.1's own algebra
  requires, since `m·adm_upper` must be a completion rate), it satisfies the audited object **0/53** and binds in all
  53 cells. **No reading of the frozen cap satisfies both (e-ii)(3) and (d-ii)'s non-binding leg.** The rate reading is
  used (it is the only one consistent with the declared sufficient-form argument), and the diagnostic leg fires
  truthfully against it.

---

## 5. The pipeline: what the link does, and the two numbers the brief asked for

### 5.1 The κ link works arithmetically; the guard formalities do not survive the frozen pipeline

- **In-loop, structural.** The cap is applied inside the annual accounting at the upper entry cohort, not as a
  post-processing clip, and it is the identity when `kappa_link = OFF`. Violations of
  `comp_uis_upper(t) ≤ 0.949·comp_uis_lower(t−3)` in the 53 scored anchor cells (1973–2025): **20 before → 0 after**
  (`results/kappa_cap_audit.csv`), with slack **+4.0 to +12.8 pp** where it binds. `κ = 0.949` was never estimated,
  updated or swept.
- **`KAPPA-GUARD-FAIL`, for a structural reason.** Sub-guard (1) of §6(e-ii) requires `primary`, `lower_secondary` and
  `tertiary` to be **cell-identical** to v1.3. That is arithmetically impossible once the cap binds: the frozen pipeline
  feeds upper-secondary graduates into the tertiary eligibility pool (`sim_v1_3.py:866-873`), into the rung-matching
  candidate pool, and into formal employment, which drives the growth equation. A binding cap on upper entry therefore
  moves **every** row's economy columns (`gdppc`, `growth`, wages, rung employment, PTR, complexity). Only **180 of the
  5 040** non-upper rows are cell-identical, and **1 620 of 1 680** upper rows differ — most of them in years where the
  cap does not itself bind, because the economy has shifted. Sub-guards (2) and (3) hold; (1) does not. **Per §6(e-ii)
  the pipelink result is recorded INVALID, and the breach is the finding**: a structural cross-level link cannot be
  confined to upper-secondary rows in this pipeline.
- **The A01 single-gate contrast is mislabelled in the predeclaration.** (a-iv) expects `same_level = 0` in A01
  "because the upper school gate is unrationed". That is true of **A00** (count **0**) but not of A01: the κ cap itself
  rations the upper gate, so `rationed_official > 0` and the count is **15**. Scored as written → the leg fails.

### 5.2 A01 linked upper 2024 vs the 63.97 expectation

**A01 upper-secondary `completion_uis` 2024 = 55.657 pp.** The predeclared ceiling is
`0.949 × 67.4073 = 63.9695 pp`, so the endpoint satisfies the declared *bound* (55.66 ≤ 63.97) but sits **8.31 pp
below** it. The arithmetic is exact and worth stating plainly:

```
63.9695  = 0.949 × comp_uis_lower(2021)          the entry-cohort bound, in completion-rate units
55.6573  = 63.9695 × surv_upper(2024)            surv_upper(2024) = 0.8700
8.3122   = 63.9695 × (1 − 0.8700)                the gap is the survival factor, nothing else
```

The §3.1 "sufficient form" argument is correct as a *bound* (upper completion = `m·adm_upper·surv ≤ κ·lower`), but the
reading "upper 2024 ≈ 63.97" in §9 of the predeclaration omits `surv_upper`; the realised endpoint is the bound times
survival. **This is not a defect of the link and it is not a reason to move κ.**

### 5.3 The required lower-2021 and the defect it exposes

The link requires `comp_uis_lower(2021) ≥ upper(2024)/0.949`. For the model's own untiered upper 2024 of 76.6391:

- **required lower 2021 = 80.76 pp** (`76.6391 / 0.949`);
- **generator lower 2021 = 67.4073 pp** (`synthetic_panel_v1_3.csv`) → **13.35 pp short**;
- **v1.5 (A11) lower 2021 = 43.73 pp** → **37.03 pp short**.

So the lower series is the binding defect, exactly as EXP-7 leg (b), class `b2`, found — and the tier block **widens**
the gap rather than closing it, because Tier O survival degrades the lower series itself. Any future attempt to reach
the observed 2024 upper figure by relaxing κ would be working on the wrong series.

---

## 6. The (b) disclosure: why MIXED did not happen

The predeclaration states, before the run, that **(b) is expected `MIXED`** — pattern holds, endpoint displaced by the
κ link. **It did not: (b) = FAIL.** The reason is arithmetic that §9 did not perform:

- §9 computed the **place-coverage** and **κ** consequences only. It did not compute the **survival** consequence of
  `q_O_mult = 0.55` under the frozen survival law `surv = surv_max·Q^θ` (T05, insertion point I5).
- With `surv_O ≈ 0.48–0.51` per level and 60–85 % of enrolments in Tier O, primary completion cannot exceed roughly
  `h_share·0.995 + (1−h_share)·0.50 ≈ 0.57` at any level, so the 92 pp primary bar is unreachable *by construction*
  of the declared parameters, and the `[55,85]` upper band is missed from below (33.68).
- **No parameter, threshold, band or arm was changed in response.** The pre-freeze arithmetic was simply incomplete,
  and the honest result is that the frozen A5 parameterisation **cannot reproduce the v1.2/v1.3 signature**. The
  tier block reproduces the *coexistence* and destroys the *level pattern*.

A useful decomposition, reported as arithmetic and **not** as a rescue: the κ link alone (arm A01, bimodal OFF) leaves
the signature intact (primary 100.0, lower 85.9, upper 55.66 — inside the `[55,85]` band, outside `[73,77]`, i.e. what
`MIXED` would have been), so **the pattern failure is attributable to the tier block, not to the pipeline link**.

---

## 7. Guards, determinism, audits

| guard | status | evidence |
|---|---|---|
| **E1 baseline (A00)** | **BASELINE-GUARD-PASS** | `results/synthetic_panel_v1_5_A00.csv` sha256 `47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3`, 6 720 rows × 89 columns, no re-fit. Independent cross-check: the frozen base code run directly (`base_v1_3_sim.run_all`) produces the **same** hash. |
| **E2 κ link (A01)** | **KAPPA-GUARD-FAIL** | 0/53 violations after (20/53 before); cell identity breached on tertiary **and**, through the economy columns, on all levels — see §5.1. |
| **E3 frozen files** | **FROZEN-FILE-GUARD-PASS** | 20/20 files in the five frozen directories plus this experiment's four frozen spec files unchanged. *Separately disclosed, not repaired:* `08_council/DECISIONS.md` moved (`6fdcf8ee…` → `59696b81…`, mtime 2026-11-21 00:05) — outside E3's declared scope and outside this worker's write scope. |
| **E4 determinism** | **DETERMINISM-PASS** | two complete runs into `results/` and `results/determinism_run2/`; **14/14** result files byte-identical (`cmp` + sha256). Seed 20261120, one `PCG64` stream, frozen v1.2 draw order, the tier block draws nothing, floats `%.10g`, no timestamp/hostname/PID. |
| **R1 ratchet** | **0 hits** | token scan of the transition code (comments stripped) for `restore, revert, rollback, return-to-prior, target_return, prior_level, reversal, reset_to, go_back` → 0. `Tstate` non-decreasing and the opened-rung set non-decreasing in all 30 countries (R2, descriptive). |
| **T-AUD-1…5** | **PASS** | no country-specific value in the tier block; one vector per parameter for all 30 countries; `K_H` recomputed from `seats × h_share` matches the panel exactly (max abs diff **0.0**); one boolean read per insertion point; `outside_utilities()` reproduces the frozen `state_shares()` to **0.0** (max abs share difference). |

**`NO REVERSAL DIAGNOSTIC IS TO BE INFERRED FROM THIS RUN.`** v1.5 contains no reversal test, no exit-episode test and
no "did the system go back" statistic. The absence of a reversal term is a construction fact, not a test of the strong
claim.

---

## 8. What this cannot claim

1. **No causal claim, no direction claim.** Nothing here says schooling causes anything, that either tier causes any
   outcome, or that the Philippines behaves like this model.
2. **`SYN00_PHL_LIKE` is not the Philippines.** It is the only synthetic country whose trait block is anchored on an
   observed PHL path; all 29 others are declared. Every number is `LABEL: SYNTHETIC`.
3. **Not fitted to the known PHL outcome.** No parameter carries a `FITTED` label; nothing was calibrated to 75.025,
   to the [73,77] band, or to any observed series. The 63.97 pp ceiling was declared before the run.
4. **Never "demand falsified", in any paraphrase.** The A3-D result remains a **model-specification** result: *the
   unrationed single-gate model cannot represent a bimodal system*. Demand is revealed and strong (shadow education,
   queues at good schools, credential chasing). What this run shows is that a two-tier structure *can* hold the
   coexistence, and that the declared A5 parameterisation then fails the level pattern.
5. **The ceiling remains `UNABLE as to cause` (D63).** A synthetic PASS or FAIL is non-diagnostic unless the ablations
   move the objects (D81) — which is exactly why (d) is reported as FAIL above.
6. **C1–C4 are not reopened.** No WT/DT cell was re-run or re-scored, no paper-test slate was added, A3-D was not
   re-tuned, and the v1.4 `c4a`/`c4b` FAILs stand exactly as delivered (D117). The tier-specific exit cost is noted
   for the Council and **not tested** (D101 unchanged).
7. **The one-way ratchet is theory, not evidence.**
8. **HELD data stay HELD.** No seat-utilisation number, no private/public capacity share and no SHS voucher take-up
   figure exists on disk and **none was fabricated**. Tier O `V_O` is a *model object*, not a measurement of
   utilisation, and it is **not** equated with the observed out-of-school rate.

### The HELD DATA ASK (still standing, D124(d))

1. **DepEd / CHED seats vs enrolment**, by level, track (SHS academic / TVL / sports / arts & design) and region.
2. **Private / public shares** of enrolment *and of provision*, by level and track (the WDI series available are
   national enrolment aggregates only).
3. **SHS voucher take-up** — number and share of recipients, by track and region.
4. **Capacity utilisation** — places offered vs places filled. This is the object Tier O's `V_O` would be validated
   against, and it has **no on-disk proxy at all**.

Corroboration that this is genuinely blocked, not an oversight: `STATE_CAPACITY.csv:2-3` records
"number of public schools by year" and "classroom construction completed by year" as `DATA BLOCKED` (deped.gov.ph 403,
DPWH 403, Wayback 429).

---

## 9. What would change the verdict

**Only a new predeclaration** with a new object or new bars — never a re-run of this one. Specifically, and each would
need to be frozen before it is computed:

- re-specifying the Tier O quality/survival mapping (the `q_O = 0.55 → surv ≈ 0.50` channel is what fails (b)); or
- declaring an explicit quality term in `U_O` (there is none, which is why (d-iv) only passes indirectly); or
- declaring the κ link on the *counting* register or with an explicit survival allowance, which would change how often
  the cap binds (and therefore (d-ii)); or
- declaring the (a-iv) contrast against A00 rather than A01.

**None of these was done here.** No threshold, band, year set, κ value, arm definition or verdict word was changed
after the freeze, and no check was rescued.

---

## 10. Deviations that had to be decided at build time (all disclosed, none calibrated)

1. **The outside refusal set is `max(U_work, U_neither)`; `U_both` is not a refusal value.** `U_both` is the frozen
   block's school+work state — a **school** state in the block (`ds = p_s + p_b`). Used as an outside value it lets a
   cell collect the schooling value *plus* the child's earnings **without occupying a place**, and it dominates Tier O
   in **15/15** cells in every year (reported per country-year-level in the panel column
   `both_would_dominate_cells`), which drives `T_O ≡ 0` and collapses enrolment to `h_share·seats` (primary 2024 would
   be ≈16 pp). The two no-place outside states are used instead, and the count of cells that *would* have been affected
   is published rather than silently dropped.
2. **The outside option is evaluated at each lattice cell's own income `y_i`**, using the frozen block's equations and
   parameters unchanged (only the income argument is the cell's rather than the representative household's).
3. **Tertiary has no tier-choice equilibrium.** The frozen child block is undefined at `L = 3` (`AGE_W` and `cost_base`
   each have three entries), so the tertiary tier *composition* inherits the same-year upper-secondary choice shares
   while the aggregate stays the model's own tertiary demand and eligibility pool.
4. **`D_O` is year-invariant by construction**: it is the same demand equation evaluated at the open tier's gate state
   (`R_O = 1`, `V_O = 0`, `dpi = 0`), the v1.3 `g0` no-gate control that §9 itself uses as the (c-i) baseline. It is
   country-specific through `(phi, s, sigma)`.
5. **When the κ cap binds at upper secondary the reduction is taken over-age → Tier H → Tier O**, so that unfilled
   Tier O places are never manufactured by the cap (T-AUD-3's independence property is preserved; the cap never
   touches `K_H`).

**One process error, disclosed in `TUNE_LOG.md` (B1):** the pre-run `SHA256SUMS.txt` was overwritten by smoke runs
before it could be snapshotted byte-for-byte, so `results/FROZEN_BEFORE_SHA256SUMS.txt` is a *reconstruction* of its 33
recorded `(sha256, path)` pairs, re-verified against disk (30/33 still match; the exceptions are the two files this run
updates and the externally edited `DECISIONS.md`). The original file's sha256 is recorded as `89638b39…` in
`RUN_MANIFEST.json` and `results/guard_report.json`.

---

**`LABEL: SYNTHETIC` — built and run to the frozen predeclaration — not evidence — no causal or direction claim — no
reversal diagnostic inferred — C1–C4 not reopened — A3-D not re-tuned — HELD data stays HELD.**
