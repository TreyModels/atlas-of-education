# MASSENG v6 Phase 1: conserved cohorts and joint admissions

**Status: illustrative mechanics; not calibrated, causally identified, or empirically validated.** This branch preserves the archived v3/v5 engine and adds a separately testable accounting kernel. It does not yet implement the full country-year v6 simulation or test H1–H3 against observations.

## Fact check

The motivating coexistence of unused accessible public places and intense gate preparation remains a hypothesis requiring independently sourced school occupancy, household cost, and tutoring data. No new empirical observations are introduced here. The handoff's reported v5 Philippine credential+deferral overprediction is a baseline diagnostic, not evidence for the surplus motor.

## Two rivals

The surplus-motor account predicts that material eligibility, household costs, and employer screening alter pipeline persistence. A measured World Society diffusion rival predicts reform timing from international script exposure and peer adoption. These mechanisms may coexist; this software milestone does not adjudicate between them.

## The separating observation

Preregistered empirical work should compare dated reform responses to material triggers against exposure-weighted peer adoption, then test rerouting among means-capable households and tutoring distributions around measured high-stakes gates. Phase 1 instead establishes the accounting needed to prevent duplicate applicants and inaccessible seats from manufacturing support for either account.

## Small, or recoverable

This milestone introduces no fitted behavioural parameters. Synthetic known-answer cases test identities, not parameter recovery. In the joint-choice case, 5 unique qualified people generate 4 admissions, not one admission per preferred sector. In the cost-exclusion case, Q=2, L=2, E=1, and R=1; latent demand therefore remains visible when effective demand is financially constrained.

## A benchmark

The naive comparator is independent sector-by-sector admission, which can count one person more than once. The joint allocator admits each applicant at most once and respects continuing reservations. The geographic case records 3 physically empty seats but 0 accessible empty seats for the listed applicant, preventing national vacancy totals from being misread as local access.

## Owned

- `CohortKey`: locates probability mass by cohort, decile, region, stage, grade, sector, education status, and orthogonal work status.
- `EntryFunnel`: enforces Q ≥ L ≥ E ≥ R and leaves conditional factors undefined at zero denominators.
- `StockLedger`: reconciles starting stock, external entries, reentries, deaths, external exits, and ending stock.
- `Market`: subtracts occupied continuing places from physical capacity before new admissions.
- `Applicant`: stores one person's ranked accessible choices; multiple applications are not multiple people.
- `clear_admissions`: deterministically assigns each effective applicant to at most one market and reports unmet demand and empty accessible seats.

## Reproduce

From this directory, with pytest available:

```bash
PYTHONPATH=. python -m pytest -q tests
PYTHONPATH=. python experiments/run_phase1.py
python make_readme.py
```

Result files contain exact input/output values and code hashes. The archived v3/v5 suite must also pass before country integration. Subsequent phases require measured denominators, real holdouts, structural recovery, and comparisons with matched naive cohort-progression benchmarks.
