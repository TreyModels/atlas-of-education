# TOY DESIGN CHECK — shadow gating module (SYNTHETIC / TOY)

**LABEL: SYNTHETIC/TOY.** This is not a v1.3 run. It evaluates the frozen demand equation on *declared illustrative gate states*, not on a v1.2 simulation, and it is evidence about nothing in the world. Pre-declared as a design check only (`PRE_DECLARATIONS.md` §12).

Pre-declaration sha256 verified at run time: `cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2`

Seed `20261120`; zero random draws (the toy is deterministic arithmetic).

## 1. What this can and cannot test

| | |
|---|---|
| Scored here | c1, c2, c3, c5 (internal properties of the equation) |
| **Not** testable here | **c4** (needs the v1.2 run's gate state and cohort exposure over time) and **c6** (needs the frozen v1.2 panel) |
| Not a result | every number below is a worked example of the arithmetic |

## 2. Participation by gate (illustrative states)

| country type | D(g0 pre) | D(g1) | D(g2) | D(g3) | D(g4 job) | D* cohort | exposure sum |
|---|---|---|---|---|---|---|---|
| SYN_HKG_LIKE | 0.0081 | 0.2785 | 0.8210 | 0.9297 | 0.7733 | 0.7414 | 0.94 |
| SYN_PHL_LIKE | 0.0078 | 0.2637 | 0.6064 | 0.8391 | 0.7833 | 0.3753 | 0.75 |
| SYN_KHM_LIKE | 0.0079 | 0.2842 | 0.5926 | 0.8761 | 0.7991 | 0.1741 | 0.43 |

`D*` is the declared cohort-incidence statistic, `sum_g nu_g D_g` over g1–g3 only (out-of-school youth count as non-participants). `g4` is reported separately and is **not** part of `D*`.

## 3. Checks

| check | verdict | components |
|---|---|---|
| c1 gate pressure | **PASS** | sign non-negative in all 12 cells: True; R-doubling at g2 raises D by SYN_HKG_LIKE +0.127, SYN_PHL_LIKE +0.248, SYN_KHM_LIKE +0.255 (threshold +0.10) |
| c2 expected returns | **PASS** | +25% on phi at g2 raises D by SYN_HKG_LIKE +0.026, SYN_PHL_LIKE +0.040, SYN_KHM_LIKE +0.037 (threshold +0.02) |
| c3 near-zero pre-gate | **PASS** | max D(g0) = 0.00806 (<= 0.025); D(g0)/D(g1) = SYN_HKG_LIKE 0.029, SYN_PHL_LIKE 0.029, SYN_KHM_LIKE 0.028 (<= 0.20) |
| c5 identity | **PASS** | p,D in [0,1]; pi1 >= pi0; spend >= 0; D* <= exposure |

## 4. Worked example only — **not** a c4 result

Per §12 of the pre-declaration, the ordering arithmetic is shown for illustration and **must not** be read as a PASS on c4. c4 requires the v1.2 gate state and the time path of exposure; this toy has neither.

| country type | D(g2) | declared band c4a | D* | ordering gap c4b |
|---|---|---|---|---|
| SYN_HKG_LIKE | 0.8210 | [0.75, 0.95] (HKG only) | 0.7414 | 0.3661 |
| SYN_PHL_LIKE | 0.6064 | n/a (band is HKG-specific) | 0.3753 | 0.2011 |
| SYN_KHM_LIKE | 0.5926 | n/a (band is HKG-specific) | 0.1741 |  |

## 5. What this toy is worth

It confirms only that the frozen equation, implemented as written, has the declared internal properties: demand is increasing in gate pressure and in the credential return, it is near zero before the first gate, and the accounting identities hold. It says nothing about v1.2, nothing about c4 or c6, and nothing about any country. If the scored v1.3 run disagrees with this toy, the v1.3 run is the result and this file is the error.

