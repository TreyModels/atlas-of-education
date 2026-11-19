# Bus model v2/v3 — memory, the credit-and-land economy, sectors and factions (18 Nov 2026)

Synthetic model, calibrated only to the shape of CCDI case counts plus qualitative patterns. Python 3.11+,
numpy, pandas, scipy, matplotlib. Run every script from this folder.

| File | What it is |
|---|---|
| `data/china_series.csv` | Land-sale revenue, BIS total credit, nominal GDP, CCDI cases filed, official defense budget (Japan MOD backdata) and equipment share (2019 white paper; UN report 2022), 1998–2025. `source_notes` flags which values were checked against a source in this session and which are from memory. |
| `bus_v2.py` | Economy + sectors + memory switch. One rule for all sectors: rents = r0 + beta·ln(discretionary money per official); land = land-sale revenue, finance = c_fin × new credit, PLA = official defense budget × equipment share (× off-budget multiplier). Models A (no memory), K (capacity only), C (full). |
| `bus_v3.py` | v2 plus faction dynamics F1–F7 (patron protection, ramped encircling with contagion, political removals, hiding ties, bandwagoning, fission, threat targeting, succession scenario). ODD summary in the header. |
| `calibrate_abc.py` | v2 ABC against case-series shape. (Edited for a three-model run that was stopped; its saved output `abc_draws.csv` is the earlier two-model run.) |
| `calibrate_v3.py` | v3 pattern-oriented ABC, round 1 (C 300, A 150, K 150 draws). ~6 min on 2 cores. |
| `calibrate_v3_round2.py` | Sequential round 2 for C with pattern P6. ~5 min. |
| `scenarios_v3.py` | 2026–2041 scenarios (incl. defense growth 4% and +50% off-budget procurement) on the 17 pattern-passing fits × 2 seeds. ~4 min. |
| `figures_v3.py` | Figures 5–10 in `figs/` (10 = PLA). |
| `abc_v3_all.csv`, `abc_v3_C_rounds.csv`, `abc_v3_accepted.csv`, `scenarios_v3.csv` | Raw outputs. |

Order: `python calibrate_v3.py && python calibrate_v3_round2.py && python scenarios_v3.py && python figures_v3.py`
