# Care-work loop and credential inflation: two Networked Domus dynamics tested (23 November 2026)

## What was tested, and the short answer
The pre-registration is `PREREGISTRATION.md`, committed as the branch's first commit (`7356e76`) before any
data extraction or estimation. Both dynamics were tested on the samples the data allow, and **both come back
as nulls on the real data**, with the pre-registered falsifiers doing the killing rather than the estimates.

- **Care-work loop: not supported.** The care share of female employment does rise steeply with female
  attainment — 8.1% in the bottom attainment tercile, 19.0% in the middle, 28.4% at the top (148 countries) —
  but the association is **fully absorbed by income and urbanisation** (attainment coefficient +0.009,
  t = +0.17, once log GDP and urban share are in; log GDP +0.24 t = 2.5, urban +0.42 t = 3.4). That is
  falsifier (ii) from the pre-registration, "fully explained by income/urbanisation", firing.
- **Credential inflation: not supported as a positional effect.** The credential-occupation gap (female
  tertiary attainment minus the share of female jobs in managerial and professional occupations) is almost
  unrelated to fertility (correlation -0.15) while attainment (-0.62) and the credentialed-jobs share
  (-0.65) both are; and the gap predicts fertility **worse** in high-attainment countries (R² 0.17) than in
  low-attainment ones (R² 0.50), the opposite of the saturation prediction.

## Data availability (what was obtained, what failed)
| source | what it gave | status |
|---|---|---|
| ILO SDMX `DF_EMP_TEMP_SEX_AGE_ECO_NB` | employment by sex and ISIC sector, 8 years 2010-2023 | **obtained**, 656 country-years, 148 countries with education/health detail |
| ILO SDMX `DF_EMP_TEMP_SEX_AGE_OCU_NB` | employment by sex and ISCO occupation, 2019 and 2023 | **obtained**, 122 country-years, 49 countries with the ISCO 1-2 share |
| World Bank WDI | total fertility (9,135 obs), female LFP (8,076), female upper-secondary attainment (2,344), female tertiary attainment (1,388), GDP per head (8,644), urban share (9,135) | **obtained** |
| ILOSTAT bulk download | flat files | **failed**: 403 from both ilostat.ilo.org and the webapps mirror |
| ILO SDMX single request 2010-2024 | all years at once | **failed**: 504 timeout; replaced by eight single-year requests |
| `/root/work/local_data/10_massification/JOBS_AND_MARKETS_PANEL.csv` | prior project panel | **checked, not used**: 6 countries, no sex-specific care-sector series (only agriculture/industry/services totals), so it cannot carry the care share |
Country coverage per ILO year: 2010: 48, 2012: 70, 2014: 89, 2016: 84, 2018: 99, 2019: 116, 2021: 105, 2023: 45.
Measures are sane: care share of female employment means **18.3%** (sd 12.1, range 1.2-52.1, n = 148),
against male care share 5.9% (n = 148) and female manufacturing 9.8% (n = 147).

## (1) Fertility

### Care-work loop
**A1, does the care share rise with the pipeline?** In the raw data, strongly: mean care share is 8.1% / 19.0%
/ 28.4% across attainment terciles (n = 47 each, 148 countries, latest ILO year per country). But with log GDP
per head in the model the attainment coefficient is **+0.009 (t = +0.17, n = 140)** while log GDP carries
+0.24 (t = 2.5) and adding urbanisation gives it +0.42 (t = 3.4). **The pipeline association is an
income-and-urbanisation association.** This is the pre-registered killing test and it kills A1.

**A3, does the education-fertility link steepen where care work is common?** Only in the raw form: the
interaction is -0.13 (t = -1.4, n = 141) without controls, and it **changes sign** to +0.13 (t = +1.5) with
log GDP and urbanisation. Not stable, so the amplification claim fails.

**Placebos behave like the treatment, which is decisive.** Replacing female care work with **male** care work
gives an interaction of +0.18 (t = +2.1), and replacing it with **manufacturing** gives -0.19 (t = -3.5) — the
unrelated-sector placebo produces a larger "effect" in the predicted direction than care work does. Falsifier
(iv) fires: whatever is being picked up is not about women's care employment.

**A2, does fertility fall faster where care work is common?** 119 country pairs (earliest vs latest ILO year),
fertility change on the early care share: +0.199 (t = 2.1) without controls — the **wrong sign**, i.e. higher
care share goes with *less* fertility decline — and -0.045 (t = -0.4) with log GDP. Null.

**Specification curve.** 36 specifications for the fertility-on-care-and-attainment model (two attainment
measures x three control sets x three samples x three fixed-effect patterns). The care-share coefficient
takes **both signs** across the curve (from about -0.57 to +0.27) and its significance tracks the fixed
effects, not the care measure. No specification survives as a robust care effect, and one degenerate
specification (perfect collinearity with the year dummies in a subsample) is reported rather than dropped.

### Credential inflation
**B1, does the positional measure beat attainment?** No. On the 46 countries with an occupational structure,
the correlation of fertility with the credential-occupation gap is **-0.15**, against **-0.62** for tertiary
attainment and **-0.65** for the credentialed-jobs share. The gap alone explains 2% of the variance. In a
horse race the gap does not survive: attainment keeps its coefficient (-0.81, t = -4.6) while the gap turns
**positive** (+0.33, t = +1.9) once attainment is in the model, which is the pre-registered "sign is the
opposite of predicted" falsifier. The reason is visible in the data: attainment and the credentialed-jobs
share are almost the same variable (correlation **+0.81**), so their difference is a small, noisy residual
rather than a queue position.
**B2, does the positional measure work better in saturated countries?** The reverse: in the 23 countries above
median tertiary attainment the model fits worse (R² 0.17) than in the 23 below it (R² 0.50), and the gap's
coefficient is larger and more precise in the *low*-attainment group. The saturation prediction fails.
Honest data limitation: the occupational measure exists for 46 countries and only 49 have the ISCO 1-2 share
at all, which is above the 30-country gate for a headline but is a small sample for a horse race, and
overeducation (education-by-occupation) could not be constructed for the same sample. It is declared
unavailable rather than approximated.

## (2) Massification
These results say the massification engine the theory proposes is **not visible in the cross-country data as
a care-work or positional mechanism**, and that is a substantive result rather than a missing one: the care
share is real and large (women are 18% of employment in education and health/social work, three times the male
share) but it lines up with national income and urbanisation, not with the schooling pipeline once those are
controlled; and the credential-occupation gap is almost collinear with attainment, so "queue position" as
measured here carries no independent information about fertility. What the data do support, strongly, is the
plain attainment channel: tertiary attainment correlates -0.62 with fertility and survives every control.
So the massification story from the earlier records stands on attainment and its consequences, without the
two additional mechanisms this job was asked to test — at least as far as this cross-section can tell.

## Limits
Cross-country associations, no causal claims. One observation per country in the cross-section (latest ILO
year, mostly 2019-2021), so country fixed effects are not available in the headline and the specification
curve is where time variation enters. ILO sectoral detail exists only for countries running detailed labour
force surveys, which over-represents middle-income and richer countries. The occupational sample is 46
countries. The gap measure assumes the same units for attainment and job shares (both percentages), which is
right in scale but not in concept: "credentialed jobs" is measured by occupation, not by required education.

## Files
`PREREGISTRATION.md` (first commit), `scripts/` (`build_care_cred.py`, `analyse_care_cred.py`, plus the small
fix/verification scripts), `results/` (`panel_cross_section.csv`, `panel_all.csv`, `coverage.json`,
`results_care_cred.json` with the specification curve, `results_fixes.json`, `results_B_clean.json`).
