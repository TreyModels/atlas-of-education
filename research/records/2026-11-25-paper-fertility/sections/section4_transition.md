# Paper F (Fertility) — Section: the transition engine, the individuation (dose) model, and the tolerance ladder

**Author: gpu-dose. Provenance: `research/transition-gpu-2026-11-23` @ `f9f2f18`; `research/dose-gpu-2026-11-23`
@ `774085c`; `research/dose-tolerance-2026-11-23` @ `baadfe6`; the transition record `research/transition-2026-11-23`
@ `b13fde8` supplies the historical paths and the mortality-leads-fertility estimate. All files below are in
those records' `results/` directories unless stated.**

## 1. The question this section answers

The demographic transition has a standard ordering in demography: mortality falls first, the population grows,
and fertility falls later. What the ordering does not establish is what **drives** the fertility fall. The two
candidates that matter for this project are the quantity-quality mechanism (schooling raises the cost of
children) and a mortality-led mechanism (parents insure against child deaths by having more births). This
section reports four results: a calibrated counterfactual that shuts off the mortality decline; a model of
individuation (the "dose" model) in which schooling and marriage-market position govern fertility; an
out-of-sample comparison of that model against a development-only rival; and a tolerance ladder showing that the
wide parameter intervals are an identification limit rather than a statistical artefact.

The engine is a GPU port of the project's published individual-level model. The port is bit-exact against the
CPU reference with its new channels switched off — woman-level states differ by zero and all four target series
by 0.0 (`trans/test_port.py`, `results/` of the transition record) — which is the precondition for reading the
counterfactual at all. The two additions for this exercise, both switchable and both labelled as extensions
rather than parts of the published model, are a configurable cohort base and a child-mortality channel.

## 2. Does the fertility collapse survive without the mortality decline?

The counterfactual holds child mortality at its pre-antibiotic level while schooling and income follow history,
for cohorts 1930 to 1995 across eight fit countries, and compares births by age 49:

| arm | 1930 cohort | 1995 cohort | change |
|---|---|---|---|
| history (child mortality follows history) | 4.96 | 3.60 | **-1.36** |
| frozen (pre-antibiotic child mortality) | 5.01 | 3.70 | **-1.31** |

Freezing the mortality decline removes **3.2 per cent of the fall in the calibrated model** (a model-internal counterfactual, not an empirical estimate of mortality's causal role) (country range -1.8 to +8.2 per cent:
Bangladesh +8.2, Egypt +7.3, Indonesia +4.8, India +0.3, Vietnam -1.8). The counterfactual does raise the
*level* of fertility — 5.01 against 4.96 in the 1930 cohort — but it adds births roughly evenly and cannot stop
a fall that the schooling rise drives. Three falsifiers were run and did not flip the verdict: a ±50 per cent
band on the calibrated mortality coefficient moves the share removed only from **0.9 to 4.7 per cent**; a 4.5×
power check (a coefficient more than four times larger than the observed relationship) moves it to only **10 per
cent**; and the 3.36-million-woman and 10.08-million-woman runs agree within 0.02 births, so the result is not
simulation noise. **In this model the fertility collapse is schooling-led, not mortality-led.**

The rival specification answers the same way. With development-only fertility behaviour the collapse is larger —
cohort fertility 5.22 to 2.08, a fall of 3.14 births against 1.35 — and freezing child mortality removes **2.0
per cent** of it. So the answer to "was it mortality-led?" is no under both specifications; the development-only
engine simply falls further and closer to the observed trajectories, which is why the levels cannot be used to
choose between them.

**The pre-antibiotic arc is only partly reachable, and this is an honest limit of the extension.** Run on
cohorts 1890-1955, the model does not generate a transition at all: cohort fertility goes 4.01 (1890) to 4.94
(1920) to 4.64 (1955), a rise of 0.63 of a birth rather than a fall. The highest cohort fertility anywhere in
the committed runs is **5.20** (1890 cohort, frozen mortality, high coefficient) and **5.42** in the 4.5× power
check, against a historical national total fertility of about 5. The model's collapse is produced by mass
schooling in cohorts born after about 1930, so the engine cannot stand in for the pre-antibiotic equilibrium;
what it can do is show what the post-1930 cohorts imply.

**On the empirical ordering, the record we build on reports that mortality leads fertility by about twelve
years** (`research/transition-2026-11-23` @ `b13fde8`, transition record). The counterfactual above does not
contradict that ordering: mortality does fall first. It shows that the *level* channel from mortality to births
is small relative to the schooling channel, which is a statement about magnitudes, not about sequence.

## 3. The individuation model: what schooling and marriage-market position do to fertility

The dose model treats a woman's schooling as a sequence of doses and asks which channels of the theory survive
rejection-based Bayesian estimation on 31 parameters against the observables. The five theory parameters are
reported with their 5th-95th percentile intervals (`research/dose-gpu-2026-11-23` @ `774085c`,
`results/rej_fitA.json`; the same numbers are tabulated in `research/dose-tolerance-2026-11-23` @ `baadfe6`,
`results/ladder.json`, fields `params.th_k.q50`, `params.th_f.q50`, `params.kappa.q50`, `params.gam.q50`,
`params.lam_s.q50` with `q05`/`q95`):

| channel | 5th | median | 95th | prior |
|---|---|---|---|---|
| kin-support loss per full dose | 0.34 | **2.80** | 4.74 | 0-5 |
| downward money flow to parents | 0.30 | **2.62** | 4.77 | 0-5 |
| cohort deepening (sibling configuration) | 0.15 | **1.58** | 2.85 | 0-3 |
| career delay at high schooling | 1.10 | **5.32** | 7.71 | 0-8 |
| pickiness (partner standards) | 0.25 | **2.41** | 4.70 | 0-5 |

Every channel points in the theory's direction and the intervals exclude zero at the 5th percentile, with 1,044
of 5,000 draws accepted (20.9 per cent) in the primary fit and a replicate fit giving a kin-support median of
2.73 (0.37-4.78), so the rank ordering is stable. **But the intervals are wide**: at the primary tolerance they cover 88 to 100 per cent of the prior range
(and 71 to 101 per cent across the three rungs of the ladder), and that width is the next section's subject.

## 4. Out of sample: individuation against development-only

The two arms are fitted on the same windows and compared on held-out country histories
(`results/analysis_holdout.json`, fields `holdout.mean_A`, `holdout.mean_B`, `holdout.diff_mean`,
`holdout.diff_ci`, `holdout.A_better`): the individuation arm's held-out distance is **24.43** against **21.10**
for the development-only arm, a difference of **+3.32 with a 95 per cent interval of [-3.76, +11.14]**, and the
individuation arm is closer in 3 of 6 held-out countries. Repeating the exercise with populations fitted by the
GPU engine rather than the CPU engine gives 25.48 against 21.68, a difference of +3.80 [-2.60, +11.96], also
3 of 6 (`results/analysis_holdout_gpuengine.json`). **The out-of-sample comparison does not separate the two
arms**: the interval spans zero, the sign favours development-only, and the country count is three of six. Any
claim that the individuation channels improve prediction would not survive this test.

The quantum-tempo decomposition makes the same point about model dependence
(`results/analysis_decomp.json`, fields `decomposition.A_fit.quantum_mean`, `.tempo_mean`,
`decomposition.A_holdout.*`): in-sample the model attributes a quantum of **2.09** and a tempo of **-0.34** to
the transition, while out of sample the same decomposition gives **2.55** and **-0.42**. The split between how
many children and when is not stable across the fit and the holdout, so quantum-versus-tempo statements from
this model should be read as model-dependent.

## 5. The tolerance ladder: the wide intervals are an identification limit

Because the earlier intervals were prior-wide, the natural objection is that the tolerance in the ABC fit — not
the data — set them. The ladder varies the tolerance from the 20th to the 10th to the 5th percentile of the
prior-predictive distance distribution, with equal-weight rejection sampling only
(`research/dose-tolerance-2026-11-23` @ `baadfe6`, `results/ladder.json`, fields `drawn`, `accepted`,
`acceptance`, `params.<name>.spread`):

| tolerance | drawn | accepted | acceptance | kin (th_k) | downward flow (th_f) | cohort (kappa) | career (gam) | pickiness (lam_s) |
|---|---|---|---|---|---|---|---|---|
| 20th pct (eps 21.5) | 5,000 | 1,044 | 20.9% | 0.96 | 1.00 | 0.98 | 0.88 | 0.98 |
| 10th pct (eps 18.33) | 10,000 | 1,012 | 10.1% | 0.98 | 1.00 | 0.94 | 0.71 | 0.97 |
| 5th pct (eps 16.59) | 12,000 | 660 | 5.5% | 0.96 | 1.01 | 0.87 | 0.76 | 1.00 |

Spread columns are `params.<name>.spread` from `ladder.json`, in the order of the ladder file (th_k, th_f, kappa, gam, lam_s), and the labels are the file's own `pretty` names.
"Spread" is the width of the 90 per cent interval relative to the prior width. Tightening the tolerance from the
20th to the 5th percentile leaves **four of the five** spreads between 0.87 and 1.01, essentially unchanged; the
one that moves is career delay, from 0.88 to 0.71-0.76, a slight tightening that does not bring the posterior near
the data. The point medians are similarly stable for kin support, downward flow and pickiness (2.80/2.82/2.82;
2.62/2.63/2.74; 2.41/2.47/2.61) but drift for cohort deepening (1.58/1.58/1.31) and career delay
(5.32/6.05/6.35), which is a further reason to treat those two channels cautiously. In the rival arm the tight tolerance accepts only **32 of 4,000 draws (0.8 per cent)**, at which point the
posterior cannot be interpreted. The conclusion is that the wide dose intervals reflect **a genuine
identification limit of this design**, not a loose tolerance, and that reporting them as though a larger
simulation would tighten them would be wrong.

## 6. Prior art for this section [DOIs Crossref-checked 24 Nov 2026; status given]

| work | DOI | Crossref status | relation |
|---|---|---|---|
| Becker & Lewis (1973), On the interaction between the quantity and quality of children, *JPE* | 10.1086/260166 | verified | the quantity-quality mechanism the dose model formalises |
| Bongaarts (1978), A framework for analyzing the proximate determinants of fertility, *PDR* | 10.2307/1972149 | verified | the decomposition logic behind quantum/tempo |
| Easterlin (1975), An economic framework for fertility analysis, *Studies in Family Planning* | 10.2307/1964934 | verified | the relative-income/cost framing |
| Becker & Barro (1988), A reformulation of the economic theory of fertility | 10.3386/w1793 | verified (working paper) | fertility as an investment in children |
| Notestein (1945), Population: the long view | not returned by Crossref in-session | **unverified** | the classic transition ordering |
| Davis (1963), The theory of change and response in modern demographic history | not returned in-session | **unverified** | change-and-response alternative to transition theory |
| Caldwell (1976), Toward a restatement of demographic transition theory | not returned in-session | **unverified** | intergenerational wealth-flow theory |
| Cleland & Wilson (1987), Demand theories of the fertility transition | not returned in-session | **unverified** | the demand-side critique |
| Galor & Weil (2000), Population, technology, and growth | not returned in-session | **unverified** | unified growth theory |
| Doepke (2004), Accounting for fertility decline during the transition to growth | not returned in-session (SSRN version resolves) | **unverified** | quantity-quality in a growth model |
| Guinnane (2011), The historical fertility transition: a survey | not returned in-session | **unverified** | the historical record |
| Coale & Watkins (1986), *The Decline of Fertility in Europe* | not returned in-session | **unverified** | the European fertility project's dating |
| Lesthaeghe (1983), The second demographic transition | not returned in-session | **unverified** | the post-transitional regime |

**What is replicated, corrected and new.** The transition ordering (mortality first) is replicated from the
prior record and is not new. The mortality **counterfactual** is new to this project and, as far as this
section's literature search found, no antecedent reports the share of a schooling-led fertility collapse that
survives a mortality freeze in a calibrated individual-level model; we do not claim it is the first such test.
The dose model's five channels are this project's construction; the quantity-quality mechanism they formalise is
Becker-Lewis's. The out-of-sample comparison is a correction of any impression that the individuation model
predicts better: it does not. The tolerance ladder is a correction of the earlier inference — the intervals are
an identification limit. No claim of precedence is made, and the historical-transition literature above is
cited because these results have to be read against it, not replaced by it.
