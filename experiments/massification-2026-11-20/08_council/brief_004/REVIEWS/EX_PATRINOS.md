> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# REVIEW — PATRINOS composite (drawing on Psacharopoulos & Patrinos 2018; Becker 1964; steel-man seat) — brief_004

**G. GROUNDING.** Literature basis: identification is a property of the contrast; empirical education economics
lives on held-out variation and measured returns, not on calibrated fits. **COUNCIL EXTRAPOLATION:** the assessment
below is the composite's.

**M. MODEL RENDERING.** M1 the moment vector m must contain moments with *different predicted signs* under the
candidate worlds, not moments all candidates were fitted to; M2 a fit/holdout split declared before fitting (period
and/or country); M3 a recovery test with truth inside and outside the set; M4 an identification-gain metric (confusion
matrix, forced-ID rate); M5 the claim = "m separates the worlds out of sample"; M6 falsifier: same fit, different
holdout predictions. C1 is exactly the M6 diagnosis: six aggregate moments are common to both worlds, so their
distances are tied (0.012–0.023), and an outside truth is confidently mis-assigned.

**A. VERDICTS.** (a) The loop is **sound in intent and wrong in order**. In `RESEARCH_LOOP.md` the target set (B)
does not yet declare which moments are *checks*; falsification (D) comes after calibration (C). That ordering makes
identification a post-hoc judgment. Fix: each row of `TARGETS_*.csv` must be labelled fit or check *before* the
calibration run, with a predicted sign for each candidate world. (b) C1 says more simulation of the same two worlds
cannot separate them. Iteration 2 needs moments that are new *to the candidates*: (i) formal-access response to a
graduate-supply shock (regional campus expansion, PH free-tuition 2018, CHED series — a real-data moment, not
simulated); (ii) stage-specific tutoring take-up (BRAY's card); (iii) provider composition; (iv) wage-premium
dynamics against attainment; (v) informality transition rates. At least two of these must be real-data and excluded
from the fit. (c) The recovery design must include a truth outside the set every round; C1's G4 forced-ID is the
regression test. (d) Publishability: a calibration that fits in-sample and misses out-of-sample is a model
description, not evidence; only out-of-sample separation plus a natural experiment supports an empirical claim.

**B. WHAT IS IMPOSED.** C2's supplied attainment means the attainment path is an input; if iteration 2 calibrates
attainment to targets, that is fitting an input. The two-way test must be symmetric: freeze schooling (does the job
path still rise?) and freeze wages/jobs (does attainment still rise?). If either side needs its schedule, name it as
supplied and remove it from the "generated" language.

**C. ESTIMAND.** Per stage: cards = measurement with source/date/definition; targets = fit/check labels and predicted
signs by world; calibration = residual table; falsification = holdout error + confusion matrix. Units and denominators
of every moment must be stated (completion vs attainment, share of cohort vs enrolled).

**D. TYPE.** Simulated moments cannot identify a model. If a target moment has no real-data counterpart, label it
"simulation-only check" and exclude it from identification claims.

**E. STRONGEST DEFENSIBLE SENTENCE.** "Iteration 2 adds real-data moments with predeclared rival-specific predictions
and an overnight holdout; the calibration is reported with residuals, and the identification claim is the confusion
matrix, not the fit."

**F. NEGATIVE.** The programme has already produced a forced identification (G4). Add it as a permanent alarm: if a
new truth outside the set is again confidently assigned, the moment set is not doing identification work.

**G2. STEEL-MAN.** The loop's best defence: real country cards with provider and access moments genuinely are new
information, and a holdout (2011–2024 for PH) is available. That is enough to make identification plausible, not
guaranteed.

**H. ALTERNATIVE.** The worlds may be observationally equivalent on *any* available national aggregate; then the
honest product is an equivalence result, not a winner. That is publishable (and important), but it must be stated.

**I. WHAT WOULD CHANGE MY MIND.** A holdout where the surplus world's formal-access response is closer to observed
than the rival's by a predeclared margin, with the reverse not true; or a natural experiment (free tuition, campus
expansion) where the rival predicts the opposite sign.
