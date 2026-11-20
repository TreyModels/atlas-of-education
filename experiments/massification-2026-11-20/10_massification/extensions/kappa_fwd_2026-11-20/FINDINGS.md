# FINDINGS — EXP-11 KAPPA-FWD

**Question.** Is the per-system lower→upper one-stage transition ratio κ — the coefficient V16-REPAIR is about to
carry as a **declared input** — constant enough to be applied **forward** in a system, or only describable **within**
the window it was computed on?

**Answer: `WINDOW-ONLY`.** The per-system transition ratio is **not forward-usable** in the sense the Council's block
defines. The ratio is a legitimate **within-window description**; it may **not** enter a downstream predeclaration as a
forward constraint, in any of the four systems on disk. Two of the three binding systems fail the stationarity leg, and
the temporal hold-out breaks in **4 of 7** cells against a **strict** pre-2021 bound.

**Labels: `OBSERVED`** for the completion series (one frozen vintage, no interpolation); **`DERIVED`** for every ratio,
slope, median, bound, error and verdict. **No causal claim. No direction claim.** κ is not asserted to cause, produce
or explain anything. **D63 stays `UNABLE as to cause`.** EXP-6 is **not** re-scored.

---

## 1. The result, per system

| system | n pairs | slope of ratio on `upper_year` | half-1 median | half-2 median | half shift | leg (a) | hold-out cells within strict bound | leg (b) per system |
|---|---|---|---|---|---|---|---|---|
| **PHL** | 8 | **−0.000704/yr** | 0.959557 | 0.938209 | **2.1348 pp** | **`κ-TRENDING`** | 2 / 2 | −5.70, −2.60 pp (inside) |
| **KOR** | 19 | **+0.002875/yr** | 0.986141 | 0.992495 | 0.6354 pp | **`κ-STABLE`** | **0 / 3** | +0.68, +0.65, +0.59 pp (**all violate**) |
| **KHM** | 11 | **+0.017318/yr** | 0.533230 | 0.607591 | **7.4361 pp** | **`κ-TRENDING`** | 1 / 2 | −0.64 (inside), **+0.58 (violates)** |
| CHN *(reported, not a forward constraint — D133)* | 5 | +0.041728/yr | 0.680716 | 0.937288 | 25.6573 pp | `κ-TRENDING` | **N/A — 0 post-2020 cells** | — |

**Bars (frozen in `PRE_DECLARATIONS.md` §4–§5 before the run):** `κ-STABLE` iff `|slope| ≤ 0.005/yr` **and**
`|second-half median − first-half median| ≤ 2.0 pp`; both conjunctive. Hold-out: `upper_t ≤ κ_pre · lower_used`,
violation iff the excess is `> 1e-9 pp`; `BOUND-HOLDS` iff **≥ 6 of 7**, `BOUND-BREAKS` iff **≥ 2 violations**.

**Aggregate.** Over the **7**-cell denominator (PHL 2 + KOR 3 + KHM 2; CHN contributes 0 by D133): **within bound 3/7,
violations 4 → `BOUND-BREAKS`**. Leg (a): **not** all of PHL/KOR/KHM are `κ-STABLE` → **FAIL**.
**Verdict `WINDOW-ONLY`** (rule: `FORWARD-USABLE` iff all three stable **and** `BOUND-HOLDS`; otherwise `WINDOW-ONLY`).

**Falsifier.** **Tripped** — on the **violations arm only** (`V = 4 ≥ 2`). The **PHL-slope arm did not fire**: PHL's
slope is *negative* (−0.000704), so the brief's signed `slope > +0.005` test passes while PHL is nonetheless
`κ-TRENDING` on the half-sample bar. Both readings are reported side by side in `results/KAPPA_FWD_RESULTS.csv`; the
verdict is unchanged either way because the violation arm fires independently.

### 1.1 Provenance check (no re-fit)

All eight declared medians were **recomputed from the observed series and match the declared register at 4 dp**:
κ_full PHL 0.9491 / KOR 0.9898 / KHM 0.5950 / CHN 0.7222 (D133) and κ_pre 0.9596 / 0.9887 / 0.5950 / 0.7222 (§6.1
item 4). The 43 pairs and the 16 dropped upper years reproduce exactly, and all 43 ratios match
`PIPE_LOO_PAIRS.csv` (`43/43`) — a reproducibility check on the **input pairs**, not a re-scoring of EXP-6.

---

## 2. What actually happened, in plain English

**PHL — the trend is flat, the level is not.** PHL's ratio has no linear trend (−0.0007/yr, r² = 0.01) but its **level**
differs between halves by **2.13 pp**: 0.9596 in 2003–2010 versus 0.9382 in 2013–2024. The series is not monotone — it
sits in a 0.93–0.97 band through 2013, spikes to **1.0724 in 2017**, then falls to **0.8892 (2023)** and **0.9274
(2024)**, the two lowest ratios in the system's eight pairs. This is exactly the case the brief's **two-bar** leg (a)
exists to catch: an OLS slope alone would have called PHL stable. It is the **level** that moved, and 2.13 pp is
0.13 pp over the 2.0 pp bar — a **boundary** call that `FINDINGS` must not inflate into a large drift (see §4).

**KOR — stationary, and still not forward-usable.** KOR is the only system that clears both stationarity bars: slope
+0.0029/yr, half shift 0.64 pp. Yet **all three** post-2020 cells exceed the pre-2021 bound, by +0.68, +0.65 and
+0.59 pp. KOR sits at saturation: its lower series is **99.90–100.00** in every pre-2021 year and its upper series
**97.6–99.5**, so κ ≈ 0.989 is **near-arithmetic by construction** (D132's recorded condition). The breaches are small
in pp but they are **all in the same direction**: the ratio drifted *above* its pre-2021 median while the upper series
pushed toward 100. A bound that holds only when a system has nowhere left to go is not evidence of stationarity.

**KHM — trending up, and one pair does real work.** KHM fails both bars: slope +0.0173/yr and half shift **7.44 pp**
(0.5332 → 0.6076). The ratio runs from 0.4883 (2008) to 0.6722 (2017) to 0.6076 (2023), against a lower series that
more than doubled over the same window. One of its two hold-out cells (**2023**, +0.58 pp) breaches the pre-2021 bound,
and its **2021** cell sits 0.64 pp inside it — i.e. the boundary is crossed in a single year.

**CHN — reported, excluded.** Slope +0.0417/yr, half shift **25.66 pp** (0.6807 → 0.9373), r² = 0.92: CHN's ratio runs
0.6448 → 0.9662 while its upper series climbs from 43.97 to 87.52. This reproduces D133's disposition exactly. CHN has
**0** post-2020 cells and is **excluded** from the forward conjunction, from the 7-cell denominator and from the
falsifier. It is shown so the reader can see the mechanism the register records, not because it can move the verdict.

**HKG / JPN** are **`NON-ENTRANT`** — zero completion pairs in the frozen file (V14/D135). Not imputed, not proxied.

---

## 3. Is the verdict an artefact of how I read the brief? No.

Two phrases in the block admit more than one reading. Both alternatives were **declared in the predeclaration**, both
are **computed and reported** (`results/KAPPA_FWD_SECONDARY.csv`), and **neither changes the verdict**:

| half-sample reading (leg a) | PHL | KOR | KHM | all three stable? |
|---|---|---|---|---|
| **primary** — median ratio per half | `κ-TRENDING` (2.13) | `κ-STABLE` (0.64) | `κ-TRENDING` (7.44) | **no** |
| **S-A1** — median of per-pair LOO κ̂ (degenerate) | `κ-STABLE` (0.03) | `κ-STABLE` (0.07) | `κ-TRENDING` (**slope** 0.0173) | **no** |
| **S-A2** — median \|LOO error\| per half | `κ-STABLE` (1.94) | `κ-STABLE` (0.11) | `κ-TRENDING` (2.09) | **no** |

| bound reading (leg b) | within / 7 | label | could it yield `FORWARD-USABLE`? |
|---|---|---|---|
| **primary** — strict `upper ≤ κ_pre · lower` | **3 / 7** | `BOUND-BREAKS` | no |
| **S-B1** — ±5.0 pp slack band (EXP-6's convention) | 7 / 7 | `BOUND-HOLDS` | **still no** — leg (a) already fails |

**Under every declared reading, at least one of PHL/KHM/KOR fails leg (a), so `WINDOW-ONLY` is invariant.** The slack
band is reported **only** because it shows the breaches are small (0.58–0.68 pp); it is **`DESCRIPTIVE-NOT-VERDICT`**
and may not be promoted after the fact. A 0.6 pp breach of a one-sided bound and a 0.6 pp *accuracy* error are
different objects and are labelled as such.

---

## 4. Honest limits

1. **n is small.** 8/19/11/5 pairs per system; half-sample medians rest on 4/9/5/2 pairs per side (PHL 4, CHN 2). A
   half-sample median of four numbers is a coarse statistic: PHL's 2.1348 pp is a difference between two 4-pair
   medians, and KHM's 7.4361 pp is a difference between two 5-pair medians. These are **not** precise estimates of a
   drift rate.
2. **KHM's instability is carried substantially by one pair — reported, not repaired.** KHM's 2000 pair (ratio
   **0.1389**, lag −1 y onto lower-1996, immediately after the 1990s collapse) sits in the first half and drags the
   first-half median down, and it is the far end of the slope. **Post-hoc, non-verdict-bearing** (computed after the
   run, not in the frozen predeclaration, and not a result): excluding that single pair gives slope **+0.0037/yr** and
   half shift **1.26 pp**, which would have made KHM `κ-STABLE`. **The frozen label stands.** Removing a pair after
   seeing its residual is a re-fit and is not licensed here; the disclosure exists so no reader over-reads KHM's
   `κ-TRENDING` as a smooth secular rise.
3. **The verdict does not depend on that pair.** With KHM treated as stable, PHL still fails leg (a), and the hold-out
   still breaks at 4/7 (KOR 3/3 + KHM 2023, none of which involve the 2000 pair).
4. **PHL is a boundary call, and a downward one.** 2.1348 vs 2.0 pp. Under the S-A2 accuracy reading it is 1.94 pp.
   What is *not* in doubt is the **direction of the level move** (down) and the size of the two late-pair ratios
   (0.889/0.927, the two lowest in PHL's eight).
5. **Leg (b) is one-sided by construction.** `upper_t ≤ κ_pre · lower` can only catch an **upward** breach. PHL's
   *downward* drift is invisible to it — both its cells sit **inside** the bound by 5.70 and 2.60 pp. So "within bound"
   is not "κ stable", and the two legs are not substitutes: leg (a) is the only leg with power against downward drift.
6. **KOR's breaches are at saturation.** A 0.6 pp breach at κ ≈ 0.99 with a lower series pinned at 100.00 is a
   different object from a 0.6 pp breach at κ ≈ 0.60. There is **no second saturation-regime system on disk** to test
   generalisation (D135's HELD ask — additional upper-secondary completion series — is the only route, and it was **not**
   requested here).
7. **Short horizon.** "Out-of-time" means **1–4 years** past a 2020 cut, on **2–3 cells** per system. This tests short-
   horizon drift, not a decade-ahead projection. No extrapolation was computed anywhere.
8. **Pairing is not cohort-exact.** 18 of 43 pairs use a ±1 y offset instead of the exact `t−3` (PHL 5, KHM 7, CHN 5,
   KOR 1), and 3 of the 7 hold-out cells do (PHL 2023 +1, KHM 2021 +1, KHM 2023 −1). The literal `lower_{t−3}` bound is
   **unobservable** in 4 of the 7 cells (no observed lower at `t−3`); it was **not imputed**, and the pairing-rule lower
   was used for every cell (declared §5.3). The ratio also mixes a completion rate at `t` with one at `t−3` — different
   cohorts by construction, an inherent property of the pipeline object, not a defect introduced here.
9. **Four systems, one vintage.** PHL/KOR/KHM/CHN only; HKG/JPN non-entrant. Nothing here generalises to other systems,
   and no claim of representativeness is made.
10. **The verifier is the worker.** One deterministic script, predeclaration hash-gated, two byte-identical runs — but a
    single worker wrote the predeclaration, the code and the report. The `S-A1`/`S-A2`/`S-B1` disclosures exist to make
    the reading choices inspectable by someone else.
11. **`WINDOW-ONLY` bounds the use of κ; it does not falsify the pipeline reclassification** (brief §6.1 item 6,
    carried verbatim). EXP-6's `PREDICTIVE (3/4)` stands untouched. D63 stays `UNABLE as to cause`.

---

## 5. What this licenses for the V16-REPAIR predeclaration

This is the actionable output, and it is the brief's own **negative branch** (item 2 of the frozen block). To be carried
into V16 **before** it is frozen:

1. **κ may not be declared a forward constraint.** No system qualifies. `KOR` clears stationarity but breaks the
   forward bound in 3/3 cells; `PHL` and `KHM` fail stationarity; `CHN` is excluded by D133.
2. **If κ is carried at all, it must be a declared within-window trajectory** — a per-system, per-year path over the
   **observed** years (PHL 2003–2024, KOR 2005–2023, KHM 2000–2023) — **never extrapolated past the last observed
   pair**, with its provenance labelled `DERIVED (observed median ratio)`, never `fitted`.
3. **Otherwise κ is dropped as a constraint**, and the model's upper side is stated against the observed lower series
   with the window label attached.
4. **Every 2025+ statement in V16 inherits the limit** and must be labelled a **scenario / trajectory** statement, not a
   constraint. The model must not carry a single κ, a global κ (D133: a single κ overstates KHM by 0.354), or an
   extrapolated κ path.
5. **If V16 still wants a bound**, it must predeclare that the bound is a **within-window description** whose
   out-of-time breach rate is **4/7** with breach sizes ≤ **0.69 pp**, and it must accept `WINDOW-ONLY` status for that
   link. It may not be described as a forward constraint, and D134's object-unit obligation (completion units with
   survival explicit: `adm_upper ≤ κ·comp_lower(t−3)/surv_upper`, or the declared endpoint form) still applies to any
   κ-shaped inequality that survives.
6. **The ceiling question does not become "what sets κ?"** — that question belongs to the positive branch. What remains
   askable here is descriptive: *what moved the ratio within the window* (PHL's 2023–24 fall, KHM's rise, KOR's drift at
   saturation). This experiment does **not** answer it, and nothing in it licenses a causal reading of any move.

---

## 6. One predeclaration-authoring note for the Council (non-verdict-bearing)

The block's falsifier names **`a PHL slope > 0.005/yr`**. PHL's slope is **negative** (−0.000704), so the falsifier's
PHL arm **cannot fire** — yet PHL is `κ-TRENDING` on the half-sample bar and its ratio fell to its two lowest observed
values in 2023–24. **The falsifier's PHL arm is a strict sub-case of the leg (a) label and does not cover a
level-shift-only drift.** The verdict is unaffected (the violations arm fired independently, and leg (a) is what the
conjunction binds on), but the pattern is the one D137 records: a falsifier written against one statistic does not
guard the other statistic in the same leg. Suggested authoring rule for the next block: **name the falsifier against
the same conjunction the verdict uses**, not against one of its arms.

---

## 7. Reproduce

```
cd 10_massification/extensions/kappa_fwd_2026-11-20
"/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" code/run_kappa_fwd.py
"/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" code/run_kappa_fwd.py --outdir results/determinism_run2
```

The script verifies the predeclaration sha256 (`bda79ac4…`) and four input sha256 values **before** computing anything,
refuses to run on mismatch, and re-extracts `SYNTHESIS_023.md` lines 403–434 to byte-compare the quoted block. The two
runs are **byte-identical**: `KAPPA_FWD_RESULTS.csv`, `KAPPA_FWD_DETAIL.csv`, `KAPPA_FWD_SECONDARY.csv` and
`console.txt` (see `RUN_MANIFEST.json` → `determinism`).

**Files:** `PRE_DECLARATIONS.md` (frozen, hashed) · `results/KAPPA_FWD_RESULTS.csv` (per system + overall) ·
`results/KAPPA_FWD_DETAIL.csv` (all 43 pairs, all 7 hold-out cells) · `results/KAPPA_FWD_SECONDARY.csv` (declared
sensitivities, cross-check, non-entrants) · `results/console.txt` · `results/determinism_run2/` · `RUN_MANIFEST.json` ·
`SHA256SUMS.txt`.
