# The full transition in the GPU engine, and the mortality counterfactual (23 November 2026)

## What this is, and what it is not
Dr. Menefee asked whether the whole arc can be shown in the GPU engine, and whether the fertility collapse
survives without the mortality decline. This record answers the second question with a calibrated
counterfactual, and reports honestly that the first is only partly achievable.

**This is a model extension, not the published model.** Two additions, both switchable and both labelled:
cohorts are placed on a configurable base instead of the published 1930-1999, and a child-mortality channel
is added, because the published model has no child mortality at all (every child survives). With the channel
switched off and the published cohort base, the engine still reproduces the published model bit for bit:
woman-level states differ by 0 and all four target series by 0.0 (`trans/test_port.py`, run in this record).
The GPU engine's marriage-market semantics remain the documented deviation from the published serial market.

## Method
Historical paths are un-data's `2026-11-23-transition` panel (child mortality per 100, income, urban share,
mean years of schooling, 1800-2024). Eight fit countries, 14 five-year cohorts, two arms, three coefficient
settings: 48 runs.

**The mortality channel, and why its size is calibrated rather than assumed.** A woman's desired number of
births is raised by the prevailing child mortality relative to the calibration era: desired births increase
by the coefficient times (child mortality minus 5 per 100). The coefficient is set from our own country-level
estimate, **0.0067 births per woman per point of child mortality per 100**, so a fall from the pre-antibiotic
42 per 100 to 3 per 100 is worth about 0.25 births. A ±50% band (0.00335 to 0.01005) is run, and a 4.5x
"power check" (0.03) is run to show what the test can detect.

**Constructed inputs (assumptions, not data).** Schooling before 1950 is built from mean years of schooling
by a normal-latent mapping onto the model's seven levels, because Barro-Lee starts in 1950. Income is
Maddison 1990-international logs rescaled to the published 2015-US$ log scale by their mean difference over
1950-2010 (offset -0.988). Both are labelled wherever they drive a conclusion.

**Scale actually simulated** (the largest run, cohorts 1930-1995): **10.08 million women, 353 million
woman-years, 48 runs of 210,000 women, 3.03 s wall time, 3.3 million women per second** on one RTX 2080 Ti.
The chain is: parameters in, batched life-course summaries out (`scripts/transition_gpu.py`).

## (1) Fertility

### The counterfactual: does the collapse survive without the mortality decline?
Yes, almost entirely. Cohorts 1930 to 1995, mean over the eight countries, births by age 49:

| arm | 1930 cohort | 1995 cohort | change |
|---|---|---|---|
| history (child mortality follows history) | 4.96 | 3.60 | **-1.36** |
| frozen (child mortality held at its pre-antibiotic level) | 5.01 | 3.70 | **-1.31** |

Levels are the mean over the eight countries of births by age 49; the 3.36-million-woman and
10.08-million-woman runs agree within 0.02, and the change is -1.357 against -1.312.

Freezing the mortality decline at its pre-antibiotic level removes **3.2% of the fall** (country range -1.8%
to +8.2%: Bangladesh +8.2%, Egypt +7.3%, Indonesia +4.8%, India +0.3%, Vietnam -1.8%). In other words: in this
model, with the mortality channel set to the observed country-level relationship, **the fertility collapse is
schooling-led, not mortality-led** — the mortality decline accounts for a few percent of it at most.
Falsifiers that could have killed this and did not: (a) the ±50% coefficient band moves the share removed
only from 0.9% to 4.7%, so the answer does not depend on the coefficient; (b) the 4.5x power check moves it to
only 10%, so even a wildly larger mortality channel would not flip the verdict; (c) the same answer at 3.36
and 10.08 million women, so it is not simulation noise. The counterfactual does raise the *level* of
fertility (5.01 against 4.96 at the 1930 cohort) — it just adds births roughly evenly and cannot stop a fall
that is driven by the schooling rise.

### The same test in the development-only scenario
Repeating the whole thing with the rival (development-only) specification gives a **larger** collapse —
cohort fertility 5.22 -> 2.08, a fall of 3.14 births against 1.35 in the individuation scenario — and freezing
child mortality at its pre-antibiotic level removes **2.0% of it** (against 3.2% in the individuation
scenario). So the answer to "was it mortality-led?" is the same under both specifications of the model: no, and
the development-only scenario is if anything more mortality-independent because its fertility response runs
through income and schooling alone. This also means the earlier A-versus-B tie in the dose record is not
reproduced here in levels: over the full arc the development-only engine falls further, closer to the observed
trajectories (figure).

**Figure** (`figures/transition_figure.png`): simulated period fertility for the eight countries, solid =
historical child mortality, dashed = frozen at its pre-antibiotic level, black dots = observed. The two line
styles lie on top of each other, which is the counterfactual result in one picture.

### The pre-antibiotic arc: only partly reachable
Run on cohorts 1890-1955 (reproductive years 1905-2004), the model **does not generate a transition at all**:
cohort fertility goes 4.01 (1890) -> 4.94 (1920) -> 4.64 (1955), a rise of 0.63 of a birth rather than a fall.
The highest cohort fertility anywhere in the committed runs is 5.20 (1890 cohort, frozen mortality, high
coefficient) and 5.42 in the 4.5x power check, against a historical national total fertility of about 5; at
the calibrated settings the 1890 cohort sits at 4.01. So the model **cannot stand in for the pre-antibiotic
equilibrium**: its collapse is produced by mass schooling in cohorts born after about 1930, and before that
it has no mechanism that produces the early high-fertility plateau. This is a structural limit of the
published model, not a data problem. It means the **simulated arc covers 1930 onward only**; the full
1800-onward arc is un-data's historical reconstruction (job 11), not this engine.

### Two things this result does not say
First, "schooling-led" here is a decomposition **of this model**, and the published model's core mechanism *is*
the schooling dose: it was calibrated to reproduce the decline through its schooling and income channels, so
a small calibrated mortality term could hardly overturn that structure. The result therefore shows what
carries the decline *inside the model*, not independent evidence about the world.
Second, it sits in real tension with the country-level result, where child survival is the most robust
correlate of fertility in the project. The honest statement is that **either the model mis-specifies what
carries the decline, or the country-level link is not causal — this is unresolved and needs micro data.**
The two cannot both be the whole story.

## (2) Massification
This is the clearest evidence in the job that the massification channel is what moves fertility. In the same
runs, holding child mortality fixed at its pre-antibiotic level while schooling, income and urbanisation
follow history leaves a fall of 1.31 births out of a total 1.36 — so the schooling-and-income channel carries
essentially the entire collapse, and the mortality channel carries at most a few percent. The caveat from the
dose record stands unchanged and is not rescued here: the *magnitudes* of the schooling channels are not
identified (their intervals are prior-wide), so this is a decomposition **within this model at its fitted
parameter values**, not an estimate of the true share. The direction of the massification channel is what is
being tested, and it survives every arm run here.

## Limits
The extension is labelled throughout: the cohort base, the pre-1950 schooling construction, and the income
rescaling are assumptions, not data. Eight countries only, all previously used to fit the model, so this is
not an out-of-sample exercise. The child-mortality channel is a single-coefficient hoarding term; real
replacement behaviour is richer. The GPU engine's market semantics differ from the published serial market
and are disclosed, not corrected. Pre-1950 lead-lag remains description, not identification. And the
pre-antibiotic corner is unreachable at the model's fitted settings, which is reported above as a negative
rather than patched.

## Files
`scripts/transition_gpu.py` (the driver: historical paths in, arms and coefficient settings out),
`scripts/analyse_transition.py` (the tables), `scripts/engine.py` and `scripts/kernel.cu` (the extended
engine: configurable cohort base, year base, and the child-mortality channel), `scripts/dosecore.py`,
`scripts/ref_numpy.py` and `scripts/test_port.py` (the unchanged-behaviour check), and `results/`
(`trans_collapse_big.json` is the 10.08-million-woman run, `trans_results.json` the 1890-1955 arc,
`trans_power.json` the 4.5x power check).
