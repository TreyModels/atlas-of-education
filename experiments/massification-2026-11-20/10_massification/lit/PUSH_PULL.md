<!-- Writer: lit-archivist, 2026-11-20, task-35. Scope: literature only. No model output below.
Verification legend: VERIFIED = primary text read this session (file in 02_lit/raw/ or /tmp archive, hash noted).
STANDARD-CITATION = canonical account, primary text NOT retrieved this session; the mechanism and any
thresholds are as standardly cited in the literature, and must be checked against the original before
publication. NOT-FOUND = searched and did not find; treat as a gap, not as zero. -->
# PUSH_PULL — does schooling follow jobs, create jobs, or co-evolve?

**Framing.** Three rival mechanisms, stated so each can lose. The programme must predeclare which quantities would count for and against each *before* estimating (per `10_massification/README.md` binding rules).

---

## Rival A — Demand-led (pull)
**Claim.** Education expansion is pulled by labour-market demand: rising returns, formal-job growth, sectoral upgrading, foreign demand for skilled workers.
**Mechanism.** Households respond to returns (human capital), firms bid for skills, states expand supply where employers demand it.
**Predictions.**
- A1. Returns lead expansion (returns up ⇒ enrolment up, with a lag).
- A2. Formal-job growth leads completion; the education series lags the employment series.
- A3. Skill shortages appear where expansion is slow (firms report skills as binding constraint).
- A4. Foreign demand shocks produce origin-country training booms.
**Evidence in hand.**
- **A4 is strongly supported (VERIFIED):** the US visa expansion produced **9 nurses licensed per additional nurse migrant** in the Philippines, +126% licensed nurses per 100k, with the response running through programme entry *and* pass rates; non-nursing enrolment declined (Abarcar & Theoharides 2024, NBER SI slides, `02_lit/raw/abarcar_theoharides2021_nber_slides.pdf`). This is the cleanest demand-pull evidence in the whole programme.
- **A3 is weakly contradicted (VERIFIED):** only **10.1%** of Philippine firms cite inadequate workforce skills as a *major* obstacle (7.8% in 2009; services 11.0%, manufacturing 7.3%) — World Bank Enterprise Surveys 2009/2015, Table 2.1 of the 2017 PHL skills report (`02_lit/raw/wb2017_phl_socioemotional_skills.txt`). If skills were the binding constraint on expansion, this should be far higher.
- A1: not established. Global returns are ~8.8%/yr and "very stable" (WPS8402) — stable returns are consistent with persistent pull but do not establish the lead-lag direction.

## Rival B — Supply-push / education-led
**Claim.** Educated cohorts create growth and jobs (human capital externalities, entrepreneurship, state capacity), or at least expand independently of demand (world society, warehousing).
**Mechanism.** Endogenous growth via human capital; institutional imitation; credential supply creating its own demand through screening.
**Predictions.**
- B1. Schooling leads (Granger-causes) formal-job creation or growth.
- B2. Graduate supply can rise with vacancies fixed, producing credential inflation and falling graduate returns rather than unemployment (the surplus-model signature; see October's graduate-shock experiment).
- B3. Expansion occurs in economies with stagnant demand and no skill shortage.
- B4. Where demand does not follow, overeducation and graduate unemployment rise.
**Evidence in hand.**
- B3 is supported by the institutional accounts (Schofer & Meyer; Trow's universal phase) and by the **10.1% firm-constraint** result above: expansion without an employer-side skills constraint is the supply-push pattern.
- B2 is a *model* result (GXL 2017 overshoot; the shadow-phase model's 0.14/−0.06/−0.36 graduate-shock table), not an observed estimate — do not present as evidence.
- B1: **NOT FOUND.** No credible estimate for any of our countries of schooling leading job creation. This is the central gap.

## Rival C — Complementary / co-evolution
**Claim.** Both directions operate; expansion and job structure co-evolve with matching frictions, so neither leads robustly and the two are often observationally equivalent in aggregate data.
**Predictions.**
- C1. Bidirectional causality in a well-powered panel; no stable lead-lag.
- C2. Structural transformation (sector shares) co-moves with education expansion without either leading.
- C3. Mismatch/overeducation indicators rise with expansion even when returns hold.
**Evidence in hand.** **No estimates retrieved.** The programme must therefore *demonstrate* the equivalence rather than assert it (README rule: "'both directions matter' is not a result unless the data can separate the channels or the equivalence is demonstrated").

---

## What the literature adds on specific channels

### Overeducation / graduate unemployment
**NOT VERIFIED this session.** No PHL/KHM/CHN/KOR estimate of overeducation incidence or graduate unemployment retrieved. The GXL 2017 model predicts the *phenomenon* (degree supply overshooting job demand), and GXL's motivating fact is descriptive: in 1970 <1% of US taxi drivers had degrees, now >15% (via Vedder et al. 2013, quoted in GXL). That is an advanced-economy regularit
y, not an estimate for our countries.

### Structural transformation / sectoral shifts
**NOT VERIFIED here.** Sector shares vs income are in the data-hunter's WDI panels (`04_data/data/wdi_4countries_long.csv`), not in the literature I retrieved. The theory (Gellner/Tilly) predicts a *co-movement* of sectoral and educational upgrading; the empirical lead-lag is unestablished.

### Migration and remittances
- **Place premium PHL = 3.99** (range 3.71–4.36) for observably identical workers vs the US (Clemens, Montenegro & Pritchett 2008, WPS4671, VERIFIED). This is a demand-pull *price* the household can respond to, and it is large.
- The nurse-supply response (9 per migrant) is the strongest causal evidence that households respond to foreign demand (VERIFIED).
- **Remittances → schooling: NOT VERIFIED.** The Clemens/Yang studies were not retrievable this session. Do not put a remittance-schooling coefficient into the model without reading them.

### Fertility / cohort effects
**NOT VERIFIED this session.** The hypothesis that shrinking cohorts raise per-child investment (the shadow phase's Japan/Korea argument) is plausible but unestimated here. A demographic channel needs cohort-size data — available in the data-hunter panels.

---

## Discriminating design (what would separate the rivals)
| Test | A (demand-led) predicts | B (supply-push) predicts | C (complementary) predicts |
|---|---|---|---|
| Lead-lag: formal-job growth vs completion, 1980–2024 | jobs lead | schooling leads | no stable lead |
| Foreign-demand shock (Abarcar–Theoharides style) | strong origin-country training response | weak/no response | response with lag and matching frictions |
| Firm skill-constraint share vs expansion rate | constraint high where expansion slow | constraint unrelated | constraint uncorrelated |
| Graduate-supply shock with vacancies fixed | graduate returns recover | diploma-holder income falls, relative wage rises | ambiguous |
| Returns vs enrolment correlation | positive | negative or zero | unstable |

**Honest bottom line.** The strongest *direct* causal evidence in hand is **demand-led in the migration channel** (nurse supply responds to foreign visa demand) — and the strongest *indirect* evidence against a skills-shortage version of demand-led is the low Philippine firm-constraint share. Everything about whether *schooling creates jobs* is currently unestablished. The programme should treat A-vs-B as the live question and C as the default that must be *proven*, not assumed.
