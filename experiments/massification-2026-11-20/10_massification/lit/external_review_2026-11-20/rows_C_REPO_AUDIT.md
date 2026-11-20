# rows_C_REPO_AUDIT — internal literature inventory, five-strand gap analysis, and the growth/complexity question

**Built:** 2026-11-20 · **Scope:** read-only audit of the repo's literature layer plus an external check of strand (e).
**Companion file:** `rows_C_projections.csv` (15 external rows, strand e).
**Write scope:** this directory only. No other repo file was modified.

**How the external rows were verified — read this before trusting a status token.**
The `web_fetch` tool refused every request in this session with
`URL hostname ... resolves to a non-public IP address`, because this environment's DNS maps
public hosts into the 198.18.0.0/15 benchmarking range. Network access itself works, so external
pages and PDFs were retrieved with `curl` (browser user-agent, redirect-following, 45 s timeout),
and the HTTP status, byte count and SHA-256 prefix were recorded for each. "VERIFIED" in
`rows_C_projections.csv` therefore means **the artefact was downloaded and its text read in this
session**, not that a particular tool fetched it. Where a publisher blocked the request, the row
says `VERIFIED-METADATA` and names the record that was read. Nothing was summarised from memory.

---

## 1. What the repo already holds — citation inventory

The repo's literature layer is **four concentric rings**, each with a different standard of proof:

| Ring | File(s) | Size | Standard |
|---|---|---|---|
| 1. Core ledger | `LITERATURE_LEDGER.md` §A | 20 sources | full row schema, explicit access status for all 20 |
| 2. Manuscript references | `LITERATURE_LEDGER.md` §B–C | 19 rows + ~27 named-but-unretrieved items | "cited, unverified" is the modal status |
| 3. Audited economics | `02_lit/ECON_LIT.md`, `ECON_TARGETS.csv`, `SHADOW_TARGETS.csv`, `COUNTRY_CARDS/` | 29 + 21 quantities | verified-at-source only where a file exists in `02_lit/raw/` |
| 4. Massification theory | `10_massification/lit/*.md` (11 files) | ~110 KB | `VERIFIED` / `STANDARD-CITATION` / `NOT-FOUND` labels used consistently |

### 1(a) Works the repo cites with a real, checkable reference

"Real reference" = author + year + title + venue, and (in the ledger's §A) a URL with a recorded HTTP status.
Most are also *read*.

| # | Work | Where it is used | Access / status |
|---|---|---|---|
| A1 | Yoo, Y.-H. (2003) *Private Tutoring as Rent Seeking…*, KDI | Ledger §A3; `MASSIFICATION_THEORY` §11; `EQUATION_REGISTER` LQ-04 | FULL-TEXT (37 pp) |
| A2 | Kim, J.-H. (2007) *A Game Theoretical Approach to Private Tutoring in South Korea*, NCSPE OP144 | Ledger §A4; `MASSIFICATION_THEORY` §11; LQ-05 | FULL-TEXT (26 pp) |
| A3 | Kang, H. (2026) *The Parental Investment Rat Race*, working paper | Ledger §A6; `MASSIFICATION_THEORY` §11; `RIVAL_MODELS_ANCHOR` §2.6 | FULL-TEXT |
| A4 | He, S. (2024) *Quantifying Educational Competition*, arXiv:2412.10974 | Ledger §A17; `MASSIFICATION_THEORY` §11; LQ-03 | FULL-TEXT (preprint) |
| A5 | Ghaffarzadegan, Xue & Larson (2017) *Work-Education Mismatch*, PMC5509065 | Ledger §A8; `MASSIFICATION_THEORY` §11; LQ-09; `PUSH_PULL` Rival B | FULL-TEXT (equations in unreadable Vensim appendix) |
| A6 | Ostrovsky & Schwarz (2010) *Information Disclosure and Unraveling…*, AEJ:Micro 2(2) | Ledger §A9; `MASSIFICATION_THEORY` §11 | FULL-TEXT (ms.) |
| A7 | Jayachandran (2014) *Incentives to teach badly*, JDE 108 | Ledger §A10; `MODEL_CARDS` §4; `ECON_TARGETS` | FULL-TEXT (16 pp) |
| A8 | Yang, Z. (2026) *Regulating Private Tutoring*, Economies 14(9):415 | Ledger §A7; `MASSIFICATION_THEORY` §11; architecture notes | ABSTRACT-ONLY (MDPI 403) |
| A9 | Boudon, R. (1974) *Education, Opportunity, and Social Inequality* | Ledger §A2 | ABSTRACT-ONLY (ERIC record) |
| A10 | Edmonds & Moss (2005) *From KISS to KIDS*, LNAI 3415 | Ledger §A1 | FULL-TEXT (but the URL is the whole proceedings) |
| A11 | Gee, C. (2012) *The Educational 'Arms Race'*, IPS WP 20 | Ledger §A20; `MASSIFICATION_THEORY` §5 note | FULL-TEXT (37 pp) |
| A12 | Yu & Ding (2011); Saha & Saha (2009); Bray et al. (2014) | Ledger §A5, A12, A15 | METADATA-ONLY |
| A13 | Biswal (1999); Ille & Peacey (2019); Choi (2010) | Ledger §A11, A13, A19 | LANDING-ONLY |
| A14 | Bray et al. (2016); Bray & Kwok (2003); Suen & Xu (n.d.) | Ledger §A14, A16, A18 | BLOCKED |
| A15 | Psacharopoulos & Patrinos (2018) WB PRWP 8402 | `MASSIFICATION_THEORY` §5; `SCALING_LAWS` §2; `ECON_TARGETS`; `EXPECTATIONS` MIN-01 | FULL-TEXT (raw file on disk) |
| A16 | Clemens, Montenegro & Pritchett (2008) WB PRWP 4671 | `PUSH_PULL`; `ANCHOR_SYSTEM_EVIDENCE` §2; `ECON_TARGETS` | FULL-TEXT |
| A17 | Abarcar & Theoharides (2024) medical-worker migration | Ledger §B; `PUSH_PULL` Rival A; `ANCHOR_SYSTEM_EVIDENCE` §2 | VERIFIED via NBER SI slides |
| A18 | World Bank (2017) *Developing Socioemotional Skills for the Philippines* | `LABOUR_MARKET_REPORTS` §1.1; `ANCHOR_SYSTEM_EVIDENCE` §2; `RIVAL_MODELS_ANCHOR` §1 | FULL-TEXT (Table 2.1) |
| A19 | IBE (2006) EFA-GMR country profile, Philippines | `RIVAL_MODELS_ANCHOR` §1; `LABOUR_MARKET_REPORTS` §1.2 | OBSERVED (archived via data-hunter) |
| A20 | Bettencourt et al. (2007) *Growth, innovation, scaling…*, PNAS 104(17) | `SCALING_LAWS` §1 (12 verified exponents) | FULL-TEXT (PMC) |
| A21 | Brehm & Silova (WP39, Cambodia); de Castro & de Guzman (2010); Rappleye & Komatsu (2020); SEA-PLM 2024 (KHM) | `02_lit/README.md` iteration-2 additions; `COUNTRY_CARDS` | FULL-TEXT in `02_lit/raw/` |

### 1(b) Works named without a full reference

The massification layer runs almost entirely on **named canonical works that were never retrieved**.
`MASSIFICATION_THEORY.md` is honest about this — every entry carries `STANDARD-CITATION` — but the
practical consequence is that the programme's theoretical spine is unaudited.

| Work | Where named | What is missing |
|---|---|---|
| Trow (1973) elite/mass/universal thresholds | `MASSIFICATION_THEORY` §1; `UNIVERSALIZATION_TIMING` §4; `RIVAL_MODELS_TO_TEST` #1 | no title, no venue, no page; thresholds used as if definitional |
| Schofer & Meyer (2005) *ASR* 70(6), world society | `MASSIFICATION_THEORY` §2; `UNIVERSALIZATION_TIMING` §4; `RIVAL_MODELS_ANCHOR` §2.1 | journal given, **specification and coefficients explicitly not retrieved** |
| Raftery & Hout (1993) *ASR* 58(1), MMI | `MASSIFICATION_THEORY` §3; ledger §B; `RIVAL_MODELS_TO_TEST` #3 | no DOI/URL; odds-ratio method described from memory |
| Breen & Goldthorpe (1997), RRA | `MASSIFICATION_THEORY` §4; ledger §B last row | **explicitly not cited in either manuscript** (0 hits) — the brief was wrong |
| Becker (1964); Mincer (1974) | `MASSIFICATION_THEORY` §5; `UNIVERSALIZATION_TIMING` §4; `EXPECTATIONS` WS-02 | books named only; the Mincer *form* is called "canonical, safe to state" |
| Spence (1973); Arrow (1973) | `MASSIFICATION_THEORY` §6; `RIVAL_MODELS_ANCHOR` §2.3 | no titles; "not reproduced here" |
| Thurow (1975); Collins (1979) | `MASSIFICATION_THEORY` §7–8; ledger §B rows 43–44; `EXPECTATIONS` WS-03 | titles given, no URL, never retrieved |
| Gellner (1983); Tilly (1990) | `MASSIFICATION_THEORY` §9; `STATE_CAPACITY` §1.1 | books named only |
| Paglayan (2024) *APSR* | `MASSIFICATION_THEORY` §9; `STATE_CAPACITY` §1.1; `RIVAL_MODELS_ANCHOR` §2.4 | venue given, text never read |
| Ansell & Lindvall (2020) | `STATE_CAPACITY` §1.1; `RIVAL_MODELS_ANCHOR` §2.4 | no title, no venue |
| Acemoglu, Johnson & Robinson (2001, 2005); Besley & Persson (2009, 2013) | `STATE_CAPACITY` §1.2 | named as a block, no titles |
| Angrist & Krueger (1991); Oreopoulos (2006) | `STATE_CAPACITY` §1.4 | named for the compulsory-schooling result, no refs |
| Benavot | `MASSIFICATION_THEORY` §10 | **no year, no title, no venue** — the weakest attribution in the set |
| Hanushek & Woessmann (2015) *The Knowledge Capital of Nations* | `EXPECTATIONS` EDU-01/EDU-02; `08_council/CHARTER.md` (HANUSHEK persona) | book named, **never in the ledger**, label UNVERIFIED/BLOCKED |
| Hidalgo & Hausmann (2009); Hausmann et al. (2013) *Atlas of Economic Complexity* | `EXPECTATIONS` ECI-01, ECI-03; `EQUATION_REGISTER` SEC-05 | method named, no ref; register calls ECI↔schooling "narrative-only" |
| Ng & Yip (2020) *Economic Modelling* 84 | Ledger §B; both manuscripts | **citation suspect** — subtitle is Gee's (2012); guessed DOI resolved to an unrelated article |
| Mousley et al. (2025) *Nature Communications*; Rawski (1979); Elman (2000); Scribner & Cole (1981); Heyes (2018); Clark & Nielsen (2024); Magallanes et al. (2021); Brinch & Galloway (2012); Banks & Mazzonna (2012); Ritchie & Tucker-Drob (2018) | Ledger §B | all "cited, unverified"; none retrieved |
| Hara & Saito; JICA study | `UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG` §1c | no year, no title |

### 1(c) Claims made with no citation at all

These are the load-bearing places where the programme **states a functional form or a magnitude and
attributes it to nothing**.

| Claim / form | Where | Status |
|---|---|---|
| `effective_push = law_t · C_t^κ`, **κ = 0.75** (range 0.5–1.0) | `EQUATION_REGISTER` SB-01; `model/anchor.py` L64–90 | `programme-invented` |
| Capacity index weights **0.5 delivery / 0.3 fiscal / 0.2 enforcement**; `x_del=clip((40−PTR)/20)`, `x_fis=clip((%GDP−2)/3)`, `x_enf=years/13` | SB-02; `anchor.py` L46–61 | `programme-invented` |
| `births_t = 0.5·Σ_{15..49} pop·TFR/35`; one-year ageing with survival **0.995/0.994/0.96** | DEM-01, DEM-02; `pushpull.py` L36–39, 71–77 | `programme-invented` |
| Intake/progression/jobs/education-led feedback equations (PP-01…PP-05, PP-07…PP-09) | `EQUATION_REGISTER` §4.6 | 8 `programme-invented` |
| Sectoral reduced forms (agriculture `0.75·exp(−0.35 ln gdp)+0.02`; services `0.45+0.08 ln gdp+0.15 educ`; formal share `0.25+0.55 educ+0.05 ln gdp`) | SEC-01…SEC-03; `pushpull.py` L123–128 | `programme-invented` (constants "chosen, not estimated") |
| Cohort-size → completion coefficient **−0.1893 / −0.1222** | DEM-03; `scaling_laws.csv` S12 | `programme-estimated` |
| ECI ↔ schooling **0.593**; ECI → growth replication "fails" | SEC-05; `09_relations` | `narrative-only` + `programme-estimated` |
| "Literacy moves with GDP growth while years of schooling do not" | `EXPECTATIONS` LIT-01 | user's 2015 observation, restated as a frozen test — explicitly no literature |
| "62–66% of adult-literacy gains is cohort replacement" | `EXPECTATIONS` LIT-02 | programme estimate |
| "Literacy can stand in for cognitive skills" | `EXPECTATIONS` LIT-03 | the programme's own identification assumption, no source |
| "Gating is a regime switch, not a slope" | `EXPECTATIONS` ABS-02 | Dr Menefee's verbal specification, "recorded as design (not evidence)" |
| Education–output elasticity | `SCALING_LAWS` §4 | declared **not a standard quantity**; no number exists and none should be inserted |
| The Yang (2026) CES form `T(e,x)=A[λe^μ+(1−λ)x^μ]^{1/μ}` | `03_model_architecture.md` | **author's conjecture**, not Yang's — register refuses to encode it |

**Count.** Of the 43 relationships in `EQUATION_REGISTER.csv`, **10 are equations the literature actually
states, 13 are narrative-only, and 20 exist only because this programme wrote them down** (15 invented,
5 estimated). That ratio — 23% literature, 47% programme — is the single most important number in this audit.

---

## 2. Five-strand gap analysis

Verdicts: **COVERED** = the strand's literature is present with usable references; **PARTIAL** = the
theme is named but not evidenced (named-only or unverified); **ABSENT** = no internal coverage at all.

| Strand | Verdict | What exists internally | What is missing | Where the gap bites |
|---|---|---|---|---|
| **(a) Schooling vs cognitive skills and growth** | **PARTIAL** | `MASSIFICATION_THEORY` §5 (Becker/Mincer, STANDARD-CITATION) and §6 (Spence/Arrow); `EXPECTATIONS` EDU-01/EDU-02 name Hanushek & Woessmann (2015) but label them UNVERIFIED/BLOCKED; `SCALING_LAWS` §4 states there is **no canonical education–output elasticity**; `PUSH_PULL` B1 "NOT FOUND" | The Hanushek–Woessmann reference itself (never entered the ledger); any learning-outcome series (no PISA/TIMSS in any on-disk panel); any growth regression using cognitive skills | The programme's headline claim — that expansion is decoupled from skills — currently rests on a **Mincer price** (8.8%) and a **firm-constraint share** (10.1%), not on any skills–growth estimate. `EXPECTATIONS` EDU-02 is marked BLOCKED for exactly this reason. |
| **(b) ECI / complexity and growth** | **PARTIAL** | ECI is used heavily in the analysis layer (282 repo files contain the token; `09_relations/DATA_PATTERNS.md` tests C1–C11); `EXPECTATIONS` ECI-01…ECI-04 name Hidalgo & Hausmann (2009) and Hausmann et al. (2013) as UNVERIFIED; `EQUATION_REGISTER` SEC-05 records ECI↔schooling as narrative-only and notes the ECI→growth replication **fails** (−0.158, −0.068) | A verified ECI-method reference; any of the growth-complexity literature; a functional form for ECI↔schooling | The complexity strand is **measured but uncited**. Every ECI coefficient in the repo is `programme-estimated`, and the one published relationship the programme tried to replicate did not replicate. A referee will ask for the Hidalgo–Hausmann citation and there is no reference to give. |
| **(c) Absorptive capacity / threshold / dual economy** | **ABSENT** | Nothing. No Lewis, no dual-economy model, no threshold/regime literature, no "absorptive capacity" citation anywhere in the lit layer. The only trace is `EXPECTATIONS` ABS-01 ("no published estimate located") and ABS-02 ("Dr Menefee's verbal specification") | The entire literature: dual-economy/structuralist accounts, threshold and poverty-trap models, absorptive-capacity arguments, and any empirical threshold estimate | This is the programme's **most original and least supported** claim. The "kickstarted" hypothesis (schooling pays only above a complexity/development threshold) is currently a verbal prior with a frozen test and **no literature behind it** — and `EXPECTATIONS` records that the on-disk interaction has the **opposite** sign. |
| **(d) Educated unemployment / credential queue / job matching** | **PARTIAL** (theory covered, empirics absent) | Thurow (1975) job competition, Collins (1979) credential inflation, Spence/Arrow signalling, Raftery–Hout MMI, GXL (2017) overshoot, Ostrovsky–Schwarz (2010) matching/unraveling, `RIVAL_MODELS_ANCHOR` §2.3 | Any measured overeducation/graduate-unemployment estimate for PHL/KHM/CHN/KOR; employer requirement series; ILO/OECD report corpus (explicitly not delivered — `LABOUR_MARKET_REPORTS` §2) | `PUSH_PULL` says the overeducation literature is "NOT VERIFIED this session"; `ECON_TARGETS` marks 11 quantities `unusable`. The queue story is therefore **theoretical only**, which is a problem because the programme's distinguishing prediction (investment rises as returns fall) is a queue prediction. |
| **(e) Existing structural / cohort-component projection models** | **ABSENT** | **Zero citations.** The only appearance of the entire field is `08_council/CHARTER.md` line 98, where Wolfgang Lutz is listed as a **council persona** ("Multi-state cohort-component model with education transitions", access column "publication") — a roster entry, not a reference. Barro–Lee and Wittgenstein appear **only as data-provenance caveats**: `DATA_LEDGER.md` line 29 and `04_data/econ_round2/WBSOURCE_NOTES.md` line 56 warn that WDI `SE.*.CUAT.*` shares are "modelled (Barro–Lee/Wittgenstein)". Searches for `IIASA`, `EPSSim`, `cohort-component` (as a literature term) return **0–1 hits**, none in the lit layer | Everything covered in `rows_C_projections.csv`: WIC/Lutz method, the 2018 and 2023 vintages, Barro–Lee, EPSSim, the UNESCO simulation model, MOSART, education ABMs | **This is the actionable gap.** The programme has built its own cohort-flow engine (`DEM-01/DEM-02`, survival constants 0.995/0.994/0.96, a `1/35` birth formula) **without citing the 20-year literature that does exactly this properly**. The demography is a reinvention, and it is the part most likely to be challenged: the WIC method is published, its data are CC BY 4.0, and its outputs are a ready external benchmark (mean years of schooling by age/sex/country). |

---

## 3. Does the repo's literature ledger contain growth/complexity literature? What does it contain instead?

**No.** `LITERATURE_LEDGER.md` — the file the programme calls its ledger — contains **no growth
literature and no complexity literature at all**. This is not an impression; it is a word-level fact
(case-insensitive, whole-word counts over the file's 74 lines):

| Search term | Occurrences in `LITERATURE_LEDGER.md` |
|---|---|
| `growth` | **0** |
| `complexity` | **0** |
| `ECI` | **0** |
| `Hanushek` / `Woessmann` | **0** / **0** |
| `Schofer` / `Meyer` | **0** / **0** |
| `Barro` / `Lutz` / `Wittgenstein` / `IIASA` | **0** / **0** / **0** / **0** |
| `PISA` | **0** |
| `absorptive` / `dual economy` / `Lewis` | **0** |
| `cognitive` | **2** (both incidental: "cognitive effects" and *Cognitive Gadgets*) |

**What it contains instead** is a **shadow-education and credential-competition** corpus: 20 core sources
(9 read in full, 6 of those at equation level) on private tutoring, positional competition and gate
mechanics — Yoo, Kim, Kang, Jayachandran, GXL, Ostrovsky–Schwarz, He, Boudon, Gee, plus the Bray/Biswal/
Saha/Ille-Peacey tutoring cluster — followed by a §B list of ~19 manuscript references (Thurow, Collins,
Raftery–Hout, Lucas, Paglayan, Abarcar–Theoharides, Stange, Ng–Yip, …) that are mostly "cited, unverified",
and a §C list of ~27 named-but-never-retrieved official documents (PSA, UIS, World Bank, PIDS, ASEAN, ADB).
It is an excellent ledger **for the shadow-education phase**. It is not a ledger for a massification model.

**The `EXPECTATIONS.csv` suspicion — half right, and the half that is wrong matters.**
The file has **19 data rows, not zero standard-citation rows**. Nine of the 19 name a real work
(EDU-01/EDU-02 Hanushek–Woessmann; MIN-01 Psacharopoulos–Patrinos; MIN-03 Clark–Nielsen; ECI-01 and
ECI-03 Hidalgo–Hausmann; WS-01 Schofer–Meyer; WS-02 Becker/Mincer; WS-03 Thurow/Collins). Ten name none
(LIT-01, LIT-02, LIT-03, MIN-02, ECI-02, ECI-04, ABS-01, ABS-02, ID-01, GEN-01). Labels split
**7 UNVERIFIED / 4 BLOCKED / 8 PROGRAMME-PRIOR**.

So the honest statement is **not** "zero standard-citation rows". It is:
**every one of the 19 rows is unsupported by a reference the repo actually holds.** The `source_file`
column says so itself, over and over: "LITERATURE_LEDGER.md (0 hits for 'ECI'/'Hidalgo')",
"LITERATURE_LEDGER.md (0 hits for 'Schofer'/'world society')", "LITERATURE_LEDGER.md (no Becker/Mincer
row)", "LITERATURE_LEDGER.md (no growth-accounting row)", "no ledger entry exists". The longitudinal
extension therefore has a **complete set of expectations and no held literature to test them against** —
which is consistent with, and explains, the suspicion that sent me to check.

**One further finding, more consequential than either.** The equation register shows the literature layer
supplies **mechanism and falsifiers, never functional forms**. Only 10 of 43 relationships are equations
the literature states; all 10 are gate/contest or Mincer mechanics. The moment the programme needed a
cohort-flow engine, a capacity gate, a sectoral structure or a demographic transition, it **invented the
form and wrote "programme-invented" in the status column**. Strand (e) is therefore not merely an
uncited literature — it is the literature that would have supplied precisely the forms the programme had
to invent.

---

## 4. What this implies for the programme (three sentences)

1. **Reusable, not just citable:** the WIC 2023 projection dataset is **CC BY 4.0** (Zenodo
   `10.5281/zenodo.7767425`) and its method is published in full (KC et al. 2010, open access;
   IIASA IR-13-018). A synthetic workbench can adopt the multi-state cohort-component structure and
   benchmark its outputs against WCDE mean-years-of-schooling **without building the demography from scratch**.
2. **Cite EPSSim for the cost-and-flow layer** (UNESCO, free, full specification) and **MOSART** for the
   individual-level microsimulation precedent — the latter is the honest contrast case because it needs
   population registers, which is exactly what a synthetic workbench would fabricate.
3. **Do not claim novelty for cohort-component education projection.** It is a 20-year-old, published,
   openly licensed literature; the programme's novelty has to sit in the gate/queue/absorptive mechanism,
   not in the demographic engine.

---

## 5. URLs fetched

Retrieved with `curl` (browser UA, `-L`, 45 s timeout) on **2026-11-20 (Asia/Shanghai)**, because the
`web_fetch` tool rejected every host as "non-public IP" (environment DNS maps public hosts to 198.18.0.0/15).
Sizes are bytes on disk; hashes are the first 16 hex characters of SHA-256.

**HTTP 200 — opened and read**

| URL | Status | Bytes | SHA-256 prefix | What it is |
|---|---|---|---|---|
| https://pure.iiasa.ac.at/id/eprint/10742/1/IR-13-018.pdf | 200 | 1,496,583 | `980db41153b083d6` | WIC method report (87 pp) |
| https://www.demographic-research.org/volumes/vol22/15/22-15.pdf | 200 | 2,185,836 | `44f1b16256a0d4c6` | KC et al. 2010 (92 pp) |
| https://www.undp.org/sites/g/files/zskgke326/files/publications/User%20Guide%20Education%20Policies%20and%20Strategies.pdf | 200 | 1,815,750 | `c14d76c7f60f1ab5` | EPSSim 2.1 User's Guide (52 pp) |
| http://specialcollections.nust.na:8080/greenstone3/library/sites/localsite/collect/unesco/index/assoc/HASH0197/b1c274bb.dir/Education_planning_through_computer_simulation.pdf | 200 | 485,727 | `a84cdec0ebc1652a` | Chang & Radi 2001 (85 pp) |
| https://www.ssb.no/en/utdanning/artikler-og-publikasjoner/_attachment/106069?_ts=13dcebade90 | 200 | 673,712 | `0cd1b1e831973333` | Gjefsen 2013 / MOSART (58 pp) |
| https://www.jasss.org/17/2/3/3.pdf | 200 | 2,044,721 | `85c650bced4689b8` | Maroulis et al. 2014 (14 pp) |
| http://barrolee.com/ | 200 | 26,458 | `2e18db1e6b9e54eb` | Barro–Lee dataset home |
| http://barrolee.com/?p=57 | 200 | 26,306 | `e6fbb7c740bfe9a5` | Barro–Lee methodology page |
| https://www.wittgensteincentre.org/en/index.htm | 200 | 25,228 | `14cc6cc484bc4415` | WIC home (links to WCDE v3) |
| https://dataexplorer.wittgensteincentre.org/wcde-v3/ | 200 | 152,604 | `1ba4ad08523546af` | WCDE 3.0 application |
| https://zenodo.org/records/7767425 | 200 | 172,812 | `e90cc8aacb95d00d` | WIC 2023 dataset record (CC BY 4.0) |
| http://epub.wu.ac.at/6458/1/jrc_cepam_report_demographic_and_hc_scenarios_pdf.pdf | 200 | 36,129 | `89259920a54d7a8a` | WU record for WIC 2018 report (PDF redirected to a landing page — abstract only) |
| https://openknowledge.worldbank.org/entities/publication/17a669b5-2128-58fe-88a8-9d7cea10e7ff | 200 | 2,372 | `95f222f5d1221167` | World Bank OKR entity shell (JS, no content) |
| https://api.openalex.org/works/doi:10.1016/j.jdeveco.2012.10.001 | 200 | 12,485 | — | Barro–Lee metadata (title/venue/authors/DOI) |
| https://api.openalex.org/works?search=… (six bibliographic queries) | 200 | — | — | KC 2010, KC & Lutz 2014, WIC 2018, OUP book, Tools for Education Policy Analysis, WIC 2023 |

**Non-200 — recorded, not used**

| URL | Status | Note |
|---|---|---|
| https://uis.unesco.org/sites/default/files/documents/projecting-the-global-demand-for-teachers-meeting-the-goal-of-universal-primary-by-2015-en_0.pdf | **404** | UIS teacher-demand projection — row C15 left UNVERIFIED |
| https://webarchive.unesco.org/web/20160802222513/http://www.uis.unesco.org/Education/Documents/fs27-2013-teachers-projections.pdf | 200 but HTML | archive stub, no PDF |
| https://op.europa.eu/en/publication-detail/-/publication/18a1b3a9-1c6a-11e8-ac73-01aa75ed71a1 | **403** | WIC 2018 official page |
| https://doi.org/10.2760/835878 | **403** | WIC 2018 DOI |
| https://global.oup.com/academic/product/world-population-and-human-capital-in-the-twenty-first-century-9780198703167 | **202** | JS challenge, 2,003 B |
| https://api.crossref.org/works/… | **429** | rate-limited (twice); OpenAlex used instead |
| https://www.iiasa.ac.at/ | **403** | Cloudflare challenge |
| https://documents1.worldbank.org/curated/en/986051468762868297/txt/multi0page.txt | 000 | connection refused |
| https://vital.voced.edu.au/vital/access/manager/Repository/ngv:23798 | 000 | catalogue record unreachable |
| http://repositorio.minedu.gob.pe/bitstream/handle/20.500.12799/4096/…EPSSim…pdf | 200 but HTML | Check Point bot wall (the UNDP copy was used instead) |

*No external claim in this file or in `rows_C_projections.csv` rests on a page that was not opened.*
