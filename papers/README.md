# Paper drafts — 25 Nov 2026 findings

**Status: DRAFTS.** These are working drafts assembled from four pre-registered workstreams completed on
25 Nov 2026. Every number is traceable to a committed record; the evidence map is below. No causal language
is used anywhere. Simulation work is labelled **SIMULATION ONLY**. Items that could not be estimated are
reported **NOT-ESTIMABLE**, never proxied.

| draft | topic | evidence branch (remote SHA) | record |
|---|---|---|---|
| `DRAFT_1_fee_abolition_ri_gender.md` | Fee abolition, primary GER, Fisher randomization inference, sex split | `research/e8-fisher-ri-2026-11-25` @ `fb8b67e`; `research/gender-split-e6e8-2026-11-25` @ `b4eb680` | `research/records/2026-11-25-e8-fisher-ri/`, `research/records/2026-11-25-gender-split-e6e8/` |
| `DRAFT_2_equifinality_simulation.md` | Equifinality + phase surface in a toy education system (SIMULATION ONLY) | `research/equifinality-phase-2026-11-25` @ `ab415f2` | `research/records/2026-11-25-equifinality-phase/` |
| `DRAFT_3_silent_failures.md` | Forensic methods: five silent failures + receipt-drift audit | `research/meta-science-silent-failures-2026-11-25` @ `de3821e` | `research/records/2026-11-25-meta-science/` |

## Upstream bases

- E8 event-study record and cited estimator: `research/e6e8-sequencing-2026-11-25` @ `bd782be`
  (`e8_fee_event_study.py`).
- Verified fee dates: `data/fee_dates.csv` @ `bd782be`, sha256 `1a08d465…`.
- Bulge-arrival data gate (`L_primary` 0/8, `t*` NOT-ESTIMABLE): `research/bulge-arrival-2026-11-25` @ `1b91a71`.

## Verification status (25 Nov 2026)

- E8 lane: QA PASS (confirmatory + documentation fix `3535e49` + exploratory probes).
- Gender lane: QA PASS (confirmatory + exploratory follow-up).
- Meta-science lane: QA PASS (confirmatory + receipt-drift audit).
- Phase lane: run and analysis complete; Lead independently recomputed seed means (max diff 3.3e-16), pair
  counts (176 within-gate / 4,132 cross / 4,308 total of 319,600), and regenerated the 1,000-permutation null
  (means, SDs and p-values bit-identical). QA re-verification in progress at draft time.

## How to cite in this draft

Cite commits, not branches (branches move). Record SHAs above are the evidence pins. Do not quote a
`NOT-ESTIMABLE` result as a null; do not quote `SIMULATION` output as empirical.
