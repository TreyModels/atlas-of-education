> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# SYNTHESIS 010 — adversarial review: "Overflow Governance" (for the author, via `lead`)

**Verdict.** A genuinely interesting hypothesis with an evidence base thinner than its claims, and a theory that
cannot currently fail. **Not publishable as-is.** It can become two publishable objects — a measurement/framework
paper and a rebuilt theory paper — but only after the factual spine and the falsifiability package are fixed. The
Council read v1 (complete) and v2 (truncated at §4.1); every number below cites on-disk files.

## 1. Draft forensics

| Item | Finding |
|---|---|
| v1 vs v2 | v1 complete; v2 ends mid-sentence at §4.1 ("…social mobility") and changes Korea to "over 80%". Keep v1 as the historical record; if v2 is a revision, finish it and label it. |
| Byline | v1: "[Name] & Mark Bray". v2: co-author blank. **A co-author line is a factual claim.** Keep Bray only on a version he actually co-authored (with his agreement); otherwise cite him as literature — the paper already cites Bray extensively. |
| Korea claim | v2's "over 80%" is wrong for all levels; official 2023 (on disk) = 78.5% all, 86.0 elementary. v1's "over 75%" is consistent. |
| Numbers not on disk | "40% of household education budgets", "300,000 instructors", Taiwan 26→83%, Singapore/Finland/NL/Germany/Greece/India/Brazil/Madagascar claims — all unverified here; flagged, not asserted. |

## 2. Evidence audit per regime

| Regime | Cases in paper | On-disk evidence | Verdict |
|---|---|---|---|
| **I Contained** | Singapore, Netherlands, Germany | **No shadow-incidence data** in `shadow_round2`/`SHADOW_TARGETS`; Singapore/Germany not in programme data | **Thinnest cell — untested.** Remove unsourced claims or source them. "Contained" needs criteria: gate-clearing share of tutoring, marginal return to tutoring, gate-position predictive power. |
| **II Arms race** | Korea, Taiwan, Japan, Greece | Korea official 2023 (78.5 all; 86.0/75.4/66.4; spend 398/449/491k; +23.4%); HKG 2003 (35.1/46.6/70.3); Japan grade-6 41.8 (22.1–57.9) | **Korea contradicts the stated mechanism as written** (falls with stage); HKG — omitted from the typology — fits it. Two-margin structure required. Taiwan/Greece no on-disk data. |
| **III Ritualised compensation** | India, Bangladesh, Brazil | No on-disk shadow data; citations unverified; **Banerjee et al. 2007 misused** (see §5) | **Unsupported as written.** Needs measured incidence and motive data, or drop to illustrative. |
| **IV Substitution** | Cambodia, Central Asia, Madagascar | Cambodia case on disk (G9 68.4, primary 41.3, urban/rural 60.5/26.4, fees 500–1,000 Riel/session, teacher US$44 vs US$80–100 tutoring); one district, six schools, 444 students | **Strongest-supported section — as a case study.** Say the scope in the same paragraph. Central Asia/Madagascar unverified here. |

**The omitted case.** HKG's rising stage gradient is the cleanest evidence for the paper's own Regime II mechanism, and
the typology leaves it out. **The Korea/HKG contrast is the paper's real puzzle:** participation falls with stage in
Korea while spend/student rises; HKG rises with stage. No one-margin terminal-gate story produces both (this is brief
009's predeclared impossibility for one-margin families). The missing structure is **participation × hours/spend** — a
two-margin account, not a regime label.

## 3. Operationalisation (the paper's main theoretical repair)

- **Differentiation** (measure, don't label): vocational/technical share of upper-secondary enrolment; number of
  nationally certified post-secondary pathways; track-mobility rate; returns to non-university qualifications;
  employer credential requirement in hiring (brief 009 P17 — currently **no empirical requirement schedule exists**).
  Institutional complementarity matters (THELEN): Germany's dual system is not "differentiated tracks" but a
  state–employer–union certification configuration.
- **Responsiveness** (one switch, not four elasticities): the scout's capacity-binding flag — tax/GDP 13.1%, GDP pc
  US$1,706, 1990 secondary GER 47.3%, urban 40.2% (`09_relations/COUNTRY_TYPOLOGY.md`) — plus a spending-response
  term (R01 = 0.111 world; Asia 0.189) and a policy-change count. "Responsive" must not be a proxy for "rich".
- **Ritual** (needs observables, not persistence): time use (KOR 7.3 h/week; HKG modal 6–10 h/month); motive surveys
  (KOR purposes: makeup 49.6%, advance 24.0%, next-level 14.2%; HKG: exam prep 84.5% at S6-7 vs homework guidance
  60.3% at S1-3); normative attitudes. **On these data the ritual claim is not supported** in the two measured cases —
  state it as an open hypothesis.
- **Intentional vs functional**: "states displace" is a functionalist slide. Either document intent (Korea hagwon
  policy; China 2021; PH K-12 — which shows a state *raising a floor*, a counterexample) or state it as an
  unintended-consequence hypothesis.

## 4. Four predeclared predictions to add (with thresholds)

1. **Ban re-route:** at unchanged gate stakes, post-ban measured paid spend persists ≥50% of pre-ban (informal/
   teacher channels); a genuine collapse (<25%) weakens the overflow account. Data now: China post-2021 ">80% did not
   attend" is an inequality, not a rate (low confidence); Korea curfew/fee-cap episodes; KHM teacher-sold.
2. **Transition requires status recalibration:** admissions/employer-return changes reduce tutoring; regulation alone
   produces ≥50% displacement. Contrast China 2021 (regulation only) with admissions reforms (Netherlands/Germany
   descriptions). The PH K-12 reform (floor raised, admissions unchanged) is a stated counterexample to test.
3. **Regime I misclassification test:** if tutoring is *required* to clear gates (gate-clearing share high, marginal
   return non-zero), the regime is misclassified as contained.
4. **Ritual test:** participation persists where marginal learning returns ≈0 and normative (non-exam-instrumental)
   motives exceed 50%. Current KOR/HKG motive data are instrumental — the prediction is at risk there and the paper
   should say so.

Add a fifth typology test: regime cells should differ in provider mix (Regime IV teacher-sold high; Regime II
commercial mass-lecture high — KOR hagwon 241/434k won spend; HKG mass lectures 72.4% at S6-7).

## 5. Citation audit (flagged, not asserted)

- **Banerjee, Cole, Duflo & Linden (2007)**: the cited study is the *balsakhi remedial-education RCT*, which reported
  **positive** learning effects; it is not a study of private tutoring and does not support "minimal academic gains
  from private tutoring". Misattribution — fix before submission.
- **Liu & Bray (2020)** is cited for India/coaching bans; the reference is their IJED paper on **Ethiopia, Kenya and
  Tanzania**. Concrete mismatch.
- Unverified this session (do not assert; verify at source): Gupta (2021, CER), Agarwal (2020, Sage), Whitaker (2010,
  LAP), Zhang & Liu (2022), "40% of household education budgets", "300,000 instructors", Taiwan 26→83%,
  Singapore/Finland/Netherlands/Germany/Greece/Madagascar/Central Asia claims.
- Missing rivals: Thurow (1975) job competition, Spence (1973)/Arrow (1973) signalling, Hirsch (1976) positional
  goods, Raftery & Hout (1993)/Lucas (2001) MMI/EII (Lucas cited but not engaged), and **Bray's own shadow-education
  framework** as the primary rival. Meyer is cited; world-culture theory is not engaged as a rival.

## 6. Publishable objects, ranked — and the referee amendments

**(1) Measurement/framework paper** from this programme — "Measuring massification and shadow education across six
Asian systems": six country cards, 21-row shadow register, 2,747 target rows, parameter map (8 observable / 10 not),
capacity-binding typology, Korea/HKG anomaly. Strongest evidence; venue `Compare`/`IJED`/`Comparative Education`.
**(2) Theory paper rebuilt** — one byline, Cambodia-led, Korea/HKG two-margin puzzle, measurement appendix, four
predictions, rivals engaged. Venue `Comparative Education Review` (conditional).
**(3) Cambodia teacher-sold case** — one district, fee/salary economics, mechanism documented; venue `Compare`/`IJED`.
**(4) Combined two-paper package.** **As-is: not publishable.**

**Exact amendments a referee will demand:** (i) one byline and one complete text; (ii) replace Korea numbers with
official 2023 and drop "over 80%"; (iii) add HKG and the two-margin contrast, revise Regime II; (iv) delete or source
every Regime I claim and define "contained"; (v) fix the Banerjee and Liu & Bray citations; verify the four flagged
references and the budget/instructor figures; (vi) separate structural/functional/ritual claims and label the
functional claim a hypothesis; (vii) add the measurement appendix (differentiation, responsiveness, ritual); (viii)
predeclare the four predictions with thresholds; (ix) engage Thurow/Spence/Arrow/Hirsch and Bray as rivals; (x) state
scope limits (Cambodia case; HKG 2003 second-hand caveat; no claim of validation); (xi) remove "states displace" as
stated until documentary evidence is supplied or rephrase as unintended consequence; (xii) reconcile the PH K-12
counterexample (state raised a floor, not designed overflow).

## 7. Cross-links to programme evidence

Brief 003 (formal-access conditional; income discriminator withdrawn) — the paper's credential mechanism must not
rest on wage-premium evidence. Brief 006/008 (identification limits; 8/9 stop rules fired) — the paper may cite the
programme only as a negative/measurement map, never as validation. Brief 009 (seven families; predeclared empty
support for one-margin KOR profile; complexity axis PENDING) — Regime I ≈ F1, II ≈ F2/F6, III ≈ F3 + income gradient,
IV ≈ F3 teacher-sold; the two-margin requirement is F6/R23. `09_relations` R01/R04/R07/R13 supply the panel context;
`PARAMETER_MAP` shows why the typology's mechanisms are mostly unobservable with current data.

## 8. The three things the author must fix first

1. **One byline, one complete text.** Resolve the Mark Bray co-authorship (keep only if real; otherwise cite as
   literature) and use the complete v1; if v2 is a revision, finish it.
2. **Fix the factual spine.** Correct Korea to the official 2023 numbers; add the Korea/HKG two-margin impossibility
   and HKG as a case; replace the Banerjee et al. misuse and the Liu & Bray India mismatch; source or delete the
   unverified figures.
3. **Make the theory falsifiable.** Separate structural/functional/ritual claims; operationalise differentiation and
   responsiveness (one capacity-binding switch); predeclare the four predictions with thresholds; engage the
   queue/signalling rival. Without this the manuscript is a hypothesis essay, not a testable theory.

## 9. Dissent recorded

BRAY: Regime IV should lead but only as a case study; a second measured case is needed before any regime claim.
PATRINOS: the measurement paper ranks first because it is the only data-backed object; theory second, conditional.
THELEN: the typology is a labelling scheme until differentiation has measures (track mobility, returns by pathway,
employer recognition); HKG's omission is a warning sign. CARTWRIGHT: the functional claim can survive only as an
explicitly labelled hypothesis with the intentional/unintended distinction. No dissent on "not publishable as-is."
