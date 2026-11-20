# FINDINGS — EXP-8 GATE-LOCUS

**`LABEL: SYNTHETIC` for every generator number in this document.** Nothing here is an estimate of any real school
system, and `SYN00_PHL_LIKE` is a synthetic type named for an anchor — it is not the Philippines.
Council brief 022, `SYNTHESIS_022.md` §6 EXP-8 (D122 #3, rank **#3**). Worker **GL**, 2026-11-20.
Predeclaration `PRE_DECLARATIONS.md` sha256 **`a8566fbfbca5cc5231ef78c35adffbf62264f82bbefe830683616105434c547d`**,
hashed before the first run; **no threshold, bar, cell rule, verdict word, branch condition or falsifier rule was
changed after results.** Every figure below is reproducible by `code/run_gate_locus.py` from the two frozen CSVs.

**This is a descriptive audit. It makes no causal claim and no direction claim.** D63 remains `UNABLE as to cause`.
It is read-only on the frozen panels: no re-fit, no new layer, no re-run of A3-S, and it does not reopen A3-D's
`FALSIFIED` verdict or A3-S's `c4a` FAIL — it *explains* them.

---

## 1. The answer in two sentences

**No — the generator does not have a school gate where the demand and shadow architecture was pointed.** Its only
binding school gates are at the floor (primary **79.11%** and lower-secondary **91.31%** of level-years at the
`p_off < 0.95` bar), upper-secondary rations in **4.70%** and tertiary in **0.00%** of level-years — and the
tertiary zero is an **accounting identity** (`admitted_official` equals `demand_official` to the last digit in
1680/1680 cells), not a measurement. **The falsifier does not trip** (0/1680 upper and 0/1680 tertiary cells below
`p_off < 0.50`), so the architecture conclusion is **not** reversed, the "ceiling as upper gate" line is **closed**,
and EXP-9 RUNG-PROB remains **dispatch-eligible**.

---

## 2. The per-level table, both bars

Rationing share = share of cells (country-year-level rows) with `p_off < bar` **and** `rationed_official > 0`.
`p_off = admitted_official / demand_official`. All 30 synthetic country types × 56 years = **1680 cells per level,
6720 in total**; no country, level or year is excluded.

| level | n | `<0.95` share | verdict | `<0.99` share | verdict | stable? | headline |
|---|---:|---:|---|---:|---|---|---|
| **primary** | 1680 | **79.11%** (1329) | **`GATE BINDS`** | **87.38%** (1468) | **`GATE BINDS`** | yes | **`GATE BINDS`** |
| **lower_secondary** | 1680 | **91.31%** (1534) | **`GATE BINDS`** | **93.33%** (1568) | **`GATE BINDS`** | yes | **`GATE BINDS`** |
| **upper_secondary** | 1680 | **4.70%** (79) | **`UNRATIONED`** | **6.55%** (110) | **`UNRATIONED`** | yes | **`UNRATIONED`** |
| **tertiary** | 1680 | **0.00%** (0) | **`UNRATIONED`** | **0.00%** (0) | **`UNRATIONED`** | yes | **`UNRATIONED`** |

**No level is `BAR-DEPENDENT`, and no level is `INTERMEDIATE`.** The choice of bar cannot change any of the four
verdicts: primary and lower are `GATE BINDS` by margins of 29 and 41 pp, upper and tertiary are `UNRATIONED` by
margins of 5.3 and 10 pp at the *worse* (bar-99) reading. The predeclared bar-99 figures reproduce the Council's
re-derived calibration exactly — primary **87.4%**, lower **93.3%**, upper **6.5%**, tertiary **0%**.

**Supporting detail (from `results/GATE_LOCUS_RESULTS.csv`):**

| level | `rationed_official > 0` | `p_off` min | `p_off` median | `p_off` max | cells with `p_off` exactly 1.0000 |
|---|---:|---:|---:|---:|---:|
| primary | 1496 | 0.6680 | 0.8567 | 1.0000 | 184 |
| lower_secondary | 1574 | 0.5752 | 0.6868 | 1.0000 | 106 |
| upper_secondary | 119 | 0.7879 | 1.0000 | 1.0000 | **1561** |
| tertiary | **0** | **1.0000** | **1.0000** | **1.0000** | **1680** |

Two facts about the components, and they matter for how the verdict may be quoted:

1. **The two-conjunct definition collapses to one conjunct in this panel.** The accounting identity
   `demand_official − admitted_official = rationed_official` holds in **6720/6720** rows (0 violations, checked to
   1e-6 relative). Hence `p_off < 1 ⟺ rationed_official > 0`, and for any bar ≤ 1 the conjunction is *numerically
   identical* to `p_off < bar` alone. The CSV reports both columns and they agree cell for cell (1329=1329,
   1468=1468, 79=79, 110=110). **The verdict does not depend on the `rationed_official > 0` conjunct**, so a reader
   who disputes that conjunct still gets the same four rows.
2. **The tertiary row is an identity, not a finding.** `admitted_official == demand_official` in all 1680 tertiary
   cells and `rationed_official ≡ 0`. In v1.2 the tertiary gate does not refuse anybody *by construction*. This is
   the strongest possible `UNRATIONED` reading and the weakest possible evidence about any real system: it cannot be
   cited as "tertiary is unrationed in reality", only as "v1.2's tertiary gate has no refusal margin to measure".

**Where the residual upper-secondary rationing lives** (`results/GATE_LOCUS_SECONDARY_S3.csv`). The 110 upper cells
at bar-99 are carried almost entirely by the **contraction and flat types**: `SYN12_DECLINE` 28 (50.0% of its 56
years), `SYN11_FLAT` 22 (39.3%), `SYN14` 21 (37.5%), `SYN19` 13 (23.2%), `SYN07` 10 (17.9%), `SYN09` 5,
`SYN01_TWIN_MFG` 4, `SYN02_TWIN_OFFICE` 4, and 1 each in `SYN06`, `SYN10_BOOM`, `SYN15`. **The anchor type
contributes 0/56.** By year the rationing sits in 1975–1999 (5–9 countries per year) with a thin tail of one country
in 1997–2002 and again in 2022–2025. So the upper gate that does exist in this generator behaves like a **contraction
valve** — it closes when a system is shrinking or flat, not as a standing capacity ceiling. That is a description of
the generator's declared rules, nothing more.

---

## 3. The anchor type (`SYN00_PHL_LIKE`) — the gate has left the school system by 2024

`results/GATE_LOCUS_ANCHOR.csv` (16 rows: 4 years × 4 levels) and `results/GATE_LOCUS_SECONDARY_S2.csv` (all 56
years).

| year | level | `p_off` | `rationed_official` | `congestion_q` | `p4` |
|---|---|---:|---:|---:|---:|
| 2000 | primary | 0.845317 | 336 396 | 1.366 | 0.0678 |
| 2000 | lower_secondary | 0.598880 | 836 088 | 2.012 | 0.0678 |
| 2000 | upper_secondary | **1.000000** | **0** | 1.936 | 0.0678 |
| 2000 | tertiary | **1.000000** | **0** | 2.636 | 0.0678 |
| 2010 | primary | 0.915214 | 202 704 | 1.262 | 0.1095 |
| 2010 | lower_secondary | 0.660950 | 776 946 | 1.823 | 0.1095 |
| 2010 | upper_secondary | **1.000000** | **0** | 1.520 | 0.1095 |
| 2010 | tertiary | **1.000000** | **0** | 1.830 | 0.1095 |
| 2020 | primary | **1.000000** | **0** | 1.135 | 0.1661 |
| 2020 | lower_secondary | 0.898259 | 233 748 | 1.341 | 0.1661 |
| 2020 | upper_secondary | **1.000000** | **0** | 1.182 | 0.1661 |
| 2020 | tertiary | **1.000000** | **0** | 1.397 | 0.1661 |
| 2024 | primary | **1.000000** | **0** | 1.071 | 0.1854 |
| 2024 | lower_secondary | **1.000000** | **0** | 1.090 | 0.1854 |
| 2024 | upper_secondary | **1.000000** | **0** | 1.062 | 0.1854 |
| 2024 | tertiary | **1.000000** | **0** | 1.245 | 0.1854 |

**The anchor-type gate state at the four brief-named years is: upper `p_off = 1.0000` and `rationed_official = 0` in
2000, 2010, 2020 and 2024 — and in every one of the 56 years 1970–2025** (min `p_off` = 1.000000, 56/56 exact
equalities). Tertiary is the same, 56/56. The full trajectory adds the fact a four-year reading would hide: the
anchor's **primary** gate rations in 49 years but not after 2018, and its **lower-secondary** gate rations in 53
years but not after 2022. **By 2024 the anchor type has no binding school gate at any level.** The only constraint
still binding in it is at the job rung, where absorption is **0.1854**.

**Rung-4 absorption `p4 = rung4_emp / rung4_demand`** (upper-secondary rows, 2010+; V8's comparison set):
panel median **0.5066** (n=480); `SYN00_PHL_LIKE` **0.1510** (0.1095–0.1854); `SYN28` **0.1766**; `SYN18`
**1.0000**. These reproduce V8's figures exactly. At the anchor: **0.0678 (2000, outside V8's 2010+ window), 0.1095
(2010), 0.1661 (2020), 0.1854 (2024)** — a slow rise, still an order of magnitude below 1.

Reading the two halves together, descriptively: at the anchor's upper level the seating stock covers only 52–94% of
the *cohort* (`congestion_q` 1.06–1.94; `congestion_q = 1/seat_coverage` and `seat_coverage = seats/cohort` in this
panel), yet **100% of official-age demand is admitted**. The shortfall against the cohort is absorbed **outside** the
admission ratio. The gate refuses nobody; the queue is not at the school door.

---

## 4. The falsifier — **`NOT TRIPPED`**

Verbatim rule: *"if any upper/tertiary level-year has `p_off < 0.50` in >20% of its years, the architecture
conclusion is reversed and RUNG-PROB (EXP-9) is not dispatched."* Operationalised at freeze as the share of each
level's cells with `p_off < 0.50`, no rationing conjunct, strict `> 20%`.

| level | n | cells `p_off < 0.50` | share | threshold | trips? |
|---|---:|---:|---:|---:|---|
| upper_secondary | 1680 | **0** | **0.00%** | > 20% | **no** |
| tertiary | 1680 | **0** | **0.00%** | > 20% | **no** |

**Outcome: `NOT TRIPPED`. Architecture conclusion: `NOT REVERSED`.** The nearest approach is the upper level's
minimum `p_off` of **0.7879** — 28.8 pp above the falsifier bar. The declared secondary reading (per individual
country series: **0 of 60** series exceed 20%) confirms the primary reading does not straddle; there is no individual
upper or tertiary series anywhere in the panel with a deep-rationing tail.

**The falsifier is measure-dependent, and that is disclosed rather than exploited.** On the *gate* panel's own
advance probability `pi0` (a different object — see §5) the picture is not the same: for the `SYN_PHL_LIKE` type the
tertiary gate `g3` has `pi0 < 0.50` in **8/56 years (14.3%)** — still under the bar — while for `SYN_KHM_LIKE` it is
**53/56 (94.6%)**, which would trip it. The predeclared primary measure is the flow panel's `p_off`, which is also the
measure the Council's calibration is stated on; substituting `pi0` would be a post-freeze threshold change and is not
done. Recorded so the Council can see that "the falsifier is clean" is a statement about **the flow panel's admission
accounting**, not a universal claim about every probability in the module.

---

## 5. Disclosure: the two on-disk constructs are not the same object

The brief names both files. They disagree, and the disagreement is informative (`results/GATE_LOCUS_SECONDARY_S1.csv`,
`S1B.csv`; all numbers `SYNTHETIC`, non-verdict-bearing).

| gate | `SYN_PHL_LIKE` mean `pi0` | years `pi0<0.95` | `SYN_HKG_LIKE` mean `pi0` | years `pi0<0.95` |
|---|---:|---:|---:|---:|
| `g0_PRE` | 0.854 | 46/56 (82.1%) | 0.805 | 56/56 (100%) |
| `g1_LS` | 0.979 | 13/56 (23.2%) | 0.982 | 10/56 (17.9%) |
| `g2_US` | **0.9975** | 1/56 (1.8%) | 0.945 | **24/56 (42.9%)** |
| `g3_TER` | **0.612** | **56/56 (100%)** | 0.998 | 1/56 (1.8%) |
| `g4_JOB` | 0.958 | 5/56 (8.9%) | 0.993 | 3/56 (5.4%) |

- **They agree where it matters for this experiment.** At the anchor type's upper gate (`g2`) the gate panel gives
  `pi0` = **0.9990, 0.9990, 0.9990, 0.9865** in 2000/2010/2020/2024 with `Q` = 0.49/0.48/0.62/0.82 — i.e. the same
  "admits everyone, capacity not scarce" state the flow panel's `p_off = 1.0000` records. **Both constructs therefore
  put the upper gate at ≈1.0 for the anchor type.** That is the load-bearing conjunction behind A3-D's `P ≈ 0.999`.
- **They disagree below and above it.** The gate panel's `g3` rations heavily for the PHL-like type (`pi0` 0.431–0.712
  in the four anchor years, 100% of years below 0.95) while the flow panel's tertiary `p_off` is exactly 1.0 in all
  1680 cells; and the gate panel's `g1` is nearly free (mean 0.979) while the flow panel's lower-secondary gate binds
  in 91.3% of years. The two objects differ in **denominator** (the gate panel's `candidates` exceed the flow panel's
  `demand_official`), so `pi0 < 1` there does **not** mean "official-age demand was refused".
- **`Q` is two different quantities in the two files.** The flow panel's `congestion_q` is `1/seat_coverage` with
  `seat_coverage = seats/cohort` (about the *cohort*); the gate panel's `Q` is `candidates/capacity` (about the
  *candidate pool*). Every table in this delivery names its source. No arithmetic mixes them.
- **`pi0` is not a pure capacity ratio.** `SYN_HKG_LIKE` `g2` has `pi0 < 0.95` in 24/56 years while `Q < 1` in all 56
  (`Q` mean 0.532). No reading of `pi0 < 0.95` as "rationing" is made here.

**Consequence for this experiment: none.** The verdict-bearing measure is the flow panel's `p_off`, as predeclared;
the gate panel is a declared secondary leg. The divergence changes the *interpretation available to the Council*, not
the four verdicts.

---

## 6. What this explains — without reopening anything

### 6.1 A3-D (`FALSIFIED`): why the `d2` lever is dead

A3-D's `d2` doubles gate pressure at `g2` and asks for **≥ +0.5 pp** of gate-level demand in all three country types;
it returned **+0.233 pp** in `SYN_PHL_LIKE` (`FAIL`) against +2.470 and +10.329 in the other two. A3-D's own
explanation is demand-side: the replacement had already driven that type's demand share to the bound (**0.993** in
2024), so a +10% return cannot add a percentage point to a share already at its ceiling.

EXP-8 supplies the **supply-side half of the same arithmetic, measured independently**: at the anchor's upper level
`p_off = 1.000000` and `rationed_official = 0` in **56/56 years**, and the gate panel's `g2` agrees (`pi0 ≈ 0.999`).
There is **no shortfall** in the quantity a gate-pressure lever would work against: the gate admits every
official-age candidate it is offered, so a lever that relaxes the gate has nothing to relax. The `d2` cell is dead
because both of its margins are gone — the demand share is at its bound and the admission ratio is at 1.0. This is a
statement about where the lever's input sits in the accounting, **not** a causal claim and **not** a rescue: A3-D's
verdict stands `FALSIFIED` as delivered, and the ceiling in v1.2/v1.3 remains a declared-taste phenomenon.

### 6.2 A3-S (`c4a FAIL`): why the anchor was out of reach at `g2`

`c4a` asks whether `D(HKG-like, g2, t*=2020) ∈ [0.75, 0.95]`; it returned **0.340215**. v1.3's own
`INTERPRETATION CORRECTION` already named the mechanism — *"the upper-secondary gate in v1.2/v1.3 is unrationed
(`P(advance) ≈ 0.999`), so the model has no scarce high-quality gate for demand to press against"* — and flagged it as
requiring a two-tier gate (v1.5 Amendment A5). **EXP-8 measures that premise directly and confirms it in both
constructs**: flow-panel `p_off = 1.000000` (56/56 anchor years, 0 rationed), gate-panel `g2` `pi0` = 0.9990 at 2020
with `Q` = 0.6214 (spare capacity). The `c4a` miss is therefore located at the **gate it was measured at**, and it is
a **rationing-margin miss, not a demand miss** — which is what v1.3 said, now with a census behind it. `c4a` is
**not** re-scored, **not** rescued, and **not** converted into a PASS; the label v1.3 gave it stands, and no
country-specific behaviour is introduced.

**A caution this measurement licenses, offered to the Council rather than acted on.** The `SYN_HKG_LIKE` type's `g2`
already has `pi0 < 0.95` in **24 of 56 years** — yet `D(g2)` stays ≈0.34 and `c4a` fails in every sensitivity cell.
So "make the upper gate ration" is **not** a sufficient fix by itself; the v1.5 two-tier design has to put scarcity at
the gate where the shadow decision is actually taken, and `pi0 < 0.95` on the existing single gate is not that. This
is a note about the module's structure, not a recommendation about any school system.

---

## 7. Should EXP-9 RUNG-PROB be dispatched?

**Yes — `DISPATCH-ELIGIBLE`, with two declared conditions, and dispatch remains the Lead's action, not this Worker's.**

- The predeclared blocking condition is **not** met: the falsifier did **not** trip, upper and tertiary are
  `UNRATIONED` at both bars, and the branch is **`POSITIVE`**. The brief's positive branch applies — the "ceiling as
  upper gate" line is **closed**, and any future demand/shadow layer must be re-declared at the **binding** gate or the
  upper gate must first be given a capacity constraint.
- **Condition 1 (arm A's input is sound).** Arm A's `P = pi0(g2) ≈ 0.999` is the one gate probability both on-disk
  constructs agree is ≈1 for the anchor type (flow `p_off` 1.0000; gate `g2` `pi0` 0.9990). A3-D's wiring error is
  therefore confirmed as an **input choice**, not a data artefact, and arm A is expected to overshoot again for the
  recorded reason (+18.41 pp, `NON-DECORATIVE`).
- **Condition 2 (arm B is arithmetic, and should be recorded as such before the run).** **No gate in either panel has
  a probability of 0.151 for the anchor type** — the anchor's 280 gate-year cells span `pi0` ∈ [0.300, 1.000], with
  none in [0.14, 0.16] and only 11 cells below 0.50 (8 at `g3`, 3 at `g4`). The 0.151 is `rung4_emp/rung4_demand`, an
  **absorption ratio**, and the nearest gate probabilities are `g3` 0.431 and `g4` 0.414 in 2024. Arm B therefore
  substitutes a ratio for a probability, and its predeclared undershoot is partly arithmetic by construction. That
  should be written into EXP-9's predeclaration, because it bounds what a `NOT DEMAND-DERIVABLE` verdict there could
  mean.
- If the Council reads the gate panel's tertiary `g3` (`pi0` 0.43–0.71, 100% of PHL-like years below 0.95) as the
  relevant gate rather than the flow panel's `p_off`, then the positive branch's *location* changes (g3, not g1) but
  the upper-gate conclusion — the gate the architecture was pointed at is not scarce — does not. That reading is a
  Council decision, not a Worker inference.

**Recommendation to the Lead in one line:** dispatch EXP-9 on arm B with the ratio/probability caveat recorded, and
record EXP-8 as what closes the "ceiling as upper gate" line — not as a rescue of A3-D or `c4a`.

---

## 8. What this does not decide

It does not test whether the lower→upper transition ratio is a system object (EXP-6), does not re-audit the level path
(EXP-7), does not test whether the ceiling is demand-derivable (EXP-9), and does not design the HKG stock object
(EXP-10). It does not say why any country's enrolment has any value. It returns one census, one falsifier result and
one dispatch-relevant fact.

---

**Note on EXP-6.** A `pipe_loo_2026-11-20/` directory appeared under `10_massification/extensions/` during this
session, **after** this experiment's predeclaration was frozen; it was not present at the freeze and nothing in it was
read or used here (see `PRE_DECLARATIONS.md` §2). EXP-8 shares no estimand with EXP-6, so this changes no number above.

---

## 9. Discipline and reproducibility

- **Read-only.** Neither frozen input is modified; its sha256 is checked at the top of every run and the script aborts
  on any mismatch (`14729c51…acf5ac` panel, `df3cab00…b351` gate panel). No file outside
  `10_massification/extensions/gate_locus_2026-11-20/` was created, moved or modified. No web; the server was not
  contacted.
- **No re-fit, no new layer, no ablation, no re-run of A3-S.** Nothing is estimated; every number is a count or a
  ratio over cells that already exist.
- **No threshold change.** All five constants (0.95, 0.99, ≥50%, ≤10%, >20% at <0.50) and the falsifier are Council
  text; the predeclaration froze them and `code/verify_predecl_verbatim.py` re-checks that the quoted block is
  byte-identical to `SYNTHESIS_022.md` lines 370–393 and that the frozen file still hashes to `a8566fbf…4c547d`.
- **Determinism.** RNG-free, clock-free, all output orders explicit, all floats format-pinned. Two independent runs
  (`results/` and `results/determinism_run2/`) compared with `cmp` on **all eight artifacts** — seven result files and
  `console.txt` — are **byte-identical**.
- **Traceability.** Every number in this document appears in a result CSV or in `console.txt`; the input, code and
  result hashes are in `RUN_MANIFEST.json` and `SHA256SUMS.txt`.
