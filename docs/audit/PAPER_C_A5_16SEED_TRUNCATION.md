# Paper C — A5: confirmatory 16-seed truncation (recorded BEFORE aggregation)

**Timestamp (UTC): 2026-11-25T23:34:22Z** — recorded and committed **before** any 16-seed aggregation or outcome analysis.

## Decision
Confirmatory stage runs **6 frozen passers × 16 matched seeds \{100,…,115\} × N=1500/T=46** (96 runs), not 32 seeds.
Seeds 116–131 are **not run** for A5; if any run existed, they are excluded from A5 analysis.

## Reason (measured, no outcome peek)
Measured per-seed wall at N=1500 with the treated G6→G9 contest gate ≈ **13–15 min (≈800–900 CPU-s/run)**, giving
192 runs ≈42–48 CPU-h — ~2× the pre-declared ≤22 CPU-h envelope. A5 pre-declares truncation to 16 seeds to stay within
a new **≤24 CPU-h** envelope (96 runs ≈21–24 CPU-h). Only per-seed timings/row counts were used; **no effect/mean was
inspected** before this record.

## Unchanged design
- passers: `b64a69f0…99e7` (signed `bbc0b92`); P12=pay_gap / A4 `8c967eab…`
- engine `846c9e0` / core `e111397b…` / spec `e5ddef6b…`; runner `ddeffe42…` @ `1b3a510`
- N=1500/T=46; Holm **m=2 α=.05, T2/T3 only**; minima unchanged (T2 ≥.10, T3 ≥.05)
- T1/T4 remain screening failures, not confirmatory; no S-generalisation beyond .85; T2 proxy caveat unchanged

## Consequence
**Precision halves (SE ×√2)**; report achieved CI/MDE and label **A5 interim precision** — no claim of full 32-seed
precision. No optional stopping: exactly seeds 100–115 per cell.
