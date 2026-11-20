# TUNE_LOG — v1.5 **BIMODAL-GATE**: what happened, in the order it happened

**`LABEL: SYNTHETIC`.** This is an unflattering build history, kept because the difference between a *bug fix* and a
*declared choice* and a *calibration* is the whole evidential value of a predeclared run. Nothing in
`PRE_DECLARATIONS.md`, `PARAMETERS.csv`, `DESIGN.md` or `DRY_RUN_PLAN.md` was edited; all four hash identically to the
frozen originals (`7178e3d2…`, `72327cf7…`, `db21055b…`, `46603905…`).

---

## 0. Freeze point (read this first)

| | |
|---|---|
| **Scored run** | the final full run, `code/sim_v1_5_bimodal.py` sha256 **`2b699c6b…`**, ≈32 s wall (two complete runs + guards) |
| **After that run began** | **no parameter, threshold, band, year set, κ value, arm, column or verdict word was changed** |
| **Runs before it** | smoke and bug-fix runs only; `results/` was rebuilt from scratch for the scored run |
| **Every bug fix** | re-ran **all four principal arms and all ten declared extras**, and re-verified the A00 guard from zero |
| **Prohibited and not done** | no re-fit, no re-tune, no rescue of a MIXED/FAIL, no arm or threshold added, no fitting to any observed series, no "demand falsified" language |

**One disclosed post-run edit, for completeness.** After the first complete scored run I added a `documents` section to
the *manifest writer* (to record the `FINDINGS.md` / `TUNE_LOG.md` hashes). That changed the code hash
(`94e076a1…` → `2b699c6b…`) and forced one more complete run. **No model logic, parameter or threshold was touched:**
A00 still hashes `47d4b082…`, every check statistic and every verdict is identical, and the full guard suite re-passed.
It is recorded here rather than hidden because a changing code hash is exactly what a reader should be able to see.

---

## 1. What was seen **before** anything was built (arithmetic from frozen files only)

Done first, read-only, because the predeclaration told me the bars and I wanted to know where they sat:

1. The base four-state utilities for `SYN00_PHL_LIKE` at `y_med` (level 2): `U_school = 0.2240`, `U_both = 0.3461`,
   `U_work = 0.0677`, `U_neither = −1.0357` — and my replication of them matched `state_shares()` exactly (this became
   audit T-AUD-5).
2. `p₄ = rung4_emp/rung4_demand` for the anchor, 2010–2024: median **0.1544** — consistent with V8's 0.151, so
   (a-iii)'s `p₄ ≤ 0.50` leg was never going to discriminate.
3. **The (c-iii) open-tier leg would fail, before a line of v1.5 existed.** At the open tier `R_O = 1`, `V_O = 0`,
   `dpi = 0`, the demand equation sits in the logit's left tail (`D_O = 0.0074`), where a **doubling of R is a ×4
   proportional shift, not ×2**: `D_O(2) = 0.0290`, i.e. **+2.16 pp** against a declared `≤ +1.0 pp` bar. That was
   noted before the build and is reported as a property of the declared bar, **not** as something discovered later.
4. **The tier quality channel would break (b), before the build.** `q_O_mult = 0.55` with `surv = surv_max·Q^θ` gives
   `surv_O ≈ 0.5`; with 60–85 % of places in Tier O, primary completion could not exceed ≈55 pp, so (b-i)'s 92 pp bar
   was unreachable. The predeclaration expects **(b) = MIXED**; my pre-build arithmetic said **FAIL**. I implemented the
   declared equations exactly and did not touch `q_O`. **This prediction is recorded here so that the FAIL cannot be
   read as a post-hoc story, and equally so that it is not mistaken for a result that was engineered.**
5. `κ × comp_uis_lower(2021) = 0.949 × 67.4073 = 63.9695`, and `required lower 2021 = 76.6391/0.949 = 80.76` against
   the generator's 67.4073.

---

## 2. Build method (and why it is unusual)

The year loop of `simulate_country_v15()` is **injected verbatim** from the frozen `base_v1_3_sim.py`
(lines 651–748, 750–780, 784–823, 825–864, 866–988) by `code/build_from_base.py`, with the declared insertions I2–I7
added around it. Reason: the A00 guard demands byte-identity, and retyping 350 lines of numerical code is exactly how
a silent re-fit gets in. The only textual change inside the injected tail is the I7 rung-4 candidate restriction,
which is inert when `bimodal = False`.

**Consequence:** the A00 panel is byte-identical (`47d4b082…`) **and** an independent cross-check — running the frozen
base code directly (`base_v1_3_sim.run_all`, the v1.3 procedure) — produces the same hash. Two independent paths, one
hash.

---

## 3. Bugs found (all before the scored run; each fix re-ran everything)

| id | bug | how it surfaced | fix | disclosed? |
|---|---|---|---|---|
| **B2** | `run_arm` resolved the shadow hosts **after** simulating, so the shadow block never ran in any arm | first A00 test returned `88ee2294…` instead of `47d4b082…` | rebuilt on the frozen v1.3 two-pass procedure: a shadow-**blind** pass resolves the host rule, the scored pass runs with the shadow block on for `SYN28` / `SYN00_PHL_LIKE` / `SYN18` | yes — it changed the panel of every arm |
| **B3** | **the declared second decision was missing.** `tier_choice()` returned the cells that ranked Tier O *first*, so `T_O` counted only those. Households refused at the Tier H gate were never offered Tier O | first A11 inspection showed `A_O ≡ 0` and `T_O ≡ 0` at **every** level and year, with unfilled share 1.000 everywhere | implemented `tier_allocate()`: rank admission at H (S06), then for each refused H-first cell `U_O > u_out` → accept O, capped by `K_O` — exactly DESIGN §3's "second decision" | yes — this is a *mechanism*, not a detail; without it the model has no coexistence at all |
| **B4** | `kappa_cap_audit.csv` published `slack_pp` **100× too large** (a double `×100`: `100·κ·(100·comp_uis)`) | spotted by eye reading the audit table (5 055 pp of slack is not possible) | fixed the units; the verdict-bearing violation count was computed in a **separate** correctly-scaled function and was 20/53 → 0/53 both before and after the fix | yes — the audit CSV was wrong for one run and is now right |
| **B5** | `same_level(p00)` passed a *list* instead of the index, crashing the check assembly | traceback | pass `ix00` | no output affected |
| **B6** | a `KeyError` in the κ bind-cell table for upper rows differing in 1970–1972, whose `lower(t−3)` does not exist | traceback | those cells are marked `not_scorable = 1` with `kappa_bound = −1`, never imputed | yes |

**Process error B1 (the one that left a mark).** Smoke runs during the build called the SHA256SUMS generator, which
rewrote `SHA256SUMS.txt`; the pre-run snapshot I had taken was then lost when `results/` was rebuilt. The snapshot in
`results/FROZEN_BEFORE_SHA256SUMS.txt` is therefore a **reconstruction** of the original 33 `(sha256, path)` pairs,
transcribed verbatim and re-verified against the on-disk files (**30/33 still match**; the three exceptions are the two
files the run updates by design and `08_council/DECISIONS.md`, edited outside this worker's scope at 00:05). The
original file's own sha256 (`89638b39…`) is recorded in `RUN_MANIFEST.json` and in `results/guard_report.json`, and the
disclosure is duplicated there. **No frozen input hash was altered or repaired.**

---

## 4. Declared choices made at build time (not calibrations — nothing was fitted to any output)

Each of these is a place where the frozen text is silent, ambiguous, or arithmetically under-determined. Each was
decided on the frozen text **before** the arm was run, and none was revisited after seeing a number.

| id | choice | why | what the alternative would have done |
|---|---|---|---|
| **D1** | outside refusal set = `max(U_work, U_neither)`; `U_both` excluded | `U_both` is the block's school+work state — a **school** state (`ds = p_s + p_b`). As an *outside* value it grants the schooling value plus earnings **without a place**, and dominates Tier O in **15/15** cells every year | including it gives `T_O ≡ 0` everywhere, enrolment = `h_share·seats`, primary 2024 ≈ **16 pp**, and (a) vacuously true. The affected-cell count is published per country-year-level (`both_would_dominate_cells`, 15 for L=0–2 in 2024) rather than dropped |
| **D2** | outside option evaluated at each cell's own `y_i` | the block is a function of household income; a lattice of 15 households means 15 income arguments. Equations and parameters unchanged | at `y_med` for all cells, poor cells refuse more; (b) still fails, so the verdict is insensitive |
| **D3** | tertiary tier composition inherits the same-year upper-secondary choice shares | the frozen child block is **undefined at L=3** (`AGE_W` and `cost_base` each have three entries), so no honest equilibrium exists there; the aggregate stays the model's own tertiary demand | applying the child block at L=3 would be a category error (adult decision) and would inflate tertiary enrolment |
| **D4** | `D_O` at the open tier's gate state (`R_O = 1`, `V_O = 0`, `dpi = 0`) — the v1.3 `g0` control | §9 itself uses `D_g0(2020) = 0.0128` as the (c-i) baseline and reuses the `0.025` c3 ceiling that applies to `D_g0`; the open tier carries no positional credential (`cred_prem_O = 0.03`, "confers no rung-4 rank") | using the high-gate intercept `a_g` at `R = 1` gives `D_O ≈ 0.056`, which fails (c-ii) outright; using `V_O > 0` makes the open-tier gap worse |
| **D5** | when the κ cap binds, the cut runs over-age → Tier H → Tier O | keeps `V_O` a *household* object: cut Tier O first and the cap itself would manufacture unfilled places, breaking the single most important accounting commitment (§3, T-AUD-3) | cutting Tier O first would corrupt the (a-i) statistic |
| **D6** | the κ cap is a **rate** comparison (`adm_upper ≤ κ·comp_lower`), not a count comparison | §3.1's algebra writes upper completion as `m·adm_upper(t−3)·surv`, so `adm_upper` must carry completion-rate units | the count reading binds in **0 of 53** cells (the cap never acts) and leaves **20/53** completion violations. **No reading satisfies both (e-ii)(3) and (d-ii)'s non-binding leg** — this is stated in FINDINGS §4 and is a property of the frozen spec, not of the code |

---

## 5. What was seen after the build, in order, and what was done about it

1. **Coexistence appeared as soon as B3 was fixed** — unfilled upper-secondary shares of 0.65–0.93 against queue ratios
   of 1.29–1.93 — and was **left alone**. No attempt was made to raise Tier O take-up, soften the unfilled share, or
   "improve" the (a) statistics.
2. **Primary completion came out at 51.6 pp** on the same run (Tier O survival 0.508). This was the pre-build
   prediction in §1.4 and was **not** re-tuned: `q_O_mult` stayed at 0.55, `surv_theta` untouched, the completion
   weighting untouched. (b) FAILs and the FAIL is the finding.
3. **The κ cap binds in all 53 scored cells** in the rate reading. (d-ii)'s third leg fails. Recorded, not "fixed" by
   switching to the count reading, which would have failed the harder guard (e-ii)(3) instead.
4. **The child-wage ablation came out with the wrong sign (+1.08 pp)**: with the cap fixing total upper entry, the
   shock can only move the H/O composition. (d-iii) fails. Not rescued.
5. **`KAPPA-GUARD-FAIL` on tertiary (and, through the economy columns, on every level).** The frozen pipeline routes
   upper graduates into the tertiary pool, the rung-matching pool and formal employment. Only 180/5 040 non-upper rows
   stay cell-identical. Per §6(e-ii) the pipelink result is recorded **INVALID**. I did **not** re-implement the cap as
   a post-hoc projection to pass the guard — that is the exact move EXP-7 ruled out.
6. **`08_council/DECISIONS.md` changed during the run** (`6fdcf8ee…` → `59696b81…`), outside this worker's write scope
   and outside E3's declared scope. Reported, not repaired, not used to excuse anything.

---

## 6. What I would have done differently, and what I did not do

- **Would do differently:** snapshot `SHA256SUMS.txt` into a directory the build cannot touch (B1) and add the
  "second decision" path to the first sketch rather than the third iteration (B3). Both cost a rebuild.
- **Did not do, deliberately:** change `q_O_mult`, `h_share`, `surv_theta`, the completion weighting, the (b) bands,
  the (a-iv) arm, or κ; add an arm; re-score A3-D's `c4a`/`c4b`; fit anything to 75.025 or to `[73,77]`; infer a
  reversal diagnostic from R1's zero hits; invent a seat-utilisation number.

---

## 7. Runtime and determinism

| step | time |
|---|---|
| one arm (two passes: shadow-blind + scored) | ≈1.2 s |
| 4 principal arms + 10 declared extras | ≈15 s |
| checks, audits, tables, guards | ≈2 s |
| determinism double-run (second complete pipeline) | ≈14 s |
| **total** | **≈32 s** |

Determinism: two complete runs into `results/` and `results/determinism_run2/`, **14/14** result files byte-identical
(`cmp` + sha256). Seed `20261120`, one `PCG64` stream, the frozen v1.2 draw order, the tier block draws no random
numbers, floats `%.10g`, no timestamp, hostname, PID or wall-clock enters any output.

---

**`LABEL: SYNTHETIC` — build history only — not evidence — no causal or direction claim — no reversal diagnostic
inferred.**
