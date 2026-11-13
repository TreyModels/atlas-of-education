# What happened to jobs in China, 2018–2026: the stories and the evidence

Research note, 5 November 2026. It feeds the story tournament (`engine/firms/stories.py`). Every number has a source at the end. Numbers I could not verify are marked.

## The headline facts the stories must explain

| Fact | Value | Source |
|---|---|---|
| Overall urban surveyed unemployment | 5.6% (2020), 5.1% (2021), 5.6% (2022), 5.2% (2023), 5.1% (2024); about 5.2% in 2025–26 | IMF Article IV 2026; NBS |
| Prime-age (25–59) unemployment | peaked 5.6% Feb 2020, near pre-pandemic by end-2022 | ADB brief 247 |
| Youth (16–24) unemployment | 11.9% (2019) → 17.6% (2022 avg, old method); new method 14.9–18.9% (2024–26), 16.5% Dec 2025 | ADB; NBS; IMF |
| College graduating class | 7.0m (2012) → 10.76m (2022) → 12.22m (2025) → 12.70m (2026) | MoE; ADB |
| Graduate job postings, H1 2025 | −22% y/y; job seekers +8% | Caixin, 19 Sep 2025 |
| Nominal non-private wage growth | 2.8% in 2024 | IMF 2026 |
| Graduate starting pay relative to the average wage | 0.75 (class of 2018) → 0.60 (class of 2023) | MyCOS; NBS (see `data_china.py`) |
| Tertiary-sector job creation | 9.1m (2018), 6.5m (2019), 2.5m (2020), 0.6m (2021) | ADB brief 247 |
| NEET rate, ages 16–34 | 11.5% (2018) → 16.1% (2022) | Caixin, citing research |

The puzzle to explain: unemployment rose for youth but not for adults, and it stayed high after COVID ended. Graduate pay fell relative to everyone else, and graduate postings fell while applicants rose.

## The stories

### 1. Cyclical demand and COVID (the ADB view)

Lockdowns hit face-to-face services. In 2020, 42.5% of employed 16–19-year-olds and 34.9% of 20–24-year-olds worked in consumer services. Youth work in private firms is concentrated 20 points above prime-age workers, and private hiring is more procyclical. ADB concludes that weak activity is "likely the main reason" for the 2019–22 rise.

**Predicts:** a rise in 2020–22 and a fall once demand recovers. The adult rate moves too, but less.
**Problem:** youth unemployment did not fall after 2023, while the adult rate returned to about 5%. This story explains the start, not the persistence.

### 2. The property collapse

Housing investment fell from 12.3% of GDP (2020) to 6.1% (2025). Completions are almost 40% below 2021, and over half of developers remain distressed (IMF 2026). Real estate was the only industry where average wages fell in 2022 (NBS). Construction and services hold most of the labour slack (IMF, employment PMIs). The NBS series on construction headcount was not reachable here.

**Predicts:** a lasting fall in demand, concentrated in construction, real estate and finance. The adult effect is large, because construction is mostly migrant and adult. Graduate effects come through real-estate, finance and design jobs.
**Problem:** the adult urban rate stayed at 5.1–5.2%. In this project's model, a general demand fall big enough to explain youth unemployment implies adult unemployment near 6% (`demand_inversion.md`). The property story has to work mainly through graduate-type jobs, or through migrants leaving the urban survey.

### 3. Regulatory shocks: tutoring and platforms

- **Tutoring ban (July 2021):** about 3 million job losses within four months (estimate; Huang et al. 2025) (Huang, Liu, Ma & Yang 2025, *J. Comparative Economics*). The effect persisted through 2022 and doubled once spillovers to arts and sports training are counted. New Oriental alone cut 60,000 staff. Tutoring hired graduates heavily.
- **Platform tightening (2021–22):** in 2022 Alibaba cut about 20,000 jobs, Meituan about 10,000, and Tencent and Baidu over 4,000 each (SCMP). Tencent's workforce shrank for the first time in a decade. Internet firms were the graduates' preferred private employers.
- Renmin University's Mao Yufei: real estate, internet, tutoring and financial services cut graduate hiring the most (Caixin 2025).

**Predicts:** a step fall in graduate demand from Aug 2021, concentrated in jobs that need degrees. Little adult effect. Graduate pay falls relative to the average.
**Fits:** the graduate-specific demand path that `demand_inversion.md` needs (6–15% below 2022), and the rise in relative-wage erosion from 2021.

### 4. Graduate supply outrunning graduate jobs (massification)

The graduating class grew 74% in 2012–25, with a jump of 1.67m in 2022 alone. The job-opening-to-applicant ratio is persistently lower for college students than for all job-seekers (ADB). Graduate starting pay fell from 0.75 to 0.60 of the urban average wage over 2018–23 (this project's data). That is the price signal of supply outrunning demand, and it began *before* the regulatory shocks.

**Predicts:** steady erosion of the graduate premium and rising graduate unemployment, made worse by any demand shock. Persistent.
**Fits:** the wage data, and the steady pre-2021 decline the two-type model missed (`wage_anchor.md`).

### 5. Queuing and waiting for secure jobs (adaptation)

Graduates increasingly wait, re-sit exams or prepare for the civil service rather than take the first job:

- Graduates entering the civil service, public institutions or SOEs rose from 39.3% (2019) to 49.3% (2021) (Peking University survey, via ADB). Rating SOEs most attractive rose from 36% (2020) to 49% (2024).
- National civil-service exam applicants passing review rose from about 2.6m (2023) to 3.03m (2024), 3.42m (2025) and 3.72m (2026), about 98 per place.
- Postgraduate entrance-exam applicants rose from 1.65m (2015) to a peak of 4.74m (2023), then fell to 4.38m (2024) and 3.88m (2025). The civil-service queue lengthened while the postgraduate one shortened.
- 77.5% of undergraduates planned further study in 2024, up from 68.5% two years earlier. "Slow employment" (慢就业) and postponed entry are widely reported.

**Predicts:** graduates enter the measured labour market over many months, not in July. Measured unemployment includes exam-takers who search half-heartedly, and participation falls as NEET status rises.
**Fits:** the seasonal result in `seasonal_2024.md`. Spreading entry over 8–11 months is the first specification to beat the naive forecast.

**Comparative precedent:** Dickens & Lang (1991) on Sri Lanka found educated youth unemployment was largely queuing for high-wage public jobs, worsened by a state preference for hiring the unemployed. The same pattern appears in Egypt (Assaad), in India's "timepass" graduates (Jeffrey 2010), and in Korea's "just resting" (쉬었음) youth: about 400–500k, with resting doubling as a reason for inactivity from 10.5% to 20%.

### 6. Mismatch and preferences: services over factories

Youth participation collapsed: ages 16–19 from about 50% (2000) to just over 10% (2020), ages 20–24 from about 80% to 50% (NUS EAI). Young workers avoid factories and farms and move into services. Gig and flexible work absorbed the overflow: over 200 million flexible workers (MOHRSS, Dec 2025), 16% of 2020–21 graduates entering gig work, and flexible job-seekers more likely than others to hold degrees (51.7% vs 48.0%).

**Predicts:** high reservation wages and a large "downgrading cost". Graduates refuse non-graduate jobs, so unemployment persists even when low-skill jobs exist. Gig work hides part of this as employment.

### 7. Jobless growth, automation and "involution"

The 2025 youth surge came with about 5% GDP growth. Economists point to automation, labour-light high-tech growth (AI, semiconductors) and price wars in steel, solar, EVs and batteries that squeeze hiring (Caixin 2025; IMF 2026).

## What each story predicts that the others do not

| Observable | Cyclical | Property | Regulatory | Supply | Queuing | Mismatch |
|---|---|---|---|---|---|---|
| Adult unemployment rises with youth | **yes** | **yes** | no | no | no | no |
| Youth unemployment persists after 2023 | no | yes | yes | yes | yes | yes |
| Graduate premium falls before 2021 | no | no | no | **yes** | no | no |
| Graduate postings fall while applicants rise | yes | yes | **yes** | no | no | no |
| Flatter seasonal swing: entry spread out | no | no | no | no | **yes** | partly |
| Civil-service applicants rise | weakly | weakly | yes | yes | **yes** | no |
| Participation falls (NEET up) | temporarily | no | no | no | **yes** | **yes** |

No single story fits every row. The tournament (`stories.py`) scores combinations by Monte Carlo against these observables jointly.

## Two-way links between education and jobs

- **Jobs → education:** a bad graduate market sends more graduates into exam queues (civil service, postgraduate). The state expanded master's places in 2020 partly to absorb graduates. Both delay entry, which lowers this year's measured unemployment and raises later supply.
- **Education → jobs:** each extra graduate cohort lowers graduate pay (CES) and pushes graduates into non-graduate jobs. It also raises firms' degree requirements (emulation), which lowers non-graduates' prospects.
- **Policy loop:** high youth unemployment → more postgraduate places and SOE hiring quotas → delayed entry and a larger later wave.

## Sources

- ADB Brief No. 247, *A Closer Look at Causes of Youth Unemployment in the PRC* (2023): https://www.adb.org/sites/default/files/publication/890896/adb-brief-247-causes-youth-unemployment-prc.pdf
- IMF Country Report 26/44, China Article IV (2026): https://www.imf.org/-/media/files/publications/cr/2026/english/1chnea2026001-source-pdf.pdf
- World Bank, China Economic Update, June 2024: https://thedocs.worldbank.org/en/doc/c7a6b75bc5c138a7ec7e62789695978f-0070012024/original/CEU-June-2024-EN.pdf
- Huang, Liu, Ma & Yang, "The Economic Toll of China's Tutoring Ban", VoxChina (2025): https://voxchina.org/show-3-422.html
- SCMP, "China's Big Tech slashed jobs by the thousands in 2022": https://scmp.com/tech/big-tech/article/3215010/chinas-big-tech-slashed-jobs-thousands-2022-amid-regulatory-scrutiny-covid-19-controls-and-tough
- NBS, interpretation of 2022 wage data: https://www.stats.gov.cn/sj/sjjd/202305/t20230509_1939288.html
- Caixin, "Youth Unemployment Surge Exposes Cracks in China's Economic Transition" (2025): https://www.caixinglobal.com/2025-09-19/analysis-youth-unemployment-surge-exposes-cracks-in-chinas-economic-transition-102363893.html
- Caixin, "How China's growing gig economy has left a generation adrift" (2026): https://www.caixinglobal.com/2026-03-02/cover-story-how-chinas-growing-gig-economy-has-left-a-generation-adrift-102418672.html
- Yicai, postgraduate exam applicants: https://www.yicai.com/news/102369061.html
- Jiemian, civil-service exam applicants 2023–26: https://www.jiemian.com/article/13527199.html
- NUS East Asian Institute Brief 1740, China's youth employment: https://research.nus.edu.sg/eai/wp-content/uploads/sites/2/2023/12/EAIBB-No.-1740-Chinas-Youth-Employment-exsum-2.pdf
- Sixth Tone, graduates in gig work (Zhaopin/Jinan University 2023): https://www.sixthtone.com/news/1013728/Many College Grads Drawn to Gig Work: Report
- Dickens & Lang, "An Analysis of the Nature of Unemployment in Sri Lanka", NBER WP 3777: https://www.nber.org/papers/w3777
- Korea Times, idle graduates (2025): https://www.koreatimes.co.kr/southkorea/society/20250706/more-idle-graduates-stay-home-shun-work-in-korea
