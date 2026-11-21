# AUDIT — education expansion (codex assumption-audit item 4): asks mapped to what this record holds

**LABEL: `DERIVED`** (mapping memo; no new run; every claim points to a file). Date 2026-11-21.
Codex's item-4 asks, as relayed: **which seat/budget paths are supplied in advance; the parent's alternative vs the
provider's decision; the failed expansion run retained; matched reversions.** Below: what exists, where, and what is
missing. **No number here is a new result.**

## 1. Seat and budget paths — supplied in advance (yes, throughout the closed phase)

| object | where | how it enters | status |
|---|---|---|---|
| generator capacity gate | `10_massification/extensions/synthetic_2026-11-20/generator_v1_3/code/sim_v1_3.py` (`phys = min(phys_cap·seats, overage_cap·cohort)`); `PARAMS.md` `phys_cap=1.15`, `overage_cap=1.05` (Z1) | **declared seat/cohort paths**, not decisions | exogenous |
| tier stock (two-tier class) | `generator_v1_5_bimodal/PRE_DECLARATIONS.md` (`K_H`, `K_O` declared tier capacities) | **declared tier places** | exogenous |
| A2 anchor capacity | `10_massification/model/anchor.py` `capacity_index()` (PTR/fiscal index) | an **exogenous capacity index** feeding the anchor class | exogenous |
| budget | — | **no budget decision exists in the closed phase**; the "capacity explains the timing" claim was **KILLED** (D61/R28) | absent (by decision) |
| coevolve v0 (new) | `10_massification/extensions/coevolve_2026-11-21/PRE_DECLARATIONS.md` §3 | **endogenous supply**: district class-opening/section/elsewhere + private-provider entry/exit; **no seat totals in advance**, D0-INPUT-SEATS release-blocking | predeclared, **not run** |

**So:** the closed phase supplies seat (and tier) paths in advance and has **no budget decision**; the requirement is
met only by the **unrun** coevolve v0.

## 2. Parent's alternative vs provider's decision

- **Parent's alternative** exists: massabm households face income (CRRA) and a hard cash constraint with a discrete
  attendance choice (`~/massification_external/massabm_2026-10-24/round2/README.md`); the closed generator's
  four-state childworld block carries **school / work / neither / both** with an outside option
  (`generator_v1_2`/`v1_3` childworld block; the `v1.5` repair reproduced it, D134/D141). The **actual alternative**
  (work/home, what stopping forgoes) is modelled, not assumed away.
- **Provider's decision** is **absent as a live object** in the closed phase: the C1 provider-entry cell is retained
  **as a design** (D86), the two-tier class supplies tier stock as declared capacity (v1.5), and no district or
  private provider decides to open a class in v1.2/v1.3. **coevolve v0 §3 supplies it** (not run).

## 3. Failed expansion run — retained, not deleted

| failed object | file | status |
|---|---|---|
| A3-D demand block (unrationed single-gate demand) | `generator_v1_4_demand/` (`FINDINGS.md`, predecl `9ed0cae3…`) | **FALSIFIED** (D116); the A3 demand line was later **KILLED** (D130) |
| v1.5 BIMODAL-GATE level collapse | `generator_v1_5_bimodal/FINDINGS.md` | **FAIL** on checks b/d; representation-only (D131) |
| EXP-14 V16-REPAIR | `generator_v1_6_repair/FINDINGS.md` | **PATH-FAILED**; no successor (D141) |
| EXP-18 PART-REPAIR (closing rule) | `generator_v1_7_partrepair/FINDINGS.md` | **PATH-FAILED; GENERATOR-LINE-CLOSED** (D150) — retained, no re-tune |
| toy battery (15 experiments) | `10_massification/extensions/codex_2026-11-20/toys_2026-11-20/` + D86 | retained **as a labelled design appendix**, off the critical path |

## 4. Matched reversions

- **massabm round-2 audit** (`~/massification_external/massabm_2026-10-24/round2/audit/findings.txt`): matched-seed
  single reversions — `diploma_by_years`, `adult_earnings_from_16` (**flips the headline sign** −0.072 → +0.063),
  `no_free_tuition_2018`, `weak_pressure_valve`, `state_sees_architecture_early`, `referrals_ignore_floor`,
  `no_cash_transfers`, `dropout_per_stage`; the headline reversal survives all but `adult_earnings_from_16`.
- **toy battery**: `codex_2026-11-20/toys_2026-11-20/cluster_A/PRE_DECLARATIONS.md` declares matched-seed cells
  (6 cells = L × {temporary, permanent}, 200 seeds, same cohorts).
- **Closed phase generator line**: **no reversion battery** (not applicable — the line was closed at representation-only;
  re-runs are forbidden by D154).

## 5. Bottom line for codex

The record **can** map the parent's alternative and retained failed expansions; it **cannot** map an endogenous
provider decision or a budget path (absent by decision), and it **has** matched-seed single reversions in massabm.
**The gap codex names (seat totals supplied in advance) is real and is exactly what coevolve v0 is predeclared to
close** — nothing in the closed phase should be read as having closed it.
