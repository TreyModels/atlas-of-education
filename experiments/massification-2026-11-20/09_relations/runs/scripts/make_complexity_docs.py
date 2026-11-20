"""Render the complexity sections into DATA_PATTERNS.md, COUNTRY_TYPOLOGY.md, MODEL_PLUG_MAP.md."""
import os, pandas as pd
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,'data')
res=pd.read_csv(os.path.join(D,'complexity_results.csv'))
cond=pd.read_csv(os.path.join(D,'complexity_conditioning.csv'))
met=pd.read_csv(os.path.join(D,'complexity_metric_choice.csv'))
pan=pd.read_csv(os.path.join(D,'economic_complexity_panel.csv'))
def md(df,cols):
    out=['| '+' | '.join(cols)+' |','|'+'|'.join(['---']*len(cols))+'|']
    for _,r in df[cols].iterrows():
        vals=[]
        for c in cols:
            v=r[c]
            vals.append(f'{v:.3f}' if isinstance(v,float) else str(v))
        out.append('| '+' | '.join(vals)+' |')
    return '\n'.join(out)

# ---- DATA_PATTERNS section ----
sec=["\n## 9. Economic complexity (task-28)\n",
"**Canonical panel:** `04_data/complexity/ECONOMIC_COMPLEXITY.csv` (6 countries x 1995-2024, Growth Lab, Harvard Dataverse doi:10.7910/DVN/XTAQMC, CC0). "
"**Usable model-input file:** `data/economic_complexity_panel.csv` (180 rows, 27 columns: ECI SITC/HS92/HS12 + ranks, growth_proj, "
"`eci_pctile`, `eci_z_year`, `eci_growth_5y`, `complexity_gap` = ECI minus the year-by-year income-implied ECI, `complexity_quadrant`, "
"plus merged gdppc, tertiary/secondary GER, completion, spending, wage-and-salaried share, vulnerable share, urban share, population, fertility). "
"A 30-country ECI column set for panel tests: `data/economic_complexity_panel_30ctys.csv`.\n",
"**Coverage for the six countries:** CHN, HKG, JPN, KHM, KOR, PHL all have **30/30 years (1995-2024)** for `eci_sitc` and `eci_hs92`; "
"`eci_hs12` only 2012-2024 (13 years); `growth_proj` 2004-2024. No gaps, no proxies needed for the six.\n",
"### ECI relations (two-way FE, CR1 clustered on country)\n", md(res,['test','outcome','driver','coef','se','t','p','n','n_cty','period','within_r2']),
"\n### Does complexity condition the spending and returns channels? (interaction tests)\n",
"Interactions use within-country-centred ECI, so country FE absorbs the ECI level and year FE absorbs common shocks; the interaction is the "
"within-country co-movement of the driver with complexity.\n", md(cond,['test','outcome','driver','coef','se','t','p','n','n_cty','note']),
"\n**Answer:** complexity does **not** condition the spending->enrolment channel (interaction 0.081, se 0.080, p=0.31; completion 0.144, se 0.099, p=0.15). "
"It **does** condition the education->growth channel, **negatively** (completion x ECI -0.039, se 0.015, p=0.007; tertiary x ECI -0.077, se 0.020, p<0.001): "
"schooling's growth payoff is concentrated in low-complexity economies in this sample. Complexity also does not condition the income->tertiary channel "
"(0.014, se 0.010, p=0.19).\n",
"### Best single complexity metric\n", md(met,['metric','n','n_cty','years','b_gdp','t_gdp','r2_gdp','b_tert','t_tert','r2_tert','b_cmpt','t_cmpt','r2_cmpt','yr_on_yr_sd','corr_sitc_hs92']),
"\n**Recommendation:** ingest **`eci_hs92`** as the primary country-year index (strongest GDP relation, standard modern classification, full coverage, "
"most stable year-on-year), carry **`eci_sitc`** as a robustness column (correlation 0.983; all relations agree within ~1 SE). "
"Never ingest **ranks** (relative, not levels), **`growth_proj`** (fails as a predictor, R36), or a spliced HS12 series (2012+ only).\n"]
p=os.path.join(ROOT,'DATA_PATTERNS.md'); s=open(p).read()
if '## 9. Economic complexity' not in s: open(p,'w').write(s+'\n'.join(sec))
print('DATA_PATTERNS updated')

# ---- COUNTRY_TYPOLOGY section ----
sec2=["\n## 7. Complexity as a second typology dimension (task-28)\n",
"**Why add it:** the Council asked whether complexity is the missing country-type axis. The tests above say: it is a *descriptive* axis and a "
"conditioner of one channel (education->growth), but **not** a conditioner of the spending channel. It should be added to the typology, but as a "
"secondary axis, not as a replacement for the state-capacity flag.\n",
"**ECI levels for the six countries (SITC, 1995 -> 2024):** JPN 2.06 -> 1.54 (high, falling); KOR 1.23 -> 1.44; HKG 1.16 -> 1.42; "
"CHN 0.72 -> 1.30 (fast catch-up); PHL 0.34 -> 0.75; KHM -1.32 -> 0.30 (from far below zero). The income ordering and the complexity "
"ordering are *not* the same: HKG is richer than KOR but slightly less complex; CHN is poorer than HKG but converging fast.\n",
"| Typology cell | Countries (1995) | Relations that are live | Relations that are dormant |",
"|---|---|---|---|",
"| **low complexity + low income** | KHM, IND, BGD, PAK, LAO, MMR | T1 spending->enrolment, T2 private provision, T3 tax capacity, T5 teacher supply, R07 fertility, R42 completion<-ECI, **R48 schooling->growth payoff is largest here** | ECI->tertiary (income carries it), spending x ECI |",
"| **low complexity + high income (resource/rentier)** | MYS (1995), TUR, MEX, ZAF, NGA | T1, T2, T3 still live; R48 payoff fading | ECI->completion weak |",
"| **mid complexity + mid income** | CHN, THA, IDN, PHL(2024), VNM | R41 income->tertiary, R42 ECI->completion survives income, R45 ECI->growth null | R48 payoff near zero |",
"| **high complexity + high income** | JPN, KOR, HKG, SGP | R21 gate tutoring, R22 income elasticity, R23 two-margin shadow demand, R49 metric | T1/T2/T3/T5 dormant (capacity not binding); R48 schooling->growth payoff fades/reverses |",
"\n**The key conditional finding (state it plainly):** for the *model's* purposes, complexity is a good **state variable** and a poor **mechanism**. "
"Use it to set a country's initial complex-job share and formal-job pool (massabm `vac_paths`, twoway `Vc0`, `eps_ec`), and to label the typology cells — "
"but do **not** use it to switch the spending elasticity (the interaction is a clean null) and do **not** assume higher complexity means a bigger schooling "
"payoff (the interaction is negative in this sample).\n"]
p=os.path.join(ROOT,'COUNTRY_TYPOLOGY.md'); s=open(p).read()
if '## 7. Complexity as a second typology dimension' not in s: open(p,'w').write(s+'\n'.join(sec2))
print('COUNTRY_TYPOLOGY updated')

# ---- MODEL_PLUG_MAP section ----
sec3=["\n## E. Economic complexity (task-28) — a country index, not a mechanism\n",
"**What is on disk:** `data/economic_complexity_panel.csv` (6 ctys x 1995-2024, 27 columns, ready to ingest: `eci_hs92` primary + `eci_sitc` robustness + "
"derived `eci_pctile`, `eci_z_year`, `eci_growth_5y`, `complexity_gap`, `complexity_quadrant`, merged education/economy columns).\n",
"| Relation (register id) | Plug point (exact) | Functional form | In-model validation | Grade |",
"|---|---|---|---|---|",
"| R41 ECI -> tertiary GER | `twoway.py`: `Vc0` (complex vacancies) and the `c_t` logit. Complexity shifts the *level* of complex demand, not the elasticity | `Vc += b_eci * (ECI_t - ECI_1995)`, b_eci calibrated from 0.23-0.31 log points per ECI point, **but** the income control absorbs it, so prefer `Vc0` scaling by country | raise ECI alone with income fixed; tertiary entry should barely move (data: 0.120, ns) | correlational |",
"| R42 ECI -> completion | `massabm` `bar_basic` / completion floor; `twoway` `s_t` intercept | level shift in the completion logit: `+0.139*(ECI_t-ECI_1995)` | hold income fixed, raise ECI 1 point -> +14% completion; if the model's ECI term is a relabelled income term it double-counts | correlational |",
"| R43 ECI -> secondary GER | `twoway` `s_t` intercept | as above, lower-secondary margin only (upper-secondary ns) | separate lower and senior gates in the response | correlational |",
"| R44 ECI -> formal share | `twoway` complex-vs-routine job split; `massabm` formal/informal shares | `formal_share += b*(ECI)` with b≈+0.03/point, **not significant** — treat as a sign prior, not a parameter | the model must not make complexity the formalisation driver; the income->formal channel is far stronger (6.11, se 1.54) | low |",
"| R45 ECI -> growth | **do not plug** | the Growth Lab premium does not replicate (-0.142, se 0.105) | run the same 10y regression on model output; a positive premium the data lack = over-fit to literature | null |",
"| R47 ECI x spending | **do not add** | the interaction is a clean null (0.081, se 0.080) | spending shocks in high- vs low-ECI presets must differ only via income/tax capacity | null |",
"| R48 ECI x schooling -> growth | `twoway` `eps_ec` / `ret_S`, `ret_C`; `massabm` `wage_hc` | if returns are made complexity-dependent: `eps_ec(ECI) = eps0 - 0.077*ECI` (the data sign), **not** `eps0 + k*ECI` | run rising vs falling returns-in-complexity; the data favour falling. If the model needs rising to fit the four countries, report that as a finding | low-medium |",
"\n**Hard caveats from `04_data/complexity/COMPLEXITY_MAP.md`, restated because they matter:** complexity is a *country-level index*, not a mechanism; "
"it may condition or proxy latent capability, never identify a causal effect. Do not treat ECI as schooling or education quality; do not use rank changes as "
"level changes; do not splice SITC/HS92/HS12; do not claim complexity causes education demand (it is endogenous to income, schooling and industrial policy); "
"do not use `growth_proj` as evidence for an education->growth effect.\n"]
p=os.path.join(ROOT,'MODEL_PLUG_MAP.md'); s=open(p).read()
if '## E. Economic complexity' not in s: open(p,'w').write(s+'\n'.join(sec3))
print('MODEL_PLUG_MAP updated')
