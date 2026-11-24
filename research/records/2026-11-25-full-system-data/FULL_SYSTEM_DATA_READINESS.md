# FULL-SYSTEM DATA READINESS — massification model

**Task-41.** Branch `research/full-system-data-2026-11-25` (additive, from handoff `e8ba60c`).
Machine-readable companion: `full_system_data_readiness.csv` (22 datasets across the 7 modules).
**Scope:** what observed data actually exist for a credible *full-system* massification model (household demand,
state supply, learning, gates, jobs, rural-urban/migration, macro), coverage/vintage, **construct mismatches**,
what is missing, and whether the model could use each **without inventing a target**. No invented targets, no
causal claims; data tiers labelled observed / reconstructed / gated.

## Readiness in one line per module

| module | best available data | coverage / vintage | construct mismatch | missing | can the model use it without inventing a target? |
|---|---|---|---|---|---|
| **1. Household demand / affordability** | DHS IR (gated) + DHS API aggregates; LSMS; Global Findex | DHS ~90 ctry, 1985-2024; LSMS irregular | women's education/CEB and asset indices ≠ household schooling demand; no fees/forgone earnings; DHS IR no attendance module | household income/consumption linked to schooling, fees, distance, opportunity cost | **No for a demand equation** — only for fertility/education associations and ecological gradients; IR under DUA can test individual schooling→fertility (designed), not affordability |
| **2. State/school supply** | UIS/EdStats pupil–teacher ratios, teachers, private share | ~200 ctry, 1970-2023 | headcount ratios ≠ effective teacher supply/quality; capacity never observed | school-level capacity, funding per pupil, teacher allocation | **Partly** — teacher/ratio covariates usable; capacity as latent with declared mapping, no invented target |
| **3. Learning/quality** | PISA/TIMSS/PIRLS, SACMEQ/PASEC/LLECE, WB Learning Poverty/HCI | assessments 1995-2022, ~80-90 ctry (many E8 missing) | assessment scales not equated; sampled populations differ; composites are imputed | annual grade-level learning profile (Pritchett's flat α(g)) | **Only as anchors** at assessment years; a grade-profile target would have to be *invented* |
| **4. Gates / transitions** | EdStats completion (SE.PRM.CMPT.ZS) + transition rates | ~120 ctry, 1970-2022 | completion is model-based, not exam pass; transition ≠ admission rule; no quotas/cutoffs | exam pass rates, admission rules, quota data harmonised | **Proxy only** — declared "gate severity" index from completion/transition, no causal target |
| **5. Jobs / credentials** | ILOSTAT wages by education; STEP (gated); repo credential-floor record | ILOSTAT ~150 ctry 1990-2023; STEP ~20 ctry | wage premia ≠ returns; informality undercount; credential requirements absent | credential-requirement series, returns by level comparable | **Returns proxy only**; credential-floor record is a sanity anchor, not a panel |
| **6. Rural-urban / migration** | WDI urban share; UN migrant stock/remittances; DHS residence | WDI 1960-2023; migration 1990-2020 | urban share ≠ migration flows; stock ≠ flows; self-reported residence | internal rural→urban flows, age/education composition of migrants | **No flow module**; urban share only (level). DHS migration module in selected rounds (gated) |
| **7. Macro / development** | WDI GDP/growth; GGDC/PWT (repo E6); WID/SWIID | 1950-2023 | GDP ≠ development; PWT demand series post-1990 only (E6) | harmonised inequality panel; human capital in same vintage | **Yes** — development covariates directly usable; E6 already established coverage limits |

## Construct mismatches that must be carried into any model statement

1. **Children in employment ≠ child labour** (WDI `SL.TLF.0714.ZS` is "children in employment"; labour is a legal/ILO
   construct not measured by that series).
2. **Shares of employed children ≠ child-labour rates** (`SL.TLF.0714.SW.ZS` denominator is employed children).
3. **Gross enrolment ratio (GER) ≠ net attendance share ≠ completion**; the model's "GER" is a share of children,
   not the WDI gross ratio (can exceed 100 %).
4. **Attainment (Barro-Lee) ≠ enrolment ≠ completion**; attainment is back-cast.
5. **Test scores are not equated across PISA/TIMSS/PIRLS/SACMEQ/PASEC/LLECE**; only within-assessment comparisons
   are defensible.
6. **Wage premia ≠ returns to schooling**; ILOSTAT wages cover employees, not informal work.
7. **Urban share ≠ migration**; UN migrant stock is cross-border, not rural-urban.
8. **DHS "education" is women's attainment**, not household demand; IR has fertility/birth histories, not fees.

## Top 5 gaps that block a credible full-system model

1. **Household demand/affordability microdata**: no public, harmonised household income/consumption × schooling
   (fees, forgone earnings, distance) panel; DHS IR is gated and lacks fees. The demand side of massification is
   therefore **not identified** by available public data — a "demand" equation would need invented parameters.
2. **Learning/quality at grade level**: no annual, comparable grade-level learning series; only sampled assessment
   anchors. A "flat learning profile" claim would be an assumption, not a target.
3. **Gate/admission rules**: no harmonised exam-pass/admission/quotas data; completion/transition proxies cannot
   separate capacity rationing from exam screening.
4. **Rural-urban migration flows**: urbanisation levels exist, flows and their education/age composition do not;
   an internal-migration module would have to be calibrated to an invented target.
5. **Credential requirements / returns by level**: wage premia exist, but credential-requirement series and
   comparable returns by education level (with informality) are missing for a jobs/gates feedback loop.

## Top 5 datasets usable immediately (no invented target)

1. **WDI/EdStats enrollment + completion + pupil-teacher ratios** (`SE.PRM.ENRR`, `SE.PRM.CMPT.ZS`,
   `SE.PRM.TCHR`, `SE.PRM.ENRL.TC.ZS`) — ~200 countries, 1970–2023, public API. State-supply and enrollment
   covariates; declared construct mapping required.
2. **WDI/ILO-UCW children-in-employment series** (`SL.TLF.0714.ZS`, `…WK.ZS`, `…SW.ZS`) — 1990–2023, E8 coverage
   sparse but usable; **construct-correct**: employment, not labour; shares of employed children for the overlap.
3. **GGDC/PWT + the E6 record** (`research/records/2026-11-25-e6e8-sequencing`, E6 classification) — structural
   change/employment shares 1950–2019, with the documented post-1990 demand-coverage limit; already used in the
   wave, reproducibly.
4. **DHS API aggregate tables** (education-specific fertility/CEB; `api.dhsprogram.com`) — ~90 countries,
   1990–2024, public; ecological use only (never individual inference without IR/DUA).
5. **UIS/EdStats + Barro-Leé/Cohen-Soto attainment** — for cohort attainment cross-checks and back-cast
   plausibility; reconstructed tier, label as such.

## What this implies for the model (no causal language)

- The **macro/development** and **state-supply** blocks can be built from public observed data today.
- The **learning**, **gates**, **jobs** and **rural-urban/migration** blocks can be included only as *declared
  assumptions* (anchors/proxies) — each must be labelled reconstructed/model-imputed with its mapping stated.
- The **household demand/affordability** block is the binding gap: it is the one module where the data needed to
  discipline the model do not exist publicly, and the DHS IR route (access plan `research/dhs-acquisition-2026-11-24`
  @ `77a2285`, still waiting on DUA) only gives individual education↔fertility, not fees/affordability.
- **A full-system model can therefore be built in a "constrained" form**: observed macro + supply, declared
  assumptions elsewhere, and every non-observed target labelled; a model that claims to *fit* demand, gates, jobs
  or migration targets with existing public data would be inventing them.

## Provenance

- Repo records: E6/E8 `research/e6e8-sequencing-2026-11-25` @ `bd782be`; source verification @ `ea6bc61`;
  DHS acquisition @ `77a2285`; E11 fertility audit @ `e926575`; Q2 @ `9a4f586`; E1 @ `6a452a4`.
- Public sources listed with URL host in the CSV; all figures in this document are **coverage statements**, not
  estimates. Data tiers: observed / reconstructed / gated as marked in the CSV.
- No server compute used. No invented targets. No causal claims.
