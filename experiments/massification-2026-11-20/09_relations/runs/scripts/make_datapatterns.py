"""Render DATA_PATTERNS.md from the generated CSV results (no hand-typed numbers)."""
import os, pandas as pd
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data')
p=pd.read_csv(os.path.join(D,'panel_results.csv'))
h=pd.read_csv(os.path.join(D,'panel_heterogeneity.csv'))
e1=pd.read_csv(os.path.join(D,'event_windows.csv'))
e2=pd.read_csv(os.path.join(D,'event_windows_gmr.csv'))
s=pd.read_csv(os.path.join(D,'shadow_gradients.csv'))
w=pd.read_csv(os.path.join(D,'panel_wdi_wide.csv'))

def md(df, cols, title=None, fmt=None):
    out=[]
    if title: out.append('### '+title+'\n')
    out.append('| '+' | '.join(cols)+' |')
    out.append('|'+'|'.join(['---']*len(cols))+'|')
    for _,r in df[cols].iterrows():
        vals=[]
        for c in cols:
            v=r[c]
            if isinstance(v,float):
                vals.append(f'{v:.4f}' if abs(v)<10 else f'{v:.2f}')
            else: vals.append(str(v))
        out.append('| '+' | '.join(vals)+' |')
    return '\n'.join(out)

L=[]
L.append('# DATA_PATTERNS — panel, event-window and gradient estimates (09_relations)\n')
L.append('**Author:** `pattern-scout` · 2026-11-20 · task-21 · P4-conditional relations layer.\n')
L.append('**Data:** observed cells only. Panel = WDI live API pull (30 countries × 1970–2024, 45 indicators), '
         'archived in `raw/wdi/` and assembled in `data/panel_wdi_wide.csv`. Shadow numbers are the observed '
         'survey values already on disk in `04_data/shadow_round2/`. No imputed cell is used as an observation.\n')
L.append(f'**Panel coverage:** {len(w)} country-years; {w.iso3.nunique()} countries; {int(w.year.min())}–{int(w.year.max())}. '
         'Countries: CHN, HKG, KHM, PHL, KOR, JPN, VNM, THA, IDN, MYS, SGP, MMR, LAO, MNG (Asia) + '
         'IND, BGD, PAK, LKA, NPL, TUR, MEX, BRA, EGY, NGA, KEN, ZAF, PER, COL, MAR, UKR.\n')
L.append('**Method.** Two-way fixed effects (country + year) by alternating projections, OLS on within-transformed '
         'data, CR1 cluster-robust SE clustered on country. `levels-two-way-FE` = y on x with country and year FE; '
         '`first-difference` = Δy on Δx, which removes country-specific trends. Every result below is reproducible: '
         '`scripts/fetch_wdi_parallel.sh` → `scripts/build_panel.py` → `scripts/analyze_panel.py` → '
         '`scripts/analyze_hetero_events.py`.\n')
L.append('> **Identification warning, stated once for the whole file.** These are panel associations, not '
         'experiments. Country and year FE remove fixed differences and common shocks; they do **not** remove '
         'reverse causality, omitted time-varying confounders (reform packages, aid cycles, regime change), or '
         'measurement change in UIS/WDI series. Only R07 (fertility→completion) is graded plausibly-causal, and '
         'only because the timing ordering is structural. Everything else is correlational.\n')

L.append('## 1. Panel estimates (two-way FE)\n')
main=p[p.spec_type=='levels-two-way-FE'].copy()
main['driver']=main['driver'].str.replace('log_','').str.replace('_',' ')
main['outcome']=main['outcome'].str.replace('log_','').str.replace('_',' ')
L.append(md(main, ['spec','outcome','driver','lag_years','coef','se','t','p','n','n_cty','period','within_r2']))
L.append('')
L.append('## 2. First differences (country-trend-free check)\n')
fd=p[p.spec_type=='first-difference'].copy()
L.append(md(fd, ['spec','coef','se','t','p','n','n_cty','period','within_r2']))
L.append('')
L.append('''### How to read the two tables

- **The spending→enrolment channel is weak in levels and absent at primary.** S01 secondary GER elasticity 0.111
  (se 0.065) at a 5-year lag; S02 primary GER 0.021 (se 0.050); the first-difference versions are ~0
  (S01-FD 0.014, se 0.076). This is the honest bottom line: at 30-country FE, public spending does not buy
  measurable enrolment except in the Asia / low-enrolment splits below.
- **Income→tertiary is the strongest relation in the panel**: S09 0.848 (se 0.172). Income→secondary is weaker
  and lagged (S08 0.154, p=0.056; FD 0.369, p=0.014) — effects appear with a 5-year lag, consistent with the
  schooling pipeline.
- **Fertility→primary completion is the most robust relation in the file**: S13 −0.189 (se 0.044) at L0 and
  −0.098 (se 0.025) at L5, holding in every split. Cohort size suppresses completion.
- **The pupil-teacher ratio result has a sign conflict and is reported as not identifiable.** Levels say +0.385
  (higher PTR ↔ higher completion, i.e. an enrolment boom raises PTR first), first differences say −1.243
  (se 0.318): tightening teacher supply per pupil hurts completion. Both are in `data/panel_results.csv`; do
  not use either as a parameter.
- **Education→growth rejects the model's positive `eps_ec`.** S21: log GDP growth on tertiary GER 15 years
  earlier = −1.035 (se 0.240). This is not a causal estimate, but it is a direct failure of the "more
  tertiary → faster growth" prior that the two-way module assumes (eps_ec > 0 in 8 of its 10 regimes).
- **Teacher stocks co-move mechanically with enrolment** (S18 0.403, se 0.080; FD 0.322). Treated as a capacity
  constraint, not a behavioural parameter.
''')

L.append('## 3. Heterogeneity — where a relation holds and where it fails\n')
KEY=[('log_ger_s','log_spend_gdp',5,'spending→secondary GER'),
     ('log_ger_t','log_gdppc',0,'income→tertiary GER'),
     ('log_ger_s','log_priv_s',0,'private share→secondary GER'),
     ('log_spend_gdp','log_tax_gdp',0,'tax/GDP→education spend'),
     ('log_ger_p','log_tch_p',0,'teachers→primary GER'),
     ('log_cmpt_p','tfr',0,'fertility→primary completion')]
for y,x,kl,lab in KEY:
    sub=h[(h.outcome==y)&(h.driver==x)&(h.lag_years==kl)]
    L.append(f'**{lab}** (`{y}` ~ `{x}`)\n')
    L.append(md(sub, ['group_type','group','coef','se','t','p','n','n_cty']))
    L.append('')
L.append('''**Thresholds used for the splits** (`data/country_typology.csv`, 1985–2000 country means):
GDP per capita median US$1,706 (2015 constant); tax/GDP median 13.1%; 1990 secondary GER median 47.3%;
urban share median 40.2%. Asia = 19 countries (CHN, HKG, KHM, PHL, KOR, JPN, VNM, THA, IDN, MYS, SGP, MMR,
LAO, MNG, IND, BGD, PAK, LKA, NPL); non-Asia = 11 (TUR, MEX, BRA, EGY, NGA, KEN, ZAF, PER, COL, MAR, UKR).

**The three strongest conditionings** (these are the "only in certain types of countries" findings):
1. **Spending→secondary enrolment is an Asia/low-enrolment relation.** Asia +0.189** (se 0.090) vs non-Asia
   +0.010 (se 0.106); low-1990-GER +0.132* vs high-GER +0.077*.
2. **Private provision expands enrolment only where the state is weak.** Asia +0.086*** vs non-Asia +0.003;
   low-income-1990 +0.081*** vs high-income +0.014; low-tax-capacity +0.102*** vs high-tax-capacity −0.065.
3. **Fiscal space (tax/GDP) translates into education spending only in Asia and in low-urban settings**
   (+0.541*** and +0.582***), and not in non-Asia (−0.320 ns) — a state-capacity condition, not an income one.
''')

L.append('## 4. Event windows (interrupted time series: linear pre-trend + post level shift)\n')
if len(e1):
    L.append('### WDI panel outcomes\n')
    L.append(md(e1, ['iso3','event_year','outcome','jump_log','se','t','pct_jump','n','pre_rms']))
    L.append('')
if len(e2):
    L.append('### Observed GMR 6-country outcomes (`04_data/data/gmr_observed_6countries_1970_2024.csv`)\n')
    L.append(md(e2, ['iso3','event_year','indicator','jump_log','se','t','pct_jump','n','y_pre','y_post','pre_rms']))
    L.append('')
L.append('''**What happened to each event we could test.**

| Event | Tested? | Result | Reading |
|---|---|---|---|
| PHL K-12 (RA 10533, 2016) | yes, GMR observed | secondary GER jump −2.4% (se 3.3), ns | **no total-GER level shift**; the documented "surge" is a composition/denominator effect of adding G11–12 to upper secondary, not a level move. This is a null the model must reproduce (R18). |
| PHL free SUC tuition (RA 10931, 2018) | yes, GMR observed | tertiary GER jump −28.9% (se 7.7), t=−4.45 | enrolment **fell** through the event, confounded by the K-12 cohort delay. Do not read it as a tuition effect (R19). |
| CHN Compulsory Education Law (1986) | yes, GMR observed | +32% (se 18.5), t=1.50 | right sign, pre-trend noise 17%, only 19 obs → weak (R20). |
| THA Education Act 1999 | yes, WDI | −9.7% (se 2.7), t=−3.78 | a *decline* at the event; series break / no detectable jump. Not usable. |
| MYS 1996 K-12 expansion | yes, WDI | +2.3% (se 1.0), t=2.19 | small positive, consistent with a slow expansion. |
| IDN 9-year compulsory (1994) | yes, WDI | −1.2% (se 2.0), ns | no jump. |
| HKG 1971 / 1978 compulsory schooling, KOR 1974 equalisation, KHM 1996/2001 | **blocked** | not estimated | the observed-only GMR panel has <13 usable secondary-GER observations per event window (series start ~1998). Never imputed. Needs EDB (HK) / KEDI (KOR) national series before running. |
''')

L.append('## 5. Shadow-education gradients (observed survey values only)\n')
L.append(md(s, ['country','year','dimension','level','value_pct','source']))
L.append('''
**Computed elasticities/gradients (and what they are not):**
- **Gate gradient, HK 2003** (Bray & Kwok, EER 22:611-620, Table 1 p.616, one survey of 6 schools n=630):
  35.1% (S1–3) → 46.6% (S4–5) → 70.3% (S6–7), a **+35.2pp** rise at the senior gate. This is the cleanest
  within-country evidence that tutoring demand is **positional/gate-driven**, and it is exactly the
  `R_gate` channel in `twoway.py`.
- **Income elasticity of tutoring expenditure, Korea 2023** (MODS/KEDI official survey): 183 → 671 thousand
  won/month across the <3m vs ≥8m won income bands; income gap 2.67×, spend gap 3.67× → **elasticity ≈ 1.33**.
  Tutoring spending is a luxury good even in a rich country.
- **Two-margin fact, Korea 2023**: participation *falls* from 86.0% (elementary) to 66.4% (high) while
  expenditure per student *rises* 398 → 491 thousand won (+23%). A single-margin demand block cannot produce
  both; the model needs an extensive and an intensive margin.
- **Urban gradient**: Japan 57.9% (Tokyo) vs 22.1% (Akita) = 2.62× (Rappleye & Komatsu 2020, Table 2);
  Cambodia grade-6 60.5% urban vs 26.4% rural = 2.29× but from a **6-school case study**, not national.
- **The one relation the model most needs and the data cannot give: returns→tutoring.** Four countries, three
  usable shadow survey years, no common instrument → not identifiable (R26). Keep it as a prior.

## 6. What could not be estimated, and why (blocked, not omitted)

| Relation | Why blocked | What would close it |
|---|---|---|
| spending→enrolment, causal | no instrument; only FE association available | a school-finance reform with a rule-based discontinuity |
| PTR/class size→completion | sign conflict between levels and FD (R11) | a class-size rule (e.g. maximum-size law) event study |
| returns→tutoring | <5 country-year cells, no common instrument | household survey with earnings + tutoring module (PHL FIES/APIS microdata is credentialed) |
| remittances→schooling | small volatile series, migration selection | PHL province-level panel with remittance shocks |
| compulsory-schooling events (HKG/KOR/KHM) | observed GER series start ~1998 | EDB / KEDI / MoEYS national series |
| price elasticity of tutoring demand | no credible estimate located | KEDI price variation / a fee deregulation episode |
| teachers→learning (not just enrolment) | no learning outcome on disk for 30 countries | PISA/TIMSS linkage (not in this panel) |

## 7. Files
| File | Content |
|---|---|
| `data/panel_wdi_wide.csv` | 30-country × 1970–2024 wide panel, observed cells only |
| `data/panel_results.csv` | 66 specifications (levels FE + first differences) |
| `data/panel_heterogeneity.csv` | 110 split-sample regressions across 5 typologies |
| `data/event_windows.csv`, `data/event_windows_gmr.csv` | interrupted-time-series event estimates |
| `data/shadow_gradients.csv` | observed shadow-education gradients |
| `data/country_typology.csv` | country baseline groups (1985–2000 means) |
| `raw/wdi/*.json` | raw API payloads, one file per indicator × country chunk |
''')
open(os.path.join(ROOT,'DATA_PATTERNS.md'),'w').write('\n'.join(L))
print('wrote DATA_PATTERNS.md', len('\n'.join(L)), 'chars')
