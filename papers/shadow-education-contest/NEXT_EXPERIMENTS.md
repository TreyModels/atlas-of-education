# Proposed next experiments (from Gemini, bridge task `ce886de8`, 25 Nov 2026 05:23Z)

**Status: PROPOSALS ONLY — not run, not pre-registered, not committed results.** Recorded because the bridge
handoff asked for them to be saved here. None of the four has been executed in this repository.

## Exp 7 — Paper B combined win-win arms (highest ROI; ~15 s on M1)

Add two explicit combined arms to `code/run_hk_korea_comparative.py` (30 matched seeds, HK and KR):

- `CF4a`: wage compression (ΔV −50%) + effort cap (`contest_max_e` −50%).
- `CF4b`: wage compression (ΔV −50%) + large seat expansion (HK `S = 0.50`, KR `S12 = 0.40`).

Falsifier: `CF4a`/`CF4b` land in the Win-Win Zone (total spend index < 80 **and** Q5 elite share below baseline)
in both jurisdictions.

**Blocker:** this requires the contest-gate engine patch. The supplied runner does not run against the committed
engine (see `RUNNER_STATUS.md`); the patched `core.py`/`tutoring.py` have not been supplied.

## Exp 2 — LSMS-ISA household tutoring check (empirical; local CPU; needs data access)

Countries: Malawi, Ethiopia, Uganda, Tanzania. Requires the operator to click through a free World Bank
microdata download of the education-expenditure modules
(`https://microdata.worldbank.org/index.php/catalog/lsms`). Test: household out-of-pocket tutoring / extra-class /
exam-fee spending in the national exam-transition grade vs one grade below, by consumption quintile and within-
grade school-quality stratum — the two micro-moments claimed in Exp 4 to restore full Jacobian rank.

**Blocker:** data access (operator click-through) and, ideally, a pre-registration before running.

## Exp 6 — wild-cluster / country-block permutation null (Paper #1 referee armour)

`B = 2,000` Rademacher wild-cluster bootstrap and country-block permutations over the E1/Q3 panel matrices.
Falsifier: Paper #1's `0/0/0/32` classification and `87%` minority-effect leakage survive finite-sample
permutation p-values.

**Caveat:** the committed record already says the E1 panel inputs are not committed and the result is
procedure-dependent; a pre-registration and committed inputs are needed before this is citable.

## Exp 8 — Korea elementary childcare/enrichment floor (optional Paper B robustness)

Add a non-exam elementary enrichment/childcare floor in Grades 1–6 for South Korea; test whether the model
reproduces the real-world age profile (~86% elementary > ~75% middle > ~67% high school) while keeping the
Grade-12 CSAT counterfactual ordering invariant.

**Blocker:** same engine-patch requirement as Exp 7.

## No paid GPU needed

Per the proposer, all four are CPU-light on the M1. Exp 2 and Exp 6 also need data access / committed inputs.
