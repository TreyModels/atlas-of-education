# COEVOLUTION DESIGN BRIEF — education massification as mutual adjustment (user directive, 2026-11-21)

**Status: design directive from Dr. Menefee (verbatim substance preserved below in §1); translated into a
predeclaration-ready spec in §2–§5. NOT RESULTS.** This opens a **new modelling phase** after the closed
massification phase and the closed generator line. Rules inherited: predeclare before any run; label
OBSERVED / DERIVED / SIMULATED; no causal or direction claims; no putting next year's seat totals into the
inputs; report all cells; deterministic scripts; keep the closed records untouched.

## 1. The directive (as given)

Model education massification as a **historical process in which families, schools, and employers change one
another's choices**: a family decides whether another year of school is worth it given the schools and jobs within
reach; a provider decides whether enough pupils can come, or whether the state will pay, to justify another class;
employers and admissions offices decide what a qualification gets its holder; by the time the next family chooses,
earlier decisions may have changed all three conditions. **Put the decisions in motion and see which kinds of
education system they produce.** Universalization is one possible outcome; stalled expansion, persistent rural
exclusion, and widespread secondary schooling followed by fierce competition for a few prestigious places are
equally important to explain.

**Three demand objects must stay distinct:** *knowledge* ("I want my child to be able to do or understand this");
*education* ("I want my child to attend this institution and have the experience, relationships, standing, or
future options"); *a credential* ("without this certificate my child cannot apply"). They can coincide in one
purchase, and **spending alone cannot tell us how much a family values each**; observed demand is what people do
given the choices available, an imperfect measure of what they value (the FFS link: a farmer can value knowledge,
learn the practice, and decline to use it at the prevailing price).

**The smallest system to put in motion:** a town with an elite secondary school, surrounding rural communities with
uneven primary provision, and a small post-secondary sector; follow successive cohorts. Four decisions suffice for
a first version:
1. **Household chooses the next year, with an actual alternative** — attendance feasibility, fees, transport, time,
   work/care displaced, what stopping forgoes, the option value of keeping a future open, and the child's wishes.
2. **Someone supplies the next place** — a district authority chooses: open a rural class, add a section, or spend
   elsewhere; where private provision is relevant, a provider asks whether fees from families able to attend sustain
   a class. A rural community can have many willing children and fail either test. **If we supply seat totals in
   advance, we have answered the supply question ourselves.**
3. **Each transition has a named gate and someone who controls it** — passing primary, securing *any* secondary
   place, entering a sought-after secondary school, winning university admission; admission by residence,
   examination, fees, or combinations. Tutoring must be available **both** to a pupil struggling with ordinary
   instruction (catch-up) and to one competing for a selective place (gate), and its concentration around gates
   must be **inspected after the run**, not written in by construction.
4. **One cohort changes the next cohort's circumstances** — more primary completers create a constituency for
   secondary places; a nearby secondary class can make finishing primary worthwhile for a younger sibling; more
   graduates can induce firms to change production, raise hiring requirements, or compete for the same work.
   Start with the economy steady, then introduce each response separately and ask when it changes the path.

## 2. The decisive test: **coexisting withdrawal and competition**

In one district and cohort: (a) **unused accessible places** (a free place within formal reach that is not taken,
because commute cost, adolescent labour, or no credible onward route), (b) **early leaving**, (c) **oversubscribed
selective places** (qualified applicants turned away), (d) **concentrated tutoring** near the selective gate —
all four simultaneously. Name precisely **what has two peaks** (tutoring expenditure? applications per place? years
completed?) — these are different claims. Then change **one** thing at a time: cut travel costs; expand ordinary
seats; expand selective seats. Each should help **different** families for an intelligible reason. **If all three
changes produce the same response, the schools are represented too crudely.**

## 3. Two report cards (success criteria)

**Report card A — the statistical portrait.** From pupil-level records (age, level, enrolment, progression,
repetition, completion) compute:
- **NER** (official-age enrolled at the level ÷ that age population) — cannot exceed 100;
- **GER** (all enrolled at the level ÷ official-age population) — **can exceed 100**; report repeaters/over-age;
- **out-of-school** separately (a child at a higher level is outside the conventional NER numerator but in school);
- **tertiary GER** using the standard five-year age group immediately after the official secondary leaving age;
- cohort completion, transition rates, and **rural–urban** differences;
- **post-secondary non-tertiary** provision distinguishable where it matters.
UIS metadata (country series, age bands, level mappings) must be verified before any cross-country comparison —
we cannot live-check it here; flag it as a held verification item.

**Report card B — the explanation.** Can the same decision rules produce expansion in one setting and a stall in
another? Who enters first, who follows when a school opens nearby, who leaves despite available places, where
families buy extra instruction? Does the system behave plausibly when a mandate comes before funding, when fees
disappear but travel costs remain, when degrees spread faster than graduate jobs? **Judge the sequence,
distribution, and response to change.** Next year's NER is a useful check; it **earns little credit if obtained by
putting next year's seat total into the inputs.**

## 4. Cross-country plan

Keep household, provider, admissions and employment decisions **common**. For Cambodia, the Philippines, China and
Hong Kong, document the actual institutions **in a named period**: who paid, who opened places, how pupils were
assigned, which examination mattered, what tutoring families could buy, what leaving made possible. Each country
needs **within-country variation** (urban vs rural under the same national rules). Start with **one historically
documented expansion and one comparison where a similar expansion stalled or took a different form**; write down
**before looking at outcomes** where the same explanation should travel and where institutional differences should
change the result. Hong Kong's tutoring discrepancy becomes valuable once ages/providers/periods are comparable —
it can tell us which demand the account overlooks. **Do not add a country-specific tutoring preference to fit.**

## 5. First paper-sized question

**When does opening the next level change demand for the level below it?** A secondary school opening within reach
may change a parent's decision to keep a younger child in primary years before that child can apply. If so, what
looked like weak demand for primary education may have been a reasonable response to a system that offered nowhere
to go afterwards. This is the mechanism to model, a proposition to investigate historically, and a direct answer to
what an enrolment figure actually tells us.

## 6. Implementation plan (Lead translation)

1. **New phase dir** `10_massification/extensions/coevolve_2026-11-21/`: `PRE_DECLARATIONS.md` (frozen before any
   run), `code/` (one deterministic simulator), `results/`, `FINDINGS.md`, `RUN_MANIFEST.json`, `SHA256SUMS.txt`.
2. **Model v0:** a town + N rural villages; primary provision uneven (some villages no school); one elite secondary
   school and ordinary secondary places; small post-secondary sector. Agents: households (income, distance, child
   age/ability, siblings, labour value), district authority (budget; open rural class / add section / elsewhere),
   private provider (enter if fees sustain a class), gate controllers (residence / exam / fee rules per transition),
   employers (hiring requirement rule, production response). Cohorts followed year by year.
3. **Tutoring block:** catch-up (triggered by failing to follow instruction) and gate (triggered by admission
   margin), priced, with access constraints — the concentration must be an output, not an input.
4. **Baselines and counterfactuals (all predeclared):** baseline; travel-cost cut; ordinary-seat expansion;
   selective-seat expansion; mandate-before-funding; fees abolished with travel costs remaining; graduate supply
   growing faster than jobs. Paired seeds.
5. **Outputs:** pupil-level records → report card A; district-level coexistence metrics; report card B comparisons;
   the endogenous-demand-spillback experiment (§5).
6. **First deliverable:** v0 report on whether the four coexistence phenomena arise in the same district/cohort,
   and the three one-change responses differ by family type. Failures reported as failures.
