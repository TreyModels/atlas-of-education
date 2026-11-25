# G2-A IDENTIFIABILITY — V540-FREEZE calibration map (frozen spec)

**Status: LOCAL IDENTIFICATION EXERCISE — result accepted with a hard instability caveat. Not global identification.**
Artefact: `results/audit/G2A_IDENTIFIABILITY_V540FREEZE.json` (box run, sha256
`ce45861bcb2ccaa5fea83b112ccd3879419d02ac30409cc5c3227fe1120b13d5`), runner `/tmp/g2a/identify.py` (subprocess-based,
no ProcessPool completion phase), declared venv py3.10.8/numpy 2.2.6, seed 0.

## Result

Parameters θ = (contest_price_mult, contest_alpha_mult, G9-track-prize mult, y_median_mult); moments = (KR
participation, KR Q5−Q1 gap, KR Q5/Q1 spend ratio, HK Grade-9 participation). Forward finite differences.

| start | rank | singular values | null dim |
|---|---|---|---|
| (1.0, 1.0, 1.0, 1.0) | **4/4** | 60.015, 32.125, 7.770, **0.683** | 0 |
| (1.5, 0.8, 1.5, 0.95) | **4/4** | 36.451, 14.423, 4.407, **0.091** | 0 |

## Hard caveats (binding for Gate 2)

1. **One-seed forward-difference Jacobians are unstable across starting points**: max |ΔJ| = **26.53**, relative
   **0.52**; the smallest singular value moves 0.683 → 0.091. Rank 4/4 at these two points therefore **does not
   settle global identification**, and local full rank is not evidence of well-conditioned estimation.
2. **Gate-2 must use multi-seed Jacobians** (≥5 matched seeds per finite-difference column), declared perturbation
   sizes (5 %/3 %/5 %/4 % as registered), and ≥3 starting points; report rank/SV/null space, **not condition numbers
   as identification evidence** (ABC lesson: cond 7.03 coexisted with rank 4/5 and a 2-dim null).
3. No prior-information inference. No condition-number inference. Any Gate-2 estimation must declare the reduced
   system if rank is inadequate.

## Consequence

The frozen spec's 4-moment calibration map is locally full-rank at the two tested points, but this is **not**
sufficient for the G2-B stop gate. The registered Gate-2 identifiability analysis (multi-seed, multi-start) must be
run before joint estimation; if it fails, the system is reduced and re-registered.
