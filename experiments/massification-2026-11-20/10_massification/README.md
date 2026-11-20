# 10_massification — the first-order phase

**Reorientation (user request, 20 Nov 2026).** The programme's first-order question is now
**massification / universalization of schooling across countries and sectors**, and the **push-pull dynamics**
between schooling and jobs/markets. Shadow education is demoted to secondary. The previous phase's close-out
(`../LOOP_CLOSEOUT.md`, `../08_council/brief_008`) remains valid **for shadow education** and is not re-fit here.

## Core questions

1. **Shape**: what trajectory does universalization take (logistic/Gompertz shape, ceiling, slope, midpoint), and
   is there a common shape with country-specific timing (scaling) or not?
2. **Push-pull**: does schooling follow jobs/markets (demand-led), do educated cohorts create jobs/growth
   (education-led), or both (complementary)? Where can cross-country/cohort data discriminate, and where are the
   rivals observationally equivalent?
3. **Scaling laws**: which relations are stable exponents (enrollment vs income, sector shares vs income, returns
   vs schooling, cohort size vs completion, urban share) and which are period/region regularities?
4. **Sectors**: how does the sectoral composition of employment (agri/industry/services, formal/informal) co-move
   with education expansion?
5. **Model**: what must a longitudinal cohort-flow model generate — rather than have supplied — to reproduce
   universalization timing and sectoral shift?

## Workstreams (disjoint write scopes)

| task | owner | path | deliverable |
|---|---|---|---|
| 34 | data-hunter | `data/` | jobs/markets panel, ILO/OECD report corpus, universalization series |
| 35 | lit-archivist | `lit/` | massification theory, push-pull, scaling-laws literature, targets |
| 36 | pattern-scout | `relations/` | universalization curves, scaling exponents, push-pull lead-lag tests |
| 37 | experiment-runner | `model/` | push-pull cohort-flow model + calibration + rival comparison |
| 38 | experiment-runner-2 | `model2/` | independent scaling estimation + rival-model recovery/identification |
| 39 | expert-council | `../08_council/brief_013/` | design review: success criteria, identification, ranked slate, stop rules |

## Sequence

theory+data (34/35) → scaling/push-pull empirics (36/38) → model+calibration (37). Council design review (39) runs in
parallel and **gates the model's success criteria before any fitting**: no calibration starts until brief 013 defines
what "reproducing universalization" means (series, countries, tolerance, holdout).

## Rules (binding)

- Predeclare every run; label **observed** vs **simulated**; never use imputed cells as observations.
- No target may be coded as a parameter; fit/holdout split declared before fitting (1980–2010 fit, 2011–2024 holdout
  where data permit).
- Do not re-fit or reopen the closed shadow-education claims; shadow work is secondary and cited only as prior.
- Scaling relations estimated in `relations/`/`model2/` are **checks or constraints** on the model, not supplied
  parameters unless declared.
- Push-pull must have a stated discriminating test and a recovery/forced-ID design; "both directions matter" is not
  a result unless the data can separate the channels or the equivalence is demonstrated.
- Results only under `experiments/massification-2026-11-20/10_massification/` on the branch; never `main`/`src`/`public`.
- Bridge: append-only, per-agent party slugs via `../DeepSeek/bridge-agent.sh` (Lead = deepseek-research).
