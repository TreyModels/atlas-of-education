#!/usr/bin/env python3
"""Self-contained regression tests for Neon's three named masseng-tutoring defects.

Covers, on the coupled PHL v5 R1 run (SIMULATION; no empirical or causal claim):
  1. ``_record()`` spend double-count when ``spend_feedback=False`` -- household spending is now two
     single-counted flows (fitted direct schedule + declared tutoring outlay); the reported total is
     schedule + outlay in the financing arm and schedule only in the learning-only arm, and the inclusive
     total is always exactly the sum of the two flows once;
  2. the OPEN MNL price/option mismatch vs the Bray reality check -- the two mappings are declared in the
     module and ``bray_mapping_gap()`` measures the gap (claim text unchanged);
  3. the ``1940-2024`` window label -- the simulation window, the observed-data window and the fit windows
     are declared and checked against the PHL config and the loaded WDI series; the record text is checked
     to say "simulated 1940-2024, observed data ..." rather than calling 1940-2024 the data window.

Run from anywhere (the model package imports scipy through ``masseng.data``):
    python3 tests/test_tutoring_fixes.py [--model-dir DIR]
The model dir defaults to the repo's ``research/masseng-v6/model`` and can be overridden with
``MASSENG_MODEL_DIR``/``--model-dir`` (used for the fail-on-base comparison against b9d68c1).
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(RECORD)))


def _arg(argv, flag, default):
    for i, a in enumerate(argv):
        if a == flag and i + 1 < len(argv):
            return os.path.abspath(argv[i + 1])
    return default


MODEL = _arg(sys.argv[1:], "--model-dir", os.environ.get("MASSENG_MODEL_DIR") or
             os.path.join(REPO, "research", "masseng-v6", "model"))
os.environ["MASSENG_MODEL_DIR"] = MODEL
sys.path.insert(0, MODEL)
for _mod in [m for m in list(sys.modules) if m.startswith("masseng")]:
    del sys.modules[_mod]

CASES = []


def check(name, ok, detail):
    CASES.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + " :: " + detail)


def _finite(x):
    try:
        return bool(np.isfinite(float(x)))
    except (TypeError, ValueError):
        return False


# ------------------------------------------------------------------ 1. single-counted household spending
from masseng.data import Country  # noqa: E402
from masseng.tutoring import TutoringModel5, TutoringParams  # noqa: E402

country = Country("PHL")
fit = json.load(open(os.path.join(MODEL, "outputs", "PHL", "v5", "fit_R1.json")))["params"]
anchor = TutoringParams()

wanted = ("edu_share_hh", "edu_share_hh_incl_tut", "spend_school_share_gdp", "tut_spend_share_gdp",
          "spend_total_share_gdp", "spend_incl_share_gdp")
missing = []
runs = {}
for feedback in (True, False):
    m = TutoringModel5(country, fit, spec="R1", switches={"tutoring": True},
                       tut_params=replace(anchor, spend_feedback=feedback))
    res = m.run()
    missing += [k for k in wanted if k not in res.ind]
    runs[feedback] = (m, res)

all_years = list(runs[True][0].years)
years = [y for y in (2010, 2024) if y in all_years]
if missing:
    check("S1 single-count decomposition outputs exist", False, f"missing output keys: {sorted(set(missing))}")
else:
    cons_share = float(runs[True][0].cons_share)
    rows = []
    ok = True
    for feedback, (m, res) in runs.items():
        for y in years:
            yi = all_years.index(y)
            sch = float(res.ind["spend_school_share_gdp"][yi])
            tut = float(res.ind["tut_spend_share_gdp"][yi])
            tot = float(res.ind["spend_total_share_gdp"][yi])
            incl = float(res.ind["spend_incl_share_gdp"][yi])
            edu = float(res.ind["edu_share_hh"][yi])
            edu_incl = float(res.ind["edu_share_hh_incl_tut"][yi])
            # (i) the inclusive total is exactly the two single-counted flows, once each
            ok &= _finite(sch) and _finite(tut) and _finite(incl) and abs(incl - (sch + tut)) < 1e-9
            # (ii) the reported total follows the declared arm: financing = +outlay once, learning-only = schedule
            ok &= abs(tot - (incl if feedback else sch)) < 1e-9
            # (iii) the reported share uses the arm's total; the inclusive indicator always uses both flows
            ok &= abs(edu - tot / cons_share) < 1e-9
            ok &= abs(edu_incl - incl / cons_share) < 1e-9
            # (iv) learning-only arm: outlay is reported separately and NOT added to edu_share_hh
            if not feedback:
                ok &= tut > 0 and abs(edu - edu_incl) > 0
            else:
                ok &= abs(edu - edu_incl) < 1e-12
            rows.append(f"fb={feedback} {y}: school={sch:.4f} tut={tut:.4f} total={tot:.4f} "
                        f"incl={incl:.4f} edu={edu:.4f} incl_edu={edu_incl:.4f}")
    check("S1 spend single-count: incl == school + tutoring once; reported total follows spend_feedback arm",
          ok, " | ".join(rows))

# ------------------------------------------------------------------ 2. MNL price/option mismatch vs Bray (OPEN, explicit)
try:
    from masseng.tutoring import BRAY_CHECK_MAPPING, PORT_MAPPING, bray_mapping_gap  # noqa: E402
    gap = bray_mapping_gap(anchor, fee=1.0)
    ok = (BRAY_CHECK_MAPPING["options"] == ("none", "own", "other")
          and BRAY_CHECK_MAPPING["commercial_option"] is False
          and abs(BRAY_CHECK_MAPPING["other_price_coef"] - 0.5) < 1e-12
          and PORT_MAPPING["options"] == ("none", "own", "other", "commercial")
          and PORT_MAPPING["commercial_option"] is True
          and abs(gap["own_gap"]) < 1e-15
          and abs(gap["other_gap"] - (-0.30)) < 1e-12
          and abs(bray_mapping_gap(anchor, fee=2.0)["other_gap"] - (-0.60)) < 1e-12)
    check("S2 MNL vs Bray mapping is declared and measured (OPEN deviation, claim unchanged)", ok,
          f"other_price_coef fit=0.5 port=0.8, other_gap(fee=1)={gap['other_gap']:+.4f} logit, "
          f"commercial option fit=False port=True")
except ImportError as exc:
    check("S2 MNL vs Bray mapping is declared and measured (OPEN deviation, claim unchanged)", False,
          f"missing declared mapping objects: {exc}")

# ------------------------------------------------------------------ 3. window labels: simulated vs observed data
try:
    from masseng.tutoring import SIMULATED_WINDOW, OBSERVED_DATA_WINDOW, FIT_WINDOWS  # noqa: E402
    cfg = country.config
    v5y = cfg["v5"]["years"]
    wdi = json.load(open(os.path.join(MODEL, "countries", "PHL", "wdi_series.json")))
    macro = ("NY.GDP.PCAP.KD", "SP.POP.TOTL", "SP.DYN.CBRT.IN", "SH.DYN.MORT")
    edu = ("SE.PRM.ENRR", "SE.SEC.ENRR", "SE.TER.ENRR", "SE.PRM.PRIV.ZS")
    span = {}
    for code in macro + edu + ("SI.POV.GINI",):
        yrs = sorted(int(k) for k in wdi[code] if str(k).lstrip("-").isdigit())
        span[code] = (yrs[0], yrs[-1])
    macro_min = min(span[c][0] for c in macro)
    edu_min = min(span[c][0] for c in edu)
    raw_max = max(span[c][1] for c in span)
    doc = open(os.path.join(RECORD, "MASSENG_TUTORING_COUPLING.md")).read()
    ok = (SIMULATED_WINDOW == (v5y["simulate_from"], v5y["simulate_to"])
          and FIT_WINDOWS["train"] == tuple(cfg["years"]["train"])
          and FIT_WINDOWS["test"] == tuple(cfg["years"]["test"])
          and OBSERVED_DATA_WINDOW[0] == macro_min
          and edu_min == 1971
          and raw_max >= OBSERVED_DATA_WINDOW[1]
          and "simulates 1940" in doc and "observed data window" in doc
          and "(1940–2024), fitted" not in doc)
    check("S3 window labels: simulation 1940-2024 vs observed data 1960-2024 vs fit 1971-1995/1996-2024", ok,
          f"sim={SIMULATED_WINDOW}, observed=({macro_min},{OBSERVED_DATA_WINDOW[1]}), education_series_from={edu_min}, "
          f"fit={FIT_WINDOWS}, raw_series_max={raw_max}, record_label_ok={('(1940–2024), fitted' not in doc)}")
except ImportError as exc:
    check("S3 window labels: simulation 1940-2024 vs observed data 1960-2024 vs fit 1971-1995/1996-2024", False,
          f"missing declared window labels: {exc}")

n_pass = sum(1 for _, ok, _ in CASES if ok)
print(f"\nSUMMARY: {n_pass}/{len(CASES)} PASS (model dir: {MODEL})")
raise SystemExit(0 if n_pass == len(CASES) else 1)
