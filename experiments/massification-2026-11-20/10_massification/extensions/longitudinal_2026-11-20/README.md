# Longitudinal battery 2026-11-20 — user-directed re-run

**DESCRIPTIVE / ASSOCIATIONAL — no causal claim, no direction claim.** Re-runs Dr. Menefee's 2015 UIS/Excel question
longitudinally, with ECI: does literacy co-move with GDP growth where years-of-schooling does not, and does economic
complexity gate that link?

- `PRE_DECLARATIONS.md` — frozen before the run (sha256 `bff1c3ec…`): S1–S8 specs, H1–H4 thresholds, derived
  `MYS_proxy` formula, verdict vocabulary.
- `stats/` — `code/run.py`, all specification CSVs, `RESULTS.csv` (H1–H4 + S1–S8), worker `FINDINGS.md`,
  `RUN_MANIFEST.json`.
- `lit/` — `EXPECTATIONS.csv` (all rows PROGRAMME-PRIOR / UNVERIFIED / BLOCKED — the repo ledger has no growth
  literature), `SYNTHETIC_TARGETS.md`, `PLAIN_ENGLISH.md`.
- `FINDINGS.md` — consolidated plain-English answer.
- `RUN_MANIFEST.json`, `SHA256SUMS.txt`.

Data: `09_relations/data/panel_wdi_long.csv` + `economic_complexity_panel_30ctys.csv`, 30 countries, 1995–2024.
No external data request; nothing sent. Phase remains CLOSED (D76); C1–C4 not reopened.
