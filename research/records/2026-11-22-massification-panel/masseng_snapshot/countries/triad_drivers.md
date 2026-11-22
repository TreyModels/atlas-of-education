# Triad drivers data note (PHL, KHM, HKG)
Data: triad_drivers.json. Read status: P = page fetched directly via WebFetch (all passed through the tool's summariser, so transcription risk exists); S = secondary summary/compiled or garbled source. WDI API fetched Nov 2026 (lastupdated 2026-11-11; MS.MIL PHL 2026-07-13). Last-year 2025 values are ILO/SIPRI projections/nowcasts; drop for training if needed.

## Series, coverage, source
| Country | Series | Years | Status |
|---|---|---|---|
| PHL | agri emp share WDI SL.AGR.EMPL.ZS | 1991-2025 | P |
| PHL | agri (primary) emp share national, Chiba Hi-Stat DP304 | 1956-1989 (no 1979) | S, garbled table |
| PHL | wage/salaried WDI | 1991-2025 | P |
| PHL | educ exp % GDP WDI | 1980,82,83,86,95-98,2000-09,2014-25 | P |
| PHL | educ exp % GNP UNESCO SY1998 | 1980,85,90,95 | P |
| PHL | tax % GDP WDI | 1990-2024 | P |
| PHL | milex % GDP SIPRI | 1960-2024 (no 1975) | P |
| KHM | agri emp WDI; wage/salaried WDI | 1991-2025 | P (ILO model) |
| KHM | educ exp % GDP | 1998,2000-02,04,07,09-14,18-23 | P |
| KHM | tax % GDP | 2002-2023 | P |
| KHM | milex % GDP | 1986-2025 | P |
| KHM | agri census/CSES | 2013 only (64.2) | S |
| HKG | agri emp WDI | 1991-2025 | P |
| HKG | agri emp census | 1961 (7.3), 1971 (4.0) | P |
| HKG | manufacturing emp share | 1961,71,81,86,91,96,2001 | mixed (1986 S) |
| HKG | services emp share | 1971,81,86,95 (+derived 91/96/01) | S |
| HKG | wage/salaried WDI | 1991-2025 | P |
| HKG | educ exp % GDP WDI | 1971-78,80-85,90,92,96,2001-24 | P |
| HKG | FYFD participation (17-20) | ~1989 7%, 1989-90 <9%, 1994-95 18%, 2001 18% | S |
| HKG | total publicly funded post-sec | 2001 ~30%; 60% target by 2010/11 | P |

## Splices needed
- PHL agriculture: Chiba 1989 (45.1) -> WDI 1991 (44.08) looks continuous; Chiba has a break at 1964/65 (not-adequately-defined reclassified) and a 1960 outlier (69.1); series is noisy (survey-round changes). PHL LFS annual 1990 missing.
- HKG: WDI agri 1991+ is tiny; use mfg/services census shares, not agriculture, as the discriminating variable. Mfg 1986->1991 uses different sources.
- PHL educ: WDI 1980 (1.51 GDP) vs UNESCO 1980 (1.7 GNP) differ in base; do not mix.

## Notes
- HK has no national military; no MS.MIL series (PLA garrison is Beijing-funded). HK tax revenue not requested/fetched.
- Premises not confirmed: HK "~2% early 1970s" degree participation (no source found); free compulsory 9-year "1978" (1974 White Paper targets 1979 subsidised 9 yrs; free primary 1971 confirmed).

## Gaps
- KHM pre-1991 anything (employment, education spend, tax; 1998/2008 census total agri share not found). KHM tertiary/secondary 1980s-90s: only 1990 upper-sec enrolment (47,562) and 1998-99 GERs (primary 89.7, lower sec 23.0, upper sec 8.7), no tertiary.
- KHM/HKG education spend pre-WDI (UNESCO yearbook tables lacked them); PHL 1970s edu spend.
- HK annual manufacturing/services 1972-1990 and 1992-2024 (GHS/LFS) not retrieved; HK 1970s-80s degree participation annual series; HK sub-degree series 1995-2003.
- PHL wage/salaried pre-1991; HK wage/salaried pre-1991; PHL tax pre-1990; KHM tax pre-2002.
