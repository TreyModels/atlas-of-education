# PHL: Employer demand and labour-market value of credentials (returns.md)

Compiled 2026-11-22 via WebSearch/WebFetch. Figures were extracted by a fetch summariser from the PDFs/pages, not read directly by me; spot-check against the source before critical use. Values not found are marked NOT FOUND.

## A. Mincer / wage-premium / IRR series

### A1. Gerochi (2002) - best 1988/1990/1995 benchmark
Gerochi, H. (2002) "Returns to education in the Philippines", Philippine Review of Economics 39(2), 37-72. https://pre.econ.upd.edu.ph/index.php/pre/article/download/574/761
Data: NSO LFS October rounds 1988, 1990, 1995; wage/salary workers aged 19-65; 1995 prices.
Method: (a) "elaborate" IRR from age-earnings profiles; (b) Mincer OLS/Heckman on log earnings.

Private IRR, complete cycle, both sexes (%), direct costs from FAPE (Table 11a): elem vs none 13.9/16.9/17.1; secondary vs elem 13.2/12.5/12.8; college vs secondary 11.8/12.8/14.0 (1988/1990/1995).
Same with Maglen-Manasan costs (Table 11b): elem 21.6/27.0/24.0; secondary 15.3/14.3/14.3; college 14.6/15.5/15.8.
Social IRR (11b): elem 13.3/15.1/15.5; secondary 14.9/13.5/13.5; college 14.2/14.6/15.6.
Earnings index (Table 6), elementary graduate = 100 (1988/1990/1995): sec grad 137.40/136.59/134.60; some college 178.55/174.31/177.31; college grad 264.28/270.78/287.50. Implied college/secondary ratio (my arithmetic): 1.92/1.98/2.14; log gap 0.65/0.68/0.76. Implied secondary/elementary log gap 0.32/0.31/0.30.
Mincer schooling coefficient (Table 13, ln earnings, All, as printed in %): OLS both 13.81 (1988), 14.24 (1990), 14.01 (1995); male 12.37/12.65/12.96; female 17.39/18.06/17.41. Per hourly earnings: 12.53/13.17/12.39 (both). Reliability: coefficients seem high versus other studies; table headers garbled in extraction.
Earlier estimates cited by Gerochi: Mincer coefficient 8.0% (1982, Paqueo & Tan), 8.1% (1985), 8.0% (1988, Hossain & Psacharopoulos), 7.3% (1994, Maluccio), 12.6% (1998, male only, Schady). Full-method IRR: 1966 private 9/29/12 (primary/secondary/higher; Williamson & DeVoretz); 1971 ILO private 8/6/8; 1985 Tan & Paqueo private 18.2/13.8/14.0; 1988 Hossain & Psacharopoulos private 18.3/10.5/11.6. (Table 2 rows for 1977/1985 Dumlao-Arcelo, Layac garbled; not used.)
Reliability: high (peer-reviewed, primary computations).

### A2. Schady (2001/2003) - APIS 1998, Filipino men
World Bank PRWP 2566 (2001); Oxford Bull. Econ. Stat. 65(2):171-196 (2003). https://ideas.repec.org/p/wbk/wbrwps/2566.html
Qualitative from abstract: primary and secondary premia significantly smaller than tertiary; sheepskin effects at graduation of each level. Numeric premia NOT FOUND (full text not fetched). Mincer coefficient 12.6% cited via Gerochi.

### A3. Psacharopoulos & Patrinos (2018) WPS 8402
https://openknowledge.worldbank.org/server/api/core/bitstreams/270b9d54-6dcb-571d-b449-9b4143738dd3/content (annex of Returns by level)
Philippines appears once: survey year 2000, private return to a year of schooling 12.6% (basic Mincer), source Kaboski (2003). Level-specific returns not reported. 1994/2004 compilations not fetched: NOT FOUND.

### A4. Montenegro & Patrinos (2014) PRWP 7020
https://openknowledge.worldbank.org/handle/10986/20340 - 139 economies, 819 surveys; findings: tertiary returns highest, returns decline over time. Philippines-specific values NOT FOUND (PDF/dataset not reached).

### A5. Sauler & Tomaliwan (2017), DLSU Research Congress
https://www.dlsu.edu.ph/wp-content/uploads/pdf/conferences/research-congress-proceedings/2017/SEP/SEP-I-005.pdf
Data: LFS October rounds 2008-2012; ln daily wage; Mincer with Heckman.
"Private return per additional year" (% ) Elementary/HS/College: 2008 -3.243/5.705/20.66; 2009 -3.746/6.205/21.17; 2010 -3.506/5.377/22.21; 2011 -3.298/5.307/22.98; 2012 -2.443/7.240/21.80.
Quantile regression coefficients (log daily wage vs "no grade completed"), median: college 0.8853 (2008), 0.8897 (2009), 0.9043 (2010), 0.9613 (2011), 1.012 (2012); high school 0.0939/0.0643/0.0533/0.0679/0.1875; elementary -0.1532/-0.1916/-0.1821/-0.1606/-0.1117.
Reliability: LOW-MEDIUM. Negative elementary returns and ~20%/yr college "per-year" figures look like dummy-coefficient artefacts, and the reference group is "no grade", so "college" is a premium over no schooling, not over HS. Use with caution; direction (rising 2008-2012) only.

### A6. World Bank PRWP 11163 (Belghith, Fernandez, Lavin), "Inequality, Education, and Occupational Change in the Philippines"
https://openknowledge.worldbank.org/server/api/core/bitstreams/e8465aa0-d45d-49bf-9cff-db624f4bc034/content (also https://ideas.repec.org/p/wbk/wbrwps/11163.html)
Data: LFS 2002-2024, wage workers 15+. College-vs-HS premium = ratio/difference of composition-adjusted mean log weekly wages from a regression on education dummies, experience, gender (footnote 7). Log points, not a Mincer coefficient.
Values stated in text: peak 2013 = 0.88 log points; 2024 = 0.59 log points (about 80% higher wages); declined 2002-2007 (no level); some-college vs HS 2024 = 53% higher. Premium higher for women. Figure 5 has no labels, so no annual series extractable from text. Sample definition ambiguity (full-time vs all wage workers).
RIF quantile coefficients (Table 2A, base: HS grad, 20-30 yrs exp, construction, low-skill): College & above Q50: 0.525 (2002-11), 0.478 (2012-16), 0.297 (2017-24); Q10 0.240/0.323/0.365; Q90 0.763/0.877/0.659.
Reliability: high for the endpoints; best single source for 2002-2024 trend.

### A7. Albert, Punongbayan & Muñoz (2024), PIDS Policy Note 2024-09
https://pids.gov.ph/publication/policy-notes/returns-to-education-in-the-philippines-2005-2022-declining-benefits-increased-inequities ; DOI 10.62986/pn2024.09 (PDF behind form; not read). Figures via press: https://dailyguardian.com.ph/?p=365083 and https://mb.com.ph/2024/8/24/pids-study-financial-returns-for-college-graduates-decline
Data: LFS 2005-2022, 621,638 individuals; 185,020 salaried graduates 25-34.
College returns: 141.4% (2010) to 93.7% (2022); -33.7 pp 2005-2022 full sample; -30.8 pp ages 25-34; +46 pp 2001-2010; P10 -64 pp, P90 -18.2 pp. Secondary vs partial college "at par" in 2018.
Definition NOT stated in press coverage (likely percent wage premium relative to the lowest/reference category, not HS). Reliability: medium (secondary reporting; definition/reference group unverified).

### A8. Yee (2023), Int. J. Educ. Dev. 101:102815
https://archium.ateneo.edu/gbseald-edu-lead-faculty-pubs/3
Salaried graduates, 2005 and 2019; returns to higher education fell 36 pp relative to no completed grade; low-wage college graduates -69 pp; high-wage stable. Cited in DLSU 2025 paper https://old.dlsu.edu.ph/wp-content/uploads/pdf/conferences/research-congress-proceedings/2025/SEP-12.pdf (Tomaliwan & Sauler, LFS 2015 & 2019, UQR-Oaxaca-Blinder; no premium series in text).

### A9. Senior high school premium
Abrigo & Orbeta (2023) PIDS PN 2023-15, https://pidswebs.pids.gov.ph/CDN/document/pidspn2315.pdf : SHS attendance wage premium 18.6% over JHS for workers aged 19-22; 10% lifetime premium (23-65); 9.2% annual IRR; cohorts born 1995-98 vs 1999-2002.

## B. Best time-series assembled
Tertiary-vs-secondary (college grad vs HS/secondary grad) log wage gap:
- 1988 0.65, 1990 0.68, 1995 0.76 (derived from Gerochi Table 6 index; wage/salary workers)
- 2013 0.88 (peak), 2024 0.59 (WB PRWP 11163; different method, so levels not strictly comparable to 1988-95)
- 2002-2007 falling, no levels.
Secondary-vs-elementary log gap: 0.32/0.31/0.30 (1988/90/95, derived). Gerochi secondary vs elementary private IRR ~12.5-13.2% (FAPE).
Gap years: 1996-2001, 2003-2012 annual values, 2014-2023 annual values (these exist only in figures).

## C. Educational composition
- WB PRWP 11163: workforce aged 25+ with some college or more about 20% (late 1980s) to about 30% (2024); only 20% completed college by 2024. Share of wage-employment hours with college degree+ 21% (2002) to 27% (2024); less than HS 38% to 26%. Female college share 31% to 40%; male 14% to 19%.
- Full annual PSA LFS employed-by-education table: NOT FOUND (PSA site table not retrievable).

## D. Unemployment by education
- Habito, Inquirer 11 Feb 2025 (citing PSA LFS) https://opinion.inquirer.net/?p=180729 : share of unemployed with any college 36.9% (Jan 2020) vs 44.1% (late 2024); college graduates 26.9% vs 35.6%; latest: SHS 15.6%, JHS 27.5%, elementary 6.3%, tech-voc 6.0%. These are shares of the jobless, not rates. Overall rate 5.3% (Jan 2020), 3.1% (Dec 2024), 3.8% annual 2024.
- WB PRWP 11163: 2024 unemployment of college graduates aged 25-34 = 6.7% vs 4.4% for lower-educated peers.
- PSA press releases carry "Table 3 unemployed by highest grade completed" as attachments (e.g. https://psa.gov.ph/system/files/iesd/Press%20Release%20for%20October%202023%20LFS.pdf); values not extracted.
- Underemployment by education: NOT FOUND. Time series of unemployment rate by education before 2020: NOT FOUND.

## E. Credential requirements
- CSC Memorandum Circular No. 46 s. 1993 (28 Oct 1993), Qualification Standards Manual policies, under EO 292 Book V: first-level assistant posts generally require two years of college or vocational/technical course; confidential second-level staff require a bachelor's degree; first-level trades/crafts require ability to read and write; QS are minimums, agencies may set higher. https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/54639
- Date bachelor's degree first required for second-level career service: NOT FOUND (pre-1993 CSC QS manuals not located). Rising education requirements in job postings: NOT FOUND (no Philippine study found; ADB/LinkedIn digital-skills items surfaced but not read). OFW credential requirements: NOT FOUND.
- Context: advocacy for skills over diploma (https://abs-cbn.com/business/2024/9/10/skills-not-diploma-should-be-basis-for-hiring-advocacy-group-1809), not read.
