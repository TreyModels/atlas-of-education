# Paper N3 record — the agricultural floor and the subsistence transition

**Status:** complete draft for the agricultural-development audience, 25 November 2026. The manuscript is `paper.md` (7,000-9,000-word target; ~7,800 words including tables). Written for *American Journal of Agricultural Economics* / *Journal of Development Economics* / *Agricultural Economics* / *World Development* / *Food Policy*, not for the education or demography audiences.

**Branch:** `research/paper-agdev-2026-11-25` (off `main`).
**Sources:** `research/subsistence-2026-11-23` @ `41f6429`; `research/subsistence-v2-2026-11-23` @ `ce66cfc`; `research/supply-demand-2026-11-23` @ `963e5e5`. Every quantitative statement is mapped to branch @ hash → file → field in `claims-to-source.md`.

## What is in this directory

- `paper.md` — full manuscript: abstract; introduction; the floor and the replication; the release and why the panel cannot order it; the sequencing result; the joint model as a demonstration; an agricultural-development literature review; implications; future research; limitations; reproducibility; appendix with definitions, data and suggested figures.
- `claims-prior-art.md` — claim-by-claim prior art with replicated / corrected / new columns, closest competitor named, search strategy recorded, no "first".
- `refs.md` — APA 7 references with Crossref status, including the flagged unverified entries.
- `claims-to-source.md` — the number → branch @ hash → file → field map.
- `README.md` — this file.

## The core argument in plain words

**1. The floor.** Poor countries keep labour in agriculture partly because investment goods and inputs are expensive relative to labour, so farmers substitute labour for machines and fertiliser. We rebuilt the objects this argument needs from public agricultural, price and macro data and re-estimated them. The direction replicates: expensive inputs go with low input intensity; low intensity goes with a large agricultural employment share; inputs explain between 55 and 69 per cent of the farm productivity gap between rich and poor countries (the original paper says "a bit less than two-thirds"). Our substitution elasticities are lower than the original's (1.24 and 1.11 against 1.90 and 1.75), and we cannot estimate the land margin at all. So it is a partial replication, not a confirmation — and the paper says so.

**2. The release.** The theory needs inputs to be adopted before labour leaves the farm. In a country panel, that sequence is not visible: the level association has the wrong sign, the reverse association (past labour release predicting current intensity) is stronger, and past changes in intensity do not predict the next decade's labour release. Labour release also does not visibly move schooling or fertility at ten-year horizons: the fertility estimate is −0.0003 with a standard error of 0.0058, and a change of 0.016 births would have been detected. This is a precise null, not an imprecise one.

**3. The surprise.** In 64 late-industrialising countries with dates for all three transitions, schooling take-off comes before the large agricultural labour release in 31 of the 34 countries where the order can be identified (the other 30 have dates on the 1965–2010 window boundary and cannot be ordered; median gap 18 years where both dates are exact). Labour-market demand — wage premia and paid jobs — leads the schooling take-off in only 7 per cent of countries, and a supply-versus-demand horse race on ten-year changes gives a supply composite of +0.456 (SE 0.174) against a demand composite of +0.006 (SE 0.203). The direction — schools before factories — is not new (Sandberg 1979; the world-polity school); what is new is the systematic 64-country coding and the horse race. It contradicts the standard structural-transformation sequence in development economics, and that is the useful part for policy.

**4. The model.** A joint demography-agriculture-absorber model reproduces the shape of the transition and produces counterfactuals: freezing mechanisation leaves 39.9 per cent of labour in agriculture and cuts schooling to 0.2 years; freezing the schooling pipeline leaves released labour unabsorbed (schooling 3.0 years, fertility 2.94); freezing the mortality decline removes the population explosion (population index 0.39 against 1.58). Two of five parameters are well identified, and the population path is mis-fitted (1.58 against 2.92). It is a demonstration of model structure, not an estimate of history.

## Verified vs provisional

**Verified (from the pushed records, reproducible):** all replication estimates (S1 `replication.json` / `replication.txt`); all corrected reduced-form tests (S1 `corrected_test.json` / `corrected_test.txt`); the 64-country event sequencing and the US order (S2 `sequencing.json` / `sequencing.txt`), with the **strict fertility ordering** recomputed from S2 `results/event_dates.csv` (canonical: paper-massification @ `95dc135`, `data/recompute_fertility_ordering.json`; source record annotated at S2 @ `8caaeac`); the supply-demand ordering and horse race (S3 `supply_demand.json` / `supply_demand.txt`); the v2 model parameters, fit, recovery and counterfactuals (S2 `model_v2_summary.txt`, `model_v2_params.json`, `model_v2_counterfactual.csv`); the v1 comparison values (S1 `model_summary.txt`, `model_params.json`).

**Provisional / weakest claims (flagged in the paper):**

- **The sequencing result is a coding and censoring result.** The earlier 61/64 and 26-year median treated window-boundary dates as exact and are withdrawn (31 forward and 3 reverse among 34 identified; 30 unordered). It depends on the event thresholds (3 points in 10 years; 1.0 year in 10 years; 1.0 birth in 10 years), the 1965-2010 window, and the schooling series' coverage (61 of 108 schooling take-offs sit on the window boundary). A date-by-date source table and an alternative-threshold robustness exercise are required before submission.
- **The direction is not new.** Sandberg (1979) and the world-polity school documented schooling before industry. The paper claims systematic measurement, not discovery.
- **The schooling-before-fertility ordering is weak and was mis-reported in the source JSON.** Strictly, schooling comes before the fertility decline in 24/64 = 37.5% (95% CI 26.6-50.0%), with 20 simultaneous and 20 fertility-first; the record's 68.75% counted ties and is not used (see "(1) Fertility"). Only the schooling-before-release result (31 of 34 identified) is strong enough to carry the sequencing claim, and it covers only the identified countries.
- **The horse race is a decomposition, not a causal test.** Education policy, state capacity and income are jointly determined; no instrument.
- **The model's counterfactuals are structural illustrations, not forecasts.** Two of five parameters are well identified; the population path is mis-fitted.
- **The replication is partial.** Original data are not public; the intermediate price is proxied; the land elasticity is untestable; our elasticities are lower than the original's.

**Unverified citations:** Sandberg (1979), Kuznets (1957/1973), Timmer (2009), Foster and Rosenzweig (1995, 2010) could not be resolved via Crossref in-session; they are flagged in `refs.md` and cited only where no page-specific claim rests on them.

## (1) Fertility

The paper's fertility content is deliberately modest. The corrected test finds **no** decadal effect of agricultural labour release on fertility (change −0.0003, SE 0.0058, n = 503; MDE about 0.016 births). The event sequencing finds that the schooling take-off comes **strictly** before the fertility decline in 24 of the 64 countries (37.5%; bootstrap CI 26.6-50.0%), with 20 simultaneous take-offs (31.3%) and 20 fertility-first (31.3%), median gap 0 (IQR −5 to +8); across all 81 countries with both dates it is 29/81 = 35.8%. (The source record's `pct_schooling_before_fertility` = 68.75 counted the ties as schooling-first and is **not used**; the record is annotated at subsistence-v2 @ 8caaeac, and the canonical strict recomputation is at paper-massification @ 95dc135.) The joint model produces a fertility path of 4.40 in 1960 to 2.35 in 2020 (data 6.01 to 2.06) driven by the mortality decline and the schooling/pipeline expansion, and its counterfactuals raise fertility when the pipeline or the mortality decline is frozen. All of that is model-level or timing-level, not an estimated fertility effect, and the paper labels it that way. Nothing here supports the claim that mechanisation causes fertility change.

## (2) Massification

This is the paper's strongest agricultural-development result. The cross-section supports the price mechanism; the panel cannot order the release; and the sequencing exercise puts the schooling expansion **before** the farm exodus in 31 of the 34 countries where the order can be identified (30 cannot be ordered), with labour-market demand leading in only 7 per cent and the supply block dominating the horse race (+0.456 against +0.006). The policy reading is that rural schooling investment may be a precondition for, not a consequence of, agricultural modernisation — the opposite of the standard sequencing assumption. The paper is explicit that this is timing plus conditional association, not causal identification, and that the direction is documented in the older economic-history literature; the increment is the systematic measurement.

## What an agricultural-development referee will attack first

1. **The cross-section is not causal**, and the paper does not claim it is. The replication is partial and the elasticities are lower than the original's.
2. **The dynamic failure** could be read as evidence against BKKM. The paper says the panel cannot identify the sequence, not that the mechanism is false; the cross-section and the theory are left standing while the dynamic claim is withdrawn.
3. **The sequencing coding** (31 of 34 identified, 30 undetermined) needs a date-by-date source table and threshold robustness; the paper flags this as the central empirical vulnerability.
4. **The sequencing direction is known** in economic history; the paper does not claim discovery and cites Sandberg and the world-polity school.
5. **The model's counterfactuals** will be read as forecasts unless labelled; the paper labels them a demonstration and reports the mis-fit.

## Files and provenance

Scripts and results live on the three source branches at the hashes above; the raw WDI pull (207,622 rows) and the OWID/FRED pulls are on the project server and are not committed. The pre-registrations were the first commits on each source record (`d47e5ed` for S1, `62730fc` for S2, `f7b38f3` for S3), before data work. Runtime is seconds to minutes on one core after the data pulls. No compute was run for this paper: it reorganises and re-frames results that already existed, with no new estimates.

## Report-format compliance

- Plain words: this README and the paper's abstract are readable without variable names; technical sections use standard terms for the ag-dev audience.
- The two applications are sorted under "(1) Fertility" and "(2) Massification" above, and in the paper's sections 3, 4 and 7.
- For every headline number: the estimate, the uncertainty (SE, CI or bootstrap), the sample (n, countries), and the test designed to kill it (pre-registered falsifiers; reverse checks; horse race; recovery test) are stated.
- Nulls are prominent: the dynamic release sequence is not identified, and the release-to-fertility link is a precise null.
- Every number is traced in `claims-to-source.md`; provisional items are flagged above.
