# GAPS AND LEADS — what survives the brief-015 toy battery, and what to do next

**Companion to** `TOY_INVENTORY.md` / `TOY_INVENTORY.csv` (same directory). **Battery root** `TOYS =`
`10_massification/extensions/codex_2026-11-20/toys_2026-11-20/`. Every number is sourced in the inventory;
this file mostly cites mechanisms, not new numbers.

**Standing status:** the toys are ILLUSTRATIVE — stipulated parameters; not calibrated; not evidence; no
historical test; phase CLOSED. Nothing below reopens C1–C4; D79–D87 stand (`08_council/DECISIONS.md`).
The point of this file is to separate (a) hypotheses that could be taken to observed data, (b) stipulations
that must never be cited, (c) design constraints already earned, (d) genuinely different directions, and
(e) what to drop.

---

## (a) Testable hypotheses: what could go to observed data, and what observable is needed

A toy mechanism is *testable* only if (i) the quantity it names is measurable independently of the model,
(ii) the prediction can fail on the data, and (iii) the test does not re-supply the answer as a parameter.
Ten rows below cover eleven of the fifteen toys — eight as genuine hypotheses, two (#5 and #9) primarily as
measurement cautions. The four not covered (B4, B5, B6, C9) cannot be taken to observed data as stated; see (b).

| # | Hypothesis the toy encodes | Toy | Observable needed | Data status (per `08_council/DECISIONS.md` D92) | Falsifier that can fire |
|---|---|---|---|---|---|
| 1 | **Public seat expansion is partly offset by private provider exit; the object is net seats.** | A2 | Private school/HEI openings **and closures** by year-region; private enrolment; public expansion events | `SCHOOL_EXPANSION.csv` partial; dated provider approvals are public documents (CHED/DepEd), 2–4 weeks | Net/gross ≥ 0.90 (no offset) |
| 2 | **Entry and exit respond to demand with different strength and a decision→installation lag.** | A1, A3 | Dated entry approvals and exit/closure events **separately**; regional demand exposure (BPO/remittance/income growth) | Public approval lists; PSA microdata held | Exit/entry ratio inside 1 ± 0.25 **and** net ≥ 90% of gross |
| 3 | **Capacity moves the floor, but saturation is set by the eligible pool/gate, not the level.** | C7 (T7c) | Applications per seat, seat utilisation and eligible-pool size by level; capacity additions by level | `STATE_CAPACITY.csv`, `UNIVERSALIZATION_SERIES.csv`, `SCHOOL_EXPANSION.csv` (partial) — runnable now | Ceiling completions rise ≥ 50 pp, or ceiling conversion exceeds floor conversion |
| 4 | **A sectoral demand shock raises *total* participation, not just field switching.** | E14 (P1c) | Total HEI enrolment **and** enrolment by field; sector employment/return growth | `JOBS_AND_MARKETS_PANEL.csv`, economic-complexity panel — runnable now (field shares partial) | Total enrolment response ≤ 10% of the field response (pure reallocation) |
| 5 | **De jure law moves the register, not the classroom; de facto enforcement is the binding margin.** | C8 | Registration/enrolment vs attendance (LFS/net attendance); inspection visits and sanctions by district-year | Attendance on disk; **annual enforcement series held** | Attendance gain ≈ register gain at e = 0 (law binds without enforcement) |
| 6 | **Roll-out order moves crossing years but not floor→ceiling spacing; the credential pipeline sets spacing.** | D10 | Crossing years by level and expansion dates; spacing distribution across countries/regions | `UNIVERSALIZATION_TIMING.csv` — runnable now | Simultaneous expansion compresses spacing by ≥ 2 years |
| 7 | **A demographic shock matters only when capacity fails to scale** (seats per child). | D11 | Cohort size (births), seats per child, completion per child | WDI + enrolment — runnable now | Cohort-size effect on timing is the same under responsive and frozen capacity |
| 8 | **Price instruments fade; belief/information instruments persist after a temporary expansion.** | D12 | Fee-waiver/scholarship start-end dates vs information-campaign dates; applications after expiry | `POLICY_TIMELINE.csv` partial; programme dates public | Post-expiry application gap ≈ 0 for the information arm |
| 9 | **With fixed seats, application-side interventions show up as queues, not completions.** | E15 | Applications per seat, admissions, distance/road access, exposure to information | Applications data are the bottleneck (school-level); roads/distance obtainable | Admissions rise with information while seats are fixed |
| 10 | **An external credentialed route (and remittances) raises origin schooling while local formal jobs stay flat.** | E13 | Overseas deployment/remittance inflows; local formal employment; completion | WDI remittance/panel series — runnable now (sign test only) | Completion rises only where local formal posts rise (local-demand story) |

**Reading the table honestly.** (i) Only #3, #4, #6, #7, #10 are runnable on series already on disk; #1, #2,
#5, #8, #9 need public-document collection or held data, i.e. they are *designs*, not next-week analyses.
(ii) #1/#2 are the same observed cell the Council already named as the only admissible C1 re-opener
(`COUNCIL_REVIEW_016.md` §5; D83); the toy battery adds only the three estimands (entry, exit, lag) and the
net-vs-gross falsifier. (iii) #5 and #9 are **measurement cautions** more than hypotheses: their content is
"do not use the register as attendance" and "do not read applications as completions", which are true almost
regardless of the mechanism. (iv) #10 is usable only as a **sign** test: the toy's magnitude is constructed
(non-binding origin seats), so a real test can confirm or reject the sign, not the size. (v) Nothing in the
table licenses a *direction* claim about massification.

**What is not testable at all** (and should not be dressed up): B4's output-sign pattern (degenerate v=1 cell),
B5's rank rule (an extreme stipulation), B6's blind-ranking contrast (zero credential–skill correlation), and
C9's buildings result (no unstaffed-seat channel). D11's interaction is definitional and is usable only as a
definition (#7 above), and E13's completion **magnitude** is not citable. Those are (b).

---

## (b) Pure stipulation — must never be cited as a result

These are the load-bearing stipulations identified by the cluster authors and by `COUNCIL_REVIEW_016.md` §6.2.
Cite the *design lesson*, never the number.

| Stipulation | Where it carries the result | Path |
|---|---|---|
| All-or-nothing provider exit; `bk = cap` knife-edge | A2's bimodality and R = 0.486 (F=$12 gives 0.665) | `TOYS/cluster_A/PRE_DECLARATIONS.md` §0.2, Amendment 1; `FINDINGS.md` §2 |
| Contemporaneous entry/exit + symmetric ±20% shock | A1's near-symmetry (timing asymmetry is zero by construction) | `cluster_A/FINDINGS.md` §1 Caveats iii |
| Installation lock + 4-period boom | A3's 8.08 vacancy (without the lock: no overshoot) | `cluster_A/FINDINGS.md` §3 Caveats iii |
| `4(1−v)` premium → 0 at v=1 | B4's degenerate signalling cell (0 applicants) | `cluster_B/PRE_DECLARATIONS.md` §1; `FINDINGS.md` §1 |
| Extreme credential-inflation queue ("all young outrank all older-diploma") | B5's older hires 0.00 and T5.1/T5.2 | `cluster_B/PRE_DECLARATIONS.md` §2 |
| Zero credential–skill correlation | B6's blind-ranking result (0.350) | `cluster_B/PRE_DECLARATIONS.md` §3 |
| `completion = seat used` + sequential gate chain | C7's `primary_only` ceiling exactly 0.00 and ceiling max 11.67 | `cluster_C/PRE_DECLARATIONS.md` §1; `FINDINGS.md` §1.5 |
| `delta_norm = 0.010` and `e × L` mapping | C8's "paper law inert" and "enforcement without law = 0.000" | `cluster_C/PRE_DECLARATIONS.md` §2 |
| `admissions = min(physical, teacher_capacity, 120)` | C9's rooms-only +0.00 pp (no unstaffed channel) | `cluster_C/PRE_DECLARATIONS.md` §3 |
| Per-child capacity definition | D11's "no effect" under responsive capacity | `cluster_D/PRE_DECLARATIONS.md` §6.3 |
| Belief memory 0.70 / reference flow 12; skill memory 0.8 | D12's persistence, half-life and hire-decay FAIL | `cluster_D/PRE_DECLARATIONS.md` §6.1, §6.4 |
| Non-binding origin seats (170 vs peak 134) | E13's completion response (a demand channel only) | `cluster_E/PRE_DECLARATIONS.md` #13 |
| `SHOCK = 2.5` > aptitude range 1.0 | E14's 100% switching and maximal participation margin | `cluster_E/PRE_DECLARATIONS.md` #14 |
| Exposure 0.30/0.70 and kin +0.22 | E15's "interaction" (a dose effect) and the tied-village gap | `cluster_E/PRE_DECLARATIONS.md` #15 |

**Also never cite:** any toy number in a results table, an evidence column, or the phase write-up (D79, D84);
"falsifier not triggered" for B4/F4, C8's built-in null, or D10/P10-1 (Cartwright's dissent,
`COUNCIL_REVIEW_016.md` §7).

---

## (c) Design choices the battery already constrains — the eight lessons, with their toys

Adopted as design constraints by D81; each is a statement about how to build the *next* test, not about the world.

| # | Design lesson | Toy support | Operational meaning for the next predeclaration |
|---|---|---|---|
| 1 | **Supply: the object is net, not gross.** Measure private exit and net seats. | A2 (gross +20 vs net +9.73; 42/200 seeds net ≤ 0 at 30-seat capacity) | Outcome = net seats/admissions after private exit; gross public seats are an input, not an outcome |
| 2 | **Do not parameterise hysteresis.** A fixed cost alone does not buy asymmetry. Measure entry and exit separately plus the decision→installation lag. | A1 (falsifier fired, 0.008 vs 0.25); A3 (overshoot only when lag > boom) | Three estimands, not one parameter: entry elasticity, exit elasticity, lag |
| 3 | **Capacity buys the floor; saturation is gate-determined, not level-determined.** | C7 T7c (70.2% conversion vs Council's < 50% prediction; ceiling max 11.67 pp; 15% idle) | Report the eligible pool / utilisation at the ceiling, not just seats; restate A10 as a gate statement |
| 4 | **Law × enforcement are complements; register compliance ≠ classroom compliance.** | C8 (register +9.91 pp vs attendance +1.09 pp, ~9× overstatement) | Measure de facto enforcement directly; never use enrolment-on-the-books as the compliance outcome |
| 5 | **Composition beats total spend at equal budget — but only the PTR caution travels.** | C9 (PTR 3.00 best yet 22.83 pp vs split 32.79–38.16 pp) | Do not use PTR as a proxy for usable places; do not cite C9 for buildings-vs-teachers |
| 6 | **Rival non-separation constrains C3:** composition metrics + a joint lever + a rationing measure. | B4 (composition is the stable signature), B5 (rationing-conditional), B6 (single-lever nulls) | A one-lever credential/visibility test is underpowered by construction; pair the levers and measure jobs-per-applicant |
| 7 | **Timing = pipeline spacing + capacity-scaling rule + belief channel**, not the size of a temporary push. | D10 (S = 11–13 years in every arm; paired difference 0.0), D11 (only under frozen capacity), D12 (price fades, beliefs persist) | Predeclare the capacity-scaling rule and the expectation channel; do not test "size of push" |
| 8 | **Demand/access shocks carry a participation margin and show up as queues before completions.** | E14 (+24.68 total completers vs ≤ 10 allowance), E15 (admissions −0.00002 while queue +0.0481) | Separate participation from switching; separate applications from admissions; expect spatial reallocation |

---

## (d) Five "different direction" candidates the battery supports

Each is a **real-data** design, not another toy. The test that distinguishes it from a toy is stated for each.

### D1. Observed two-friction provider-entry cell (the C1 route) — highest value

- **What:** estimate entry and exit elasticities to demand **separately**, the decision→installation lag, and
  **net** seats after exit, in high- vs low-demand-exposure regions; second stage: OOS income-scaling exponents
  generated with **no exponent supplied as a parameter**.
- **Toy support:** A1 (fixed cost ≠ asymmetry), A2 (net/gross), A3 (lag > boom).
- **Observables:** dated provider approvals/openings and closures (CHED/DepEd school and programme lists, HEI
  programme approvals), private enrolment by region; demand exposure from BPO/remittance/income growth.
- **Real test vs another toy:** the entry, exit and lag quantities are **measured**, not stipulated; the
  falsifier can fire on data (exit/entry inside 1 ± 0.25 **and** net ≥ 90% of gross ⇒ supply channel recorded
  absent, C1 negative); and the second stage is an out-of-sample forecast, not a re-run.

### D2. Net-of-exit accounting of a public expansion

- **What:** take actual public school/classroom/teacher-post expansion events and measure the private
  enrolment and provider exits that follow, in a matched event design; report net/gross.
- **Toy support:** A2 (R = 0.486; 42/200 seeds net ≤ 0 at tight capacity).
- **Observables:** public expansion events (construction/teacher posts), private school closures and private
  enrolment (school lists, LIS/private enrolment), local cohort size.
- **Real test vs a toy:** exit is an **outcome measured in the data**, not a stipulated rule; the design has
  pre-trends and a comparison group; if net/gross ≥ 0.90 the A2 mechanism is simply not there — a recorded
  negative, not a parameter to change.

### D3. Gate-not-level capacity diagnostic

- **What:** where capacity was added at a specific level, ask whether completions at that level moved with the
  **eligible pool** or with seats; report applications per seat and utilisation by level.
- **Toy support:** C7's T7c failure (70.2% conversion; 15% idle; ceiling 11.67 pp even doubling everything).
- **Observables:** `STATE_CAPACITY.csv`, `UNIVERSALIZATION_SERIES.csv`, `SCHOOL_EXPANSION.csv` (partial);
  applications/place, transition and exam-pass rates, fee affordability by level.
- **Real test vs a toy:** the gate is **measured** (eligible pool, utilisation), not an imposed threshold
  function; a competing "seats explain it" model can win; the test can show capacity moving the ceiling, which
  would falsify the gate reading.

### D4. Participation-vs-switching decomposition of a sectoral demand shock

- **What:** for a sector boom (e.g. BPO/health), decompose the enrolment response into **total participation**
  and **field switching**, with field access/tracking as a moderator.
- **Toy support:** E14's T14-P1c failure (+24.68 total completers vs ≤ 10 allowance; 0.303 gate attenuation).
- **Observables:** total HEI enrolment and enrolment by field; sector employment/returns; `JOBS_AND_MARKETS_PANEL.csv`,
  economic-complexity panel; field-level completer/licensure data.
- **Real test vs a toy:** both margins are **observed** and separately identified; a design that cannot separate
  them is rejected in advance; a pure-reallocation result (total completer change inside the predeclared ±10
  allowance, as against the +24.68 the toy produced) would support the "sectoral pull" reading and falsify the
  participation-margin warning.

### D5. De facto enforcement vs de jure law (C4)

- **What:** build a district-year panel of **inspection reach / sanctions / attendance** against the de jure
  compulsory-schooling status, and estimate the behavioural margin, not the register margin.
- **Toy support:** C8 (register +9.91 pp vs attendance +1.09 pp at e = 0; +18.63 pp at e = 1).
- **Observables:** inspection visits/sanctions, attendance vs enrolment (`BASELINE_SERIES.csv`, LFS), law dates
  (`POLICY_TIMELINE.csv`); annual enforcement series currently **held**.
- **Real test vs a toy:** `e` is **measured**, not assigned; the built-in null ("enforcement without law = 0")
  is not available as a result; a null with a measured enforcement instrument is evidence against the de facto
  story.

**Runner-ups (not in the five, but supported):** price-vs-belief temporary-push design (D12; needs programme
start/end dates) and queues-not-places access test (E15; needs school-level applications). Both are weaker on
data availability, not on mechanism.

---

## (e) What should be dropped from the portfolio

1. **Drop C9 (buildings vs teachers) as a toy.** It is an artefact by construction: `admissions = min(physical,
   teacher_capacity, 120)` has no unstaffed-seat channel, so rooms-only completion is exactly 0.00 pp by
   definition (`cluster_C/FINDINGS.md` §3.3; `COUNCIL_REVIEW_016.md` §1). Keep one sentence — "PTR is not usable
   places" — and the DATA ASK for real construction cost; retire the experiment.
2. **Drop D11 (cohort shock × capacity) as a finding.** Under responsive capacity the seats-per-child stock is
   identical by construction, so the "interaction" is arithmetic (`cluster_D/FINDINGS.md` §2.3; review §1).
   Keep the definition ("a demographic shock is only a shock when capacity fails to scale"); do not carry the
   +4.0 years / 240-240 numbers.
3. **Drop E13 (migration/remittance) as evidence.** Origin seats are deliberately non-binding (170 vs peak 134),
   so the completion response is a demand-channel construction that would be a queue under binding seats
   (`cluster_E/FINDINGS.md` §2.1, §6; review §1). Keep the **count-migrants-once** measurement note.
4. **Disarm B4's falsifier and retire the "output direction" test.** F4's v=0 leg can never fire (HC adds +1.0
   skill by definition) and the v=1 cell is degenerate (premium 4(1−v) = 0). Keep only the composition lesson
   (`cluster_B/FINDINGS.md` §1, §5; review §7 Cartwright).
5. **Never re-run to rescue a thin PASS.** A2 (0.486), A3 (8.08), C7 T7c/T7e, D10 P10-3, E14-P1c, E15-P1/T15-P3
   are boundary artefacts; re-running or re-parameterising them is on the Council's KILL list
   (`COUNCIL_REVIEW_016.md` §4.4; D86). If the battery is kept at all, keep it as the labelled design appendix —
   **do not add a 16th toy** (D82, D86).

**Net recommendation.** The portfolio's durable output is 5 informative design constraints (#1, #7, #8, #10,
#14), 4 boundary-conditioned results that may be cited only as directions (#2, #3, #12, #15), and 6 toys that
should not be cited at all (#4, #5, #6, #9, #11, #13). The single forward move is **D1**, which is also the
Council's D83; D3 and D4 are the strongest of the directions that can start on data already on disk (with the
D10/D11/E13 sign-diagnostics as cheaper, lower-value companions).

---

## (f) Integrity / mislabel summary (details in `TOY_INVENTORY.md` §5)

1. **`README.md` fails its own SHA-256** (`71a49cb6…` vs `0fe6b6fb…` in `SHA256SUMS.txt`); 59/60 entries verify.
   `SHA256SUMS.txt` is timestamped 19:14:42, the README 19:20:10, the review 19:19:46 — the README's mtime
   post-dates both the hash file and the review, so the checksum is stale, not fabricated. Fix = regenerate
   `SHA256SUMS.txt` (and add `COUNCIL_REVIEW_016.md`, which is not covered).
2. **`cluster_A` has no `seed = AGG` rows** in `RESULTS.csv`, although both its predeclaration (§4) and findings
   (§6) say the aggregates are written there. Aggregates are in `RESULTS_SUMMARY.json`/`verdicts.json`; no data lost.
3. **"Several include a `verify_results.py`"** (`README.md` line 63) — only `cluster_E` does. A and D have no
   independent verdict re-derivation; B has `test_toys.py` (structural) and C has `selftest.py` (invariants).
4. **D10 prose error:** `cluster_D/FINDINGS.md` §1.3 says "`upper_first` not until 13" while the table gives 13 vs
   `primary_first` 16 — i.e. earlier, not later. Numbers correct; the sentence is wrong.
5. **Path labels:** all predeclarations/manifests (and most findings) still say `extensions_archive/…`; the
   canonical tree is `TOYS/`. The ~30 MB duplicate recorded in D84 was not present under
   `experiments/massification-2026-11-20/` or `massification_live/` at audit time — only the label issue remains.
6. **Disclosed and consistent:** C's predeclaration re-freeze (11:03:59Z → 11:05:55Z, hash `b0b0bdef…`, only F7's
   applicability condition changed); D's post-run P10-3 comparator defect with a full re-run; E's per-village →
   per-household unit fix that flipped T15-P3 from PASS to FAIL (conservative direction); A's Amendment 1.

*Label applies to everything here: ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no
historical test; phase closed; do not cite numbers as estimates.*
