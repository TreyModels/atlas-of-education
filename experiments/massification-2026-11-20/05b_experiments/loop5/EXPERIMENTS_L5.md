# EXPERIMENTS — Loop 5: E1 gate-architecture gradient, E1b KOR no-fit benchmark, E4 income gradient

**New code:** `loop5/code/e1.py` (NEW). Structural variable = binding-gate stakes vector; frozen
structural configs from loop-4 uncalibrated KOR/HK; **no take-up fitting in E1**. E1b fits fee
multipliers only to Korean fee moments. E4 uses declared income bands. Predeclaration:
`PRE_DECLARATIONS_L5.md`. All numbers stylized model output; only observed cells compared; no imputed
cell used. **Relation slots PENDING** (`09_relations/` slot tables not consulted). **0 failed cells.**
Gate dates from `02_lit/COUNTRY_CARDS`: KOR CSAT terminal (1994 date **ASSUMED**), high-school
equalisation; HKG single terminal HKDSE first cohort **2012** (card says dates not independently
verified; pre-DSE HKCSE+HKALE).

## E1 — gate-architecture gradient (the Council's #1 identification test)

Frozen structural params (no demand-intercept calibration, no take-up fitting); arms differ only in the
binding-gate stakes vector: terminal_only `[0.30,0.50,1.50]`, gate_each_transition `[1.20,0.90,0.60]`,
continuous `[0.80,0.80,0.80]`. Policy-dated assignment: **KOR = gate_each_transition** (CSAT +
equalisation + continuous records), **HKG = terminal_only** (single HKDSE/JUPAS).

| country | arm | stage1 | stage2 | stage3 |
|---|---|---|---|---|
| KOR-like | terminal_only | 13.2 | 18.2 | 44.2 |
| KOR-like | **gate_each_transition** (policy) | **27.3** | **25.0** | **24.4** |
| KOR-like | continuous | 20.1 | 23.1 | 28.3 |
| HK-like | **terminal_only** (policy) | **14.4** | **19.7** | **46.7** |
| HK-like | gate_each_transition | 29.2 | 26.8 | 26.2 |
| HK-like | continuous | 21.7 | 24.9 | 30.3 |

**Six policy-dated rates vs targets:** KOR model 27.3/25.0/24.4 vs **86.0/75.4/66.4** (misses −58.7/−50.4/−42.0);
HKG model 14.4/19.7/46.7 vs **35.1/46.6/70.3** (misses −20.7/−26.9/−23.6). **E1 verdict: FAIL** — all six
outside ±5 pp. The *shape* is right in both countries (KOR gate-each-transition falls 27.3→24.4; HKG
terminal-only rises 14.4→46.7 vs the correct monotone direction), but with frozen structural parameters
and no take-up fitting the levels are 20–59 pp low everywhere. Per the predeclaration, **the
gate-position story is dropped, not re-fitted**. The shape-only observation is a diagnostic, not a claim.

## E1b — KOR no-fit benchmark (single-country rescue)

Frozen structural params; only three stage fee multipliers fitted to the official by-level fee moments
(11.5/14.9/18.4% of GDP pc): fitted multipliers 0.852/1.104/1.363; model fees reproduce the fitted
targets exactly; overall checks per-participant **13.5% vs 13.8% observed**, per-student 14.2% vs 10.8%.
Participation NOT fitted.

| stage | target | model | miss |
|---|---|---|---|
| elementary | 86.0 | 27.8 | −58.2 |
| middle | 75.4 | 24.6 | −50.8 |
| high | 66.4 | 23.3 | −43.1 |

**E1b verdict: FAIL — the stop-rule stands permanently.** Participation is 43–58 pp below the official
rates; the direction checks are mixed (hours direction passes: participation falls while fitted spend
rises; provider direction fails: commercial share 41.4% < 50% vs the observed hagwon 55.5% of spend).
Hours level 7.3 h/wk remains **UNABLE** (no hours object). So no one-country incidence claim is restored.

## E4 — KOR income gradient (demand-consistent)

Declared income-band multipliers 0.50/0.75/1.00/1.40/2.00; demand recalculated per band at the single
market price. Model participation rises 16.7→21.9→25.8→30.5→35.6%; spend per student 2.3→3.0→3.5→4.1→4.8%
of GDP pc. **Demand-consistent top/bottom spend ratio = 2.14** vs observed **3.67** (183k→671k won),
monotone increasing; inside the predeclared band [1.84,5.51]. (The mechanical income-multiplier identity
would give 8.55 and is reported only as a diagnostic.) **E4 verdict: PASS (demand-consistent)** — the
model generates a monotone but shallower income gradient than observed.

## Overall

- E1 FAIL ⇒ gate-position story dropped (per predeclaration). E1b FAIL ⇒ stop-rule stands permanently
  (no one-country incidence claim). E4 PASS ⇒ the income-gradient demand channel is the only positive
  loop-5 result (ratio 2.14 vs 3.67).
- KHM/PH transfer stays out-of-sample, not run. Relation slots PENDING.
