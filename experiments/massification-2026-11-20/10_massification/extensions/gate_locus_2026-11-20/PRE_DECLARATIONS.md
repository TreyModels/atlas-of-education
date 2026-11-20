# PRE_DECLARATIONS — EXP-8 GATE-LOCUS

**`LABEL: SYNTHETIC`** for every generator number in this experiment. No observed data series is read, compared or
scored here.

**Experiment:** EXP-8 **GATE-LOCUS** — *where do the generator's gates actually bind?*
**Source:** Council brief 022, `08_council/brief_022/SYNTHESIS_022.md` §6, EXP-8 block (D122 #3, rank **#3**).
**Worker:** WORKER GL. **Date frozen:** 2026-11-20.
**Status at freeze:** `PRE-DECL-FROZEN` — this file is hashed (`PRE_DECLARATIONS.sha256`) **before** `code/run_gate_locus.py`
is first executed. No result file exists at the moment of the freeze.

**This is a descriptive/diagnostic audit of a declared-assumption simulator.** It makes **no causal claim** and **no
direction claim**. It is read-only on frozen panels: **no re-fit, no new layer, no re-run of A3-S**, and it does not
reopen A3-D's verdict or A3-S's `c4a` — it *explains* them. D63 remains `UNABLE as to cause`.

---

## 1. The EXP-8 block, verbatim

Transcribed from `08_council/brief_022/SYNTHESIS_022.md` lines 370–393 (the file hashes
`9508dd55be8dd64da8322a8277c8342a4f50be6790a3d287e39e7004537c109b`). The block below is inserted
programmatically from the source file and is byte-identical to it. **Every definition, bar, threshold and
falsifier used in this experiment is transcribed from here. None is invented, none is tuned.**

```markdown
### EXP-8 — **GATE-LOCUS**: where do the generator's gates actually bind? (rank **#3**)

1. **First-order link (government capacity / rationing).** Whether the generator has a *school* gate where the demand and
   shadow architecture was pointed, or only at the floor — the difference between a mis-parameterised layer and a layer
   with no home.
2. **What changes if positive vs negative.** **Positive** (upper/tertiary unrationed, primary/lower rationed — the
   re-derived state, V3) → the "ceiling as upper gate" line is **closed**; any future demand/shadow layer must be
   re-declared at the **binding** gate (g1) or the upper gate must be given a capacity constraint first; A3-D and c4a
   are explained, not rescued. **Negative** (some upper years ration hard) → the c4a failure is parameter-side and a
   re-declaration at g2 becomes admissible.
3. **Why it is not a niche.** It decides whether the user's explicit demand directive has an implementable home in this
   generator and it explains **two** delivered failures (A3-D's d2, A3-S's c4a) with one measurement.
4. **Data on disk.** `synthetic_panel_v1_2.csv`: `demand_official`, `admitted_official`, `demand_overage`,
   `admitted_overage`, `rationed_official`, `seats`, `congestion_q`, `ger`; `generator_v1_3/results/shadow_gates_v1_3.csv`:
   `Q`, `pi0`, `pi1`, `capacity`, `candidates`, `advances`. **No DATA ASK.**
5. **Threshold + falsifier.** Per level, rationing share = share of country-years with `p_off < 0.95` **and**
   `rationed_official > 0`; `GATE BINDS` iff **≥50%**, `UNRATIONED` iff **≤10%**; both the <0.95 and <0.99 bars reported.
   Re-derived: at <0.99 primary **87.4%**, lower **93.3%**, upper **6.5%**, tertiary **0%**. **Falsifier:** if any
   upper/tertiary level-year has `p_off < 0.50` in **>20%** of its years, the architecture conclusion is reversed and
   RUNG-PROB (EXP-9) is not dispatched.
6. **Closed-claim check.** Read-only on the frozen panel; no re-fit, no new layer, no re-run of A3-S; it *explains*
   A3-D's verdict without reopening it; no direction claim.
7. **Cost / rank.** **Small.** **Rank #3.**
```

**Provenance of the verbatim splice.** `code/build_predeclarations.py` reads the source lines above and writes this
file; `code/verify_predecl_verbatim.py` re-reads the frozen file and asserts the quoted block still equals the source
lines byte for byte. The splice is therefore exact, and a tampered quote is detectable.

---

## 2. Dependency precondition (brief §4.4), recorded at freeze

Brief §4.4 makes the sequencing **EXP-7 → EXP-6 → EXP-8 → EXP-9 → EXP-10** binding: *"Nothing downstream of EXP-7 may
be predeclared before EXP-7's path audit returns."* Recorded state at this freeze, read off disk:

| precondition | state | evidence |
|---|---|---|
| EXP-7 REPRO-PATH returned | **RETURNED** — `ENDPOINT-ONLY` + `b2` + `BASELINE-GUARD-PASS`, predecl `74f9d0e0…3db12` | `10_massification/extensions/repro_path_2026-11-20/FINDINGS.md` |
| EXP-6 PIPE-LOO on disk at freeze | **NOT PRESENT** — no `pipe_loo*` directory under `10_massification/extensions/` | `ls 10_massification/extensions/` |

EXP-8 consumes **no output of EXP-6** and shares **no estimand** with it (EXP-6 is an out-of-sample prediction test on
observed completion pairs; EXP-8 is a rationing-share census on the frozen synthetic panel). This predeclaration is
therefore frozen on EXP-7's return and records EXP-6's absence as a fact rather than waiting on it. If the Lead requires
strict EXP-6-before-EXP-8 ordering, this file may be held unrun without edit: **no threshold in it depends on EXP-6**.

---

## 3. Frozen inputs (read-only; declared hashes)

| input | path | sha256 | role |
|---|---|---|---|
| frozen panel | `10_massification/extensions/synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv` | `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` | **primary** — `p_off`, `rationed_official`, `rung4_*`, `congestion_q`, `seats`, `ger` |
| shadow gate panel | `10_massification/extensions/synthetic_2026-11-20/generator_v1_3/results/shadow_gates_v1_3.csv` | `df3cab007ce5fbe9a48d58b0701d04e6d762591848ca1517a634c8f897edb351` | **secondary, non-verdict-bearing** — `Q`, `pi0`, `pi1`, `capacity`, `candidates`, `advances` |
| Council brief | `08_council/brief_022/SYNTHESIS_022.md` | `9508dd55be8dd64da8322a8277c8342a4f50be6790a3d287e39e7004537c109b` | definitions, thresholds, falsifier |

The panel hash is the one the Council recorded for the frozen v1.2 panel (`14729c51…acf5ac`); the run re-verifies it and
**aborts** if it differs. **No file outside this experiment directory is written, and neither input is modified.**
**No DATA ASK.**

---

## 4. Operational definitions (fixed here, before the run)

The brief's thresholds are stated on a **"rationing share = share of country-years with `p_off < 0.95` and
`rationed_official > 0`"**. The following fixes the units that the brief leaves implicit. These are **definitional
choices about units, not thresholds**; no bar, boundary or verdict word is set by them.

| # | term | definition fixed at freeze |
|---|---|---|
| D1 | **cell** (the brief's "country-year") | one row of the frozen panel, i.e. one `(country_id, level, year)` triple. Rationing shares are computed **within level**, so `n = 1680` cells per level (30 countries × 56 years). |
| D2 | **`p_off`** | `admitted_official / demand_official`, read from the same row. The panel carries no `p_off` column; this is the ratio V3 uses (`admitted_official/demand_official < 0.99`), and it reproduces V3's four re-derived percentages to 0.1 pp (§9). The run aborts if any `demand_official ≤ 0` or any operand is non-finite. **`p_off` is never clipped, floored or capped.** |
| D3 | **`rationed_official > 0`** | strict: `rationed_official` strictly greater than zero at full float precision. No rounding, no tolerance. |
| D4 | **levels** | exactly four, in this order: `primary`, `lower_secondary`, `upper_secondary`, `tertiary`. No level is merged, split or dropped. |
| D5 | **country set** | **all 30** `country_id` values present in the panel (`SYN00_PHL_LIKE` … `SYN29`). **No exclusion, no winsorising, no outlier rule.** The anchor type `SYN00_PHL_LIKE` is **not** removed from the pooled shares; it is reported separately as well. |
| D6 | **years** | all panel years, 1970–2025 inclusive (56 per country-level). No year window, no truncation. |
| D7 | **anchor type** | `SYN00_PHL_LIKE` (`country_id == 0`). |
| D8 | **`p4`** (rung-4 absorption) | `rung4_emp / rung4_demand` from the row's own columns, as V8 defines it. Reported for the anchor type at 2000/2010/2020/2024; the V8 comparison set is the anchor's **upper-secondary rows, 2010+** (2010 is inside the window; 2000 is reported but flagged as outside V8's window). |
| D9 | **`Q`** | `congestion_q` from the panel where reported; `Q` from the gate panel where the gate panel is the source. The source is named in every table. |

---

## 5. The two bars, the verdict vocabulary, and the verdict algorithm

**Bars (verbatim from the brief): both the `< 0.95` and the `< 0.99` bars are reported.** They are computed
**independently and identically**, over the same cells, with the same `rationed_official > 0` conjunct.

| bar | name in this experiment | status |
|---|---|---|
| `p_off < 0.95` | **bar-95** (the bar the brief names first) | **operative, reported** |
| `p_off < 0.99` | **bar-99** (the bar whose calibration the Council re-derived) | **operative, reported** |

**Verdict vocabulary (exactly three words, no others):**

| verdict | rule (verbatim from the brief) |
|---|---|
| **`GATE BINDS`** | share **≥ 50%** |
| **`UNRATIONED`** | share **≤ 10%** |
| **`INTERMEDIATE`** | strictly between 10% and 50% (the brief's third state, *"intermediate"*) |

**Algorithm (fixed):** for each level `L` and each bar `b ∈ {0.95, 0.99}`:
`share(L,b) = |{cells in L : p_off < b and rationed_official > 0}| / |{cells in L}|`,
then map `share` to the three words above. **Both bars are always reported for every level** — never one bar alone.

**Bar-agreement rule (fixed).** A level is **`CLASS-STABLE`** iff its bar-95 and bar-99 verdicts are the same word. A
level whose two verdicts differ is reported as **`BAR-DEPENDENT`** with both words and both shares shown; no dodge, no
averaging, no selecting the friendlier bar after the fact. Class-stability is verified and reported, not assumed.

**Precedence (fixed).** No share is recomputed on a subset in order to move a level across a boundary. The pooled
all-30-country, all-56-year, both-bar figures are the verdict-bearing numbers.

---

## 6. The falsifier (verbatim) and how it is operationalised

**Verbatim from the brief:** *"if any upper/tertiary level-year has `p_off < 0.50` in **>20%** of its years, the
architecture conclusion is reversed and RUNG-PROB (EXP-9) is not dispatched."*

**Primary operationalisation (verdict-bearing), fixed at freeze.** For each of the two levels `upper_secondary` and
`tertiary` separately, compute
`deep(L) = |{cells in L : p_off < 0.50}| / |{cells in L}|`
(note: **no `rationed_official > 0` conjunct** on the falsifier — the brief's falsifier clause states only `p_off < 0.50`).
The falsifier **TRIPS** iff `deep(upper_secondary) > 0.20` **or** `deep(tertiary) > 0.20`. Otherwise it
**DOES NOT TRIP**. The comparison is strict: a share of exactly 20.0% does **not** trip it.

**Secondary reading (declared, NON-verdict-bearing).** Because *"any upper/tertiary level-year"* can be read at the level
or at the individual series, the run also reports, for transparency only, the per-country per-level share
`deep(country, L)` and how many of the 30 country series individually exceed 20%. This second reading **cannot** change
the falsifier outcome, the architecture state, or the EXP-9 dispatch decision; it is reported so that the Council can see
whether the primary reading is a straddle.

**Consequence if it TRIPS (fixed, from the brief; not negotiable after results):** the architecture conclusion is
**reversed**, and **RUNG-PROB (EXP-9) is not dispatched**. The reversal is recorded explicitly and prominently in
`FINDINGS.md` and in `results/GATE_LOCUS_FALSIFIER.json`, in the word `REVERSED`, together with the level and the share
that tripped it.

---

## 7. Predeclared outcome branches and the EXP-9 dispatch rule

The brief's item 2 gives a positive and a negative branch. Because the three-word vocabulary admits a middle state, the
mapping is fixed **now**, before any share is computed:

| branch | condition (fixed) | consequence (from the brief, item 2) |
|---|---|---|
| **`POSITIVE`** | `upper_secondary` and `tertiary` are both `UNRATIONED` at both bars | the "ceiling as upper gate" line is **closed**; any future demand/shadow layer must be re-declared at the **binding** gate or the upper gate must first be given a capacity constraint; A3-D and `c4a` are **explained, not rescued** |
| **`NEGATIVE`** | `upper_secondary` is `GATE BINDS` at both bars | the `c4a` failure is **parameter-side** and a re-declaration at **g2** becomes admissible |
| **`MIXED`** | neither of the above (e.g. `INTERMEDIATE`, or `BAR-DEPENDENT`, or upper/tertiary disagree) | **neither** consequence is licensed. Report the middle state; the "closed" reading and the "parameter-side" reading are both withheld, and the next action is a Council decision, not a Worker inference |

**EXP-9 dispatch rule (fixed).** RUNG-PROB is **NOT dispatched** if the falsifier trips. If the falsifier does not trip:
EXP-9 **may be dispatched** and, on a `POSITIVE` branch, is the informative next test — **but** dispatch is recorded as
the Lead's action, not this Worker's; this experiment only records the gate state and the falsifier result on which that
action depends. Under `MIXED` the dispatch is reported as `CONDITIONAL` with the reason stated.

---

## 8. Anchor-type reporting (`results/GATE_LOCUS_ANCHOR.csv`)

For `SYN00_PHL_LIKE` at **2000, 2010, 2020, 2024**, and for **all four levels** at each year, report:
`p_off`, `rationed_official`, `admitted_official`, `demand_official`, `congestion_q`, and `p4`.
This is 16 rows. No other year is added to that file; the full 1970–2025 anchor trajectory is a declared **secondary**
file (§9), so that the Council can see whether a 4-year reading is a straddle. The four years are exactly the brief's
four; they are not selected for their values.

---

## 9. Secondary legs (declared now; NON-verdict-bearing by construction)

These are computed by the same script, reported in separate files, and **cannot** alter the shares, the verdicts, the
falsifier outcome, the branch or the dispatch record. They exist so the Council can see the structure behind the four
numbers the brief pre-quoted.

| leg | content | why declared |
|---|---|---|
| **S1** | Gate panel (`shadow_gates_v1_3.csv`) per gate `g0…g4` × country type: mean `pi0`, share `pi0 < 0.95`, share `pi0 < 0.50`, share `Q > 1` | The brief's item 4 names this file as data; V3's *cause* claim ("spare capacity") lives here. Reported because the gate panel and the flow panel are two different objects and their disagreement is a fact the Council should see. |
| **S2** | Anchor type, all 56 years × 4 levels: `p_off`, `rationed_official`, `congestion_q` | A 4-year anchor reading is only as good as its trajectory. |
| **S3** | Upper/tertiary rationing by country and by year-regime (counts and shares) | Identifies *which* systems carry the 110 upper cells at bar-99 — a share with no owner is not a finding. |

**Exploratory work already done before this freeze (disclosed).** To fix D2 and to confirm that the panel really does
carry the cells the brief names, this Worker read column values and confirmed that the panel's `p_off` at bar-99
reproduces the Council's four re-derived figures (primary **87.4%**, lower **93.3%**, upper **6.5%**, tertiary **0%**) to
0.1 pp. **No threshold was open at that moment** — all five thresholds (0.95, 0.99, ≥50%, ≤10%, >20% at <0.50) and the
falsifier are Council text — so nothing could be, and nothing was, adjusted to the data. That check is required by
D113a and is reported as a **calibration reproduction**, not as a result.

---

## 10. Deliverables (exact)

| file | content |
|---|---|
| `PRE_DECLARATIONS.md` | this file; hashed before the first run |
| `PRE_DECLARATIONS.sha256` | sidecar, `sha256  PRE_DECLARATIONS.md` |
| `code/build_predeclarations.py` | writes this file with the block spliced verbatim from the brief |
| `code/verify_predecl_verbatim.py` | asserts the frozen quote still equals the brief's lines 370–393 |
| `code/run_gate_locus.py` | the analysis; deterministic, RNG-free, timestamp-free |
| `results/GATE_LOCUS_RESULTS.csv` | per level: `n`, share and count at bar-95, share and count at bar-99, both verdicts, class-stability, verdict on components (`rationed_official>0` alone, `p_off<bar` alone) |
| `results/GATE_LOCUS_ANCHOR.csv` | the 16 anchor rows of §8, with `p4` |
| `results/GATE_LOCUS_FALSIFIER.json` | the `<0.50` / `>20%` check per level, the secondary per-country reading, the outcome word, and the consequence |
| `results/GATE_LOCUS_SECONDARY_S1.csv` | gate-panel leg S1 |
| `results/GATE_LOCUS_SECONDARY_S2.csv` | anchor trajectory, leg S2 |
| `results/GATE_LOCUS_SECONDARY_S3.csv` | upper/tertiary rationing by country and regime, leg S3 |
| `results/console.txt` | full stdout of the run |
| `results/determinism_run2/` | a second, independent run of the same script; every artifact must be **byte-identical** |
| `FINDINGS.md` | plain-English report |
| `RUN_MANIFEST.json` | predecl, code, input and result hashes |
| `SHA256SUMS.txt` | `shasum -c`-checkable sums of every file in this directory except itself |

---

## 11. No-threshold-change rule

**No threshold, bar, level, country, year, cell rule, verdict word, branch condition or falsifier rule in this document
may be changed after any result is seen.** If any such change is needed, this predeclaration is **void**, its results are
**withdrawn**, a new predeclaration is frozen and hashed, and the run is repeated under it. The correct record of a
post-freeze change is a **new experiment**, never an edit to this file. Any result produced by a script whose declared
constants do not match §5–§7 is reported as **`FAIL-PREDECL`** and is not a result.

**Determinism requirement.** The script uses **no RNG**, no clock, no environment-dependent ordering, and no floating-point
summation over an unordered container (all aggregations are over sorted, explicit lists; all output row orders are
explicitly sorted). Two independent runs into `results/` and `results/determinism_run2/` must be **byte-identical** for
every artifact, compared with `cmp`. A failure of byte-identity is reported as a delivery defect, not silenced.

---

## 12. Closed-claim note

- **Read-only on frozen panels.** No file under `generator_v1_2/`, `generator_v1_3/`, `generator_v1_4_demand/`,
  `repro_path_2026-11-20/` or anywhere else outside this directory is written, moved or modified. No file in the
  programme root is touched.
- **No re-fit, no new layer, no new parameter, no ablation.** Nothing is estimated. Every number is a ratio or a count
  over cells that already exist on disk.
- **No re-run of A3-S**, and no re-scoring of A3-S's `c4a`. No re-run of a WT/DT cell, no reopening of C1–C4, no
  re-scoring of A3-D's `FALSIFIED` verdict. This experiment **explains** those two failures; it does not rescue,
  overturn, narrow or re-open either.
- **No direction claim and no causal claim.** "The gate binds at primary/lower" is a statement about where an
  accounting constraint is *active* in a simulator, not about why any country's enrolment has any value. The word
  "cause" is not used of any observed outcome. D63 remains `UNABLE as to cause`.
- **No web, no server.** The running server is not contacted or touched. No network access.
- **Every table and every sentence about the generator carries `SYNTHETIC`.** No number here is an estimate of any real
  school system's capacity; `SYN00_PHL_LIKE` is a synthetic type named for an anchor, not the Philippines.

---

## 13. What this experiment does not decide

It does not test whether the transition ratio is a system object (EXP-6), does not re-audit the level path (EXP-7), does
not test whether the ceiling is demand-derivable (EXP-9), and does not design the HKG stock object (EXP-10). It returns
**one** measurement — where the generator's gates bind, at two bars, with a falsifier — and one dispatch-relevant fact.
