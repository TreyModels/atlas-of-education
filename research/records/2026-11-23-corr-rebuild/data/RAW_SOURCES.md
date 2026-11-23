# Data sources (task 15)

Project panel, box2 `/root/work/data` (observed annual country-year series, 1960-2024):
fertility (total fertility rate), primary completion, secondary enrolment, lower-secondary completion,
tertiary enrolment, gender parity indices, income per head (file holds LEVELS; natural log taken in the
scripts), urbanisation, country metadata (region, income group).

Our World in Data grapher exports, downloaded 2026-11-23 to box2 `/root/work/corr_rebuild/raw`
(exact URLs in `scripts/download_raw.sh`; raw files not committed, ~1 MB):
- `mean-years-of-schooling` — average years of education, 15+ (Barro & Lee via OWID), 1870-2020, total.
- `average-years-of-schooling-males-vs-females` — mean years of schooling by sex, 1990-2023; used for the
  female and male series (Barro-Lee based).
- `gender-ratios-for-mean-years-of-schooling` — adjusted gender parity index, 25+, 1970-2024.
- `cohort-fertility-rate` — completed cohort fertility by birth cohort, 33 countries, cohorts 1876-1975.
- `children-per-woman-un` — UN WPP total fertility rate (cross-check only).

Known acquisition failure: the Barro-Lee official site (barrolee.com) was unreachable from box2
(SSL error / timeout on the xlsx tables), so the 5-year age-group female tables could not be used; the
OWID female mean-years series (1990+) is the substitute, which limits the female long-lag cells. This is
recorded as a deviation in the README.

No interpolation was used for estimation: every regression row is an observed country-year. Income is logged.
