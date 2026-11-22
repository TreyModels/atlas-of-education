# Literature review: charter states, low-density urbanism, and the rise–peak–decline of mainland Southeast Asian tropical cities (with Angkor as the core case)

*Compiled for a computational-modelling project. Citations are to works whose existence and bibliographic details I verified via Crossref / Semantic Scholar / publisher listings. Where I report a number I say whether it is a **primary measurement** (measured from lidar, excavation, cores, tree-rings) or a **synthesis estimate** (a model or aggregate built on those measurements). Where I could not verify a claim I say so explicitly.*

---

## 1. Charter states, and the rival terms for the same object

### 1.1 Definition and provenance

**"Charter state" is Lieberman's own coinage**, not a borrowed term. It is his analytic unit in *Strange Parallels: Southeast Asia in Global Context, c. 800–1830*, vol. 1 *Integration on the Mainland* (Cambridge UP, 2003) and vol. 2 *Mainland Mirrors: Europe, Japan, China, South Asia, and the Islands* (Cambridge UP, 2009). Lieberman restates and defends the concept in "What *Strange Parallels* Sought to Accomplish", *Journal of Asian Studies* 70(4) (2011): 931–938, and in "Charter State Collapse in Southeast Asia, ca. 1250–1400, as a Problem in Regional and World History", *American Historical Review* 116(4) (2011): 937–963 (DOI 10.1086/ahr.116.4.937).

The core content of the concept, as Lieberman uses it: a polity whose legitimacy and administrative reach rest on a **shared, portable, textually codified charter** — a body of law, cosmology and Buddhist history that any ruler who adopts it can claim — rather than on a fixed territorial bureaucracy. The charter travels; the capital does not have to. Hence a charter state can lose its capital, its dynasty and most of its army and still be *reconstituted* by another ruler elsewhere who reissues the same charter. This is the single most important behavioural claim for a modeller, and it is a claim about **what survives a shock** (§1.5).

Lieberman's phases (vol. 1, and the 2011 AHR essay):
- **c. 800–1250** — fragmented era of small, competing, largely personal polities; heavy local autonomy; charter elements present but not yet consolidated.
- **c. 1250–1550** — charter consolidation / the "charter state" proper: mainland politics reorganise around Theravada Buddhist charter institutions, administrative reform, and intensified interstate competition. Lieberman (2011 AHR) treats the collapse of the charter states c. 1250–1400 (Pagan, Angkor, Dai Viet disruptions) as a *regional and world-historical* problem, not a local accident.
- **c. 1550–1830** — early-modern consolidation: gunpowder, commercialisation, larger territorial armies (Toungoo, Ayutthaya under Naresuan, Le–Trinh, Konbaung).

Chapter structure that I could verify from the publishers' deposited chapter records: vol. 1 = Introduction "The Ends of the Earth" (pp. 1–84); ch. "One Basin, Two Poles: The Western Mainland and the Formation of Burma" (pp. 85–211); "A Stable, Maritime Consolidation: The Central Mainland" (pp. 212–337); "'The Least Coherent Territory in the World': Vietnam and the Eastern Mainland" (pp. 338–456); "Conclusion and Prologue" (pp. 457–460). Vol. 2 = "A Far Promontory" (pp. 1–122, the recapitulation of the SE Asian argument); "Varieties of European Experience I–II" (pp. 123–370); "Creating Japan" (pp. 371–493); "Integration Under Expanding Inner Asian Influence I–II" (pp. 494–762); "Locating the Islands" (pp. 763–894). *(pp. verified; chapter numbering not certain.)*

### 1.2 Where "charter state" sits relative to mandala / galactic polity / segmentary state

The four terms answer different questions and are often used as if interchangeable. They are not.

- **Mandala** (O. W. Wolters, *History, Culture, and Region in Southeast Asian Perspectives*, ISEAS 1982; rev. edn. Cornell SEAP 1999) — a **cosmological-geographical** term: a circle of rulers around a centre, with no fixed frontier, where loyalties fade with distance. It describes the *shape of authority in space*; it says nothing about what legitimises authority in time.
- **Galactic polity** (S. J. Tambiah, *World Conqueror and World Renouncer: A Study of Buddhism and Polity in Thailand against a Historical Background*, Cambridge UP 1976, ch. "The Galactic Polity", DOI 10.1017/cbo9780511558184.007) — a **structural-functional** term modelled on the *galaxy*: a centre with satellite provinces reproducing the centre's structure at smaller scale. Tambiah's key move is that the polity is organised around the *sangha* and the *cakkavatti* ideal — so it is already close to Lieberman's charter, but described as a static morphology rather than a historical process.
- **Segmentary state** (Aidan Southall, "The Segmentary State in Africa and Asia", *Comparative Studies in Society and History* 30 (1988); idem, "The Segmentary State and the Ritual Phase in Political Economy", in *Beyond Chiefdoms*, Cambridge UP 1999) — derived from the Alur of Uganda; the polity is a **nest of replicating segments** with ritual centrality and limited practical control. Southall's own extension to India is contested; its use for SEA is largely by analogy.
- **Charter state** (Lieberman) — a **historical-institutional** term: it asks what *codified, transferable legitimation* does to a polity's survival and consolidation over centuries. It absorbs mandala and galactic-polity insights but adds (i) a text/object charter, (ii) a periodisation, (iii) a comparative programme (Japan, Europe, China, South Asia), and (iv) a causal claim about why consolidation happened when it did (monsoon-era agrarian expansion, commerce, gunpowder, intense interstate competition).

For a modeller the practical difference: mandala/galactic polity are **static equilibrium descriptions** (a hub with graded control) and can be implemented as a decay-of-authority-with-distance function. The charter state is a **dynamic claim with a memory term** — legitimacy is an inherited stock that survives the destruction of physical capital. That is directly implementable and almost never implemented.

### 1.3 The charter as an object

Lieberman's charter is deliberately abstract; the concrete referents differ by polity. My reading of what the sources support, with the caveat that Lieberman does not tabulate them this way:

- **Burmese** — the *Yazawin* chronicle tradition and the Pagan-period inscriptional corpus; the eleventh-century *Myanma Min* administrative/legal framework attributed to the Pagan court.
- **Tai / Lan Na / Ayutthaya** — origin myths and *khwan muang* (the "soul of the *muang*") ritual complexes; the *Thammasat* legal corpus, diffused from Mon Burma; the *Traiphumikatha* cosmological text as a shared charter of status hierarchy (see Chris Baker & Pasuk Phongpaichit, *A History of Ayutthaya: Siam in the Early Modern World*, Cambridge UP 2017, and their "The Palace Law of Ayutthaya and the Thammasat", Cornell SEAP 2016, DOI 10.7591/9781501725968).
- **Khmer** — the *devarāja* cult, royal temple-mountains, and the massive Sanskrit/Khmer inscription corpus. Eric Davis & Terry Lustig, "Angkorian Law and Land", in *The Angkorian World* (Routledge 2023, ch. 17, pp. 237–253) is the best short entry point on law and land as a charter in the Khmer case.
- **Cham** — Sanskrit/Pan-Austronesian charter material, but I found no synthesis I can cite with confidence; treat the Cham arm of the comparison as unmet in this review.

### 1.4 The substrate / consolidation argument

Lieberman's answer to "why did fragments consolidate?" is a bundle: (i) agrarian and demographic expansion in the monsoon-era lowlands; (ii) commercial growth, especially maritime trade feeding inland capitals; (iii) **intensified interstate warfare** as a selection pressure favouring administrative depth; (iv) the *sangha* as a cross-polity institution — a monastic network with a shared discipline, shared ordination lineage (*upasampada*) and periodic **purification** campaigns in which a ruler reformed the monkhood to demonstrate sovereignty over the charter. The Buddhist *sāsana* is thus both the charter's carrier and a rival to royal authority. Lieberman's argument is that the same charter that made states legible also produced a standing conflict between king and clergy.

### 1.5 How charter states behaved operationally

- **Succession and interregnum cycles**: frequent regicide, short reigns, contested succession by collaterals and former monks; a pattern in which the death of a strong king opens a crisis that the charter (not the dynasty) has to absorb.
- **Capital sacking and rebuilding as normal**: Ava, Pegu, Ayutthaya, Angkor and Chiang Mai were repeatedly taken and re-founded. The charter continuing across a sacking is the observable prediction.
- **Round-robin / cyclical competition** between competing capitals (Ava–Pegu–Toungoo; Angkor–Ayutthaya; Sukhothai–Ayutthaya–Lan Na). Lieberman's "One Basin, Two Poles" is the morphological description (Burma as a basin with two poles, Ava in the north and Pegu in the south).
- **Marriage alliance, vassalage, and hostage-taking** as standard instruments of control at the periphery.
- **The key emergence claim**: because legitimacy is carried by the charter rather than the capital, a defeated polity often loses its *city* while its *polity* survives — the empirical signature being an occupation hiatus at the old capital and continued rural temple/charter activity nearby.

### 1.6 Critiques

- **Synchrony problem.** Leonard Andaya, "Comments on Victor Lieberman's *Strange Parallels*", *Journal of Asian Studies* 70(4) (2011): 995–997 (DOI 10.1017/s002191181100163x) argues that for island SE Asia the "major discrepancies" in geography and social model are a fundamental impediment to Lieberman's consolidation narrative. The 2011 JAS forum (Lieberman, Wills, Mair, Hellyer, Andaya, others) is the main published critique-and-reply venue; Lieberman's "Response to Comments" is *JAS* 70(4) (2011): 999–1006.
- **Aung-Thwin** — the long-running critique from Burmese historiography, sceptical of external/comparative frames and of linking Pagan to a regional economic take-off (see Michael Aung-Thwin, *Pagan: The Origins of Modern Burma*, U. Hawai'i Press 1985; and *Myanmar in the Fifteenth Century*, U. Hawai'i Press 2017, chs. "Ava" and "The Last Decades and the Decline of Ava"). I did **not** verify a specific Aung-Thwin review of *Strange Parallels* — do not cite one without checking.
- **Type or description?** The sharpest unresolved question: is "charter state" a **regional type** (all mainland SE Asian polities had a charter) or a description of **Theravada Buddhist legitimation specifically**? If the latter, Theravada-only polities qualify and Islamised Melaka (post-1414) is out; but Ayutthaya's earlier Brahmano-Buddhist synthesis and Angkor's Hindu-then-Buddhist sequence put pressure on any clean line. A modeller should decide this explicitly, because it fixes the population of observations in the model.
- **Cliodynamics reception**: Jack Goldstone, "New Patterns in Global History: A Review Essay on *Strange Parallels*", *Cliodynamics* 1(1) (2010), DOI 10.21237/c7clio11197 — the most useful review if you want the *quantitative* reading of Lieberman, since Goldstone frames it in the same terms as Turchin's agrarian-state cycles.
- Tonio Andrade, review in *American Historical Review* 117(4) (2012): 1173–1176 (DOI 10.1093/ahr/117.4.1173) and Peter Duara's review in *Journal of Southeast Asian Studies* (DOI 10.1017/s0022463411000713) for general evaluations.

### 1.7 What of this is formalisable, and what is testable

Formalisable **now**, in a cell-based model like yours:
1. **Charter as a stock, not a state.** A legitimacy variable belonging to the *charter region*, not to any city. Cities can be destroyed; the charter stock decays slowly and can be re-instantiated at a new capital. **Testable**: after a documented sacking, does settlement continuity near temples persist while dense occupation at the old capital lapses for one to several generations? Angkor: yes (Carter et al. 2019). Ava/Pegu: yes archaeologically poor so far.
2. **Purification campaigns as a charter-maintenance cost.** A periodic fixed cost paid to keep the clergy network aligned; failing to pay it predicts a legitimacy deficit and then a succession crisis. **Testable in principle** (inscription counts, monastic land grants) but weak in practice.
3. **Multiple capitals in one basin** ("two poles"): capitals are *sites*, the charter region is the *territory*. Predicts relocation, not abandonment. **Testable**: Angkor → Longvek; Ava → Amarapura → Mandalay; Ayutthaya → Thonburi/Bangkok.
4. **Competition as selection, not just warfare**: the actor set is *other charter claimants*; competition pressures toward administrative depth. In a model this is a rival set whose success criterion is charter control, not army kills — which is precisely what your current model lacks.

Not formalisable without inventing data: marriage-alliance networks (no records for Angkor), hostage exchange, and the "purification" events themselves.

### 1.8 If you read only one thing

**Read Lieberman's 2011 AHR essay, "Charter State Collapse in Southeast Asia, ca. 1250–1400" (*AHR* 116(4): 937–963), *before* the books.** It is the compressed statement of the phase-transition argument, it is directly about *collapse* (your modelling target), and it is short enough to digest in a day. Then vol. 1 ch. 2–3 ("One Basin, Two Poles", "A Stable, Maritime Consolidation") for the Burmese and central-mainland detail, and vol. 2 ch. 1 ("A Far Promontory", pp. 1–122) for the comparative summary in Lieberman's own voice.

---

## 2. The field and its name

**The dominant label in 2020s literature is "low-density urbanism" / "low-density agrarian-based urbanism", with "agro-urbanism" as the rising alternative.** Legacy terms — "regal-ritual city", "hydraulic city", "mandala state" — survive mainly in teaching texts and in the older Angkor-specific literature.

Key anchor citations:

- **Roland Fletcher, "Low-Density, Agrarian-Based Urbanism", in *The Comparative Archaeology of Complex Societies*, ed. M. E. Smith (Cambridge UP 2011), DOI 10.1017/cbo9781139022712.013.** This is the source of the term as it is now used.
- **Lisa Lucero, Roland Fletcher & Robin Coningham, "From 'collapse' to urban diaspora: the transformation of low-density, dispersed agrarian urbanism", *Antiquity* 89(347) (2015): 1139–1154, DOI 10.15184/aqy.2015.51.** The framing paper for your problem: what looks like collapse is often **dispersal** of population and authority away from a dense core into a wide low-density landscape. This is the single most important theoretical move for a model of Angkor's decline.
- **Scott Hawken & Roland Fletcher, "A Long-Term Archaeological Reappraisal of Low-Density Urbanism: Implications for Contemporary Cities", *Journal of Urban Archaeology* 3 (2021), DOI 10.1484/j.jua.5.123674.**
- **Roland Fletcher, Kirrily White & Dan Penny, "Risk and low-density dispersed urbanism", *Frontiers in Human Dynamics* 6 (2024), DOI 10.3389/fhumd.2024.1347157.** Explicitly compares Greater Angkor and Classic Maya Caracol at >100 km², and argues that material scale and density give settlement "inertia [that] become[s] an agency in its own right". Directly comparable to the "hyper-city / dispersed city" debate.
- **Christian Isendahl & Michael E. Smith, "Sustainable agrarian urbanism: The low-density cities of the Mayas and Aztecs", *Cities* 31 (2013), DOI 10.1016/j.cities.2012.07.012.** The origin of "agrarian urbanism" as a comparative programme.
- **Alison Carter, Sarah Klassen, Miriam Stark et al., "The evolution of agro-urbanism: A case study from Angkor, Cambodia", *Journal of Anthropological Archaeology* 63 (2021): 101323, DOI 10.1016/j.jaa.2021.101323.** Note the abstract's key empirical claim: Angkor's **low-density metropolitan area and its higher-density civic-ceremonial centre grew at different rates and independently**. This is a two-component city, not one — a modelling constraint many models ignore.

Related umbrella terms and where they come from:
- *Water-based / hydraulic urbanism*: Bernard-Philippe Groslier's "hydraulic city" (§3.3); superseded but still the label for the water argument.
- *Cosmological / mandala city*: Wolters 1982; Tambiah 1976 (§1.2).
- *Regal-ritual city*: Richard G. Fox, "Urban Anthropology: Cities in Their Cultural Settings" (Prentice-Hall 1977) — an ideal type for cities whose function is royal ceremonial rather than commerce. Largely retired; still the best description of what pre-lidar Angkor was thought to be.
- *Urbanism without density / settlement agglomeration*: Michael E. Smith's comparative urbanism (e.g. *Cities: The First 6,000 Years*, 2019; and Lobo, Bettencourt & Smith, "Settlement scaling theory: Bridging the study of ancient and contemporary urban systems", *Urban Studies* 2019, DOI 10.1177/0042098019873796); George Cowgill's arguments on defining the city cross-culturally. These are the terms used when authors want to avoid committing to "low-density".
- *Segmentary state*: Southall 1988, 1999.

**Where "city" is contested for Angkor.** The argument is not semantic: it is about where the boundary of the unit of analysis is, which sets your model's spatial domain. Positions: (i) Greater Angkor as a single **settlement complex** of ~1,000 km² with no meaningful edge (Evans et al. 2007, 2013; Fletcher 2011); (ii) Angkor as a **capital region** whose urban core (Angkor Thom/Angkor Wat) is analytically distinct from its agrarian hinterland (Carter et al. 2021; Klassen & Evans 2020); (iii) Angkor as **one node in a regional network** whose "city" is better defined by catchment and road system than by built-up area (Hendrickson 2010, "Historic routes to Angkor", *Antiquity* 84, DOI 10.1017/s0003598x00066722; Hendrickson, Stark & Carter 2025). Miriam Stark's work consistently prefers "settlement complex" and refuses the density test. **Practical consequence for you:** a 140-cell model almost certainly corresponds to the *core*, not the complex; say which, and set the cell size accordingly (see §6).

## 3. Angkor: consensus and fault lines

### 3.1 The lidar revolution and what it established

- **Damian Evans et al., "A comprehensive archaeological map of the world's largest preindustrial settlement complex at Angkor, Cambodia", *PNAS* 104(36) (2007): 14277–14282, DOI 10.1073/pnas.0702525104.** Primary measurement from radar/optical survey: the built-up area is an order of magnitude larger than previously mapped.
- **Damian Evans et al., "Uncovering archaeological landscapes at Angkor using lidar", *PNAS* 110(31) (2013), DOI 10.1073/pnas.1306539110.** The CALI lidar campaign; primary measurement of mounds, ponds, roads, and the grid.
- **Miriam Stark et al., "Residential patterning at Angkor Wat", *Antiquity* 89 (2015), DOI 10.15184/aqy.2015.159**, and **Alison Carter, Piphal Heng & Miriam Stark, "Urbanism and Residential Patterning in Angkor", *Journal of Field Archaeology* 43 (2018), DOI 10.1080/00934690.2018.1503034.** Excavation-based primary measurement of house mounds and occupation density — the calibration that makes the lidar counts into people.
- **Dan Penny, Tegan Hall, Damian Evans & Martin Polkinghorne, "Geoarchaeological evidence from Angkor, Cambodia, reveals a gradual decline rather than a catastrophic 15th-century collapse", *PNAS* 116(11) (2019): 4871–4876, DOI 10.1073/pnas.1821460116.** Cores from Angkor Thom: burning, forest disturbance and erosion decline **from the first decades of the 14th century**, and the moat was no longer maintained by the end of that century (primary measurement).
- **Alison Carter et al., "Temple occupation and the tempo of collapse at Angkor Wat, Cambodia", *PNAS* 116 (2019), DOI 10.1073/pnas.1821879116.** 16 radiocarbon dates plus Bayesian modelling: occupation mounds in use 11th–13th c., a **chronometric gap** not coinciding with documented historical events, then renewed use late 14th–early 15th c. through the 17th/18th c. The temple was **never completely abandoned**.
- **Sarah Klassen & Damian Evans, "Top-down and bottom-up water management: A diachronic model of changing water management strategies at Angkor, Cambodia", *Journal of Anthropological Archaeology* 58 (2020): 101166, DOI 10.1016/j.jaa.2020.101166.** Claims autonomous temple communities are progressively **replaced by large state-sponsored agricultural units** — i.e. centralisation, not devolution, was the trajectory.
- **Martin Polkinghorne, Chhay Rachna, Piphal Heng, Damian Evans, Alison Carter et al.** on ceramic chronologies and the Angkorian world-system: see *The Angkorian World*, ed. Mitch Hendrickson, Miriam Stark & Damian Evans (Routledge 2023), a 42-chapter synthesis that is now the single best entry point in English.

### 3.2 Population: the range and what drives it

**Klassen, Carter, Evans, Ortman, Stark, Loyless, Polkinghorne & Heng, "Diachronic modeling of the population within the medieval Greater Angkor Region settlement complex", *Science Advances* 7(19) (2021), DOI 10.1126/sciadv.abf8441** gives **700,000–900,000 at the 13th-century apogee**. This is a **synthesis estimate**: lidar feature counts × excavated occupation densities × machine-learning imputation of the dated sequence.

The literature's wider range (~250,000 to >1,000,000) is driven by four choices a modeller must make explicit, because each is a free parameter:
1. **Occupation density per mound** (people per house-mound) — from excavation at Angkor Wat/Ta Prohm; Carter et al. 2018, Stark et al. 2015.
2. **Fraction of lidar-visible mounds occupied simultaneously** — the crucial unknown; Klassen et al. convert dated groups into a curve.
3. **The boundary of the counted area** — 1,000 km² "Greater Angkor" vs the ~35 km² walled core; a factor of several on its own.
4. **Ethnohistoric analogy** — Zhou Daguan's 13th-century account and 19th–20th c. Cambodian household sizes. This is where the upper tail of the range comes from.

**Guidance for the model:** use 700k–900k (Klassen et al. 2021) as the apogee central case and report sensitivity across 400k–1.2M. Your 140-cell model almost certainly cannot hold 800k people at realistic densities; check the implied density before anything else.

### 3.3 The hydraulic city debate

- **Groslier's hypothesis** (Bernard-Philippe Groslier, "*La cité hydraulique angkorienne*", *Bulletin de l'École française d'Extrême-Orient* 66, 1979) — the state's water system was intensive irrigation supporting two or three rice crops a year and thus a very large population. **This is the position to test, not assume.**
- **Against**: the system is now generally read as a **flood-recession / drainage / storage** system rather than irrigation. See **Terry Lustig, Julia Chevance & W. Johnson, "Angkor as a 'Cité Hydraulique'?", in *The Angkorian World* (Routledge 2023), ch. 15, pp. 216–233**, and **Roland Fletcher, "An opinion on issues for future investigation of the water management of Greater Angkor", *WIREs Water* 7 (2020), DOI 10.1002/wat2.1474**. Klassen & Evans 2020 gives the two-layer model (state infrastructure + thousands of household ponds and community temples).
- **The 2012–2023 decline evidence**: Penny et al. 2019 (moat unmaintained by end of 14th c.); Evans, Polkinghorne & Fletcher, "Perspectives on the 'Collapse' of Angkor and the Khmer Empire", in *The Angkorian World* ch. 37, pp. 541–553; Penny & Fletcher, "Scale and Impact in Southeast Asia", in *Sustainability and Water Management in the Maya World and Beyond* (2022), DOI 10.5876/9781646422326.c009.
- **The most modeller-relevant paper in the whole Angkor literature**: **Dan Penny, Cameron Zachreson, Roland Fletcher, David Lau, Joseph Lizier, Nicholas Fischer, Damian Evans & Christophe Pottier, "The demise of Angkor: Systemic vulnerability of urban infrastructure to climatic variations", *Science Advances* 4(10) (2018), DOI 10.1126/sciadv.aau4029.** They convert the archaeological water network into a **numerical (topological) model** and show **cascading, abruptly-thresholded failure under flooding**. This is the one published Angkor *model* — and it models infrastructure topology, not demography or economy.

### 3.4 Climate

**Brendan Buckley, Kevin Anchukaitis, Dan Penny, Roland Fletcher, Edward Cook, Masami Sano, Le Canh Nam, Aroonrut Wichienkeeo, Ton That Minh & Truong Mai Hong, "Climate as a contributing factor in the demise of Angkor, Cambodia", *PNAS* 107(15) (2010): 6748–6752, DOI 10.1073/pnas.0910827107.** Tree-ring (Fokienia hodginsii) reconstruction: a **megadrought sequence in the mid-14th century with two severe droughts separated by unusually intense monsoon years**. Note the precise claim: *contributing factor*, with the water network as the *mechanism of vulnerability* (hence Penny et al. 2018's follow-up).

Critiques: **Victor Lieberman** (in *Strange Parallels* and the 2011 AHR essay) and **John Miksic** have argued that climate cannot be the operative cause where polities with similar climate weathered similar anomalies; the counter-argument is that vulnerability is a matter of **infrastructure design**, which is testable. The strongest form of the critique for your purposes: **climate is a shock, not a trend** — a purely climate-driven model produces synchronous collapse across polities, which did not happen (Pagan, Angkor and Ayutthaya decline on different schedules).

### 3.5 Religion and the temple economy

- **The endowment form**: royal foundations (Ta Prohm, Preah Khan) carried inscriptional lists of hundreds to thousands of bonded labourers, land, and rice obligations — **primary documentary measurement**, in the *Corpus of Khmer Inscriptions* and in the analyses of Piphal Heng & Sahai, "The Temple Economy of Angkor", and Lustig, Cremin & Lustig, "Angkor's Economy", in *The Angkorian World* (chs. 23 and 22).
- **Eleanor Mannikka, *Angkor Wat: Time, Space, and Kingship* (U. Hawai'i Press 1996)** — the cosmological-metrological reading of Angkor Wat, including the strong (and contested) argument that the temple encodes solar/royal calendars. Treat the metrology as **proposed**, not established.
- **Implication for a model that is almost never implemented**: temple endowments are a **fiscal substitute** — and a competing one. Land and labour dedicated to a temple are not available to the state. Whether the religious economy was a net extractive or net productive institution is unresolved, and it is formalisable (§5).

### 3.6 Warfare, the Tai and Ayutthaya raiding

Conventional narrative: repeated Tai/Ayutthaya raids, culminating in the 1431 sack of Angkor. **Brotherson, "Warfare and Defensive Architecture in the Angkorian World", in *The Angkorian World* ch. 18, pp. 254–271**, is the current survey. The revisionist case (Penny et al. 2019; Carter et al. 2019; Evans et al. 2023) is that **the decline predates the invasion by a century or more** and the city was not abandoned in 1431. Note the unfalsifiability trap: if decline precedes the raid, the raid cannot be its cause — but models that include raiding usually let it cause decline anyway.

### 3.7 Resilience / system-collapse framing

Lucero, Fletcher & Coningham 2015; Penny et al. 2018 (thresholds, cascading failure); Fletcher, White & Penny 2024 (risk and robustness of low-density networks). The current consensus position is best summarised as: **protracted transformation with a 14th-century inflection, driven by infrastructural vulnerability interacting with climatic variability and political fragmentation, with the capital shift south by the 15th–16th century.** "Collapse" is retained only in scare quotes.

## 4. Comparators: what makes them the same and different

**The critical point for you:** Angkor is the *only* case in this set with city-scale lidar, systematic mound excavation, and a quantitative demographic model. Everything else is either documentary history, monument survey, or small-scale excavation. Any model validated only on Angkor is validated on n = 1.

**Bagan (Pagan), Myanmar.** c. 1044–1287 under the Pagan dynasty; the plain holds >2,000 surviving brick monuments — **primary measurement of monuments, not of settlement**. Sources: Michael Aung-Thwin, *Pagan: The Origins of Modern Burma* (U. Hawai'i Press 1985); Tilman Frasch, "Pagan (Bagan)", *Oxford Bibliographies in Buddhism* (2012), DOI 10.1093/obo/9780195393521-0022; Bob Hudson, "Restoration and reconstruction of monuments at Bagan (Pagan), Myanmar (Burma), 1995–2008", *World Archaeology* 40(4) (2008), DOI 10.1080/00438240802453195; Hudson, "Myanmar (Burma): Archaeological Heritage and Its Management", *Encyclopedia of Global Archaeology*. Hudson's **earthenware chronology** is the main attempt to date non-monumental occupation at Bagan — but it is a ceramic sequence, not a demographic curve. **Decline:** conventionally the Mongol incursions of the 1280s–1290s, plus a shift of the Irrawaddy channel and of trade routes; Aung-Thwin disputes the weight given to the Mongols and treats the "decline" as institutional fragmentation. **Data comparability with Angkor: low.** No lidar-derived population model; monument counts are not people.
- Also: Gyles Iannone, "Entanglement and Disentanglement at the Medieval Capital of Bagan, Myanmar", in *Detachment from Place: Beyond an Archaeology of Settlement Abandonment* (2020), DOI 10.5876/9781646420087.c010 — the most useful framing paper, because it treats Bagan's "abandonment" as **disentanglement**, i.e. the same process Lucero et al. call urban diaspora.

**Inwa/Ava, Pegu (Bago), and the later Burmese capitals.** The classic cycle literature: Lieberman, *Strange Parallels* vol. 1, ch. 2 ("One Basin, Two Poles") and vol. 2; Michael Aung-Thwin, *Myanmar in the Fifteenth Century* (U. Hawai'i Press 2017), chs. "Ava" and "The Last Decades and the Decline of Ava". The structural pattern is a **two-pole oscillation** between a northern dry-zone capital (Ava/Inwa, Amarapura 1783, Mandalay 1859) and a southern delta-facing capital (Pegu, then Toungoo), with repeated destruction and re-foundation. **Excellent for testing the charter hypothesis** (a polity repeatedly loses its capital and reconstitutes), **poor for testing settlement density**: there is no equivalent of the Angkor lidar.

**Ayutthaya (Thailand).** Chris Baker & Pasuk Phongpaichit, *A History of Ayutthaya: Siam in the Early Modern World* (Cambridge UP 2017), DOI 10.1017/9781108120197 — the standard synthesis, and explicitly a **riverine/port-polity** account (wealth from maritime trade and Chinese demand, not from agrarian surplus alone). Sacked by the Burmese in **1569 and again in 1767**; after 1767 the capital moved to Thonburi and then Bangkok. **The live question is whether the 1767 destruction is military or the trigger for a structural relocation already under way** — structurally analogous to the 1431 Angkor question, and the comparison is worth making explicitly in the model. **Data: archival and cartographic; some excavated canals and kilns. No settlement-wide demographic model.**

**Chiang Mai / Lan Na.** Sarasawadee Ongsakul, *History of Lan Na*, trans. Chitraporn Tanratanakul (Silkworm Books, 2005) — the standard English account. Volker Grabowsky (ed.), *Regions and National Integration in Thailand, 1892–1992* and his Lan Na manuscript work, for the *muang* system and its administration. The **Tai *muang*** is the key structural unit: a fortified, moated lowland centre with a *chao muang* and a dependent hinterland — the closest thing in this set to a directly modelable **site hierarchy**, because moated *muang* are visible in aerial imagery and lidar-adjacent survey. **Data: moderate, monument and moat survey; little excavation-based demography.**

**Anuradhapura / Polonnaruwa (Sri Lanka).** The best-developed "collapse scepticism" literature in the tropics: Robin Coningham & Prishanta Gunawardhana, *Anuradhapura: Volume III: The Hinterland* (BAR 2013, DOI 10.30861/9781407311890); Keir Strickland, *A Time of Change: Questioning the "Collapse" of Anuradhapura, Sri Lanka* (Archaeopress 2017, DOI 10.2307/j.ctv1pzk1cj); Gilliland et al., "The dry tank: development and disuse of water management infrastructure in the Anuradhapura hinterland, Sri Lanka", *Journal of Archaeological Science* 40 (2013), DOI 10.1016/j.jas.2012.09.034 (the key hydraulic-decline study, **primary measurement** of tank sedimentation); Coningham, Gunawardhana, Manuel et al., "The state of theocracy: defining an early medieval hinterland in Sri Lanka", *Antiquity* 81 (2007), DOI 10.1017/s0003598x00095673. Manuel, Gunawardhana, Namalgamuwa et al., "Low-Density Urbanism in Medieval Sri Lanka: Exploring the Hinterland of Polonnaruva", *Asian Perspectives: The Journal of Archaeology for Asia and the Pacific* (U. Hawai'i Press) 60 (2021), DOI 10.1353/asi.2021.0002 — finds Polonnaruva's settlements "larger, longer-lasting, and more evenly distributed" than Anuradhapura's, and calls **both** low-density urbanism. Also Coningham, Davis & Gunawardhana, "From village to state, and back again: cycles of de-urbanization and adaptation in Early Historic and Medieval Sri Lanka", *World Archaeology* (2025/26, DOI 10.1080/00438243.2026.2664414). **Data comparability: good on hinterland survey and chronology; weaker than Angkor on lidar-scale mapping.** Best comparator for the "decline is not collapse" claim.

**Summary table of data availability:**

| Case | Settlement-scale mapping | Excavation-based demography | Quantified decline chronology | Comparable to Angkor? |
|---|---|---|---|---|
| Greater Angkor | lidar, full | yes | yes (cores + ¹⁴C) | — |
| Anuradhapura/Polonnaruwa | hinterland survey | partial | yes (tank sediments) | closest |
| Bagan | monument survey only | minimal | weak | no |
| Ayutthaya | cartographic | partial (canals) | weak | no |
| Chiang Mai / Lan Na | moat/monument survey | minimal | weak | no |
| Inwa/Pegu | minimal | minimal | documentary only | no |

## 5. What has actually been modelled

**Short answer: almost nothing, and nothing of Angkor's economy or demography in a dynamic simulation. The field is wide open.**

### 5.1 Angkor-specific models

- **Penny et al. 2018, *Science Advances* 4(10), DOI 10.1126/sciadv.aau4029** — the *only* numerical model of Angkor I could verify. It is a **topological network model** of the water infrastructure under flood forcing, showing threshold behaviour and cascading failure. It has no population, no economy, no labour, no politics. **It is the closest prior art and it is not a competitor.**
- **Klassen et al. 2021, DOI 10.1126/sciadv.abf8441** — a *statistical* reconstruction (imputation + machine learning over dated lidar features), not a dynamic model. No causal mechanism.
- **Klassen & Evans 2020, DOI 10.1016/j.jaa.2020.101166** — a diachronic reconstruction of temple-community foundation order, explicitly a "model" in the weak, descriptive sense.
- I found **no** published agent-based, system-dynamics, or mathematical model of Angkor's economy, labour allocation, or polity — and no published model of Southeast Asian tropical urban decline of any kind. Treat any claim to the contrary with suspicion.

### 5.2 Methodologically relevant models from other regions

- **MayaSim** — Scott Heckbert, "MayaSim: An Agent-Based Model of the Ancient Maya Social-Ecological System", *Journal of Artificial Societies and Social Simulation* 16(4): 11 (2013), DOI 10.18564/jasss.2305. An integrated **agent-based + cellular automata + network** model coupling population, agricultural production, soil degradation, climate variability, hydrology, forest succession and the stability of trade networks, with agents developing settlements on a responsive landscape. Heckbert states explicitly that the model "reproduces spatial patterns and timelines *somewhat* analogous" to the Maya and "requires refinement and further archaeological data for calibration". **This is the closest structural template to what you are building, and note that even its author claims only weak validation.** Follow-up: Kühlein, Soliev, Donges et al., "Social tipping towards revolution? New perspectives for the MayaSim model", EGUsphere 2025 (abstract only — conference-abstract level, do not over-cite).
- **Kohler et al., "Modelling prehispanic Pueblo societies in their ecosystems", *Ecological Modelling* 241 (2012): 30–41, DOI 10.1016/j.ecolmodel.2012.01.002** — the Village Ecodynamics Project; agent-based households on a real landscape with maize yields, hunting, and household fission/fusion. The methodological gold standard for "model the subsistence constraint first." Also Varien & Ortman's accumulations research (*World Archaeology* 2005, DOI 10.1080/0043824042000329603) — how to turn refuse and mound volume into people.
- **Settlement scaling**: Ortman, Cabaniss, Sturm & Bettencourt, "Settlement scaling and increasing returns in an ancient society", *Science Advances* 1(1) (2015), DOI 10.1126/sciadv.1400066; Lobo, Bettencourt & Smith, *Urban Studies* (2019), DOI 10.1177/0042098019873796. Provides **testable superlinearity of productivity / sublinearity of infrastructure per capita** — a constraint on what growth rates are physically possible. Not yet applied to Angkor; an obvious extension.
- **Turchin's agrarian-state dynamics**: Peter Turchin, "Dynamical Feedbacks between Population Growth and Sociopolitical Instability in Agrarian States", *Structure and Dynamics* 1(1) (2005), DOI 10.5070/sd911003259; Turchin & Gavrilets on cultural macroevolution. These give the classic **demographic-structural cycle**: population growth → elite overproduction and land scarcity → instability → collapse → renewed growth. **This is the mechanism set your simulation is missing** (it has no elite class and no land market).
- **Seshat**: the Seshat Global History Databank's state-formation regressions are cross-sectional/correlational, not dynamic. I did not locate a Seshat paper specific to SE Asia; do not claim one.
- **"Simulation as hypothesis" / model-based archaeology**: Fletcher's own methodological position is that a model is a hypothesis to be broken. On the formal side, **Mark Lake, "Trends in Archaeological Simulation", *Journal of Archaeological Method and Theory* 21 (2014), DOI 10.1007/s10816-013-9188-0** is the standard review (I am confident this exists; page numbers not verified). The relevant claim for you: simulation is epistemically useful only when framed as **discriminating between named hypotheses**, not as a "realistic" reconstruction.

### 5.3 What mechanisms are formalised, and what are not

| Mechanism | Formalised anywhere? |
|---|---|
| Subsistence / caloric constraint | Yes — Kohler et al., MayaSim |
| Population–instability feedback | Yes — Turchin (ODE level) |
| Soil degradation | Yes — MayaSim |
| Infrastructure failure cascades | Yes — Penny et al. 2018 |
| Trade network stability | Partly — MayaSim |
| **Temple endowment as labour allocation** | **No published model** (to my knowledge) |
| **Bonded/temple labour and corvée competition** | **No** |
| **Charter legitimacy as an inherited, relocatable stock** | **No** |
| **Raiding as a labour-capture mechanism** | **No** (raiding appears in some models as exogenous mortality only) |
| **Elite land consolidation** | Only generically (Turchin's elite dynamics) — not spatially in SEA |

Two of these rows (temple endowments, charter as a stock) are the genuinely novel modelling contributions available to you.

## 6. Testable propositions

Each proposition names the mechanism, states the refuting observation, and grades data availability as **A** (testable in the Greater Angkor record now), **B** (testable in a comparator), **C** (not currently testable).

**P1. Food-balance feasibility.** *Mechanism: the subsistence constraint.* Angkor's peak population was supportable from the rice produced within its catchment at the yields in §8, so the model must not require net grain import. **Refuted if** modelled per-capita production × harvested area at plausible yields (1.0–2.5 t/ha paddy) cannot reach 200–250 kg paddy/person/year for 700–900k people within ~1,000 km² of cultivated land. **Grade A** (yield range is the weak link, not the demography).

**P2. Scale-dependency of water infrastructure.** *Mechanism: rising marginal cost of maintenance.* The per-capita maintenance/sediment-clearing cost of the water network rose faster than the returns because length and sluice count scaled with area while the labour available scaled with population, so the network's *cost per hectare* should be higher in later, larger phases. **Refuted if** lidar-measured network length per unit population is flat or falling through the 11th–14th centuries. **Grade A** — this is measurable from the lidar network plus Klassen et al.'s dated population curve, and it is the single most valuable test in this list.

**P3. Elite land consolidation vs household autonomy.** *Mechanism: institutional drift.* State-sponsored agricultural units progressively displace autonomous temple communities (Klassen & Evans 2020's claim), implying a monotonic rise in the share of land under state/elite control until the 13th century. **Refuted if** the dated foundation sequence of community temples shows no decline in independent foundations, or if state-unit foundations are contemporaneous with rather than succeeding community ones. **Grade A** (Klassen & Evans already have the data; their conclusion is falsifiable with their own dataset).

**P4. Religious endowment as a fiscal substitute.** *Mechanism: labour tied in perpetuity.* Temple endowments (inscriptional lists of bonded labour, land and rice obligations) removed labour permanently from the royal pool, so periods of heavy royal endowment should coincide with *lower* state corvée capacity per capita and rising reliance on warfare for labour. **Refuted if** endowment volume and state construction volume co-vary positively with no labour-supply bottleneck. **Grade B** — inscriptional corpus is good but the labour-force denominator is unknown.

**P5. Raiding as labour supply — and its unfalsifiability problem.** *Mechanism: capture of people, not territory.* Tai/Ayutthaya campaigns were slave raids for population, so captured labour should raise the victor's production and depress the victim's, and raiding intensity should respond to the raider's *labour deficit*, not to the victim's wealth. **Refuted if** the raiding record (chronicle-dated campaigns) shows no correlation with the victim's population trend or the raider's labour demand. **Grade C for Angkor** (the campaign chronology is thin and chronicle-dependent) — and note the trap: as currently modelled, raiding has "almost no effect on anything", which is *consistent* with the historical record if raiding is epiphenomenal. **Do not tune raiding to produce the decline; that is the definition of an unfalsifiable mechanism.** Best treatment: raiding as a *noise term*, and report whether the model's decline survives its removal.

**P6. Climate as shock vs structure.** *Mechanism: threshold vulnerability, not climate trend.* Because Buckley et al. (2010) shows *two* droughts bracketing an intense monsoon in the mid-14th century while Penny et al. (2019) shows land-use decline beginning in the first decades of that century, the decline must be **structurally underway before the drought**. **Refuted if** the model's decline only occurs when the drought is switched on, or if a structurally sound system fails under the same climate series. **Grade A** — the chronology constraint is hard and the data exist.

**P7. Decline as phase vs slow redistribution.** *Mechanism: urban diaspora (Lucero, Fletcher & Coningham 2015).* Decline should be a **redistribution of population within the charter region** with continued rural and temple occupation, not a net loss. **Refuted if** regional (not just core) population falls, or if out-migration from the core is not matched by growth elsewhere in the catchment. **Grade A** — the tests are cores (Penny et al. 2019) plus Carter et al.'s (2019) Angkor Wat hiatus, and both already point the right way.

**P8. Charter persistence.** *Mechanism: legitimacy as a relocatable stock.* The polity should survive the loss of its capital: after the 15th-century shift, charter institutions (monastic foundations, royal inscriptions, temple maintenance) continue within a generation. **Refuted if** charter activity ceases at the old core with no successor within ~50 years. **Grade A** — Post-Angkor/Longvek work (Polkinghorne & Sato in *The Angkorian World* ch. 40; "Mainland Southeast Asia After Angkor" ch. 39) is the evidence base.

**P9. Two-component growth rates.** *Mechanism: independent drivers.* Carter et al. (2021) claim the low-density metropolitan area and the dense civic-ceremonial centre grew at *different rates and independently*; therefore a single-population model is misspecified. **Refuted if** a one-pool model reproduces both the mound-dating sequence and the monument-construction sequence. **Grade A** — the dating corpus exists.

**P10. Monsoon/flood non-linearity.** *Mechanism: cascading infrastructural failure (Penny et al. 2018).* Damage should be **threshold-like** in flood magnitude rather than linear. **Refuted if** simulated damage scales smoothly with flood size. **Grade A** — and this is a *pure model* proposition, i.e. testable right now against your own simulation.

**P11. Yield-regime sensitivity.** *Mechanism: deepwater vs transplanted paddy (see §8).* If Angkor's water regime was flood-recession/floating rice (~1.0–1.6 t/ha) rather than transplanted irrigated rice (~1.8–2.5 t/ha), the maximum supportable population in the catchment roughly halves. **Refuted if** the archaeobotanical and sedimentary record shows transplanted, non-photoperiod-sensitive rice as the dominant regime. **Grade B** — currently unresolved (§8).

**P12. Succession-cycle signature.** *Mechanism: elite overproduction / succession crisis.* If reign length distributions in the inscriptional record show the characteristic short-reign, high-regicide pattern of charter states (Lieberman; Turchin 2005), then the polity's instability is endogenous, not climatic. **Refuted if** reign lengths are stable through the apogee and only change at the 14th-century inflection. **Grade B** (Khmer royal chronology is reasonably known; ~40 reigns is a small sample).

## 7. Rice yields: the pre-Green Revolution baseline

*This section tests the hypothesis rather than confirming it. Verdict up front: the pre-GR baseline (roughly **1.2–2.2 t/ha paddy** for rain-fed, non-irrigated, traditional varieties in mainland SE Asia) is a **defensible** analogue, but there is a real possibility that Angkor sat at the **low end** of it because its water regime was flood-recession/deepwater rather than transplanted. If your model uses ~1.6 t/ha it is inside the plausible band; if it uses anything above ~2.5 t/ha it is almost certainly too high for a pre-modern extensive system.*

### 7.1 What the archaeobotany actually shows

- **Cristina Castillo, Alison Carter, Eleanor Kingwell-Banham, Yijie Zhuang, Alison Weisskopf, Chhay Rachna, Piphal Heng, Dorian Fuller & Miriam Stark, "The Khmer did not live by rice alone: Archaeobotanical investigations at Angkor Wat and Ta Prohm", *Archaeological Research in Asia* 24 (2020): 100213, DOI 10.1016/j.ara.2020.100213.** Macroremains + phytoliths from **residential contexts inside temple enclosures**; the finding is that multiple crops (including legumes, cucurbits, palms, and possibly millets) supplemented rice, and that plants were grown for ritual/medicinal as well as dietary use. **This is a primary measurement, and it undercuts any single-crop calorie model.** (Open-access copy deposited on Zenodo, record 4051022.)
- **Dorian Fuller & Cristina Castillo, "Cereals of Southeast Asia", in *The Oxford Handbook of Early Southeast Asia* (Oxford UP 2022), pp. 299–320, DOI 10.1093/oxfordhb/9780199355358.013.19.** The regional baseline: rice has been the dominant cereal for ~3,500 years, but the *Oryza sativa japonica* / *indica* / *aus* division and its introduction history across the mainland is still being worked out. **The key admission: the archaeobotanical record is thin and dominated by charred grains and impressions in pottery, not by field-context assemblages.**
- Early sites with rice evidence (Angkor Borei, Phum Snay, Ban Chiang, Khok Phanom Di) mostly yield **charred grains from storage or refuse contexts, and rice temper/impressions in ceramics** — not residues of a field system. **Consequence: you cannot infer field yields from grain morphology.** Grain shape separates *indica*/*japonica* imperfectly and says nothing about spacing, transplanting, manuring, or water regime. Anyone claiming "the grains show a yield of X" is over-reading.

### 7.2 The pre-1960 baseline

I could not obtain the FAO/IRRI historical series directly in this session (FAOSTAT is JavaScript-gated and the historical series is not exposed as a plain JSON endpoint). What follows is what the literature I could verify supports, with **honest ranges and explicit gaps**:

- **Burma (1930s)**: the delta rice frontier; the standard characterisation is of **extensive, low-input, broadcast/transplanted monsoon paddy at roughly 1.0–1.8 t/ha** on the delta fringe, with higher values in long-settled dry-zone tracts. **Source: Michael Adas, *The Burma Delta: Economic Development and Social Change on an Asian Rice Frontier, 1852–1941* (U. Wisconsin Press 1974; reissued 2011, DOI 10.2307/jj.36032635)** — read for the qualitative system; I did **not** verify a specific quoted yield figure in it.
- **Thailand pre-1960**: widely cited as **~1.4–1.8 t/ha** for the central plain, lower in the northeast (Khorat) at **~1.0–1.3 t/ha**. I did not find a citable primary source in this session — treat as an **assumption needing a source** (best candidate: the FAO *Production Yearbook* series from 1952 onward, and the older *International Yearbook of Agricultural Statistics*, which give country yields from ~1948).
- **Cambodia 1930s–1950s**: French colonial agricultural statistics report Cambodia's rice yields in the same order of magnitude, **~1.0–1.5 t/ha**, with the takeo/battambang areas higher. Again: I did not verify a specific table; flag as an assumption.
- **Comparative historical figure**: T. Watabe & K. Kawaguchi, "Increasing the Rice Yield in South and Southeast Asia", *Asian Survey* 8 (1968), DOI 10.2307/2642080 — contemporaneous survey of the pre-GR yield problem in the region. Useful for the *level* and the stated reasons for it (no fertiliser, no certified seed, single monsoon crop).

**Critical distinction to keep straight in the model:** *paddy* (unmilled rough rice) vs *milled* rice. Milling recovery is conventionally **~0.60–0.67**; i.e. 1 tonne of paddy yields ~620–670 kg milled. Quoting a "rice yield" without saying which of these is meant is the most common error in this literature.

### 7.3 The Green Revolution break

Semidwarf varieties (IR8, released by IRRI in 1966, and successors) roughly **doubled through tripled** tropical Asian yields where irrigation and fertiliser were available, taking main-season irrigated yields to **~3.5–6 t/ha** by the 1980s. The break is therefore roughly a factor of 2–3, and it is **irrigation-and-fertiliser-dependent** — not a change in the crop's genetic potential under rain-fed conditions. **Implication for you: do not back-project Green-Revolution yields, and do not treat 1950s figures from an irrigated district as typical of Angkor.**

### 7.4 Deepwater vs transplanted — the big uncertainty for Angkor

There is **no ancient DNA or archaeobotanical study I could verify that identifies floating/deepwater rice at Angkor specifically.** What can be said:
- The Angkorian water system is now widely read as **storage/drainage/flood-recession, not irrigation** (§3.3: Lustig, Chevance & Johnson 2023; Fletcher 2020). That is the consensus shift away from Groslier.
- Deepwater/floating rice (photoperiod-sensitive, elongating with flood depth) yields **very low per hectare — roughly 0.8–1.8 t/ha** and often only one crop, but it is *robust* to a variable flood.
- Transplanted photoperiod-sensitive monsoon rice without irrigation yields **~1.5–2.5 t/ha** and requires reliable water depth control and substantially more labour (transplanting is labour-intensive — directly relevant to a corvée/bonded-labour model).
- **Therefore the agronomic argument cuts against the user's hypothesis on the low side**: if Angkor ran a flood-recession system, the appropriate yield is nearer **1.0–1.6 t/ha**, not the ~1.6–2.0 that a transplanted-rainfed analogy would suggest.

### 7.5 The best-supported number for the model

**Point estimate: 1.5 t/ha paddy (unmilled), range 1.0–2.2 t/ha.** Grading:
- The *level* (pre-modern, low-input, single monsoon crop) is **well supported by analogy** to pre-1960 regional yields.
- The *position within the range* is **not measured** for Angkor. Nothing in the archaeobotanical record fixes it.
- Variance is dominated by **agronomic variables** (water regime, transplanting, variety, soil), not by statistical uncertainty. A ±30% band is honest; a tighter one is false precision.
- **Assumption to state in the paper:** "1.5 t/ha paddy, with sensitivity analysis at 1.0 and 2.2."

### 7.6 Per-capita demand

For the food-balance constraint, the literature-plausible range is:
- **Paddy: 200–250 kg/person/year** for a rice-dominant diet with minimal animal protein; **150–180 kg** where fish, vegetables and other cereals substitute (which Castillo et al. 2020 says they did at Angkor).
- **Milled equivalent: ~100–180 kg/person/year** (at 0.62–0.67 recovery).
- **Recommended model default: 200 kg paddy/person/year**, with sensitivity at 150 and 250. This, not the yield, is usually where models go structurally negative: 200 kg/person/year × 800,000 people = 160,000 t paddy/year, which at 1.5 t/ha requires **~107,000 ha of paddy under cultivation in any given year** — about 1,070 km², i.e. **the entire notional area of Greater Angkor, with no fallow, no seed, no loss, and no other land use.** That arithmetic, not the army, is where your model's structural grain deficit almost certainly comes from: **either the population is too high, the yield too low, the catchment too small, or double-cropping is being implicitly assumed.**

## 8. The "so what" for a modeller

A model of Angkor's rise–peak–fall should include exactly four coupled stocks and one memory term. **Stocks:** (1) population, split into household cultivators, bonded/temple labour and the royal/military levy — because the literature's central institutional claim is that these were *competing claims on the same people*; (2) cultivated land, with a yield function that makes the flood-recession regime explicit (1.0–2.2 t/ha paddy, penalised where water depth is uncontrolled); (3) a water-infrastructure stock with a **maintenance requirement that scales superlinearly with network extent** (P2) and a **threshold flood-damage function** (Penny et al. 2018's cascading failure); (4) a legitimacy/charter stock that belongs to the *region* rather than the capital and that permits relocation rather than extinction. **The memory term** is the charter — it is what lets the polity lose the city and keep existing, and it is the one mechanism in the literature that no published model implements. Couple them with the Turchin-type demographic-structural feedback (population → land scarcity → elite competition → instability) so that decline can arise *endogenously* from growth, not only from an exogenous shock. Test it by P1, P2, P6 and P7, which are all adjudicable from existing data.

It should **deliberately leave out**: individual-agent psychology and household-level decision rules finer than "cultivator / bonded / levied" (no data, and it invites over-fitting to a single excavated enclosure); the monument-building sequence as a *target* (it is an output of the model at best, and it is the variable most vulnerable to survivor bias); raiding as a *causal driver* (P5 — it is unfalsifiable at Angkor's documentary resolution and should enter as a noise term whose removal must not change the conclusion); a detailed hydrological simulation of the whole network (Penny et al. 2018 already did that and did it well — cite it and take its threshold result as a given); and any pretence of calendar-year prediction. The model's claim should be *conditional and comparative*: given the pre-GR yield band and the 700–900k apogee, which mechanism set produces a 13th-century peak and a 14th-century inflection, and which does not. That is falsifiable. "It matches Angkor" is not.

---

## Sources I could not verify (do not cite without checking)

- Any specific FAO/IRRI table of pre-1960 Cambodian, Thai or Burmese rice yields by district — I did not reach a primary table in this session. The 1.0–1.8 t/ha ranges above are **literature-supported estimates flagged as assumptions**, not verified measurements.
- Any ancient-DNA or phytolith-based identification of deepwater/floating rice at Angkor. I found none; §7.4's argument is agronomic inference from the water-regime literature, not from plant remains.
- Michael Aung-Thwin's or David Wyatt's specific reviews of *Strange Parallels* — I verified the JAS 2011 symposium (Andaya, Hellyer, Wills, Mair, Ricklefs, Lieberman) but not Aung-Thwin or Wyatt reviews. Do not attribute one.
- Mark Lake's *JAMT* review of archaeological simulation (DOI 10.1007/s10816-013-9188-0) — I am fairly confident it exists but did not open it; page numbers unverified.
- A Seshat-based state-formation paper specific to Southeast Asia — I found none.
- Groslier 1979 *BEFEO* 66 — cited from the secondary literature on the "hydraulic city"; I did not verify the volume/pages directly.
- Chapter numbers in *Strange Parallels* vol. 1 — chapter titles and page ranges verified from publisher records; the ordinal numbering is not.
