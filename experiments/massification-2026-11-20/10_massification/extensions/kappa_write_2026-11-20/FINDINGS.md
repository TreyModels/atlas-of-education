# FINDINGS — EXP-24 **KAPPA-WRITE**

**Worker KW · Council brief 025, `SYNTHESIS_025.md` §6.4 (rank #4) · adopted by D156.**
Static register of the per-system transition ratio κ, built as a **write-up instrument**. No model run, no
re-fit, no adoption, no causal or direction claim.

**Verdict: `REGISTER-NARROWED`** (the block's own label: `USE-OUTSIDE-WINDOW`).

Predeclaration `PRE_DECLARATIONS.md` sha256 `db20d123835164f0274e7d486d87c9eadd4ef7fa7dbcb74ad6cdb437583776f1`,
**enforced by the runner at the moment the verdict was written** (D158 rule 1). The EXP-24 block in it is
injected byte-for-byte from the synthesis and re-verified as `IDENTICAL` (39 lines). Determinism: two runs,
**four of four files byte-identical**.

---

## 1. The short answer

**May the per-system κ register be used in the write-up? Yes — but only in narrowed form, and only as four
fixed sentences about a declared window.**

The register itself is sound: four systems, κ reproduced from their own pairs at 4 dp, every register line
traceable to a file and a column, no falsifier trip. What is **not** sound is the claim that "every κ use on
disk is inside its window": **233 of 299 applied uses are in-window (77.93 %)**; **68 are outside it**, and all
68 sit in seven named objects that are either closed artifacts or prose. The bar is 100 %, so the answer to the
block's positive branch (`REGISTER-CLEAN`) is **no**. The answer to "may the four sentences ship?" is **yes**.

Under the declared precedence (`REGISTER-CONSISTENT > REGISTER-NARROWED > REGISTER-UNUSABLE`) the verdict is
`REGISTER-NARROWED`: the register is usable, the out-of-window objects are named, their sentences are barred,
and **no live verdict rests on any of them**.

---

## 2. The register

| system | κ (full) | κ (pre-2021) | window, pre-2021 | window, full | slope /yr | half-shift | hold-out | admissible use |
|---|---:|---:|---|---|---:|---:|---|---|
| **PHL** | 0.949135 | 0.959557 | 2003–2017 | 2003–2024 | −0.000704 | **2.1348 pp** | 2/2 within | SENTENCE-ONLY |
| **KOR** | 0.989758 | 0.988665 | 2005–2020 | 2005–2023 | +0.002875 | 0.6354 pp | **0/3 within** | SENTENCE-ONLY |
| **KHM** | 0.594984 | 0.594984 | 2000–2017 | 2000–2023 | **+0.017318** | **7.4361 pp** | 1/2 within | SENTENCE-ONLY |
| **CHN** | 0.722222 | 0.722222 | 2012–2020 | 2012–2020 | **+0.041728** | **25.6573 pp** | N/A — 0 cells | REPORTED-ONLY |
| **HKG** | — | — | empty | empty | — | — | — | **NONE** (non-entrant) |
| **JPN** | — | — | empty | empty | — | — | — | **NONE** (non-entrant) |

`DERIVED`: κ is the median ratio of each system's own observed pairs (`KAPPA_FWD_DETAIL.csv`, 8 / 19 / 11 / 5).
Windows are derived, not chosen, and reconciled against the anchor spans. Labels `OBSERVED` / `DERIVED` only.
HKG and JPN have zero completion pairs on disk: empty window, no claim, no proxy.

### The KOR counter-example, which this register carries

> **KOR is the counter-example that bars "κ-STABLE is forward-usable": slope +0.002875/yr and half-shift
> 0.6354 pp both clear their bars, yet 0/3 hold-out cells (excess +0.6824, +0.6506, +0.5917 pp).**

KOR is the only system that clears both stationarity bars, and it is the one that breaks every forward cell.
That is the whole reason κ may not be written forward. A register that reports KOR as `κ-STABLE` without this
sentence is defective; the runner checks for the sentence and marks the verdict `UNVERIFIED` if it is missing.

---

## 3. The count, and what is outside the window

| | count |
|---|---:|
| κ uses enumerated (17 declared files) | **309** |
| applied (excludes 8 not-applied and 2 out-of-object) | **299** |
| **in-window** | **233** (77.93 % of applied) |
| out-of-window, below the window | 64 |
| out-of-window, above the window | 4 |
| projections (year-bearing, beyond the window) | 64 |
| `NOT-COMPARABLE` (κ applied to a model-generated series) | 44 |
| observed-pair descriptive uses in-window (the sentence ground) | **132** |
| register lines traceable / falsifier tripped | 6/6 TRACEABLE / **FALSE** |

Per system, in-window uses: **PHL 104, KOR 60, KHM 42, CHN 27** — so a window-only sentence is groundable for
all four. Every out-of-window use is PHL's (68), because every one of them is a PHL κ applied somewhere else.

**The seven barred objects, named (never re-scored, never repaired):**

1. `repro_path_2026-11-20/results/KAPPA_LINK.csv` — **62 uses**. κ = 0.949 (and the 0.960 sensitivity) is
   applied as a hard bound `upper_t ≤ κ · lower_{t−3}` for the **53 synthetic years 1973–2025**; the PHL window
   is **2003–2024**, so **31 of 53 years are out-of-window**. The `lower` series is **model output**, not the
   observed PHL series, so even its in-window years are `NOT-COMPARABLE` (44 uses) under D158 rule 2. The
   object's own FINDINGS disclose the act ("applied **in memory** as a projection"); this register **names** it
   and **bars** it. EXP-7's verdict is final and is **not** re-scored.
2. `synthetic…/generator_v1_5_bimodal/results/KAPPA_BIND_CELLS.csv` — κ = 0.949 applied across **1970–2025**
   for 29 synthetic objects (1,620 rows). Class **v1.5**; closed under D150/D153.
3. `…/generator_v1_5_bimodal/results/kappa_cap_audit.csv` — κ bound on the A01/A11 arms, **1970–2025** (56
   years). Class **v1.5**; closed.
4. `…/generator_v1_6_repair/results/kappa_object_audit.csv` — κ enforced at completion level, **1973–2025** (53
   years, 0/53 enforced, binds 23/53). Class **v1.6**; closed.
5. `…/generator_v1_6_repair/results/panel_A01D_kappa.csv` — the κ-conditioned panel, 6,720 rows, 1970–2025.
   Class **v1.6**; closed.
6. `08_council/DECISIONS.md` — **1 projection**: D133's sentence "κ-implied upper max for **2027** = 87.710".
   A stated future value computed from κ. Barred as written; the decision's substance (D63 `UNABLE`) is not
   affected.
7. `10_massification/STATUS.md` — **1 projection**, the same 2027 sentence in the status narrative. Barred.

**A cross-system substitution is on disk and is *not* a use.** `pipe_loo` and `STATUS` both write "a single
κ = 0.949 overstates KHM by 0.354" — that is a **warning against** substituting PHL's coefficient for KHM's, and
the register records it as a **PHL** use (the value is PHL's), not as a KHM use. The 29 `SYN*` objects in the
v1.5 files are declared PHL-like synthetic variants of one anchor, not 29 countries, so `κ = 0.949` across
them is not a cross-country substitution; that judgment is declared here rather than hidden.

**The two κ symbols.** The programme also writes κ for the model's congestion elasticity (`G(C) = C^κ`,
`κ ∈ [0.5, 1.0]`). That is a different object, with different units and a different decision history. It is
excluded by declaration (D9), counted (2 lines: `DECISIONS.md` L69, `STATUS.md` L301), and **not** merged into
the register.

---

## 4. Why `REGISTER-NARROWED` and not `REGISTER-UNUSABLE`

The declared narrowing test has five conditions; all five hold:

* every register line is `TRACEABLE` and the 4-dp reconciliation is `MATCH` (PHL 0.949135 vs recomputed
  0.9491355; KOR 0.989758; KHM 0.594984; CHN 0.722222);
* the KOR counter-example and all four fixed sentences are carried;
* every out-of-window, projection or `NOT-COMPARABLE` use is in a **closed** artifact (v1.5, v1.6, the EXP-7
  link whose label is final) or in **prose** that carries no verdict;
* **0** live verdicts rest on any of them (`live_verdict_load_bearing_uses = 0`);
* the four systems still have in-window descriptive uses (132), so the sentences are groundable.

The falsifier did **not** trip. Had any register line failed its provenance re-read, the verdict would be
`UNUSABLE` regardless of the counts.

---

## 5. Sentence constraints for the write-up (the operative output of this cell)

**Admissible — these four, verbatim, one per system, each with its window stated in the same paragraph:**

* PHL: *"within-window; slope flat but half-shift 2.1348 pp > 2.0, so not stationary in level"* — window
  2003–2024.
* KOR: *"slope flat and shift 0.6354 pp, yet 0/3 hold-out cells — κ-STABLE is never written forward-usable"* —
  window 2005–2023.
* KHM: *"trending, shift 7.4361 pp"* — window 2000–2023.
* CHN: *"reported only; non-stationary; not a forward constraint"* — window 2012–2020.

**Plus** the KOR counter-example sentence (§2) wherever κ-STABLE is mentioned at all.

**Rules that travel with those sentences:**

1. **Window-only.** Every κ sentence states its system and its window. A κ sentence without a window is
   `UNVERIFIED` and may not ship (D158 rule 3).
2. **No generalisation across systems.** κ ranges 0.5950–0.9898 on four systems; a cross-system stability
   claim is false as written and is banned (B2).
3. **No forward claim.** `κ-STABLE` may never be written as a forward, predictive or validated quantity, nor as
   a constraint (B3). KOR is the counter-example, not an exception to it.
4. **CHN is reported only** — never a forward constraint, in any sentence, in any form (D133; B8).
5. **No projection.** No `κ-implied` value for a future year, no κ trend carried past 2024/2023/2020, no κ bound
   applied to a model-generated series and cited as evidence (D6/D8; B4, B5, B6).
6. **No causal or direction claim.** κ describes a ratio; it does not explain, cause or drive the level (B9).
7. **No adoption.** The register is a citation, not a parameter. Nothing here is fitted, adopted, or re-scored.
8. **Cite the register, and only its universe.** A κ value from a file outside the 17 adjudicated files has no
   register line and is `UNVERIFIED`.

**Barred, specifically, by this run** (both are on disk today):

* *"κ = 0.949 links the delivered path"* / any citation of the κ-link as validation — the link is a
  **projection over 53 model years**, 31 of them outside the window, applied to a model-generated lower series.
* *"κ-implied upper completion for 2027 = 87.710"* — a stated future value computed from κ (`DECISIONS.md`
  D133; `STATUS.md`). Barred in both places; the D63 `UNABLE as to cause` position is unchanged.

<!-- BANNED-EXAMPLES (quoted only to bar them; stripped before any assertion scan) -->
Banned phrasings, quoted: "κ ≈ 0.95 for the Philippines"; "κ is stable across systems"; "κ-STABLE is
forward-usable"; "κ predicts upper completion"; "the κ-link validates the model path"; "κ is a parameter";
"CHN is a forward constraint"; "the register is clean".
<!-- /BANNED-EXAMPLES -->

---

## 6. Honest limits

1. **The universe is 17 files, not the 193 that contain a κ token.** A repository-wide scan finds **193** text
   files with a κ/kappa token; **17** are adjudicated. The other **176** are prior-cycle predeclarations,
   findings and logs. The register certifies the 17 and says so; it does **not** certify the corpus. This is the
   largest single limit on the claim "every κ use on disk".
2. **The projection count is a floor, not a ceiling.** Prose projections are detected by **language**
   (`κ-implied … for <year>`), not by incidental years. A future-tense sentence with no year (`κ will predict
   …`) is **not** machine-detected; it is covered only by the banned-sentence register. The 2 detected prose
   projections are exactly the two 2027 sentences; there may be others in the unadjudicated 176 files.
3. **Text extraction is a reading, not a measurement.** Rules are declared in `PRE_DECLARATIONS.md` §4.2–4.3
   (κ-adjacent literals; ISO3-adjacent literals accepted only on a register-value match; nearest-ISO3
   attribution with a value-match override; one use per file/line/system/value). Three pre-run amendments were
   made because the first passes **mis-read prose**: the naive "first year on the line" rule turned **11**
   `DECISIONS.md` citations into false projections (every Council row carries its own date) and "first ISO3 on
   the line" attributed PHL's coefficient to HKG on a line that mentions HKG in passing. **No amendment touched
   the 100 % bar, the windows, the four sentences or the verdict precedence**; the verdict is `NARROWED` under
   both the naive and the corrected reading, and only the count of barred prose rows changes.
4. **The κ-conditioned model objects are aggregated at file-span granularity** (4 rows, with `n_records`
   carried), not one row per cell. The alternative would have produced ~9,500 rows of one repeated fact. The
   aggregation is declared, and the rows carry their record counts so it can be audited.
5. **This register adds no evidence.** It re-reads 17 delivered files and reports what is in them. It does not
   estimate κ, does not re-derive pairs from the completion series, and does not test any new hypothesis.
6. **No HKG / JPN content.** Both are non-entrant with an empty window. The block's HKG leg (the two-part
   re-entry test, item 5(iii)) is **not executed here** — it belongs to the HELD ledger — and it is not
   summarised as if it had been done.
7. **The 100 % bar was not met, and this is the finding.** A programme that wrote κ into four objects and then
   ruled it window-only was always likely to fail its own register. That is what the register is for. Nothing
   in the register has been repaired to make the bar pass.

---

## 7. What this does not license

* It does **not** make κ a constraint, a parameter, a calibration target or a forecast input.
* It does **not** turn `κ-STABLE` into `forward-usable` (KOR: 0/3).
* It does **not** license a cross-system or cross-level κ sentence.
* It does **not** re-score EXP-6, EXP-7, EXP-11 or EXP-14, and does **not** re-open the HKG arm.
* It does **not** support any causal or direction claim, and makes none.
* It does **not** adopt the register as a paper object; adoption is a Council act.

---

## 8. Reproduction

```
cd 10_massification/extensions/kappa_write_2026-11-20
"/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" code/run_kappa_write.py
"/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" code/run_kappa_write.py --outdir results/determinism_run2
"/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" code/make_manifest.py
```

**Files:** `PRE_DECLARATIONS.md` (frozen, hash-enforced) · `results/KAPPA_WRITE_REGISTER.csv` (6 rows: four
systems + two non-entrants) · `results/KAPPA_WRITE_USES.csv` (309 uses, each with file + column + row key) ·
`results/KAPPA_WRITE_SUMMARY.csv` (counts and verdict) · `results/console.txt` · `results/determinism_run2/` ·
`RUN_MANIFEST.json` · `SHA256SUMS.txt`.

Labels: `OBSERVED` (the delivered ratio/pair inputs) and `DERIVED` (medians, spans, counts, verdict) only. No
model run. No re-fit. No adoption. No causal or direction claim.
