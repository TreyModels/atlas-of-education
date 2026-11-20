#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build PARAMS.md (declared values + provenance + frozen spec hash) from the FROZEN
shadow_module/PARAMETERS.csv plus the inherited v1.2 block. One source of truth: the CSV.
No number in the generated file is typed by hand.

LABEL: SYNTHETIC / DECLARED. No result here.
"""
import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT13 = HERE.parent
SYNTH = ROOT13.parent
SHADOW = SYNTH / "shadow_module"
PARAMS = SHADOW / "PARAMETERS.csv"
PREDECL_SHA = "cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2"
S1_SHA = "af49a616a7b57c4ef23a693c155d022cd17817f66f5acafba4dc6798dedb65eb"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


rows = list(csv.DictReader(PARAMS.open()))
assert len(rows) == 42, "PARAMETERS.csv must carry 42 declared rows, found %d" % len(rows)

L = []
L.append("# PARAMS — declared parameters of the v1.3 shadow-education-at-the-gates module\n")
L.append("**LABEL: SYNTHETIC / DECLARED.** This is a declared-assumption parameter table. It contains no "
         "result, no estimate, no fit, and nothing about any real country. `SYN_HKG_LIKE`, `SYN_PHL_LIKE` "
         "and `SYN_KHM_LIKE` are synthetic country types, not Hong Kong, the Philippines or Cambodia.\n")
L.append("Generated from the frozen `shadow_module/PARAMETERS.csv` by `_scratch/build_params.py`; the "
         "table below is that file's 42 rows, reproduced mechanically, so there is one source of truth. "
         "`code/sim_v1_3.py` refuses to run unless this file's sha256 matches the value frozen in its "
         "header.\n")
L.append("## 0. Frozen identities\n")
L.append("| object | sha256 |")
L.append("|---|---|")
L.append("| `shadow_module/PRE_DECLARATIONS.md` (frozen v1.3 spec) | `%s` |" % PREDECL_SHA)
L.append("| `shadow_module/PRE_DECLARATIONS_S1_NOTE.md` (binding controller note) | `%s` |" % S1_SHA)
L.append("| `shadow_module/PARAMETERS.csv` (this table's source) | `%s` |" % sha(PARAMS))
L.append("| `generator_v1_2/code/sim_v1_2.py` (inherited code) | `%s` |" %
         sha(SYNTH / "generator_v1_2" / "code" / "sim_v1_2.py"))
L.append("| `generator_v1_2/results/synthetic_panel_v1_2.csv` (c6 reference) | `%s` |" %
         sha(SYNTH / "generator_v1_2" / "results" / "synthetic_panel_v1_2.csv"))
L.append("| `IMPLEMENTATION_NOTE.md` (spec-gap resolutions, pre-run) | `%s` |" %
         sha(ROOT13 / "IMPLEMENTATION_NOTE.md"))
L.append("")
L.append("## 1. The demand equation (frozen, PRE_DECLARATIONS.md §4)\n")
L.append("```")
L.append("p_{i,c,g,q,t} = sigma( a_g + b_Z ln R_{c,g,t} + b_V ln(1+V_{c,g}) + b_D ln(1+Delta-pi_{c,g,t})")
L.append("                       + b_y ln(y_{c,q,t}/ybar_{c,t}) - b_F ln(1 + s_{c,g}/(y_{c,q,t}/ybar_{c,t})) )")
L.append("D_{c,g,t}   = sum_q omega_q p_{c,g,q,t}          omega_q = 0.2 (equal quintile weights)")
L.append("S_{c,g,t}   = D_{c,g,t} * s_c                     (declared fee units = shares of mean monthly")
L.append("                                                   household income; no currency conversion exists)")
L.append("D*_{c,t}    = sum_{g in g1,g2,g3} nu_{c,g} D_{c,g,t}   (cohort incidence; g0 never enters)")
L.append("Pi_{c,g,t}  = (1-D) pi0 + D pi1                   |Pi - pi0| <= delta_g (1 - pi0)")
L.append("R_{c,g,t}   = (1+Q)^0.40 (1/pi0)^0.40 kappa^0.20   clipped [1,20]")
L.append("V_{c,g}     = phi_c r_EAP DeltaS_g H  (g1-g3);  V_{c,g4} = phi_c G_c H;  V_{c,g0} = 0")
L.append("Delta-pi    = pi1 - pi0 = delta_g (1 - pi0),  pi1 = min(0.999, pi0 + delta_g (1-pi0))")
L.append("```")
L.append("")
L.append("**One behavioural rule for every country.** There is no country-specific value of `a_g, b_Z, "
         "b_V, b_D, b_y, b_F, delta_g` anywhere in the code; `c4c` audits the behavioural functions for "
         "exactly that. Country variation enters only through `phi, s, sigma, nu` (§3 below).\n")
L.append("## 2. The 42 declared rows (verbatim from `PARAMETERS.csv`)\n")
L.append("| id | symbol | meaning | value / range | unit | provenance | evidence file:line | enters | notes |")
L.append("|---|---|---|---|---|---|---|---|---|")
for r in rows:
    L.append("| %s | `%s` | %s | %s | %s | %s | %s | %s | %s |" % (
        r["id"], r["symbol"], r["meaning"], r["value_or_range"], r["unit"],
        r["provenance_label"], r["evidence_file_line"], r["enters_equation"], r["notes"]))
L.append("")
L.append("## 3. Country input bundles (the ONLY country-varying quantities)\n")
L.append("| input | SYN_HKG_LIKE | SYN_PHL_LIKE | SYN_KHM_LIKE | label |")
L.append("|---|---|---|---|---|")
L.append("| `phi_c` = 1 − vulnerable employment (2019) | 0.940 | 0.677 | 0.464 | OBSERVED (WDI/ILO), DECLARED interpretation |")
L.append("| fee share `s_c` of mean monthly household income | 0.0305 | 0.0400 | 0.0210 | DERIVED / DECLARED / DERIVED |")
L.append("| income dispersion `sigma_c` | 0.55 | 0.80 | 0.75 | DECLARED (no Gini series on disk) |")
L.append("| cohort weights `nu_{c,1}, nu_{c,2}, nu_{c,3}` | 0.10, 0.62, 0.22 (0.94) | 0.30, 0.35, 0.10 (0.75) | 0.28, 0.13, 0.02 (0.43) | DERIVED from observed UIS out-of-school + DECLARED split |")
L.append("| observed out-of-school at upper-secondary age (2020) | 5.428% | 24.737% | 56.987% | OBSERVED (UIS SDG4) |")
L.append("")
L.append("## 4. Host mapping (which v1.2 country carries which declared bundle)\n")
L.append("The frozen v1.2 generator contains no HKG-like and no KHM-like country, so the shadow block is "
         "layered on the gate state of three designated v1.2 countries. The rule is **shadow-blind** "
         "(it reads 2020 GDP per capita, which is not an argument of the demand equation) and is fixed in "
         "`IMPLEMENTATION_NOTE.md` §1 before any shadow output exists:\n")
L.append("| declared type | host | rule |")
L.append("|---|---|---|")
L.append("| `SYN_PHL_LIKE` | `SYN00_PHL_LIKE` | v1.2's own declared PHL-informed country |")
L.append("| `SYN_HKG_LIKE` | the country with the highest 2020 `gdppc` | HKG is the high-income system |")
L.append("| `SYN_KHM_LIKE` | the country with the lowest 2020 `gdppc` | KHM is the poorest system |")
L.append("")
L.append("Resolved names are written to `results/shadow_country_inputs_audit.csv` and `RUN_MANIFEST.json`. "
         "No v1.2 parameter, path, draw or arithmetic is altered by this mapping; the host country is "
         "generated by the frozen v1.2 code exactly as delivered.\n")
L.append("## 5. Inherited v1.2 parameters read by the gate-state extractor (unchanged)\n")
L.append("Read-only, never re-fitted: `phys_cap = 1.15`, `overage_cap = 1.05`, `rank_gain = 0.20`, "
         "`seek = (0.15,0.35,0.60,0.80)`, `queue_retain = 0.50`, `sep = (0.10,0.07,0.05,0.04)`, "
         "`rung_mult = (2.20,3.20,4.60,6.40)`, `cred_prem = 0.10`, `psi = (0.02,0.22,0.12)`. The gate "
         "contract is `IMPLEMENTATION_NOTE.md` §2; `generator_v1_2/PARAMS.md` is the authoritative v1.2 "
         "table and is not reproduced here.\n")
L.append("## 6. Freeze declaration\n")
L.append("These values were frozen by `shadow_module/PRE_DECLARATIONS.md` before any v1.3 run. This "
         "worker changed none of them. The central-value run is the scored run; the pre-declared "
         "one-at-a-time sensitivity grid is reported beside it and cannot replace it. A FAIL is reported "
         "as a FAIL and is never rescued by re-parameterising.\n")
L.append("Seed `20261120` (PCG64, inherited from v1.2); floats `%.10g`; two clean runs byte-identical.\n")

(ROOT13 / "PARAMS.md").write_text("\n".join(L) + "\n")
print("wrote PARAMS.md (%d lines), sha256 = %s" % (len(L) + 1, sha(ROOT13 / "PARAMS.md")))
