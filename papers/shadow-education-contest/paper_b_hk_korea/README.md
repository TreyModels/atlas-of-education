# Paper B — Why Tutoring Taxes Backfire and Expanding Elite Seats Fuels the Arms Race

**A comparative structural study of shadow education in Hong Kong and South Korea.**
Trey Menefee, Atlas of Education Research Program. **Draft (author-reported); simulation only.**
(An 18-arm / 540-run bundle run was reproduced against its supplied reference on 2026-11-25 — see
"Verification status" below; it is a different design from this draft's table and its CF4 result is negative.)

Manuscript: `Shadow_Education_Arms_Race_HK_Korea_APA.docx` (APA 7th, 4 embedded 200-DPI charts,
15 references as supplied). sha256 `fe63be84fe873ef57f1dde5ae0d588077d957b75d127b7a656a7fc884d8b9602`.
Charts extracted to `figures/`.

## What the paper does

Extends the `eduengine` Plackett–Luce / Tullock contest framework to universal-K–12 vertical-tier routing
(`fail = "track"`) for two systems:

- **Hong Kong** — single Grade-12 HKDSE gate, elite seat share `S = 0.23`.
- **South Korea** — stacked Grade-9 and Grade-12 CSAT gates, `S₁₂ = 0.12`.

Design: 30 matched stochastic seeds per arm, **14 arms, 420 runs**, `N = 400`, `T = 70`.

## Calibration (author-reported)

| benchmark | published | simulated |
|---|---|---|
| HK Grade 9 participation | 53.8% | 53.8 ± 0.1% |
| HK Grade 12 participation | 71.8% | 71.6 ± 0.1% |
| KR overall K–12 participation | 75.7–78.5% | 76.5 ± 0.1% |
| KR Q5−Q1 participation gap | 32.1 pp | 34.1 ± 0.3 pp |
| KR Q5/Q1 tutoring spend | 3.4× | 3.19 ± 0.02× |

## Counterfactuals (author-reported; total spend index, baseline = 100)

| arm | HK spend | KR spend | HK G12% | KR G12% | HK Q5 elite share | KR Q5 elite share |
|---|---|---|---|---|---|---|
| Baseline | 100.0 | 100.0 | 71.6% | 71.8% | 30.0% | 24.6% |
| CF1a tutoring tax +50% | 104.8 | 107.4 | 67.7% | 62.7% | 34.2% | 26.0% |
| CF1b effort cap / curfew −50% | 82.1 | 74.1 | 82.0% | 84.3% | 25.1% | 22.9% |
| CF2a marginal seat expansion | 117.4 | 105.9 | 79.3% | 82.0% | 28.6% | 23.7% |
| CF2b large seat expansion | 173.8 | 122.3 | 97.1% | 99.6% | 24.8% | 21.6% |
| CF3a wage compression ΔV −30% | 73.1 | 74.8 | 68.1% | 63.7% | 33.7% | 25.8% |
| CF3b wage compression ΔV −50% | 52.8 | 54.9 | 66.2% | 57.4% | 36.3% | 27.5% |

Paper's reading: a +50% tutoring tax raises total spend and top-quintile elite capture; expanding elite seats
raises Grade-12 participation and spend (the 2024 Korean medical-seat shock); only wage compression paired with
effort caps/seat expansion reaches the win-win frontier.

**Update 2026-11-25 14:00 CST (SIMULATION).** The exact patched engine + tested runner were received and the
540-run bundle job was reproduced (18 arms × 30 seeds; matches the supplied reference to last-bit float). On
the pre-stated Win-Win criterion (spend index < 80 **and** elite Q5 share below baseline, in both
jurisdictions), **the combined arms CF4a/CF4b fail**: CF4a fails in Hong Kong on elite capture (+2.28 pp above
baseline; Korea passes), and CF4b fails in both on spend (90.88 / 88.04). The only arm that passes is the
single effort-cap arm **CF1b**. So this reproduction does **not** support the "only wage compression paired
with caps/seats reaches the win-win frontier" reading. Note also that the reproduced run is an
**18-arm / 540-run / `N=300` / `T=46`** design — not the 14-arm / 420-run / `N=400` / `T=70` design tabulated
above, so the table is **not** reproduced here. Full numbers: `../code/REPRODUCTION_CF4_2026-11-25.md`.

## Verification status

- The four embedded charts were extracted and checked against the handoff numbers: **all four match**
  (calibration, counterfactual spend, seat-expansion, trade-off frontier).
- The exact patched engine files, the tested runner and the bundle reference output have now been received,
  verified byte-identical, committed, and **reproduced** (540/540 runs; see
  `../code/REPRODUCTION_CF4_2026-11-25.md`). That reproduction covers the bundle's 18-arm design, **not** the
  14-arm / 420-run design tabulated in this README, whose run code and results file are still not in the
  repository. The table above therefore remains **author-reported**.
- The reproduced CF4a/CF4b result is **negative** on the stated criterion (above); report it as SIMULATION and
  do not cite the win-win reading as reproduced.
- Treat as a draft. Do not quote as verified empirical findings; it is a simulation study.

## Charts

1. `figures/fig1_calibration.png` — published vs simulated benchmarks.
2. `figures/fig2_counterfactual_spend.png` — total K–12 spend by arm.
3. `figures/fig3_seat_expansion.png` — seat share vs Grade-12 participation.
4. `figures/fig4_tradeoff_frontier.png` — spend vs Q5 elite-admission share.
