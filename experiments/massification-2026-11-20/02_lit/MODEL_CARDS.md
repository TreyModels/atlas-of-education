# MODEL CARDS — formal models behind *Massification and Its Mechanisms*
**Compiler:** lit-archivist · **Compiled:** 2026-11-20 (UTC+8) · **Task:** task-1
**Scope:** the 7 formally load-bearing models (deep cards, §1–§7) + 13 secondary cards (§8–§20 plus the Stange annex). Every core source on the 20-item reading list has a card.

**Reading-status legend (applies to every card):**
`FULL` = complete text retrieved this session and mined for equations (raw file in `02_lit/raw/`, hash in `SOURCES.json`).
`ABSTRACT` = only abstract/metadata obtained; equations **not** seen — do not present as verified structure.
`LANDING` = citation record only (title/venue/year); no abstract.
`BLOCKED` = retrieval failed (HTTP 403 / JS challenge / SSL).

> **Standing warning for Trey.** Equation-level claims marked `ABSTRACT` or `LANDING` are **not verified** and must not be quoted as the source's equations. Where an equation in `03_model_architecture.md` is reproduced below, it is labelled *(architecture conjecture — unverified against source)*. PDF text extraction mangled some mathematical symbols; where a symbol is unrecoverable I say so rather than reconstruct it.

---

## 1. Yoo (2003) — Private tutoring as rent seeking — **FULL** (37 pp.)
**Citation verified:** Yoon-Ha Yoo, "Private Tutoring as Rent Seeking and Effects of Some Measures to Curb It", KDI School of Public Policy, dated **July 2003**; JEL I2, D72. Source PDF: `raw/yoo2003_private_tutoring_rent_seeking.pdf` (sha256 `479957d8…`, 368,217 B).

**Agents & timing.** A continuum of students/parents in a tuition-controlled college market; one-shot static contest. Demand `D(X)`, supply `S(X)` in tuition `X`; regulated price ceiling `Y < x*` creates excess demand and an admittance rent `X − Y`. Admission rate `= S(Y)/D(Y)`.

**Choice variables.** Effort `e` = quantity of private tutoring purchased (assumed to have *no* intrinsic productivity; pure rent seeking, p. 6–7). Individual valuation of the prize `X` distributed on `[Y, Ȳ]` with cdf `H(X)`.

**Exact equations (recovered verbatim):**
- Test score (eq. 1): `T = αe + ε`, `α > 0`; `E(T) = αe`; `ε` mean 0, variance `σ²`, symmetric pdf `f`, cdf `F`, `f' > 0` for `ε<0`, `f' < 0` for `ε>0`.
- Cost of tutoring (eq. 2): `βc(e)`, `β > 0`, with `c' > 0`, `c'' > 0`, `c'(0) = 0`. `c'(0)=0` is imposed so that every positive-surplus student participates (p. 10).
- Fixed-cutoff admission probability (eq. 3): `Prob(T > t*) = 1 − F(t* − αe) = F(αe − t*)` (last equality by symmetry).
- Objective (eq. 4): max over `e` of `X · F(αe − t*) − βc(e)`.
- FOC (eq. 5): `X f(αe − t*) α = β c'(e)`; SOC (eq. 6) requires `σ²` large and/or `c'` steep — the paper states this assumption explicitly (fn. 8), because SOC can fail as in standard tournament models.
- Effort solution: `e* = e*(X, t*, α, β, σ)` (eq. 7).
- Social objective (eq. 8) = aggregate rent-seeking expenditure, to be **minimised**. *(Symbol-level reconstruction blocked: the integral's limits/argument did not survive PDF text extraction. Reported qualitatively: aggregate `e` integrated over `H(X)`.)*

**Quota variant (Section 3, "the model is expanded to cover the cases where admission quota is fixed").** Under a fixed quota the *relative rank* admits, and the cutoff `t*` is endogenous to the quota. The paper states the key structural consequence directly: "a fixed quota necessarily introduces negative externalities among students" (line 138–139) — one student's extra effort lowers another's admission probability at constant quota; under a fixed quality standard there is no such direct externality.

**Verified results (comparative statics):**
1. `∂e*/∂X > 0` (eq. 9): higher valuation ⇒ more tutoring.
2. Effort is **highest for students near the cutoff** (because `f` is symmetric and maximal at `ε = 0`), not for the highest-valuation students.
3. `∂e*/∂t*` has **indeterminate sign**; it depends on where `t*` sits. Pushing the cutoff toward either extreme lowers aggregate rent seeking; moving it toward the mid-point raises it. Concretely: "making a hard test harder, or an easy test easier" reduces aggregate rent seeking; the reverse aggravates it (p. 14).
4. Lowering `α` (making tutoring less effective at raising scores) is the analysed "test redesign" lever.

**Identification/empirics.** None. Purely theoretical; no data, no calibration, no parameter values beyond signs. (This matters: the paper's numbers are *not* Korean estimates.)

**Mapping to Trey's architecture.**
- Directly implements the **gate** distinction in `03_model_architecture.md`: fixed bar (`t*` exogenous, a quality standard) vs quota (rank, `t*` endogenous). This is the cleanest analytic template for "credential eligibility (fixed passing bar)" vs "rank quota" in §1 of the module list.
- Supplies the **discontinuous payoff** intuition behind gate-clustered shadow education: effort concentrates where `f(αe − t*)` is largest, i.e. where the gate's line sits among its takers. October's Prediction 3 and its "3 → 76%" bar-sweep is the ABM analogue of Yoo's result 3.
- Does **not** model the relational floor (no informality, no formal/informal margin), no insurance/option value, no state.
- Caution: `β` is a marginal-cost shifter, not a tuition price; do not map it to fees.

---

## 2. Kim (2007) — A game-theoretic approach to private tutoring in South Korea — **FULL** (26 pp.)
**Citation verified:** Ji-Ha Kim, Department of Education, Yonsei University, **July 2007**, NCSPE Occasional Paper **OP144**. Integrates Spence signalling + Thurow job-queue into two 2×2 parent games.

**Model 1 (symmetric parents).** Strategy set `{PT, No PT}`. Payoffs from monetary + non-monetary benefits of university graduation minus tutoring cost.
- Expected payoff (eq. 3, recovered): `EW = P·W + (1 − P)·0 − C`, where `P` = probability of passing the entrance exam, `W` = benefit if the child succeeds, `C` = cost of PT.
- Contest technology: if one parent spends `C` and the other spends `0`, the spender's child is admitted with probability `1`; if both choose the same action, each child has probability `0.5`.
- **Verified threshold result:** if `W > 2C` → PT is a **dominant strategy** for both; the Nash equilibrium is (PT, PT) and is suboptimal — the Prisoner's Dilemma. The paper derives the three regimes from comparing `W` and `C` (Table 2).

**Model 2 (asymmetric parents).** Parents `i = 1,2`; income `M_i`; PT expenditure `m_i ∈ [0, M_i]` (cannot exceed income); child ability `a_i ∈ (1, 2)` independent across children, **opponent's ability unknown and uniform on (1,2)**; utility of admission `W_i` proportional to parental preference. Admission rule stated as an ordered comparison of `(1 + PT expenditure) × (child's ability)`: the "1" means college entry is determined by ability alone absent PT; equal ability ⇒ probability 1/2. Utility functions piecewise as printed (OCR partially garbled).

**Verified framing.** The paper explicitly grounds the games in Spence's signalling and Thurow's job-queuing models (Section 1), and reports suboptimal (PD-like) equilibria for symmetric families, with asymmetry changing the equilibrium set.

**Identification/empirics.** None — analytic 2×2 games; South Korea is institutional motivation, not data. No estimated numbers.

**Mapping to Trey's architecture.**
- The `W > 2C` condition is the cleanest *sufficient condition* in the literature for the defensive-investment equilibrium; it is a two-household microfoundation for "households stay in the pipeline even when aggregate returns fall".
- Rank/queue structure = positional layer; the credential as admission token = early statement of the relational layer (but no illegibility/extended margin).
- October's model is a many-household generalisation in which the `W>2C` logic is replaced by a floor rule + ranked slots; the mapping is structural, not literal.

---

## 3. Kang (2026) — The Parental Investment Rat Race — **FULL** (69 pp., Sept 2026 version)
**Citation verified:** Hyunjae Kang (Institute of Economic Research, Kyoto University), "The Parental Investment Rat Race: College Admissions Tournament and Household Welfare", **September 2026**, first version Nov 2022; supersedes "Dynamic Competition in Parental Investment and Child's Efforts". Source: `jaykanglabor.github.io/jobmarket/Tournament_WP.pdf` (1,727,221 B) — **current version confirmed live**.

**Model.** Estimated **dynamic tournament** of college admissions with **endogenous skill formation**, embedding the Lazear–Rosen (1981) tournament. Households are altruistic dynasties; in each secondary-school year they choose **tutoring expenditure**, **tutoring hours**, and **child self-study hours**. Investments produce the child's cognitive and non-cognitive skills; **relative position in the admission tournament** plus the **vector of available seats** determine **college tier** through endogenous admission cutoffs (rank quota, not a fixed bar). Investment is both productive and positional; the prize is a tier, not a wage.

**Verified headline numbers (abstract, p. 1).**
- Competition drives **77%** of tutoring expenditure during secondary school and **89%** in the final year, holding direct human-capital returns fixed.
- **Less than half** of self-study time is competition-driven.
- Both investments **erode non-cognitive skills**, but tournament + cognitive returns outweigh the cost.
- Policy: direct investment-targeting policies improve mobility at **substantial welfare cost**; admissions reforms achieve mobility gains at **smaller welfare cost**.

**Identification.** Structural estimation on **Korean longitudinal data** ("longitudinal data from South Korea"); two descriptive facts used to discipline it: (i) college tier is a vertical ordering that matters; (ii) parental investment is strongly income-graded while self-study hours are not. Counterfactuals remove the tournament channel by **equalising tier** (i.e., the 77%/89% shares are model counterfactual decompositions, not observed quantities).

**Mapping to Trey's architecture.** Closest available **positional-race** engine with an estimated parameter vector: separates tutoring cost/time/self-study, has an explicit seat vector, and produces a *quantified* competition share — the natural benchmark for October's "slope" claims and for a "competition vs human capital" decomposition in the Triad/Massabm lineage. Missing for Trey's purpose: no relational floor / informality margin, no foreign readers, single country.

---

## 4. Jayachandran (2014) — Incentives to teach badly — **FULL** (16 pp.)
**Citation verified:** Seema Jayachandran, "Incentives to teach badly: After-school tutoring in developing countries", ***Journal of Development Economics*** **108 (2014) 190–205**, received 2013-06-03, revised 2014-01-17, accepted 2014-02-27, online 2014-03-12. JEL O12, O15, I20, J45. (The handoff file name says "tutoring.pdf"; the working paper is the JDE article.)

**Agents & timing.** A teacher (shorthand for teacher+school, interests assumed aligned) and households; one school year. Student achievement `s(m, t)` increasing in material taught at school `m` and tutoring `t`. Household utility `u = s(m,t) + v(c)`, `v'' < 0`, income `y`, tutoring a discrete good `t_i ∈ {0,1}`, total demand `T = Σ t_i`. Higher income ⇒ higher willingness to pay.

**Objective (eq. 1, verbatim):**
`V(p, m) = p · T(p, m) + φ(m)` if `T > 0`; `= φ(m) + W` if `T = 0`.
`W` = value of the time otherwise spent tutoring. `φ(m)` bundles effort cost (increasing in `m`) with penalties/psychic cost of teaching little; assumed `φ'(m) → ∞` as `m → 0` and `→ −∞` as `m → ∞` (interior solution). Teacher chooses **price `p` and instructional quantity `m`**.

**Key structural point (p. 192, verbatim sense):** the teacher differs from a standard monopolist because he can raise demand by *lowering `m`* when tutoring and school are substitutes. Substituting the optimal price gives `R_t(m)` and the reduced problem (eq. 2) `max_{m≥0} R_t(m) + φ(m)`, where `R_t(m)` is decreasing in `m` iff `s_mt < 0` (substitutes) and increasing iff `s_mt > 0` (complements).

**Proposition 1 (verified).** Write `λ = 1` if teacher tutoring is permitted, `0` if banned/absent; problem is `max_{m≥0} λ R_t(m) + φ(m)` (eq. 3). If substitutes (`s_mt < 0`) the maximand is supermodular in `(−m, λ)`, so by Topkis `m*` decreases in `λ`: **a ban raises instructional quantity**. If complements, the opposite. This is the exact formal basis for "the incentive may reverse" in `03_model_architecture.md`.

**Empirical identification (Nepal).** Survey + test-score data, student fixed effects and subject fixed effects, standard errors clustered by school; propensity-score trimming and weighting to compare government and private schools.
- `Offers × GovtSchool` coefficient **−0.053** (5% level): offering tutoring makes government-school teachers **5.3 pp** less likely to teach the whole class period = a **30%** increase in the likelihood of not teaching the whole period. Robust at −0.063 with propensity-score trimming.
- Tutoring associated with an **11 pp** lower national-exam pass rate, "or by about 14%" (p. ~200).
- Setting: 2004 Nepal; private-school annual fees 7,960 rupees vs per-capita GDP 20,800 rupees (≈76 rupees/US$); median government-school fees 640 rupees; monthly teacher salaries 3,000 (govt) / 400 (private) rupees in the appendix table.

**Mapping.** Supplies the **deliberate-withholding hypothesis as a separate, testable branch** — exactly what `03_model_architecture.md` §5 demands ("keep deliberate withholding and costly supplementary service as separate hypotheses"). The supermodularity condition `sign(s_mt)` is the switch Trey's provider module needs; the Nepal estimates are the only credible causal evidence in the core set, and they are about **teacher-sold** tutoring, not commercial shadow education.

---

## 5. Ghaffarzadegan, Xue & Larson (2017) — Work–education mismatch — **FULL** (PMC HTML)
**Citation verified:** PMC5509065, *Systems Research and Behavioral Science* / PMC deposit; title "Work-Education Mismatch: An Endogenous Theory of Professionalization". Retrieved as HTML (206,627 B); equations live in Appendix I (Vensim), so formulas were **not** individually readable — structure below is from the body text.

**Model type.** System-dynamics, aggregate, continuous time. Three workforce subpopulations `W1, W2, W3` (e.g. high school, undergraduate, graduate credentials) and two education stages `S2, S3` as transition stocks. Constant inflow to `W1`; attrition/retirement; `S2` admission from `W1`; degrees conferred after a delay. `n = 3` chosen "in the interest of parsimony".

**Matching rule (verbatim).** In each period the active workforce is matched to jobs by highest education. Jobs `J3, J2, J1` are filled from the top down: higher degrees have competitive advantage; **nobody can take a job requiring more education than they hold**; people prefer matched jobs; `Job discrepancy_3` = `W3` minus `J3` drives over-education of the most educated. Baseline: 1,000 people and 1,000 jobs at each of the three levels (3,000/3,000), initially with no unemployment or underemployment.

**Two mechanisms (the paper's contribution).**
1. **Cascading effect**: a shortage at the top pushes `W3` people into `J2` jobs, displacing `W2`, etc., down the chain.
2. **Pipeline reinforcing effect**: universities expand capacity by hiring the unemployed most-educated as **temporary positions in academia (TPA)**; those TPA holders train more students, which further increases degree supply. Parameter `r` = share of unmatched `W3` hired into TPA.

**Verified simulations.**
- Baseline steady state; a **20% job shock during 5 ≤ t ≤ 10** produces **overshoot** in `W3` and long-lasting non-uniform distributions (shortage of middle-skilled) before convergence.
- Technological-shift scenarios move jobs from `J1` to `J3` at **25%, 30%, 32%, 34%**; there is a **tipping point around 25%** below which no overshoot occurs and above which long waves appear; very large shifts also do not produce mismatch (absorption into new high-tech posts).
- `r` has a **U-shaped** effect: small `r` buffers shocks (absorbs the unmatched), large `r` amplifies long-run mismatch via pipeline reinforcement; direction reverses after a tipping point (`r ≈ 0–0.03` at −30% shock; `r ≈ 0–0.075` at −10% shock).
- Sensitivity: **Vensim DSS**, 8 one-at-a-time tests, **1,000 runs** each over predefined ranges (±100%), reported as 50/75/95% bands; qualitative predictions robust except at extremes.
- Explicitly hypothetical parameters — authors state the model "does not depict U.S. or other labor markets precisely" (p. ~5).

**Mapping.** This is the **closest structural benchmark** in the set and the one Trey's pipeline module should be docked against: same objects (credential stocks, job tiers, ranked matching, delays), different method (aggregate SD vs ABM). Two concrete borrowings: (i) the *cascading* rule is a cleaner statement of "credential holders displace downward" than October's informal-cushion story; (ii) TPA is a **provider-capacity feedback** — the missing "fourth leg" October itself proposes as the fix for its nurse-response failure.

---

## 6. Ostrovsky & Schwarz (2010) — Information disclosure and unraveling — **FULL** (25 pp.)
**Citation verified:** Michael Ostrovsky (Stanford GSB), Michael Schwarz (Yahoo! Research/NBER), "Information Disclosure and Unraveling in Matching Markets"; manuscript version dated **July 3, 2009**; published *AEJ: Microeconomics* 2(2), 2010, 34–56 (DOI `10.1257/mic.2.2.34`).

**Setting.** Many schools, students, positions. School evaluates students and issues a **transcript**; outsiders (employers, residency programmes) rank students **solely by expected ability** inferred from the transcript. Position desirability `q ∈ [q_L, q_H]` with continuous exogenous density `μ(·)`, mass of positions = mass of students ⇒ assortative stable matching between expected ability and position desirability.

**Choice variable.** Each school picks a **transcript structure** = a (coarsening) map from true ability to a reported signal, subject to a **no-lying-on-average / distribution-preserving** restriction (schools may compress the reported ability distribution but not inflate its mean), to **maximise the total desirability of positions obtained by its students**. Schools are small price-takers in the market for expected ability. Commitment to the structure is assumed, with a cheap-talk footnote (Crawford–Sobel 1982).

**Central concept — "balanced" disclosure.** The amount of information disclosed in equilibrium when schools can choose freely; Theorems 2 and 3 state that if the balanced amount is disclosed, (i) the same balanced amount is disclosed in essentially all equilibria (static case) and (ii) students and employers do **not** profit from early contracting; disclosing **more** than balanced induces **unraveling**. Balanced disclosure "mimics" the distribution of position desirability (p. ~15).

**Worked examples (verified, reproducible).** Example 1: abilities `U[0,100]`, desirabilities `U[0,100]` ⇒ full revelation is an equilibrium with linear mapping `Q(â) = â`. Example 2: half the schools `U[0,100]`, half `U[50,100]` ⇒ the full-revelation mapping `Q(·)` is piecewise linear with two pieces (the printed `Q` is the object Trey's "compression" section should cite).

**Identification/empirics.** None; theory. But note the **institutional evidence** the paper opens with: GSB curve-grading (very informative transcripts, *not* revealed), MIT internal vs external transcripts (B+ vs B− distinction), noisy grading standards as deliberate obfuscation.

**Mapping.** This is the *formal* ancestor of Trey's "positional vs domain resolution" and of the reader-specific decompression claim, with two important disanalogies to state in the paper:
- OS's school **chooses** compression to game placement; Trey's credential compression is a by-product of institutional form. The strategic-disclosure channel is absent from October's account.
- OS derives a *unique balanced* amount; Trey's claim that foreign readers decompress **coarsely** (years, completion, tier) is a different mechanism (reader-side information cost), not an equilibrium disclosure result. Border-coarsening should therefore be modelled as reader-specific partitions, not as OS noise.

---

## 7. Yang (2026) — Regulating private tutoring — **ABSTRACT ONLY** (MDPI 403)
**Metadata verified:** *Economies* (MDPI), **2026, 14(9), article 415**, DOI `10.3390/economies14090415`; RePEc record `gam/jecomi/v14y2026i9p415-d2044259`. Title: "Regulating Private Tutoring: Human Capital Formation, Inequality, and Intergenerational Mobility". MDPI HTML/PDF returned **HTTP 403** to this session; abstract obtained from the RePEc record (`raw/yang2026_ideas_page.html`).

**What is verified from the abstract.**
- **Quantitative partial-equilibrium overlapping-generations** model.
- **Heterogeneous households**, **endogenous ranking-based college admission**, **intergenerational human-capital transmission**.
- Tutoring can affect **exam performance and productive human capital differently** — the distinction that lets it separate competitive from productive roles.
- **Calibrated to Chinese microdata and reduced-form empirical evidence.**
- Three policies compared: **complete ban**; **ban with imperfect enforcement + black-market tutoring**; **welfare-selected tutoring tax partly financing public education**.
- Findings: complete ban ⇒ large model-implied **welfare and human-capital losses**, especially when tutoring contributes to productive skills; imperfect enforcement preserves some tutoring but can **widen group differences in access** when informal tutoring costs vary by household type; the **tutoring tax outperforms prohibition**, keeping mean child human capital close to baseline — conditional on assumed enforcement and public-financing arrangements.

**NOT verified — do not cite as Yang's.** `03_model_architecture.md` gives the functional form `h_exam = h_inherited + T(e_public, p)`, `h_pre = h_inherited + T(e_public, ω·p)`, `T(e,x) = A[λ e^μ + (1−λ) x^μ]^{1/μ}` *(architecture conjecture — unverified against source)*. The CES-style `T` and the `ω` parameter are **plausible reconstructions by Trey, not text I read**. The abstract is consistent with a two-output human-capital technology and a ranking admission rule; it does not license the specific CES form. **Action: obtain the MDPI PDF (institutional access or author copy) before the paper prints any equation attributed to Yang.**

**Mapping.** Yang is the closest *published* formal model to the paper's own question (tutoring regulation with ranking + intergenerational transmission), so it is the sharpest novelty risk. October's Triad/Massabm add: informality/formal-work floor, foreign readers, state capture — none of which appear in the abstract of Yang. That is the defensible differentiation, and it should be stated explicitly.

---

## Secondary cards (shorter; all verified at the level noted)

### 8. He (2024) — Quantifying Educational Competition — **FULL** (arXiv preprint, 14 pp.)
Siyuan He, Dec 2024, arXiv:2412.10974. **Preprint — not peer-reviewed; treat as provisional.**
Equations verified:
- `S_i = γ_i · t_i` (eq. 1) — score from study time `t_i` and aptitude `γ_i`; explicitly **no random exogenous shock**.
- `S̄ = ∫_0^∞ (γ_i t_i) dF(S_i)` (eq. 2) — average score.
- **`S_cut = S̄ + k · σ_S`** (eq. 3) — the gate is the mean plus `k` standard deviations; the paper notes `k ≈ 1.645` corresponds to the 5th percentile. This is a *fixed relative* (quota-like) threshold, not an administrator's bar.
- Utility (eq. 4): `u_i = log(2 + S_i − S_cut) − C_i` if `S_i ≥ S_cut`; `= −C_i` otherwise. Cost (eq. 5): `C_i = P_i · t_i`. Corner solution: if `E[S_i] < S_cut`, `t*_i = 0` (complete give-up).
- Extended with **Spence (1973) signalling** for the inefficiency/policy analysis; simulation on the model set.
Mapping: gives Trey a clean **mean-plus-k-sigma gate** — a compact formalisation of "rank quota with a pass line in the middle of the crowd" and of Yoo's result that effort peaks near the line. China policy framing (Double Reduction) but **no data, no calibration**.

### 9. Edmonds & Moss (2005) — From KISS to KIDS — **FULL** (in MABS 2004 proceedings)
**Citation correction, verified.** The handoff URL `ccl.northwestern.edu/2004/henein2004.pdf` returns the **entire MABS 2004 proceedings volume** (LNAI 3415, 275 pp.), not a single paper. Inside it, the target paper is **"From KISS to KIDS – An 'Anti-simplistic' Modelling Approach", Bruce Edmonds & Scott Moss, pp. 130–144** (TOC line 220). The same volume contains Henein & White (pp. 173+) — the file name reflects *that* paper, not Edmonds–Moss. **Do not cite the URL as the Edmonds–Moss paper; cite the chapter.** KIDS = "Keep It Descriptive, Stupid": demand that ABM be justified against descriptive case knowledge rather than simplified for tractability. Methodological, not a formal model. Mapping: this is the warrant for `02_modeling_standards.md`'s KIDS section and for Trey's case-first design; it supplies **no equations**.

### 10. Gee (2012) — The Educational 'Arms Race' — **FULL** (37 pp.)
Christopher Gee, *IPS Working Papers No. 20 (September 2012)*, Institute of Policy Studies, Lee Kuan Yew School of Public Policy, NUS. Title verified on the title page: "The Educational 'Arms Race': All For One, Loss For All". Singapore. Policy essay/descriptive political economy of positional competition — **not** a formal model; no estimated equation. **Important:** the phrase "All for one, loss for all" in this title matches the subtitle June attributes to **Ng and Yip (2020)** — see MANUSCRIPT_COMPARISON §2.

### 11. Boudon (1974) — Education, Opportunity, and Social Inequality — **ABSTRACT** (ERIC ED091493)
Raymond Boudon, 1974, 220 pp. (book). ERIC record retrieved: `raw/boudon1974_eric_page.html`. Abstract confirms the object: inequality of educational opportunity (IEO) = attainment differences by social background; social mobility = achievement differences; **primary vs secondary effects** and the sequential/simulated mobility model. The original simulation model was **not** obtained (book, not digitised open access). Mapping: the ancestor of Trey's "relative risk aversion at each transition" idea; **no equation verified this session**.

### 12. Yu & Ding (2011) — How to get out of the prisoners' dilemma — **LANDING/METADATA ONLY**
Crossref-verified: Hongxia Yu & Xiaohao Ding, "How to get out of the prisoners' dilemma: Educational resource allocation and private tutoring", ***Frontiers of Education in China*** **6(2), 279–292, 2011**, Springer. DOI `10.1007/s11516-011-0132-4`. The DOI landing page returned a JavaScript challenge; no abstract, no equations. **Treat as citation-verified, content-unverified.**

### 13. Saha & Saha (2009) — Private Tutoring, School Education and Government Policy — **METADATA ONLY (BLOCKED)**
Crossref-verified: Bibhas Saha & Subhra Baran Saha, ***Review of Market Integration***, 2009 (note: handoff says 2009; Crossref issued year 2009), DOI `10.1177/097492921000100305`; SAGE returned **403**. No abstract, no model. The handoff characterisation ("infrastructure, teacher incentives and fiscal trade-off") is **unverified**.

### 14. Ille & Peacey (2019) — Forced private tutoring in Egypt — **LANDING ONLY (BLOCKED)**
DOI `10.1016/j.ijedudev.2018.12.003`, *International Journal of Educational Development*; Elsevier landing page returned only a redirect stub. No abstract, no evolutionary-game equations. **Do not reproduce its equations**; the "evolutionary game + social norms" description in the handoff is unverified.

### 15. Bray, Zhan, Lykins et al. (2014) — Differentiated demand — **ABSTRACT/METADATA ONLY**
Crossref-verified: Mark Bray, Shengli Zhan, Chad Lykins (+ others), "Differentiated demand for private supplementary tutoring: Patterns and implications in Hong Kong secondary education", ***Economics of Education Review***, **2014**, DOI `10.1016/j.econedurev.2013.10.002`. No full text (Elsevier). This is the citation behind June's **85% senior-secondary tutoring rate** claim — **the 85% figure itself was not verified** this session.

### 16. Choi (2010) — Analysis of private tutoring decisions in Korea — **LANDING ONLY**
RePEc-verified: "Analysis of Private Tutoring Decisions in Korea: A Game Theory Approach", ***East Asian Economic Review*** vol. 10 (2010), issue 3, article 2 (`repec: eaa:eerese:v10y2010i3_2`). Metadata only; no abstract extracted, no model. Game-theoretic per the title; **contents unverified**.

### 17. Biswal (1999) — Private tutoring and public corruption — **LANDING ONLY**
IDE (JETRO) record verified: Bagala P. Biswal, "Private Tutoring and Public Corruption: A Cost-Effective Education System for Developing Countries", ***The Developing Economies***, **Vol. 37, No. 2 (June 1999)**. Only the IDE landing page was retrievable; the article body was not. Model unverified.

### 18. Suen & Xu (HKU) — Private tutoring as a signal-jamming activity — **BLOCKED (403)**
HKU CRIS project record `hkugrant127273` returned 403. **This is a grant/project record, not a paper.** No publication located. Per the handoff's own warning: do not cite as evidence that a completed article exists.

### 19. Bray et al. (2016) — Internal dynamics of privatised public education (Cambodia) — **BLOCKED (403)**
HKU Hub bitstream returned 403. Author/title only, from the handoff. **The Cambodian teacher-tutoring description in October (Brehm & Silova's *rien kuo*) rests on Brehm & Silova 2014, which was not retrieved either.** The Cambodia claims in both manuscripts are therefore second-hand and unverified this session.

### 20. Bray & Kwok (2003) — Demand for private supplementary tutoring (HK) — **BLOCKED (SSL)**
HKU `web.edu.hku.hk` PDF failed with `SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC`. No content. HK historical demand figures therefore unverified.

### Annex. Stange (2012) — option value of college enrollment — **BLOCKED (AEA 403)**
Kenneth Stange, "An Empirical Investigation of the Option Value of College Enrollment", ***AEJ: Applied Economics*** 4(1), 49–84, 2012 (citation as printed in June's reference list; AEA PDF returned **403**). **June's "approximately 14 percent of total enrollment value" is UNVERIFIED.** This is the single most important number June carries that October silently drops — see MANUSCRIPT_COMPARISON §3.
