# CAP AUDIT — clamps, ceilings, floors and renormalisations (DEBUG)

**LABEL: DEBUG.** Audit only. No model behaviour was modified, no generator was run, no
experiment was re-run, nothing was fitted, no RNG was used, no causal or direction claim is
made. Every number below is a **count of cells on the frozen panels**, a **panel value**, or
an **arithmetic identity** on those panels; all of them are produced by `code/audit_caps.py`.

- Contract: `../PRE_DECLARATIONS.md`, sha256 `7d8bade95407a2fe76c95a740e0c98a74f34962117b33846df37a7d6a48f56a9` — **v1 + AMENDMENT 1 (measure-aware)**; the dispatch version was
  `748335cf915394c3f0dc0241fa2c5b6eaaae9c0af201dba97d3c2de24d8f6553`. The contract was AMENDED
  mid-audit (AMENDMENT 1, measure-aware); both hashes are recorded in `RUN_MANIFEST.json` and the
  audit applies the stricter, amended one.
- Named defect source: `08_council/DECISIONS.md` D160 / D164.
- Frozen panels audited: **v1.3** (6,720 rows), **v1.2** (6,720), **A17** (6,720).
- Determinism: two runs, byte-identical (`results/` vs `results/determinism_run2/`).

## 0. Headline

| item | value |
|---|---|
| clamp / ceiling / floor / renormalisation sites enumerated | **34** |
| — declared conventions (a) | **30** |
| — implementation artefacts (b) | **1** |
| — undetermined (c) | **3** |
| sites the fix must address | **1** |
| `completion_uis <= 1.0` binding cells | **v1.3: 35 · v1.2: 35 · A17: 0** (of 6,720 each) |

The named defect is confirmed exactly: **35/6,720** cells on v1.3 and **35/6,720** on v1.2 have
`completion_uis` printed at exactly 1.0 while the uncapped declared object `m x completion_cohort`
is above 1.0 (max **1.044677728** on v1.3, **1.044677728** on v1.2), and **0/6,720** on A17 (max uncapped
**0.9402099553**). The cap therefore binds only where the declared UIS object exceeds 1.0 — on the
two register panels, never on A17. That is the mechanism D160 recorded: the measured factor
`completion_uis / completion_cohort` equals 1.10 to
1e-9 on A17 (no cell capped), but falls below 1.10 wherever the cap overwrites the product, so `m`
reads NON-CONSTANT on v1.3/v1.2 (4.7043695535e-02) while it reads CONSTANT on A17 (8.8395202269e-10).

## 1. The `completion_uis <= 1.0` cap

Seven site lines in six code files carry the identical expression; the register panels are produced
by the **v1.3** copy (v1.3 panel), the **v1.2** copy (v1.2 panel) and the **frozen v1.6** copy inside
`generator_v1_7_partrepair/code/frozen/` (A17 panel). A17 imports that frozen copy
(`generator_v1_7_partrepair/code/sim_v1_7_partrepair.py:1117-1120`), so repairing any other v1.6
copy would not move A17.

| # | file:line | produces | binding cells |
|---|---|---|---|
| 1 | `generator_v1_3/code/sim_v1_3.py:832` | v1.3 panel | **35** |
| 2 | `generator_v1_2/code/sim_v1_2.py:610` | v1.2 panel | **35** |
| 3 | `generator_v1_7_partrepair/code/frozen/sim_v1_6_repair.py:1318` | A17 panel | **0** |
| 4 | `generator_v1_6_repair/code/sim_v1_6_repair.py:1318` | source of #3 | 0 |
| 5 | `generator_v1_4_demand/code/sim_v1_4_demand.py:969` | v1.4 | not in the register |
| 6–7 | `generator_v1_5_bimodal/code/sim_v1_5_bimodal.py:756, 808` | v1.5 (two branches) | not in the register |

Expression (verbatim): `out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)`
where `clip(x, lo, hi) = max(lo, min(hi, float(x)))` (`sim_v1_3.py:211-212`) and
`P["meas_completion_factor"] = 1.10`.

**Why it is an artefact and not a convention.** The declared UIS convention is
`completion_uis = m x cohort-flow`, m = 1.10, single constant, all levels and countries
(`generator_v1_2/PARAMS.md` §7; v1.6 `PRE_DECLARATIONS.md` R7c). **No PARAMS, PRE_DECLARATIONS
or MODEL_ARCHITECTURE text declares a 1.0 ceiling on `completion_uis`.** The two on-disk texts
that come nearest are quoted exactly:

1. `generator_v0/FINDINGS.md:39` — C5 'hard sanity: no negative enrolment; GER/completion in
   [0,105]; rates in [0,1]'. This is a **check on v0's own output** (v0 completion 0.77–95.01,
   in pp) and not a declared convention of the v1.2+ `completion_uis` object.
2. `generator_v1_2/FINDINGS.md:191` — '**The model's primary UIS completion reaches 100 % by 2024**
   (observed 98.3 %) — a ceiling artifact of `m × cohort-flow` clipping. It is not used as a check.'
   The programme's own v1.2 findings therefore **already named this cap a ceiling artefact**, which
   is the classification this audit independently reaches from the code and the panels.

By construction the declared object **must** exceed 1.0 whenever
cohort-flow > 1/1.10 = 0.909090…, so the ceiling changes the declared object. That is exactly the
35 cells; the companion `comp_coh` cap at 1.0 (CAP-02) binds in **0** cells because cohort-flow
itself never reaches 1.0 (max **0.9497070255** on v1.3, **0.854736323** on A17).

**Arithmetic verified, not assumed.** The audit reconstructs cohort-flow from the panels
(`admitted_official(t - DVEC) / cohort(t - DVEC)` x `clip(surv_max x Q^theta, 0.02, 0.995)`) and
checks it against the emitted `completion_cohort` column and against the cap itself. Maximum
absolute residual over the 6,720 rows of each panel (three panels, 20,160 rows): **6.61e-10** (cohort-flow) and **6.98e-10**
(`completion_uis` vs `min(m x cohort-flow, 1.0)`, at the panels' 10-significant-figure CSV
precision). The reconstruction
therefore reproduces the panel's own arithmetic, so the 35-cell count is the cap and nothing else.

### The 35 cells (v1.3; the identical set on v1.2)

All 35 are **primary** level, in five countries; the cap never binds at lower-secondary,
upper-secondary or tertiary:

| country | level | n cells | years | cohort-flow range | uncapped m x flow | capped |
|---|---|---|---|---|---|---|
| SYN00_PHL_LIKE | primary | 2 | 2024–2025 | 0.9162480129–0.9200914785 | 1.007872814–1.012100626 | 1.0 |
| SYN07 | primary | 14 | 2012–2025 | 0.9286930711–0.9497070255 | 1.021562378–1.044677728 | 1.0 |
| SYN10_BOOM | primary | 2 | 2024–2025 | 0.9162480128–0.9202209151 | 1.007872814–1.012243007 | 1.0 |
| SYN19 | primary | 5 | 2021–2025 | 0.9093260975–0.9153694921 | 1.000258707–1.006906441 | 1.0 |
| SYN23 | primary | 12 | 2014–2025 | 0.9097506217–0.923735361 | 1.000725684–1.016108897 | 1.0 |

Per-cell values (panel, cell id, country, level, year, panel row, uncapped, capped) are in
`CAP_AUDIT_CELLS.csv`, `clamp_id == CAP-01` — 70 rows (v1.3 35 + v1.2 35).

### 1.1 Measure classification (AMENDMENT 1, binding)

The contract was amended while this audit ran: every clamp must be classified **by measure**, and
the cap must not be read as an NER bound. The measures on disk are different objects, and only one
of them is bounded above by construction:

| id | measure | definitional bound? | class |
|---|---|---|---|
| CAP-01 | CR (UIS completion rate, m x cohort-flow) | NOT definitional: a CR's denominator is the 3-5-years-above-grade cohort, so a CR is not bounded by 1.0 (AMENDMENT 1 / sec.6). A 1.0 ceiling on a CR is NOT an NER bound. | (b) |
| CAP-02 | CR (cohort-flow share) | definitional-ish: cohort-flow is a share of the entry cohort, bounded by 1 by construction. | (a) |
| CAP-05 | CR (measurement constant m) | convention: m = 1.10 is the declared CR measurement choice (a stand-in for the older denominator), not a bound. | (a) |
| CAP-06 | GER (all enrolment / official-age population) | NOT an NER bound: this is a declared Z1 GATE on GER, and GER may exceed 100 by definition (repeaters / over-age). Per AMENDMENT 1 it must never be read as 'GER cannot exceed 105'. | (a) |
| CAP-10 | demand (applicants, not a rate) | declared domain/identity bound | (a) |
| CAP-12 | eligibility share (of cohort) | declared domain/identity bound | (a) |
| CAP-18 | share (probability simplex) | definitional: a probability vector sums to 1. | (a) |

**NER is the only measure bounded by 100 (definitional).** No NER object exists in the pipeline:
the panels emit `ger`, `completion_cohort` (CR) and `admission` shares, and **no** `ner` column on
any of the three panels. So the 1.0 ceiling cannot be defended as an NER bound — it is applied to a
**CR**, whose denominator is the older 3–5-years-above-grade cohort and which is therefore **not**
bounded by 1.0 (AMENDMENT 1: PHL 2024 = 98.3 CR on 94.0 GER).

### 1.2 The 35 capped cells against GER (AMENDMENT 1 requirement)

For every capped cell the audit reports the model's own GER at that cell and whether the uncapped
CR is above it (`CAP_AUDIT_CELLS.csv` columns `ger_at_cell`, `cr_over_ger`, `cr_minus_ger_pp`,
`measure_verdict`).

| question | answer |
|---|---|
| capped cells with **CR > GER** (legitimate CR-above-GER cases) | **0 of 70** rows (v1.3: **0 of 35**, v1.2: **0 of 35**) |
| capped cells with **CR <= GER** | **70 of 70** rows |
| GER at the capped cells | **105.0 in all 70** (the declared Z1 gate is binding there) |
| uncapped CR at the capped cells | **100.0258707–104.4677728 pp** |
| CR − GER spread at the capped cells | **-4.974129277 to -0.5322271897 pp** (all negative) |

**Verdict on the 35: none is a legitimate CR-above-GER case.** In all 35 the model's GER sits at
its declared 105 gate and the CR is *below* it (100.03–104.47 pp). The cap therefore cuts a CR that
is already under the model's own GER — it cannot be described as 'holding CR down to GER' or as an
NER-style impossibility. The 15 cells on v1.3 where the model does put CR above GER (max +2.65 pp)
are **not** capped (their CR < 1.0). Both facts are arithmetic on the frozen panels.

Note the co-location, which is descriptive only: all 35 capped cells are primary cells in which
official-age admission is ≈0.991–0.996 of the cohort and survival 0.916–0.956, so cohort-flow is
0.909–0.950 and m x cohort-flow is 1.000–1.045; the same cells sit on the cohort branch of the
declared capacity gate (1.05 x cohort), which is why GER is at 105 there. No causal claim is made.

## 2. Full register

**`cells`** = panel cells in which the bound **changes** the value (strictly beyond the bound),
except for a constant convention (CAP-05) where it is the number of cells the constant is applied
to, and for a renormalisation (CAP-18) where it is the number of cells the identity holds in.
`n/a` = the site is not on the frozen-panel path (§4) or the pre-clip object is internal and not
emitted. The note in `CAP_AUDIT_TABLE.csv` gives ties, ranges and per-panel qualifiers.

`CAP_AUDIT_CELLS.csv` adds `binding_kind`: **strict** = the pre-clip value is reconstructed and
lies beyond the bound (CAP-01, CAP-04, CAP-06); **branch** = a `min()` arm was selected (CAP-07);
**at_bound_not_reconstructible** = the emitted column is already post-clip, so the bound is
observed but the pre-clip value cannot be recovered from the panel (CAP-11, CAP-23).

| id | stage | symbol / expression | file:line | bound | object | v1.3 | v1.2 | A17 | class |
|---|---|---|---|---|---|---|---|---|---|
| CAP-01 | completion (UIS convention) | `out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, …` | `sim_v1_3.py:832` | [0.0, 1.0] | completion_uis (UIS-convention completion) | 35 | 35 | 0 | **(b)** |
| CAP-02 | completion (cohort flow) | `comp_coh = clip(a_entry * surv, 0.0, 1.0)` | `sim_v1_3.py:828` | [0.0, 1.0] | completion_cohort (cohort-flow completion) | 0 | 0 | 0 | **(a)** |
| CAP-03 | survival | `surv = clip(P["surv_max"][L] * Qq[L] ** P["surv_theta"][L], 0.02, 0.995)` | `sim_v1_3.py:826` | survival <= 0.995 | survival | 0 | 0 | 0 | **(a)** |
| CAP-04 | survival | `surv = clip(P["surv_max"][L] * Qq[L] ** P["surv_theta"][L], 0.02, 0.995)` | `sim_v1_3.py:826` | survival >= 0.02 | survival | 24 | 24 | 24 | **(c)** |
| CAP-05 | measurement convention | `clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)` | `sim_v1_3.py:832` | m = 1.10 (single constant, all levels/countries) | measurement_factor | 6720 | 6720 | 6720 | **(a)** |
| CAP-06 | enrolment ratio | `out["ger"][L, t] = clip(100.0 * admitted / max(C[L, t], 1e-9), 0.0, P…` | `sim_v1_3.py:817` | GER in [0, 105] | GER | 27 | 27 | 0 | **(a)** |
| CAP-07 | capacity gate | `phys = min(P["phys_cap"] * seats[L], P["overage_cap"] * C[L, t])` | `sim_v1_3.py:809` | phys <= min(1.15 x seats, 1.05 x cohort) | physical admission capacity | 125 | 125 | 125 | **(a)** |
| CAP-08 | capacity gate | `adm_off = min(D_off, phys)` | `sim_v1_3.py:810` | adm_off <= phys | admitted_official (rationing) | 3189 | 3189 | 5733 | **(a)** |
| CAP-09 | capacity gate | `adm_oa = min(D_oa, max(0.0, phys - adm_off))` | `sim_v1_3.py:811` | adm_oa <= phys - adm_off | admitted_overage | 3543 | 3543 | 332 | **(a)** |
| CAP-10 | tertiary demand | `D_off = p3 * min(pools[3], 1.05 * C[3, t])` | `sim_v1_3.py:797` | tertiary demand <= 1.05 x cohort | demand_official (tertiary) | 116 | 112 | 79 | **(a)** |
| CAP-11 | eligibility pool | `pools[L] = min(newpool, 1.05 * C[L, t])` | `sim_v1_3.py:873` | pool <= 1.05 x cohort | eligibility_pool | 77 | 77 | 62 | **(a)** |
| CAP-12 | eligibility share | `elig = 1.0 if L == 0 else min(1.0, pools[L] / max(C[L, t], 1e-9))` | `sim_v1_3.py:788` | elig <= 1.0 | eligibility share | 1655 | 1651 | 1079 | **(a)** |
| CAP-13 | out-of-school composition | `both_f = p_b * elig * C[L, t] * min(1.0, adm_off / max(D_off, 1e-9))` | `sim_v1_3.py:847` | share <= 1.0 | both_share mass | 3531 | 3531 | 987 | **(a)** |
| CAP-14 | reported PTR | `out["ptr"][:, t] = np.clip(ptr, 2.0, 150.0)` | `sim_v1_3.py:883` | PTR in [2, 150] | ptr | 0 | 0 | 0 | **(c)** |
| CAP-15 | growth | `g = clip(gs + comp_term + gnoise[t], P["g_floor"], P["g_cap"])` | `sim_v1_3.py:945` | growth in [0.0, 0.090] | growth | 0 | 0 | 0 | **(a)** |
| CAP-16 | labour queue | `queue_carry = np.minimum(P["queue_retain"] * np.maximum(remaining, 0.0),` | `sim_v1_3.py:931` | queue_carry <= 0.20 x LF | queue carry-over | n/a | n/a | n/a | **(a)** |
| CAP-17 | employment | `E_r = np.minimum(E_r, J)` | `sim_v1_3.py:934` | employment <= jobs | formal employment by rung | n/a | n/a | n/a | **(a)** |
| CAP-18 | four-state shares | `Pr /= Pr.sum()` | `sim_v1_3.py:632` | shares on the simplex (sum = 1) | school/both/work/neither shares | 5040 | 5040 | 5040 | **(a)** |
| CAP-19 | sector shares | `v = np.maximum(np.array([a, i, m, s]), floors)` | `sim_v1_3.py:704` | sector shares >= sec_floors = (0.02, 0.05, 0.03, 0.05) | s_ag / s_inf / s_man / s_srv | 2188 | 2188 | 1980 | **(a)** |
| CAP-20 | sigmoid argument | `x = max(-30.0, min(30.0, float(x)))` | `sim_v1_3.py:207` | |x| <= 30 | sigmoid argument | n/a | n/a | n/a | **(c)** |
| CAP-21 | gate numbers Q / pi0 / kappa / R | `Q = min(max(float(cand) / max(float(cap), 1e-9), 0.0), 10.0)` | `sim_v1_3.py:306` | Q in [0,10]; pi0 in [0.01,0.999]; kappa in [1.0,5.0]; R in [1.0,20.0] | Q_gate / pi0 / kappa / R | 622 | n/a | 664 | **(a)** |
| CAP-22 | two-tier capacity split (v1.6/A17) | `K_H_L = tc["h_share"][L] * seats[L]` | `sim_v1_6_repair.py:1164` | K_H = h_share x seats; K_O = seats - K_H | tier_K_H / tier_K_O | n/a | n/a | 5738 | **(a)** |
| CAP-23 | advancement share (v1.6/A17) | `p_adv_L = clip(admitted_H / max(A_H_L, 1e-9),` | `sim_v1_6_repair.py:1191` | p_adv in [0.01, 0.999] | tier_p_adv_H | n/a | n/a | 1059 | **(a)** |
| CAP-24 | kappa constraint (v1.6, COMPLETION units) | `_cap_rate = clip(_bound_e / max(_m * _surv_u, 1e-12), 0.0, 1.0)` | `sim_v1_6_repair.py:1252` | e(s) <= kappa x comp_lower(s-3); _cap_rate in [0,1] | upper-secondary admitted (A17 only) | 0 | 0 | 0 | **(a)** |
| MOD-01 | A1 anchor: capacity sub-indices | `parts.append(float(np.clip((40.0 - p[t]) / 20.0, 0, 1))); wts.append(…` | `anchor.py:54` | sub-index in [0,1] | capacity index C_t | n/a | n/a | n/a | **(a)** |
| MOD-02 | A1 anchor: capacity index | `C[t] = float(np.clip(np.average(parts, weights=wts), 0, 1))` | `anchor.py:60` | C_t in [0,1] | capacity index | n/a | n/a | n/a | **(a)** |
| MOD-03 | A1 anchor: gate | `return float(max(C, 0.0) ** kappa)` | `anchor.py:68` | gate >= 0 | G(C) = C^kappa | n/a | n/a | n/a | **(a)** |
| MOD-04 | A1 anchor: policy markers | `if 2013 <= t:  m = max(m, 1.0)` | `anchor.py:77` | marker in {0,1} | K-12 / free-SHS / free-tertiary markers | n/a | n/a | n/a | **(a)** |
| MOD-05 | A1 anchor: ceiling push | `CEIL = 0.25` | `anchor.py:82` | ceiling push = 0.25 x PUSH x gate | ceiling-level saturating share | n/a | n/a | n/a | **(a)** |
| MOD-06 | push-pull: intake rate | `intake_rate = float(np.clip(intake_rate * (max(gdp_lag, 1e-9) ** eta_…` | `pushpull.py:90` | intake_rate in [0,1] | intake rate | n/a | n/a | n/a | **(a)** |
| MOD-07 | push-pull: participation probabilities | `p_pri = float(np.clip(p_pri + _pv, 0.02, 0.995))` | `pushpull.py:109` | p_pri in [0.02,0.995] etc. | level participation probabilities | n/a | n/a | n/a | **(a)** |
| MOD-08 | push-pull: sector shares | `agri = float(np.clip(0.75 * np.exp(-0.35 * logy) + 0.02, 0.01, 0.95))` | `pushpull.py:123` | sector shares in [0.01,0.95] / [0.02,0.95] | agri / services / formal shares | n/a | n/a | n/a | **(a)** |
| MOD-09 | push-pull: reported GER | `ger_primary=100 * prim / max(pop[6:12].sum(), 1e-9)` | `pushpull.py:140` | enrolment / population (no cap) | ger_primary..ger_tertiary | n/a | n/a | n/a | **(a)** |
| MOD-10 | repair: logit transform guard | `c = np.clip(np.array([x['completion_lower'] for x in h])[w] / 100.0, …` | `repair.py:65` | c in [1e-4, 1-1e-4] | completion share entering a logit | n/a | n/a | n/a | **(a)** |

`file:line` is the first site of each entry; CAP-01 lists all seven copies in §1, and CAP-21
covers four bounds at one site. `CAP_AUDIT_TABLE.csv` carries the same register with the full
`why`, `declared_in`, the complete site list and the per-panel notes.

## 3. Declared conventions vs implementation artefacts

**Declared conventions (a), 30 sites** — bounds that are part of the declared object:

- **CAP-02** `sim_v1_3.py:828` — completion_cohort (cohort-flow completion). Declared in: MODEL_ARCHITECTURE.md sec.1: 'completion is a cohort-flow object'; a cohort-flow share is a proportion of the entry cohort and is bounded by 1 by construction
- **CAP-03** `sim_v1_3.py:826` — survival. Declared in: survival is a probability (PARAMS surv_max, 'survival at zero congestion'); the 0.995 guard sits inside the declared envelope max(surv_max) = 0.96
- **CAP-05** `sim_v1_3.py:832` — measurement_factor. Declared in: generator_v1_2/PARAMS.md sec.7 'CONVENTION / measurement choice'; v1.6 PRE_DECLARATIONS R7c 'm frozen at 1.10 ... a CONVENTION, not a conversion'
- **CAP-06** `sim_v1_3.py:817` — GER. Declared in: PARAMS overage_cap = 1.05 commented 'GER hard cap (Z1 gate)'; MODEL_ARCHITECTURE.md line 45 'GER bounded <=105'; v1.3 PRE_DECLARATIONS sec.4.1 (Z1)
- **CAP-07** `sim_v1_3.py:809` — physical admission capacity. Declared in: PARAMS phys_cap = 1.15 'max pupils per adequate place (double shifts)' and overage_cap = 1.05 'GER hard cap (Z1 gate)'
- **CAP-08** `sim_v1_3.py:810` — admitted_official (rationing). Declared in: the declared capacity gate: admission = min(demand, physical capacity) (MODEL_ARCHITECTURE.md Layer 1c; PRE_DECLARATIONS sec.4.1)
- **CAP-09** `sim_v1_3.py:811` — admitted_overage. Declared in: declared residual-capacity allocation of over-age applicants (PARAMS oa_rate)
- **CAP-10** `sim_v1_3.py:797` — demand_official (tertiary). Declared in: the same declared Z1 1.05 ceiling on demand (PARAMS overage_cap)
- **CAP-11** `sim_v1_3.py:873` — eligibility_pool. Declared in: the same declared Z1 1.05 ceiling, applied to the carry-over pool
- **CAP-12** `sim_v1_3.py:788` — eligibility share. Declared in: a share of the cohort cannot exceed 1; declared pool construction (PARAMS init_pipe / pool_retain)
- **CAP-13** `sim_v1_3.py:847` — both_share mass. Declared in: a probability mass; bounded by construction
- **CAP-15** `sim_v1_3.py:945` — growth. Declared in: PARAMS g_floor = 0.0, g_cap = 0.090 (declared band)
- **CAP-16** `sim_v1_3.py:931` — queue carry-over. Declared in: PARAMS queue_retain = 0.50, queue_max_lf = 0.20 (declared)
- **CAP-17** `sim_v1_3.py:934` — formal employment by rung. Declared in: the employment identity (employment cannot exceed the rung's job stock) -- declared Layer 0/3
- **CAP-18** `sim_v1_3.py:632` — school/both/work/neither shares. Declared in: the borrowed-structural multinomial (BORROWED-FROM-ATLAS); a probability vector sums to 1
- **CAP-19** `sim_v1_3.py:704` — s_ag / s_inf / s_man / s_srv. Declared in: PARAMS sec_floors (declared), applied in the marked-share projection with a 60-step project-back loop
- **CAP-21** `sim_v1_3.py:306` — Q_gate / pi0 / kappa / R. Declared in: v1.3 PRE_DECLARATIONS.md sec.4.1 lines 124-128 (frozen R definition), reproduced in PARAMS.md line 28 ('clipped [1,20]')
- **CAP-22** `sim_v1_6_repair.py:1164` — tier_K_H / tier_K_O. Declared in: v1.6 PRE_DECLARATIONS (I2-I4 declared two-tier allocation; T01 h_share from v1.5 PARAMETERS.csv)
- **CAP-23** `sim_v1_6_repair.py:1191` — tier_p_adv_H. Declared in: v1.6 PARAMS.md:39 S08 padv_clip = (0.01, 0.999) DECLARED (PRE_DECLARATIONS.md:254)
- **CAP-24** `sim_v1_6_repair.py:1252` — upper-secondary admitted (A17 only). Declared in: v1.6 PRE_DECLARATIONS I6 / Rule R1: the kappa constraint in completion units, 'enforced == audited'
- **MOD-01** `anchor.py:54` — capacity index C_t. Declared in: docstring: 'C_t in [0,1]: delivery 0.5 (PTR), fiscal 0.3, enforcement 0.2'; declared mapping
- **MOD-02** `anchor.py:60` — capacity index. Declared in: declared composite index (anchor.py docstring; PRE_ANCHOR_A1)
- **MOD-03** `anchor.py:68` — G(C) = C^kappa. Declared in: declared gate; kappa in [0.5,1.0] with sensitivity reported (anchor.py KAPPA note)
- **MOD-04** `anchor.py:77` — K-12 / free-SHS / free-tertiary markers. Declared in: declared POLICY mapping (anchor.py comments per marker; PRE_ANCHOR_A1)
- **MOD-05** `anchor.py:82` — ceiling-level saturating share. Declared in: declared 'saturating share to ceiling levels' (A10, anchor.py comment)
- **MOD-06** `pushpull.py:90` — intake rate. Declared in: a rate (share of the cohort); the [0,1] domain is the object's definition
- **MOD-07** `pushpull.py:109` — level participation probabilities. Declared in: probabilities; the guard keeps them inside (0.02, 0.995) -- declared in the model's parameter block
- **MOD-08** `pushpull.py:123` — agri / services / formal shares. Declared in: shares of employment; declared guards in the ported Layer 0/3 block
- **MOD-09** `pushpull.py:140` — ger_primary..ger_tertiary. Declared in: this site has NO clamp at all -- it divides by the band population with an epsilon guard; recorded to show the observed chain does not cap GER at 105
- **MOD-10** `repair.py:65` — completion share entering a logit. Declared in: numerical guard required by log(c/(1-c)) in an analysis helper (A3 logit regression)

**Implementation artefacts (b), 1 site** — a bound that changes a declared object and is declared
nowhere on disk:

- **CAP-01** `sim_v1_3.py:832` — [0.0, 1.0] (completion_uis (UIS-convention completion)). the declared object can exceed 1 by construction when cohort-flow > 1/1.10, so the 1.0 ceiling changes the declared object; the programme's own v1.2 findings already called it a ceiling artefact, and D160 names it the defect; 35/6,720 cells bind

**Undetermined (c), 3 sites** — undeclared bounds that need the Lead / Council:

- **CAP-04** `sim_v1_3.py:826` — survival >= 0.02 (survival). undeclared numerical floor that BINDS and raises survival in 24 tertiary cells (1970-1972, 20 countries, burn-in); it changes completion_cohort and therefore every downstream level number. Not the named defect (it is upstream of the m-cap and identical on all three panels), but it must be adjudicated before any level sentence is called clean
- **CAP-14** `sim_v1_3.py:883` — PTR in [2, 150] (ptr). undeclared reporting guard, but NON-BINDING: observed PTR range 7.71-63.13 over all three panels, 0 cells at either bound; recorded for completeness, no fix
- **CAP-20** `sim_v1_3.py:207` — |x| <= 30 (sigmoid argument). cannot bind on any observed argument (sigmoid saturates at |x| ~ 30, where 1/(1+e^-x) is 1.0 to double precision); 0 informative cells; no fix. Guard only.

Only **CAP-04** among the (c) items actually binds on a model object (24 tertiary cells, below).
CAP-14 (`ptr` guard) and CAP-20 (`sig` guard) bind in 0 informative cells.

## 4. Scope and what was NOT audited

- **In scope and counted**: the synthetic generator chain v1.2→v1.7 that produces the frozen
  panels — every `comp_uis` / `comp_coh` / `surv` / `ger` / capacity / share / gate-number site.
- **Adjacent model code, listed not counted**: `10_massification/model/{anchor,pushpull,repair}.py`
  belongs to the **A1 anchor class / observed chain**, not to the synthetic panel path. Its bounds
  are declared (MOD-01…MOD-10) and none of them can bind on a synthetic panel cell; they are in the
  register so the enumeration is complete, with `n/a` counts. MOD-09 is deliberately listed as a
  site with **no** clamp (the observed chain does not cap GER at 105) to show the contrast.
- **Econometric input guards excluded as non-model**: `np.log(x.clip(lower=1e-3))`-style guards in
  the `dt_/edu_eci_/lab_` extension scripts (log-domain hygiene on observed inputs). They never
  touch a model object; no panel cell depends on them, so they are not clamps of model behaviour.
- **Internal state that is not emitted** (`queue_carry <= 0.20 x LF`, `E_r <= J`, `att`): the
  bound is real but the pre-clip quantity is not in any panel, so **no cell count is claimed** —
  stated, not guessed (CAP-16, CAP-17).
- **No re-derivation of model values**: the audit reads the frozen panels; it does not re-run the
  generator, does not re-score EXP-21 and produces no new model number.

## 5. Minimal defect set for Agent 2

**One defect, one expression, seven site lines in six files — three of them produce the register**
**panels:**

```
out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)
```

The fix must make `completion_uis` the **declared** object `m x cohort-flow` (m = 1.10, no
undeclared upper bound). At minimum it must touch the copies that produce the register panels:
`sim_v1_3.py:832` (v1.3), `sim_v1_2.py:610` (v1.2) and `frozen/sim_v1_6_repair.py:1318` (A17).
The lower bound `0.0` may stay (a completion cannot be negative; 0 cells bind), but the upper
bound must go, or be replaced only by an explicitly declared and defended UIS CR convention.
**No threshold, parameter, seed or fitted value changes; the repair is the ceiling only.**

**Measure-aware conditions on that fix (AMENDMENT 1):**

1. **Do not touch the GER cap (CAP-06) as part of this fix.** It is a declared Z1 gate, not an NER
   identity, and the amendment forbids recasting GER as if it were NER-bounded. Moving it would be a
   threshold change, which the contract bars.
2. **Do not introduce an NER cap anywhere.** No NER object exists on disk; NER <= 100 is
   definitional and needs no clamp, because there is nothing to clamp.
3. **The declared convention to state explicitly** in the repaired code/manifest is the UIS CR
   convention: completion = share of the population 3–5 years above grade that completed the level,
   with repeaters across years and over-age entrants counted, m = 1.10 as the declared single
   constant standing in for that older denominator. On that convention a CR above 1.0 and a CR
   above GER are both admissible.
4. **Report, per cell, whether the repaired CR now exceeds GER** (the same four columns the audit
   emits), so the measure question is answered on the re-run and not asserted.

**Not in the minimal set** (reported, not licensed by this defect):

- **CAP-04** — survival floor 0.02: 24 tertiary cells (20 countries, 1970–72 burn-in), identical
  on v1.3/v1.2/A17. It binds and is undeclared, so it is a genuine open item, but it is upstream of
  the m-cap and cannot explain the v1.3-vs-A17 constancy difference. It must be adjudicated
  separately and must **not** be changed under the ceiling-cap licence.
- **CAP-14 / CAP-20** — undeclared, non-binding guards: 0 cells, no action.
- **CAP-18 note (not a clamp)** — on A17 the four-state shares sum to 1 in 5,040/5,040
  lower/upper/primary cells, exactly as on v1.3; the tertiary rows that do not sum to 1
  (1,590 of 1,680 on A17, all 1,680 on v1.3) are the declared adult exemption, not a violation.

## 6. Reproduction

```
python code/audit_caps.py --out results
python code/audit_caps.py --out results/determinism_run2
```

Each run writes `CAP_AUDIT.md`, `CAP_AUDIT_TABLE.csv`, `CAP_AUDIT_CELLS.csv` and `console.txt`
into `--out`; the two runs are byte-identical. `python code/audit_caps.py --manifest-only`
regenerates `RUN_MANIFEST.json` from the same counts without writing any other artifact.
Hashes of every input and output are in `RUN_MANIFEST.json` and `SHA256SUMS.txt`.

