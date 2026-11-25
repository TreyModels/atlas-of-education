# PAPER C CONFIRMATORY — preregistration draft (design-only, pending review; no compute authorized)

**Status: DRAFT for adjudicator review against the four Codex criticisms. Not yet preregistered-final, no confirmatory
run launched.** The current 128-run Pilot-0 v3 is **EXPLORATORY/hypothesis-generating** and **cannot** be used as
confirmatory evidence. Paper C asks: *why does shadow education emerge, and what determines its supply form* — private
tutor vs the pupil's own (public) teacher vs school-provided preparation. Engine pin to be frozen at the confirmatory
run: `846c9e0` (core `e111397b…8e71`), spec `docs/audit/canonical_spec.json` (re-pinned, file `e5ddef6b…`), runner
committed before launch; every output carries engine/spec/runner hashes and per-run `unfired_events==[]` assertions.

## 1. Design — orthogonal 36-cell grid + 4 regime anchors

Factors (explicitly separated, no bundling):
* **S (school provision)**: `q0 ∈ {0.85, 1.0, 1.15}` (q0 scales school quality 1:1; it also scales PRIVATE school
  quality — declared contamination).
* **L (gate pressure)**: selective G6→G9 gate `share ∈ {0.25, 0.45}` (or a bar threshold pair), plus `contest_r`
  ∈ {1.2, 1.6} on the upstream contest gate where the design is contest-based.
* **Private supply**: `own_ban ∈ {0, 0.95}`, `firm_ban ∈ {0, 0.9}`, `pay_ratio ∈ {0.55, 1.2}`, `monitoring ∈ {0.2, 0.5}`.
* **36-cell orthogonal grid** = 3 S × 2 L × 3 private-supply configurations × 2 pay_ratio/monitoring settings (cells
  declared in the appendix table; no post-hoc cells).
* **4 regime anchors** (hypothesis-generating contexts, not causal labels): market-only (own_ban .95, pay_ratio .55),
  own-open pay-gap (own_ban 0, pay_ratio .55), own-open incentive (withhold_mode='incentive', pay_ratio 1.2),
  own-open + firm ban (own_ban 0, firm_ban .9).
* **Gates**: two-stage — **N=600 screening** (canonical HK base; ~2.2 CPU-h at 8 workers) → **N=1500 confirmatory**
  only for cells passing screening (pre-declared: |effect| ≥ minimum effect AND binding assertions hold; screening
  cells that fail are reported, not silently dropped).
* **Seeds**: 8 matched seeds/cell for screening; 16 matched seeds/cell for confirmatory (matched across cells).
* **L fixed for Pilot-0 → L varied here**; `contest_prep_mode='learning'` is NOT used (inert at small learning_gain;
  a learn_gain≈0.5 arm is a declared wave-2 extension).

## 2. Primary outcomes, one per test (pre-declared)

| test | primary outcome | predicted sign / minimum effect | decision rule |
|---|---|---|---|
| T1 (S substitution) | K-12 tutoring participation | S↑ ⇒ participation↓; min effect −3 pp from q0 0.85→1.15 | holds / fails / indeterminate (CI crosses 0 and |effect|<MDE) |
| T2 (private supply form) | own_share (own-teacher share of tutored) | firm_ban .9 ↑ own_share; min +0.10 | holds/fails/indeterminate |
| T3 (withholding) | withheld h and own_share | pay_gap with pay_ratio .55 ⇒ h>0 and own_share>0.1 vs market-only | holds/fails (binding assertion first) |
| T4 (gate pressure L) | Q5−Q1 spend gap / participation | L↑ ⇒ gap/spend↑ (positional) but not via learning | holds/fails/indeterminate |
| T5 (learning decomposition) | L9/learning vs contest effort | positional mode: effort↑ with L, learning flat | wave-2 (learning mode) — declared not testable now |

Primary per test is the **first-listed** outcome; all other outcomes secondary/exploratory; multiplicity family = 4
tests (Holm across T1–T4); no post-hoc primary switching.

## 3. Uncertainty, power, decision rules

* Seed Monte-Carlo uncertainty (matched seeds; sd, 95 % CI); parameter uncertainty is **zero by construction** (frozen
  parameters) and stated as such.
* **MDE** = the pre-declared minimum effect; achieved CI half-width reported; an estimate below the MDE is
  **indeterminate**, not "no effect".
* Paired comparisons across cells use matched seeds; CIs by seed bootstrap (5,000).
* Decision outcomes are **holds / fails / indeterminate-by-context**, never "the model is wrong"; negative results are
  preserved and reported (no silent re-runs to fix signs).

## 4. Binding assertions and contamination declarations

* Non-market regimes MUST satisfy `withheld > 1e-3` and `own_share > 0.1` (else cell raises; no silent no-op); canonical
  HK/KR has withholding OFF (pay_ratio 1.2 ⇒ h=0) — all withholding cells set pay_ratio<1 or incentive mode AND own_ban<1.
* `q0` scales **both** public and private school quality (declared; not a public-only lever).
* `own_share` / `tut_firm_by_grade` mix contest-prep with firm tutoring (engine has no clean own-vs-firm split) —
  declared; supply-form claims limited to own_share with this caveat.
* `firm_price` is an OUTCOME, not an input; private-supply inputs are p_firm/firm_elast/firm_entry/rural_firm_access.
* Gate `share` denominator = cohort N by default (share_of='cohort'); declare in cells.
* Realized admission series need per-level nanmean extraction (X-29); diagnostic-only rerun separate.

## 5. Evidence layering (no cross-layer overreach)

Engine simulation establishes **mechanism plausibility only**; empirical tests use ILSA/household data
(PISA 2022 ST297 participation; SEA-PLM 2024 PA18A–D candidate; CIEFR-HS/CEPS/CFPS expenditure/withholding) and published
estimates as baseline. **No engine result is evidence about the world**; no empirical result is used to validate the
engine's calibration. The data portfolio's binding limitation (HK-vs-PH own-vs-firm unobserved) is recorded; Paper C's
empirical leg is feasible-partial (participation), theory-only for withholding/S/learning decomposition.

## 6. Compute envelope

Screening: 36 cells × 8 seeds × N=600 ≈ 288 runs ≈ **2.2 CPU-h at 8 workers**; confirmatory (passing cells) × 16 seeds
× N=1500, capped at **≤4 CPU-h**; diagnostic rerun separate (1,280 runs ≈ 35 min, DIAGNOSTIC-ONLY). Total ≤ ~7 CPU-h
box, scheduled only after G2-B and Codex review.

## 7. Prereg checklist (12 items, per `MODEL_ZOO_DISCRIMINATORS.md`)

engine pin + core sha / spec sha / runner sha; cells/seeds declared; primary outcome per test; predicted signs + minimum
effects; decision + indeterminate rules; binding assertions; contamination declarations; evidence layering; negative
result preservation; compute envelope; no post-hoc cells; no confirmatory use of Pilot-0.
