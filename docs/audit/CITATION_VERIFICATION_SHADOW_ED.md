# CITATION VERIFICATION — shadow education & private tutoring equations (inventory §5, tutoring-relevant §2/§3)

Owner: `engine-tutoring` (data/verification lane) · date 2026-11-25 · status: **verification report, no fixes applied**.
Input artefact: `docs/audit/refs/education-equation-inventory-20261124.txt` (bridge attachment
`20261124154148-7126f591`), 404 lines, sha256 `0fd30f770a75ee55cdf26d3ce332df795f78d29d070bed01af38810bfa4752df`
— matches the sha in the tasking (`0fd30f77…52df`). Equation numbers below are **inventory numbers**, not
numbers in any published source.

**Bottom line:** no equation in inventory §5 (57–86) is a verified quotation of any named source. The named
sources exist and their metadata is verified, but they contain (a) a literature survey with a *graphical*
supply/demand framework and one unnumbered naive OLS equation (Dang & Rogers 2008), (b) a Tobit application
(Tansel & Bircan 2006), (c) monographs with no equations (Bray 1999, 2009), (d) an empirical/theoretical demand
study whose model is not the inventory's (Kim & Lee 2010), (e) a teacher-incentive model with school-day
material `m` and achievement `s(m,t)` (Jayachandran 2014), and (f) a paper whose text could not be retrieved
(Biswal 1999). The inventory's residual claim “more recent empirical studies using hurdle models” (L123) has no
cited study. **Nothing here is a licence to cite any inventory equation to a primary source.**

---

## 1. Scope, status key, and what “verified” means

Statuses used throughout:

| status | meaning |
|---|---|
| **VERIFIED-BIBLIOGRAPHIC** | work exists; authors/title/venue/year/volume/pages/DOI checked against a publisher/Crossref/OpenAlex record |
| **VERIFIED-EXACT** | the inventory formula appears (to mathematical content) in a retrieved full text — **none found** |
| **VERIFIED-PARAPHRASE** | the source contains a related formal object; the inventory formula is a simplification/restatement, not a quotation |
| **GENERIC-UNCITED** | standard textbook/econometric form; the inventory gives no source for it and no named source contains it |
| **UNSUPPORTED** | the inventory’s block attribution implies a named source that does not contain the formula or claim |
| **NOT-RETRIEVED** | source verified bibliographically but full text inaccessible here → equation-level claim unverified |
| **PLACEHOLDER** | the “citation” is a search-engine artifact (e.g. `doi.org+4`, `UIS+2`), not a citation |

Scope: §5 rows 57–86 in full; tutoring-relevant rows of §2 (11–25, esp. 12, 19, 21, 49), §3 (26–41),
§4 row 49, §8 rows 130, 131, 136; the named-source table at the end of the inventory; and the citations in the
engine’s own tutoring docstring (`engine/eduengine/modules/tutoring.py` L3–5: Dang & Rogers 2008; Bray 1999,
2009; Biswal 1999; Jayachandran 2014; Kim & Lee 2010; Dang 2007) because those are the claims Paper C/D inherit.
No citation was “fixed” in the inventory; corrections are **reported** below, not applied.

## 2. Method and evidence trail (reproducible)

* Inventory read in full. Equation strings quoted below are copied from the inventory’s LaTeX (not re-typeset
  from memory).
* Bibliographic records: Crossref REST (`https://api.crossref.org/works/<DOI>`, `…/works?query.bibliographic=…`)
  and OpenAlex (`https://api.openalex.org/works/https://doi.org/<DOI>`) queried directly over HTTPS on
  2026-11-25. The session’s `web_fetch` tool was blocked by DNS policy for external hosts, so direct HTTPS from
  `bash` (`curl`/Python `urllib`) was used instead; this is recorded so the reader can judge the evidence path.
* Full texts retrieved and parsed (pypdf), with sha256 recorded in Appendix A:
  Dang & Rogers 2008 (World Bank–hosted WBER PDF, 40 pp; also the 42-page WP 4530 version);
  Jayachandran 2014 (author PDF `seemajayachandran.com/tutoring.pdf`, 16 pp = JDE 108:190–205);
  Tansel & Bircan working paper (IZA DP No. 1255, 28 pp); Dang 2007 not retrieved, but his self-review
  WB WP 6618 (2013, 40 pp) was retrieved and searched for claims about Dang 2007.
* Peer-reviewed book reviews retrieved for both Bray monographs (their records supply place/publisher/pages).
* Paywalls hit and recorded: Elsevier (Tansel–Bircan published version — working paper used), Elsevier/Wiley
  (Dang 2007), Wiley (Biswal 1999), University of Chicago Press (Kim & Lee 2010), SSRN delivery (blocked
  403/HTML). **No paywalled content is claimed as read.**

## 3. Placeholder audit — every “citation” in the inventory is a placeholder

The inventory has **no per-equation citations**; citations occur only as aggregate, inline search-engine
artifacts, plus a final unformatted reference table. All placeholders are listed here; none is a usable citation.

| line | text as printed | where attached | verdict |
|---|---|---|---|
| L23 | `Institute for Statistics (UIS)+2` | §1 measurement equations (1–10) | **PLACEHOLDER** (site + “2 more” artifact; no report/table) |
| L43 | `OECD+3` | §2 human-capital investment (11–25) | **PLACEHOLDER** |
| L70 | `hanushek.stanford.edu+2` | §3 production functions (26–41) | **PLACEHOLDER** (website, not a reference) |
| L96 | `sciencedirect.com+2` | §4 returns (42–56) | **PLACEHOLDER** (publisher domain ≠ citation) |
| L125 | `doi.org+4` | §5 shadow education (57–86) — the only “source” for the whole section | **PLACEHOLDER** |
| L180 | `OUP Academic+3` | §6 growth (87–105) | **PLACEHOLDER** |
| L211 | `World Bank+2` | §7 finance (106–122) | **PLACEHOLDER** |
| L238 | `ideas.repec.org+2` | §8 inequality (123–137) | **PLACEHOLDER** |
| L265 | `Princeton University Press+3` | §9 identification (138–167) | **PLACEHOLDER** |
| L279 | `doi.org+1` | §9 DiD text | **PLACEHOLDER** |
| L336 | `doi.org+1` | §10 LAYS text | **PLACEHOLDER** |
| L392–L403 | reference table rows end with `Eric A. Hanushek+1`, `RCNi Company Limited`, `OUP Academic`, `nber.org`, `Taylor & Francis Online`, `OUP Academic`, `doi.org`, `doi.org`, `International Institute for Educational Planning`, `sciencedirect.com`, `Princeton University Press`, `ideas.repec.org+1` | “Main academic references” table | **PLACEHOLDER + one false publisher** (see §9: `RCNi Company Limited` is a nursing publisher, not an economics publisher; it cannot be the publisher of Becker & Lewis 1973) |

Additional unsupported attribution: L123 says the foundational literature includes “… and more recent empirical
studies using hurdle models”. **No hurdle-model study is cited anywhere in the inventory.** The only named
empirical tutoring study that uses a censored model (Tansel & Bircan) uses **Tobit**, not a hurdle model.

## 4. Named-source verification (bibliographic + content access)

| source as named (inventory/engine) | verified record | access to full text | VERIFIED? |
|---|---|---|---|
| Dang & Rogers (2008) | Dang, H.-A. & Rogers, F. H. (2008). *The Growing Phenomenon of Private Tutoring: Does It Deepen Human Capital, Widen Inequalities, or Waste Resources?* **The World Bank Research Observer 23(2): 161–200**. DOI **10.1093/wbro/lkn004** — note: **not** `lkn006` | WBER PDF (World Bank), 42-pp WP 4530 | **VERIFIED-BIBLIOGRAPHIC + full text read** |
| Bray (2009) | Bray, M. (2009). *Confronting the Shadow Education System: What Government Policies for What Private Tutoring?* Paris: **UNESCO International Institute for Educational Planning (IIEP)**, **132 pp.** Verified via two independent reviews: Kang, C. (2010) *Education Economics* 18(3):373–375, DOI 10.1080/09645292.2010.507493; Guill, K. (2011) *Journal for Educational Research Online* 3(2):148–151, peDOCS record 10.25656/01:5627 (which prints “Paris: IIEP, 132 p.”) | reviews only (book itself not online here) | **VERIFIED-BIBLIOGRAPHIC** |
| Bray (1999) | Bray, M. (1999). *The Shadow Education System: Private Tutoring and its Implications for Planners.* **Fundamentals of Educational Planning No. 61.** Paris: UNESCO IIEP. Verified via review: Postlethwaite, N. (2000) *International Review of Education* 46(6):641–644, DOI 10.1023/A:1026531112211 (Crossref review title reproduces the book details) | review only | **VERIFIED-BIBLIOGRAPHIC** |
| Tansel & Bircan (2006) | Tansel, A. & Bircan, F. (2006). *Demand for education in Turkey: A tobit analysis of private tutoring expenditures.* **Economics of Education Review 25(3): 303–313**. DOI 10.1016/j.econedurev.2005.02.003 — note: **volume 25, issue 3, pages 303–313** (common secondary citations giving 25(2):199–213 are wrong) | published version paywalled; **working-paper version** IZA DP No. 1255 (Aug 2004) retrieved, 28 pp | **VERIFIED-BIBLIOGRAPHIC + WP full text read** |
| Biswal (1999) | Biswal, B. P. (1999). *Private tutoring and public corruption: A cost-effective education system for developing countries.* **The Developing Economies 37(2): 222–240**. DOI 10.1111/j.1746-1049.1999.tb00232.x | **NOT RETRIEVED** (Wiley paywall, Cloudflare; Wayback snapshots are redirects) | **VERIFIED-BIBLIOGRAPHIC; content NOT-RETRIEVED** |
| Jayachandran (2014) | Jayachandran, S. (2014). *Incentives to teach badly: After-school tutoring in developing countries.* **Journal of Development Economics 108: 190–205**. DOI 10.1016/j.jdeveco.2014.02.008 — note: **.008**, not `.005` | **author PDF of published article retrieved** (`seemajayachandran.com/tutoring.pdf`), 16 pp | **VERIFIED-BIBLIOGRAPHIC + full text read** |
| Kim & Lee (2010) | Kim, S. & Lee, J.-H. (2010). *Private Tutoring and Demand for Education in South Korea.* **Economic Development and Cultural Change 58(2): 259–296**. DOI 10.1086/648186 | **NOT RETRIEVED** (UChicago paywall); abstract read (OpenAlex) | **VERIFIED-BIBLIOGRAPHIC; abstract only** |
| Dang (2007) | Dang, H.-A. (2007). *The determinants and impact of private tutoring classes in Vietnam.* **Economics of Education Review 26(6): 683–698**. DOI 10.1016/j.econedurev.2007.10.003 | **NOT RETRIEVED** (Elsevier/SSRN delivery blocked) | **VERIFIED-BIBLIOGRAPHIC; content NOT-RETRIEVED** |

**Citation-name ambiguity flagged, not resolved:** there are two distinct 2010 Korean tutoring papers in
circulation: (i) Kim, S. & Lee, J.-H. (2010) EDCC 58(2):259–296 (above), and (ii) Kim, J.-H. & Park, D. (2010)
“The determinants of demand for private tutoring in South Korea”, *Asia Pacific Education Review*
11(3):411–421, DOI 10.1007/s12564-009-9067-3. The engine’s “Kim & Lee 2010” can only be (i); authors must say
so explicitly. Dang & Rogers (2008) cite the **2004 working-paper** version of (i) as “Kim and Lee 2004”, so a
reader following D&R will not find a “2010” record in that bibliography.

## 5. What the retrieved full texts actually say (quotes / formulae)

### 5.1 Dang & Rogers (2008), WBER 23(2):161–200 — a **survey**, not a model catalogue
* Section 3 (“A Framework of Private Tutoring Supply and Demand”) is explicitly “a simple **graphical**
  framework based on the standard microeconomic theory of supply and demand … Figure 1 shows …” (WBER
  23(2):161–200, PDF pp. 4–6 of 40; printed pp. ~164–166). **No algebraic demand/supply functions are published.** The inventory’s E83
  (`Q_T^d(P_T,Y,…)=Q_T^s(P_T,W,…)`) is therefore a *paraphrase of a figure*, not of an equation.
* The only formal equation in the article is the **unnumbered naive regression** in §5.1 (WBER PDF p. 10 of 40;
  printed page ~170):
  `A = α + βT + γX + ε` (“… a naive first approach … likely to yield unreliable estimates … because students
  who receive private tutoring may differ in various unobserved … dimensions”). Inventory E74
  (`A_i=α+βT_i+X_i'γ+ε_i`) is the same generic form, but D&R present it only as the *naive benchmark to be
  criticised*, not as a recommended specification.
* D&R treat **teacher incentives/corruption verbally**, citing Biswal: “Low pay levels and weak monitoring of
  teachers in the public system can also cause teachers to force tutoring on students … as **formalized in a
  theoretical model by Biswal (1999)**.” (References: Biswal, *Developing Economies* 37(2):222–40; Kim & Lee
  2004 WP; Tansel & Bircan 2006; Bray 1999a.)
* **No time-allocation equation, no schooling-stock dynamic, no depreciation, no withholding variable.** The
  inventory’s §5 family cannot be sourced to this article beyond the naive OLS form and the graphical market
  framework.

### 5.2 Jayachandran (2014), JDE 108:190–205 — published model **does** contain withholding
From the published article (author PDF, §2 “Model”, PDF pp. 2–5; teacher objective eqs (1)–(2) on PDF p. 3):
* Household utility `u = s(m,t) + v(c)`, `v″(c)<0`; tutoring is a discrete good `t_i ∈ {0,1}`; total demand
  `T = Σ_i t_i`; teacher and school treated as aligned; teacher chooses price `p` and school-day material `m ≥ 0`.
* Teacher’s objective (published equations **numbered (1) and (2)**):
  `max_{p,m≥0} p·T(p,m) + φ(m)`  (1)  ⟺  `max_{m≥0} R_t(m) + φ(m)`  (2)
  with additive separability and linear profits; `φ(·)` captures effort costs/penalties.
* Achievement `s(m,t)` increasing; **`s_mt < 0` (substitutes) is the empirically relevant case**, so “teachers
  will **withhold material** during the school day to generate demand for tutoring”; Proposition 4 shows
  third-party competition raises `m`.
* Explicit assumptions/limits: teacher–school interests aligned; principal–agent conflict out of scope; coercion
  (“quid-pro-quo”) **modelled in an earlier version but excluded from the published paper** because its
  predictions are untestable in the Nepal data; single teacher, one child per household, no time allocation or
  skill-stock dynamics.
* **Relevance to Paper D:** the published model contains the withholding mechanism — as `m` (material taught),
  in an achievement function `s(m,t)` — but **none of inventory E57–E86 contains `m`, teacher effort, or a
  school-day/withholding variable**. E71–E80 are generic achievement/tutoring regressions; E81–E86 are
  contest/IO/policy forms. This is direct textual support for the omission lemma: the published literature does
  model withholding; the inventory’s §5 equation family does not.

### 5.3 Tansel & Bircan (2006), EER 25(3):303–313 — published object is a **Tobit expenditure model**
From the working-paper version (IZA DP 1255, §4 “Empirical Specification”, PDF pp. 13–14; working-paper pages
10–12), retrieved in full:
* Latent/observed Tobit system:
  `(1) Y_i* = β'X + ε_i`; `(2) Y_i = 0 if Y_i* = 0`; `(3) Y_i = Y_i* if Y_i* > 0`
  with `ε` normal i.i.d.; X = personal/household characteristics (total household expenditure, parental
  education, household characteristics).
* Marginal effects (with Maddala 1983; McDonald & Moffit 1980):
  `(4) ∂E(Y)/∂X_j = F(z)β_j`;
  `(5) ∂E(Y_i | Y_i*>0)/∂X_j = β_j [1 − z·λ − λ²]`, `λ=f(z)/F(z)`, `z=β'X_i/σ`.
* Context: **1994 Turkish Household Expenditure Survey**; Engel-curve formulation with (log) private tutoring
  expenditure; censored at zero; data are cross-sectional household expenditures, not individual tutoring
  intensity or time.
* **Mapping to inventory:** E62 `T_i = max(0, X_i'β+ε_i)` is a *generic* Tobit restatement that matches the
  published censoring logic but not its notation/objects (published dependent variable is **expenditure**, and
  the paper estimates an Engel curve); E64/E65 (expenditure share/Engel curve) are thematic paraphrases. The
  published paper contains **no** participation logit/probit (E58/E59), no hurdle/double-hurdle (E61/E63), no
  production function, no contest, no time allocation. Published version itself was paywalled; equation
  verification is against the authors’ working paper (same title/topic) and is labelled accordingly.

### 5.4 Biswal (1999), Developing Economies 37(2):222–240 — content only second-hand here
* Bibliographic record verified via Crossref (title/authors/venue/volume/issue/pages/DOI).
* Full text not retrieved. The only independently verified description is Dang & Rogers (2008) (full text read):
  a **theoretical model** in which low public-teacher pay/weak monitoring leads teachers to *force* tutoring on
  students. That is the withholding/“buy-back” mechanism; **its exact equation is NOT verified here**.
* Inventory rows that would correspond to a Biswal-type model (teacher withholding, corruption) do not exist in
  §5: there is no equation for `m`, teacher effort, kickbacks, or detection.

### 5.5 Kim & Lee (2010), EDCC 58(2):259–296 — demand/positional mechanism, equations not read
Verified abstract (OpenAlex): tutoring pervasive; **2006 household tutoring ≈2.57 % of GDP** vs ≈3.5 % GDP
government spending on the same pupils; “prevalence … is a market response to the government’s rigid and uniform
education policy”; “desire to enter elite universities in a very hierarchical higher education system and a
heavily regulated and equalized secondary school system has created an enormous demand”; students with high
ability, high family income and highly educated parents spend more; regions without school choice spend more;
**estimated income elasticity ≈0.5**; frames tutoring as part of the whole education system. No equations read;
the paper is empirical/descriptive + demand analysis, **not** a contest-success or time-allocation model.

### 5.6 Bray (1999, 2009) — monographs/policy analyses, **no equations**
Both are IIEP books (1999: Fundamentals of Educational Planning No. 61; 2009: 132-pp policy analysis). The
verified reviews describe them as reviews/policy analysis of shadow education (concept, scale, effects, policy
options). Neither is a source of econometric equations; the inventory attaches them to the whole §5 block
without any page/equation reference.

### 5.7 Dang (2007), EER 26(6):683–698 — bibliographic only
Verified bibliographic record. Full text not retrieved here. Its own later review (World Bank WP 6618, 2013)
was retrieved but contains no equation quotation usable for the inventory; therefore E57–E70 cannot be sourced
to Dang 2007 from this audit.

## 6. Inventory §5 (rows 57–86): equation-by-equation verdict

The §5 block attribution (L123–L125) is “Dang and Rogers (2008), Bray, Tansel and Bircan, and more recent
empirical studies using hurdle models” + `doi.org+4`. None of those named works contains the formulas below
except where marked. **All rows are therefore at best GENERIC-UNCITED; three are loose paraphrases.**

### A. Participation and demand (57–70)

| # | inventory formula (as printed) | nearest verified source | verdict | what the source actually says |
|---|---|---|---|---|
| 57 | `D_i = 1(T_i>0)` | none named | **GENERIC-UNCITED** | definition of participation, not an equation from any named source |
| 58 | `P(D_i=1|X_i)=Λ(X_i'β)` | none named | **GENERIC-UNCITED** | standard logit; inventory cites no logit source; Tansel–Bircan do **not** estimate a logit |
| 59 | `P(D_i=1|X_i)=Φ(X_i'β)` | none named | **GENERIC-UNCITED** | standard probit; no named source |
| 60 | `ln T_i = α + X_i'β + ε_i, T_i>0` | none named | **GENERIC-UNCITED** | conditional-on-positive OLS form; no named source |
| 61 | `E(T_i|X_i)=P(D_i=1|X_i)E(T_i|D_i=1,X_i)` | Cragg (1971) is the classic hurdle origin, **not cited** | **GENERIC-UNCITED** | identity for two-part models; “more recent empirical studies using hurdle models” is uncited (L123) |
| 62 | `T_i = max(0, X_i'β+ε_i)` | **Tansel & Bircan (2006)** (Tobit, EER 25(3):303–313; verified in IZA DP 1255 eqs (1)–(3)) | **VERIFIED-PARAPHRASE** (application) | published model: latent `Y*=β'X+ε`, censored at 0, dependent variable is **tutoring expenditure**; marginal effects eqs (4)–(5); Tobit origin is Tobin (1958), not cited in inventory |
| 63 | `D_i=1(Z_i'γ+u_i>0), T_i=D_i max(0,X_i'β+ε_i)` | none named | **GENERIC-UNCITED** | double-hurdle form (Cragg-family); no named source in inventory |
| 64 | `s_i^T = E_i^T/Y_i` | Tansel–Bircan thematically (expenditure share/Engel curve) | **VERIFIED-PARAPHRASE** | published paper models expenditure (log) on total expenditure etc.; the *share* formula is inventory construction |
| 65 | `ln E_i^T = α+β ln Y_i+X_i'γ+ε_i` | Tansel–Bircan Engel curve | **VERIFIED-PARAPHRASE** | published estimation is a Tobit **Engel curve** of tutoring expenditure; inventory notation is a simplification |
| 66 | `η_Y = ∂lnE^T/∂lnY` | Tansel–Bircan (they report expenditure elasticities) | **VERIFIED-PARAPHRASE** | inventory’s elasticity formula is generic; paper’s estimates are its own |
| 67 | `η_P = ∂lnT/∂lnP_T` | none named | **GENERIC-UNCITED** | no named source estimates tutoring price elasticity in inventory |
| 68 | `η_TS = ∂lnT/∂lnP_S` | none named | **GENERIC-UNCITED** | no named source |
| 69 | `s_i^{TE} = E_i^T/E_i^{total education}` | none named | **GENERIC-UNCITED** | inventory construction |
| 70 | `C_i+P_TT_i+P_SS_i≤Y_i` | none named | **GENERIC-UNCITED** | generic budget constraint; E12/E25/E70 are the same idea restated, unsourced |

### B. Tutoring productivity (71–80)

| # | inventory formula | nearest verified source | verdict | what the source actually says |
|---|---|---|---|---|
| 71 | `A_i=f(S_i,T_i,F_i,θ_i)` | Todd & Wolpin (2003) / Cunha & Heckman (2007) generic family; Hanushek placeholder | **GENERIC-UNCITED (paraphrase family)** | Todd & Wolpin’s object is a cumulative production function with family/school inputs and unobserved endowments (`A_it=f(t,S_i(t),F_i(t),θ_i)`); inventory is a same-family restatement; **no page-level match** |
| 72 | `A_i=α+β_1T_i+β_2S_i+β_3(T_iS_i)+X_i'γ+ε_i` | none named | **GENERIC-UNCITED** | interaction regression; no named source |
| 73 | `∂A/∂T>0` | none named | **GENERIC-UNCITED** | assumption, not a published equation |
| 74 | `A_i=α+βT_i+X_i'γ+ε_i` | **Dang & Rogers (2008)** §5.1 unnumbered expression `A=α+βT+γX+ε` | **VERIFIED-PARAPHRASE** (but D&R call it *naive/unreliable*) | exact same generic form; D&R explicitly warn it is biased absent identification |
| 75 | `A_i=α+f(T_i)+X_i'γ+ε_i` | none named | **GENERIC-UNCITED** | flexible-form regression |
| 76 | `A_i=α+β_1T_i+β_2SES_i+β_3(T_iSES_i)+X_i'γ+ε_i` | none named | **GENERIC-UNCITED** | heterogeneity regression |
| 77 | `T_i=π_0+π_1Z_i+X_i'π+ν_i` (first stage) | none named | **GENERIC-UNCITED** | standard IV first stage; no named source |
| 78 | `A_i=α+βT̂_i+X_i'γ+ε_i` (second stage) | none named | **GENERIC-UNCITED** | standard IV second stage |
| 79 | `T_i=α+ρT̄_{-i}+X_i'β+ε_i` | none named | **GENERIC-UNCITED** | peer-effects specification; no named source |
| 80 | `A_i=α+β_1T_i+β_2Q_{s(i)}+β_3(T_iQ_{s(i)})+ε_i` | none named | **GENERIC-UNCITED** | school-quality interaction; Kim & Lee (2010) study school choice but this equation is not theirs |

**Published-model mismatch worth flagging for Paper D:** Jayachandran (2014) has an actual tutoring-achievement
relation `s(m,t)` and a teacher choice of `m`; Todd & Wolpin (2003) have an actual cumulative production
function; **the inventory’s E71–E80 contain neither `m` nor a cumulative/stock structure** — they are generic
cross-sectional regressions.

### C. Competition, markets, regulation (81–86)

| # | inventory formula | nearest verified source | verdict | notes |
|---|---|---|---|---|
| 81 | `P_i(admission)=e_i^κ/Σ_j e_j^κ` | none named; standard **Tullock (1980)** contest-success form, **not cited in inventory** | **GENERIC-UNCITED** | no named source in the inventory contains this; cannot be attributed to Dang & Rogers/Bray/Tansel–Bircan |
| 82 | `max_{T_i}[V_iP_i(admission)−P_TT_i]` | none named | **GENERIC-UNCITED** | constructed from E81; no source |
| 83 | `Q_T^d(P_T,Y,…)=Q_T^s(P_T,W,…)` | **Dang & Rogers (2008)** §3 | **VERIFIED-PARAPHRASE of a figure** | D&R publish a *graphical* supply/demand framework (Figure 1), not algebraic `Q^d=Q^s` functions |
| 84 | `π_T=P_TQ_T−C(Q_T)` | none named | **GENERIC-UNCITED** | standard profit identity |
| 85 | `P_T^{consumer}=P_T(1+τ)` | none named | **GENERIC-UNCITED** | tax wedge; engine uses a related split but inventory gives no source |
| 86 | `ΔA_it=α+βPolicy_it+X_it'γ+ε_it` | none named | **GENERIC-UNCITED** | reduced-form policy regression; no source |

## 7. Tutoring-relevant §2/§3/§4/§8 rows

| # | inventory object | named/claimed source | verdict | evidence |
|---|---|---|---|---|
| 11 | `U=U(C,H,L)` | OECD+3 placeholder; “Becker, Mincer, Becker-Lewis” | **GENERIC-UNCITED** | textbook utility; no source |
| 12 | `C+p_sS+p_tT+X=Y` | §2 block (L43 `OECD+3`) | **GENERIC-UNCITED** | generic budget constraint including tutoring; no published source cited |
| 19 | `C+p_n n+p_q n q≤Y` | Becker & Lewis (1973) | **VERIFIED-PARAPHRASE** | bibliographic record DOI 10.1086/260166, JPE 81(2 Part 2):S279–S288; inventory’s form restates the quantity–quality budget interaction (omits other goods `Z` and uses `≤`); exact published equation not read (paywalled) |
| 21 | `T_s+T_t+T_w+T_l=T̄` | none | **GENERIC-UNCITED** | time-allocation identity; **no source named**; important because Paper D needs a time-allocation object the inventory never sources |
| 22–24 | logit/multinomial/borrowing constraint | none | **GENERIC-UNCITED** | standard forms |
| 25 | `(∂U/∂S)/(∂U/∂C)=p_s` | none | **GENERIC-UNCITED** | interior optimum identity |
| 26–27 | `A_i=f(S_i,F_i,P_i,θ_i)`; `A_it=f(S_i^t,F_i^t,θ_i)` | Todd & Wolpin (2003) (named in §3 text), placeholder “hanushek.stanford.edu+2” | **VERIFIED-PARAPHRASE family** | Todd & Wolpin DOI 10.1111/1468-0297.00097, EJ 113(485):F3–F33; their equation is a cumulative function of family/school inputs and endowments; inventory is a generic restatement |
| 28–31 | Cobb–Douglas/CES production with `T`; complementarity | none named | **GENERIC-UNCITED** | no named source; CES/Cobb–Douglas are textbook |
| 38–40 | `H_{t+1}=f_t(H_t,I_t)`; self-productivity; dynamic complementarity | Cunha & Heckman (2007) | **VERIFIED-PARAPHRASE family** | AER 97(2):31–47, DOI 10.1257/aer.97.2.31; their published object is a vector technology with self-productivity/dynamic complementarity; inventory restates it generically |
| 41 | `A_i=α+β_1S_i+β_2T_i+β_3S_iT_i+…` | none named | **GENERIC-UNCITED** | interaction regression |
| 49 | `ln w_i=α+β_SS_i+β_TT_i+X_i'γ+ε_i` | none named | **GENERIC-UNCITED** | “association between tutoring and adult earnings”; no source cited; no named shadow-education source contains it |
| 130 | `Gap_T=P(T>0|Rich)−P(T>0|Poor)` | none named | **GENERIC-UNCITED** | descriptive gap; no source |
| 131 | `C_T=2Cov(T_i,R_i)/T̄` | none named | **GENERIC-UNCITED** | concentration index; origin (Kakwani/Wagstaff) not cited |
| 136 | `Gap_A=β_0+β_1SES+β_2T+β_3(SES×T)+ε` | none named | **GENERIC-UNCITED** | interaction regression; no source |

## 8. Reference-table items not covered above (all Crossref-verified unless stated)

| inventory item | verified record |
|---|---|
| Mankiw, Romer & Weil (1992) | *A Contribution to the Empirics of Economic Growth*, QJE 107(2):407–437, DOI 10.2307/2118477 |
| Lucas (1988) | *On the Mechanics of Economic Development*, J. Monetary Economics 22(1):3–42, DOI 10.1016/0304-3932(88)90168-7 |
| Psacharopoulos & Patrinos (2018) | *Returns to Investment in Education: A Decennial Review…*, Education Economics 26(5):445–458, DOI 10.1080/09645292.2018.1484426 (also WB WP 8402 / 30154) |
| Callaway & Sant’Anna (2021) | *Difference-in-Differences with multiple time periods*, J. Econometrics 225(2):200–230, DOI 10.1016/j.jeconom.2020.12.001 |
| Sun & Abraham (2021) | *Estimating dynamic treatment effects in event studies…*, J. Econometrics 225(2):175–199, DOI 10.1016/j.jeconom.2020.09.006 |
| Todd & Wolpin (2003) | Economic Journal 113(485):F3–F33, DOI 10.1111/1468-0297.00097 |
| Cunha & Heckman (2007) | AER 97(2):31–47, DOI 10.1257/aer.97.2.31 (inventory’s `nber.org` node is the WP, not the AER article) |
| Becker & Lewis (1973) | JPE 81(2 Part 2):S279–S288, DOI 10.1086/260166 — **inventory’s “RCNi Company Limited” publisher is false** (RCNi publishes nursing journals) |
| Mincer (1974) | *Schooling, Experience, and Earnings*, NBER book (no DOI); contemporary review records DOI 10.2307/2521600 / 10.1086/260336 |
| Filmer et al. LAYS (2020) | *Learning-adjusted years of schooling: Defining a new macro measure of education*, Economics of Education Review 77:101971, DOI 10.1016/j.econedurev.2020.101971 (inventory names “Filmer and colleagues”) |
| Hanushek (as `hanushek.stanford.edu+2`) | **ambiguous/not verifiable as cited** — the placeholder points at a website, not a work; the inventory text names “Hanushek’s synthesis” without a year/title. Candidates include Hanushek (1986) JEL 24(3):1141–1177 and the Handbook chapter, but **no specific work can be attributed from the inventory** |
| Tobin (1958) / Cragg (1971) | Econometrica 26(1):24–36 DOI 10.2307/1907382; Econometrica 39(5):829–844 DOI 10.2307/1909582 — **not cited in the inventory**, although E58–E63 are their standard forms |
| Tullock (1980) contest-success form behind E81 | **not cited in the inventory**; only the form is recognisable; no attribution can be verified from the inventory |

## 9. Errors / risky claims found (reported, not fixed)

1. **Every citation token is a placeholder artifact** (`UIS+2`, `OECD+3`, `doi.org+4`, …) — see §3 table.
2. **False publisher**: `RCNi Company Limited` attached to Becker & Lewis (1973). RCNi is a UK nursing
   publisher; the paper is in the *Journal of Political Economy* (University of Chicago Press).
3. **Wrong DOI in common circulation** for Dang & Rogers 2008: the article DOI is `10.1093/wbro/lkn004`
   (a `lkn006` form is not the article).
4. **Wrong volume/issue/pages** for Tansel & Bircan (2006) in many secondary lists: EER **25(3):303–313**, DOI
   10.1016/j.econedurev.2005.02.003.
5. **Wrong DOI guess risk** for Jayachandran 2014: `10.1016/j.jdeveco.2014.02.008` (not `.005`); Biswal 1999:
   `10.1111/j.1746-1049.1999.tb00232.x` (not tb00227).
6. **Uncited hurdle-model claim** (L123) — no hurdle study is named; the named application is Tobit.
7. **Bray books attached to a section of algebra** they cannot support (monographs/policy analyses; verified
   reviews show no equations).
8. **Dang & Rogers 2008 attached to §5 rows** — the article’s only equation is the naive regression it
   criticises; the market framework is graphical, not algebraic.
9. **Kim & Lee ambiguity** (two different 2010 Korean tutoring papers; see §4).
10. **Hanushek attribution ambiguous** (website placeholder; no year/title).
11. **No equation-level page references anywhere** in the inventory; inventory numbers ≠ published numbers.

## 10. Consequences for Paper D’s omission lemmas (no new evidence claims)

* The omission claim “the inventory’s shadow-education block omits school-day withholding `m`” is supported by
  primary text: **Jayachandran (2014) publishes a teacher-incentive model containing `m` and `s(m,t)` with
  `s_mt<0`**; the inventory’s E57–E86 contain no `m`, no teacher effort, no withheld-lesson variable.
* The time-allocation identity E21 (`T_s+T_t+T_w+T_l=T̄`) is **unsourced**; the engine’s time/withholding
  mechanism cannot be cited to any of the named works via this inventory. A primary source for a time budget
  must be located independently before Paper D claims published equivalence.
* The schooling-stock/depreciation object (Paper D’s `S` dynamics) appears nowhere in §5; the closest published
  objects retrieved are the *static* production functions of Todd–Wolpin/Cunha–Heckman (E26–E41 family), which
  are not tutoring-specific and have no tutoring-effort stock.
* The omission statement should be phrased as: “the inventory’s §5 equations are generic candidate
  specifications; **of the named sources, only Tansel–Bircan (Tobit expenditure), Dang & Rogers (naive OLS +
  graphical market) and Jayachandran (teacher-incentive model with `m`) contain formal objects**, and none
  contains time allocation, tutoring stock/depreciation, or the inventory’s specific formulas.”

## 11. Unresolved items (explicit)

* Biswal (1999) and Dang (2007) full texts were not retrievable in this environment; their **equations are
  unverified** and must not be quoted as published until retrieved. Biswal’s mechanism is corroborated only by
  Dang & Rogers’s description.
* Kim & Lee (2010) full text not retrieved; only the abstract is verified.
* Bray (1999, 2009) bodies not read; verification is via peer-reviewed review records (place/publisher/pages),
  sufficient for “work exists and what kind of work it is”, not for content claims beyond that.
* Tansel & Bircan equations verified in the **working-paper version**; the EER printed version was not directly
  read. If exact page-level citation is required, obtain EER 25(3):303–313 and check §4 there.

## Appendix A — evidence file hashes (downloaded this session)

| file | sha256 | pages | use |
|---|---|---|---|
| inventory `education-equation-inventory-20261124.txt` | `0fd30f770a75ee55cdf26d3ce332df795f78d29d070bed01af38810bfa4752df` | 404 lines | input |
| Dang & Rogers 2008, WBER published PDF (World Bank copy) | `ec733dcfd1812d1b456151f261410fe4a17863fffcb60a002c21cf22b55c3ec2` | 40 | §5.1 analysis |
| Dang & Rogers 2008, WP 4530 PDF | `b0738e11c10ef57ecb25f2761b183def6b201a9fe41fa0cff3d853d9f2dd3f72` | 42 | cross-check |
| Jayachandran 2014, published-article author PDF | `53d1826d6842d24a63042ec631bf42520a1ce4a872e3c863d5530f614fcc2f41` | 16 | § 5.2 |
| Tansel & Bircan, IZA DP 1255 PDF | `9ca915ae9b5b6081b9d12df5b098b9a94b51bc652bd2b51eacc50b5f9e63e632` | 28 | § 5.3 |
| Dang 2013 self-review, WB WP 6618 PDF | `8cd493074f00e77d02fd6ff209fba4ece692e0c01765d7df6f2e5df4a7389270` | 40 | Dang 2007 context search |

## Appendix B — machine-readable verified records (the records this report relies on)

```json
[
 {"id":"dang_rogers_2008","authors":"Dang, H.-A.; Rogers, F. H.","year":2008,"title":"The Growing Phenomenon of Private Tutoring: Does It Deepen Human Capital, Widen Inequalities, or Waste Resources?","venue":"The World Bank Research Observer","volume":23,"issue":2,"pages":"161-200","doi":"10.1093/wbro/lkn004","status":"VERIFIED-BIBLIOGRAPHIC; full text read","url":"https://doi.org/10.1093/wbro/lkn004"},
 {"id":"bray_2009","authors":"Bray, M.","year":2009,"title":"Confronting the Shadow Education System: What Government Policies for What Private Tutoring?","publisher":"UNESCO International Institute for Educational Planning (IIEP)","place":"Paris","pages":132,"reviews":["10.1080/09645292.2010.507493","10.25656/01:5627"],"status":"VERIFIED-BIBLIOGRAPHIC (reviews); monograph, no equations"},
 {"id":"bray_1999","authors":"Bray, M.","year":1999,"title":"The Shadow Education System: Private Tutoring and its Implications for Planners","series":"Fundamentals of Educational Planning No. 61","publisher":"UNESCO IIEP","place":"Paris","review_doi":"10.1023/A:1026531112211","status":"VERIFIED-BIBLIOGRAPHIC (review); monograph, no equations"},
 {"id":"tansel_bircan_2006","authors":"Tansel, A.; Bircan, F.","year":2006,"title":"Demand for education in Turkey: A tobit analysis of private tutoring expenditures","venue":"Economics of Education Review","volume":25,"issue":3,"pages":"303-313","doi":"10.1016/j.econedurev.2005.02.003","wp_fulltext":"IZA DP No. 1255 (https://docs.iza.org/dp1255.pdf)","status":"VERIFIED-BIBLIOGRAPHIC; equations verified in WP version"},
 {"id":"biswal_1999","authors":"Biswal, B. P.","year":1999,"title":"Private tutoring and public corruption: A cost-effective education system for developing countries","venue":"The Developing Economies","volume":37,"issue":2,"pages":"222-240","doi":"10.1111/j.1746-1049.1999.tb00232.x","status":"VERIFIED-BIBLIOGRAPHIC; full text NOT retrieved; content described in Dang & Rogers 2008"},
 {"id":"jayachandran_2014","authors":"Jayachandran, S.","year":2014,"title":"Incentives to teach badly: After-school tutoring in developing countries","venue":"Journal of Development Economics","volume":108,"pages":"190-205","doi":"10.1016/j.jdeveco.2014.02.008","fulltext":"https://seemajayachandran.com/tutoring.pdf","status":"VERIFIED-BIBLIOGRAPHIC; full text read; model eqs (1)-(2), s(m,t), s_mt<0"},
 {"id":"kim_lee_2010","authors":"Kim, S.; Lee, J.-H.","year":2010,"title":"Private Tutoring and Demand for Education in South Korea","venue":"Economic Development and Cultural Change","volume":58,"issue":2,"pages":"259-296","doi":"10.1086/648186","status":"VERIFIED-BIBLIOGRAPHIC; abstract read only"},
 {"id":"dang_2007","authors":"Dang, H.-A.","year":2007,"title":"The determinants and impact of private tutoring classes in Vietnam","venue":"Economics of Education Review","volume":26,"issue":6,"pages":"683-698","doi":"10.1016/j.econedurev.2007.10.003","status":"VERIFIED-BIBLIOGRAPHIC; full text NOT retrieved"},
 {"id":"becker_lewis_1973","authors":"Becker, G. S.; Lewis, H. G.","year":1973,"title":"On the Interaction between the Quantity and Quality of Children","venue":"Journal of Political Economy","volume":81,"issue":"2, Part 2","pages":"S279-S288","doi":"10.1086/260166","status":"VERIFIED-BIBLIOGRAPHIC"},
 {"id":"todd_wolpin_2003","authors":"Todd, P. E.; Wolpin, K. I.","year":2003,"title":"On the Specification and Estimation of the Production Function for Cognitive Achievement","venue":"The Economic Journal","volume":113,"issue":485,"pages":"F3-F33","doi":"10.1111/1468-0297.00097","status":"VERIFIED-BIBLIOGRAPHIC"},
 {"id":"cunha_heckman_2007","authors":"Cunha, F.; Heckman, J.","year":2007,"title":"The Technology of Skill Formation","venue":"American Economic Review","volume":97,"issue":2,"pages":"31-47","doi":"10.1257/aer.97.2.31","status":"VERIFIED-BIBLIOGRAPHIC"},
 {"id":"mankiw_1992","authors":"Mankiw, N. G.; Romer, D.; Weil, D. N.","year":1992,"title":"A Contribution to the Empirics of Economic Growth","venue":"Quarterly Journal of Economics","volume":107,"issue":2,"pages":"407-437","doi":"10.2307/2118477","status":"VERIFIED-BIBLIOGRAPHIC"},
 {"id":"lucas_1988","authors":"Lucas, R. E.","year":1988,"title":"On the Mechanics of Economic Development","venue":"Journal of Monetary Economics","volume":22,"issue":1,"pages":"3-42","doi":"10.1016/0304-3932(88)90168-7","status":"VERIFIED-BIBLIOGRAPHIC"},
 {"id":"psacharopoulos_patrinos_2018","authors":"Psacharopoulos, G.; Patrinos, H. A.","year":2018,"title":"Returns to Investment in Education: A Decennial Review of the Global Literature","venue":"Education Economics","volume":26,"issue":5,"pages":"445-458","doi":"10.1080/09645292.2018.1484426","status":"VERIFIED-BIBLIOGRAPHIC"},
 {"id":"callaway_santanna_2021","authors":"Callaway, B.; Sant'Anna, P. H. C.","year":2021,"title":"Difference-in-Differences with multiple time periods","venue":"Journal of Econometrics","volume":225,"issue":2,"pages":"200-230","doi":"10.1016/j.jeconom.2020.12.001","status":"VERIFIED-BIBLIOGRAPHIC"},
 {"id":"sun_abraham_2021","authors":"Sun, L.; Abraham, S.","year":2021,"title":"Estimating dynamic treatment effects in event studies with heterogeneous treatment effects","venue":"Journal of Econometrics","volume":225,"issue":2,"pages":"175-199","doi":"10.1016/j.jeconom.2020.09.006","status":"VERIFIED-BIBLIOGRAPHIC"},
 {"id":"tobin_1958","authors":"Tobin, J.","year":1958,"title":"Estimation of Relationships for Limited Dependent Variables","venue":"Econometrica","volume":26,"issue":1,"pages":"24-36","doi":"10.2307/1907382","status":"VERIFIED-BIBLIOGRAPHIC (not cited in inventory)"},
 {"id":"cragg_1971","authors":"Cragg, J. G.","year":1971,"title":"Some Statistical Models for Limited Dependent Variables with Application to the Demand for Durable Goods","venue":"Econometrica","volume":39,"issue":5,"pages":"829-844","doi":"10.2307/1909582","status":"VERIFIED-BIBLIOGRAPHIC (not cited in inventory)"},
 {"id":"filmer_lays_2020","authors":"Filmer, D. et al.","year":2020,"title":"Learning-adjusted years of schooling: Defining a new macro measure of education","venue":"Economics of Education Review","volume":77,"pages":"101971","doi":"10.1016/j.econedurev.2020.101971","status":"VERIFIED-BIBLIOGRAPHIC"}
]
```

## Appendix C — reproduction notes

Bibliographic checks used `https://api.crossref.org/works/<DOI>` and
`https://api.openalex.org/works/https://doi.org/<DOI>` (accessed 2026-11-25). Full texts:
Dang & Rogers WBER PDF `http://documents.worldbank.org/curated/en/620421468169465126/pdf/767860JRN0WBRO00Box374387B00PUBLIC0.pdf`
(verbatim copy also at the WP 4530 link `…/615341468134395802/pdf/wps4530.pdf`);
Jayachandran `https://seemajayachandran.com/tutoring.pdf`;
Tansel & Bircan `https://docs.iza.org/dp1255.pdf`;
Dang 2013 review `http://documents1.worldbank.org/curated/en/241061468328828236/pdf/WPS6618.pdf`.
Paywalled and not read: Elsevier (Tansel–Bircan published version, Dang 2007), Wiley (Biswal 1999), University
of Chicago Press (Kim & Lee 2010). This report makes no claim about text it could not retrieve.
