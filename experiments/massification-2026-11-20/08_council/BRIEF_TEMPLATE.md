# RESULTS BRIEF template — 08_council

Fill this in and send `lead` → `expert-council` with the path to the filled file. Any path is fine; if you send the
fields inline in a message instead, the Council transcribes them into `08_council/brief_NNN/BRIEF.md` and flags it.
**A brief missing fields 1, 2 or 3 is returned BLOCKED in the same turn.**

---

## 0. ID and ask

- **brief id (leave blank; council assigns):**
- **sent by / date:**
- **purpose (one line):**
- **what this informs** (paper section, decision, go/no-go):
- **provisional or final?**
- **follow-up cycle expected?** yes / no

## 1. Artifacts

| artifact | path | sha256 | commit | command | seed(s) | N | runtime | status |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | completed / partial / failed |

If code or output is absent, write `ABSENT` — the Council will treat those numbers as *reported, unverified* and
capped at `UNABLE TO ASSESS`.

## 2. Claims table

| ID | claim (one sentence) | type | unit | estimand / quantity (denominator) | key numbers ± uncertainty, N | where (path:line) | set by hand | falsifier |
|---|---|---|---|---|---|---|---|---|
| C1 | | description / simulation / mechanism / causal / forecast / theoretical | | | | | | |

Rules: one claim per row; a claim with two mechanisms is two rows; every number carries its artifact and a
`path:line`; "set by hand" lists the hand-set values the claim depends on (floor level, vacancy count, elasticity,
bar height, discount rate, priors).

## 3. Rivals the result is claimed to have beaten

- **rival 1** — name / literature; how it was made comparable (same population, shock, information, outcome, and
  elasticity range):
- **rival 2** — same:
- **how a rival could win** — what result would let the rival win, and was that cell run?

## 4. Questions to the Council (≤6, numbered)

1.
2.
3.

## 5. Known limitations and failures

- incomplete/failed runs, with paths:
- assumptions with no source (assumed / placeholder / prior):
- data that could not be obtained:
- the one result you are least sure of:

## 6. Out of scope / do not read

## 7. Budget

- deadline:
- Council output wanted: reviews + deliberation + synthesis (default) or synthesis only:
- max words in the reply:

---

**Minimum viable brief:** artifacts + hashes, claims table, one rival, three questions.
**Every experiment the Council proposes back will have arms, estimand, threshold and cost — the Brief may use the
same columns to save time.**
