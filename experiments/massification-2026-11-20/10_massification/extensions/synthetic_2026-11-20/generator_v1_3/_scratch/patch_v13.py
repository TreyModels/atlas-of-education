#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build code/sim_v1_3.py = frozen v1.2 code + the shadow block (named patches).

Every patch is an exact-string replacement against the frozen v1.2 source and is
asserted to occur exactly once. Nothing else in the v1.2 code is touched, which is what
makes c6 (byte-identity with the block off) a meaningful check rather than a formality.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT13 = HERE.parent
SYNTH = ROOT13.parent
V12 = SYNTH / "generator_v1_2" / "code" / "sim_v1_2.py"
OUT = ROOT13 / "code" / "sim_v1_3.py"

src = V12.read_text()
core = (HERE / "shadow_core.py").read_text()
tail = (HERE / "tail_v13.py").read_text()

DOCSTRING = '''SIM_V1_3 -- SYNTHETIC generator v1.3: v1.2 + SHADOW EDUCATION AT THE GATES.

EVERYTHING THIS SCRIPT EMITS IS SYNTHETIC. It is a declared-assumption simulator: not an
estimate, not evidence about any country, not a forecast, and it licenses no causal or
direction claim. Country labels are synthetic ("SYN28", "SYN00_PHL_LIKE", ...); no real
country is modelled or measured.

Implements, on top of the frozen v1.2 generator (code/sim_v1_2.py, unchanged arithmetic),
the FROZEN shadow-module specification in shadow_module/PRE_DECLARATIONS.md (sha256
cf8c61cb...) and its binding controller note PRE_DECLARATIONS_S1_NOTE.md (sha256
af49a616...):

  * household tutoring demand at a gate, ONE behavioural rule for every country
    (a_g, b_Z, b_V, b_D, b_y, b_F, delta_g), country variation only through the declared
    input bundle (phi, s, sigma, nu);
  * gate pressure R built mechanically from v1.2's own queue/transition/rank state;
  * V the positional credential value; Delta-pi = delta_g (1 - pi0);
  * feedback: Pi replaces pi0 as the realised advance rate, one-year lag, bounded
    |Pi - pi0| <= delta_g (1 - pi0), touching nothing else in v1.2;
  * no passive "neither" sink (v1.2's out-of-school => work default is inherited);
  * g0 is the structural near-zero control, never scored as a gate, never in D*.

Frozen checks c1-c6 are scored exactly as PRE_DECLARATIONS.md sec.8 states. A FAIL is
reported as a FAIL; no parameter or threshold is ever adjusted to rescue one.

Determinism: one numpy PCG64 stream, seed 20261120 (inherited from v1.2), v1.2 draw order,
shadow block draws nothing, floats written at %.10g. Two clean runs into separate output
directories are byte-identical.

REFUSES TO RUN if the frozen shadow predeclaration, the S1 note, the inherited v1.2
predeclaration, the local verbatim copy, or PARAMS.md no longer match their frozen hashes.

Usage:  python sim_v1_3.py [--out DIR] [--manifest FILE] [--smoke] [--no-sensitivity]
"""
'''

PATHS = '''ROOT = Path(__file__).resolve().parent.parent   # generator_v1_3/
CODE = Path(__file__).resolve()
SYNTH = ROOT.parent                             # synthetic_2026-11-20/
V12_DIR = SYNTH / "generator_v1_2"              # frozen v1.2 (read-only)
PREDECL = SYNTH / "v1_2" / "PRE_DECLARATIONS.md"          # frozen v1.2 spec (inherited)
SHADOW_DIR = SYNTH / "shadow_module"                      # frozen v1.3 spec (read-only)
SHADOW_PREDECL = SHADOW_DIR / "PRE_DECLARATIONS.md"
SHADOW_S1 = SHADOW_DIR / "PRE_DECLARATIONS_S1_NOTE.md"
LOCAL_PREDECL = ROOT / "PRE_DECLARATIONS.md"              # verbatim copy of both
PARAMS_MD = ROOT / "PARAMS.md"
V12_PANEL = V12_DIR / "results" / "synthetic_panel_v1_2.csv"
MASS = ROOT.parents[2]                          # 10_massification/
PROG = ROOT.parents[3]                          # massification-2026-11-20/
DATA = MASS / "data"
ECI_PATH = PROG / "09_relations" / "data" / "economic_complexity_panel_30ctys.csv"

# sha256 of v1_2/PRE_DECLARATIONS.md at freeze time (2026-11-20). If the file changes,
# the code refuses to run: the predeclaration is not edited after results are seen.
EXPECTED_PREDECL_SHA = "fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16"

# sha256 of the FROZEN v1.3 shadow spec and its binding controller note. These are the
# values recorded when the module was frozen, before any v1.3 run. A mismatch refuses.
EXPECTED_SHADOW_PREDECL_SHA = "cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2"
EXPECTED_SHADOW_S1_SHA = "af49a616a7b57c4ef23a693c155d022cd17817f66f5acafba4dc6798dedb65eb"

# sha256 of PARAMS.md (the declared parameter table delivered with this module). Frozen
# before the scored run; DRY_RUN_PLAN.md sec.1.4 requires the run to re-hash it.
EXPECTED_PARAMS_SHA = "__PARAMS_SHA__"
'''

import hashlib as _hl
_params = ROOT13 / "PARAMS.md"
if _params.exists():
    PATHS = PATHS.replace("__PARAMS_SHA__", _hl.sha256(_params.read_bytes()).hexdigest())
else:
    PATHS = PATHS.replace("__PARAMS_SHA__", "PARAMS_MISSING")

OUT_DICT_OLD = '''        w_for=np.zeros((4, T)), g=np.zeros(T), yos=np.zeros(T), att=np.zeros((NL, T)),
        public_ptr=np.zeros(T),
    )'''
OUT_DICT_NEW = '''        w_for=np.zeros((4, T)), g=np.zeros(T), yos=np.zeros(T), att=np.zeros((NL, T)),
        public_ptr=np.zeros(T),
        # ---- v1.3 shadow block stores (diagnostics/state; no v1.2 quantity above changes)
        hires=np.zeros((4, T)),
        D_sh=np.zeros((5, T)), S_sh=np.zeros((5, T)), R_sh=np.zeros((5, T)),
        Q_sh=np.zeros((5, T)), pi0_sh=np.zeros((5, T)), pi1_sh=np.zeros((5, T)),
        Pi_sh=np.zeros((5, T)), kappa_sh=np.zeros((5, T)), V_sh=np.zeros((5, T)),
        dpi_sh=np.zeros((5, T)), ratio_sh=np.ones((5, T)), p_sh=np.zeros((5, 5, T)),
        cand_sh=np.zeros((5, T)), cap_sh=np.zeros((5, T)), adv_sh=np.zeros((5, T)),
    )'''

POOL_OLD = '''        # ---- pools (pipeline eligibility for next levels) -------------------------
        for L in range(1, NL):
            newpool = out["grads"][L - 1, t] + P["pool_retain"] * pools[L]
            pools[L] = min(newpool, 1.05 * C[L, t])'''
POOL_NEW = '''        # ---- pools (pipeline eligibility for next levels) -------------------------
        # v1.3 (frozen spec sec.5, DRY_RUN_PLAN sec.1.2): the realised advance rate Pi
        # replaces pi0 for the ONE-YEAR-LAGGED pool, and nothing else. With the shadow
        # block off, pool_mult == 1.0 exactly and this line is arithmetically v1.2's.
        for L in range(1, NL):
            pool_mult = float(ratio_prev[L]) if sh_in is not None else 1.0
            newpool = out["grads"][L - 1, t] * pool_mult + P["pool_retain"] * pools[L]
            pools[L] = min(newpool, 1.05 * C[L, t])'''

SHADOW_CALL = '''        # ---- shadow block (H4): household tutoring demand at the gates --------------
        # Frozen equation, frozen parameters, declared country inputs. Pure: reads state,
        # writes only the shadow stores. No RNG, no v1.2 parameter, no v1.2 state.
        if sh_in is not None:
            cap_c = [min(P["phys_cap"] * seats[L], P["overage_cap"] * C[L, t])
                     for L in range(NL)]
            gate_gs = gate_state(C[:, t], cap_c, out["grads"][:, t], out["enrol"][:, t],
                                 rf, qr, vac, hires, beh)
            sb = shadow_block(beh, sh_in, gate_gs, w_for, w_inf)
            # NOTE: loop names must not shadow v1.2 locals (g = growth rate, q = congestion,
            # gs = sector growth). Renamed deliberately; see TUNE_LOG.md D3.
            for gg in GATES:
                out["D_sh"][gg, t] = sb[gg]["D"]
                out["S_sh"][gg, t] = sb[gg]["S"]
                out["R_sh"][gg, t] = sb[gg]["R"]
                out["Q_sh"][gg, t] = sb[gg]["Q"]
                out["pi0_sh"][gg, t] = sb[gg]["pi0"]
                out["pi1_sh"][gg, t] = sb[gg]["pi1"]
                out["Pi_sh"][gg, t] = sb[gg]["Pi"]
                out["kappa_sh"][gg, t] = sb[gg]["kappa"]
                out["V_sh"][gg, t] = sb[gg]["V"]
                out["dpi_sh"][gg, t] = sb[gg]["dpi"]
                out["ratio_sh"][gg, t] = sb[gg]["ratio"]
                out["cand_sh"][gg, t] = sb[gg]["candidates"]
                out["cap_sh"][gg, t] = sb[gg]["capacity"]
                out["adv_sh"][gg, t] = sb[gg]["advances"]
                for qq in range(5):
                    out["p_sh"][gg, qq, t] = sb[gg]["ps"][qq]
            ratio_prev = out["ratio_sh"][:, t].copy()

'''


def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, "expected %d occurrence(s), found %d for:\n%s" % (count, n, old[:200])
    src = src.replace(old, new)


# ---- R0: imports (csv at module level; v1.2 imports it locally in two functions) ------
rep("import argparse\nimport hashlib", "import argparse\nimport csv\nimport hashlib")

# ---- R1: docstring -------------------------------------------------------------------
parts = src.split('"""')
assert len(parts) >= 3
_doc = DOCSTRING.rstrip()
if _doc.endswith('"""'):
    _doc = _doc[:-3].rstrip()
src = parts[0] + '"""' + _doc + '\n"""' + '"""'.join(parts[2:])

# ---- R2: paths + frozen hashes --------------------------------------------------------
old_paths = src[src.index("ROOT = Path(__file__)"):src.index('EXPECTED_PREDECL_SHA = "fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16"') + len(
    'EXPECTED_PREDECL_SHA = "fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16"')]
src = src.replace(old_paths, PATHS.rstrip("\n"))

# ---- R3: shadow core after sha256_file ------------------------------------------------
anchor = '''def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
'''
rep(anchor, anchor + "\n\n" + core.strip("\n") + "\n")

# ---- R4: simulate_country signature ---------------------------------------------------
rep("def simulate_country(cp, gnoise, hhnoise, S_path, Pop_path):",
    "def simulate_country(cp, gnoise, hhnoise, S_path, Pop_path, sh_in=None, beh=None):")

# ---- R4b: local beh default + ratio_prev initial state --------------------------------
rep("""    gp = np.array(P["gp"])
    cap = cp["cap0"]""",
    """    gp = np.array(P["gp"])
    cap = cp["cap0"]
    beh = SHADOW_BEHAV if beh is None else beh
    ratio_prev = np.ones(5)          # v1.3: Pi/pi0 carried to the next year's pool (lag 1)""")

# ---- R5: shadow stores in out ---------------------------------------------------------
rep(OUT_DICT_OLD, OUT_DICT_NEW)

# ---- R6: pool update with the lagged realised advance rate ---------------------------
rep(POOL_OLD, POOL_NEW)

# ---- R7: store hires (needed by the g4 gate state; diagnostic only) ------------------
rep('        out["rankf"][:, t] = rf; out["w_inf"][t] = w_inf; out["w_for"][:, t] = w_for',
    '        out["rankf"][:, t] = rf; out["w_inf"][t] = w_inf; out["w_for"][:, t] = w_for\n'
    '        out["hires"][:, t] = hires')

# ---- R8: shadow block before the store ------------------------------------------------
rep("        # ---- store -----------------------------------------------------------------",
    SHADOW_CALL + "        # ---- store -----------------------------------------------------------------")

# ---- R9: keep the declared inputs with the run ----------------------------------------
rep("""    out["cp"] = cp
    out["S"] = S_path""",
    """    out["cp"] = cp
    out["shadow_in"] = sh_in
    out["beh"] = beh
    out["S"] = S_path""")

# ---- R10: replace section 9 (run + main) with the v1.3 run/checks/outputs -------------
marker = ("# ======================================================================================\n"
          "# 9. RUN + MAIN\n")
i = src.index(marker)
src = src[:i] + tail.strip("\n") + "\n"

OUT.write_text(src)
print("wrote %s (%d lines)" % (OUT, src.count("\n") + 1))
