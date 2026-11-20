# PRE_DECLARATIONS — EXP-9 **RUNG-PROB**

**Programme:** Dr. Trey Menefee massification research programme, cycle 14.
**Experiment:** EXP-9 RUNG-PROB (Council brief 022, D122 #4, rank #4).
**Worker:** RP9. **Directory:** `10_massification/extensions/rung_prob_2026-11-20/`.
**LABEL: SYNTHETIC.** Every generator number below is synthetic. Not evidence, not an estimate,
not a forecast, **no causal and no direction claim**; no real country is modelled or measured.

**Status:** frozen before the first scored run. This file is hashed; `code/run_rung_prob.py`
records the hash and refuses to run if this file changes. The definitions, thresholds, band,
ablation bar, arm rules, fallback rule and verdict vocabulary below may not be changed after any
result is seen.

---

## 1. Provenance

This pre-declaration implements, without change, the Council's EXP-9 block in
`08_council/brief_022/SYNTHESIS_022.md` §6 and the V8 measurement in §2. Both are reproduced
**verbatim** below so that the operational rules in §4–§8 can be checked against their source.
The experiment is a **new declared object** (D116), not a rescue of A3-D.

### 1.1 EXP-9 block, verbatim (SYNTHESIS_022.md §6, lines 394–419)

```text
### EXP-9 — **RUNG-PROB**: is the ceiling demand-derivable from the probability the model actually has? (rank **#4**)

1. **First-order link (markets + schooling at the destination).** Whether the demand block was mis-wired rather than
   wrong: A3-D replaced the taste parameter with the **school-gate** probability (**≈0.999**), while the model's binding
   probability is **rung-4 absorption** (**0.151** in the anchor type) — a **6.6×** domain error (V8).
2. **What changes if positive vs negative.** **Positive** (either probability reproduces upper 2024 within
   **[73,77] ± 2 pp** with no other change) → the ceiling is **demand-derivable**; a v1.5 demand block is licensed as a
   declared, ablation-tested layer. **Negative** (both overshoot or undershoot) → **the ceiling is not demand-derivable
   from any probability in this parameterisation**; the **A3 line is KILLED**, not parked, and the taste parameter is
   recorded as irreducible without a fit. Both outcomes end the parked state.
3. **Why it is not a niche.** It is the only test that can distinguish "demand does not matter" (A3-D's reading) from
   "demand was pointed at the wrong probability" (V8's reading) — and the answer decides whether the markets channel of
   the first-order question is implemented in the generator at all.
4. **Data on disk.** Frozen `generator_v1_4_demand/` code + `results/DETAIL.csv` (`p`, `P(advance)`, `E[R]`,
   `v_D`, `demand_share`); `synthetic_panel_v1_2.csv` (`rung4_demand`, `rung4_emp`, `demand_share`). **No DATA ASK.**
5. **Threshold + falsifier.** Two arms, each a single declared substitution, all else frozen, baseline guard
   byte-identical: **arm A** uses `P = pi0(g2)` (≈0.999); **arm B** uses `P = rung4_emp / rung4_demand` (≈0.151).
   `DEMAND-DERIVABLE` iff an arm's upper 2024 lands in **[71,79]** (band ± 2 pp) **and** the arm's ablation moves 2024
   by **≥3.0 pp** (D81). Re-derived expectation: arm A overshoots (**+18.41**) — already measured — so the informative
   arm is B, which must **undershoot** by arithmetic (0.151/0.999 ≈ 0.15× the return). **Falsifier:** if both arms fall
   outside [71,79], `NOT DEMAND-DERIVABLE`; the A3 line is KILLED and no further demand re-specification is admitted
   this phase.
6. **Closed-claim check.** Not a rescue of A3-D's verdict (that stands as FALSIFIED); a **new declared object** as D116
   required; no fitted demand parameter (R4/R27); no direction claim; the migration/remittance channel remains
   DECLARED/NOT-VERIFIED and is not used.
7. **Cost / rank.** **Medium.** **Rank #4.**
```

### 1.2 V8, verbatim (SYNTHESIS_022.md §2)

```text
| **V8** | **The model's queue is at the top *job* rung, not at the school gate.** Rung-4 absorption `p₄ = rung4_emp/rung4_demand` (2010+, upper-secondary rows): `SYN00_PHL_LIKE` median **0.151** (0.110–0.189), `SYN28` **0.177**, `SYN18` **1.000**; panel median **0.507**. The upper-gate advance probability is **≈0.999**. The demand block (A3-D) was wired to the 0.999 quantity, not to the 0.15 quantity — a **6.6×** domain error, and the concrete meaning of "model the office rung queue". | 0.151 / 0.177 / 1.000; 0.999 vs 0.151 | `synthetic_panel_v1_2.csv` (`rung4_demand`, `rung4_emp`, `demand_share`); `generator_v1_3/results/shadow_gates_v1_3.csv` (`pi0`, `Q`) |
```

### 1.3 Frozen inputs (read-only; hashes recorded in `RUN_MANIFEST.json`)

| item | path | role |
|---|---|---|
| v1.4 generator | `synthetic_2026-11-20/generator_v1_4_demand/code/sim_v1_4_demand.py` (`6e4a6761…`) | the code being bracketed; copied byte-identically into `code/frozen_v1_4/` |
| v1.3 base code | `…/generator_v1_4_demand/code/base_v1_3_sim.py` (`70ae8f0e…`) | untouched; the OFF arithmetic |
| v1.4 predecl | `…/generator_v1_4_demand/PRE_DECLARATIONS.md` (`9ed0cae3…`) | frozen A3-D spec (not edited) |
| v1.4 ON panel | `…/generator_v1_4_demand/results/synthetic_panel_v1_4_demand.csv` (`ffecd450…`) | baseline guard G2 |
| v1.4 OFF panel | `…/generator_v1_4_demand/results/_ablation/synthetic_panel_v1_4_demand_off.csv` (`47d4b082…`) | baseline guard G1 / ablation OFF |
| v1.2 panel | `synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv` (`14729c51…`) | the arm-B probability source (`rung4_demand`, `rung4_emp`) |
| v1.3 shadow gates | `…/generator_v1_3/results/shadow_gates_v1_3.csv` | read-only cross-reference for V8 (not used in the substitution) |

The frozen v1.4 code is **copied byte-for-byte** into `code/frozen_v1_4/`; its own path constants
are re-pointed at the frozen read-only directories by the runner. No line of the copied code is
edited. The substitution is applied at run time by replacing the module's `demand_values` symbol
with a wrapper that changes exactly one argument (see §4.2); the frozen text is never touched.

---

## 2. The question

**Is the ceiling demand-derivable from the probability the model actually has?**

A3-D replaced the declared taste parameter with the **school-gate** probability `P(advance) ≈ 0.999`
and produced upper 2024 = **95.04548615** (**+18.4064 pp** vs the demand-OFF baseline
**76.63908112**). V8 shows the model's binding queue is at the top **job** rung, not the school
gate: rung-4 absorption `p4 = rung4_emp / rung4_demand` has anchor-type (`SYN00_PHL_LIKE`) median
**0.151** (0.110–0.189), while the upper-gate advance probability is **≈0.999** — a **6.6×** domain
error. EXP-9 substitutes each candidate probability, one at a time, into the **same** frozen v1.4
demand block and asks whether either reproduces the ceiling in **[71,79]** while remaining
ablation-live. Nothing else changes.

---

## 3. Scored object, band, ablation bar (verbatim criteria)

- **Scored object:** `SYN00_PHL_LIKE` upper-secondary **UIS-convention completion in 2024**
  (`completion_uis × 100`, i.e. `m = 1.10` times the cohort-flow series). This is the same object
  v1.2/v1.3 check (a) and v1.4 §6 score.
- **Band:** **[71.0, 79.0]** inclusive (= [73, 77] ± 2 pp). `in_band` iff
  `71.0 <= upper_2024 <= 79.0`.
- **Ablation (D81):** for each arm, `Δ_pp = upper_2024(arm ON) − upper_2024(OFF)`, and the bar is
  **`|Δ_pp| >= 3.0 pp`**. `>= 3.0` → `NON-DECORATIVE`; `< 3.0` → `DECORATIVE`. The OFF state is
  the unmodified demand-OFF v1.3 world (upper 2024 = **76.63908112**).
- **Arm verdict:** an arm is **`DEMAND-DERIVABLE`** iff its upper 2024 is in band **and** its
  ablation clears the bar. Otherwise the arm is **`NOT DEMAND-DERIVABLE`**.
- **Overall verdict:** **`DEMAND-DERIVABLE`** iff the baseline guard passes and **at least one**
  arm is `DEMAND-DERIVABLE`; **`NOT DEMAND-DERIVABLE`** iff the guard passes and no arm is
  `DEMAND-DERIVABLE`; **`guard-fail`** iff either guard check fails (in which case no arm is
  scored). No other outcome string is permitted.
- **Falsifier flag:** `both_arms_outside_band = TRUE` iff both arms' upper 2024 values lie outside
  [71.0, 79.0]. Per the block, this is the `NOT DEMAND-DERIVABLE` / **A3 line KILLED** condition.
  A single arm outside the band does not by itself kill the line if the other arm is in band and
  ablation-live.

---

## 4. The two declared arms — one substitution each, all else frozen

Both arms run the **same** frozen v1.4 code (byte-identical copy), the same one PCG64 stream
(`seed = 20261120`, inherited from v1.2/v1.3/v1.4), the same 30 synthetic countries, the same
declared parameters, the same host mapping and the same `%.10g` formatting. The only difference
between an arm ON and the demand-OFF run is the arm's single probability substitution at
`L = 2` (upper secondary), the level the v1.4 replacement arm already occupies.

### 4.1 Arm A — school-gate probability `P = pi0(g2)`

`P(advance at L=2) := pi0(g2)`, the frozen code's own gate advance probability for upper-secondary
entry, read from the previous year's realised gate state exactly as the frozen block already does.
**No code change and no substitution are made: arm A is the frozen v1.4 replacement arm.** The
expected value is the A3-D measured value, `95.04548615`; it is re-derived here, not assumed, and
its panel must pass guard G2.

### 4.2 Arm B — rung-4 absorption `P = rung4_emp / rung4_demand`

`P(advance at L=2) := rung4_emp / rung4_demand`, read from the **frozen v1.2 panel**
(`synthetic_panel_v1_2.csv`) for the same synthetic country and the same calendar year, and
substituted for `gs[2]["pi0"]` inside the frozen `demand_values()` only.

- **Single substitution.** The wrapper copies the gate-state dict, replaces `gs[2]["pi0"]` with the
  panel ratio, and calls the frozen `demand_values()` unchanged. Consequently `P` enters exactly
  where the frozen block reads `p_adv`: in `gross`, in `ER_P`, and hence in `v_D`; all other
  arguments (`w_for`, `w_inf`, `J`, `hires`, `queue`, `R_gate`, cost, foregone, migration and
  remittance terms, `B_Z_D`, `ER_floor`, lag) are frozen. **`R_gate` is not changed** — only `P`
  is substituted. No random draw is made by the substitution.
- **Year alignment.** `demand_values()` is called exactly once per country per year. The wrapper
  infers the calendar year from that exact, deterministic call order (1970 … 2025; 56 calls per
  country) and asserts, after the run, that `D_padv[2, t]` equals the panel ratio in every
  country-year where the ratio is defined. A mismatch is a hard error, not a reportable value.
- **Definedness / fallback (declared before the run).** The panel ratio is defined where
  `rung4_demand > 0`. Where `rung4_demand == 0` (the country-year has no rung-4 job queue, so the
  model has no rung-4 absorption to substitute), the wrapper **leaves `pi0(g2)` in place** — the
  model's own gate probability — and records that cell as a fallback. The fallback affects
  **100 of 1 680** country-years (all before 2006) and **zero** `SYN00_PHL_LIKE` years; it is
  therefore **inert for the scored anchor**. This rule is part of the arm definition and may not be
  changed after the run.
- **No clipping or re-scaling.** The panel ratio lies in `[0.0002628, 1.000]`; it is used as-is
  (no 0.999 clip, no re-scaling). Values equal to 1.000 are the model's own numbers.

### 4.3 What is *not* an arm

No third arm, no re-specification, no `ER_scale`, no re-tuning, no change of destination set,
migration value, `H`, `B_Z_D`, band, tolerance, seed or scored object. Arm A and arm B are the
complete set. A negative result may not be met by adding an arm or moving a threshold after the
fact.

---

## 5. Baseline guard (byte-identical, mandatory)

Both checks are on files written by the runner's own unmodified run:

- **G1 (OFF).** The demand-OFF panel (`dem=False`) must have
  `sha256 == 47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3`
  (frozen v1.3 panel; also the frozen v1.4 `_ablation` OFF panel).
- **G2 (ON, unmodified).** Arm A's demand-ON panel (`dem=True`, no substitution) must have
  `sha256 == ffecd450514cf8259512647db4e78bcd058639c208a1a2057bbac8b506ddbdaa`
  (frozen v1.4 `synthetic_panel_v1_4_demand.csv`).

**Guard PASS iff G1 and G2.** A mismatch is `guard-fail`: the arm values are reported as
`VOID`/unscored, and the experiment reports `guard-fail`, not a demand verdict. The guard is the
analogue of v1.3 c6 and v1.4 §7a.

---

## 6. Expected direction — declared before the scored run

- **Arm A** is expected to **overshoot**: A3-D already measured upper 2024 = **95.04548615**,
  **+18.4064 pp** vs OFF, and **+18.0455 pp above the band edge**. It cannot be in band.
- **Arm B** is expected to **undershoot** by arithmetic: `0.151 / 0.999 ≈ 0.15×` the return, so
  the demand signal is roughly an order of magnitude smaller and upper 2024 should fall below 71.
  The informative arm is B, for the reason the block states.
- **Expected overall verdict: `NOT DEMAND-DERIVABLE`; expected disposition: the A3 line is
  `KILLED`, not parked; the taste parameter is recorded as irreducible without a fit.** A negative
  is the **expected** outcome and is reported as such. It is a successful execution of the bracket
  test, not a failed experiment.

---

## 7. No-threshold-change rule

After the first scored run: no band edge (71/79), tolerance, ablation bar (3.0 pp), scored object,
arm definition, substitution rule, fallback rule, seed, code path or formatting rule may be
changed. No parameter of the frozen v1.4 code or of the frozen v1.2 panel may be re-tuned. No
fitted demand parameter may be introduced (R4/R27). Only a coding error that makes the code
disagree with this document may be corrected, and only with the before/after hash recorded in
`TUNE_LOG.md`; no value may be changed to rescue an outcome.

---

## 8. Closed-claim check (binding)

- **A3-D's `FALSIFIED` verdict stands.** EXP-9 is **not** a rescue, re-score or re-run of A3-D; it
  is a new declared object as D116 required. The A3-D numbers are used only as the arm-A result.
- **No fitted demand parameter (R4/R27).** Nothing is chosen by looking at `[71,79]`; the band and
  the bar come from the block and are copied verbatim. The arm-B probability is a frozen panel
  column, not a fitted value.
- **No causal or direction claim.** The result is about a declared synthetic generator, not about
  any real education system or labour market.
- **Migration / remittance:** remains **DECLARED / NOT-VERIFIED**; no literature coefficient is
  inserted, and the channel is **not used** to explain any result. The substitution does not touch
  the migration or remittance terms.
- **Language ban.** The phrase "no demand falsified" (or any equivalent) must not be used. What
  failed in A3-D was the demand channel's **specification** — a demand block pointed at a
  non-binding gate — **not demand as a phenomenon**. Demand is revealed and strong; the generator's
  single-gate household block has no dimensionally neutral slot for it.
- **Scope.** No C1–C4 reopening; no WT/DT cell re-run; no paper-test slate; D63 remains `UNABLE`
  as to cause; the phase verdict is untouched.

---

## 9. Outputs and determinism

- `results/RUNG_PROB_RESULTS.csv` — per-arm (and OFF/overall) upper 2024, in-band, distance,
  ablation, verdict, anchor components.
- `results/RUNG_PROB_ARMS.csv` — per-country/per-year `L=2` detail for both arms and the OFF
  baseline (the cells behind the aggregate).
- `results/BASELINE_GUARD.json` — G1/G2 hashes and byte-identical booleans.
- `results/determinism_run2/` — a second clean run; every result file must `cmp` byte-identical to
  run 1.
- `RUN_MANIFEST.json`, `SHA256SUMS.txt`, `FINDINGS.md`.

Determinism: one PCG64 stream (`seed = 20261120`); no RNG in the substitution; floats at `%.10g`;
no wall-clock or absolute paths in outputs. Two clean runs into separate directories must be
byte-identical.

---

## 10. What this experiment does **not** test

It does not test whether demand matters, whether returns drive schooling, whether the ceiling is
demand-led in any real system, or whether some *other* demand specification (a bimodal-gate model,
a scarcity-based `P`, a different destination mapping) could reproduce `[71,79]`. It tests exactly
the block's question: whether the ceiling is demand-derivable from **either** probability the
frozen model actually has, under one declared substitution each, all else frozen.
