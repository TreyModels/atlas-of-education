# Equation suite + full-system multiverse audit (task-47)

**Record:** `research/records/2026-11-25-suite-audit/` · branch `research/edsystem-audit-2026-11-25`
(base `origin/research/handoff-2026-11-24` @ `f15a802`). **Auditor:** suite-auditor. **Date:** 2026-11-25.
**Scope:** claim-layer and engine/data audit only — decision rules, FAIL reporting, observed-vs-synthetic labels,
η²/identifiability claims, and the cluster-robust/seed-FE/Holm/stratum tests. **No literature verification**
(stopped by instruction). **No server compute.** Read-only: no audited file was edited.
**Sources:** `research/equation-suite-2026-11-25` @ **`a7fcfb9`** (10 scripts);
`research/masseng-edsystem-2026-11-25` @ **`b7108da`** (1,440 runs);
`research/edsystem-tests-2026-11-25` @ **`aadbbb4`**. Script/results: `scripts/audit_claims.py`,
`results/audit.json` (26 checks, 18 flags).

---

## 0. Bottom line

1. **10/10 scripts executed; 3 decision rules fail** (S3/eq03 learning, S4/eq04 gates, S6/eq06 migration). But
   only **S4's failure is on a clearly pre-registered rule**. S3's failed criterion ("ρ recovered within 0.10 in
   half the replications") is **not in the pre-registration** — the pre-registered rule ("recovered ρ closer to
   the truth than Cobb–Douglas implies, ρ = 1") **passes** (median ρ̂ = 0.2 vs truth 0.5 vs CD 1.0). S6 is a new
   script created by Amendment 02 and has **no pre-registered decision rule** at all. And S10's **PASS is wrong
   under the old pre-registered S3 rule**: in the single-process world the Tobit income elasticity is **7.499**
   against a truth of 0.8, so the pre-registered "both within 0.15" condition fails, yet S10 reports PASS.
2. **The three FAILs are partly buried.** The report headline says **"Failures: []"**, the per-script section is
   titled **"smoke PASS, full PASS"**, and the table has no verdict column. The per-script bullets do show
   `PASS=False`, but the plain-English summaries say the opposite in two of three cases: S4 says a reserved quota
   "flips the gap (0.091)" although the quota gap is **+0.0906** (not flipped); S6 says "networks increase the
   effect" although the network marginal effect **0.00892** is *smaller* than the no-network **0.01402**; S3's
   plain summary omits the failed ρ criterion entirely.
3. **Full-system statistics:** the cluster-robust OLS with seed FE reproduces `full_system_tests.json` exactly
   (max |Δeffect/se| = 5.6e-14), but the **decision-rule machinery has false positives**: 4 "supported" rows have
   *no strata at all* (empty `all([])` returns True), and one zero-variance outcome is classified supported
   (tut_rate effect 2.8e-17, SE 4.2e-19, p_holm 0). The committed JSON and the report disagree on the supported
   set (report says supply supports only public quality; JSON also marks formal share supported). **p-values and
   Holm were introduced although the multiverse pre-registration says "no p-values"**, and there is no
   pre-registration for the test layer.
4. **η² values are supported; the "overlap 1.00" claims are not.** The η² table matches
   `summary_multiverse.json` (max difference 0.0049, rounding). But "supply vs attainment: overlap **1.00** for
   primary/lower/upper; **?** for tertiary" is wrong: committed worst overlaps are **0.932 / 0.888 / 0.872 /
   0.850**, and "learning configuration vs attainment: not identified for primary (overlap 1.00)" is wrong
   (actual **0.819**). The *conclusion* "supply not identifiable from attainment" still holds under the
   pre-declared ≥ 0.80 rule. "Tutoring η² ≈ 0" is imprecise: learning-axis η² on completion is **0.014–0.041**.
5. **Labels:** observed-vs-synthetic is mostly right (only S7/S8/S10 touch committed observed/reconstructed or
   literature targets), but **eq07's top-level `data_tier` says SYNTHETIC** despite its observed dashboard check.
   **eq04's `mechanism_in_masseng_v5` flag is `true`**, contradicting Amendment 03 and the suite's own README
   ("exam bar/quota no"). No MASSENG-output mislabelling was found in text: the suite says standalone, not
   MASSENG v5 output; the full-system record is eduengine (toy), not MASSENG v5. No causal claims found; the PHL
   check is honestly labelled a level check, not calibration.

---

## 1. Equation suite — what ran and what failed

`run_all.json`: 10 scripts, execution **failures = []**, all status PASS, wall **61.69 s**. Per-script hash
provenance is intact: all 10 script and output sha256 values match `run_all_manifest.csv` and the committed
files.

| S | script | execution | decision rule | failing sub-rule | pre-registered? |
|---|---|---|---|---|---|
| S1 | eq01_family_demand | PASS | **PASS** | — | **no rule** in prereg (new script, Amendment 02) |
| S2 | eq02_supply_finance | PASS | PASS | — | prereg S7 rule replaced by ad hoc criteria |
| S3 | eq03_learning_quality | PASS | **FAIL** | `rho_recovered_within_0.10_in_half_reps=False` | **criterion not pre-registered**; pre-registered ρ rule passes |
| S4 | eq04_transitions_gates | PASS | **FAIL** | `quota_flips_gap_negative=False` | **yes** (old S5 rule) |
| S5 | eq05_returns_credentials | PASS | PASS | — | old S1 rule simplified (no CI coverage) |
| S6 | eq06_migration_rural_urban | PASS | **FAIL** | `network_spec_effect_larger_than_no_network=False` | **no rule** in prereg (new script) |
| S7 | eq07_inequality_dashboard | PASS | PASS | — | old S8 rule mostly applied |
| S8 | eq08_growth | PASS | PASS | — | old S6 rule replaced by "near truth"/NP criteria |
| S9 | eq09_identification | PASS | PASS | — | old S9 rule simplified (null thresholds, no coverage) |
| S10 | eq10_tutoring_shadow | PASS | PASS | — | old S3+S4 rules only partly applied; **old S3 single-world rule fails** |

**S3 (eq03).** The pre-registration (S2, learning production) says: "in the ρ = 0.5 world the ability-controlled
interaction is positive with CI excluding 0 in ≥80%; CES's recovered ρ is closer to the truth than Cobb–Douglas
implies (ρ = 1)." The script instead uses `abs(mean interaction) ≤ 2×0.02`, `mean interaction > 0`, and a new
`share of ρ̂ within 0.10 ≥ 0.5`. The data: median ρ̂ = 0.2 (truth 0.5; CD implies 1.0 — so **closer than CD,
the pre-registered criterion passes**); share within 0.10 = 0.0 (the new criterion fails). The FAIL is therefore
on an **unregistered stricter criterion**; the report's table and plain summary present it as a pre-declared
failure without saying so.

**S4 (eq04).** The pre-registered rule is exactly applied: bar gap **+0.5472**, quota gap **+0.0906** (not < 0),
contest **+0.7614** → FAIL is legitimate. The plain summary says "a reserved quota flips the gap (0.091) by
construction" — **contradicted by its own number**: 0.091 is positive, the same sign as the bar gap; the rule
failed precisely because it did not flip.

**S6 (eq06).** Migration/rural-urban is a new script created by Amendment 02; the pre-registration only lists its
multiverse choices, not a decision rule. The implemented rule ("education positive in every spec" AND "network
effect larger than no network") is ad hoc. The data: education marginal effect positive in every spec (true), but
network **0.00892 < no-network 0.01402** → FAIL. The plain summary says "networks increase the effect" —
**opposite to the output**.

**S10 (eq10).** The old S3 tutoring-demand rule required: in the DIFFERENT world, two-part |η̂−0.8| ≤ 0.15 and
Tobit |η̂−0.8| > 0.15 in ≥90%; in the SINGLE world, **both** within 0.15. Data: single-process Tobit η̂ =
**7.499**, two-part = **0.802**; the single-world rule fails. The final S10 rule checks only "two-part closer than
Tobit", "ban raises Gini", "not claimed to fit Bray" → reports PASS. A pre-registered sub-rule was dropped, and
the dropped rule fails in the committed output.

**Report presentation (S3/S4/S6).** `SUITE_REPORT.md` line 4: "Failures: []" (execution failures, but unqualified);
line 10: "Per-script results (smoke PASS, full PASS)"; the table's "Estimat / pass-fail" column contains only the
rule text, not PASS/FAIL; line 95: "All ten scripts passed smoke and full. No script failed". The only place the
three failures appear is the per-script bullet "Decision rule: PASS=False" — no aggregate count, no
"decision-rule failures: 3" sentence. Two of the three plain-English summaries assert the opposite of the failed
rule, and the third omits it. The report has **no deviations section**, although Amendment 02 renumbered/mapped
scripts and the implemented rules do not match the pre-registered rules (see §2).

---

## 2. Pre-registration vs implementation

The pre-registration was committed before code (as required) and Amendments 01–02 were committed before the run.
But Amendment 02 changed the script set/order and only said "the counting/decision rules in S1–S10 remain". The
final scripts' rules are not the S1–S10 rules as written:

| final script | pre-registered rule | implemented rule | status |
|---|---|---|---|
| S1 family demand | none (new script) | affordability positive; forgone earnings reduce; zero-signal absorbed | ad hoc |
| S2 supply finance | old S7: "regressive if concentration index positive" | universal vs means-tested CI; NPV > 0; IRR > 5% | changed |
| S3 learning | old S2: interaction CI/80% + recovered ρ closer than CD | mean-sign checks + new ρ within 0.10 ≥ 50% | changed; failing criterion new |
| S4 gates | old S5: quota flips admission gap | same, + contest criterion | mostly applied |
| S5 returns | old S1: 2SLS CI covers truth ≥90%; OLS CI excludes truth | mean-bias thresholds; no CI coverage | simplified |
| S6 migration | none (new script) | education positive; network effect larger | ad hoc |
| S7 inequality | old S8: report Gini/Theil/IGE/rank/Oaxaca; null CI includes 0 | null CI + persistent + Theil between | mostly applied |
| S8 growth | old S6: λ within 2 SE; β_H sign flip/shrink | λ "near truth"; β_H inflation; NP interaction > 0 | changed, extra criterion |
| S9 identification | old S9: null CIs include 0 in ≥90% | fixed near-zero thresholds; IV closer than OLS | simplified |
| S10 tutoring | old S3 + S4: hurdle/Tobit thresholds; ban ΔGini > 0 with CI; Bray not fit | two-part closer; ban Gini share; Bray not fit | partly applied; dropped rule fails |

This is not itself a failure of honesty — the scripts are transparent about their implemented rules in
`decision_rule` JSON — but **the record does not log the rule changes as deviations**, and the report's "pre-declared
FAILs" framing is only true for S4. Any reader who takes "pre-declared" at face value is misled about S3 and S6, and
misses that S10's pre-registered rule fails.

---

## 3. Full-system multiverse — statistics and claims

### 3.1 Design and provenance

- 1,440 runs = 144 design cells × 10 seeds, N=400, T=70, measure from year 35; six axes (affordability 3,
  supply 2, learning 3, gates 2, jobs 2, rural 2); `results_multiverse.json` sha256 `004173aa…` is identical on
  the masseng-edsystem and edsystem-tests branches; run wall 304.1 s at 12 workers (matches log/meta).
- Labels: "SIMULATION ONLY — eduengine toy worlds; illustrative parameters; no causal/empirical claims"; missing
  mechanisms (migration, sorting, remittances, calibration, informal/formal composition) and the unusable push-out
  decomposition are stated in the report. Good.
- But `full_system_tests.json` has **no code hash, environment, commit, or pre-registration reference**; the
  record has no test pre-registration.

### 3.2 What is statistically correct

- The OLS with all main effects + **seed fixed effects** and **cluster-robust SEs by design cell (144 clusters)** is
  implemented as described; I rebuilt the design/CRVE independently and reproduce every committed effect and SE to
  5.6e-14. The normal-approximation p-values and 95% CIs are arithmetically consistent with those SEs.
- Holm is applied within each axis-value contrast across the nine outcomes. That is a defensible family if stated,
  but the report does not say it; and there are **8 contrast blocks**, each with its own 9-outcome family, so the
  whole table is not jointly controlled. No pre-registration defines the family.

### 3.3 What is wrong

1. **The stratum check can pass vacuously.** `sign_consistent = all(sign(x) == sign(effect) for x in strat)`; when
   `strat` is empty, `all([])` is True. Four supported rows have `stratum_min = stratum_max = None`:
   - supply → `formal_share_gdp` (effect 0.135, SE 0.003, p_holm 0) — this outcome exists only in the fiscal arms,
     so fixed-budget rows are NaN; the supply dummy is collinear with the intercept. The coefficient/CI are
     unidentified, not evidence. The report correctly does **not** list it, but the JSON marks it supported.
   - learning → `tut_rate` for `plus_private` (effect 2.8e-17, SE 4.2e-19, p_holm 0) — a **zero effect with zero
     variance classified as supported**. This is a clear false positive.
   - learning → `tut_rate` for `plus_private_tutoring` (0.159, no strata).
   - jobs → `skill_premium` (0.882, no strata; skill premium only exists in competitive arms).
2. **The JSON/report supported sets disagree.** JSON has **49 supported rows**; the report's tables are a selection.
   Missing/contradicted examples: supply `formal_share_gdp` (JSON supported, report says "supply: only public quality
   is supported"); family credit `formal_share_gdp` (+1.66/+3.81, not shown); jobs `skill_premium` (+0.882, not
   shown); learning `plus_private` formal share/skill premium/q_pub (only the plus-tutoring values are shown); the
   zero-effect learning `tut_rate` is absent. The report never says the table is incomplete.
3. **p-values were not pre-registered.** The multiverse pre-registration's analysis plan (item 5) explicitly says:
   "Seed-level uncertainty: mean and 90% interval across 10 seeds for every reported cell; **no p-values**; no causal
   language". The edsystem-tests record adds OLS p-values, 95% CIs, Holm and a "supported" decision rule without a
   new pre-registration or a deviations note. This is the largest procedural problem in the full-system layer: a
   post-hoc significance criterion now drives the word "supported".
4. **False precision.** Many `p_holm` values are exactly 0.0 from normal-tail underflow; the report prints neither
   p-values nor the Holm family, but the JSON's "supported" flag depends on them.
5. **η² vs overlap claims.** The η² table in `RUN_REPORT.md` matches `summary_multiverse.json` (spot checks:
   primary afford 0.691, lower gates 0.701, q_pub supply 0.418, mpl learning 0.612; max report-vs-JSON difference
   0.0049 at 2-dp rounding). The identifiability prose does not:
   - "supply vs attainment: overlap **1.00** for primary/lower/upper; **?** for tertiary" — actual **0.932 / 0.888 /
     0.872 / 0.850**; the "?" is an unfinished placeholder.
   - "learning configuration vs attainment: not identified for primary (overlap **1.00**)" — actual **0.819**.
   - "tutoring η² ≈ 0 for completion" — actual learning-axis η² **0.0405 / 0.0138 / 0.0217 / 0.0254**; small, not 0.
   The **conclusions** survive: supply overlaps ≥ 0.80 for all completion outcomes, so under the pre-declared
   ≥ 80%-overlap rule supply is not distinguished; learning is 0.819, just above threshold. But the numbers and the
   placeholder must be corrected.
6. **PHL check** is honest: observed 2024 lower-secondary completion 84.75%, simulated mean 0.635, 90% range
   [0.550, 0.833]; the report calls it a level check on one construct-limited variable, not calibration. Supported.

---

## 4. Labels, causality, MASSENG attribution

- **Observed vs synthetic.** Report text: only S7/S8 use committed observed/reconstructed panels (descriptive) and
  S10 uses Bray literature targets; all other scripts synthetic. The input provenance hashes match the committed
  files (`long_run_panel.csv`, `x4_panel.csv`, `bray_targets.json`). One label bug: **eq07 JSON top-level
  `data_tier` = "SYNTHETIC"** although it runs an OBSERVED/RECONSTRUCTED dashboard check (nested
  `dashboard_real.data_tier` says observed). eq08 and eq10 include observed/literature in their tiers. The report
  labels S7 correctly; only the JSON is wrong.
- **MASSENG boundary.** Every script carries `masseng_boundary.used = "standalone synthetic demonstration (NOT
  MASSENG v5 output)"`; no script claims a MASSENG v5 run. But **eq04's `mechanism_in_masseng_v5` is `true`**,
  contrary to Amendment 03 ("score bar/quota gates are outside MASSENG v5") and the README ("S4: progression/capacity
  yes; **exam bar/quota no**"). The boolean should be split (progression/capacity in; gate bar/quota out) or set
  false for the gate mechanism; the generic note currently misleads.
- **Causal language.** Script/report labels say "SIMULATION / no causal claims"; plain results use model-internal
  language ("raises demand", "reduces") but always about the stipulated DGP. No causal claim about a country was
  found. The full-system report's "structural axes dominate attainment" is a statement about the toy design and is
  labelled as such.
- **No MASSENG-output mislabelling** found in the suite (all "standalone", the full-system engine is eduengine).
  The only attribution error is the eq04 boundary flag above.

---

## 5. Numbers that do not reproduce from committed files, and missing caveats

| item | committed value | claim | action |
|---|---|---|---|
| supply overlap on completion | 0.932 / 0.888 / 0.872 / 0.850 | "1.00 … ; ? for tertiary" | correct to actual values; fill the "?" |
| learning overlap on primary completion | 0.819 | "1.00" | correct |
| tutoring η² on completion | 0.0405 / 0.0138 / 0.0217 / 0.0254 | "≈ 0" | state the range, not zero |
| eq04 quota gap | +0.0906 | "flips the gap (0.091)" | say "does **not** flip; still positive" |
| eq06 network effect | 0.00892 vs 0.01402 | "networks increase the effect" | say "networks slightly reduce the marginal effect" |
| eq03 ρ recovery | median 0.2, share-within-0.10 = 0.0 | FAIL presented as pre-declared | state the criterion is added; pre-registered "closer than CD" passes |
| eq10 single-process Tobit | 7.499 (truth 0.8) | PASS | apply old S3 rule; it fails; report both |
| eq07 Theil within | NaN | "Theil within/between" | report that within is undefined/NaN; only between (0.0128) is usable |
| eq04 MASSENG boundary | true | "inside MASSENG v5" | split/false for gate bar/quota |
| eq07 data tier | "SYNTHETIC" | observed dashboard check | "SYNTHETIC + OBSERVED/RECONSTRUCTED descriptive" |
| full-system p-values | not pre-registered | "supported (Holm p<0.05 …)" | add a test pre-registration or label exploratory; restore the "no p-values" rule |
| full-system supported set | 49 rows, including 4 empty-stratum rows (one of them the zero-variance tut_rate) | "all Holm p<0.05 and sign-consistent across strata" | fix the empty-stratum/zero-variance guards; publish the full set and the report/JSON reconciliation |
| full-system category labels | no code hash/env/commit in tests JSON; no test prereg | reproducibility implied by script name only | commit hash/env and a pre-registration/amendment |

**Other missing caveats.** (i) No deviations section in `SUITE_REPORT.md` for the rule changes/renumbering, despite
the pre-registration saying changes must be logged. (ii) The report's table header numbers the rows "EQ0" for nine
scripts and "EQ1" for the tenth — a label bug that obscures the S1–S10 mapping. (iii) `eq07`'s Theil-within NaN is
not disclosed. (iv) The full-system "supported" criterion uses a normal approximation for p-values and a raw-mean
stratum sign check (no seed FE/clustering in the stratum step) — acceptable as a heuristic, but not stated. (v) The
`full_system_tests.json` has no schema/hash for `test_full_system.py`, so the committed statistics cannot be tied to
the committed code by a reader.

---

## 6. Claims to downgrade or withdraw

**Withdraw as stated:**

1. "The three FAILs S3/S4/S6 are pre-declared." → Only S4 is on a pre-registered rule; S3's failing criterion is
   added post-preregistration, S6's rule is not pre-registered, and S10's pre-registered rule fails while S10 is
   marked PASS.
2. "All ten scripts passed / Failures: [] / smoke PASS, full PASS." → "10/10 executed; 3 decision-rule failures
   (S3, S4, S6); 2 of those criteria were not pre-registered; S10 fails a pre-registered sub-rule but is marked
   PASS."
3. S4 plain: "a reserved quota flips the gap (0.091)." → quota gap is **+0.0906**; it did not flip; this is the
   FAIL.
4. S6 plain: "networks increase the effect." → network effect **0.00892** < no-network **0.01402**; this is the
   FAIL.
5. Full-system "supported effects (all Holm p < 0.05 and sign-consistent across strata)" → false as a set: 4
   empty-stratum rows and 1 zero-variance row are flagged supported; the report/JSON supported sets differ; p-values
   are not pre-registered. Downgrade to "exploratory significance screen with known stratum/empty-cell defects".
6. "supply/learning overlap 1.00" and "?" → actual 0.85–0.93 and 0.819; the "not identifiable" conclusion holds at
   the pre-declared ≥ 0.80 rule; correct the numbers.
7. "tutoring η² ≈ 0" → 0.014–0.041 (small, not zero).
8. "Theil within/between decomposition" → within is NaN; only between (0.0128 in the persistent world) is usable.
9. "S10 passes" → only under the reduced rule; old S3 single-world Tobit rule fails (7.499 vs 0.8).
10. "The decision rules in S1–S10 remain" → several were replaced by ad hoc/simplified criteria; log this as a
    deviation and attach the implemented criterion to every script.

**Downgrade (keep with wording):**

11. "Pre-registered decision rules correctly applied" → "implemented rules are transparent in each JSON; they match
    the pre-registration exactly for S4 and approximately for S7; they are changed/simplified for S2/S5/S8/S9 and
    absent/added for S1/S3/S6/S10."
12. "PHL level check" → keep: honest, construct-limited, not calibration.
13. "η² ranking" → keep: values match committed output; say "η²" not "variance explained causally".
14. "450/1,440-run design, 304 s" → keep; matches.
15. "Only S7/S8/S10 non-synthetic" → keep for the report, but fix eq07's JSON tier.
16. "eq04 inside MASSENG v5" → split: progression/capacity in; score bar/quota out.
17. "Full-system statistical tests" → label "post-hoc test layer, no pre-registration; p-values contrary to the
    pre-registered 'no p-values' plan"; if kept as confirmatory, add a dated amendment/prereg.

---

## 7. What holds

- The execution/hash provenance is clean: 10/10 scripts ran, no execution failures, manifest and committed hashes
  match; the full-system design (1,440 = 144×10) and results hash are consistent across branches.
- The full-system cluster-robust/seed-FE OLS is correctly implemented and independently reproducible.
- The η² variance decomposition is correctly computed and matches the committed summary; the η² ranking supports
  the qualitative statements (affordability and gates dominate; learning/tutoring is second-order; jobs dominate
  formal share).
- The PHL check is honestly labelled; missing mechanisms and the unusable push-out decomposition are stated.
- No causal claims or MASSENG-output mislabelling were found; the main attribution bug is eq04's boundary flag.

## 8. Reproduce

```sh
git fetch origin 'refs/heads/*:refs/remotes/origin/*'
python3 research/records/2026-11-25-suite-audit/scripts/audit_claims.py
# -> research/records/2026-11-25-suite-audit/results/audit.json
```

The script reads the three branches with `git show`, verifies script/output hashes, recomputes the cluster-robust
OLS/seed-FE design with numpy, and checks the claims above. No server compute; no audited file edited. Limits: the
audit does not re-run any script (the suite's own full run and the multiverse are taken as committed), does not
re-derive the engines' behavioural code, and does not verify literature (stopped by instruction).
