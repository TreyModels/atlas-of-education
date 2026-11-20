# PRE-DECLARATION / DESIGN NOTE — portability checkpoints A6 (CHN) and A7 (HKG), prepared before any run

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** design note, **NOT run**; prepared against the fixed PHL
behaviour from the completed A1 anchor (branch `dbec38e`, anchor_out). **Authority:** ANCHOR_SYSTEM.md §D (portability
protocol), A5/A6/A7 (R20/R28), `UNIVERSALIZATION_MILESTONES.md` (M0–M4, censoring, ±5 y/±3 y), A10/R29 (floor/ceiling,
capacity response fixed), D56–D58/D61 (phase cap). Nothing is fitted here.

## What is FIXED (may not be re-fitted — behavioural re-fit = FAIL, R20)
- The behavioural core: household demand/liquidity rules, schooling production/progression response functions,
  state-capacity response function (same gate form `G(C)=C^κ`, κ=0.75 declared), provider/cohort accounting.
- The **PHL parameter values** estimated in the anchor/PHL cells (held fixed; not re-estimated on CHN or HKG).
- The A6/A10 verdict structure: capacity is a **floor precondition**, not a ceiling sufficiency; crossing years are
  never fitted; the standing scaling FAIL appears in every portability table.

## What may be re-set (declared country inputs, dated)
Initial cohort structure; observed income/urbanisation/sector-share/remittance paths; **policy-marker dates**;
**capacity trajectories C_t** built from each country's observed series (fiscal/delivery/enforcement with the same
declared weights and the same missing-input rule: drop weight, renormalise, never impute); institutional level/gate
mapping; measurement definitions (completion vs enrolment vs attendance), harmonised or excluded (brief 013 §6).

## A6 — CHN portability (massifying state-push system)
Declared inputs: policy markers 1986 Compulsory Education Law, 1999 higher-education expansion, 2006 rural fee
abolition (dates exogenous, R12); observed series from `04_data`/`10_massification/data`; capacity C_t from CHN fiscal
(education %GDP where observed), delivery (PTR primary/secondary, teacher counts), enforcement proxy (compulsory
duration). **Declared expectations (pre-run):** the gate should explain why the 1986 law misses the primary crossing by
~27 y (low capacity then) while the 1999 expansion aligns at tertiary (+4.70 pp, t=7.94); CHN lower-secondary
completion crossed ≥90 around 2016 — test timing within ±5 y and the M0/M1 censoring rules. **Metrics:** M0–M4 crossing
years/intervals (left/right censoring per `UNIVERSALIZATION_MILESTONES.md`), ordering/gaps, level check-only where
censored, §3 tolerances (5/8 pp, beat persistence + linear trend) where levels are observable, event-marker alignment
screen (R24) before any event-break claim. **Failure modes to report, not fix:** crossings outside ±5 y; generated
universalization the CHN record does not show (R6); any need to re-fit behaviour (then portability = FAIL).

## A7 — HKG portability, TIMING-ONLY (near-universal system)
Declared inputs: policy markers 1971 free primary, 1978 nine-year compulsory, 2009 free senior secondary, 2012 HKDSE
structural context; observed NER/GER series (HKG has no UIS completion → levels are **CHECK-ONLY**); capacity C_t from
HKG fiscal (EDB table) and delivery (PTR 23.7→13.4).
**Timing regime:** HKG crossings are **NER-based**: NER ≥90 crossed **1974** (3 y after the 1971 reform), NER ≥95 crossed
**1979** (threshold-specific; the scout 1978–79 row is the ≥95 crossing). Test the model's generated crossing years
against those bands within **±5 y** (±3 y where band ≤2 y); left-censored milestones = boundary constraint only (model
must cross at/before Y0); no level fitting, levels check-only. **Failure modes:** timing miss outside tolerance; generating
a crossing the record does not show; requiring level re-fit (FAIL).

## Verdict vocabulary and gates
PASS only if, with **fixed PHL behaviour and parameters**, the portability crossings/levels meet the declared
tolerances and the event-marker screen (R24) is respected; PARTIAL if timing partially reproduced; FAIL if the port
requires behavioural re-fit (R20) or shows a false crossing (R6); **EQUIVALENT** if the same record is matched by the
fixed-behaviour port and a re-fitted comparator (no identification, R3/R13). Data asks that would strengthen both:
JPN/HKG completion series (UIS absent → national sources), annual classroom construction, CHN/HKG capacity series with
vintage; per-student spending/revenue capacity (DATA BLOCKED). **No run before Council intake approval**; no direction
claims; no git writes.
