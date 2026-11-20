# MANUSCRIPT COMPARISON — June draft vs October revision (and the intermediate drafts)
**Compiler:** lit-archivist · 2026-11-20 · task-1

## 0. What I actually compared (verified file relationships)

| File | Path | Lines | sha256 |
|---|---|---|---|
| **June draft** — "Massification and its Mechanisms: Credential Pipelines as Convergent Evolution", single author, working paper June 2026. Extracted from `massification(final)7.docx` sent to Bjorn 2 June 2026 | `00_handoff/papers/01_june_bjorn.txt` | 196 | — |
| **October draft** — "…Credential Pipelines, Compression Technology, and the Formal Economy Threshold", Menefee & Nordtveit, revised October 2026 | `00_handoff/papers/02_october_massification.md` | 377 | — |
| **Oct 25 repo paper** — same title | `01_sources/massification_project/paper/Massification_and_Its_Mechanisms.md` | 377 | **byte-identical to the Oct 20 handoff version** (diff after trailing-whitespace normalisation = **0 lines**). No action needed; there is no "two Octobers" problem. |
| Intermediate v1 — "July 4 original" | `…/paper/previous_versions/v1_July4_original.md` | 272 | — |
| Intermediate v2 — "case-centered Oct 24" | `…/paper/previous_versions/v2_case_centered_Oct24.md` | 371 | — |

**Lineage, established by token-overlap (5+ letter words) and section presence:**
- June → v1: only **44%** of June's vocabulary appears in v1 ⇒ the June draft is a *different, shorter text*, not an early cut of v1.
- v1 → v2: **96%** overlap ⇒ v2 is a revision of v1, not a rewrite.
- v2 → October: **75%** overlap ⇒ October = v2 + further revisions.
- **The two agent-based models first appear in v2.** v1 has zero occurrences of "Formalizing / agent-based / Appendix: Model"; v2 has 7. So the computational core is an **October addition**, not a revision of June material.
- `CHANGES.md` in the repo describes the July 4 → Oct 24 revisions and is consistent with this lineage.

**Consequence for how to read the comparison:** June and October are not two drafts of one paper. June is a **theoretical/conceptual paper about world culture theory**; October is a **mechanism paper with two computational models and a country case**. Roughly 58% of June's distinctive vocabulary does not appear in October at all.

---

## 1. Structural change: what was cut, what was added

### Cut between June and October (whole sections / apparatus)
1. **The *keju* as "proof of concept"** (June §"The Keju as Proof of Concept", ~7 paragraphs: Sui→1905, xiucai/juren/jinshi tiers, 1657 Jiangnan scandal, Rawski's near-miss population, Korea's gwageo 958 CE, Vietnam's khoa cử, Japan as partial exception). **Zero occurrences of "1,300", Elman, Rawski, or keju in October.** The strongest rhetorical argument in June is gone.
2. **Developmental capital as a research program** (June §: Scribner & Cole's Vai study, Heyes' cognitive gadgets, Flynn Effect at 3 IQ pts/decade, Mousley et al.'s 9/32/66/83-year topological turning points, the ~15,000 hours figure, and the explicit anti-hereditarian argument). October contains **none** of Mousley, Heyes, Rawski, or the neuroimaging material; Scribner & Cole survive once, in a footnote, as *supplementary support* for the human-capital component, not as a research program.
3. **Thick vs thin institutions** (June's central metatheoretical move: the four-criterion structural-ecological definition of thickness, environmental ministries/diversity offices/TQM as the "thin" comparators, boot camp as the formatting parallel, literacy as the irreversibility example). October keeps a compressed version of the *domain-boundary* argument (its §"The Domain Boundary") but drops the thickness typology and the boot-camp analogy.
4. **The WCT ontology dispute** (June: Wendt, Finnemore & Sikkink, the "unfalsifiability" charge, the Sumerian cuneiform / oracle-bone / Upper Paleolithic material-interests argument, the Lindblom/Simon satisficing account of why states copy). October retains only the short "Domain Boundary" section.
5. **The four "throttling" variants** (Equatorial Guinea rentier suppression, Orbán's vocational choke point, Erdoğan's Imam Hatip parallel track, coup-proofing). Absent from October.
6. **The three detailed falsifiable-prediction tests** of June (shadow-education migration test; demographic-contraction test in Japan/Korea; the "concentrates rather than slows" claim). October replaces these with five different, model-linked predictions.
7. **The June reference list** (46 entries incl. Elman, Rawski, Heyes, Mousley, Wendt, Finnemore & Sikkink, Lindblom, Simon, Hidalgo & Hausmann, Cohen & Levinthal, Baker, Tilly 1990/1998, Mann, Gellner, Hirsch). October's bibliography is still a **key-citation list, not a compiled bibliography** — its own note says so — and it adds Thurow, Raftery & Hout, Lucas, Paglayan, Abarcar & Theoharides, Caplan, Dore, Trow, Busemeyer, Thelen, Archer, Ansell & Lindvall.

### Added in October
1. **Two agent-based models** (Triad three-actor + Massabm Philippine case), six-arm floor/race design, graduate-supply shock, actor knockouts, gate-clustering sweep, state-margin fiscal counterfactuals, and an **appendix of estimands** with replications and SDs.
2. **The Philippines as a worked case** with a dated event table (1940 → 2018), the Trillanes dissent, the many-floors post-reform picture (CSC Resolution 2500229), and the tertiary GER dip/surge.
3. **Five model-linked predictions** replacing June's three.
4. **Failures section** (nurse response 0.25 vs ≈9; recovery not reproduced; gender only under one condition) and a **limits note** documenting two retracted results and three corrected accounting errors.
5. **The state as capture rather than investor**, with the fiscal-margin results.
6. **The three other short-cycle systems** (Angola, Djibouti, Myanmar) — present in v2's abstract, demoted to a body section in the final.

---

## 2. Citation integrity issues found (highest priority for Trey)

**2.1 "Ng and Yip (2020), Positional concerns and education: All for one, loss for all" — suspect, and now doubly so.**
- Both manuscripts rely on it for the formal result that aggregate investment can rise as individual returns fall (June l.41; October note `6`). This is **load-bearing for the paper's sharpest discriminator**.
- The subtitle "All for one, loss for all" is **verbatim the title of Gee's 2012 IPS Working Paper No. 20** ("The Educational 'Arms Race': All For One, Loss For All"), which **is** on the core list (#20) and which I retrieved in full. Gee's paper is a Singapore policy essay, not a formal model.
- My attempted Crossref resolution of the DOI I guessed (`10.1016/j.econmod.2019.09.033`) returned an **unrelated article** (Rhee & Song, "Wage rigidities and unemployment fluctuations in a small open economy"). **That DOI is wrong and is recorded as a discarded guess in `SOURCES.json` — do not reuse it.**
- Status: **the Ng & Yip (2020) citation is unverified and the title looks conflated with Gee (2012).** Action: locate the paper via an author/journal index before submission; if it does not exist as cited, the "intensification under saturation" result must be rested on Kang (2026) and Yoo (2003) instead, and Gee (2012) cited for the *framing*, not the model.
- This is exactly the problem the handoff flagged for the June paper's Ng-and-Yip reference; the October revision **did not fix it**.

**2.2 Breen–Goldthorpe is cited in neither manuscript** (0 occurrences of "Breen" or "Goldthorpe" in both files), despite being listed as an embedded reference in the task brief. Relative-risk-aversion at transitions is, however, effectively what June's "insurance with sequential option value" and October's "floor as insurance" are doing. **Recommendation: add Breen–Goldthorpe properly — it is the standard citation for class-differentiated continuation and it strengthens the floor argument.**

**2.3 Stange (2012) disappears between drafts.** June cites Stange for the option component at **≈14%** of total enrollment value, "rising at the margin where wage returns are most uncertain". October does not cite Stange at all and does not offer an option-value number. So the paper's **only quantified option-value anchor was deleted, not verified**. Either restore it with a verified figure or drop the option-value framing's quantitative claim explicitly.

**2.4 Edmonds & Moss URL problem (affects the standards, not the paper).** The handoff's URL is the whole MABS 2004 proceedings; the actual chapter is Edmonds & Moss, "From KISS to KIDS", LNAI 3415, **pp. 130–144**. Cite it that way.

---

## 3. Numeric claims present in June and **absent from October** (all `unresolved` — see CLAIM_REGISTER J-01…J-08)

| June claim | Value | Source June cites | Status |
|---|---|---|---|
| Upper-secondary completion, last observed UIS value | **67.0% (2022)**, near **67.5%** 2013 baseline | UNESCO UIS 2024 | unverified; **dropped in October** |
| Hong Kong senior-secondary tutoring rate | **85%** | Bray & Lykins 2012 | unverified; dropped |
| HS graduates' wage premium over elementary | **≈32%** (2011; <$5/day at elementary) | PIDS 2013 | unverified; dropped |
| SHS premium over pre-reform curriculum | **≈19%** | PIDS 2024 | unverified; dropped |
| Access to medium-skill occupations | **16.2 pp** | PIDS 2024 | unverified; dropped |
| Option component of college enrollment value | **≈14%** | Stange 2012 | unverified; dropped |
| Flynn Effect | **3 IQ points/decade** | (uncited) | dropped (developmental-capital section gone) |
| Lifespan topological turning points | **9 / 32 / 66 / 83 yrs; >4,000 participants** | Mousley et al. 2025 | dropped |
| Hours of structured exposure | **≈15,000** | (uncited, derived) | dropped |

**Interpretation (two readings, both worth stating):** either (a) these were prudent removals of unverifiable numbers, or (b) the empirical wage/completion backing for the book's central *household* claim was removed without replacement — October's case section now leans on 40%/70–75% completion (late-1990s surveys) and simulation output instead. **Reading (b) is the risk: the October paper's empirical claims are now thinner than June's prose implies, even though its model claims are far stronger.**

---

## 4. Claims softened or withdrawn between drafts

1. **"The opposite of what human-capital theory predicts."** June asserts the directional prediction is *opposite* to human-capital theory. October (and even the v2→final revision) softens three times: the abstract goes from "which **reverses** what simple human-capital theory predicts" (v2) to "which simple human-capital theory **does not predict**" (final); the body adds "The reversal alone does not separate the theories, because a sophisticated human-capital theorist also predicts more investment when the next-best option collapses"; and the discriminating test is moved to the graduate-supply shock (Prediction 2). **This is a genuine improvement and should be preserved.** It also means the June framing cannot be quoted as the paper's position.
2. **The floor's role.** June: relational floor as "insurance product with sequential option value" doing the heavy lifting. October: **the floor explains persistence and exclusion; the race explains intensification; inside a ranked queue the floor's distinct contribution is its *movement*.** This is a real theoretical revision driven by the model (the six-arm table), and October's own abstract states it. Good.
3. **Persistence: lock-in → redundancy.** June: "four independent lock-in mechanisms". October: "persistence comes from redundancy, not lock-in" (an earlier lock-in result was **retracted as an artifact**). Direct reversal; the paper is explicit about it.
4. **State: investment → capture.** June's state captures surplus from taxable output; October reframes the state's gain as **capture of a household-financed tax base**, with subsidies rarely paying back fiscally. Note `state` labels ledger parameters "first guesses".
5. **Scope typology: prediction → heuristic.** June presents the 2×2 as generating predictions; October calls it "a heuristic" and concedes "the cells differ sharply on whether the state extends the cycle, but only slightly on shadow-education intensity, so 'shadow education industrializes under Full Engagement' is **not yet a model prediction**."
6. **Trillanes: "wrong about the aggregate" withdrawn.** Per `CHANGES.md`, the July draft claimed the lone dissenting senator was wrong about the aggregate; the model shows the counterfactual aggregate is ~6.5 points lower, so the claim was withdrawn and the dissent is now treated as substantively correct about the gradient. **The June draft does not contain the "wrong about the aggregate" claim in the text I read** (it only reports 43/100 and 14/100 attrition), so this is a v1→v2 correction, not a June→October one.
7. **Keywords:** June = world culture theory, institutional isomorphism, surplus motor, massification, thick institutions, developmental capital. October = massification, credential economy, **relational floor, positional competition**, compression technology, gray box, agent-based model, **informality**, Philippines. The paper's self-description changed from *theory-of-WCT* to *mechanism-and-model*.

---

## 5. Contradictions and internal inconsistencies I found inside October

1. **Actor-knockout arithmetic.** Text: households 3.5 years, employers 1.5, state 1.2, out of 4.3. Appendix: years 11.6 / 8.2 / 10.1 / 10.4. Differences are 3.4 / 1.5 / 1.2 — the household figure is **3.4, rounded to 3.5** in the text. Trivial, but a reader checking the appendix will notice; state it as 3.4 or report both.
2. **Gender ratio.** Text note: model 0.88 as built, 1.16 with women's informal earnings at 60% of men's; data mean ≈1.23. Appendix: "0.88 vs ≈ 1.23". The 1.16 and 1.23 refer to different objects (a modified-model result vs the data target) and the paper never says so in one place.
3. **Reform simulation, three different framings of the same run.** §5.2 says the reform "cuts full-cycle completion by about 22 points in the poorest quintile and about 2 in the richest… aggregate cost near 6.5 points"; the appendix row says aggregate 0.784 → 0.719 (6.5 points) — consistent. But note `14` adds that "with a yearly dropout hazard the aggregate effect roughly doubles while the distribution barely changes", which is **not** in the appendix table. Two numbers circulate for one counterfactual; label them.
4. **Two claims with no appendix row** (O-40 ~40 points under a uniform Grade-10 floor; O-41 ~70% employer discretion) are in-text model results with no stored table. Under `02_modeling_standards.md` §10 (report all planned cells and output hashes) these should be backed by a stored run or flagged as exploratory.
5. **The `state` note** contains the strongest caution in the paper ("the numbers should be read as signs and orders of magnitude") while the abstract quotes the fiscal result as a finding ("Marginal state subsidies rarely pay for themselves fiscally in the models"). The abstract should carry the caveat, not just the note.
6. **"93 percent of licensure-board takers buy review"** vs October's earlier and correct statement that the model is not the Philippines: these are model shares for 2000–12 cohorts in a *Philippine-parameterised* model whose spending levels are, per note `9`, partly "built into the model". Read as illustrative; the paper says so in note `9` but not in the body sentence.
7. **Model-vs-model tension:** the three-actor model's household slope changes sign across formal-job responsiveness (+0.44, +0.07, −0.45, +0.29, −0.15 — appendix), so the intensification claim is **regime-dependent in the abstract model but robust in the case model**. October states this correctly in §4.2 ("the intensification prediction should be stated with its conditions rather than as a general law"). Flag: this undercuts any simple presentation of the book's headline.

---

## 6. Where June is still stronger than October (do not lose these)

1. **The timing argument is far more developed in June** (the full Jomtien/MDG2/SDG4 sequence, "every major framework was fully operational across the same period and consistently asking for the wrong thing", the WCT-consistent counterfactual the Philippines *didn't* choose). October compresses this to a paragraph and then, admirably, spends a section listing what its own evidence does **not** establish. **June's version is the better-written argument; October's is the better-caveated one.**
2. **The keju material is why a reader believes the surplus motor is not a modernity artifact.** October has no answer to "isn't this just a story about modern credentialism?" June does.
3. **Thick vs thin institutions is the paper's most original metatheoretical contribution** and it survives only as an essayistic contrast in June. It is also the part most vulnerable to the "you built the typology from the cases you then interpret" charge — which June itself concedes in its honest-limits paragraph. That concession should survive into any merged version.
4. **June's three falsifiable predictions are *observational*; October's five are *model-derived*.** A merged paper needs both kinds.

---

## 7. What I could not verify (explicit)
- Every external number in both drafts sourced to UNESCO UIS, PSA, PIDS, CHED, FRED, World Bank, and the EU directives: **not queried this session** (31 of 68 claim-register rows are `unresolved`).
- **Stange (2012) 14%**, **Abarcar & Theoharides (2024) ≈9 nurses**, **Mousley et al. (2025) turning points**, **Ng & Yip (2020)** existence/structure: not retrieved (paywall / not located).
- **Yang (2026)**: abstract only; the equations attributed to it in `03_model_architecture.md` are **not** from a text I read.
- **Brehm & Silova (2014)** and **Bray et al. (2016)**: not retrieved ⇒ the Cambodia/*rien kuo* paragraph in both drafts is **second-hand**.
- Whether the June draft's `[DOCUMENT COMMENTS]` block contained reviewer instructions: the extraction ends at the marker with no content.
