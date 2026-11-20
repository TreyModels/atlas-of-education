# PARAMS — declared parameters of the v1.4 Layer-2c demand-signal core

**LABEL: SYNTHETIC / DECLARED.** This is a declared-assumption parameter table. It contains no
result, no estimate, no fit, and nothing about any real country. Prose about "the ceiling" refers
to the synthetic `SYN00_PHL_LIKE` path, not the Philippines.

`code/sim_v1_4_demand.py` refuses to run unless this file's sha256 matches the value frozen in its
header. Authoritative copy of every value is the `P`, `DEM` and `DEST` dicts in the code; this file
is the human-readable mirror.

## 0. Frozen identities

| object | sha256 |
|---|---|
| `PRE_DECLARATIONS.md` (this module's spec) | `9ed0cae353c9a3dfba00582ff47d19ca8b761d8dd7b7ce5f9a8a8e4c5c5f49b3` |
| `code/base_v1_3_sim.py` (v1.3 base, byte-identical copy) | `70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877` |
| `generator_v1_3/results/synthetic_panel_v1_3.csv` (guard reference) | `47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3` |
| `generator_v1_2/results/synthetic_panel_v1_2.csv` (v1.3 c6 reference) | `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` |

## 1. What is added, and what is inherited unchanged

The base is v1.3 (`generator_v1_3/code/sim_v1_3.py`), whose own PARAMS.md remains
authoritative for the inherited v1.2 + shadow-module values. **No inherited value is changed.** This
table lists only what the demand block adds, plus the inherited values it reads (read-only).

| provenance label | meaning in this module |
|---|---|
| **OBSERVED-INPUT** | an observed series on disk that enters only as an input path (base generator); nothing new is observed |
| **BORROWED-STRUCTURAL** | read from the model's own state or from a frozen v1.2/v1.3 parameter; no new value is chosen |
| **DECLARED** | chosen by this worker, frozen before the run, not estimated |
| **NOT-VERIFIED** | declared because the literature coefficient is not retrievable; carries no evidential weight |

## 2. The demand block's own declared values

| id | symbol | meaning | value | unit | provenance | enters |
|---|---|---|---|---|---|---|
| D01 | `R_L` | declared destination rung sets of each credential: `L=1 → {1,2}` (clerical, production), `L=2 → {1,2,3}`, `L=3 → {2,3}` | sets, not numbers | rung index | **DECLARED** | `ω_r(L)`, `access_L`, `w_dest_L` |
| D02 | `mig_L` | declared migration probability of a holder of credential `L` | 0.010 / 0.040 / 0.070 | probability | **DECLARED / NOT-VERIFIED** | `ER_mig_L`, `remit_lift` |
| D03 | `dest_mult` | declared destination-wage differential (destination formal wage / home formal wage) | 3.50 | ratio | **DECLARED / NOT-VERIFIED** | `ER_mig_L`, `remit_lift` |
| D04 | `export_L` | declared exportability of the credential (share of holders for whom the foreign destination is relevant) | 0.10 / 0.50 / 0.70 | share | **DECLARED / NOT-VERIFIED** | `ER_mig_L`, `remit_lift` |
| D05 | `remit_prop` | declared remittance propensity of a migrant | 0.25 | share of destination wage | **DECLARED / NOT-VERIFIED** | `remit_lift` → fee-burden term only |
| D06 | `B_Z_D` | demand block's gate-pressure coefficient | 0.20 | utility per ln R | **DECLARED** | `v_D_L` |
| D07 | `ER_floor` | floor applied to `ER_P` inside `ln(1+·)` | −0.95 | household income units | **DECLARED** (numerical) | `v_D_L` |
| D08 | `lag` | expectation lag on every demand input | 1 | years | **DECLARED** | every `p_adv`, `R_gate`, `w_for`, `w_inf`, `J`, `hires`, `queue` term |

## 3. Inherited values the demand block reads (read-only, never re-fitted)

| quantity | value | provenance | enters |
|---|---|---|---|
| `H` | 20 years | **BORROWED-STRUCTURAL** (`shadow_module/PARAMETERS.csv` B17) | `gross_L`, cost/foregone capitalisation |
| `cost_base` | (0.05, 0.14, 0.22) | **BORROWED-STRUCTURAL** (v1.2 §5.3) | `cost_L` |
| `AGE_W` | (0.25, 0.70, 1.00) | **BORROWED-STRUCTURAL** (v1.2 §5.3) | `foregone_L` |
| `w_child`, `farm`, `cost`, `y_med`, `v0`, `decay`, `compat`, `neither`, `girl_care`, `haz` | per-country declared draws (v1.2 §5.3) | **BORROWED-STRUCTURAL** | `foregone_L`, `ER_hh` conversion, the household block |
| `phi_formal`, `rung_mult`, `cred_prem`, `rank_gain`, `seek`, `queue_retain`, `sep`, `psi`, `gp`, `accel_*` | frozen v1.2 values | **BORROWED-STRUCTURAL** (v1.2 PARAMS §6-7) | the model's own `w_for`, `w_inf`, `J`, `hires`, `queue`, `pi0`, `R` |
| gate pressure `R`, advance probability `pi0`, `Q`, `kappa` | computed by the model | **BORROWED-STRUCTURAL** (v1.3 gate contract) | `p_adv_L`, `R_gate_L` |
| `meas_completion_factor` `m` | 1.10 | **BORROWED-STRUCTURAL** (v1.2, single declared constant) | the scored UIS completion series |

## 4. Derived quantities (no free parameter)

```
w_dest_L   = Σ_{r∈R_L} ω_r(L) · w_for[r]        ω_r(L) = J_r / Σ_{r'∈R_L} J_r'
access_L   = Σ_{r∈R_L} ω_r(L) · a_r             a_r = hires_r / (hires_r + queue_r)
gross_L    = p_adv_L · (w_dest_L − w_inf) · H · access_L
ER_L       = gross_L − H·cost_L − H·foregone_L
ER_ann_L   = ER_L / H
ER_hh_L    = ER_ann_L · (y_med / w_inf)         [numeraire bridge: model wage units → household units]
ER_mig_L   = mig_L · (dest_mult − 1) · export_L · max(ER_hh_L, 0)
ER_net_L   = ER_hh_L + ER_mig_L
ER_P_L     = ER_net_L · p_adv_L
v_D_L      = ln(1 + max(ER_P_L, −0.95)) + B_Z_D · ln R_gate_L
remit_lift = remit_prop · mig_L · dest_mult · export_L
```

`v_D_2` replaces `v_2 = v0·decay²` **in the replacement arm only**, for all 30 countries. The
placement probability `a_r` uses `queue_r` (rung queues) and `hires_r` from the model's own matching
block; both are v1.2 state variables.

## 5. Units and the one declared conversion

`w_for`, `w_inf` and `ER_ann` are in model income units; `y_med` and the household block are in
household income units. The bridge is `y_med / w_inf`, the model's own informal wage expressed in
the household-block numeraire. There is **no free conversion constant**: the ratio is a model state
variable. `H` cancels between `gross` and `ER_ann`; `ER_L` is retained only because it is the
architecture's declared object and is reported in `DETAIL.csv`.

## 6. Calibration statement

**No value in this table was chosen by looking at the 2024 upper-secondary outcome.** The design-phase
record in `TUNE_LOG.md` lists what was seen before the freeze: the v1.3 baseline state magnitudes
(`w_for`, `w_inf`, `pi0`, `J` at 1970 and 2024) used to check that the declared formula's units were
coherent, and the v1.3 baseline ceiling (76.64). The declared values D01-D08 are round, declared
numbers; the only design-phase change to the code was correcting the `H` treatment (the one-year
horizon conversion in §5) before the freeze, which is recorded in `TUNE_LOG.md`. No coefficient was
set, moved or selected to place the replacement inside `[73,77]` or to clear the 3.0 pp ablation bar.

## 7. Migration/remittance status (repeated from the predeclaration)

`10_massification/lit/PUSH_PULL.md`: "Remittances → schooling: **NOT VERIFIED** ... Do not put a
remittance-schooling coefficient into the model without reading them." Accordingly: no literature
coefficient is inserted; D02-D05 are declared behavioural values; a measured remittance→schooling
coefficient remains **HELD** and is **not** imputed, proxied or back-filled. The observed remittance
series in `10_massification/data/JOBS_AND_MARKETS_PANEL.csv` is **not** encoded. The verified place
premium (Clemens, Montenegro & Pritchett 2008, 3.99, range 3.71-4.36) is a wage ratio, not a schooling
coefficient, and is **not** adopted here.

## 8. Freeze declaration

These values were frozen by `PRE_DECLARATIONS.md` before any scored run. The central-value run is the
scored run; the pre-declared sensitivity grid is reported beside it and cannot replace it. A FAIL is
reported as a FAIL and is never rescued by re-parameterising. Seed `20261120` (PCG64); floats `%.10g`;
two clean runs byte-identical.
