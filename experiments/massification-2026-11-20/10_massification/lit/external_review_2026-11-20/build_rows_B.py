#!/usr/bin/env python3
# Build rows_B_absorption_credential.csv  (strands c and d)
# Every field written by hand from a document actually read in this session.
import csv, os

OUT = os.path.dirname(os.path.abspath(__file__))
COLS = ["row_id", "strand", "claim", "what_is_established_or_contested", "direction_or_sign",
        "reported_magnitude_verbatim", "source_authors", "source_year", "source_title",
        "venue", "url", "doi", "verification_status", "notes"]

R = []


def add(*a):
    assert len(a) == len(COLS) - 1, len(a)
    R.append(dict(zip([c for c in COLS if c != "row_id"], a)))


# ============================ STRAND C ============================
add("c",
    "Dual-economy ('unlimited supplies of labour') model: the modern/capitalist sector can draw labour from a subsistence sector at a constant subsistence wage, so expansion does not require rising wages; growth is the reinvested capitalist surplus, and the transfer of labour out of the subsistence sector IS the growth mechanism.",
    "ESTABLISHED as the canonical dual-economy frame and the reference point for all later structural/absorptive-capacity work (14,000+ citations in OpenAlex). CONTESTED only as an empirical description of contemporary labour markets (the 'Lewis turning point' debate), not as a formal model.",
    "+ expansion without wage pressure; + labour transfer as growth mechanism",
    "'converts itself into an economy where voluntary saving is running at about 12 to 15 per cent. of national income or more' -- Lewis's own statement of 'the central problem', i.e. the saving/investment share of national income (rising from 4-5 per cent).",
    "Lewis, W. Arthur", "1954", "Economic Development with Unlimited Supplies of Labour",
    "The Manchester School 22(2):139-191",
    "https://www.depfe.unam.mx/doctorado/teorias-crecimiento-desarrollo/lewis_1954.pdf",
    "10.1111/j.1467-9957.1954.tb00021.x", "VERIFIED-FULLTEXT",
    "Full text read (31-pp retyped PDF of the article, no page images; OCR artefacts such as 'hich' left as printed). Crossref/OpenAlex confirm venue/volume/pages. NOTE: the article contains no education-specific claim; schooling enters only inside 'capital' ('knowledge and skills with capital').")

add("c",
    "Rural-urban migration responds to the EXPECTED urban wage (the wage times the probability of finding a job), not the actual wage. Equilibrium therefore contains urban unemployment, and when the rate of job creation is below the rate of migration unemployment rises.",
    "ESTABLISHED as the canonical model of surplus labour WITH open unemployment; the expected-wage mechanism is textbook. Magnitudes are model-specific and contested.",
    "+ migration despite unemployment; ambiguous/negative sign of job creation on measured unemployment",
    "no magnitude seen",
    "Harris, John R.; Todaro, Michael P.", "1970",
    "Migration, Unemployment and Development: A Two-Sector Analysis",
    "American Economic Review 60(1):126-142",
    "https://www.aeaweb.org/aer/top20/60.1.126-142.pdf",
    "none (AER 1970 has no DOI)",
    "VERIFIED-FULLTEXT",
    "Full text read (AEA top-20 archive PDF, 17pp). Verbatim mechanism: 'rural-urban migration will continue so long as the expected urban real income at the margin exceeds real agricultural product'; and 'expected and actual earnings will converge to a positive number even though the rate of job creation is less than the rate of migration so that unemployment is increasing'. This is the theoretical bridge from Lewis to educated-unemployment queues.")

add("c",
    "Schooling raises an economy's capacity to adopt and diffuse new technology, so the return to education rises with the rate of technological progress: human capital and technology are complements in TFP growth, not substitutes.",
    "Standard citation in the human-capital-and-diffusion literature. NOT verified in this session.",
    "+ (education x technology interaction)",
    "no magnitude seen",
    "Nelson, Richard R.; Phelps, Edmund S.", "1966",
    "Investment in Humans, Technological Diffusion, and Economic Growth",
    "American Economic Review 56(1/2):69-75",
    "NONE-OPENED",
    "none (AER 1966 has no DOI)",
    "UNVERIFIED",
    "PLACEHOLDER -- DO NOT CITE YET. Bibliographic record located in OpenAlex/Crossref searches, but NO page of this article was opened: AER pre-1999 is paywalled (JSTOR), no open copy was located, and web_fetch is non-functional in this environment (every hostname resolves to a non-routable address). The claim above is the standard secondary characterisation only; it must be checked against pp.69-75 before use.")

add("c",
    "Convergence is conditional on 'social capability' (and technological congruence): a lagging country catches up only if it can absorb and exploit the leader's technology; leaders can 'forge ahead' and the ranking can reshuffle. Productivity growth varies inversely with level only WITHIN the group able to absorb.",
    "ESTABLISHED as the origin of the absorptive-capacity / social-capability qualification to convergence; this is what killed the strong unconditional-convergence claim (Barro-style convergence is conditional on exactly these variables).",
    "+ for absorbers; 0 or - for non-absorbers (club convergence)",
    "no magnitude seen",
    "Abramovitz, Moses", "1986", "Catching Up, Forging Ahead, and Falling Behind",
    "The Journal of Economic History 46(2):385-406",
    "https://api.crossref.org/works/10.1017/S0022050700046209",
    "10.1017/S0022050700046209", "VERIFIED-ABSTRACT",
    "Abstract read from the Crossref deposit for the DOI (publisher-supplied text). Article body NOT read. The abstract states convergence 'showed marked strength only during the first quarter-century following World War II' -- i.e. the effect is period-dependent, which is the programme-relevant point.")

add("c",
    "Structural change = the reallocation of labour across sectors with different productivity levels. It is driven by industry-level technological change plus demand and trade, and produces regionally distinct patterns; it is the central object of development economics.",
    "ESTABLISHED as the standard definitional and measurement frame (Groningen/GGDC). The developmental PAYOFF of structural change is contested -- see McMillan & Rodrik and Rodrik rows.",
    "+ when labour moves to higher-productivity sectors; sign is empirical, not theoretical",
    "no magnitude seen",
    "Timmer, Marcel P.; de Vries, Gaaitzen J.; de Vries, Klaas", "2015",
    "Patterns of Structural Change in Developing Countries",
    "Routledge Handbook of Industry and Development, ch. 5, pp. 79-97 (working-paper version: GGDC Research Memorandum 149, 2014)",
    "https://research.rug.nl/en/publications/86407a2f-5d6e-4ace-9899-27c9bdf6baf2",
    "10.4324/9780203387061-11", "VERIFIED-ABSTRACT",
    "Abstract read on the University of Groningen research portal. Chapter PDF not retrieved (Routledge paywall); GGDC RM 149 not located. PAGINATION CAUTION: Crossref gives pp. 79-97 for this DOI while the Groningen portal record showed first page 65 -- check the printed chapter before citing a page. Do not quote numbers from this chapter on my authority.")

add("c",
    "Labour flows from low- to high-productivity activities are a key driver of development, but the payoff is not automatic: since 1990 structural change has been growth-REDUCING in Africa and Latin America and growth-enhancing in Asia, and differences in the pattern of structural change account for the bulk of the Asia-vs-rest productivity difference.",
    "ESTABLISHED and widely replicated: the growth payoff to structural change can be negative. CONTESTED how much of the Latin American/African result is measurement (informal-sector deflators, self-employment).",
    "+ in Asia; - in Latin America and Africa (1990-2005)",
    "'the rise in unemployment between 1990 and 2005 worsens the structural change term by an additional 0.2 percentage points' -- effect on the within/between decomposition of labour-productivity growth (p.16, note 6).",
    "McMillan, Margaret S.; Rodrik, Dani", "2011",
    "Globalization, Structural Change and Productivity Growth",
    "NBER Working Paper 17143 (prepared for a joint ILO-WTO volume)",
    "https://www.nber.org/system/files/working_papers/w17143/w17143.pdf",
    "10.3386/w17143", "VERIFIED-FULLTEXT",
    "NBER WP full text read (54pp); the UNU-WIDER version (wp2011-056) was also downloaded and read in part. Published version is in a joint ILO-WTO volume, not verified here.")

add("c",
    "Premature deindustrialization: the hump-shaped relationship between industrialization (employment or output shares) and income has shifted downwards and toward the origin, so countries run out of industrialization opportunities sooner and at much lower income levels than the early industrializers. Asia and manufactures exporters were largely insulated; Latin America was hit hardest.",
    "ESTABLISHED as an empirical pattern in manufacturing EMPLOYMENT shares. CONTESTED as a welfare claim (services may substitute) and on measurement (manufacturing output shares at constant prices deindustrialize far less).",
    "- manufacturing employment share at a given income; timing earlier",
    "no magnitude seen (paper reports figures, not a single headline effect size)",
    "Rodrik, Dani", "2015", "Premature Deindustrialization",
    "NBER Working Paper 20935",
    "https://www.nber.org/system/files/working_papers/w20935/w20935.pdf",
    "10.3386/w20935", "VERIFIED-FULLTEXT",
    "NBER WP full text read (50pp). Deliberately reports 'no magnitude seen': the paper's magnitudes are figure-based (peak employment share vs. log income), and I did not extract a defensible single number.")

add("c",
    "Cross-country technology differences are SKILL-BIASED: rich (skill-abundant) countries use skilled labour more efficiently and unskilled labour relatively (possibly absolutely) less efficiently, because they choose technologies suited to their skill endowment. Identical schooling therefore has a different productivity value depending on development level.",
    "ESTABLISHED as the appropriate-technology / directed-technology family. CONTESTED: the authors themselves list capital-skill complementarity and schooling-quality differences as alternatives they cannot reject.",
    "+ for skilled labour in rich countries; - (relative) for unskilled labour in rich countries",
    "no magnitude seen",
    "Caselli, Francesco; Coleman, Wilbur John II", "2006", "The World Technology Frontier",
    "American Economic Review 96(3):499-522",
    "http://personal.lse.ac.uk/casellif/papers/wtf.pdf",
    "10.1257/aer.96.3.499", "VERIFIED-FULLTEXT",
    "Author's LSE copy of the published AER article read (24pp). This is the cleanest formal statement that the return to a given qualification is conditional on the technology in use -- i.e. an absorptive-capacity claim at the technology level.")

add("c",
    "The growth effect of human capital is conditional on DISTANCE TO THE TECHNOLOGY FRONTIER: tertiary (high-skill) human capital raises growth only near the frontier, while primary/secondary schooling matters further behind. An explicit threshold/non-linearity claim about which kind of education pays when.",
    "Widely cited as THE formalisation of the threshold claim; the replication record is mixed and the result is sensitive to how 'distance to frontier' is measured.",
    "+ tertiary near frontier; + primary/secondary far from frontier",
    "no magnitude seen",
    "Vandenbussche, Jerome; Aghion, Philippe; Meghir, Costas", "2006",
    "Growth, distance to frontier and composition of human capital",
    "Journal of Economic Growth 11(2):97-127",
    "NONE-OPENED",
    "10.1007/s10887-006-9002-y", "UNVERIFIED",
    "PLACEHOLDER -- DO NOT CITE. Both open copies were blocked: Harvard DASH returned HTTP 429 on three attempts and the IFS WP 0431 URL 404s. Bibliographic record verified via Crossref only. The threshold claim above is the standard characterisation; the sign/strength must be read off the paper before use.")

add("c",
    "Human capital contributes to growth mainly through TFP and technology diffusion rather than as a direct factor of production; in direct specifications the education-growth link is weak or absent, while education matters for the Solow residual.",
    "Influential but CONTESTED; the specification (levels vs. changes, enrolment vs. attainment, quality) drives the result.",
    "0 direct; + via TFP/diffusion",
    "no magnitude seen",
    "Benhabib, Jess; Spiegel, Mark M.", "1994",
    "The role of human capital in economic development: evidence from aggregate cross-country data",
    "Journal of Monetary Economics 34(2):143-173",
    "NONE-OPENED",
    "10.1016/0304-3932(94)90047-7", "UNVERIFIED",
    "PLACEHOLDER -- DO NOT CITE. No open copy located; Elsevier paywall. Bibliographic record verified via Crossref only (no abstract in the Crossref deposit either). The claim above is the standard characterisation from surveys.")

add("c",
    "Cross-nationally, increases in the human-capital stock from rising educational attainment are NOT associated with the growth rate of output per worker; the association of education growth with conventional TFP measures is large, significant and NEGATIVE. 'Where has all the education gone?'",
    "A landmark NEGATIVE result and the standard citation for 'expansion without growth'. CONTESTED on measurement (attainment vs. years, quality, endogeneity) -- see Krueger & Lindahl.",
    "0 for output per worker; - for TFP",
    "'Cross-national data show no association between increases in human capital attributable to the rising educational attainment of the labor force and the rate of growth of output per worker.' (abstract, verbatim; a cross-country association, not a point estimate).",
    "Pritchett, Lant", "2001", "Where Has All the Education Gone?",
    "The World Bank Economic Review 15(3):367-391",
    "https://api.openalex.org/works/doi:10.1093/wber/15.3.367",
    "10.1093/wber/15.3.367", "VERIFIED-ABSTRACT",
    "Abstract read via the OpenAlex API (publisher-deposited text). Full text NOT retrieved: the OpenKnowledge bitstream link returns a 2.4 KB HTML gate, not a PDF. The abstract also flags that the results are 'on average' results, which is the opening for the heterogeneity literature.")

add("c",
    "Macro growth regressions and micro Mincer returns diverge, and the divergence is informative: in the macro literature the INITIAL STOCK of human capital matters, not its change; secondary and post-secondary education matter more for growth than primary; female education is insignificant and sometimes negative.",
    "ESTABLISHED as the standard reconciliation of the macro-micro puzzle; the specification sensitivity it documents is itself the central caution for anyone running a growth regression with education.",
    "+ for the initial stock; level-dependent (secondary/tertiary > primary)",
    "no magnitude seen",
    "Krueger, Alan B.; Lindahl, Mikael", "2001", "Education for Growth: Why and for Whom?",
    "Journal of Economic Literature 39(4):1101-1136 (NBER WP 7591)",
    "https://www.nber.org/system/files/working_papers/w7591/w7591.pdf",
    "10.1257/jel.39.4.1101", "VERIFIED-FULLTEXT",
    "NBER WP 7591 read (65pp); published JEL version DOI verified via Crossref. Key sentences quoted in the claim field. This is the paper to cite for 'the return depends on WHICH level and WHOSE education'.")

add("c",
    "Global private return to an extra year of schooling averages about 9 per cent; private returns to HIGHER education have increased (raising financing and equity issues); social returns remain high; women have higher average returns than men.",
    "ESTABLISHED as the standard global benchmark (1,120 estimates, 139 countries, 1950-2014). CONTESTED for relying on Mincerian estimates that assume exogenous schooling and that mix methods across studies.",
    "+ (positive, ~9% per year of schooling)",
    "'The private average global return to a year of schooling is 9 percent a year.' -- average Mincerian private return across 1,120 estimates in 139 countries, 1950-2014.",
    "Psacharopoulos, George; Patrinos, Harry Anthony", "2018",
    "Returns to investment in education: a decennial review of the global literature",
    "Education Economics 26(5):445-458 (World Bank Policy Research WP 8402)",
    "https://api.openalex.org/works/doi:10.1596/1813-9450-8402",
    "10.1080/09645292.2018.1484426", "VERIFIED-ABSTRACT",
    "Abstract read via OpenAlex (WB working-paper record). IMPORTANT LIMIT: I did NOT read the by-income-level table, so do NOT attribute a 'poor countries get more' gradient to this paper on my reading -- the abstract does not state it.")

add("c",
    "Fast-growing economies downshift as they approach upper-middle income: growth slows by at least 2 percentage points when per-capita income reaches around $17,000 (2005 constant international prices). This is the empirical core of the 'middle-income trap' timing claim.",
    "ESTABLISHED as a robust descriptive regularity across post-1957 data. CONTESTED as a 'trap': regression to the mean and case selection can generate the same pattern (the Pritchett-Summers 'Asiaphoria' critique), and the threshold is not stable across specifications.",
    "- at the threshold; level-dependent",
    "'the growth rate downshifts by at least 2 percentage points, when their per capita incomes reach around $17,000 US in year-2005 constant international prices' -- the slowdown threshold in per-capita income.",
    "Eichengreen, Barry; Park, Donghyun; Shin, Kwanho", "2012",
    "When Fast-Growing Economies Slow Down: International Evidence and Implications for China",
    "Asian Economic Papers 11(1):42-87 (NBER WP 16919)",
    "https://www.nber.org/system/files/working_papers/w16919/w16919.pdf",
    "10.1162/asep_a_00118", "VERIFIED-FULLTEXT",
    "NBER WP 16919 read (50pp). Note the sample starts 1957 and the paper is explicit that this is a conditional regularity, not a law.")

add("c",
    "Computerisation substitutes for labour in ROUTINE cognitive and manual tasks and complements labour in NON-ROUTINE analytic, interactive and manual tasks, shifting relative demand against the routine middle. This is the microfoundation for skills-technology complementarity and for mismatch between schooling and job content.",
    "ESTABLISHED (the task framework is now standard in labour economics). CONTESTED in magnitude, and in developing-country generality: the task measures are US 1960 Dictionary of Occupational Titles scores.",
    "+ non-routine; - routine",
    "'by 1997, these industries would be 19 percentage points apart in the distribution of computer adoption - approximately 13 percentage points apart in on-the-job computer use' -- a MODEL-IMPLIED separation between industries one standard deviation apart in routine-task intensity (pp.13-14), NOT an estimated causal effect.",
    "Autor, David H.; Levy, Frank; Murnane, Richard J.", "2003",
    "The Skill Content of Recent Technological Change: An Empirical Exploration",
    "Quarterly Journal of Economics 118(4):1279-1333",
    "http://www.frbsf.org/economics/conferences/0311/alm-skillcontent-qje.pdf",
    "10.1162/003355303322552801", "VERIFIED-FULLTEXT",
    "Read from the FRBSF conference PDF of the QJE version (56pp, pre-publication pagination). The NBER WP 8337 copy has an unreadable text layer (custom font encoding) -- use this URL, not the NBER one.")

add("c",
    "Technology-skill complementarity is historically contingent, not a universal: it EMERGED in US manufacturing as batch and continuous-process methods spread and electrification replaced steam/water power (1909-1929); industries using more capital per worker employed relatively more educated blue-collar workers and paid them more.",
    "ESTABLISHED and foundational for the 'race between education and technology' frame. CONTESTED whether the mechanism generalises to service economies and to late industrialisers.",
    "+ (education x technology complementarity), period- and sector-specific",
    "no magnitude seen",
    "Goldin, Claudia; Katz, Lawrence F.", "1998", "The Origins of Technology-Skill Complementarity",
    "Quarterly Journal of Economics 113(3):693-732 (NBER WP 5657)",
    "https://www.nber.org/system/files/working_papers/w5657/w5657.pdf",
    "10.1162/003355398555720", "VERIFIED-FULLTEXT",
    "NBER WP 5657 read (40pp). The point for the programme: complementarity is an outcome of a particular production regime, so its absence in a different regime is not an anomaly.")

# ============================ STRAND D ============================
add("d",
    "The 'overeducated American': after about 1969 the economic payoff to a bachelor's degree fell sharply as graduate supply outran demand, producing overeducation and the downgrading of graduates into jobs below their qualification.",
    "Landmark diagnosis that created the field. Its TIMING and interpretation are contested: later work reads the 1970s as a transient episode of the technology-skill race rather than a permanent oversupply regime.",
    "- college wage premium (1970s)",
    "no magnitude seen",
    "Freeman, Richard B.", "1976", "The Overeducated American",
    "Academic Press (New York)",
    "https://openlibrary.org/search.json?q=The+Overeducated+American+Freeman",
    "none (monograph)",
    "UNVERIFIED",
    "PLACEHOLDER -- DO NOT CITE NUMBERS. Book text NOT read. OpenLibrary search record confirms author/title/1976 (work OL1953834W). The claim is the standard secondary characterisation; any page reference or percentage must come from the book or a review of it. The modern, verifiable magnitudes for the same phenomenon are in the Leuven & Oosterbeek and World Bank rows.")

add("d",
    "The Credential Society: schooling expands mainly to allocate access to elite occupations and status groups rather than to raise productivity; credential requirements ratchet upward as supply grows, so expansion is self-defeating as a distributional strategy.",
    "ESTABLISHED as the canonical conflict/closure account of credential inflation, and the standing rival to human-capital accounts. CONTESTED empirically: hard to distinguish from signalling and from genuine skill demand.",
    "+ credentials, - productivity value of each credential",
    "no magnitude seen",
    "Collins, Randall", "1979", "The Credential Society: An Historical Sociology of Education and Stratification",
    "Academic Press (New York)",
    "https://openlibrary.org/search.json?q=The+Credential+Society+Collins",
    "none (monograph)",
    "UNVERIFIED",
    "PLACEHOLDER -- DO NOT CITE NUMBERS. Book text NOT read. OpenLibrary record confirms Collins/1979 (work OL28946W); a later edition carries a foreword by Tressie McMillan Cottom and Mitchell L. Stevens. Claim is the standard characterisation.")

add("d",
    "Higher education as a FILTER: schooling may certify pre-existing ability rather than create it, so the social return to education can fall below the private return -- the filter critique of human capital accounting.",
    "ESTABLISHED as the canonical statement of the filter/screening alternative. CONTESTED: the empirically relevant question is the SIZE of the sheepskin/signal component, not its existence.",
    "+ private return; social return < private return",
    "no magnitude seen",
    "Arrow, Kenneth J.", "1973", "Higher education as a filter",
    "Journal of Public Economics 2(3):193-216",
    "https://api.crossref.org/works/10.1016/0047-2727(73)90013-3",
    "10.1016/0047-2727(73)90013-3", "UNVERIFIED",
    "PLACEHOLDER -- DO NOT CITE. Crossref record opened (venue/volume/pages confirmed) but the deposit carries NO abstract, and the ScienceDirect full text is paywalled. The claim above is the standard characterisation; it must be checked against the article.")

add("d",
    "Job market signalling: under hiring uncertainty, education can carry information about unobserved ability, so equilibria exist in which schooling raises a worker's wage without raising that worker's productivity. Private and social returns to schooling diverge by construction.",
    "ESTABLISHED as the foundational signalling model (the most-cited warrant for credential/queue arguments about massification). CONTESTED only in magnitude and in how much of the return is signal versus skill.",
    "+ private wage; 0 or + (ambiguous) social product",
    "no magnitude seen",
    "Spence, Michael", "1973", "Job Market Signaling",
    "Quarterly Journal of Economics 87(3):355-374",
    "https://api.crossref.org/works/10.2307/1882010",
    "10.2307/1882010", "VERIFIED-ABSTRACT",
    "CAVEAT: the Crossref 'abstract' for this DOI is the article's TABLE OF CONTENTS (sections: hiring as investment under uncertainty; applicant signaling; informational feedback and the definition of equilibrium; properties of informational equilibria). So bibliographic identity and section structure are verified, but the substantive argument was NOT read. Treat as metadata-level verification only.")

add("d",
    "Job competition model: workers compete for JOBS, not for wages; wages attach to jobs, employers rank applicants by expected trainability, and education is used to order the queue. More education therefore redistributes queue positions rather than raising output -- the sharpest statement of credential inflation.",
    "ESTABLISHED as the third canonical model (alongside human capital and signalling). CONTESTED: Leuven & Oosterbeek show that pure job competition (zero return to surplus schooling) is rejected by the data.",
    "+ education as queue position; 0 output effect",
    "no magnitude seen",
    "Thurow, Lester C.", "1975", "Generating Inequality: Mechanisms of Distribution in the U.S. Economy",
    "Basic Books (New York)",
    "NONE-OPENED",
    "none (monograph)",
    "UNVERIFIED",
    "PLACEHOLDER -- DO NOT CITE. No accessible copy; the model is also set out in Thurow (1972) 'Education and Economic Equality', The Public Interest, which was likewise not read this session. Claim is the standard characterisation.")

add("d",
    "Overeducation/mismatch is measurable in three standard ways (job analysis, worker self-assessment, realised matches). Returns to SURPLUS schooling are far below returns to REQUIRED schooling, which rejects both the pure human-capital prediction (equal returns) and the pure job-competition prediction (zero returns); overeducation carries a wage penalty and is only partly persistent.",
    "ESTABLISHED as the standard survey of the field and the best single methodological reference. CONTESTED: the measurement method drives incidence estimates, so cross-country 'share overeducated' figures are not comparable.",
    "+ required schooling; small + surplus; surplus << required",
    "'the returns to surplus and deficit schooling are very low in absolute value and represent only around 45% of the returns to required schooling' (Leuven & Oosterbeek quoting McGuinness 2007, p.147 -- ratio of the surplus-education return to the required-education return).",
    "Leuven, Edwin; Oosterbeek, Hessel", "2011", "Overeducation and Mismatch in the Labor Market",
    "Handbook of the Economics of Education, vol. 4, ch. 3 (IZA Discussion Paper 5523)",
    "https://docs.iza.org/dp5523.pdf",
    "10.1016/b978-0-444-53444-6.00003-1", "VERIFIED-FULLTEXT",
    "IZA DP 5523 full text read (56pp). The paper reviews Freeman's overschooling diagnosis directly, which makes it the correct modern bridge back to the 1976 book.")

add("d",
    "Survey of overeducation: incidence estimates vary widely with measurement; overeducated workers earn less than adequately-matched workers with the same schooling; the phenomenon is assessed against human capital theory, assignment theory and job competition, and none fits cleanly.",
    "ESTABLISHED as a survey of measurement controversy (this is the paper to cite for 'the numbers are not comparable across studies'). CONTESTED: the theory that best explains overeducation.",
    "- earnings for overeducated at given schooling",
    "no magnitude seen",
    "McGuinness, Seamus", "2006", "Overeducation in the Labour Market",
    "Journal of Economic Surveys 20(3):387-418",
    "https://api.openalex.org/works/doi:10.1111/j.0950-0804.2006.00284.x",
    "10.1111/j.0950-0804.2006.00284.x", "VERIFIED-ABSTRACT",
    "Abstract read via OpenAlex (publisher-deposited). Full text paywalled (Wiley). The abstract gives no numbers, hence 'no magnitude seen'.")

add("d",
    "Philippines: vertical mismatch is large -- about one in five tertiary-educated workers holds a job that mainly requires basic skills -- and horizontal mismatch is reported as the norm. Professional licences pay a premium ONLY when education and occupation credentials align; labour-market experience and structural mismatch matter more for pay than school characteristics.",
    "ESTABLISHED (for the Philippines, on 2021-2022 PRC/LFS-type data): mismatch, not schooling quantity, is what governs the graduate pay premium. CONTESTED: the horizontal-mismatch figure is imported (see notes).",
    "+ for matched and licensed; - for mismatched",
    "'one in five workers with tertiary education credentials engaged in occupations that primarily require basic skills (Bayudan-Dacuycuy and Dacuycuy 2021)' -- vertical mismatch; and 'around seven in 10 graduates not employable in their chosen occupation due to inadequate skills (Aspiring Minds 2017)' -- horizontal mismatch.",
    "Bayudan-Dacuycuy, Connie G.; Vargas, Anna Rita P.; Luzon, Paola Ellaine D.", "2025",
    "Returns to Professional Licenses and Education-Occupation (Mis)matching",
    "Philippine Institute for Development Studies, Discussion Paper Series No. 2025-32 (November 2025), 21pp",
    "https://pidswebs.pids.gov.ph/CDN/document/pidsdps2532.pdf",
    "none (PIDS DP)",
    "VERIFIED-FULLTEXT",
    "Full text read. CAUTION on the second statistic: the 'seven in 10' horizontal-mismatch figure is cited BY the PIDS authors to Aspiring Minds (2017), an India-based employability assessment -- it is NOT a Philippines measurement. Use the one-in-five vertical-mismatch figure for the Philippines and treat seven-in-ten as imported. Study supported by EDCOM II.")

add("d",
    "Philippines: the graduate labour market has turned. The college wage premium has fallen and real wages for college graduates were flat while wages for workers below secondary level rose by nearly 50 per cent; college graduates in their twenties face the HIGHEST unemployment of any group; more than a third of workers hold more education than their jobs require.",
    "ESTABLISHED (World Bank, on PSA/LFS data to 2025): expansion has not been matched by graduate-appropriate job growth, and the return has shifted toward the bottom of the distribution. The authors themselves read the graduate unemployment as partly reservation wages, partly skills mismatch -- i.e. the mechanism is CONTESTED.",
    "- graduate wage growth; + overeducation; + graduate youth unemployment",
    "'More than a third of workers (39 percent) have more education than their jobs require and receive only modest returns on their extra schooling.'; 'wages for workers with less than secondary education grew by nearly 50 percent, real wages for college graduates were flat'; 'college graduates in their twenties face higher unemployment rates than any other group'.",
    "World Bank", "2026",
    "Building the Filipino Middle Class: Towards Resilient Futures and Poverty Eradication (Philippines Poverty and Equity Assessment)",
    "World Bank, Washington DC (115pp)",
    "https://openknowledge.worldbank.org/server/api/core/bitstreams/1e48613c-2045-441f-aa91-b9f92484b91b/content",
    "none located",
    "VERIFIED-FULLTEXT",
    "Full text read (115pp). This is the single most directly useful document for the programme's demand-absorption test in the anchor country. Retrieved via the OpenKnowledge server API; the openknowledge /download and documents1.worldbank.org routes are blocked in this environment.")

add("d",
    "Philippines youth labour market: youth are a large and still-growing share of the working-age population; about 7.1 million youth are employed; 21 per cent of working youth live in moderate or extreme poverty; the gender gap in youth labour-force participation is 16.8 percentage points.",
    "ESTABLISHED as official ILO modelled estimates (Nov 2019) for the pre-pandemic baseline; the levels are dated, the structure is not.",
    "+ employment; + working poverty among youth",
    "'Around 7.1 million young women and men are employed. Among working youth, 21% live in moderate or extreme poverty.' and 'gender gaps in labour force participation remain at 16.8 percentage points.'",
    "International Labour Organization", "2020",
    "Decent work and youth in the Philippines: Facts and trends (country fact sheet, January 2020)",
    "ILO Country Office for the Philippines, Manila (2pp; ILOSTAT modelled estimates, November 2019)",
    "https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@asia/@ro-bangkok/@ilo-manila/documents/publication/wcms_742036.pdf",
    "none (fact sheet)",
    "VERIFIED-FULLTEXT",
    "Full text read (2pp). Small document: it gives the youth baseline but NOT unemployment by educational attainment -- the Philippines-specific breakdown by education has to come from the World Bank assessment or PSA (psa.gov.ph returns HTTP 403 here).")

add("d",
    "Philippine IT-BPM (BPO) capacity: the sector is the country's main employer of tertiary-educated labour at scale -- on track to about 1.9 million jobs and US$40 billion in export revenue, more than 8 per cent of GDP, adding around 80,000 jobs in 2025 at 4 per cent employment growth.",
    "ESTABLISHED as IBPAP's own industry accounting (reported January 2026). CONTESTED as an absorption solution: the sector's growth rate (4% employment) is now below the growth rate of tertiary graduates, and it is exposed to AI/automation and to US demand.",
    "+ jobs for graduates; but +80k/yr vs. a much larger graduate flow",
    "'on track to reach 1.9 million jobs and $40 billion in export revenues, adding around 80,000 jobs and $2 billion in revenues in 2025'; 'Employment growth reached 4 percent, while revenue growth stood at 5 percent'; 'more than 8 percent of the country's gross domestic product'.",
    "IBPAP (Industry association), reported by Ayeng, Raffy (Daily Tribune)", "2026",
    "IT-BPM sector posts strong growth in 2025, eyes nearly 2M jobs",
    "Daily Tribune (Philippines), 1 January 2026",
    "https://tribune.net.ph/2026/01/01/it-bpm-sector-posts-strong-growth-in-2025-eyes-nearly-2m-jobs",
    "none (news report)",
    "VERIFIED-FULLTEXT",
    "VERIFIED AS A NEWS REPORT quoting IBPAP's official 2025 report -- the primary IBPAP report was NOT opened (ibpap.org is a JS app; admin.ibpap.org/api/v1 exists but was not queried). Attribute to IBPAP-via-Daily-Tribune, not to a peer-reviewed source.")

path = os.path.join(OUT, "rows_B_absorption_credential.csv")
with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL)
    w.writeheader()
    for i, r in enumerate(R, 1):
        r["row_id"] = "B%02d" % i
        w.writerow({k: r[k] for k in COLS})
print("wrote", path, len(R), "rows")
