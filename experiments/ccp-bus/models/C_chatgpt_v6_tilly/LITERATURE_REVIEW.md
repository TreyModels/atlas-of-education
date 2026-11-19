# What the Bus model explains: CCP corruption, patronage and the literature

Critical scoping review and assessment of the executed hierarchical model. Research cutoff: 18 November 2026.

## Assessment

The model supplies a coherent account of how corrupt cooperation can survive removals when appointments and relationships reproduce the incentives of those who leave. Its current results align with several established mechanisms in research on the CCP. This review narrows the interpretation of the earlier run summary: computational repetition demonstrated internal behavior, while country-specific explanations remain hypotheses. Its strongest prospective contribution is to investigate the conditions governing their interaction.

Most component ideas already have substantial predecessors. Hierarchical corruption ABMs exist, Chinese factions have been modeled formally and estimated empirically, and recent PLA research explicitly describes the rebuilding and subsequent purging of networks around a leader's own appointees. The current model has achieved a useful theory demonstration. Establishing a distinct explanation of Chinese outcomes requires sharper comparisons with that work and evidence capable of distinguishing rival mechanisms.

A promising research question is: **Under what combinations of appointment control, enforcement capacity, concealment cost and sectoral rents does a campaign suppress informal networks, drive surviving cooperation into less observable forms, or allow networks to regenerate?**

## Review scope and access

This review covers 48 scholarly works, methodological references and empirical source sets. It draws on searches for CCP corruption, faction formation, patronage, information concealment, military appointments, procurement, authoritarian anticorruption and agent-based simulation, followed by targeted searches for close predecessors and competing explanations. Recent-work searches included 2025–2026. Publisher records, author-hosted papers and university repositories were preferred.

It is a broad critical scoping review. It has no preregistered search protocol, exhaustive database export or meta-analysis. Coverage concentrates on English-language scholarship; subscription databases and the full Chinese-language literature were outside the accessible search. Some items were available only through abstracts or book descriptions. The bibliography states the basis for each assessment, and working papers are identified separately. Neither full books nor every article were read end to end in this session.

## What the simulation has taught us

The latest implementation uses synthetic behavioral coefficients. The real-world files supplied with it were not used to estimate those coefficients. Its 768 runs establish behavior of the specified artificial system and test reproducibility across an experimental parameter design.

The principal batch contains 24 parameter combinations, four seeds and six regimes at 50,000 agents. Size checks add 192 runs at 10,000 and 100,000 agents, using the same first four parameter combinations.

| Executed finding | Interpretation supported within the model | Boundary of the finding |
| --- | --- | --- |
| Sustained campaigns lower misconduct in every sampled parameter combination while patron relationships remain | Greater enforcement can coexist with continuing reproduction of an informal organization | Protection and capacity constraints are encoded assumptions. Their magnitude in China remains unestimated. |
| Temporary campaigns produce substantial rebound after the intervention ends | Personnel turnover and temporary deterrence can leave conditions for renewed misconduct | This is an experiment with an assumed termination date, rather than an observed account of Xi's campaign ending. |
| Hidden trust increases under sustained campaigns in 18 of 24 parameter combinations; it decreases in six | Suppression and concealment can dominate under different conditions | The concealment decision explicitly responds to enforcement. Its direction is partly constructed; its empirical frequency is unknown. |
| Procurement expansion increases misconduct in the procurement sector | Additional transaction opportunities can offset enforcement under the assumed rent response | The model directly assigns positive procurement elasticity. It does not establish actual diversion rates or adjudicate the motives for military purges. |
| Open recruitment improves outcomes throughout the sampled design | Entry mechanisms can alter the long-run composition of an organization | Sponsored entrants are assumed to have lower average integrity. A productive role for patronage and alternative selection patterns need representation. |
| Aggregate misconduct differs by less than 0.1 percentage point between the matched 10,000- and 100,000-agent checks | Those particular aggregate patterns are stable to the tested changes in organizational span | Only four parameter combinations were checked. The experiment holds 64 organizations fixed and changes rank composition, so it is not a general convergence result. |

For reference, the paired median reduction under the sustained campaign is 11.5 percentage points across the 96 principal draw-seed pairs. The paired median procurement-sector increase under procurement expansion is 13.9 points. These are effects on synthetic populations. The published tables' endpoint medians and the median of paired differences answer different questions.

The concealment result deserves more attention than the overall average. Parameter combinations with a falling hidden-trust share had higher average capacity than combinations with a rising share. That is an exploratory association in 24 designed draws. It motivates a targeted experiment in which capacity changes while other inputs remain fixed.

## How closely the model maps onto the CCP

| Feature | Empirical connection | Current representation and assessment |
| --- | --- | --- |
| Hierarchical authority and appointments | Career research consistently treats appointments and promotion relationships as central to CCP organization [11–19] | Five ranks and distinct superior/patron links provide a plausible organizational skeleton. Individual career progression and promotion competition remain absent; agents occupy fixed seats whose occupants turn over. |
| Corrupt exchanges spanning public and private actors | Case and network research documents brokerage across offices and business [7,20,21] | Official-supplier pairs and trust contacts capture part of this structure. Intermediaries, families and SOE ownership links require more detail. |
| Protection and selective punishment | Studies identify protection but differ over its timing, beneficiaries and institutional setting [16–18] | One protection coefficient simplifies several distinct processes. Investigation, sanction and job removal need separate events. |
| Concealment | Empirical work documents manipulation of reports and indirect patronage [22,23,42] | Hidden edges capture a latent relationship state. The model does not yet represent complaints, investigators' beliefs or selective disclosure of ties. |
| The Xi transition | Research studies changing appointments, inspections and military organization [17,19,25,28–31] | A policy switch in 2013 is an abstraction. There is no strategic leader choosing an evolving campaign, and later institutional reforms are not reconstructed. |
| Faction formation and survival | Formal and empirical studies describe endogenous factional advantage and changes in network influence [14,19,30] | Patron roots form groups without fixed faction names. Those tree-based groups are proxies; overlapping alliances and political bargaining are largely missing. Official trust contacts have fixed endpoints, although their weights and visibility change. |
| PLA procurement | Fieldwork and contemporary sources connect personnel markets, suppliers and procurement vulnerabilities [28,46,47] | Procurement has larger opportunities in one experiment. There are no endogenous bids, equipment quality, combat readiness or documented contract allocations. |
| Singapore comparison | Comparative research emphasizes sustained implementation, enforcement and administrative design [5,26,27,48] | The institutional-controls bundle is a hypothetical comparison. Its coefficients were not fitted to Singapore. |

The model's empirical correspondence is at the level of mechanisms and institutional motifs. The current population shares, behavioral distributions and time paths lack country-specific estimation. A general explanatory model can work at that level, provided its claims remain attached to the mechanisms actually tested.

## What the literature already explains

### Corruption as an institutional system

Lü [6] places organizational development at the center of the history of cadre corruption. Pei [7] emphasizes networks built around control of assets and personnel. These works provide strong precedents for treating corruption as something reproduced through organization.

Ang [8] separates different forms of corruption and their economic effects. Wedeman [9] addresses the coexistence of growth and substantial corruption. Their work exposes a limitation in a single binary misconduct variable: the same aggregate rate can conceal shifts among extortion, theft and politically connected transactions.

Bai, Hsieh and Song [10] analyze special deals as part of China's development system. A deal-based relationship can have an economic coordination function, so connections cannot automatically be coded as evidence of corrupt intent.

### Persistence, norms and enforcement constraints

Andvig and Moene [1] formalize feedback between the prevalence and profitability of corruption. Mishra [2] examines persistent corrupt equilibria and evolutionary reproduction. Persson, Rothstein and Teorell [3] argue that systemic settings challenge reforms that assume an effective, incorruptible principal; their evidence comes from Kenya and Uganda, so its application to China needs a separate argument.

These are close theoretical predecessors of persistent misconduct in the Bus model. A useful extension would show how career reproduction changes the boundaries of these dynamics under different enforcement technologies. The current runs do not establish multiple equilibria or hysteresis; temporary persistence and rebound can arise through ordinary adjustment.

### Patronage, performance and political protection

Jiang [11] finds evidence that patron relationships can improve bureaucratic coordination and performance. Jia, Kudamatsu and Seim [12] analyze complementarity between connections and performance. Shih, Adolph and Liu [13] establish the importance of elite ties in advancement. Together they require an account of what patronage accomplishes for the organization as well as what it permits clients to extract.

Francois, Trebbi and Xiao [14] already provide an estimated organizational model of CCP factions, with feedback from promotion support to factional power. Li, Roland and Xie [15] integrate corruption rents, party hierarchy and the Center's political objectives. A claim to be the first general formal model of this political economy would therefore be untenable.

Protection also has several forms. Zeng and Yang [16] distinguish incumbent and retired patrons. Lorentzen and Lu's early-campaign working paper [17] supports both genuine anticorruption targeting and selective protection. Trinh [18] differentiates protection before investigation from leniency or delay afterward. These studies use different populations, periods and measures; one constant exemption parameter cannot reproduce their distinctions.

### Evidence that networks can contract

Li and Manion [19] find that broad purge pressure during 2013–2017 encouraged provincial bosses to avoid appointing their own clients, including among bosses connected to Xi. This supplies an important empirical challenge to a model in which pressure simply reinforces sponsorship. Their finding concerns appointment decisions in a particular period and setting.

Wang and Yan [24] document risk avoidance and bureaucratic slack following disruption of informal relationships. Modeling effort and implementation would allow a campaign to improve integrity while also generating governance costs.

### Underground cooperation and distorted information

Pan and Chen [22] show that internal reporting can omit corruption complaints implicating connected officials. Ruan, Lu and Ruan [23] document indirect trust chains under anticorruption pressure in a county setting. Those are distinct concealment mechanisms: suppression of information reaching a principal, and reorganization of cooperation among clients.

Tu, Gong and Li [42] study corruption latency under agent-controlled transparency. A decline in visible network evidence can reflect a change in disclosure as well as a change in underlying conduct. The Bus model needs an observation process to distinguish those possibilities.

### PLA appointments, procurement and recurrent purges

Peng Wang [28] examines guanxi in the buying and selling of military positions. Mattingly's published work [29] studies the balance between domestic political concerns and external military requirements in appointments. These establish why the military module should connect careers and organizational capability with financial transactions.

A Yale-hosted draft dated June 16, 2026 [30] explicitly describes old networks being dismantled, allies forming new patronage groups, and renewed purges. It analyzes 12,884 positions held by 1,358 officers. This is a particularly close predecessor for the regeneration argument. It remains a working draft, and its title page omits an author name.

Woods [31] offers a formal alternative based on imperfect monitoring during centralized modernization. Similar dismissal patterns can arise through uncertainty about implementation and performance. The present model lacks the variables needed to compare that explanation with network-based targeting.

CSIS [46] supplies contemporary purge records, with confirmed and possible cases distinguished. CSET [47] supplies selected procurement records. Neither is a random sample of latent military corruption, and a procurement relationship is not itself a corruption label.

### Anticorruption as governance and institutional change

Carothers and Zhu [25] examine inspections serving a widening set of governance objectives. Carothers's comparative book [26] also offers an account of successful authoritarian corruption control. Those contributions challenge any specification that makes widespread corruption unavoidable under every form of concentrated authority.

Quah [27] treats Singapore as an institutional achievement requiring sustained political support and implementation. Manion's mainland/Hong Kong comparison [5] gives another close comparative frame. The Singapore benchmark should specify observable institutions and their operation; copying a low simulated endpoint into the label would add no comparative evidence.

## Has anyone built something similar computationally?

Yes. There is a substantial computational corruption literature, and some recent papers overlap closely with this project.

| Predecessor | Overlap with this project | Distinction that could motivate further work |
| --- | --- | --- |
| Hammond [32], 2000 | Heterogeneous agents, social information and endogenous changes in corruption | CCP-specific appointment reproduction and sectoral political economy |
| Zausinová et al. [33], 2020 | History, information and transitions in citizen-bureaucrat corruption | Hierarchical careers and latent patronage relations |
| Valverde et al. [35], 2024 | Businesses and public servants, group size and institutional control | Political protection, careers and relationships after leadership turnover |
| Kovács and Yorke-Smith [36], MABS 2025 / proceedings 2026 | Administrative corruption in hierarchical organizations | A CCP application with explicitly measured appointment and concealment patterns |
| Barsekh-onji and Cardoso Espinosa [37], 2026 | Procurement, clientelist ties and institutional interventions | Political control of appointments and sectoral faction regeneration |
| Neo, Higgs and Floridi [38], 2026 working paper | Repeated procurement, learning and detection interventions | Joint recruitment and concealment mechanisms tied to CCP evidence |
| Francois, Trebbi and Xiao [14], 2023 | Estimated CCP hierarchy and endogenous factional advantage | A richer explicit process of corrupt transactions and observability, if it generates additional testable implications |

The 2021 overview by Elnawawy, Okasha and Hosny [34] confirms that this is an established research field. Computational scale, Python implementation and Monte Carlo repetition do not themselves constitute a literature contribution.

## Research gaps the project could address

The gaps below are candidates identified by this scoping review. Each needs comparison with the nearest cited studies before any claim of priority.

### 1. Conditions governing suppression, concealment and regeneration

The empirical literature contains evidence of reduced client appointments, covert cooperation and renewed patronage influence in different contexts. A unified model could identify when each occurs and produce observable implications about their timing. The current 18-versus-six concealment result is an initial diagnostic.

To make this substantive, officials need to choose visible sponsorship, indirect sponsorship or open recruitment in response to political risk. Concealment must affect what investigators observe. The design should permit early network contraction and later reconstitution, including a regime in which contraction persists.

A discriminating implication would be declining publicly identifiable appointment favoritism alongside increasing use of intermediaries or a higher concentration of repeatedly connected suppliers. Evidence would need to measure these processes separately.

### 2. Separating the productive and extractive functions of relationships

Current sponsored entrants receive a built-in integrity penalty. A stronger model would also let patrons transmit information, coordinate projects and reward competence. It could then ask which institutional arrangements preserve coordination while restricting illicit extraction.

Relevant outcomes would include implementation effort, transaction quality and rents, each measured separately. An institutional reform that lowers misconduct but depresses output would be distinguishable from one that improves both. This is essential for a model described as political economy.

### 3. Testing competing explanations of PLA purges

The model could compare network-power targeting, procurement misconduct and noisy performance monitoring under a common observation process. Their predicted patterns may overlap at the top level but differ in the ordering of removals, exposure across organizations and subsequent appointments.

Examples include whether related personnel are removed before a senior patron, whether a procurement shock changes targeting after accounting for existing networks, and whether performance signals predict removals among weakly connected officers. These require explicit rival mechanisms; the existing rent-expansion scenario alone cannot adjudicate them.

### 4. Measuring hidden relationships through multiple imperfect traces

The latent network could generate public career overlap, contract relationships, complaints, investigation disclosures and sanctions. Testing the same latent structure against multiple traces would create a stronger connection to evidence.

The observation rules should allow a successful crackdown to change detection and disclosure. A fitted latent network would still depend on assumptions about missing data, so sensitivity to those assumptions must be visible.

### 5. Mechanism-specific comparison with Singapore

Use a small set of documented institutional differences, retaining comparable distributions of individual incentives at the start. Vary appointment discretion, investigation independence in practice, procedural controls and reporting incentives separately.

The research value would lie in explaining which mechanisms change the reproduction process. Raw case totals are incompatible targets without comparable populations and definitions. The current bundled institutional-controls experiment supplies a starting counterfactual rather than a fitted Singapore comparison.

## What a defensible contribution would look like

A suitable central claim would be that **campaign pressure can alter the organization and visibility of corrupt cooperation, with its long-run effects depending on career reproduction and sectoral transaction opportunities**. That statement connects established mechanisms and specifies conditions for evaluation.

The next analysis should include:

- Entrant selection with zero, adverse and favorable relationships between sponsorship and integrity, plus a separate competence variable.
- Endogenous choice among public sponsorship, covert intermediaries and open recruitment.
- Distinct investigation, sanction and employment-exit events.
- A productive output or procurement-quality measure.
- Rival military-targeting mechanisms and mechanism-removal experiments.
- Empirical checks against several independent patterns, with at least some evidence reserved from calibration.

A successful explanatory paper would identify a boundary or interaction that simpler models miss and show that it helps make sense of independent observations. It would remain valuable without attempting to predict individual officials or exact annual totals.

## Annotated bibliography and access register

Codes: **T** means a primary full-text source was available and relevant sections were inspected; **A** means the assessment relies on a primary abstract, publisher record or institutional research record; **B** means a book's publisher/author synopsis or preview; **W** marks a working paper; **O** marks an official or original empirical source set. T does not mean every page or mathematical proof was audited.

### [1] Andvig, Jens Chr., and Karl Ove Moene (1990)

[How Corruption May Corrupt](https://www.sciencedirect.com/science/article/pii/016726819090053G). Journal of Economic Behavior & Organization 13(1): 63–76. **Access: A.**

Formalizes feedback between corruption prevalence and its returns, including multiple self-fulfilling equilibria. Establishes a major theoretical predecessor for peer reinforcement; no China-specific calibration.

### [2] Mishra, Ajit (2006)

[Persistence of Corruption: Some Theoretical Perspectives](https://www.sciencedirect.com/science/article/pii/S0305750X05001658). World Development 34(2): 349–358. **Access: A.**

Treats persistence through equilibrium and evolutionary approaches. Persistent behavior under interventions is an established theoretical subject; a new application needs an additional mechanism or discriminating implication.

### [3] Persson, Anna, Bo Rothstein, and Jan Teorell (2013)

[Why Anticorruption Reforms Fail: Systemic Corruption as a Collective Action Problem](https://doi.org/10.1111/j.1468-0491.2012.01604.x). Governance 26(3): 449–471. **Access: A.**

Interview-based argument from Kenya and Uganda concerning systemic corruption and the assumption of effective principals. Useful theoretical framing with an explicit cross-context transfer problem.

### [4] Manion, Melanie (1996)

[Corruption by Design: Bribery in Chinese Enterprise Licensing](https://academic.oup.com/jleo/article-abstract/12/1/167/896197). Journal of Law, Economics, and Organization 12(1): 167–195. **Access: A.**

Models licensing and institutional design in China. A direct predecessor to studying changes in corrupt equilibria through organizational rules.

### [5] Manion, Melanie (2004)

[Corruption by Design: Building Clean Government in Mainland China and Hong Kong](https://polisci.duke.edu/books/corruption-design). Harvard University Press; later digital/paperback editions exist. **Access: B.**

Comparative institutional analysis relevant to transitions out of widespread corruption. Hong Kong is the main comparison, making it a closer regional counterpart worth considering alongside Singapore. Book contents were assessed through descriptions, not a complete reading.

### [6] Lü, Xiaobo (2000)

[Cadres and Corruption: The Organizational Involution of the Chinese Communist Party](https://www.degruyterbrill.com/document/doi/10.1515/9780804764483/html). Stanford University Press. **Access: B.**

Historical organizational account extending beyond market-era incentives. Supports attention to how the party reproduces cadre practices. Publisher synopsis and bibliographic record inspected.

### [7] Pei, Minxin (2016)

[China’s Crony Capitalism: The Dynamics of Regime Decay](https://fairbank.fas.harvard.edu/events/the-origins-and-dynamics-of-crony-capitalism-in-china-insights-from-260-cases-of-collusive-corruption/). Harvard University Press. **Access: B.**

Author presentation describes collusive cases linking assets, appointments and elite networks. Supplies a close substantive predecessor for the organizational argument. A selected set of exposed cases cannot identify population prevalence.

### [8] Ang, Yuen Yuen (2020)

[China’s Gilded Age: The Paradox of Economic Boom and Vast Corruption](https://www.cambridge.org/core/books/chinas-gilded-age/389BE063CCB6E75DDA144C36DABACD7A). Cambridge University Press. **Access: B.**

Distinguishes corruption types and their growth consequences. Requires a political-economy model to distinguish transactions and losses rather than assign one interpretation to every corrupt act. Publisher material inspected.

### [9] Wedeman, Andrew (2012)

[Double Paradox: Rapid Growth and Rising Corruption in China](https://academic.oup.com/cornell-scholarship-online/book/29922). Cornell University Press. **Access: B.**

Addresses China’s growth-corruption coexistence. Useful historical context for differentiating economic consequences and avoiding a universal prediction of immediate organizational collapse.

### [10] Bai, Chong-En, Chang-Tai Hsieh, and Zheng Michael Song (2019 working paper / NBER Macroeconomics Annual 2019 volume)

[Special Deals with Chinese Characteristics](https://www.nber.org/papers/w25839). NBER Working Paper 25839; corresponding NBER book chapter. **Access: A/W.**

Explains how special deals interact with distorted institutions and growth. Preferential access and socially costly corruption require distinct definitions when interpreting official-business connections.

### [11] Jiang, Junyan (2018)

[Making Bureaucracy Work: Patronage Networks, Performance Incentives, and Economic Development in China](https://www.junyanjiang.com/uploads/5/8/1/9/58193547/jiang_making_bureaucracy_work_full.pdf). American Journal of Political Science 62(4): 982–999. **Access: T.**

Career-based city panel evidence for a coordination and incentive function of patronage. A key challenge to the model’s adverse integrity shift for every sponsored entrant. Author-hosted full paper inspected in relevant sections.

### [12] Jia, Ruixue, Masayuki Kudamatsu, and David Seim (2015)

[Political Selection in China: The Complementary Roles of Connections and Performance](https://academic.oup.com/jeea/article-abstract/13/4/631/2319780). Journal of the European Economic Association 13(4): 631–668. **Access: A.**

Finds complementarity between connections and performance in selection. Suggests modeling competence, information and rewards alongside loyalty and misconduct.

### [13] Shih, Victor, Christopher Adolph, and Mingxing Liu (2012)

[Getting Ahead in the Communist Party: Explaining the Advancement of Central Committee Members in China](https://www.polisci.washington.edu/research/publications/getting-ahead-communist-party). American Political Science Review 106(1): 166–187. **Access: A.**

An influential empirical study of elite advancement and connections. Central Committee evidence should not be generalized mechanically to all ranks or later political periods.

### [14] Francois, Patrick, Francesco Trebbi, and Kairong Xiao (2023)

[Factions in Nondemocracies: Theory and Evidence From the Chinese Communist Party](https://onlinelibrary.wiley.com/doi/10.3982/ECTA19274). Econometrica 91(2): 565–603. **Access: T/A.**

An estimated organizational model of factions and promotions. The 2020 author-hosted working version was inspected alongside publication metadata. Essential prior work for endogenous factional advantage and hierarchical counterfactuals.

### [15] Li, Weijia, Gérard Roland, and Yang Xie (2022)

[Crony Capitalism, the Party-State, and the Political Boundaries of Corruption](https://research.monash.edu/en/publications/crony-capitalism-the-party-state-and-the-political-boundaries-of-/). Journal of Comparative Economics 50(3): 652–667. **Access: A.**

A particularly close formal predecessor combining local rents, hierarchical flows and central political objectives. Its integration of productivity and political control identifies mechanisms missing from the current ABM.

### [16] Zeng, Qingjie, and Yujeong Yang (2017)

[Informal Networks as Safety Nets: The Role of Personal Ties in China’s Anti-Corruption Campaign](https://experts.illinois.edu/en/publications/informal-networks-as-safety-nets-the-role-of-personal-ties-in-chi/). China: An International Journal 15(3): 26–57. **Access: A.**

Studies over 500 provincial officials and differentiates incumbent from retired patrons. Useful evidence for conditional protection, without equating a relationship with an observed corrupt act.

### [17] Lorentzen, Peter, and Xi Lu (2018 draft)

[Personal Ties, Meritocracy, and China’s Anti-Corruption Campaign](https://www.aeaweb.org/conference/2019/preliminary/paper/hSA5ri6d). Working paper dated November 21, 2018; hosted for the 2019 AEA meeting. **Access: T/W.**

Analyzes the first campaign phase, supporting corruption targeting alongside selective protection. Its scope and working-paper status matter when using it to constrain later PLA behavior.

### [18] Trinh, Duy (2025 issue / online 2024)

[The Factional Logic of Political Protection in Authoritarian Regimes](https://researchportal.hkust.edu.hk/en/publications/the-factional-logic-of-political-protection-in-authoritarian-regi/). Comparative Political Studies 58(1): 155–189. **Access: A.**

China–Vietnam comparison differentiates exclusion from investigation and protection through subsequent punishment. An explicit reason to separate stages of enforcement and allow forms of protection to vary.

### [19] Li, Zeren, and Melanie Manion (2023 issue / online 2022)

[The Decline of Factions: The Impact of a Broad Purge on Political Decision Making in China](https://www.cambridge.org/core/journals/british-journal-of-political-science/article/decline-of-factions-the-impact-of-a-broad-purge-on-political-decision-making-in-china/F7DE172435D36DABBA3B51A26BC692EA). British Journal of Political Science 53(3): 815–834. **Access: T.**

Finds anti-client appointment bias under broad purge pressure. Provides a direct empirical challenge to automatic sponsorship reinforcement; a strong target pattern for a revised model.

### [20] Chang, Zheng (2018)

[Understanding the Corruption Networks Revealed in the Current Chinese Anti-corruption Campaign: A Social Network Approach](https://scholars.cityu.edu.hk/en/publications/understanding-the-corruption-networks-revealed-in-the-current-chi/). Journal of Contemporary China 27(113): 735–747. **Access: A.**

Network analysis of public records and indictments. Helps operationalize connected misconduct, with the limitation that exposed networks depend on investigation and disclosure.

### [21] Wang, Yingyao (2020 issue / online 2019)

[A Network-Exchange Approach to Corruption: Brokers and Institution Spanning in a Chinese Corruption Network](https://www.tandfonline.com/doi/full/10.1080/01639625.2019.1640525). Deviant Behavior 41(12): 1636–1649. **Access: A.**

A 161-person case illustrates brokerage across institutional boundaries. Supports separate roles for intermediaries and resource holders; it is a strategic case rather than a representative national network.

### [22] Pan, Jennifer, and Kaiping Chen (2018)

[Concealing Corruption: How Chinese Officials Distort Upward Reporting of Online Grievances](https://www.cambridge.org/core/journals/american-political-science-review/article/abs/concealing-corruption-how-chinese-officials-distort-upward-reporting-of-online-grievances/43D20A0E5F63498BB730537B7012E47B). American Political Science Review 112(3): 602–620. **Access: A.**

Internal communications reveal omission of complaints involving connected officials. Direct evidence for an information channel of protection, distinct from changing the existence or visibility of a social tie.

### [23] Ruan, Ji, Yuanyuan Lu, and Shizhan Ruan (2026)

[Trust Chains and the Resilience of Patronage Networks: The Use of Indirect Guanxi Under Anti-Corruption](https://kar.kent.ac.uk/113556/). Journal of Contemporary China; DOI 10.1080/10670564.2026.2639982. **Access: A.**

County ethnography provides an immediate substantive predecessor for indirect patronage and adaptive trust chains. Its bounded setting constrains national claims and quantitative hidden-network shares.

### [24] Wang, Peng, and Xia Yan (2020)

[Bureaucratic Slack in China: The Anti-corruption Campaign and the Decline of Patronage Networks in Developing Local Economies](https://www.cambridge.org/core/journals/china-quarterly/article/abs/bureaucratic-slack-in-china-the-anticorruption-campaign-and-the-decline-of-patronage-networks-in-developing-local-economies/8CBF5E3B2DEF19012ED980C2F62FDDFE). The China Quarterly 243: 611–634; DOI 10.1017/S0305741019001504. **Access: A.**

Qualitative evidence connects anticorruption, disrupted relationships and bureaucratic risk avoidance. Provides an outcome dimension, implementation effort, missing from the binary misconduct model.

### [25] Carothers, Christopher, and Zhang Zhu (2023 issue / online 2022)

[From Corruption Control to Everything Control: The Widening Use of Inspections in Xi’s China](https://www.tandfonline.com/doi/full/10.1080/10670564.2022.2071885). Journal of Contemporary China 32(140); DOI 10.1080/10670564.2022.2071885. **Access: A.**

Uses inspection reports to examine widening governance objectives. Supports treating campaign policy as a broader organizational strategy and motivates an endogenous principal objective.

### [26] Carothers, Christopher (2022)

[Corruption Control in Authoritarian Regimes: Lessons from East Asia](https://www.cambridge.org/core/books/corruption-control-in-authoritarian-regimes/F09BC4457E285EE04E392A78941B3FD2). Cambridge University Press. **Access: B.**

Comparative account of authoritarian corruption control. The author emphasizes motivation, discretion and implementation capacity. A counterweight to treating concentrated authority as mechanically producing one corruption equilibrium.

### [27] Quah, Jon S. T. (2017)

[Singapore’s Success in Combating Corruption: Lessons for Policy Makers](https://doi.org/10.1108/AEDS-03-2017-0030). Asian Education and Development Studies 6(3): 263–274. **Access: A.**

Institutional account emphasizing political commitment, capacity and impartial enforcement. Useful for selecting comparison mechanisms; it supplies no direct calibration of the Bus parameters.

### [28] Wang, Peng (2016)

[Military Corruption in China: The Role of Guanxi in the Buying and Selling of Military Positions](https://www.cambridge.org/core/journals/china-quarterly/article/abs/military-corruption-in-china-the-role-of-guanxi-in-the-buying-and-selling-of-military-positions/970EC9E8D37441C1E03B4F055A39D42F). The China Quarterly 228: 970–991; DOI 10.1017/S0305741016001144. **Access: A.**

Fieldwork and published materials connect guanxi with military personnel transactions. Demonstrates why procurement and appointments should be linked in the sector model.

### [29] Mattingly, Daniel C. (2024 issue / online 2022)

[How the Party Commands the Gun: The Foreign–Domestic Threat Dilemma in China](https://onlinelibrary.wiley.com/doi/10.1111/ajps.12739). American Journal of Political Science 68(1): 227–242. **Access: A.**

Examines officer appointments under competing domestic and external threats. Requires a military application to represent professionalism and competence alongside loyalty.

### [30] Author name absent on retrieved title page; hosted in Mattingly’s Yale research directory (June 16, 2026 draft)

[Why Do Autocrats Turn Against Their Allies? The Logic of Purge Cycles in China’s Military](https://bpb-us-w2.wpmucdn.com/campuspress.yale.edu/dist/3/4318/files/2026/06/Mattingly_PLA_Purges.pdf). Yale-hosted working draft; publication and author attribution require confirmation. **Access: T/W.**

A close predecessor linking successive patronage networks with renewed purges. Its empirical analysis is suggestive and explicitly leaves alternative motives unresolved. It should not be presented as a settled peer-reviewed finding.

### [31] Woods, Dwayne (2026)

[The Paradox of High-level Military Dismissals in China: A Formal Bayesian Model](https://link.springer.com/article/10.1007/s11366-026-09934-z). Journal of Chinese Political Science; DOI 10.1007/s11366-026-09934-z. **Access: T.**

Models dismissal under noisy monitoring during centralized modernization. Provides a rival explanation to factional targeting; the current model cannot compare them because it omits implementation and performance signals.

### [32] Hammond, Ross (2000)

[Endogenous Transition Dynamics in Corruption: An Agent-Based Computer Model](https://www.brookings.edu/wp-content/uploads/2016/06/ross.pdf). Brookings, Center on Social and Economic Dynamics working paper. **Access: T/W.**

Early corruption ABM with heterogeneous bureaucrats and citizens, social information and endogenous transitions. Establishes that social interaction and emergent corruption dynamics are longstanding computational subjects.

### [33] Zausinová, Jana, Martin Zoričak, Marcel Vološin, and Vladimír Gazda (2020 issue / online 2019)

[Aspects of Complexity in Citizen–Bureaucrat Corruption: An Agent-Based Simulation Model](https://link.springer.com/article/10.1007/s11403-019-00240-x). Journal of Economic Interaction and Coordination 15: 527–552. **Access: A.**

Studies history, social information and transitions. Publisher abstract and accessible notes inspected; subscription sections were not treated as read. A relevant predecessor for memory and information mechanisms.

### [34] Shaymaa Elnawawy M., Ahmed E. Okasha, and Hazem A. Hosny (2021 online / 2022 issue)

[Agent-Based Models of Administrative Corruption: An Overview](https://www.tandfonline.com/doi/full/10.1080/02286203.2021.1907652). International Journal of Modelling and Simulation, pp. 350–358. **Access: A.**

Reviews the established ABM field and identifies opportunities involving social ties, behavioral rules and monitoring. Publisher abstract assessed; full text was access-limited.

### [35] Valverde, Pablo, Jaime Fernández, Edwin Buenaño, Juan Carlos González-Avella, and Mario G. Cosenza (2024)

[Controlling Systemic Corruption Through Group Size and Salary Dispersion of Public Servants](https://puceinvestiga.puce.edu.ec/en/publications/controlling-systemic-corruption-through-group-size-and-salary-dis-2/). Heliyon 10(3): e25148. **Access: A.**

A business-public servant ABM examining group size, salary variation and institutional control. A close generic comparator for heterogeneous agents and procurement-like exchanges.

### [36] Kovács, Bertold B., and Neil Yorke-Smith (2025 conference / 2026 proceedings)

[An Agent-Based Model of Administrative Corruption in Hierarchical Organisations](https://research.tudelft.nl/en/publications/an-agent-based-model-ofadministrative-corruption-inhierarchical-o/). Multi-Agent-Based Simulation XXVI, pp. 77–88; DOI 10.1007/978-3-032-16328-8_6. **Access: A.**

A direct methodological predecessor on hierarchy and administrative corruption. Publisher/repository abstract inspected; attempted full-text retrieval failed. Its preliminary welfare results caution against evaluating only corruption rates.

### [37] Barsekh-onji, Aboud, and Edgar Oliver Cardoso Espinosa (2026)

[The Algorithmic Bureaucrat: Dismantling Clientelist Networks in Public Procurement Through Agent-Based Modeling](https://journals.sagepub.com/doi/full/10.1177/26643286261493873). Urban Governance; online September 30; DOI 10.1177/26643286261493873. **Access: T.**

Recent procurement and clientelism ABM reporting use of confidential Mexican agency data. The claims and model description provide a close comparator; confidential-data calibration was not independently audited.

### [38] Neo, Hui-Yuan, James Higgs, and Luciano Floridi (2026 draft)

[E-procurement Systems and the Deterring of Corruption: An Agent-based Modeling Approach](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7156518). SSRN working paper 7156518; revised August 5, 2026. **Access: A/W.**

Models repeated procurement and learning under detection changes. A current working-paper comparator for institutional interventions and changes in corrupt cooperation.

### [39] Fang, Hanming (2024 issue / 2023 working version)

[Measurements, Determinants, Causes, and Consequences of Corruption: Lessons from China’s Anti-corruption Campaign](https://doi.org/10.1007/s10797-023-09803-y). International Tax and Public Finance 31: 3–25; DOI 10.1007/s10797-023-09803-y. **Access: A.**

Review of measurement and behavioral consequences. Helps distinguish observable enforcement from latent corruption and situates the model within a wider empirical economics literature.

### [40] Tong, Shenghui (2022 issue / online 2021)

[Corruption and Anti-corruption in China: A Review and Future Research Agenda](https://onlinelibrary.wiley.com/doi/10.1111/apel.12345). Asian-Pacific Economic Literature 36(1): 3–16. **Access: A.**

Review identifies uneven coverage across micro and macro questions. Its gap assessment provides historical context, not proof that no subsequent paper addressed an issue.

### [41] Kautz, Carolin (2020)

[Power Struggle or Strengthening the Party: Perspectives on Xi Jinping’s Anticorruption Campaign](https://link.springer.com/article/10.1007/s11366-020-09665-9). Journal of Chinese Political Science 25: 501–511. **Access: A.**

Review maps debates around organizational strengthening and elite competition. Supports treating multiple campaign objectives as potentially coexisting mechanisms.

### [42] Tu, Wenyan, Ting Gong, and Hui Li (2024)

[The Divergent Effects of Agent-Controlled Transparency on Corruption Latency: Evidence from China](https://igpp.fudan.edu.cn/igppen/64/4c/c18266a681036/page.htm). Government Information Quarterly; publisher record S0740624X24000340. **Access: A.**

Differentiates latency across corruption types under agent-controlled transparency. Adds an empirical measurement dimension beyond recording whether a tie is visible.

### [43] Edmonds, Bruce, and coauthors (2019)

[Different Modelling Purposes](https://www.jasss.org/22/3/6.html). Journal of Artificial Societies and Social Simulation 22(3): 6. **Access: A.**

Distinguishes explanatory, predictive and other modeling purposes. Supports judging this project by an explicit explanatory question and evidence appropriate to it.

### [44] Grimm, Volker, and coauthors (2005)

[Pattern-Oriented Modeling of Agent-Based Complex Systems: Lessons from Ecology](https://pubs.usgs.gov/publication/70161783). Science 310: 987–991. **Access: A.**

Methodological basis for confronting multiple patterns at different scales. A pattern imposed by an acceptance rule or hard-coded behavior has limited value as independent evaluation.

### [45] Grimm, Volker, and coauthors (2020)

[The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism](https://www.jasss.org/23/2/7.html). Journal of Artificial Societies and Social Simulation 23(2): 7. **Access: T.**

Framework for a reproducible statement of purpose, entities, scheduling, assumptions and evaluation. Documentation supports scrutiny of an explanation without validating its substantive claims.

### [46] CSIS China Power Project (2026)

[CSIS Database of Chinese Military Purges](https://chinapower.csis.org/data/chinese-pla-military-purges/). Original dataset, updated through February 20, 2026. **Access: O.**

Separates confirmed and potential cases among senior officers. Suitable for observation definitions and organizational patterns, with uncertainty and restricted rank coverage retained.

### [47] CSET / Georgetown University (2021 release; contracts from 2020)

[Harnessed Lightning: Public Procurement Data](https://github.com/georgetown-cset/harnessedlightning). Original public repository, georgetown-cset/harnessedlightning. **Access: O.**

The downloaded file contains 343 nonempty AI-related contract records. It offers organizational and supplier relationships, not population-wide procurement or corruption labels.

### [48] Corrupt Practices Investigation Bureau, Singapore (2026 release covering 2025)

[Effective Enforcement and Collective Action Key to Keeping Singapore Corruption Free](https://www.cpib.gov.sg/press-room/effective-enforcement-and-collective-action-key-to-keeping-singapore-corruption-free/). Official annual statistics release, April 28, 2026. **Access: O.**

Reports investigations, prosecutions and other measures with explicit definitions. Useful comparison evidence after aligning concepts and populations; raw counts cannot calibrate a China-Singapore prevalence ratio.

## Suggested reading order

Start with Li, Roland and Xie [15] and Francois, Trebbi and Xiao [14] for the nearest formal political-economy models. Read Jiang [11] and Li and Manion [19] as checks on the current recruitment assumptions, followed by Pan and Chen [22] and Ruan, Lu and Ruan [23] for information and concealment. For the military module, compare the June 2026 draft [30] with Woods [31], then use the hierarchical ABM [36] and procurement ABMs [37,38] as methodological comparators.
