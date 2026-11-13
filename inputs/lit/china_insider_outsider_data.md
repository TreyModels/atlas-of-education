## Bottom line

- **Best microdata for a Tilly-style "categorical inequality" test on Chinese graduates' labour-market entry:** CFPS (2010–2022) and CGSS (2003–2023) are the only *open, free-registration* sources that carry **own party membership + own hukou + father's/mother's party membership + parents' work-unit type/ownership** in the same file. CLDS adds a usable **father's party** variable. CHIP gives party + ownership but weaker parent linkage. The graduate-specific surveys (**CCSS-Tsinghua, BCSPS, MyCOS**) have the best outcome measures (first-job wage, state-sector offer) but are **not open** (or not microdata at all).
- **Verified published estimates:** cadre/party-elite parent premium on graduate first-job wages = **15%** (Li, Meng, Shi & Wu 2012) and **4.46%** (Yu, Lin & Jiang 2019); **party membership has no significant direct effect on graduate starting salary** (Guo & Sun 2019); **rural hukou carries a *premium* of 6.2%**, i.e. no urban-hukou advantage among enrolled graduates (Wang, Cousineau, Boswell & Li 2024); party members and graduates with cadre parents are **more likely to get state-sector offers** (Li, Meng, Xiong & Cook 2024).
- **I could not find any 2010–2024 paper by "Wang & Moll" or "Zhang & Zhao"** on these premia. The likely intended papers are Wang/Cousineau/Boswell/Li (2024) and Li/Meng/Shi/Wu (2012) or Yu/Lin/Jiang (2019). Details in §4.

---

## 1. Microdata sources

Legend for variable columns: ✔ present, ◐ partial/derivable with caveats, ✘ absent.

| Source | Years / waves | Sample size | Access route | Own hukou | Own CCP | Parents' CCP | Parents' sector (state vs private) | Youth employment outcomes |
|---|---|---|---|---|---|---|---|---|
| **CFPS** (Peking U., ISSS) | 2010, 2012, 2014, 2016, 2018, 2020, 2022 (2022 released; 8th round fielded 2024) | baseline ~15,000 households, 25 provinces (~95% of pop.); 2022 round re-contacted ~20,000 households / ~75,000 individuals | Free registration at `isss.pku.edu.cn/cfps` data platform; mirrored at PKU Open Research Data, DOI **10.18170/DVN/45LCSO** | ✔ | ✔ (`party`; proxy Q N4001) | ✔ derived **`fparty`, `mparty`** | ◐ parent's own employer type available only if parent is a co-resident CFPS respondent (~38% fathers / 40% mothers); otherwise only parents' occupation text (ISCO/ISEI) | ✔ wages, employment, job history; graduates identifiable by age/education |
| **CGSS** (Renmin U.) | 2003–2023 annual/biennial | ~10,000–12,000 per wave (2023: **11,326 cases, 437 variables**) | Free registration, `cnsda.org` | ✔ (A14a series) | ✔ | ✔ father A89c, mother A90c | ✔ father A89g unit type (党政机关/企业/事业单位/社会团体/自雇/军队) and A89h ownership (国有/集体/私有/港澳台/外资); mother A90g/h | ◐ wage/occupation, but not graduate-specific cohorts |
| **CLDS** (Sun Yat-sen U.) | 2012, 2014, 2016, 2018 | 2014: 401 communities, 14,226 households, **23,594 individuals**; 2016: **21,086 individuals**, 29 provinces | Free registration at `css.sysu.edu.cn` (SYSU Social Science Survey Center) | ✔ | ✔ (`I1_6`) | ✔ (`fparty` used in published work) | ✔ own employer nature (机关事业单位/国企/民营/外资); parent sector via household roster | ✔ employment, wages, job mobility |
| **CHIP** (BNU / CIID) | 1988, 1995, 2002, 2007, 2013, 2018 (2023 in field) | 15,000–20,000 households per wave (urban/rural/migrant sub-samples from 2002) | Register + application at `chip.bnu.edu.cn`; older waves also via ICPSR | ✔ | ✔ | ◐ household roster + CHIP 2013 dedicated module on head's/spouse's parents | ✔ ownership/单位所有制 of own job; parent's occupation & ownership for matched parents | ✔ wages, employment |
| **BCSPS** (Renmin U. + CASER/NYU Shanghai) | 2009 baseline; 2010, 2011, 2012, 2013; wave 6 in 2024–25 | 5,100 sampled; 4,771 (2009); 4,426 / 4,271 / 4,043 / 2,603 follow-ups; 15 Beijing universities, 2006 & 2008 entry cohorts | Not open download; request via project team (CASER page lists contact; "secure data access early") | ✔ urban hukou pre-college | ✔ | ✔ ("family party member") | ◐ parental occupation/class measures; sector detail limited | ✔✔ school-to-work transition, first job, wages |
| **CCSS** (Tsinghua China Data Center graduate survey) | 2010–2015 annual (May–June, pre-graduation) | **40,911–40,916** graduating students, 90 colleges, 26 provinces | **No public access route found**; held by Tsinghua China Data Center / authors | ✔ pre-college hukou | ✔ | ✔ cadre parent, parental party membership, parental income/education | ✔ parental cadre/state background + state-sector offer | ✔✔ first-job wage, offer sector, job search |
| **MyCOS** (麦可思) | Annual since 2009 (2008–2025 cohorts) | e.g. 2025 cohort: ~195,000 bachelor + ~170,000 vocational respondents | **No microdata access**; results only in 就业蓝皮书 (Social Sciences Academic Press; 皮书数据库) | ✘ | ✘ | ✘ | ✘ | ✔ aggregate wages/employment rates only |

**Practical notes on the three "must-have" variables:**

- **CFPS** is the strongest for *both-generation* party membership: the CFPS methodology note ("CFPS小课堂 | 父母SES的综合变量") confirms `fparty/mparty/feduc/meduc/foccup*/moccup*` were constructed from the 2012 adult-questionnaire **V module** (V102–V104 father's education/occupation/political status at age 14; V201–V204 mother's) and merged into the 2010 family-roster release. Employer nature is asked as **QG2/PG25**: 1 政府部门/党政机关/人民团体, 2 事业单位, 3 国有企业, 4 私营企业/个体工商户, 5 外商/港澳台, …; plus **编制** (`GC2032`) — ideal for an SOE/government vs private split.
- **CGSS** is the cleanest for **father's sector at age 14** (unit type *and* ownership), which is exactly the "parent in state sector" regressor; caveat: the A89/A90 family-background block is **module-dependent** — verify per wave before pooling.
- **CLDS** is the only source where I found a published paper explicitly using **`fparty`** (father CCP member) as a constructed variable, alongside birth hukou, to define "system insider" status (2014 CLDS).

---

## 2. Published estimates (2010–2024)

| Study | Data | Key coefficient | Where | Read depth |
|---|---|---|---|---|
| **Li, Meng, Shi & Wu (2012)**, "Does having a cadre parent pay? Evidence from the first job offers of Chinese college graduates", *J. Development Economics* 99(2): 513–520. DOI **10.1016/j.jdeveco.2012.06.005** | CCSS (authors' own graduate survey), urban fresh graduates | **+15% first-job wage premium for having ≥1 cadre parent**; "remains as high as **14%** after controlling for CEE scores, college quality/major, all college human-capital attributes and job characteristics"; same for males and females | Abstract (p. 513); magnitude sequence in §1/introduction | **Abstract + introduction full text verified** (ScienceDirect abstract page). Table numbers/pages not retrieved. |
| **Yu, Lin & Jiang (2019)**, "Are cadre offspring in the fast lane? Evidence from the labour market for college graduates in China", *Applied Economics* 51(36). DOI **10.1080/00036846.2019.1584375** | Graduate labour-market survey ("a recent data set") | **+4.46% wage premium for cadre parent**; also advantages in **obtaining hukou**, entering high-level occupations, job satisfaction; guanxi/information channel | Abstract | **Abstract-only read** (T&F + SSRN abstract, 2 independent records agree). |
| **Guo & Sun (2019)**, "Re-examining economic returns to Communist Party membership in Mainland China", *J. Asia Pacific Economy* 24(1): 24–41. DOI **10.1080/13547860.2018.1490069** | CCSS 2010, college graduates | **Party membership has no direct (significant) effect on starting salaries**; but raises probability of graduate-school admission and of **obtaining permanent urban hukou** (partly via SOE entry); positive indirect effects via certificates, student leadership, GPA rank | Abstract | **Abstract-only read** (Ingenta/EBSCO), corroborated by Amighini et al. (2025) Table A1 entry: "Guo and Sun (2018) | CCSS 2010 | ATT | Not significant on entry wages". |
| **Wang, Cousineau, Boswell & Li (2024)**, "Estimating the Impact of Rural Hukou Status on Earnings for College Graduates in China", *The China Quarterly* 259: 677–695. DOI **10.1017/S0305741024000274** | CCSS 2010–2015, 90 colleges, **40,916** graduates | **Rural hukou = +6.2% first-job wage premium vs urban hukou**, significant at 1% (urban-hukou advantage = **zero/negative**, not positive). Also: +8.4% male premium; +4.6% if ≥1 parent has a college degree; ~0.55% per extra ¥10,000 parental income | **Table 4, column 3** (results section text explicitly attributes 6.2% to the column adding family SES) | **Full text verified** (OA). |
| **Li, Meng, Xiong & Cook (2024)**, "Job Preferences and Outcomes for China's College Graduates", *The China Quarterly* 258: 529–547. DOI **10.1017/S0305741023001510** | CCSS 2010–2015, 90 colleges, **40,911** graduates | Descriptive/logit: 63.8% prefer state sector; only 41.8% receive state-sector offers; **CCP membership, pre-college urban hukou, male, elite university, higher test scores, higher household income, college-educated parents, Party-cadre parents, social connections to the state sector → higher probability of a state-sector offer**. State-sector entry wages exceeded private by >12% in 2015 | Abstract + §"Student Job Offers"; regression table columns not retrievable | **Direction/significance verified via abstract & full text; exact coefficients NOT retrieved** (tables behind paywall/render truncation). |
| **Amighini, Fang & Zagler (2025)**, "On the evolution of the wage premium for party membership in China", *World Development* 188: 106909. DOI **10.1016/j.worlddev.2024.106909** | CHIP 1995, 2002, 2013, 2018 (urban + rural) | Party wage premium fell from **~50% (1995/2002) to ~30% (2013/2018)**; in 2013/2018 **10–15 pp (≈⅓ of the gap) is unexplained** = "pure discrimination"; premium now increasing in the wage distribution; contains **Table A1** summarising ~20 prior studies' party-premium estimates (incl. CHIP/CGSS/CCSS/CHES) | Abstract; §4 results; Table A1 | **Full text verified** (ScienceDirect HTML). Not graduate-specific — use as the aggregate benchmark. |
| **Li, Liu, Zhang & Ma (2007)**, "Economic returns to Communist Party membership: evidence from urban Chinese twins", *Economic Journal* 117(523): 1504–1520 | Urban Chinese twins | OLS party-member coefficient **≈0.100 (10%)**, but **≈0 once twin fixed effects absorb family background/ability** | Table 2 col. 2 and Table 4 (working-paper version) | **Working-paper read only** (Stanford King Center WP PDF). Journal DOI not verified — do not cite a DOI for this one without checking. |

---

## 3. Recommended design given the data

1. **Tilly-style categorical gap, two generations:** CFPS 2010→2022 or CGSS pooled. Define categories on `own CCP × own hukou × father's CCP × father's unit type (党政机关/事业单位/国企 vs 私营/自雇/外资)`, outcome = log hourly/monthly earnings of 22–35-year-olds, plus a graduate subsample (16+ years schooling). CFPS gives panel FE; CGSS gives the cleaner age-14 parental sector.
2. **Graduate entry premium:** the numbers to beat are Li et al.'s **15%** cadre-parent premium (elite/university graduate survey, 2008-ish cohort) versus Yu et al.'s **4.46%** (more recent, broader sample) — the discrepancy is itself a publishable question, and neither paper reports the *categorical* (state-insider vs outsider) gap you want.
3. **Note the sign surprise:** among *enrolled* graduates the urban-hukou premium is essentially **absent/negative** (Wang et al. 2024). Any insider/outsider story therefore has to operate through **access to college** and **sector allocation**, not through within-graduate wage gaps on hukou — which is exactly consistent with Li, Meng, Xiong & Cook's finding that party membership and cadre parentage buy **state-sector offers**, not higher pay.

---

## 4. Things I could NOT verify (do not treat as true)

- **"Wang & Moll"** and **"Zhang & Zhao"**: no such 2010–2024 paper on party/hukou/parental-sector graduate premia surfaced in any search. Likely candidates: Wang, Cousineau, Boswell & Li (2024) — hukou; or Wang, Nikolov & Acker (2019/2020, *Pacific Economic Review* 25(3): 309–338) — party premium 7.5% (PSM), but **not** graduate-specific and I did not fetch it. Please re-check the citation; I have not invented a substitute.
- Exact regression coefficients in Li, Meng, Xiong & Cook (2024) — I verified sign/significance from prose, not the table cells.
- Page numbers for the specific tables in Li, Meng, Shi & Wu (2012) and Yu, Lin & Jiang (2019).
- Whether **BCSPS** contains a direct "state/SOE vs private" employer-type question for parents (parental class is measured, but sector detail unconfirmed) — needs the BCSPS codebook.
- Whether **CFPS** waves after 2012 re-collect `fparty/mparty` (the derived variables are documented for the 2010 family roster using 2010 + 2012 information; later-wave updates not confirmed).
- **CCSS (Tsinghua)**: I found no public data-access procedure, only the survey description and the papers using it. Treat as restricted/collaborative access.

---

## Sources

**Verified by fetching:**
- https://www.sciencedirect.com/science/article/pii/S0305750X24003802 (Amighini, Fang & Zagler 2025, full text + Table A1 entries)
- https://www.cambridge.org/core/journals/china-quarterly/article/estimating-the-impact-of-rural-hukou-status-on-earnings-for-college-graduates-in-china/07B6CBEEDA5A7CB9D36722DCE728D85A (Wang et al. 2024, full text)
- https://www.cambridge.org/core/journals/china-quarterly/article/job-preferences-and-outcomes-for-chinas-college-graduates/61F29319F22E2DB8918A94ABD2361138 (Li, Meng, Xiong & Cook 2024)
- https://www.sciencedirect.com/science/article/abs/pii/S0304387812000508 (Li, Meng, Shi & Wu 2012, abstract + intro)
- https://www.isss.pku.edu.cn/cfps/cjwt/jtgxk/1201867cfps1356856.htm (CFPS 父母SES综合变量: `fparty/mparty`, 2012 V module)
- http://www.isss.pku.edu.cn/cfps/attachments/d1d05602314f4820b3a8c88e1e0a5935.pdf (CFPS 2012 questionnaire, V102–V204)
- http://www.isss.pku.edu.cn/cfps/docs/20230418165136294533.pdf (CFPS 2020 proxy questionnaire: `party`, employer type PG25)
- http://www.isss.pku.edu.cn/cfps/attachments/61d7e66d93084611932777481e6feac5.pdf (CFPS employer nature/编制 categories)
- https://www.cnsda.org/index.php/index.php?r=projects/view&id=11256439 (CGSS 2023: 11,326 cases, 437 vars)
- https://access.gesis.org/dbk/62532 and https://access.gesis.org/dbk/66554 (CGSS codebook: A14a hukou, A89c/A90c parents' party, A89g/h parents' unit type & ownership)
- https://bs.bnu.edu.cn/zgjmsrfpdcsjk/sjjs/ and https://bs.bnu.edu.cn/zgjmsrfpdcsjk/sjsq/ (CHIP waves, sample, `chip.bnu.edu.cn` application)
- https://www.isss.pku.edu.cn/docs/2025-06/20250605130803393137.pdf (CFPS 2022 data release conference report)
- https://caser.shanghai.nyu.edu/caser-projects/bcsps/ (BCSPS design, waves, access note)
- https://isg.sysu.edu.cn/article/254 (CLDS 2012/2014/2016, sample sizes, `css.sysu.edu.cn` registration)

**Search-result/abstract level only:**
- https://www.tandfonline.com/doi/abs/10.1080/00036846.2019.1584375 (Yu, Lin & Jiang 2019 abstract)
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3405455 (same, SSRN)
- https://www.ingentaconnect.com/content/routledg/rjap/2019/00000024/00000001/art00002 (Guo & Sun 2019 abstract)
- https://openurl.ebsco.com/EPDB%3Agcd%3A3%3A37908675/detailv2?sid=ebsco%3Aplink%3Aresult-item&id=ebsco%3Adoi%3A10.1080%2F13547860.2018.1490069 (Guo & Sun 2019 DOI/abstract record)
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1849485 (Li et al. 2012 SSRN version, DOI 10.2139/ssrn.1849485)
- https://kingcenter.stanford.edu/sites/g/files/sbiybj16611/files/media/file/280wp_0.pdf (Li, Liu, Zhang & Ma twins WP, Table 2/4 discussion)
- https://www.cambridge.org/core/services/aop-cambridge-core/content/view/07B6CBEEDA5A7CB9D36722DCE728D85A/S0305741024000274a.pdf/... (Wang et al. 2024 PDF — DOI + pagination 259:677–695 confirmed)
- https://cpk-front.mzk.cz/SummonRecord/... and https://www.cambridge.org/core/search?filters[authorTerms]=Yanyan+Xiong (Li, Meng, Xiong & Cook: CQ 258, 529–547, DOI 10.1017/S0305741023001510)
- https://www.sgpjbg.com/searchtag/26664632.html and https://baike.baidu.com/item/麦可思大学生就业报告 (MyCOS 2025-cohort sample sizes, report access via 皮书数据库)
- https://www.tandfonline.com/doi/pdf/10.1080/24761028.2019.1633987 (Yan 2019, CCP entry/premium over three CHIP waves — context only)
- https://www.atlantis-press.com/article/125959721.pdf and https://jjxdt.ajcass.com/... (CHIP 2013 individual variables incl. CCP member/cadre/ownership; CHIP 2013 parents module)
- https://qks.shufe.edu.cn/j/PDFFull/A4893936e-bb08-4009-88eb-fdc0625d0628.pdf (CLDS 2014 + `fparty` construction, 23,594 individuals)
- https://paper.njau.edu.cn/openfile?... (CLDS codebook: `I1_6` political status)
