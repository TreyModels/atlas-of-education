# HKG H1 OUTCOME — construct-equivalence test FAILED → the transfer is `BLOCKED-MEASURE(SR-1)`

**Date:** 2026-11-20 (cycle 13 execution). **Authority:** Council D111 H1, D112 EXP-3; test executed as EXP-3 M1-NER
(`10_massification/extensions/m1_ner_2026-11-20/`, predecl sha256 `9eb35a92…`). **This is a terminal state record, not a
result and not a diagnostic.**

## The ruling

Council D111 granted the HKG diagnostic transfer **AUTHORISE-WITH-CONDITIONS**, with **H1: measure admissibility** —
the cohort-flow NER analogue must pass the construct-equivalence test (|stock − flow| ≤ 2.0 pp in every year where the
analogue ∈ [85, 95], and implied first-sustained 5-year crossing years differing by ≤ 1 y); else
`BLOCKED-MEASURE(SR-1)` and the authorisation is **void for that object**.

EXP-3 M1-NER (predeclared, deterministic, two runs byte-identical) returned **H1 NOT ADMISSIBLE** on the declared
verdict series (`SYN00_PHL_LIKE` primary, stock = mean of `admitted_official / cohort` over the last `dur = 6` years):

| H1 condition | result |
|---|---|
| Band: \|stock − flow\| ≤ 2.0 pp in every year with flow ∈ [85, 95] | **NOT MET** — max 2.685005 pp at 2001 (stock 82.452834, flow 85.137839); 7/15 band years > 2.0 pp |
| Crossings: first-sustained (5y) crossing years differ ≤ 1 y | **NOT MET** — ≥90: flow 2007 vs stock 2010 (**3 y**); ≥95: flow 2016 vs stock 2018 (**2 y**) |
| Expected sign (descriptive) | holds — 15/15 band expansion years flow ≥ stock; mean stock − flow = −1.751664 pp |
| Overall | **NOT ADMISSIBLE** |

Panel-wide sensitivity points the same way (max 6.739943 pp; 141/582 band series-years over 2.0 pp; 90-crossing within
1 y in only 4/30 both-defined series). The analogue is a **cohort-flow** object that leads a stock-style object by
2–3 years — exactly the direction that could flatter a 1974/1979 target, which is why H1 was predeclared.

## Consequence

- The HKG diagnostic transfer **must not be run** on the cohort-flow NER analogue. If attempted, it returns
  **`BLOCKED-MEASURE(SR-1)`** — a terminal non-verdict, never a diagnostic, never a PASS/FAIL.
- The authorisation in D111 is **void for this object**. Any future HKG attempt requires a **new predeclaration that
  specifies a stock-style NER object** (e.g. a grade-progression stock reconstruction), with its own construct test —
  that is a new Council decision, not a controller action.
- Recorded in `DECISIONS.md` as D114. The frozen HKG predeclaration (`HKG_TRANSFER_PRE_DECLARATIONS.md`, sha256
  `99be01d7…`) is **not edited**; this note is the outcome record.
- **No HKG result exists.** No portability, timing, capacity, or phase-verdict claim is made or implied.

**Reference-only (not validation, not compared to synthetic targets):** observed HKG `ner_primary` 1971–1996 (17
observations): first-sustained ≥90 = **1974**, ≥95 = **1979**; PHL `ner_primary` 1976–2017: ≥90 = **1981**, ≥95 =
none by 2025 (first-at 1976).
