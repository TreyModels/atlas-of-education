> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing here is a statement by, or endorsed by, the named individuals or any living person;
> names identify the published work each composite draws on, not participants in a deliberation.

# SYNTHESIS 008 — FINAL LOOP ADJUDICATION (for `lead`)

**Headline.** **The identification limits are established — scoped to this model class and this evidence base.** Five
claim classes are excluded by predeclared tests; eight of nine stop rules fired; the one surviving positive object is
a negative/identification map whose headline is *observational equivalence*, supported by a measurement programme and
a narrow Korean provider/fee descriptive note. This is a decisive close, not a salvage operation.

## 1. VERDICT

| Class | Status | Evidence cell |
|---|---|---|
| Gate architecture (where the binding gate sits) | **EXCLUDED** — tested, failed all six rates | E1: KOR 27.3/25.0/24.4 vs 86.0/75.4/66.4; HKG 14.4/19.7/46.7 vs 35.1/46.6/70.3 — all outside ±5 pp by 20–59 pp (`05b/loop5/runs/E1/findings.txt`) |
| Provider technology as the missing channel | **EXCLUDED** — fails thresholds; sign flips with priors; fees are rents | E2: hagwon 47.7 vs 73.7 (−26 pp); 3/36 quality parameterisations pass; T2 −55.3 pp at prior but 33/36 grid cells pass; cost-plus fees 1.5–4.2× cost (`05/loop5/E2/findings.txt`); does not rescue U1 (`05/loop5/LOOP5_STATUS.md`) |
| Cross-country shadow incidence | **EXCLUDED** — not identifiable with public targets | loop-3 S1 3/3 outside; S2 PH best 11.7 pp; E1b KOR no-fit −43 to −58 pp (`05b/loop5/runs/E1b/findings.txt`) |
| Mechanism classification (surplus vs competitive; demand- vs supply-led) | **EXCLUDED** — no identification; forced-ID persists | C1 equidistant fits 0.012–0.023, forced-ID 2/2; U2 recovery 0.50, forced-ID 0.30 (placebo)/0.50 (`05b/loop4/runs/U2`) |
| Country completion forecasting | **EXCLUDED** — fails out of sample and against naive benchmarks | U3 PH held-out MAE 14.68 vs naive 5.70 (FAIL); KHM 1.84 (PASS but one country); calibration hold MAE up to 16.5 pp; ledger long-run collapse (`05_experiments/loop2/findings_ledger.txt`) |
| Positive two-way feedback (general claim) | **EXCLUDED as universal**; retained only as asymmetry | loop-2 freeze-both: job side 3–4% generated; education side genuine; 20–40% shadow residual (upper bound) |
| Negative/identification map | **POSSIBLE (P1)** | C1, U2, loop-3, E1/E1b/U1b/U3, PARAMETER_MAP |
| Measurement programme | **POSSIBLE (P2)** | 6 country cards; SHADOW_TARGETS 21 rows (11 YES); shadow_round2 38 incidence + 20 fee rows; TARGETS 747 flow/13 shadow/4,031 economy; PARAMETER_MAP 8 observable/10 not |
| Korean provider/fee descriptive block | **POSSIBLE (P3), descriptive only** | E1b fee multipliers fit; E2 T3 3.56% inside band; cost-plus rent diagnostic; KOR official 2023 |
| Income-gradient demand channel | **WEAK REGULARITY, not a claim** | E4 2.14 vs 3.67 inside [1.84,5.51], monotone; mechanical identity 8.55 diagnostic (`05b/loop5/runs/E4`) |
| Japan density channel | **NOT REJECTED, not identified** | E3 required elasticity 0.226 in band; n=2 endpoints; T5 not computable (`05/loop5/E3/findings.txt`) |
| Relations layer | **PENDING/partial** — next experiment | `09_relations/` has panel WDI data + scripts; RELATION_CANDIDATES/DATA_PATTERNS/MODEL_PLUG_MAP absent |

**Verdict language (binding):** "Within this model class and the available evidence, identification of these five
claim classes is not established. This is a statement about the evidence base and the model, not about the world."

## 2. STOP-RULE AUDIT

| # | Rule (RESEARCH_LOOP §5) | Status | Evidence |
|---|---|---|---|
| 1 | Shadow incidence fails in ≥2 of 4 countries | **FIRED** | loop-3 S1: 3/3 assessable outside; E1b KOR no-fit fail |
| 2 | Two-way feedback imposed (job share unchanged when schooling frozen) | **FIRED** | loop-2 freeze-both: schooling adds 3–4% of job level |
| 3 | Identification fails (new moments cannot separate worlds) | **FIRED** | C1 no-ID/forced-ID; U2 recovery 0.50, forced-ID 0.30; U1b OOS fail |
| 4 | Cohort flows fail to balance | **NOT FIRED** | loop-2 ledger B1/B2/B3 = 0 exactly; note: long-run path collapses (E6 diagnostic), a different defect |
| 5 | Target coded as a parameter (restatement) | **FIRED** | HK 0.85 was the fitted moment (loop-2 Amendment L2-3); restatement test in brief 005/006 |
| 6 | Out-of-sample miss beyond predeclared threshold | **FIRED** | U3 PH 14.68 vs threshold 5.0/naive 5.70; calibration hold MAE 16.5 pp PH tertiary |
| 7 | Sign instability of an unmeasured parameter | **FIRED** | E18/E18b substitution sign flip; E2 T2 sign flips across 33/36 priors |
| 8 | Institutional-parameter audit (hand-set rules ⇒ description) | **FIRED** | E1 uses assumed CSAT/HKDSE dates; E2 assumed quality priors; KOR/HKG configs hand-set ⇒ description not mechanism |
| 9 | Two iterations without identification gain ⇒ stop claiming mechanism | **CONFIRMED** with definition: gain = predeclared threshold passed on a moment not used in fitting. Iterations 4–5: U2 no ID, U1b fail, E1 fail, E2 fail, E3 n=2; E4 weak regularity on a ±50% band | — |

**8 of 9 rules fired.** The programme's termination is rule-governed, not discretionary: the rule that ended its
central claims was predeclared before the results that fired it. That is the programme's methodological success.

## 3. FINAL PUBLISHABLE OBJECTS (ranked)

**P1 — "Observational equivalence and its limits: a predeclared negative map for a massification model."** (methods /
computational social science; the headline is PAGE's claim.) *Claim:* on available national aggregates, the leading
accounts (surplus/relational-floor vs competitive human capital; demand- vs education-led growth) are observationally
equivalent; gate architecture, provider technology as the missing channel, shadow incidence, mechanism classification
and completion forecasting are not identifiable with this evidence. *Evidence:* C1 equidistant fits + forced-ID 2/2;
U2 recovery/forced-ID; loop-3 S1/S2/S3; E1/E1b; U1b; U2/U3; E2/E3; PARAMETER_MAP (8 observable / 10 not). *Referee
asks:* predeclaration log with dates, recovery design, a second model class to show the equivalence is not one class's
artifact, data provenance, replication package.

**P2 — "Measuring massification and shadow education across six Asian systems: country cards, target register, and a
parameter observability map."** *Claim:* what can and cannot be measured, by country/stage/provider, with provenance,
denominators and confidence (incl. the finding that only 8 of 28 model quantities are observable). *Evidence:* six
country cards; SHADOW_TARGETS 21 rows (11 YES); shadow_round2 38 incidence + 20 fee rows; TARGETS 747 flow/13
shadow/4,031 economy; PARAMETER_MAP; WB snapshots. *Referee asks:* harmonisation and denominators, second coder,
versioning/update protocol, access log.

**P3 — "Provider fees, rents and the income gradient of private tutoring: a Korean descriptive calibration."
(conditional, descriptive).** *Claim:* fee levels and the income gradient are reproducible in a demand+rent block
(fee multipliers fit; fee/income 3.56% inside 1.1–5.0%; cost-plus 1.5–4.2× ⇒ rents/brand, not pure teacher time);
provider mix and incidence remain unidentified. *Evidence:* KOR MODS/KEDI 2023 (434/553k won; stage 462/596/740;
provider spend 241/37/22/16); E1b; E2 T1/T2/T3; E4. *Referee asks:* provider rent/cost data, an hours object, the 2011
archive, the survey's inclusion of arts/physical spend.

**P4 (conditional) — "What predicts massification? A graded relation panel"** — only if `09_relations` lands
(RELATION_CANDIDATES/DATA_PATTERNS/MODEL_PLUG_MAP currently absent; the WDI panel layer exists). Not a publication
yet.

**Do not publish:** any incidence, forecast, gate-architecture or provider-as-missing-channel paper.

## 4. DATA-FIRST PROGRAM (ranked by reopening power; cost/access route)

| # | Acquisition | Reopens | Cost / route |
|---|---|---|---|
| 1 | **PSA FIES/APIS/LFS microdata** (PH) | shadow incidence (national), wage premium by education, formality transitions, LFPR by education, formal wage premium | Credentialed data request (~2–6 weeks; PSA currently 403; via PSA microdata catalog / WB catalog application) |
| 2 | **Cambodia national tutoring module** (CSES/CLFS-style) | KHM national incidence (currently case study only) | NIS request + questionnaire advocacy (~2–6 weeks); no public route today |
| 3 | **Provider/firm data:** establishment censuses + WB Enterprise Surveys credential module | provider entry costs; credential requirement in hiring; formal-job creation elasticity — the most load-bearing NOT-observable parameters | WB ES API returns HTTP 000; microdata credentialed (~2–6 weeks) |
| 4 | **Korea 2011 archive + provider counts/fees** (KOSIS/KEDI) | KOR time path; E1b/E2 provider mix; the untraceable 2011 "90%" | Public tables/KOSIS query (~1 day–2 weeks) |
| 5 | **Japan fees (MEXT 子供の学習費調査, e-Stat API ID) + full 47-prefecture juku table** | E3 density identification (n=2 → n=47) | API application (~1–3 days) + MEXT/NIES table (~1–2 weeks) |
| 6 | **Hong Kong repeated gradient** (EDB/HKEAA + a re-weighted survey) | HKG OOS check; 1996/2010 weak rows | Institutional re-contact (~2–4 weeks) |
| 7 | **China post-2021 incidence/provider split** (CFPS/CEPS applications; MOE monitoring) | the CHN bound → a rate | Application (~4–8 weeks); registered/restricted |
| 8 | **LFS two-wave panels** (any country) | formal/informal transitions; mechanism classification | Institutional access (months) |
| 9 | **ILOSTAT/public-sector employment + formal wage premium** | public-sector share; formality payoffs | ILOSTAT registration/API (~weeks) |
| 10 | **Per-student spending + teacher pay sparse series** (UIS/EdStats/IMF) | cost structure; teacher-supply channel | Public/semi-public (~weeks) |

**Dissent (BRAY):** for *reopening cross-country incidence*, PH and KHM national surveys should rank above the Korean
archive; KOR ranks higher only on feasibility. Recorded and retained in §6.

## 5. CLOSE-OUT LANGUAGE for `06_report/LOOP_CLOSEOUT.md`

> **Loop close-out — 20 November 2026.** This programme built and tested a massification/credential model against six
> Asian systems using predeclared experiments, matched seeds, and a synthetic council auditing both design and
> results. It established its own limits.
> **What it found.** The mechanism suite reproduces its stored tables (floor/race, graduate supply, gates), and a
> Phase-0 ledger conserves people, money and jobs exactly. On available national aggregates the leading accounts —
> surplus/relational-floor versus competitive human capital, and demand- versus education-led growth — are
> observationally equivalent: they fit the same moments equally well, and a truth outside the candidate set is
> confidently mis-assigned (C1; U2 recovery 0.50, forced-ID 0.30–0.50). Gate architecture fails all six predeclared
> stage rates (E1), and provider technology fails its thresholds and reverses across defensible priors (E2);
> cross-country shadow-education incidence is not identifiable with the public targets available (loop-3 3/3 outside;
> the Korean no-fit benchmark fails by 43–58 pp); Philippine completion forecasts fail out of sample (14.7 pp versus a
> 5.7 pp naive benchmark). The only behavioural positives are a weak income-gradient regularity (2.14 versus 3.67)
> and a not-rejected Japanese density channel with n = 2.
> **What it could not do.** Identify its five central claim classes on the available evidence; claim any
> country-level shadow-education level or completion trajectory; classify mechanisms from national aggregates. These
> are limits of the evidence base and the model class, not findings about the world.
> **What the next team should do.** Treat the negative map and the measurement programme as the deliverable; acquire
> the ranked data (Philippine microdata, a Cambodian national module, provider/firm data, Korean and Japanese fee
> series); and run the graded relation panel before re-fitting any model. Eight of nine predeclared stop rules fired;
> the one that did not was cohort conservation, which passed exactly.

## 6. DISSENT RECORDED

- **BRAY** (three points): (i) the close-out must say "not identified with the available evidence and this model" — it
  does; (ii) data-first order should put PH/KHM national surveys above the Korean archive for reopening incidence —
  recorded, not adopted (feasibility ranking kept KOR higher); (iii) provider technology is excluded as *the* missing
  channel for the loop-4 inversion and as an identified explanation, not as a mechanism in the world — wording in
  P1/P3 reflects this.
- **PATRINOS**: rule 9 is blunt for a data-poor programme and E4/E3 are real signals; concurred after the definitional
  fix (gain = predeclared threshold pass on an out-of-fit moment).
- **PAGE**: adopted — the equivalence is the headline of P1, not a footnote.
- **CARTWRIGHT**: no dissent; the rule-governed termination is the programme's methodological success and is stated in
  the close-out.

**Final position:** the identification limits are established; the programme closes with a publishable negative map, a
measurement asset, and a costed data agenda. Files: `08_council/brief_008/`. Closing verdict posted to the bridge.
