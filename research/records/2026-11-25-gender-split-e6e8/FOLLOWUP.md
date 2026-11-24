# FOLLOW-UP — EXPLORATORY POST-HOC weighting/leverage probes of the gender split (task-7)

**Status: EXPLORATORY / POST-HOC. Additive; the confirmatory `PRE_REGISTRATION.md` and `REPORT.md` are not edited.**
**Pre-registration for this follow-up:** `PRE_REGISTRATION_FOLLOWUP.md`, commit **`dab608c`**, written and
committed **before any follow-up computation**. Confirmatory record: commit **`5b42bfd`** (task-3).
**Branch:** `research/gender-split-e6e8-2026-11-25`. **Date:** 25 November 2026. **Author:** `gender-split`
(task-7). **Host-only** (host venv; no AutoDL box, no GPU, no power/watcher action).
**Language:** association only; no causal wording. Every number below is labelled RECOMPUTATION or
RE-ESTIMATION.

**Operator's question.** The confirmatory primary statistic `D = mean_{e=+1..+6}(ATT_F − ATT_M) = −3.94 pp`,
95% paired percentile CI **[−8.72, +0.29]** (includes 0 → "no detected sex difference"), yet the event-level
differences at **+1** (−3.99 [−7.09, −0.53]) and **+2** (−4.67 [−8.61, −0.87]) have CIs excluding 0. **Is the
aggregate null a weighting artefact?**

**Short answer (exploratory).** **No — not a weighting artefact.** The aggregate is stable: inverse-variance
weighting moves the point estimate only from −3.94 to **−4.05**, leave-one-event-out spans just **−4.07 to
−3.80** (0.27 pp), and dropping MOZ gives **−3.95**. What flips the "includes zero / excludes zero" reading is the
**CI construction**, not the weights: the pre-registered B1 formula combines six *marginal* CIs as if independent,
while the confirmatory paired country-cluster bootstrap makes the six post-event differences strongly positively
correlated (joint paired SE ≈ **2.30**, versus ≈ **0.96** implied by independent combination), so the B1/IV CI is
anti-conservative. With paired uncertainty the IV aggregate CI is **[−8.56, +0.45]** and includes zero. The
confirmatory headline is preserved — with one honest fragility note: the paired percentile CI's upper endpoint is
only **+0.29**, so "no detected sex difference" is close to the boundary.

---

## B1 — inverse-variance weighted mean of the six post-event differences — **RECOMPUTATION**

Arithmetic on committed `results/e8_event_difference_verified8.csv`; **no new estimation**. Formula (fixed in
`PRE_REGISTRATION_FOLLOWUP.md`): `se_e = (ci_hi − ci_lo)/(2×1.96)`; `w_e = 1/se_e²`;
`D_IV = Σw_e d_e / Σw_e`; `SE_IV = 1/√(Σw_e)`; 95% CI `= D_IV ± 1.96·SE_IV`. Stated approximation: the reported
paired percentile CIs are treated as symmetric normal intervals.

| event e | d_e = ATT_F − ATT_M | committed 95% CI | se_e from CI | normalised weight |
|---|---|---|---|---|
| +1 | −3.987 | −7.087, −0.525 | 1.674 | **33.1%** |
| +2 | −4.668 | −8.615, −0.869 | 1.976 | **23.8%** |
| +3 | −4.162 | −10.473, −0.004 | 2.671 | 13.0% |
| +4 | −3.679 | −9.864, 1.736 | 2.959 | 10.6% |
| +5 | −3.868 | −9.505, 3.416 | 3.296 | 8.5% |
| +6 | −3.301 | −9.122, 2.261 | 2.904 | 11.0% |

| statistic | value |
|---|---|
| **D_IV (inverse-variance weighted)** | **−4.053 pp**; SE_IV 0.963; **95% CI [−5.94, −2.17]** (excludes 0) |
| D (pre-registered equal weight) | **−3.944 pp**; committed paired percentile 95% CI [−8.72, +0.29] (includes 0) |
| D equal-weight mean of the six d_e | −3.944 pp |
| equal weight with the *same* normal approximation | −3.944; 95% CI **[−6.06, −1.83]** (excludes 0) |

**Weight profile.** Weights concentrate on +1 (33%) and +2 (24%) simply because those event CIs are the
narrowest — not because of any post-hoc choice.

**Pre-registered B1 rule fired mechanically** (IV CI excludes 0 → report "weighting artefact" as exploratory).
**But the pre-registered comparator refutes that interpretation**: applying the *same* independent normal
approximation to the *equal-weight* mean also excludes zero ([−6.06, −1.83]). So the apparent flip is **not**
about weighting. Post-hoc diagnostic (added after seeing B1, labelled — see Deviations): the confirmatory paired
percentile CI implies a **joint paired SE of ≈2.30** for the aggregate, while the B1 formula's independent
combination implies ≈0.96; the six event differences share the same country draws and overlapping event windows
and are therefore strongly positively correlated. Using the joint paired SE: **D_IV 95% CI = [−8.56, +0.45]
(includes 0)** and equal-weight [−8.45, +0.56] (includes 0).

**Conclusion for B1:** with paired (confirmatory-appropriate) uncertainty, the inverse-variance weighted aggregate
still includes zero; the equal-weight aggregate null is **not** a weighting artefact. The confirmatory "no
detected sex difference" headline stands. The B1 IV interval as pre-registered is reported for completeness but is
anti-conservative and is not used to overturn the confirmatory inference.

## B2 — leave-one-event-out equal-weight D — **RECOMPUTATION**

Full equal-weight D = −3.94395. For each dropped post event, D over the remaining five:

| dropped event | D_(−e) | leverage vs full D |
|---|---|---|
| +1 | −3.9354 | +0.0086 |
| **+2** | **−3.7991** | **+0.1448 (largest)** |
| +3 | −3.9004 | +0.0436 |
| +4 | −3.9970 | −0.0531 |
| +5 | −3.9592 | −0.0152 |
| +6 | −4.0726 | −0.1287 |

**Range: [−4.073, −3.799] (0.27 pp); most influential event: +2** (max |leverage| 0.145). The aggregate is
insensitive to any single event; no dropped event changes the sign. Descriptive leverage only; no significance
test invented.

## B3 — drop-MOZ paired CS D — **EXPLORATORY RE-ESTIMATION** (not recomputation)

MOZ 2004 contributes no e=0 row (missing 2003 base) and reduces treated n at several horizons. Same pre-registered
design and seeds as the confirmatory run (`att_cs` @ `bd782be`, SSA 1990–2015, verified dates, universal base
`g−1`, not-yet-treated controls, event −5..+6, cohort-weighted, 500 paired country-cluster bootstrap reps, seeds
`20261125+i`, percentile CIs), with **MOZ removed from the whole sample** (7 treated countries; MOZ cannot re-enter
as a never-treated control).

| statistic | value |
|---|---|
| **D_dropMOZ** | **−3.947 pp**; 95% paired percentile CI **[−8.32, +0.24]**; 499/500 replicates |
| confirmatory D (all 8) | −3.944 pp; [−8.72, +0.29] |
| sign | male-higher; CI includes zero |

MOZ does not drive the aggregate: the point estimate moves by 0.003 pp and the conclusion is unchanged.

---

## What this does and does not change

- **Confirmatory headline preserved:** "both sexes' post-abolition primary-GER trajectories are similar; the
  female-minus-male post-period mean is −3.94 pp with a 95% CI that includes zero (no detected sex difference)."
  No exploratory output replaces it.
- **The aggregate null is not a weighting artefact** (IV point −4.05 vs equal −3.94; LOO 0.27 pp; drop-MOZ
  −3.95). The event-level +1/+2 pattern is a descriptive, multiplicity-untested observation on 7 treated
  countries; the six post-event estimates are positively correlated, so a significant-looking pair of events does
  not imply the aggregate mean is non-zero.
- **Honest fragility note (exploratory):** the confirmatory paired percentile CI's upper endpoint is +0.29 —
  close to zero. A symmetric normal framing of the same uncertainty crosses zero (equal-weight normal approx
  [−6.06, −1.83]; IV with joint paired SE [−8.56, +0.45]). "No detected sex difference" is therefore a
  near-boundary non-detection, not a precise zero. More treated countries (power), not a different weighting, is
  what would sharpen it.
- **Deviations (declared):** (i) B1's independent-normal-SE formula and the equal-weight normal-approx comparator
  are stated approximations inherited from the pre-registration; (ii) one **post-hoc diagnostic** was added after
  seeing B1 — the joint paired SE implied by the confirmatory percentile CI — to explain the discrepancy; it is
  labelled "diagnostic_not_in_prereg", adds no decision rule, and the pre-registered fields remain as computed;
  (iii) B3 is a re-estimation on a reduced sample (exploratory), not a recomputation.
- No new data were downloaded, no series imputed, no proxies used; all nulls and all three probes are reported.

## Reproduction

```
cd research/records/2026-11-25-gender-split-e6e8
/Users/treymenefee/neon-boot/venv/bin/python scripts/gender_split_followup.py
# reads committed results/e8_event_difference_verified8.csv + results/gender_split_results.json (B1/B2),
# re-runs the pre-registered paired CS design with MOZ excluded (B3), writes results/gender_split_followup.json
```

Output: `results/gender_split_followup.json` (`B1`, `B2`, `B3`, `confirmatory_headline`,
`confirmatory_headline_changed: false`; B1 also carries `pre_registered_rule_fired: true`,
`weighting_artefact_supported: false`).

## Claims → source map

| claim | number | source field |
|---|---|---|
| IV-weighted D | −4.053 [−5.94, −2.17]; weights +1 33.1%, +2 23.8% | `results/gender_split_followup.json` → `B1.D_IV`, `B1.weight_profile_normalised` |
| equal-weight confirmatory D | −3.944 [−8.72, +0.29] | `B1.D_equal_weight_confirmatory*` (from `results/gender_split_results.json`) |
| equal-weight normal-approx comparator | −3.944 [−6.06, −1.83] | `B1.D_equal_weight_normal_approx_ci95` |
| joint paired SE / IV with paired SE | 2.30; [−8.56, +0.45] | `B1.diagnostic_not_in_prereg` |
| LOO D range / most influential | [−4.073, −3.799]; event +2 (0.145) | `B2` |
| drop-MOZ D | −3.947 [−8.32, +0.24] | `B3` |
| headline unchanged | `confirmatory_headline_changed: false` | top-level |
