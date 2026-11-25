# MODEL ZOO — scope and test protocol (design-only; no compute yet)

**Status: SCOPED, NOT YET PREREGISTERED, NOT RUN.** Operator direction 2026-11-25: test *competing education models*
(not only audit equations). Decision outcomes are **holds / fails / indeterminate-by-context**, never "the model is
wrong". Sequencing: Paper C Pilot-0 → grid/G2-B → Paper C confirmatory → Model Zoo (reusing pilot cells).
Codex has been asked to identify "Kaplan" (test-prep/for-profit supply form vs a named academic model vs
Kaplan–Meier attrition) and to propose the canonical model list + test protocol; this document is our draft scope
until that reply lands. **No Model Zoo computation will run before the preregistration is drafted and Codex replies.**

## 1. Candidate models (declared predictions, discriminating moments, data needs)

| # | model | core claim / prediction set | discriminating moment(s) | data need | planned decision rule |
|---|---|---|---|---|---|
| 1 | **Becker human capital** | schooling/tutoring raises skills and earnings; investment responds to returns | learning/mpl/earnings gradient; completion vs spending | PISA/CEPS learning + earnings returns | fails if learning response absent where spending rises |
| 2 | **Mincer returns** | log earnings linear in schooling/experience | returns coefficient stability across contexts | household survey earnings | indeterminate if no earnings data |
| 3 | **Spence signalling/screening** | credentials matter beyond skills; gate pressure raises investment without learning | elite/track share vs L, contest effort vs L, learning flat | gate + learning data | holds if effort rises with L but learning does not |
| 4 | **Hanushek production function** | school inputs → achievement with diminishing returns | q0/S variation → learning; teacher pay/PTR | PISA school inputs | fails if S variation leaves learning flat |
| 5 | **Hirsch positional competition** | demand driven by relative rank / seats, not absolute skill | gap/spend vs gate share; positional-vs-learning decomposition | contest gate data | holds if spend tracks L, not q |
| 6 | **Bray shadow-education demand** | tutoring demand responds to high-stakes exams + household capacity | own_share/spend vs L and income | HK/PH/KH tutoring data | holds if participation rises with L |
| 7 | **Biswal/Jayachandran withholding** | public teachers withhold lessons when pay gap + sellable | withheld, own_share, q_pub under pay_ratio/own_ban | teacher-pay + tutoring data (thin) | holds if h>0 and own_share rises when sellable |
| 8 | **Kaplan-type test-prep supply** | commercial supply form (for-profit prep) scales with exam stakes and ability to pay | firm_price/firm share vs L and income | prep-market data (thin) | TBD after Codex identification |
| 9 | **China state-provision (DL) model** | state supply crowds out private tutoring | firm/own share vs q0/S, private share | China data (CEPS) | holds if S crowds out private demand |
| 10 | **Household time allocation** | student time is the binding constraint; tutoring trades off work/leisure | time-use vs participation (no current data) | time-use survey | indeterminate (data gap) |

## 2. Test protocol (draft)

1. **Declared prediction set** per model (sign/magnitude on named moments), registered before runs.
2. **Common engine runs** (Pilot-0 cells, grid cells, G2-B runs) as the test bed; no bespoke runs unless registered.
3. **Discriminating moments**: a moment is usable only if two models predict different signs/magnitudes for the same
   parameter change (e.g. L↑: positional → spend↑; human capital → spend flat unless learning returns change).
4. **Evidence layering**: engine simulation (mechanism plausibility), DHS/ILSA evidence (empirical pattern), and
   published estimates (baseline) kept separate; no model "wins" on simulation alone.
5. **Decision rule**: holds / fails / indeterminate-by-context, with the context variables (L, S, supply form) named;
   a fail must be a pre-declared falsification test, not a post-hoc story.
6. **Data-need matrix**: every model marked observed / proxy / theory-only before any claim.
7. **Multiplicity**: family-wise reporting of all models × moments; no selective model reporting.
8. **Paper D** (equation audit) is the *methodological companion*: classify standard equations as identity / stylized
   theory / empirical spec / incomplete-for-mechanism, with divergence tests; the Zoo supplies the competing
   predictions that make those divergences testable.

## 3. What exists vs missing (per the engine-core mapping)

* Engine supports: human-capital learning response, positional contest, own-teacher vs firm supply, withholding
  (pay-gap/incentive), gate pressure, school-quality proxy q0.
* Missing (blocks full Zoo testing): positive school-supply lever S (homework/feedback/supervision/teacher effort),
  student/teacher time budgets, own-vs-firm spend split, teacher hours/workload, clean identification data for
  HK/PH/Cambodia/China (see `TUTORING_DATA_INVENTORY.md`), earnings returns data in-scope.
* Therefore **Pilot-0 is hypothesis-generating only**; Zoo tests requiring missing levers must be marked
  indeterminate/data-blocked until the levers/data exist.

<!-- REFS_DOIS_CROSSREF -->
## Reference register (DOI/ISBN) — cross-reference

Every external source cited in this document is listed below with the identifier that exists (DOI, else ISBN/publisher) and the verification status recorded in the programme register. **Register:** [`docs/audit/REFS_DOIS.md`](REFS_DOIS.md). Add a register row before citing a new source; do **not** cite the 183-equation inventory’s placeholder tokens (`UIS+2`, `doi.org+4`, …).

- `biswal_1999` — Biswal, B. P. (1999). Private tutoring and public corruption: A cost-effective education system for developing countries. The Developing Economies 37(2):222–240. **Identifier:** DOI 10.1111/j.1746-1049.1999.tb00232.x. **Status:** PAYWALLED — NOT RETRIEVED (content described in Dang & Rogers 2008).
- `hanushek_1986` — Hanushek, E. A. (1986). The Economics of Schooling: Production and Efficiency in Public Schools. Journal of Economic Literature 24(3):1141–1177. **Identifier:** No DOI. JSTOR stable URL: https://www.jstor.org/stable/2725865. **Status:** BIBLIOGRAPHIC — AMBIGUOUS AS CITED (docs say only “Hanushek” without year/title; this is the standard candidate work).
- `jayachandran_2014` — Jayachandran, S. (2014). Incentives to teach badly: After-school tutoring in developing countries. Journal of Development Economics 108:190–205. **Identifier:** DOI 10.1016/j.jdeveco.2014.02.008. **Status:** VERIFIED PRIMARY TEXT.
- `spence_1973` — Spence, M. (1973). Job Market Signaling. The Quarterly Journal of Economics 87(3):355–374. **Identifier:** DOI 10.2307/1882010. **Status:** VERIFIED BIBLIOGRAPHIC.
- `becker_human_capital` — Becker, G. S. (1964; 3rd ed. 1993). Human Capital: A Theoretical and Empirical Analysis, with Special Reference to Education. New York: Columbia University Press / NBER; 3rd ed. Chicago: University of Chicago Press. **Identifier:** No DOI. 3rd ed. 1993, University of Chicago Press, ISBN 978-0-226-04119-3 (ISBN via OpenLibrary edition record); 1st ed. 1964 Columbia UP/NBER. **Status:** BOOK — BIBLIOGRAPHIC (not read).
- `caplan_2018` — Caplan, B. (2018). The Case against Education: Why the Education System Is a Waste of Time and Money. Princeton, NJ: Princeton University Press. **Identifier:** No DOI. Princeton University Press, 2018; ISBN 978-0-691-17465-5 (OpenLibrary edition record). **Status:** BOOK — CITATION UNVERIFIED (model-zoo tag V).
- `hirsch_1977` — Hirsch, F. (1977). Social Limits to Growth. London: Routledge & Kegan Paul; Cambridge, MA: Harvard University Press. **Identifier:** No DOI. Publishers: Routledge & Kegan Paul / Harvard UP (ISBN not independently verified in this pass). **Status:** BOOK — BIBLIOGRAPHIC (not read).
- `mincer_1974` — Mincer, J. (1974). Schooling, Experience, and Earnings. New York: NBER / Columbia University Press. **Identifier:** No DOI. NBER/Columbia University Press, 1974; ISBN 0-87014-265-8 / 978-0-87014-265-9 (OpenLibrary edition record). **Status:** BOOK — BIBLIOGRAPHIC (not read).
- `ceps` — China Education Panel Survey (CEPS), Renmin University of China. Datasets (Peking University Open Research Data): 10.18170/DVN/B6HK6Y, 10.18170/DVN/KE1JYM, 10.18170/DVN/QOM4FT, 10.18170/DVN/YDQJ3D. **Identifier:** Dataset DOIs 10.18170/DVN/B6HK6Y; 10.18170/DVN/KE1JYM; 10.18170/DVN/QOM4FT; 10.18170/DVN/YDQJ3D (resolve to opendata.pku.edu.cn; metadata pages 403-restricted). **Status:** INSTITUTIONAL DATASET — DOIs resolve; metadata access restricted (403); no analysis in corpus.
- `dhs` — The DHS Program / Demographic and Health Surveys, ICF International. Public-use datasets & API. **Identifier:** No DOI. Provider: https://dhsprogram.com/ (restricted microdata; local copies only). **Status:** INSTITUTIONAL DATASET — no DOI; access documented in programme records.
- `oecd` — OECD — Organisation for Economic Co-operation and Development (PISA programme; see PISA entries for specific DOIs). **Identifier:** Covered by PISA DOIs above; general OECD data: https://data.oecd.org/. **Status:** INSTITUTIONAL DATA SOURCE — no standalone DOI (inventory placeholder “OECD+3” excluded).
- `bray_1999` — Bray, M. (1999). The Shadow Education System: Private Tutoring and its Implications for Planners. Fundamentals of Educational Planning No. 61. Paris: UNESCO IIEP. **Identifier:** No DOI. Publisher: UNESCO IIEP, Paris (ISBN not independently verified in this pass). **Status:** VERIFIED BIBLIOGRAPHIC (peer-reviewed review record).
