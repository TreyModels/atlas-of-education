# EXTERNAL LITERATURE REVIEW — what the literature already says, so the programme does not redo it

**Built:** 2026-11-20 (Asia/Shanghai). **Requested by:** Dr. Trey Menefee (via the dashboard): *"what does the
literature already say — maybe we don't have to redo it."* **Status: DESCRIPTIVE BIBLIOGRAPHIC REVIEW. Not
evidence about the Philippines; no causal claims; no policy claims.**

**Companions:** `EXTERNAL_LITERATURE_ROWS.csv` (every checkable claim, one row, with URL and verification tag),
`EXTERNAL_LITERATURE_CITE_INDEX.csv` (one row per unique source), the three workstream evidence files
(`rows_A_schooling_complexity.csv`, `rows_B_absorption_credential.csv`, `rows_C_projections.csv`,
`rows_C_REPO_AUDIT.md`), and `build_rows.py` (deterministic assembler).

---

## 1. How this was verified — read this before trusting any row

- **Every claim carries a URL and a verification tag.** `VERIFIED-FULLTEXT` = the paper/PDF was fetched in this
  session and its text read; `VERIFIED-ABSTRACT` = the abstract/metadata page was fetched and read; `UNVERIFIED` =
  named but not fetched this session (included only where the work is canonical and its status is flagged).
- **No citation, author, year, venue or number was written from memory.** Where a source could not be opened, the row
  says `UNVERIFIED` and the memo does not rely on it for a magnitude.
- `web_fetch` was blocked in this environment (its DNS maps public hosts into the 198.18.0.0/15 benchmarking range),
  so retrieval was done with `curl` (browser UA, redirects, 45 s timeout) and HTTP status / byte count / sha256 prefix
  were logged by the workstreams (`rows_C_REPO_AUDIT.md` §5 is the model). This does not change the verification
  standard: a row is VERIFIED only if the artefact was downloaded and read.
- **Where a canonical claim is contested, the row says so.** "Established" in this memo means *the field treats it as
  a benchmark or canonical frame*, not that it is true in this panel or for the Philippines.

**Scale and integrity of this pass (so the reader can calibrate it).** The assembled table has **76 claim rows from
63 unique sources**: **38 VERIFIED-FULLTEXT**, 10 `VERIFIED` (projection-model artefacts), **14 VERIFIED-ABSTRACT**,
4 VERIFIED-METADATA, and **10 UNVERIFIED** (flagged, never used for a magnitude). Caveats that must travel with it:

1. **Abstract-only rows were read from OpenAlex/Crossref records, not publisher pages** where the publisher blocked
   access (e.g. Hanushek & Woessmann 2021, Barro 1991, Sala-i-Martin 1997). They are tagged VERIFIED-ABSTRACT and must
   not be quoted as if full text was read.
2. **A critique the brief expected was not located and was NOT invented.** No "Glawe & Wagner" ECI critique exists in
   the indexes searched (their work is on the middle-income trap, 2016/2019); the ECI critique record here is
   Mealy–Farmer–Teytelboym (spectral clustering), Sciarra et al. (contrasting rankings), Albeaik et al. (metric
   choice) and Hausmann–Hidalgo (EXPY vs ECI measurement). If a specific Glawe–Wagner citation is required, it has to
   be supplied before use.
3. **Numbers that sat in unread appendices are not asserted.** Where a magnitude was not visible in the read text
   (e.g. Hidalgo–Hausmann 2009 supplementary regression tables), the row says "no magnitude seen".
4. **Pritchett (2013) *The Rebirth of Education*** is UNVERIFIED (CGD page returned 403); the Andhra Pradesh
   "one in twenty" figure is a single-state illustration, not a cross-country estimate.

## 2. What the programme's own literature layer already holds (and does not)

Full audit in `rows_C_REPO_AUDIT.md`. The short version:

- The repo's literature layer is **four rings**: the 20-source core ledger (shadow-education corpus), ~19 manuscript
  references (mostly "cited, unverified"), audited economics files (`02_lit/`), and the massification theory layer
  (`10_massification/lit/*.md`, ~110 KB, labelled `STANDARD-CITATION` / `NOT-FOUND`).
- **`LITERATURE_LEDGER.md` contains no growth, complexity, ECI, Hanushek, Schofer, Barro, Lutz or IIASA entry** — the
  whole-word counts are zero. It is a shadow-education/credential-competition corpus, excellent for the closed phase,
  not a ledger for a massification model.
- **Correction to an earlier internal statement:** `longitudinal_2026-11-20/lit/EXPECTATIONS.csv` is **not** a
  zero-standard-citation file. It has **19 data rows; 9 name a real work** (Hanushek–Woessmann, Psacharopoulos–Patrinos,
  Clark–Nielsen, Hidalgo–Hausmann, Schofer–Meyer, Becker/Mincer, Thurow/Collins), 10 name none; labels split 7
  UNVERIFIED / 4 BLOCKED / 8 PROGRAMME-PRIOR. The accurate statement is: **every row is unsupported by a reference the
  repo actually holds** — the file's own `source_file` column says "0 hits" over and over.
- **Only 10 of the 43 relationships in `equations/EQUATION_REGISTER.csv` are equations the literature states**; 13 are
  narrative-only and 20 exist only because the programme wrote them down (15 invented, 5 estimated). The literature
  layer supplies mechanism and falsifiers, **not functional forms**. That ratio (~23% literature) is the single most
  important number in the audit, and it is why strands (c) and (e) below matter so much.

---

## 3. Strand (a) — years of schooling vs cognitive skills/literacy and growth

**Verdict: settled in its main outlines — and the settlement is the opposite of "more schooling = more growth".**
The field's central claim is that **cognitive skills**, not years of attainment, are what relate to growth; the
counter-claim (better data restore a schooling coefficient) is real but does not rescue years-of-schooling as a
*skill* proxy. The programme's literacy-vs-years horse race is therefore a **restatement of a known finding class**,
not a discovery — and the programme currently has no learning-outcome data, which is exactly the literature's
measuring instrument.

| claim | source | status |
|---|---|---|
| Cognitive skills, not years of school attainment, are what relate to earnings, income distribution and growth | Hanushek & Woessmann (2008), *J. Economic Literature* 46(3):607–668, `doi:10.1257/jel.46.3.607` | VERIFIED-ABSTRACT |
| **One SD** of student test performance ≈ **1.2–2.0 pp/yr** faster GDP-per-capita growth; with a direct skill measure, years of attainment is **never** statistically significant; explanatory power rises from ~¼ to ~¾ of growth variance | Hanushek & Woessmann (2012), *J. Economic Growth* 17(2):267–321, `doi:10.1007/s10887-012-9081-x` | VERIFIED-FULLTEXT |
| Causal identification rests on instrumenting test scores with school-system institutions; the IV is close to OLS **but the first-stage F-statistic is relatively low** (the authors say so) | Hanushek & Woessmann (2012), same paper | VERIFIED-FULLTEXT |
| **Three-quarters of the cross-country variation in 1960–2000 growth** of GDP per capita can be accounted for by international math/science test scores | Hanushek & Woessmann (2021), *Oxford Research Encyclopedia of Economics and Finance*, `doi:10.1093/acrefore/9780190625979.013.651` | VERIFIED-ABSTRACT |
| Cross-national data show **no association** between the growth of educational capital and output-per-worker growth; growth-accounting implies a coefficient of **0.21–0.42 (≈0.3)**, so the observed zero is a shortfall, with three candidate explanations (governance, falling marginal returns, quality so low that years created no human capital) | Pritchett (2001), *World Bank Economic Review* 15(3):367–391, `doi:10.1093/wber/15.3.367` | VERIFIED-FULLTEXT |
| The macro-micro divergence is reconciled by **initial stock vs change**: Mincer private returns are strong, but the evidence that the *stock* of education raises a country's growth is "tenuous"; initial stock matters, secondary/tertiary more than primary, female education insignificant/sometimes negative | Krueger & Lindahl (2001), *J. Economic Literature* 39(4):1101–1136, `doi:10.1257/jel.39.4.1101` | VERIFIED-FULLTEXT |
| In a 98-country 1960–85 cross-section, growth is positively related to **initial** human capital (1960 enrolment rates) | Barro (1991), *QJE* 106(2):407–443, `doi:10.2307/2937943` | VERIFIED-ABSTRACT |
| **+1 year of male secondary-or-higher attainment raises growth on impact by 0.44 pp** (implied asymptotic output gain ~19%) | Barro (2013), *Annals of Economics and Finance* 14-2, `http://aeconf.com/Articles/Nov2013/aef140201.pdf` | VERIFIED-FULLTEXT |
| Extreme-bounds testing exaggerates fragility; analysing the full distribution shows many variables robustly related to growth | Sala-i-Martin (1997), *AER* 87(2):178–183, `doi:10.1257/aer.87.2.178` | VERIFIED-ABSTRACT |
| **Better schooling data reverse the earlier null**: with improved attainment series, schooling coefficients are significant in cross-country *and* panel growth regressions | Cohen & Soto (2007), *J. Economic Growth* 12(1):51–76, `doi:10.1007/s10887-007-9011-5` | VERIFIED-ABSTRACT |
| Book-length statement that schooling expansion has outrun learning ("schooling is not the same as learning"; rural Andhra Pradesh: ~1 in 20 fifth-graders can do basic arithmetic) | Pritchett (2013), *The Rebirth of Education*, CGD | UNVERIFIED (monograph; not fetched) |

**Established:** (i) measured cognitive skills dominate years of attainment in cross-country growth work; (ii) years of
schooling is a **misleading proxy** for skills (educational quality/learning varies enormously); (iii) the
micro-Mincer vs macro-growth divergence is real and is explained largely by initial stock, level composition and
measurement, not by a genuine "returns are zero" result.

**Contested:** (i) the *causal* magnitude of the skills effect (the 1.2–2.0 pp number depends on a weak first-stage IV
and on cross-country identification assumptions); (ii) whether better data restore a schooling coefficient (Cohen–Soto
say yes for attainment; Hanushek–Woessmann say that is precisely the wrong regressor); (iii) whether Pritchett's null
is a measurement artefact.

**What a careful programme cannot assume:** it cannot use years of schooling — or adult literacy — as a *skill*
measure and then interpret coefficients as "education's effect"; it cannot quote the 1.2–2.0 pp magnitude as causal;
it cannot claim novelty for showing that years-of-schooling does not move with growth (Pritchett 2001, Krueger–Lindahl
2001 already report that class of result); and it cannot assess "learning" at all without the data the literature
uses (PISA/TIMSS-type learning measures), which the repo does not hold.

**Implication for this programme:** the H1 horse race (literacy moves, schooling-years does not) is *consistent* with
this literature but is **not evidence for it**: the literature's point is that *neither* series is a skill measure.
A genuine test of the user's 2015 hunch would require a learning series — which is a data ask, currently HELD.
Do not re-derive "schooling ain't learning"; cite it, and state that the programme lacks the instruments.

## 4. Strand (b) — economic complexity/ECI and growth, and education → complexity

**Verdict: ECI is a well-defined, heavily used index with a contested construct and a contested growth-prediction
record; the direct *education → complexity* evidence is thin, and the field's own authors say years-of-schooling is an
inadequate capabilities proxy.**

### 4a. What ECI is, and what it predicts

| claim | source | status |
|---|---|---|
| Economic complexity (diversification/ubiquity eigenvector, ECI) is correlated with income per capita, and **deviations of income from that relation predict future growth** | Hidalgo & Hausmann (2009), *PNAS* 106(26):10570–10575, `doi:10.1073/pnas.0900943106` | VERIFIED-FULLTEXT |
| ECI is robust to country dummies and **outperforms alternative structure measures** (Hirschman–Herfindahl, entropy) in predicting growth | Hidalgo & Hausmann (2009), same paper | VERIFIED-FULLTEXT |
| **Path dependence**: a country's current export structure predicts which new products it can move into (relatedness/product space) — the field's most replicated result | Hidalgo & Hausmann (2009), same paper | VERIFIED-FULLTEXT |
| ECI is a significant **negative** predictor of income inequality and predicts it better than income per capita (R²=0.58 vs 0.36) | Hartmann et al. (2017), *World Development* 93:75–93, `doi:10.1016/j.worlddev.2016.12.020` | VERIFIED-FULLTEXT |
| Trade complexity adds explanatory power to a Solow-convergence baseline (adjusted R² 0.25 → 0.34); multidimensional (trade+technology) complexity adds ~7 more points | Stojkoski, Koch & Hidalgo (2023), *Communications Earth & Environment* 4:130, `doi:10.1038/s43247-023-00770-0` | VERIFIED-FULLTEXT |
| Review-level synthesis: complexity metrics explain and predict income, growth, inequality and emissions; relatedness anticipates specialisation changes | Hidalgo (2021), *Nature Reviews Physics* 3:92–113, `doi:10.1038/s42254-020-00275-1` | VERIFIED-ABSTRACT |
| The Growth Lab institutionalises ECI as an annual ranking and growth-projection instrument | Hausmann, Hidalgo et al. (2014), *The Atlas of Economic Complexity*, MIT Press / `atlas.hks.harvard.edu`, `doi:10.7551/mitpress/9647.001.0001` | VERIFIED-ABSTRACT |

### 4b. What is contested — the replication/critique record

| critique | source | status |
|---|---|---|
| **Construct validity**: the ECI is mathematically equivalent to a **spectral clustering** algorithm on a country-similarity graph — not a direct measure of latent capabilities | Mealy, Farmer & Teytelboym (2018), INET Oxford WP 2018-04, `https://oms-inet.files.svdcdn.com/production/files/main_feb4.pdf` | VERIFIED-FULLTEXT |
| **Metric disagreement**: commonly used complexity methodologies produce **contrasting country rankings**, undermining acceptance/application | Sciarra, Chiarotti, Ridolfi & Laio (2020), *Nature Communications* 11:3352, `doi:10.1038/s41467-020-16992-1` | VERIFIED-FULLTEXT |
| **Which metric?** A simpler alternative (ECI+) predicts growth better than ECI and Fitness (one SD ECI+ ≈ **4–5% faster annualised growth**), though it is a preprint; ECI+ and ECI correlate R²≈85% but rank countries differently | Albeaik, Kaltenberg, Alsaleh & Hidalgo (2017), arXiv:1707.05826, `doi:10.48550/arXiv.1707.05826` | VERIFIED-FULLTEXT |
| Measurement caveat from inside the field: EXPY-style sophistication uses GDP-per-capita weights whereas ECI uses only country–product links — so results depend on the network, not on GDP | Hausmann & Hidalgo (2011), *J. Economic Growth* 16(4):309–342, `doi:10.1007/s10887-011-9071-4` | VERIFIED-FULLTEXT |
| Alternative operationalisation: classify 779 products by sophistication/connectivity instead of ECI → 352 "good"/427 "bad" products, 28 countries in a "middle-product trap" | Felipe, Kumar & Abdon (2010), Levy Economics Institute WP 644, `doi:10.2139/ssrn.1730743` | VERIFIED-FULLTEXT |

**The programme's own replication record is part of this contested picture, not a contradiction of it:** in the
30-country panel, ECI does not predict positive growth (10-year growth ~ ECI: coefficient **−0.158** without controls,
**−0.068** with the canonical year-FE cross-section; the Growth Lab's own `growth_proj` does not predict realised
growth, **−0.004**) — `09_relations/LITERACY_ECI_DEMOGRAPHY.md` and `longitudinal_2026-11-20`. The critique
literature (metric disagreement, spectral-clustering interpretation) already explains why ECI→growth is fragile. **The
programme does not need to re-run the ECI→growth debate; it needs to stop treating ECI→growth as the question.**

### 4c. Education → complexity (the user's current hypothesis) — thin, theoretical, and worth stating carefully

| claim | source | status |
|---|---|---|
| In the capability theory underlying ECI, **specific labour skills are one of the non-tradable capabilities** that make a country productive; income differences are attributed to the diversity of locally available capabilities | Hidalgo & Hausmann (2009), *PNAS*, `doi:10.1073/pnas.0900943106` | VERIFIED-FULLTEXT |
| The same authors explicitly say **aggregate human capital measured as years of schooling is an inadequate proxy** for capabilities, and that development economics erred in hoping otherwise | Hidalgo & Hausmann (2009), *PNAS* | VERIFIED-FULLTEXT |
| Country complexity is **only weakly correlated with years of schooling** in the authors' own data: **R = 0.13** (schooling) and 0.22 (rule of law), 2006 | Hausmann & Hidalgo (2011), *J. Economic Growth* 16(4), `doi:10.1007/s10887-011-9071-4` | VERIFIED-FULLTEXT |
| Growth cannot be explained as accumulation of aggregate physical/human capital; "something else" (capabilities/complexity) is needed | Hausmann & Hidalgo (2011), same paper | VERIFIED-FULLTEXT |
| Complexity adds predictive power **beyond** log human capital (years of education) in cross-country growth regressions | Stojkoski, Koch & Hidalgo (2023), *Comms Earth & Env* 4:130 | VERIFIED-FULLTEXT |
| A **direct empirical literature on complexity × human capital exists** (at least three studies: Zhu & Li; Lee & Vu; Ben Saâd & Assoumou-Ella), identified from Hidalgo's (2021) reference list — **not fetched in this review** | Hidalgo (2021) reference list | UNVERIFIED (titles only; do not cite findings) |

**Reading of the evidence.** The user's hypothesis — *more education → more economic complexity* — is a **capability-theory
claim**, not an established empirical result. The verified literature says: skills are *one* of many non-tradable
capabilities (theory); complexity is **weakly correlated** with schooling-years (R = 0.13, the field's own number);
and aggregate schooling is a poor capabilities proxy. The direct tests exist but were not retrieved; they are the
next targeted literature pass, not something this memo can certify.

**Implication for the programme:** this is *consistent with* the predeclared education→ECI matrix result — a small,
fragile association carried by the **completion flow** (primary completion, PARTIAL at 5 and 10 years) with **no**
upper-level or low-base pattern — and it is *inconsistent with* a strong reading of "education builds complexity".
The synthetic world should therefore encode education→`X` as a **declared assumption to be tested** (Amendment A1),
not as a literature-established fact.

## 5. Strand (c) — absorptive capacity, thresholds, dual economy, structural transformation

**Verdict: the canonical frame exists and is old; the specific "education only pays above a development/complexity
threshold" claim exists in several formalisations but has a contested replication record. The Philippines-style
composition argument has a strong structural-change literature and a weaker causal one.**

What is **established** as framing (and therefore needs no re-invention):

| claim | source | status |
|---|---|---|
| Dual economy: a modern sector draws labour from a subsistence sector at a constant wage; the transfer of labour **is** the growth mechanism | Lewis (1954), *The Manchester School* 22(2):139–191, `doi:10.1111/j.1467-9957.1954.tb00021.x` | VERIFIED-FULLTEXT |
| Surplus-labour models with open unemployment: migration responds to the **expected** urban wage (wage × job-finding probability), so urban unemployment is an equilibrium phenomenon | Harris & Todaro (1970), *AER* 60(1):126–142 | VERIFIED-FULLTEXT |
| Convergence is conditional on **social capability / absorptive capacity** — laggards catch up only if they can absorb the leader's technology | Abramovitz (1986), *J. Econ. History* 46(2):385–406, `doi:10.1017/S0022050700046209` | VERIFIED-ABSTRACT |
| Structural change = reallocation of labour across sectors with different productivity levels; it is the central object of development economics | Timmer, de Vries & de Vries (2015), *Routledge Handbook of Industry and Development*, ch. 4, `doi:10.4324/9780203387061-4` | VERIFIED-ABSTRACT |
| Structural change can be **growth-reducing**: 1990–2005 labour flowed the "wrong" way in Africa and Latin America, growth-enhancing in Asia; the pattern of structural change accounts for the bulk of the Asia-vs-rest productivity difference | McMillan & Rodrik (2011), NBER WP 17143, `doi:10.3386/w17143` | VERIFIED-FULLTEXT |
| **Premature deindustrialisation**: the manufacturing-employment hump has shifted down and toward the origin; countries exhaust industrialisation at much lower incomes; Asia/manufactures exporters largely insulated | Rodrik (2015), NBER WP 20935, `doi:10.3386/w20935` | VERIFIED-FULLTEXT |
| Technology choice is **skill-biased**: rich/skill-abundant economies use skilled labour more efficiently and choose technologies suited to their endowment, so identical schooling has different productivity value by development level | Caselli & Coleman (2006), *AER* 96(3):499–522, `doi:10.1257/aer.96.3.499` | VERIFIED-FULLTEXT |
| Technology–skill complementarity is historically contingent, not universal (it emerged in US manufacturing 1909–29) — the "race between education and technology" | Goldin & Katz (1998), *QJE* 113(3):693–732, `doi:10.1162/003355398555720` | VERIFIED-FULLTEXT |
| Task framework: computerisation substitutes for **routine** tasks and complements **non-routine** analytic/interactive tasks — the microfoundation of mismatch | Autor, Levy & Murnane (2003), *QJE* 118(4):1279–1333, `doi:10.1162/003355303322552801` | VERIFIED-FULLTEXT |
| Middle-income slowdown: growth downshifts by **at least 2 pp** when per-capita income reaches ~**$17,000** (2005 constant international prices) | Eichengreen, Park & Shin (2012), *Asian Economic Papers* 11(1):42–87, `doi:10.1162/asep_a_00118` | VERIFIED-FULLTEXT |
| Global private return to a year of schooling averages **~9%** (1,120 estimates, 139 countries, 1950–2014) — the standard benchmark against which any "returns have collapsed" claim must be stated | Psacharopoulos & Patrinos (2018), *Education Economics* 26(5):445–458 (WB PRWP 8402), `doi:10.1080/09645292.2018.1484426` | VERIFIED-ABSTRACT |

**Named but not verified this session** (canonical; treat as citations, not as evidence): Nelson & Phelps (1966) on
education and technology diffusion; Vandenbussche, Aghion & Meghir (2006) on tertiary human capital and distance to the
frontier; Benhabib & Spiegel (1994) on human capital through TFP. **The threshold claim the user's model rests on**
("schooling pays only above some development/complexity level") is exactly the Vandenbussche–Aghion–Meghir /
Abramovitz family, and its replication record is **mixed** — the audit records it as "widely cited, sensitive to how
distance to frontier is measured". So the programme's "kickstarted" hypothesis is **not novel**, is a known contested
claim, and cannot be treated as a design premise without its own test (which the programme has now run and found
**not supported**: ECI-tercile slopes do not differ, `longitudinal_2026-11-20` H3).

**Contested / not settled** (do not cite as settled): the payoff of structural change (measurement of informality and
deflators); the "trap" reading of the middle-income slowdown (regression to the mean and case selection can generate
the same pattern); whether the skill-bias mechanism generalises to late industrialisers and service economies.

**What this means for the programme:** the dual-economy/structural frame is the **right frame** for the user's
"absorption" point, and it is already well developed — there is no need to invent a new structural story. What the
literature does **not** supply is (i) a functional form for "education → absorptive capacity" at the country level,
and (ii) any estimate of the threshold for a country like the Philippines. Those remain open.

## 6. Strand (d) — education expansion, educated unemployment, credential/queue, job matching

**Verdict: the theory is fully established and the Philippines-specific empirics exist. What the programme must not
redo: the theory. What it must not ignore: the measured PHL evidence, which already says the graduate market has
turned.**

Theory (established; cite, do not re-derive):

| claim | source | status |
|---|---|---|
| Overeducation: after ~1969 the payoff to a bachelor's fell sharply as graduate supply outran demand | Freeman (1976), *The Overeducated American* | UNVERIFIED (monograph; not fetched) |
| Credential inflation: schooling expands mainly to allocate access to elite occupations/status groups; credential requirements ratchet upward as supply grows | Collins (1979), *The Credential Society* | UNVERIFIED (monograph) |
| Filter: schooling may certify pre-existing ability rather than create it; social return can fall below private | Arrow (1973), *J. Public Economics* 2(3):193–216, `doi:10.1016/0047-2727(73)90013-3` | UNVERIFIED (metadata) |
| Signalling: education can carry information about unobserved ability; equilibria exist where schooling raises wages without raising productivity | Spence (1973), *QJE* 87(3):355–374, `doi:10.2307/1882010` | VERIFIED-ABSTRACT |
| Job competition: workers compete for **jobs**, wages attach to jobs, education orders the queue — the sharpest credential-inflation statement | Thurow (1975), *Generating Inequality* | UNVERIFIED (monograph) |
| Overeducation measurement (job analysis / self-assessment / realised matches); returns to **surplus** schooling are far below returns to **required** schooling (~**45%** of the required-schooling return) — rejecting both pure human capital (equal returns) and pure job competition (zero) | Leuven & Oosterbeek (2011), *Handbook of the Economics of Education* vol. 4, ch. 3 (IZA DP 5523), `doi:10.1016/b978-0-444-53444-6.00003-1` | VERIFIED-FULLTEXT |
| Survey/method warning: incidence estimates vary widely with measurement, so cross-country "share overeducated" figures are **not comparable** | McGuinness (2006), *J. Economic Surveys* 20(3):387–418, `doi:10.1111/j.0950-0804.2006.00284.x` | VERIFIED-ABSTRACT |

Philippines-specific measured evidence (the part that matters most, and the part the programme has not been using):

| claim | source | status |
|---|---|---|
| **Vertical mismatch**: about **1 in 5** tertiary-educated workers holds a job that mainly requires basic skills; horizontal mismatch reported as the norm; professional licences pay a premium **only when education and occupation credentials align**; experience and structural mismatch matter more for pay than school characteristics | Bayudan-Dacuycuy, Vargas & Luzon (2025), *Mismatch and the graduate labour market in the Philippines*, PIDS Discussion Paper Series No. 2025-32, `https://pidswebs.pids.gov.ph/CDN/document/pidsdps2532.pdf` | VERIFIED-FULLTEXT |
| **The graduate market has turned**: the college wage premium has fallen and real graduate wages were flat while wages below secondary rose **nearly 50%**; college graduates in their twenties face the **highest unemployment** of any group; **more than a third (39%)** of workers have more education than their jobs require and receive modest returns on the extra schooling | World Bank (2026), *Building the Filipino Middle Class* (Philippines poverty and equity assessment, 115 pp), `https://openknowledge.worldbank.org/server/api/core/bitstreams/1e48613c-2045-441…` | VERIFIED-FULLTEXT |
| Youth labour market: ~**7.1 million** youth employed; **21%** of working youth in moderate/extreme poverty; gender gap in participation **16.8 pp** | ILO (2020), Country Office for the Philippines fact sheet, ILOSTAT modelled estimates | VERIFIED-FULLTEXT |
| **BPO/IT-BPM capacity**: ~**1.9 million** jobs and **US$40 bn** export revenue, **>8% of GDP**, adding ~**80,000** jobs in 2025 at **4%** employment growth — i.e. absorption capacity exists but the sector's job growth is *below* graduate-flow growth and exposed to AI/US demand | IBPAP, reported by *Daily Tribune* 1 Jan 2026, `https://tribune.net.ph/…` | VERIFIED-FULLTEXT |

**What the literature already established that the programme should not re-derive:** the *mechanism* of credential
inflation and queueing (three canonical models: human capital, signalling/filter, job competition); that pure job
competition is rejected and surplus schooling earns roughly 45% of required-schooling returns; and — crucially —
that the *Philippines-specific* graduate market has already been measured, with the direction (falling premium, high
graduate-youth unemployment, large mismatch, a BPO sector whose job growth is now slower than graduate flow) exactly
matching the user's composition/absorptive hypothesis. **The programme's "queue" story is therefore theory-supported
and PHL-measured; what it lacks is a *dynamic* estimate — what happens to the marginal graduate when the office rung
fills — and no published source supplies that for the Philippines.**

**Caution list — claims the programme must NOT make (from the strand-d workstream's own notes):**
1. **Do not treat PHL graduate unemployment as proof of excess supply.** The World Bank itself says it "partially
   reflects higher reservation wages and a longer search period" *as well as* skills mismatch — the standard data
   cannot separate the two. The queue story is therefore consistent with the data, not demonstrated by it.
2. **Do not quote "seven in ten graduates not employable in their chosen occupation" as Philippine evidence.** PIDS
   cites it to *Aspiring Minds (2017)*, an India-based assessment. The verifiable PHL numbers are the World Bank's
   39% overeducation / flat graduate wages / highest graduate-youth unemployment, and PIDS's 1-in-5 vertical mismatch.
3. **Compute, do not assume, the absorber ratio.** IBPAP's ~80,000 net jobs per year is an order of magnitude below
   the annual tertiary graduate flow; the programme should compute that ratio from its own data, not assert it.
4. **Do not cite Freeman, Collins, Arrow or Thurow for magnitudes** — those rows are `UNVERIFIED` placeholders; the
   verifiable equivalents are World Bank (2026), PIDS (2025) and Leuven & Oosterbeek (2011).
5. **Do not compare overeducation rates across countries without fixing the measurement method** (McGuinness 2006).

**Contested / open:** the magnitude of the signal vs skill component of returns; whether overeducation is persistent
or transitional; comparability of overeducation incidence across countries.

## 7. Strand (e) — existing structural / synthetic / cohort-component education projection models

**Verdict: this literature is fully developed, openly licensed, and the programme has (audit finding) reinvented its
demography without citing it. Do not build a cohort-component education projection from scratch.**

| model | what it is | method | reusability | source | status |
|---|---|---|---|---|---|
| **Wittgenstein Centre (WIC) / IIASA multi-state model** | 120-country multi-state cohort-component with education as an explicit state; education-specific fertility/mortality/migration; 195 countries to 2100 | multi-state cohort-component | **citable and adoptable** — the canonical method | Lutz/KC et al., *Demographic Research* 22(15): `https://www.demographic-research.org/volumes/vol22/15/22-15.pdf`; method report IIASA IR-13-018: `https://pure.iiasa.ac.at/id/eprint/10742/1/IR-13-018.pdf` | VERIFIED |
| **WIC 2023 dataset (WCDE 3.0)** | population & human-capital projections by age/sex/education, SSP-consistent; **CC BY 4.0** | multi-state, 2020 base | **directly reusable**: download, use as external benchmark (mean years of schooling) — the single most actionable item in this review | `https://zenodo.org/records/7767425`; explorer `https://dataexplorer.wittgensteincentre.org/wcde-v3/` | VERIFIED |
| WIC 2018 (CEPAM/JRC) | 201 countries, SSP scenarios, labour-force module for EU | multi-state + SSP | citable | `http://epub.wu.ac.at/6458/1/jrc_cepam_report_demographic_and_hc_scenarios_pdf.pdf`; `doi:10.2760/835878` | VERIFIED-METADATA |
| **Barro–Lee attainment dataset** | educational attainment 1950–2010 (+2021 update), 5-year age groups, 15+/25+ | **reconstruction/extrapolation, not projection** | use for **base-year cross-checks**, not as a projection | `http://barrolee.com/?p=57`; `https://barrolee.com/` | VERIFIED |
| **EPSSim 2.1 (UNESCO/UNDP)** | ministry-level cohort-flow + cost/finance simulation; output = financing gap | demographic flow + cost model | free, full user guide; **the right precedent for the cost/flow layer** | `https://www.undp.org/sites/g/files/zskgke326/files/publications/User%20Guide%20Education%20Policies%20and%20Strategies.pdf` | VERIFIED |
| UNESCO generic education planning simulation model | generic cohort/flow + cost simulation for countries to adapt | cohort/flow + scenarios | citable precedent | `http://specialcollections.nust.na:8080/greenstone3/library/sites/localsite/collect/unesco/index/assoc/HASH0197/b1c274bb.dir/Education_planning_through_computer_simulation.pdf` | VERIFIED |
| World Bank *Tools for Education Policy Analysis* | embedded education-sector simulation model | sector toolkit | citable | `https://openknowledge.worldbank.org/entities/publication/17a669b5-2128-58fe-88a8-9d7cea10e7ff` | VERIFIED-METADATA |
| **MOSART (Statistics Norway)** | dynamic **microsimulation** of individual schooling choices → attainment and labour supply | individual life-course microsim | methodological precedent; needs population registers (exactly what a synthetic workbench fabricates) | `https://www.ssb.no/en/utdanning/artikler-og-publikasjoner/_attachment/106069` | VERIFIED |
| Agent-based schooling transitions | district-level outcomes from household school choice (Chicago) | ABM | precedent for the household-choice layer | `https://www.jasss.org/17/2/3/3.pdf` | VERIFIED |
| UIS teacher-demand projections | global teacher-need projections from a cohort-flow model | flow/PTR model | would have been the UN's own projection product; the PDF was **404** | `https://uis.unesco.org/…` | UNVERIFIED |

**The actionable conclusion:** adopt the **WIC multi-state cohort-component structure** (published method, CC BY 4.0
data) for the demographic layer and **benchmark** the synthetic workbench's schooling outputs against WCDE mean years
of schooling; cite EPSSim for the cost/flow layer and MOSART as the microsimulation precedent. The programme's genuine
novelty is **not** the demographic engine — it is the gate/queue/absorptive mechanism (strands c–d) and the
education→complexity channel (strand b).

---

## 8. What we do NOT need to redo (the deliverable)

1. **The demographic engine.** Multi-state cohort-component education projection is a 20-year-old published method
   with open data (WIC 2023, CC BY 4.0). Reuse/benchmark; do not rebuild. The programme's `DEM-01/02` are a
   reinvention — keep them only as a declared synthetic device and say so.
2. **The structural/dual-economy frame.** Lewis, Harris–Todaro, Abramovitz, Timmer/McMillan–Rodrik/Rodrik already
   supply the absorptive-capacity and structural-change frame. The "composition > totals" idea is a restatement of
   structural change, not a new mechanism.
3. **The credential/queue theory.** Human capital vs signalling/filter vs job competition is settled theory; the
   empirical benchmark is that surplus schooling earns ~45% of required-schooling returns. Cite; do not re-derive.
4. **The global returns benchmark.** ~9% average private return per year of schooling (1,120 estimates) is the number
   against which any "returns collapsed" claim must be stated.
5. **The macro-micro puzzle and its resolution.** Krueger–Lindahl (initial stock matters; secondary/tertiary more than
   primary; change in schooling is a weak growth correlate) and Pritchett ("Where has all the education gone?") already
   state the negative/weak aggregate result and its contested measurement basis. The programme's nulls are
   **replications**, not discoveries — and Pritchett's contested status must be stated.
6. **The Philippines-specific graduate-market facts.** Falling college premium, 39% overeducation, highest
   graduate-youth unemployment, 1-in-5 vertical mismatch, BPO ~1.9M jobs / 80k net adds/yr. These are already measured;
   the programme can *use* them rather than generating proxies.
7. **The middle-income slowdown and threshold claims.** They are known, contested, and already tested by the
   programme (H3 not supported). Do not re-litigate them as novel.

## 9. What genuinely remains open (what the programme could own)

1. **A dynamic estimate of the queue**: what happens to the marginal graduate (wage, employment, migration) when the
   office/formal rung fills — no published source estimates this for the Philippines. This is the user's distinctive
   question and it is genuinely open.
2. **Education → complexity**: the capability-theory claim (more education → more complex economy) is largely
   theoretical; direct evidence is thin (see strand b/b2). The programme's predeclared panel now reports a fragile
   primary-completion-flow association only. This is open.
3. **A functional form for absorptive capacity at the country level** — the literature supplies the concept and the
   qualitative conditional-convergence claim, not a usable parametric form.
4. **The measurement-definition work**: completion vs GER denominators, modelled attainment series, ECI as a modelled
   index. The programme's own completion>GER finding is a genuine measurement contribution.
5. **The demographic-overflow mechanism** (cohort surge + lagged capacity + quality collapse) as the *cause* of the
   PHL completion ceiling: the literature has the pieces (EPSSim-style flow models; quality/PTR literatures) but no
   tested account of the Philippine boom-and-ceiling. That is the v1.2 question.

---

## 10. Files

- `EXTERNAL_LITERATURE_ROWS.csv` — every claim (columns: row_id, strand, claim, status_or_model, direction_or_magnitude,
  magnitude_verbatim, source_authors, source_year, source_title, venue, url, doi, verification_status, notes,
  workstream).
- `EXTERNAL_LITERATURE_CITE_INDEX.csv` — unique sources with URLs and best verification status.
- `rows_A_schooling_complexity.csv`, `rows_B_absorption_credential.csv`, `rows_C_projections.csv` — workstream evidence.
- `rows_C_REPO_AUDIT.md` — internal citation inventory, five-strand gap analysis, URL log.
- `build_rows.py` — deterministic assembler (re-running reproduces the CSV from the workstream files).
