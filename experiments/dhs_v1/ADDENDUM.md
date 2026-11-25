# Addendum — simulator, equation inventory, dense matrix, and the Domus/Massification mapping

**Scope of this addendum:** what the eight DHS experiments can and cannot say to the
Atlas models. It is deliberately conservative. Nothing here claims the models are
calibrated, and nothing here treats previously used data as untouched.

---

## 1. What is actually in this checkout

| Component | Located? | Where |
|---|---|---|
| Education-system simulator / engine | **Yes** | `engine/` (`eduengine/`, `camchild.py`, `floorworld.py`, `childworld*.py`, `countries/`, `firms/`, `mc.py`, `atlas_sobol.py`) |
| Massification family | **Yes** | `src/data/model-catalogue.ts`, `education-journey.ts`, `model-tags.ts`, `translations.json` |
| Model catalogue | **Yes** | `src/data/model-catalogue.ts` — 56 entries, 9 families (per `docs/AUDIT_MODEL_COVERAGE_2026-11-19.md`) |
| "150-equation inventory" | **Not found** | No artifact in `research/`, `docs/`, or `engine/` matching this description. `docs/engine/facts_register.md` and `cambodia_observation_equation.md` exist but are not an equation inventory. |
| "Prior dense matrix" | **Not found** | No file or document matching. `research/phase-transition*` and `wt2/dense` worktrees exist but the artifact is not present in this checkout. |
| "Domus v44" | **Not found** | The only occurrences of "Domus" are the starter README and `public/reference/mandala/model_card.json`; neither is a v44 model specification. |

**Consequence:** the equation inventory and dense matrix cannot be *integrated* here
without inventing them. What follows maps observables and specifies what integration would
require. That is the honest deliverable; manufacturing a 150-equation list would be
fabrication.

## 2. Observable mapping (verified fields → model quantities)

Each row is a DHS observable this run actually estimated, and the model quantity it could
constrain. "Compatible" means same definition; "adjacent" means related but not the same
measure.

| DHS observable (this run) | Model quantity | Status | Why |
|---|---|---|---|
| Attendance 14–17 by wealth quintile | enrolment/attendance by household asset rank in the education engine | **adjacent** | model wealth is a parameterised asset index, not the DHS `HV270` construct; quintile cut-points differ per wave |
| Attendance by residence | urban/rural enrolment gap | **compatible** | both are a binary residence contrast, though the definition of "urban" differs by country |
| Attendance by sex | gender gap in attendance | **compatible** | direct |
| Children ever born, women 40–49 | completed fertility by education | **adjacent** | model fertility is a transition rate; CEB is a stock over a lifetime, sensitive to cohort and mortality selection |
| Birth before 20 | early-fertility hazard | **adjacent** | a single-threshold indicator, not a hazard; schooling may post-date the birth |
| Union before 20 | union formation timing | **adjacent** | first *union*; Cambodia 2000 measures first *marriage* |
| Current school participation 20–24 | tertiary/late-secondary continuation | **adjacent** | mixes institution types; no completion |
| Current household size, women 40–49 | household size | **incompatible as kin support** | household size is co-residence, not kin network or support |

**Two observables the models need but this run does not provide:**
schooling *completion* (we have attendance and years, not credentials) and the model's
"exits" (we observe attendance states, not transitions). These are distinct observables and
must not be treated as interchangeable.

## 3. Three genuinely distinct follow-on analyses — and what each needs

None of these is run here. Each is specified so it is not confused with the descriptive work
above, and each is **BLOCKED** pending real additional data.

1. **Migration.** Requires a migration-history or place-of-birth/prior-residence module.
   DHS has no migration history; the PR recode gives current residence only. Local files
   contain no such module. *Blocked: no verified source with timing and origin.* A design
   must fix geography, timing and a feasible counterfactual before any estimation.
2. **Agricultural prices.** Requires price series matched to survey clusters and fieldwork
   months. No price data are present locally, and cluster geocodes are restricted.
   *Blocked: no price data, no approved geocode access.*
3. **Education spending.** Requires household education expenditure (or per-capita public
   spending matched by region/year). The DHS household questionnaire as held here has no
   expenditure module. *Blocked: variable absent from every local recode.*

Each of these is a different unit of analysis from the eight experiments, and none may be
satisfied by re-labelling an existing DHS variable.

## 4. Calibration honesty

- These experiments are **validation targets**, not calibration inputs. A descriptive gap
  (e.g. E1's wealth gradient) constrains a model only once the model's wealth construct is
  shown to be the same object; §2 shows it is adjacent at best.
- **One aggregate fit discriminates weakly** between mechanisms (the repo's own
  `research/README.md` makes this point). E3's sign reversal and E7's non-narrowing gap are
  more useful as *falsification* targets than as fit statistics: a model that cannot produce
  a male→female crossover while also producing a stable early-union gap is wrong regardless
  of its aggregate attendance fit.
- **Prior held-out data are not untouched.** The Cambodia attendance series used for
  validation in §3 of the report has already informed earlier credential-floor work; it is a
  replication target, not out-of-sample evidence. Any claim of out-of-sample predictive
  success must use outcomes that have not already influenced model design.
- The two E4/E8 findings that most constrain the models are (a) the education gradient in
  completed fertility narrowing sharply in Cambodia and (b) household size being
  **unrelated** to schooling there. (b) is a negative result and should stop any model that
  uses household size as a proxy for kin support or for schooling's household returns.

## 5. What integration would require

To actually integrate the simulator, an equation inventory and a dense matrix, a subsequent
task needs: the equation inventory file (with equation IDs and parameter provenance), the
dense-matrix artifact and its provenance, and the Domus v44 specification. With those, the
mapping in §2 can be completed row-by-row and each parameter labelled measured / estimated /
calibrated / assumed, as `research/README.md` requires.
