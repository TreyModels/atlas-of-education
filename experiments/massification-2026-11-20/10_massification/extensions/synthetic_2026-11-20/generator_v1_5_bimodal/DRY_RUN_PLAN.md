# DRY-RUN PLAN — v1.5 **BIMODAL-GATE** build plan (run-ready, **NOT EXECUTED**)

**`LABEL: SYNTHETIC` — build plan only. No model was run, no results file exists, no RNG was drawn.** This document
says exactly what a future authorised run must build, in what order, with which guards, and what it must emit. It
adds no threshold (all thresholds are in the frozen [`PRE_DECLARATIONS.md`](PRE_DECLARATIONS.md)) and no parameter
(all parameters are in [`PARAMETERS.csv`](PARAMETERS.csv)).

---

## 0. Preconditions before a single line of v1.5 code may run

| # | precondition | how it is checked | on failure |
|---|---|---|---|
| P1 | `PRE_DECLARATIONS.md` sha256 == the value in `RUN_MANIFEST.json` → `predeclaration.sha256` | the constant is embedded in `code/sim_v1_5_bimodal.py` as `EXPECTED_PREDECL_SHA`; the script refuses to start on mismatch | **refuse to run** |
| P2 | every input hash in `SHA256SUMS.txt` verifies (`shasum -a 256 -c SHA256SUMS.txt`) | shell check before execution | **refuse to run** |
| P3 | `PARAMETERS.csv`, `DESIGN.md`, `DRY_RUN_PLAN.md` hashes match `SHA256SUMS.txt` | same | **refuse to run** |
| P4 | the frozen base is byte-identical: `code/base_v1_3_sim.py` == `70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877` | copy + hash | **refuse to run** |
| P5 | a user/Council authorisation to execute exists | none exists today | **this plan stays unexecuted** |

**Authorisation status: NOT AUTHORISED.** This file, `PRE_DECLARATIONS.md`, `DESIGN.md` and `PARAMETERS.csv` are a
design + frozen pre-declaration delivery. Nothing below has been done.

---

## 1. Build sequence (files, in order, all inside `generator_v1_5_bimodal/`)

| step | artefact | work |
|---|---|---|
| 1 | `code/base_v1_3_sim.py` | `shutil.copy2` of `generator_v1_3/code/sim_v1_3.py`; hash asserted `70ae8f0e…`. **Read-only forever after.** |
| 2 | `code/sim_v1_5_bimodal.py` | new file: the switches, `tier_split()`, `tier_choice()`, `kappa_cap()`, tier survival/wage paths, tier panel columns, the A00/A01/A10/A11 arms, the checks, the guards, the audits. `EXPECTED_PREDECL_SHA` in the header. |
| 3 | `code/checks_v1_5.py` | the five checks + legs + verdict assembly; reads the emitted panels, writes `results/v1_5_checks*.csv`. **No fitting, no thresholds.** |
| 4 | `code/guards_v1_5.py` | E1–E4 and `tier_audit.csv`, `RATCHET_AUDIT.json`. |
| 5 | `code/run_v1_5.py` | the arm orchestrator (4 principal + 10 declared sensitivity/ablation arms), determinism double-run, `RUN_MANIFEST.json` for the run. |
| 6 | `results/…` | created **only** by an authorised run. |

**Discipline for step 2:** each insertion point is guarded by **one** boolean read at **one** place
(`bimodal`, `kappa_link`), never by scattered branch logic, so that arm A00's byte-identity is auditable
(T-AUD-4). No `if country == …`, no per-level hard-coded utility constant, no anchor array
(T-AUD-1/2 — the mirror of shadow `c4c`).

---

## 2. Insertion points and the order of operations inside the year loop

Ordered exactly as the loop must execute (anchors are line numbers in `code/base_v1_3_sim.py`, which equals
`sim_v1_3.py`):

```
for t in years:
  1  X, takeoff, sectors                                  :735-756   unchanged
  2  capacity: seats[L] = update_seats(...)                :757-765   unchanged
  3  q, Q, class size                                     :766-780   unchanged; then
     NEW tier_split:  K_H[L] = h_share[L]*seats[L];  K_O[L] = seats[L]-K_H[L]
     NEW Q_H = q_H_mult*Q;  Q_O = q_O_mult*Q                      (bimodal ON only)
  4  household demand                                     :782-806
     OFF -> v1.3 lines verbatim
     ON  -> tier_choice(): 15 cells x 5 states; yields A_H, A_O, OUT_work, OUT_both, OUT_neither
  5  NEW kappa cap on the upper entry cohort              (after demand, before admission)
        adm_upper <- min(adm_upper, kappa*comp_lower_cohort(t))       (kappa_link ON only)
  6  admission / rationing                                :808-824
     OFF -> v1.3 lines verbatim
     ON  -> admitted_H = min(A_H, K_H) by rank_score; T_O = min(A_O, K_O); V_O = K_O - T_O
            queue_H = A_H - admitted_H; p_adv_H = admitted_H/A_H; unfilled_share_O = V_O/K_O
  7  survival / completion                                 :826-838
     OFF -> v1.3 line verbatim
     ON  -> surv_H from Q_H, surv_O from Q_O; completion = (adm_H*surv_H + adm_O_tier*surv_O)/cohort-flow
  8  out-of-school composition                             :840-864   unchanged in form; fed by the tier decision
  9  pools                                                 :866-873   unchanged (the kappa cap is at step 5)
 10  teachers / PTR                                        :875-894   unchanged
 11  literacy / attainment / yos                           :896-911   unchanged
 12  rungs, matching, wages, growth                        :896-947
     NEW: the rung-4 slot is rank-rationed from Tier H credential holders (step 12 block);
          p4 = rung4_emp/rung4_demand is stored; Tier O holders do not enter the rung-4 rank order
 13  shadow block                                          :948-1000
     unchanged equation/parameters; NEW: also evaluate the same demand at the open-tier gate state -> D_O
 14  store                                                 :1001-1002 + NEW tier stores
```

**Why the κ cap sits at step 5 and not at step 7.** The cap must act on the **entry cohort** (`adm_upper` at year
`s`) because that is the object that flows through the 3-year duration to completion at `s+3`. Capping `comp_upper`
at step 7 would be the post-hoc projection EXP-7 rules out (`repro_path_2026-11-20/FINDINGS.md:152-166`) and would
leave the upper level **clipped**, not **inherited**.

**Cross-check that must be emitted every year:** `comp_uis_upper(t) ≤ κ·comp_uis_lower(t−3)` (implied by the cap);
a single violation in the 53 scored cells is `KAPPA-GUARD-FAIL`.

---

## 3. Arms and what each writes

| arm | switches | output file | scored? |
|---|---|---|---|
| A00 | bimodal OFF, κ OFF | `results/panel_v1_5_A00_v13cols.csv` (v1.3 columns **only**, v1.3 order, `%.10g`) | guard E1 |
| A10 | bimodal ON, κ OFF | `results/panel_v1_5_A10_bimodal_noKappa.csv` | **no** (diagnostic, reported) |
| A01 | bimodal OFF, κ ON | `results/panel_v1_5_A01_linked.csv` | guard E2 only |
| A11 | bimodal ON, κ ON | `results/synthetic_panel_v1_5.csv` | **yes** (a)–(e) |
| S1–S2 | `h_share ± 0.10` (A11 otherwise) | `results/SENSITIVITY.csv` rows | no (bars reported; (a) magnitudes) |
| S3–S4 | `q_H_mult ∈ {1.10, 1.40}` | `results/SENSITIVITY.csv` rows | no |
| S5–S6 | `q_O_mult ∈ {0.40, 0.70}` | `results/SENSITIVITY.csv` rows | no |
| S7 | `κ = 0.960` | `results/SENSITIVITY.csv` row | no (explicitly non-verdict) |
| D1 | child wage +10 % | `results/ABLATIONS.csv` row | **yes** (d-iii) |
| D2 | Tier O quality −20 % | `results/ABLATIONS.csv` row | **yes** (d-iv) |
| D3 | sorting OFF (uniform weights; single tier within the κ cap) | `results/ABLATIONS.csv` row | reporting only (context for (d)) |

All arms share seed `20261120`, one `PCG64` stream, the v1.2 draw order; **the tier block draws nothing**, so the arm
differences are entirely deterministic parameter/switch differences.

---

## 4. Expected outputs (the run's contract)

### 4.1 `results/v1_5_checks.csv` — one row per check

```
check, expected_pattern, synthetic_value, threshold, verdict, legs_passed, legs_failed, scope_note, label
a, "untaken Tier O places AND Tier H queues in the same country-year", "...", "sec.6 a", PASS/FAIL/MIXED/UNDETERMINED, "...", "...", "D119 scope line", SYNTHETIC
b, ...
c, ...
d, ...
e, ...
ALL, "combined verdict (precedence FAIL > MIXED > UNDETERMINED > PASS)", "...", "...", ..., ..., ..., ...
```

`verdict` may contain **only** `PASS`, `FAIL`, `MIXED`, `UNDETERMINED` (`PRE_DECLARATIONS.md` §7). `scope_note`
carries, verbatim, the D119 line: *"v1.3 levels are a 2021–2024 placement, 24–37 pp low before 2021; 9/33 within
±5 pp; EXP-7 leg (a) = ENDPOINT-ONLY; statement readable as a 2022–2024 placement only."*

### 4.2 The other required tables

| file | one row per | required columns |
|---|---|---|
| `results/v1_5_checks_detail.csv` | check leg | `check, leg, statistic, value, threshold, holds, n_cells, note` |
| `results/BIMODALITY_CELLS.csv` | scored `(t, L)` cell (30 rows) + the job-gate years | `year, level, K_O, T_O, V_O, unfilled_share_O, A_H, K_H, queue_H, queue_ratio_H, p_adv_H, p4, rung4_emp, rung4_demand` |
| `results/TIER_PANEL_tabs.csv` | country-year-level (6 720) | `country, year, level, tier, seats, K_H, K_O, q, Q_H, Q_O, takeup_O, unfilled_O, unfilled_share_O, admitted_H, queued_H, p_adv_H, p4, wage_H, wage_O, cred_prem_H, cred_prem_O, exit_cost_O` |
| `results/synthetic_panel_v1_5.csv` | country-year-level (6 720) | v1.3's 89 columns + `tier` columns + `kappa_bound, kappa_binds, slack_pp` |
| `results/ABLATIONS.csv` | declared ablation | `arm, object, baseline_value, ablation_value, delta_pp, bar_pp, holds` |
| `results/SENSITIVITY.csv` | declared sensitivity cell | `arm, parameter, value, statistic, value_observed` |
| `results/BASELINE_GUARD.json` | guard | `sha_A00, sha_v1_3, match, columns, rows` |
| `results/KAPPA_GUARD.json` | guard | `cell_identity_counts, bind_cells, violations_before, violations_after` |
| `results/KAPPA_BIND_CELLS.csv` | differing upper row | `country, year, upper_unlinked, kappa_bound, upper_linked, delta_pp` |
| `results/FROZEN_FILE_GUARD.json` | frozen file | `path, sha_before, sha_after, unchanged` |
| `results/RATCHET_AUDIT.json` | audit | `tokens_searched, hits, tstate_monotone_all_countries, opened_rungs_monotone` |
| `results/tier_audit.csv` | audit | `audit_id, rule, hits, status` (T-AUD-1..4) |
| `results/console.txt`, `results/determinism_note.md` | run | plain text |

### 4.3 The report format (what a FINDINGS file must contain, in this order)

1. **The answer in two sentences** — one for the *coexistence* object, one for the *pipeline* object.
2. **Verdict string** — `a=…; b=…; c=…; d=…; e=…; ALL=…` plus the guard statuses (`BASELINE-GUARD-…`,
   `KAPPA-GUARD-…`, `FROZEN-FILE-GUARD-…`, `DETERMINISM-…`).
3. **Every leg, passed or failed**, with its number and its bar, including the legs that were expected to fail
   ((b-iii) endpoint; (a-i) arithmetical caveat).
4. **The two ablations that carry the weight** — (d-iii) child wage and (d-iv) Tier O quality — reported **before**
   any interpretation, because a non-moving ablation makes a PASS non-diagnostic (D81).
5. **The D119 scope paragraph** and the statement that a synthetic PASS says nothing about the Philippines.
6. **A "what this does not say" block**: no causal claim; no direction claim; C1–C4 not reopened; A3-D not
   re-scored or re-tuned; the ceiling remains `UNABLE as to cause` (D63); the ratchet is theory and **no reversal
   diagnostic is inferred**; the HELD data are still HELD.
7. **A "what would change the verdict" block**, declared in advance: only a *new* predeclaration (new object, new
   bars) — never a re-run of this one.

**Banned in the report:** "demand falsified" and all paraphrases. Correct label: **"the unrationed single-gate
model cannot represent a bimodal system."**

---

## 5. Runtime estimate (declared; not measured, because nothing ran)

| component | estimate | basis |
|---|---|---|
| one arm, 30 countries × 56 years × 4 levels | **3–6 s** | v1.2 measured ≈0.6 s (`generator_v1_2/PARAMS.md` §1); v1.5 adds 15 cells × 5 states × 4 levels × 56 y = 16 800 utility evaluations per country (15 × 5 × 4 × 56 = 16 800; × 30 = 504 000 total) with no RNG |
| 4 principal arms | ≈15–25 s | — |
| 10 sensitivity/ablation arms | ≈40–60 s | — |
| checks + guards + audits (panel scans, 6 720 rows × 14 files) | ≈20–40 s | O(n) CSV |
| determinism double-run (A11 twice) | +5 s | — |
| **total** | **≈1.5–2.5 min** | well inside the inherited ≤300 s per-arm contract |

If any arm exceeds 300 s the run **stops and reports** `RUNTIME-CONTRACT-FAIL`; it does not silently proceed.

---

## 6. Guard tests (verbatim, in the order they must run)

1. **E1 baseline.** Run A00; project to the v1.3 column set; assert
   `sha256 == 47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3` (and, transitively, the v1.2
   value `14729c51…acf5ac` is **not** expected here — v1.5's base is v1.3 with the shadow block ON).
2. **E2 link.** Run A01; assert (i) `primary|lower_secondary|tertiary` cell-identical to v1.3 in all 6 720 rows;
   (ii) every differing `upper_secondary` row is listed in `KAPPA_BIND_CELLS.csv` and `adm_upper` decreased there;
   (iii) `0/53` violations of the completion-ratio statement.
3. **E3 frozen files.** Re-hash every path in `SHA256SUMS.txt` under the frozen directories; assert identical.
4. **E4 determinism.** A11 twice into separate directories; `cmp` every produced file; assert identical.
5. **T-AUD-1/2.** Source audit: no level-targeted utility constant; no country-specific value of
   `h_share, q_mult, cost_mult, cred_prem, rank_weights, v_H, v_O, sigma_tier`; no `if country ==` in the tier block.
6. **T-AUD-3.** `K_H` computed from `seats` and `h_share` only; static check that no code path passes `T_O`/`V_O`
   into `K_H` (no reallocation).
7. **T-AUD-4.** One boolean read per insertion point; no nested `if bimodal` inside the rationing or matching loops.
8. **R1 ratchet.** Token scan (`restore`, `revert`, `rollback`, `return-to-prior`, target-return feedback) → **0 hits**;
   `Tstate` non-decreasing for all 30 countries; opened-rung set non-decreasing. **R1 failure ⇒ run `VOID`.**
9. **R2 monotonicity report.** Descriptive only; no inference.

**Any guard failure ⇒ the corresponding result is `INVALID` and the failure is the finding** — no re-run to pass, no
"fix and retry" without a new predeclaration.

---

## 7. What must NOT happen in the build (checklist for the builder)

- [ ] no edit to any file under `generator_v1_2/`, `generator_v1_3/`, `generator_v1_4_demand/`, `shadow_module/`,
      `repro_path_2026-11-20/`, or anywhere else in the repo;
- [ ] no threshold, bar, band, year set, κ, arm or verdict word changed after the freeze;
- [ ] no fitting, tuning, calibration run, likelihood, or "sensitivity sweep that becomes the answer";
- [ ] no per-level anchor array, no `if country ==` branch in the tier block, no level-targeted utility constant;
- [ ] no reallocation of unfilled Tier O places to Tier H;
- [ ] no sub-trend, no forecast, no causal or direction claim, no "demand falsified";
- [ ] no fabricated seat-utilisation or quality number for any real system;
- [ ] no use of a synthetic PASS as evidence about the Philippines;
- [ ] no reversal diagnostic inferred from the absence of a reversal term;
- [ ] no write outside `generator_v1_5_bimodal/`; no touch to the running server.
