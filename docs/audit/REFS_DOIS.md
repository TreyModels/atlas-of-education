# REFS_DOIS — DOI / ISBN / publisher register for sources cited in the audit corpus

Owner: citation/register pass (`engine-tutoring` lane; task from Lead) · date 2026-11-25 · **status: register only — no claim in any document is upgraded by being listed here**; status column records what was actually verified.

Purpose: answer the operator question “are we giving all these DOIs?”. One row per source cited anywhere in the audit corpus, with the identifier that exists (DOI, else ISBN/publisher), the verification status, and the documents that cite it. The 183-equation inventory is treated as a **candidate map, not a bibliography**: its placeholder tokens are excluded (§5). Documents patched with cross-references: `MODEL_ZOO_DISCRIMINATORS.md`, `MODEL_ZOO_SCOPE.md`, `PAPER_D_EQUATION_AUDIT.md` (see each doc’s final section).

**Scope of corpus scan:** all `docs/audit/*.md` (62 files) and `verification/lean/*.lean` (2 files): 63 files total. "Docs citing" uses basenames; `CITATION_VERIFICATION_SHADOW_ED.md` is itself a verification report and appears as a citing doc where it discusses the work.

**Status legend:** `VERIFIED PRIMARY TEXT` = full text obtained and the cited object checked; `VERIFIED BIBLIOGRAPHIC` = publisher/Crossref record checked, full text not read here; `ABSTRACT-ONLY`; `PAYWALLED — NOT RETRIEVED`; `BOOK — BIBLIOGRAPHIC` (monograph, no equation claims made from it); `INSTITUTIONAL DATA SOURCE`; `UNVERIFIED` = no traceable primary source found; `CITATION UNVERIFIED` = model-zoo tag V.

## 1. Register (all sources)

| key | citation | DOI / ISBN / publisher | status | docs citing (basenames, `.md` omitted) |
|---|---|---|---|---|
| `becker_lewis_1973` | Becker, G. S. & Lewis, H. G. (1973). On the Interaction between the Quantity and Quality of Children. Journal of Political Economy 81(2, Part 2):S279–S288. | DOI 10.1086/260166 | **VERIFIED BIBLIOGRAPHIC** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `biswal_1999` | Biswal, B. P. (1999). Private tutoring and public corruption: A cost-effective education system for developing countries. The Developing Economies 37(2):222–240. | DOI 10.1111/j.1746-1049.1999.tb00232.x | **PAYWALLED — NOT RETRIEVED (content described in Dang & Rogers 2008)** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, DHS_E1E8_MODEL_MAPPING.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `bray_2016` | Bray, M., Kobakhidze, M. N., Liu, J., & Zhang, W. (2016). The internal dynamics of privatised public education: Fee-charging supplementary tutoring provided by teachers in Cambodia. International Journal of Educational Development 49:291–299. | DOI 10.1016/j.ijedudev.2016.04.003 | **VERIFIED BIBLIOGRAPHIC (not full-text read)** | — (register-only; not yet cited in scanned corpus) |
| `bray_kwok_2003` | Bray, M. & Kwok, P. (2003). Demand for private supplementary tutoring: Conceptual considerations, and socio-economic patterns in Hong Kong. Economics of Education Review 22(6):611–620. | DOI 10.1016/S0272-7757(03)00032-3 | **VERIFIED BIBLIOGRAPHIC (not full-text read)** | — (register-only; not yet cited in scanned corpus) |
| `callaway_santanna_2021` | Callaway, B. & Sant’Anna, P. H. C. (2021). Difference-in-Differences with multiple time periods. Journal of Econometrics 225(2):200–230. | DOI 10.1016/j.jeconom.2020.12.001 | **VERIFIED BIBLIOGRAPHIC** | CITATION_VERIFICATION_SHADOW_ED.md, COMPUTE_SCHEDULE.md, CS_ESTIMATOR_NEWGEN.md, E8_BULGE_NEWGEN.md, GATE2_PREREGISTRATION.md, PAPER_A_REPRODUCTION_ATTEMPT.md, PAPER_A_VERIFICATION.md |
| `cragg_1971` | Cragg, J. G. (1971). Some Statistical Models for Limited Dependent Variables with Application to the Demand for Durable Goods. Econometrica 39(5):829–844. | DOI 10.2307/1909582 | **VERIFIED BIBLIOGRAPHIC** | CITATION_VERIFICATION_SHADOW_ED.md |
| `cunha_heckman_2007` | Cunha, F. & Heckman, J. (2007). The Technology of Skill Formation. American Economic Review 97(2):31–47. | DOI 10.1257/aer.97.2.31 | **VERIFIED BIBLIOGRAPHIC** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `dang_2007` | Dang, H.-A. (2007). The determinants and impact of private tutoring classes in Vietnam. Economics of Education Review 26(6):683–698. | DOI 10.1016/j.econedurev.2007.10.003 | **PAYWALLED — NOT RETRIEVED** | CITATION_VERIFICATION_SHADOW_ED.md |
| `dang_rogers_2008` | Dang, H.-A. & Rogers, F. H. (2008). The Growing Phenomenon of Private Tutoring: Does It Deepen Human Capital, Widen Inequalities, or Waste Resources? The World Bank Research Observer 23(2):161–200. | DOI 10.1093/wbro/lkn004 | **VERIFIED PRIMARY TEXT** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `filmer_2020_lays` | Filmer, D., Rogers, H., Angrist, N., & Sabarwal, S. (2020). Learning-adjusted years of schooling (LAYS): Defining a new macro measure of education. Economics of Education Review 77:101971. | DOI 10.1016/j.econedurev.2020.101971 | **VERIFIED BIBLIOGRAPHIC** | CITATION_VERIFICATION_SHADOW_ED.md, DASHBOARD.md, DHS_E1E8_MODEL_MAPPING.md, ENGINE_INTERFACE_CONTRACT.md, PAPER_D_EQUATION_AUDIT.md, TUTORING_AUDIT.md, TUTORING_CODEBOOK_VERIFICATION.md, TUTORING_DATA_INVENTORY.md, TUTORING_PHASE_B.md |
| `hanushek_1986` | Hanushek, E. A. (1986). The Economics of Schooling: Production and Efficiency in Public Schools. Journal of Economic Literature 24(3):1141–1177. | No DOI. JSTOR stable URL: https://www.jstor.org/stable/2725865 | **BIBLIOGRAPHIC — AMBIGUOUS AS CITED (docs say only “Hanushek” without year/title; this is the standard candidate work)** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, DHS_E1E8_MODEL_MAPPING.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md, SYNTHETIC_DGP_VALIDATION.md |
| `jayachandran_2014` | Jayachandran, S. (2014). Incentives to teach badly: After-school tutoring in developing countries. Journal of Development Economics 108:190–205. | DOI 10.1016/j.jdeveco.2014.02.008 | **VERIFIED PRIMARY TEXT** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, DHS_E1E8_MODEL_MAPPING.md, LEMMA_LEDGER.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `karakus_2024` | Karakus, M., Tlessov, A., Hajar, A., & Courtney, M. (2024). Illuminating the shadows: the role of private supplementary tutoring on student math performance in PISA 2022. Large-scale Assessments in Education 12, article 00228-5. | DOI 10.1186/s40536-024-00228-5 | **VERIFIED BIBLIOGRAPHIC (Crossref); full text not read here** | TUTORING_DATA_INVENTORY.md |
| `kim_lee_2010` | Kim, S. & Lee, J.-H. (2010). Private Tutoring and Demand for Education in South Korea. Economic Development and Cultural Change 58(2):259–296. | DOI 10.1086/648186 | **ABSTRACT-ONLY (full text paywalled)** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `kwo_bray_2014` | Kwo, O. & Bray, M. (2014). Understanding the nexus between mainstream schooling and private supplementary tutoring: Patterns and voices of Hong Kong secondary students. Asia Pacific Journal of Education 34(4):403–416. | DOI 10.1080/02188791.2014.961900 | **VERIFIED BIBLIOGRAPHIC (not full-text read)** | MANUSCRIPT_ERRATA.md |
| `lucas_1988` | Lucas, R. E. (1988). On the Mechanics of Economic Development. Journal of Monetary Economics 22(1):3–42. | DOI 10.1016/0304-3932(88)90168-7 | **VERIFIED BIBLIOGRAPHIC** | CITATION_VERIFICATION_SHADOW_ED.md |
| `mankiw_romer_weil_1992` | Mankiw, N. G., Romer, D., & Weil, D. N. (1992). A Contribution to the Empirics of Economic Growth. The Quarterly Journal of Economics 107(2):407–437. | DOI 10.2307/2118477 | **VERIFIED BIBLIOGRAPHIC** | CITATION_VERIFICATION_SHADOW_ED.md |
| `psacharopoulos_patrinos_2018` | Psacharopoulos, G. & Patrinos, H. A. (2018). Returns to Investment in Education: A Decennial Review of the Global Literature. Education Economics 26(5):445–458. | DOI 10.1080/09645292.2018.1484426 | **VERIFIED BIBLIOGRAPHIC** | CITATION_VERIFICATION_SHADOW_ED.md |
| `spence_1973` | Spence, M. (1973). Job Market Signaling. The Quarterly Journal of Economics 87(3):355–374. | DOI 10.2307/1882010 | **VERIFIED BIBLIOGRAPHIC** | DHS_E1E8_MODEL_MAPPING.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md |
| `sun_abraham_2021` | Sun, L. & Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. Journal of Econometrics 225(2):175–199. | DOI 10.1016/j.jeconom.2020.09.006 | **VERIFIED BIBLIOGRAPHIC** | CITATION_VERIFICATION_SHADOW_ED.md |
| `tansel_bircan_2006` | Tansel, A. & Bircan, F. (2006). Demand for education in Turkey: A tobit analysis of private tutoring expenditures. Economics of Education Review 25(3):303–313. | DOI 10.1016/j.econedurev.2005.02.003 | **VERIFIED PRIMARY TEXT (working-paper version; published version bibliographically verified)** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `tobin_1958` | Tobin, J. (1958). Estimation of Relationships for Limited Dependent Variables. Econometrica 26(1):24–36. | DOI 10.2307/1907382 | **VERIFIED BIBLIOGRAPHIC** | CITATION_VERIFICATION_SHADOW_ED.md |
| `todd_wolpin_2003` | Todd, P. E. & Wolpin, K. I. (2003). On the Specification and Estimation of the Production Function for Cognitive Achievement. The Economic Journal 113(485):F3–F33. | DOI 10.1111/1468-0297.00097 | **VERIFIED BIBLIOGRAPHIC** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `zhan_2013` | Zhan, S., Bray, M., Wang, D., Lykins, C., & Kwo, O. (2013). The effectiveness of private tutoring: Students’ perceptions in comparison with mainstream schooling in Hong Kong. Asia Pacific Education Review 14(4):495–509. | DOI 10.1007/s12564-013-9276-7 | **VERIFIED BIBLIOGRAPHIC (not full-text read)** | MANUSCRIPT_ERRATA.md |
| `becker_human_capital` | Becker, G. S. (1964; 3rd ed. 1993). Human Capital: A Theoretical and Empirical Analysis, with Special Reference to Education. New York: Columbia University Press / NBER; 3rd ed. Chicago: University of Chicago Press. | No DOI. 3rd ed. 1993, University of Chicago Press, ISBN 978-0-226-04119-3 (ISBN via OpenLibrary edition record); 1st ed. 1964 Columbia UP/NBER | **BOOK — BIBLIOGRAPHIC (not read)** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, DHS_E1E8_MODEL_MAPPING.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `caplan_2018` | Caplan, B. (2018). The Case against Education: Why the Education System Is a Waste of Time and Money. Princeton, NJ: Princeton University Press. | No DOI. Princeton University Press, 2018; ISBN 978-0-691-17465-5 (OpenLibrary edition record) | **BOOK — CITATION UNVERIFIED (model-zoo tag V)** | AUDIT_VERDICT.md, DASHBOARD.md, LEMMA_LEDGER.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_C_CONFIRMATORY_PREREG.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `hirsch_1977` | Hirsch, F. (1977). Social Limits to Growth. London: Routledge & Kegan Paul; Cambridge, MA: Harvard University Press. | No DOI. Publishers: Routledge & Kegan Paul / Harvard UP (ISBN not independently verified in this pass) | **BOOK — BIBLIOGRAPHIC (not read)** | DHS_E1E8_MODEL_MAPPING.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md |
| `mincer_1974` | Mincer, J. (1974). Schooling, Experience, and Earnings. New York: NBER / Columbia University Press. | No DOI. NBER/Columbia University Press, 1974; ISBN 0-87014-265-8 / 978-0-87014-265-9 (OpenLibrary edition record) | **BOOK — BIBLIOGRAPHIC (not read)** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, DHS_E1E8_MODEL_MAPPING.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `tullock_1980` | Tullock, G. (1980). Efficient Rent-Seeking. In J. M. Buchanan, R. D. Tollison & G. Tullock (eds.), Toward a Theory of the Rent-Seeking Society, pp. 97–112. College Station: Texas A&M University Press. | No DOI for the 1980 original. Book: Texas A&M University Press, 1980, ISBN 0-89096-090-9 / 978-0-89096-090-5 (OpenLibrary record); 2001 reprint chapter DOI 10.1007/978-1-4757-5055-3_2 | **BIBLIOGRAPHIC (1980 original not read; reprint record verified)** | CITATION_VERIFICATION_SHADOW_ED.md, CODE_CHANGES.md, CONTEST_MATH_VALIDATION.md, DASHBOARD.md, EXTERNAL_AUDIT_GPU_2026-11-25.md, GATE1_REPORT.md, GATE2_PLAN.md, GPU_ABC_AUDITOR_PACKET.md, LEMMA_LEDGER.md, MANUSCRIPT_ERRATA.md, PAPER_A_VERIFICATION.md, PAPER_B_ADJUDICATION.md, PAPER_D_EQUATION_AUD… |
| `ceps` | China Education Panel Survey (CEPS), Renmin University of China. Datasets (Peking University Open Research Data): 10.18170/DVN/B6HK6Y, 10.18170/DVN/KE1JYM, 10.18170/DVN/QOM4FT, 10.18170/DVN/YDQJ3D. | Dataset DOIs 10.18170/DVN/B6HK6Y; 10.18170/DVN/KE1JYM; 10.18170/DVN/QOM4FT; 10.18170/DVN/YDQJ3D (resolve to opendata.pku.edu.cn; metadata pages 403-restricted) | **INSTITUTIONAL DATASET — DOIs resolve; metadata access restricted (403); no analysis in corpus** | AUDIT_VERDICT.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_C_CONFIRMATORY_PREREG.md, SCIENTIFIC_CLAIM_LEDGER.md, TUTORING_CODEBOOK_VERIFICATION.md, TUTORING_DATA_INVENTORY.md |
| `dhs` | The DHS Program / Demographic and Health Surveys, ICF International. Public-use datasets & API. | No DOI. Provider: https://dhsprogram.com/ (restricted microdata; local copies only) | **INSTITUTIONAL DATASET — no DOI; access documented in programme records** | AUDIT_VERDICT.md, COMPUTE_SCHEDULE.md, DHS_E1E8_MODEL_MAPPING.md, LEMMA_LEDGER.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, SCIENTIFIC_CLAIM_LEDGER.md, TUTORING_CODEBOOK_VERIFICATION.md, TUTORING_DATA_INVENTORY.md |
| `hk_shadow_survey_2011_12` | Hong Kong 2011/12 private supplementary tutoring survey (Grade 9 53.8 %, Grade 12 71.8 %), likely Bray/Kwo or EDB survey. | No DOI. No traceable citation in the tree; host unreachable (see G2A_CITATION_VERIFICATION.md) | **UNVERIFIED — benchmark moment DROPPED at G2-A** | AUDIT_VERDICT.md, DASHBOARD.md, G2A_CITATION_VERIFICATION.md, GATE2_PLAN.md, LEAD_GROUND_TRUTH.md, LEMMA_LEDGER.md, MANUSCRIPT_ERRATA.md, PAPER_B_ADJUDICATION.md, PAPER_C_MODEL_GAP.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `kedi_2024_2025` | KEDI / Statistics Korea (2024, 2025). Private Education Expenditure Survey reports (Korean). | No DOI. Publishers: KEDI / Statistics Korea (report hosts were unfetchable in this environment; no traceable citation in the tree) | **UNVERIFIED — source of the 80.0 %/75.7 % benchmark moments; G2-A gate DROPPED the moments** | DASHBOARD.md, G2A_CITATION_VERIFICATION.md, GATE2_PLAN.md, MANUSCRIPT_ERRATA.md, MODEL_ZOO_DISCRIMINATORS.md, PAPER_B_ADJUDICATION.md, PAPER_B_TABLE_REGENERATION.md, TUTORING_CODEBOOK_VERIFICATION.md, TUTORING_DATA_INVENTORY.md |
| `keia_2026` | KEIA (Korea Employment Information Service) material cited in MANUSCRIPT_ERRATA (2026) for the Korean labour-market context. | No DOI. Provider: KEIA (https://www.keia.or.kr/); no traceable document in the tree — source unverified | **UNVERIFIED — no traceable citation in the tree** | MANUSCRIPT_ERRATA.md |
| `kostat_provider` | Statistics Korea (KOSTAT). Private education expenditure statistics / provider-type breakdowns. | No DOI. Provider: https://kostat.go.kr/ | **INSTITUTIONAL — cited in programme docs; provider-type series not verified in this pass** | AUDIT_VERDICT.md, DHS_E1E8_MODEL_MAPPING.md, MODEL_ZOO_DISCRIMINATORS.md, SCIENTIFIC_CLAIM_LEDGER.md, TUTORING_CODEBOOK_VERIFICATION.md, TUTORING_DATA_INVENTORY.md |
| `oecd` | OECD — Organisation for Economic Co-operation and Development (PISA programme; see PISA entries for specific DOIs). | Covered by PISA DOIs above; general OECD data: https://data.oecd.org/ | **INSTITUTIONAL DATA SOURCE — no standalone DOI (inventory placeholder “OECD+3” excluded)** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, DHS_E1E8_MODEL_MAPPING.md, LEMMA_LEDGER.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_C_CONFIRMATORY_PREREG.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md, SYNTHETIC_DGP_VALIDATION.md, TUTORING_COD… |
| `oecd_pisa_2018` | OECD (2019). PISA 2018 Results (Volume II): Where All Students Can Succeed. Paris: OECD Publishing. | DOI 10.1787/b5fd1b8f-en | **INSTITUTIONAL DATA SOURCE — VERIFIED RECORD** | AUDIT_VERDICT.md, DHS_E1E8_MODEL_MAPPING.md, LEMMA_LEDGER.md, MODEL_ZOO_DISCRIMINATORS.md, PAPER_C_MODEL_GAP.md, SCIENTIFIC_CLAIM_LEDGER.md, TUTORING_CODEBOOK_VERIFICATION.md, TUTORING_DATA_INVENTORY.md |
| `oecd_pisa_2022` | OECD (2023). PISA 2022 Results (Volume I): The State of Learning and Equity in Education. Paris: OECD Publishing. (Volume II: DOI 10.1787/a97db61c-en) | DOI 10.1787/53f23881-en (Vol I); 10.1787/a97db61c-en (Vol II) | **INSTITUTIONAL DATA SOURCE — VERIFIED RECORD** | AUDIT_VERDICT.md, DHS_E1E8_MODEL_MAPPING.md, LEMMA_LEDGER.md, MODEL_ZOO_DISCRIMINATORS.md, PAPER_C_CONFIRMATORY_PREREG.md, PAPER_C_MODEL_GAP.md, SCIENTIFIC_CLAIM_LEDGER.md, TUTORING_CODEBOOK_VERIFICATION.md, TUTORING_DATA_INVENTORY.md |
| `seaplm_2019` | UNICEF & SEAMEO (2020). SEA-PLM 2019 Main Regional Report. Bangkok: UNICEF East Asia and Pacific Regional Office / SEAMEO. | No DOI. Publisher: UNICEF/SEAMEO (programme: https://www.seaplm.org/) | **INSTITUTIONAL DATA SOURCE — no DOI; report not retrieved in this pass** | AUDIT_VERDICT.md, DHS_E1E8_MODEL_MAPPING.md, MODEL_ZOO_DISCRIMINATORS.md, SCIENTIFIC_CLAIM_LEDGER.md, TUTORING_CODEBOOK_VERIFICATION.md, TUTORING_DATA_INVENTORY.md |
| `seaplm_2024` | SEA-PLM 2024 Assessment Framework (item PA18A–D on private supplementary tutoring). UNICEF/SEAMEO. | No DOI. Publisher: UNICEF/SEAMEO (framework text cited by our docs; dataset/linkage remains V) | **INSTITUTIONAL — framework text verified in programme record; dataset/linkage UNVERIFIED** | AUDIT_VERDICT.md, LEMMA_LEDGER.md, MODEL_ZOO_DISCRIMINATORS.md, PAPER_C_CONFIRMATORY_PREREG.md, SCIENTIFIC_CLAIM_LEDGER.md, TUTORING_CODEBOOK_VERIFICATION.md, TUTORING_DATA_INVENTORY.md |
| `uis` | UNESCO Institute for Statistics (UIS). Education statistics (UIS Data Centre / SDG 4 indicators). | No DOI. Provider: https://uis.unesco.org/ | **INSTITUTIONAL DATA SOURCE — no DOI (inventory placeholders “UIS+2” excluded)** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, GATE2_PREREGISTRATION.md, LEMMA_LEDGER.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZOO_SCOPE.md, PAPER_A_REPRODUCTION_ATTEMPT.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md |
| `world_bank` | World Bank. World Development Indicators / Education Statistics (EdStats) and country documents. | No DOI. Provider: https://data.worldbank.org/ ; https://databank.worldbank.org/ | **INSTITUTIONAL DATA SOURCE — no DOI (inventory placeholders “World Bank+2” excluded)** | AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, COMPUTE_SCHEDULE.md, E8_BULGE_NEWGEN.md, MANUSCRIPT_ERRATA.md, PAPER_C_MODEL_GAP.md, PAPER_D_EQUATION_AUDIT.md, SCIENTIFIC_CLAIM_LEDGER.md, TUTORING_DATA_INVENTORY.md |
| `sbs_news` | SBS News (secondary media coverage of Korean private-education spending). | No DOI. Media — secondary, not a primary source | **UNVERIFIED SECONDARY MEDIA — flagged for replacement in MANUSCRIPT_ERRATA** | G2A_CITATION_VERIFICATION.md, MANUSCRIPT_ERRATA.md, PAPER_B_ADJUDICATION.md |
| `seoulstart` | SeoulStart (secondary web summary of Korean private-education spending). | No DOI. Web summary — secondary, not a primary source | **UNVERIFIED SECONDARY WEB SOURCE — flagged for replacement in MANUSCRIPT_ERRATA** | LEMMA_LEDGER.md, MANUSCRIPT_ERRATA.md, PAPER_B_ADJUDICATION.md |
| `bray_1999` | Bray, M. (1999). The Shadow Education System: Private Tutoring and its Implications for Planners. Fundamentals of Educational Planning No. 61. Paris: UNESCO IIEP. | No DOI. Publisher: UNESCO IIEP, Paris (ISBN not independently verified in this pass) | **VERIFIED BIBLIOGRAPHIC (peer-reviewed review record)** | ABC_IDENTIFICATION_AUDIT.md, AUDIT_VERDICT.md, CITATION_VERIFICATION_SHADOW_ED.md, CONTEST_MATH_VALIDATION.md, DHS_E1E8_MODEL_MAPPING.md, EXTERNAL_AUDIT_GPU_2026-11-25.md, GPU_ABC_AUDITOR_PACKET.md, LEAD_GROUND_TRUTH.md, LEMMA_LEDGER.md, MANUSCRIPT_ERRATA.md, MODEL_ZOO_DISCRIMINATORS.md, MODEL_ZO… |
| `bray_2009` | Bray, M. (2009). Confronting the Shadow Education System: What Government Policies for What Private Tutoring? Paris: UNESCO IIEP, 132 pp. | No DOI. Publisher: UNESCO IIEP, Paris, 132 pp (ISBN not independently verified in this pass) | **VERIFIED BIBLIOGRAPHIC (two peer-reviewed review records)** | CITATION_VERIFICATION_SHADOW_ED.md |
| `bray_lykins_2012` | Bray, M. & Lykins, C. (2012). Shadow Education: Private Supplementary Tutoring and Its Implications for Policy Makers in Asia. Mandaluyong City: Asian Development Bank. | No DOI. Publisher: Asian Development Bank (ISBN not independently verified in this pass) | **VERIFIED BIBLIOGRAPHIC (publisher/record)** | SYNTHETIC_DGP_VALIDATION.md |
| `bray_1999_review_postlethwaite` | Postlethwaite, N. (2000). Book review: Bray, M. (1999) The Shadow Education System… International Review of Education 46(6):641–644. | DOI 10.1023/A:1026531112211 | **VERIFIED BIBLIOGRAPHIC (supporting record for bray_1999)** | — (register-only; not yet cited in scanned corpus) |
| `bray_2009_review_guill` | Guill, K. (2011). Book review: Bray, M. (2009) Confronting the Shadow Education System. Journal for Educational Research Online 3(2):148–151 (peDOCS record; prints “Paris: IIEP, 132 p.”). | DOI 10.25656/01:5627 (peDOCS) | **VERIFIED BIBLIOGRAPHIC (supporting record for bray_2009)** | CITATION_VERIFICATION_SHADOW_ED.md |
| `bray_2009_review_kang` | Kang, C. (2010). Book review: Confronting the Shadow Education System (Bray 2009). Education Economics 18(3):373–375. | DOI 10.1080/09645292.2010.507493 | **VERIFIED BIBLIOGRAPHIC (supporting record for bray_2009)** | — (register-only; not yet cited in scanned corpus) |
| `kim_park_2010` | Kim, J.-H. & Park, D. (2010). The determinants of demand for private tutoring in South Korea. Asia Pacific Education Review 11(3):411–421. | DOI 10.1007/s12564-009-9067-3 | **VERIFIED BIBLIOGRAPHIC — DISTINCT from the register’s kim_lee_2010; flagged for citation ambiguity** | — (register-only; not yet cited in scanned corpus) |
| `mincer_review_records` | Contemporary review records of Mincer (1974): Industrial and Labor Relations Review 29(3):454 (DOI 10.2307/2521600); Journal of Political Economy 83(2):444–446 (DOI 10.1086/260336). | DOIs 10.2307/2521600; 10.1086/260336 | **VERIFIED BIBLIOGRAPHIC (supporting records for mincer_1974)** | CITATION_VERIFICATION_SHADOW_ED.md |

## 2. Sources that have **no DOI** (book / report / data-source rows)

These are the rows where the honest answer to “what is the DOI?” is *there is none*; the publisher (and ISBN where independently known) is the identifier. No DOI was invented.

| key | identifier that exists | why no DOI |
|---|---|---|
| `hanushek_1986` | No DOI. JSTOR stable URL: https://www.jstor.org/stable/2725865 | programme report/dataset or book chapter without a DOI |
| `becker_human_capital` | No DOI. 3rd ed. 1993, University of Chicago Press, ISBN 978-0-226-04119-3 (ISBN via OpenLibrary edition record); 1st ed. 1964 Columbia UP/NBER | monograph/book |
| `caplan_2018` | No DOI. Princeton University Press, 2018; ISBN 978-0-691-17465-5 (OpenLibrary edition record) | monograph/book |
| `hirsch_1977` | No DOI. Publishers: Routledge & Kegan Paul / Harvard UP (ISBN not independently verified in this pass) | monograph/book |
| `mincer_1974` | No DOI. NBER/Columbia University Press, 1974; ISBN 0-87014-265-8 / 978-0-87014-265-9 (OpenLibrary edition record) | monograph/book |
| `tullock_1980` | No DOI for the 1980 original. Book: Texas A&M University Press, 1980, ISBN 0-89096-090-9 / 978-0-89096-090-5 (OpenLibrary record); 2001 reprint chapter DOI 10.1007/978-1-4757-5055-3_2 | programme report/dataset or book chapter without a DOI |
| `ceps` | Dataset DOIs 10.18170/DVN/B6HK6Y; 10.18170/DVN/KE1JYM; 10.18170/DVN/QOM4FT; 10.18170/DVN/YDQJ3D (resolve to opendata.pku.edu.cn; metadata pages 403-restricted) | programme report/dataset or book chapter without a DOI |
| `dhs` | No DOI. Provider: https://dhsprogram.com/ (restricted microdata; local copies only) | programme report/dataset or book chapter without a DOI |
| `hk_shadow_survey_2011_12` | No DOI. No traceable citation in the tree; host unreachable (see G2A_CITATION_VERIFICATION.md) | programme report/dataset or book chapter without a DOI |
| `kedi_2024_2025` | No DOI. Publishers: KEDI / Statistics Korea (report hosts were unfetchable in this environment; no traceable citation in the tree) | programme report/dataset or book chapter without a DOI |
| `keia_2026` | No DOI. Provider: KEIA (https://www.keia.or.kr/); no traceable document in the tree — source unverified | programme report/dataset or book chapter without a DOI |
| `kostat_provider` | No DOI. Provider: https://kostat.go.kr/ | programme report/dataset or book chapter without a DOI |
| `seaplm_2019` | No DOI. Publisher: UNICEF/SEAMEO (programme: https://www.seaplm.org/) | programme report/dataset or book chapter without a DOI |
| `seaplm_2024` | No DOI. Publisher: UNICEF/SEAMEO (framework text cited by our docs; dataset/linkage remains V) | programme report/dataset or book chapter without a DOI |
| `uis` | No DOI. Provider: https://uis.unesco.org/ | programme report/dataset or book chapter without a DOI |
| `world_bank` | No DOI. Provider: https://data.worldbank.org/ ; https://databank.worldbank.org/ | programme report/dataset or book chapter without a DOI |
| `sbs_news` | No DOI. Media — secondary, not a primary source | programme report/dataset or book chapter without a DOI |
| `seoulstart` | No DOI. Web summary — secondary, not a primary source | programme report/dataset or book chapter without a DOI |
| `bray_1999` | No DOI. Publisher: UNESCO IIEP, Paris (ISBN not independently verified in this pass) | programme report/dataset or book chapter without a DOI |
| `bray_2009` | No DOI. Publisher: UNESCO IIEP, Paris, 132 pp (ISBN not independently verified in this pass) | programme report/dataset or book chapter without a DOI |
| `bray_lykins_2012` | No DOI. Publisher: Asian Development Bank (ISBN not independently verified in this pass) | programme report/dataset or book chapter without a DOI |

## 2b. Sources still lacking full verification (beyond having no DOI)

Rows whose status is not a clean primary/bibliographic verification, or whose source could not be traced at all — the list the Lead asked for. `BOOK — BIBLIOGRAPHIC` rows are included because the monograph was not read (no equation/content claim may rest on them).

| key | status | what is missing |
|---|---|---|
| `biswal_1999` | **PAYWALLED — NOT RETRIEVED (content described in Dang & Rogers 2008)** | full text/version not verified in this pass |
| `dang_2007` | **PAYWALLED — NOT RETRIEVED** | full text/version not verified in this pass |
| `hanushek_1986` | **BIBLIOGRAPHIC — AMBIGUOUS AS CITED (docs say only “Hanushek” without year/title; this is the standard candidate work)** | full text/version not verified in this pass |
| `kim_lee_2010` | **ABSTRACT-ONLY (full text paywalled)** | full text not retrieved; only abstract verified |
| `becker_human_capital` | **BOOK — BIBLIOGRAPHIC (not read)** | full text/version not verified in this pass |
| `caplan_2018` | **BOOK — CITATION UNVERIFIED (model-zoo tag V)** | full text/version not verified in this pass |
| `hirsch_1977` | **BOOK — BIBLIOGRAPHIC (not read)** | full text/version not verified in this pass |
| `mincer_1974` | **BOOK — BIBLIOGRAPHIC (not read)** | full text/version not verified in this pass |
| `dhs` | **INSTITUTIONAL DATASET — no DOI; access documented in programme records** | full text/version not verified in this pass |
| `hk_shadow_survey_2011_12` | **UNVERIFIED — benchmark moment DROPPED at G2-A** | no traceable primary source in the tree |
| `kedi_2024_2025` | **UNVERIFIED — source of the 80.0 %/75.7 % benchmark moments; G2-A gate DROPPED the moments** | no traceable primary source in the tree |
| `keia_2026` | **UNVERIFIED — no traceable citation in the tree** | no traceable primary source in the tree |
| `kostat_provider` | **INSTITUTIONAL — cited in programme docs; provider-type series not verified in this pass** | no version/table verified in this pass |
| `oecd` | **INSTITUTIONAL DATA SOURCE — no standalone DOI (inventory placeholder “OECD+3” excluded)** | full text/version not verified in this pass |
| `seaplm_2019` | **INSTITUTIONAL DATA SOURCE — no DOI; report not retrieved in this pass** | full text/version not verified in this pass |
| `seaplm_2024` | **INSTITUTIONAL — framework text verified in programme record; dataset/linkage UNVERIFIED** | no version/table verified in this pass |
| `uis` | **INSTITUTIONAL DATA SOURCE — no DOI (inventory placeholders “UIS+2” excluded)** | full text/version not verified in this pass |
| `world_bank` | **INSTITUTIONAL DATA SOURCE — no DOI (inventory placeholders “World Bank+2” excluded)** | full text/version not verified in this pass |
| `sbs_news` | **UNVERIFIED SECONDARY MEDIA — flagged for replacement in MANUSCRIPT_ERRATA** | full text/version not verified in this pass |
| `seoulstart` | **UNVERIFIED SECONDARY WEB SOURCE — flagged for replacement in MANUSCRIPT_ERRATA** | full text/version not verified in this pass |

**Answer to the operator question, in numbers:** the register has 52 rows. Of these, 27 carry a Crossref DOI (journal articles / OECD reports) and 1 carry dataset DOIs (CEPS); 20 are books/reports/datasets with **no DOI** (ISBN or publisher recorded, never an invented DOI); the remaining rows are supporting/verification records. Every DOI string found in the scanned corpus maps to a register row (0 unregistered); every citation-like mention is either registered or flagged in §4 (0 unflagged).

## 3. DOIs present in the corpus that are **not** in this register

None: every DOI string found in the scanned corpus maps to a register row above.

## 4. Citation-like mentions not covered by a register row (flagged)

None beyond the register.

Also flagged as **not citations** (excluded from the register): agent/handles `Codex`, `Gemini`, `Claude`, `Luna`, `Lead`, `operator`, and internal artefacts (`LEMMA_LEDGER.csv`, `verification/lean/*`, engine commit hashes); these are correspondents or repository objects, not published sources.

## 5. 183-inventory sources — only those actually used, placeholders excluded

The inventory (`docs/audit/refs/education-equation-inventory-20261124.txt`, sha256 `0fd30f77…52df`) is **not a bibliography**; its “citations” are search-engine placeholders (`UIS+2`, `OECD+3`, `doi.org+4`, `hanushek.stanford.edu+2`, `World Bank+2`, `sciencedirect.com+2`, `ideas.repec.org+2`, `Princeton University Press+3`, `OUP Academic+3`, `doi.org+1`). Those tokens are **excluded** and appear nowhere as references. The register includes only inventory-attributed works that our corpus actually uses:

| inventory origin | register key | used/verified? |
|---|---|---|
| inventory-attributed | `becker_lewis_1973` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `biswal_1999` | PAYWALLED — NOT RETRIEVED (content described in Dang & Rogers 2008) — see row §1 |
| inventory-attributed | `callaway_santanna_2021` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `cragg_1971` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `cunha_heckman_2007` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `dang_2007` | PAYWALLED — NOT RETRIEVED — see row §1 |
| inventory-attributed | `dang_rogers_2008` | VERIFIED PRIMARY TEXT — see row §1 |
| inventory-attributed | `filmer_2020_lays` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `hanushek_1986` | BIBLIOGRAPHIC — AMBIGUOUS AS CITED (docs say only “Hanushek” without year/title; this is the standard candidate work) — see row §1 |
| inventory-attributed | `jayachandran_2014` | VERIFIED PRIMARY TEXT — see row §1 |
| inventory-attributed | `kim_lee_2010` | ABSTRACT-ONLY (full text paywalled) — see row §1 |
| inventory-attributed | `lucas_1988` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `mankiw_romer_weil_1992` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `psacharopoulos_patrinos_2018` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `sun_abraham_2021` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `tansel_bircan_2006` | VERIFIED PRIMARY TEXT (working-paper version; published version bibliographically verified) — see row §1 |
| inventory-attributed | `tobin_1958` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `todd_wolpin_2003` | VERIFIED BIBLIOGRAPHIC — see row §1 |
| inventory-attributed | `mincer_1974` | BOOK — BIBLIOGRAPHIC (not read) — see row §1 |
| inventory-attributed | `bray_1999` | VERIFIED BIBLIOGRAPHIC (peer-reviewed review record) — see row §1 |
| inventory-attributed | `bray_2009` | VERIFIED BIBLIOGRAPHIC (two peer-reviewed review records) — see row §1 |

Verification detail for the shadow-education family (full-text evidence, quoted formulae, corrections) is in `CITATION_VERIFICATION_SHADOW_ED.md`; this register does not duplicate that report.

## 6. Known citation defects reported, not fixed

1. `PAPER_D_EQUATION_AUDIT.md` and `MODEL_ZOO_*` previously carried no DOIs; they now end with a cross-reference section generated from this register.
2. The inventory has no equation-level citations; see `CITATION_VERIFICATION_SHADOW_ED.md` §3–§8 (Dang & Rogers DOI is `10.1093/wbro/lkn004`; Tansel & Bircan pages are `25(3):303–313`; the inventory’s “RCNi Company Limited” publisher for Becker & Lewis is false).
3. Benchmark moments (KR 2024 80.0 %, KR 2025 75.7 %, HK 2011/12 53.8 %/71.8 %, KR Q5−Q1 32.1 pp, 3.4×) have **no traceable primary source** in the tree (G2-A gate; G2A_CITATION_VERIFICATION.md); their register rows (`kedi_2024_2025`, `hk_shadow_survey_2011_12`) are marked UNVERIFIED and must not be cited as published numbers until sources are supplied.
4. “Hanushek” is cited without year/title in several docs; the register maps it to Hanushek (1986) JEL as the standard production-function work but flags the attribution as ambiguous — the docs must add the year/title before citation.
5. “Kaplan” in the model zoo is provisionally Bryan Caplan (2018) with tag V; register row `caplan_2018` is a book with no DOI and an unverified citation.

## 7. Reproduce / edit protocol

Any new citation added to our corpus must get a register row here first. For a journal article: resolve the DOI via `https://api.crossref.org/works/<DOI>` (fields: title, author, container-title, volume, issue, page, issued); click-through the DOI to a publisher/author PDF and record whether full text was read. For a book: record publisher + place + year + ISBN where the publisher/OpenLibrary record is reachable, else record **No DOI** and the publisher (do not invent an ISBN). For a report/dataset: record the issuing institution, programme URL, access restrictions, and version/date. Placeholder tokens (`site+2`, `doi.org+4`) are never acceptable citations.

### Corpus files scanned (63)

```
ABC_IDENTIFICATION_AUDIT.md
AUDIT_VERDICT.md
BOOTSTRAP_REPORT.md
CITATION_VERIFICATION_SHADOW_ED.md
CODE_CHANGES.md
COMPUTE_SCHEDULE.md
CONTEST_MATH_APPROX_ERROR.md
CONTEST_MATH_PERF.md
CONTEST_MATH_VALIDATION.md
CS_ESTIMATOR_NEWGEN.md
DASHBOARD.md
DHS_E1E8_MODEL_MAPPING.md
E8_BULGE_NEWGEN.md
ENGINE_CORE_AUDIT.md
ENGINE_INTERFACE_CONTRACT.md
ENGINE_MIDRUN_EVENTS.md
EXTERNAL_AUDIT_GPU_2026-11-25.md
FIRST_FAILURE_REPORT.md
FORECAST_NEWGEN.md
G2A_CITATION_VERIFICATION.md
G2A_IDENTIFIABILITY.md
G2A_IDENTIFIABILITY_MULTISEED.md
GATE0_REPORT.md
GATE0_VERIFICATION.md
GATE1_MIGRATION_TABLE.md
GATE1_POOL_HANG_INCIDENT.md
GATE1_REPORT.md
GATE2_PLAN.md
GATE2_PREREGISTRATION.md
GPU_ABC_AUDITOR_PACKET.md
GRID_X27_NOTE.md
LEAD_GROUND_TRUTH.md
LEAN_PROOF_STATUS.md
LEAN_VERIFICATION_SCOPE.md
LEMMA_LEDGER.md
LEMMA_LEDGER_AUDIT.md
MANUSCRIPT_ERRATA.md
MODEL_ZOO_DISCRIMINATORS.md
MODEL_ZOO_SCOPE.md
NEW_GENERATION_CAMPAIGN.md
PAPER_A_BASELINE_VS_NEWGEN_TEMPLATE.md
PAPER_A_REPRODUCTION_ATTEMPT.md
PAPER_A_VERIFICATION.md
PAPER_B_ADJUDICATION.md
PAPER_B_NEWGEN.md
PAPER_B_NEWGEN_2026-11-25.md
PAPER_B_TABLE_REGENERATION.md
PAPER_C_CONFIRMATORY_PREREG.md
PAPER_C_MODEL_GAP.md
PAPER_D_EQUATION_AUDIT.md
PILOT0_QA.md
PILOT0_RECORD.md
RUNNER_HARDENING.md
SCIENTIFIC_CLAIM_LEDGER.md
SYNTHETIC_DGP_VALIDATION.md
TEST_REPORT.md
TEST_REPORT_AFTER.md
TUTORING_AUDIT.md
TUTORING_CODEBOOK_VERIFICATION.md
TUTORING_DATA_INVENTORY.md
TUTORING_PHASE_B.md
Atlas.lean
LeanStarter.lean
```
