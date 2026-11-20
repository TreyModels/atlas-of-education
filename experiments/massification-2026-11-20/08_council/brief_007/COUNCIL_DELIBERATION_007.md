> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# COUNCIL DELIBERATION 007 — country-evidence-driven experiment slate

**Panel (AI composites):** BRAY (shadow education, mandatory), PATRINOS (education economics; steel-man), PAGE
(model reasoning).
**Input:** `brief_007/BRIEF.md`; on-disk evidence (country cards, `SHADOW_TARGETS.csv`, target/economy series,
`04_data/shadow_round2/`, loop2 calibration + ledger, loop3 stop-rule, loop4 U1/U1b/U2/U3, `RESEARCH_LOOP.md`).
**PENDING:** `09_relations/RELATION_CANDIDATES.csv`, `DATA_PATTERNS.md`, `MODEL_PLUG_MAP.md` — directory exists,
empty at intake. No relation id is invented; every experiment carries a relation slot PENDING and a design-intent
type.

## Agreed

1. **Korea is the calibration/identification anchor, not an incidence check.** Official 2023 data (86.0/75.4/66.4;
  fees 434/553k won; provider spend 241/37/22/16) are high-confidence; loop-4 U1 already shows the model's by-level
  ordering is inverted, which is a structural, not parameter, failure.
2. **Hong Kong 2003 is a check, not a calibration.** 35.1/46.6/70.3 is the usable stage anchor; U1b shows shape-pass,
  level-fail, provider-order-fail. The 2010 85% stays the single calibration moment and the 1996/2010 surveys stay
  low-confidence.
3. **Japan's prefecture range is the best within-country variation in the set** (41.8% mean; 22.1–57.9% range).
4. **China is a bounded prior only** (2014 29.8% medium; post-2021 ">80% did not attend" is an inequality, not a
  rate). **Cambodia is a case-study mechanism** (one district, six schools, teacher-sold Rien Kuo). **Philippines
  incidence is blocked** and stays data-first.
5. **All seven experiments change a structural variable**, carry arms that map to rival mechanisms, and have a
  predeclared sign + numeric threshold. Provider mix and gate architecture are the two variables that loop 2–4
  identified as load-bearing.
6. **The relation layer is pending.** Design-intent grades are recorded (causal / plausibly-causal / correlational);
  when `09_relations` lands, each experiment inherits the scout's grade rather than being re-labelled.

## Disagreements preserved

**D1. BRAY vs PAGE/PATRINOS — which experiment comes first?**
BRAY: provider technology first, because both loop-4 OOS failures are provider-order failures and the programme is
provider-blind. PAGE: gate-architecture first, because it is the paper's central mechanism and the only experiment
that can explain the KOR fall, the HKG rise *and* the U1 ordering contradiction. PATRINOS: gate-architecture first on
identification value; JPN within-country is the cleanest design but a narrower claim. *Resolution:* gate-architecture
#1, provider technology #2; BRAY's point is recorded as a condition — if #1 passes while provider order stays wrong,
#2 becomes the immediate follow-up.

**D2. BRAY vs PATRINOS — KHM teacher-tutor: experiment or demonstration?**
BRAY: it is the Cambodian mechanism and deserves a cell. PATRINOS: with a six-school case it cannot identify anything
national; run it as a mechanism demonstration with a predeclared case-scope claim only. *Resolution:* included at
rank 5, labelled "mechanism demonstration (case scope)".

**D3. All — the 09_relations absence.**
The slate cannot yet map experiments to identified empirical relationships. All relation slots are PENDING; the
slate's ranking may change when the scout's grades land (a plausibly-causal relation for gate architecture would
strengthen #1; a purely correlational grade would demote it to description).

## Design contest — the top two

| | Gate-architecture gradient (E1) | Provider technology & fee block (E2) |
|---|---|---|
| Structural variable | where the binding gate sits (single terminal vs multiple transitions) | provider production (mass lecture vs 1:1 vs teacher-sold) |
| Predicted sign | terminal gate → rising stage gradient (HKG); multi-gate → falling (KOR) | exam-oriented mass lecture dominates senior (HKG); hagwon dominates spend (KOR) |
| Data on disk | KOR 2023 by level; HKG 2003 gradient; policy timelines from cards | KOR spend mix/fees; HKG provider/fee moments |
| Kill condition | any structure that cannot produce both gradients within ±5 pp | provider shares/gap thresholds missed |
| Type | identification (plausibly-causal) | identification/description |
| Cost | ~30–45 min | ~45–60 min |

**Resolution:** E1 first, E2 second; all seven in `SYNTHESIS_007.md`.
