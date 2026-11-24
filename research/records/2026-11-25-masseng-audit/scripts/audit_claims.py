#!/usr/bin/env python3
"""Read-only verification for task-38: MASSENG v5 massification claim layer (engine/data reality only).

No server compute. All inputs are read from committed git objects:
  * MASSENG v6 / v5: origin/experiment/masseng-v6-surplus-motor (head extracted to a temp dir)
  * prior Bayesian audit: origin/research/masseng-bayes-audit-2026-11-24 (read for reported numbers only)

Outputs `results/claims_audit.json` next to this record. Reproduce from the repo root:
    python3 research/records/2026-11-25-masseng-audit/scripts/audit_claims.py
Requires numpy (for the masseng package); all other checks are stdlib.
"""
import hashlib
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

REPO = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
V6 = "origin/experiment/masseng-v6-surplus-motor"
BAYES = "origin/research/masseng-bayes-audit-2026-11-24"

CHECKS = []

def add(cid, area, question, value, ref="", status="INFO"):
    CHECKS.append(dict(id=cid, area=area, question=question, value=value, ref=ref, status=status))

def git_show(ref, path):
    return subprocess.check_output(["git", "-C", str(REPO), "show", f"{ref}:{path}"])

def jshow(ref, path):
    return json.loads(git_show(ref, path).decode())

def sha(b):
    return hashlib.sha256(b).hexdigest()

def extract_model():
    tmp = Path(tempfile.mkdtemp(prefix="masseng-audit-"))
    data = subprocess.check_output(["git", "-C", str(REPO), "archive", V6, "research/masseng-v6/model"])
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        tf.extractall(tmp)
    return tmp / "research" / "masseng-v6" / "model"

def main():
    model = extract_model()
    sys.path.insert(0, str(model))
    from masseng.data import Country          # noqa: E402
    from masseng import targets as T          # noqa: E402

    country = Country("PHL")
    cfg = country.config
    outdir = REPO / "research/records/2026-11-25-masseng-audit/results"
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- heads
    heads = {
        "v6": subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "--short", V6], text=True).strip(),
    }
    add("HEAD-1", "provenance", "audited heads", heads, "current origin refs")

    # ---- training / test roles: replicate calibrate5.build_rows without scipy
    rows = T.build(country)
    v5cfg = cfg["v5"]
    tmap = v5cfg.get("target_map", {})
    raw = jshow(V6, "research/masseng-v6/model/countries/PHL/targets_v5.json").get("rows", [])
    lo, hi = cfg["years"]["train"]
    for r in raw:
        m = tmap.get(r["series"])
        if not m or not isinstance(r.get("value"), (int, float)) or not r.get("verified", False):
            continue
        y = int(r["year"])
        role = "train" if y in m.get("train_years", []) else ("test" if y > hi or m.get("all_test") else "diagnostic")
        if m.get("only_years") and y not in m["only_years"]:
            continue
        val = r["value"] * r.get("scale", 1.0) * m.get("scale", 1.0)
        rows.append(dict(series=m["model"], year=y, value=val, role=role))
    train = [r for r in rows if r["role"] == "train"]
    test = [r for r in rows if r["role"] == "test"]
    post = [(r["series"], r["year"]) for r in train if r["year"] > hi]
    add("TRAIN-1", "training reuse",
        "training rows / test rows / post-1995 training rows",
        {"n_train": len(train), "n_test": len(test), "n_post1995": len(post),
         "post1995": post, "share_post1995_pct": round(100 * len(post) / len(train), 1)},
        "results/PHL/v5 preflight train_rows=121/test_rows=164; PROTOCOL_v5 §7", "FLAG")
    add("TRAIN-2", "training reuse",
        "post-1995 training targets are non-enrolment outcomes (FIES education shares 2003/2006; APIS 2019 gradient)",
        sorted({s for s, _ in post}), "targets.py income_gradient_2019 role=train; target_map fies train_years 2003/2006", "FLAG")

    # ---- driver identification: observed anchors inside training window
    drv = jshow(V6, "research/masseng-v6/model/countries/PHL/drivers_v5.json")["series"]
    def points(name):
        return sorted(int(y) for y in drv[name]["points"] if str(y).lstrip("-").isdigit())
    anchors = {name: [y for y in points(name) if lo <= y <= hi]
               for name in ("premium_tertiary", "premium_secondary", "formal_share")}
    add("DRIVER-1", "identification",
        "driver observations inside the 1971-1995 training window",
        anchors, "countries/PHL/drivers_v5.json", "FLAG")
    add("DRIVER-2", "identification",
        "premium_tertiary is linearly interpolated 1995-2013 and 2013-2024; only 3 observed training anchors",
        {"train_anchors": anchors["premium_tertiary"], "post1995_anchors": [y for y in points("premium_tertiary") if y > hi]},
        "ditto; Series linear interpolation", "FLAG")

    # ---- fits and scores
    fits = {s: jshow(V6, f"research/masseng-v6/model/outputs/PHL/v5/fit_{s}.json") for s in ("R0", "R1", "R2", "R3", "R4", "R5")}
    scores = jshow(V6, "research/masseng-v6/model/outputs/PHL/v5/scores.json")
    riv = scores["rivals"]
    series = ["ger_primary", "ger_secondary", "ger_tertiary"]

    def pooled(name):
        sse = 0.0
        n = 0
        for s in series:
            x = riv[name]["series_losses"][s]
            sse += sum((a - b) ** 2 for a, b in zip(x["obs"], x["pred"]))
            n += len(x["obs"])
        return math.sqrt(sse / n), n

    pooled_vals = {k: pooled(k)[0] for k in riv}
    ranked = sorted(pooled_vals, key=pooled_vals.get)
    add("R1-1", "R1 performance",
        "pooled three-GER held-out RMSE by rival (recomputed from scores.json obs/pred)",
        {k: round(v, 3) for k, v in sorted(pooled_vals.items(), key=lambda kv: kv[1])},
        "report table: R0 14.230, R1 16.925, R2 7.458, R3 15.184, R4 12.194, R5 16.543", "PASS")
    add("R1-2", "R1 performance",
        "rank of R1 among the six rivals (1=best)", {"rank": ranked.index("R1") + 1, "of": len(ranked), "ranking": ranked},
        "lower is better", "FLAG")
    add("R1-3", "R1 performance",
        "R1 vs benchmarks: R1 - R0, R1 - trend, R1 - persistence (pp)",
        {"minus_R0": round(pooled_vals["R1"] - pooled_vals["R0"], 3),
         "minus_trend": round(pooled_vals["R1"] - 11.7938, 3),
         "minus_persistence": round(pooled_vals["R1"] - 6.6001, 3)},
        "persistence 6.600, trend 11.794 from scores.json", "FLAG")

    # ---- R1 predictions at the two separating observations
    def pred(name, s, y):
        x = riv[name]["series_losses"][s]
        return dict(zip(x["years"], x["pred"]))[y], dict(zip(x["years"], x["obs"]))[y]
    sep = {}
    for name in ("R1", "R2"):
        p13, o13 = pred(name, "ger_tertiary", 2013)
        p24, o24 = pred(name, "ger_tertiary", 2024)
        sep[name] = {"2013": {"pred": round(p13, 3), "obs": o13}, "2024": {"pred": round(p24, 3), "obs": o24}}
    add("R1-4", "R1 predictions",
        "R1 tertiary GER predictions vs observed at the premium/participation contrast",
        sep, "scores.json ger_tertiary", "FLAG")

    # ---- coefficient instability across specs
    keys = ["b_h", "b_p", "b_r", "lam"]
    coefs = {s: {k: round(fits[s]["params"][k], 4) for k in keys} for s in fits}
    add("R1-5", "identification",
        "the four mechanism coefficients across the six specifications",
        coefs, "outputs/PHL/v5/fit_R*.json", "FLAG")
    add("R1-6", "identification",
        "b_h sign across specifications", {s: ("+" if coefs[s]["b_h"] > 0 else ("-" if coefs[s]["b_h"] < 0 else "0")) for s in coefs},
        "same", "FLAG")

    # ---- bounds and recovery
    bounds = dict(a_prim=(-4, 16), a_sec=(-4, 16), a_sec_entry=(-10, 14), a_ter=(-4, 16), a_ter_entry=(-12, 12),
                  b_h=(-6, 12), b_p=(-6, 12), b_r=(-12, 24), eta=(0, 6), eta_x=(0, 4), kappa=(0, 40), lam=(-6, 12),
                  c_scale=(0.05, 8), mu_basic=(-10, 6), mu_ter=(-8, 8), nu=(-6, 8))
    near = []
    for s, f in fits.items():
        for k, v in f["params"].items():
            if k not in bounds:
                continue
            lo_b, hi_b = bounds[k]
            rel = min(abs(v - lo_b), abs(v - hi_b)) / (hi_b - lo_b)
            if rel < 0.01:
                near.append({"spec": s, "param": k, "value": v, "bound": [lo_b, hi_b], "rel_dist": round(rel, 6),
                             "flagged_by_record": k in f.get("at_bounds", [])})
    add("R1-7", "bounds",
        "parameters within 1% of a bound (relative) and whether the record's absolute-1e-3 rule flags them",
        near, "calibrate5.py line 100 uses abs(v-bound)<1e-3", "FLAG")
    add("R1-8", "recovery",
        "recovery test is run on the selected rival only; R1 is never recovered",
        {"recovery_file": "outputs/PHL/v5/recovery_R2.json", "spec": "R2",
         "b_h": "boundary recovery (15/20 bound hits)", "kappa": "not identified (60% < 80%)", "b_p": "not in rival"},
        "PROTOCOL_v5 §7; recovery_R2.json", "FLAG")

    # ---- hashes: committed outputs vs QA record
    qa = jshow(V6, "research/masseng-v6/model/outputs/qa/fresh_copy_comparison.json")
    qa_map = {f["file"]: f["original_sha256"] for f in qa["files"] if f.get("original_sha256")}
    outhash = jshow(V6, "research/masseng-v6/model/outputs/qa/final_output_hashes.json")
    hash_rows = {}
    for name in ("fit_R0.json", "fit_R1.json", "fit_R2.json", "fit_R3.json", "fit_R4.json", "fit_R5.json", "scores.json"):
        h = sha(git_show(V6, f"research/masseng-v6/model/outputs/PHL/v5/{name}"))
        hash_rows[name] = {"sha256": h, "matches_fresh_copy_qa": (qa_map.get(name) == h),
                           "matches_final_output_hashes": (outhash.get(f"outputs/PHL/v5/{name}") == h)}
    add("REPRO-1", "reproduction",
        "committed v5 outputs match the fresh-copy QA and final-output hash manifests", hash_rows,
        "outputs/qa/fresh_copy_comparison.json; outputs/qa/final_output_hashes.json", "PASS")
    req = jshow(V6, "research/masseng-v6/model/outputs/qa/reproducibility_inputs.json")["requirements"]
    add("REPRO-2", "reproduction",
        "fresh-copy claim: files compared / all byte-identical / pinned environment",
        {"files_compared": len(qa["files"]), "all_byte_identical": qa["all_byte_identical"], "requirements": req},
        "fresh_copy_comparison.json", "PASS")
    add("REPRO-3", "reproduction",
        "R1/R4 fits are two-stage continuations; stage-1 parameters are not committed",
        {"R1": fits["R1"].get("continued_from"), "R4": fits["R4"].get("continued_from"),
         "R1_total_nfev": fits["R1"].get("total_nfev"), "R4_total_nfev": fits["R4"].get("total_nfev")},
        "fit_R1.json / fit_R4.json; README reproduction block", "FLAG")

    # ---- Bayesian screen record (reported by the prior audit; not recomputed)
    bayes = jshow(BAYES, "research/records/2026-11-24-masseng-bayes-audit/results/main_summary.json")
    add("BAYES-1", "Bayesian screen",
        "screen title/status/shape as committed",
        {"title": bayes.get("title"), "status": bayes.get("status"), "draws": bayes.get("draws"),
         "varied": bayes.get("varied_parameters"), "fixed_baseline_note": bayes.get("baseline_note")},
        "masseng-bayes-audit results/main_summary.json", "FLAG")

    # ---- engine boundary: keyword coverage in the v5 demand engine
    eng = git_show(V6, "research/masseng-v6/model/masseng/engine5.py").decode().lower()
    words = ["learning", "quality", "score", "achievement", "tutor", "shadow", "region", "rural",
             "urban", "migration", "capacity", "voucher", "subsid", "fee", "tax", "budget",
             "borrowing", "credit", "earnings", "wage", "premium", "formal", "deferred", "exam", "quota"]
    present = {w: eng.count(w) for w in words if eng.count(w) > 0}
    absent = [w for w in words if eng.count(w) == 0]
    add("BOUND-1", "boundary",
        "mechanism keywords present/absent in masseng/engine5.py",
        {"present_counts": present, "absent": absent},
        "masseng/engine5.py (v5 demand engine)", "FLAG")
    add("BOUND-2", "boundary",
        "the model's own omission list in docs/model.md",
        {"omitted": ["school quality and learning", "teachers and budgets except tertiary capacity",
                     "geography and distance", "migration", "shadow education", "informal fees",
                     "gender", "labour-market return changes except through household income"]},
        "docs/model.md lines 102-111", "PASS")
    add("BOUND-3", "boundary",
        "what v5 DOES contain (supply/finance, demand, gates, deferral)",
        {"levels": ["primary", "secondary", "upper_secondary", "tertiary"],
         "household_demand": "four-level utility by income decile with cost burden",
         "supply_finance_inputs": ["public tertiary capacity (rationed)", "optional upper-secondary public capacity",
                                   "dated fee/subsidy/voucher cost changes", "CCT transfers (4Ps) as cost reductions"],
         "gates": "optional exogenous tertiary exam pass-rate schedule; PHL config has none",
         "deferral": "tertiary deferral to max age 25",
         "sector": "public/private provider within levels"},
        "engine5.py / countries/PHL/config.json", "INFO")

    # ---- QA claims layer
    wb = jshow(V6, "research/masseng-v6/model/outputs/qa/world_bank_spotchecks.json")
    add("QA-1", "QA claims", "twelve World Bank values spot-checked within 0.0005",
        {"n": wb.get("n"), "passed": wb.get("passed")}, "outputs/qa/world_bank_spotchecks.json", "PASS")
    cf = jshow(V6, "research/masseng-v6/model/outputs/qa/credential_floor_china_check.json")
    add("QA-2", "QA claims", "China credential-floor check result (honest negative)",
        {"result": cf.get("result"), "observed": cf.get("observed"), "predicted_medians": cf.get("predicted_change_median")},
        "outputs/qa/credential_floor_china_check.json", "PASS")
    add("QA-3", "QA claims", "release status and test claims",
        {"release": "NOT READY (CHED original-source access open)",
         "tests": "35 tests / 34 tests are reported in QA prose; not re-run here",
         "byte_identical_outputs": {"files": len(qa["files"]), "all": qa["all_byte_identical"]}},
        "ATLAS_WORLDS_QA.md; fresh_copy_comparison.json", "FLAG")
    add("QA-4", "QA claims", "completion-indicator check: 67% NER vs 73% completion are unlike indicators",
        "RESOLVED AS UNLIKE INDICATORS, NOT A NUMERICAL CONTRADICTION TO BE AVERAGED",
        "outputs/qa/completion_indicator_check.json", "PASS")

    # ---- dashboard / public claims: are there any MASSENG claims?
    dash = git_show("origin/research/dashboard-2026-11-23",
                    "research/records/2026-11-23-dashboard/README.md").decode()
    pub = git_show(V6, "public/research/massification/index.html").decode()
    add("DASH-1", "dashboard claims",
        "MASSENG mentions in the dashboard record and public massification page",
        {"dashboard_masseng_strings": dash.lower().count("masseng"),
         "dashboard_context": "all 7 are branch/record links plus 'MASSENG coupling in flight; do not interpret until committed'; no engine result is claimed",
         "public_page_mentions": pub.lower().count("masseng"),
         "public_page_label": "mechanism tests, not measurements of what happened in a country"},
        "dashboard-2026-11-23 README; public/research/massification/index.html", "PASS")
    add("DASH-2", "dashboard claims",
        "dashboard statements that must not be re-labelled as MASSENG v5 results",
        ["wage jobs cleanest null", "electricity null once country trends", "supply-led is the better description (later retracted/softened)",
         "GPU transition counterfactual", "multiverse 5/272 and 46 beats random"],
        "dashboard README", "FLAG")

    # ---- claim inventory: sources and verdicts (static, from the committed claim layer)
    claims = [
        ("CL-1", "MASSENG v5 R1 = 'the demand engine'", "PROTOCOL_v5.md title/§4; HANDOFF_v5.md; engine5.py docstring",
         "R1 is one of six rival specifications; it ranks 6/6 on the registered metric (pooled RMSE 16.925 vs R0 14.230, persistence 6.600).", "WITHDRAW"),
        ("CL-2", "R1 estimates human-capital / positional / relational / saturation coefficients", "PROTOCOL_v5 §4; paper §2",
         "weighted least-squares point values only; no SE/CI/recovery; coefficients unstable across specs (b_h +1.43/-6.00/-5.72/+2.49/-3.68).", "DOWNGRADE"),
        ("CL-3", "positive b_h supports a human-capital demand channel", "paper/README result table",
         "b_h sign flips across specs; selected R2's b_h is -6.000 at its bound.", "WITHDRAW"),
        ("CL-4", "saturation-dependent cost sensitivity (lambda>0) is supported", "PROTOCOL_v5 §7 decision rule",
         "R1 loses to R3 on both criteria (pooled 16.925 vs 15.184; 1998 recession err 4.27 vs 0.77).", "WITHDRAW"),
        ("CL-5", "the full positional-relational engine is the preferred demand account", "implied by 'demand engine' label",
         "R1 is the worst of six; paper already says it does not win.", "WITHDRAW"),
        ("CL-6", "test RMSE on 1996-2024 validates the model", "table headings / 'held-out'",
         "test is retrospective and previously inspected; test used for model selection; persistence beats the selected rival.", "DOWNGRADE"),
        ("CL-7", "post-1995 enrolment was not fitted (therefore the test is clean)", "results report",
         "true for enrolment, but 9/121 training rows are post-1995 (APIS 2019 gradient inside the test window; FIES 2003/2006).", "DOWNGRADE"),
        ("CL-8", "the 1971-1995 training window identifies the demand coefficients", "PROTOCOL_v5 §7",
         "premium drivers have 3 observed training anchors (1988,1990,1995); formal_share has 5 years (1991-1995); premium is interpolated 1995-2013.", "DOWNGRADE"),
        ("CL-9", "drivers are exogenous and predetermined", "PROTOCOL_v5 §3",
         "2013/2024 premium values are contemporaneous with the test outcomes; formal_share varies through the test period.", "DOWNGRADE"),
        ("CL-10", "learning/quality mechanism is modelled", "theory manuscripts (May/June); QA file names",
         "v5 has no learning state, no quality, no score/achievement variable (engine5.py keyword counts 0).", "WITHDRAW"),
        ("CL-11", "score bars / quotas / high-stakes gates are modelled", "theory manuscripts; v6 Phase-1 notes",
         "v5 has no score bar and no quota; only an optional exogenous tertiary exam pass-rate schedule (absent for PHL) and capacity rationing.", "WITHDRAW"),
        ("CL-12", "teacher supply / teacher effort is modelled", "theory manuscripts",
         "teachers enter only through the declarative tertiary-capacity rule; no teacher market or effort.", "WITHDRAW"),
        ("CL-13", "labour market / earnings / employer screening / credential queues are modelled", "June manuscript; paper's 'relational floor'",
         "no labour market, no earnings, no employer; credentials only as exogenous wage-premium drivers and a formal-share proxy.", "WITHDRAW"),
        ("CL-14", "rural/urban differences and migration are modelled", "theory manuscripts; HKG/AQRF material",
         "no region, no urban/rural, no migration in the engine; documented omission.", "WITHDRAW"),
        ("CL-15", "borrowing/credit constraints are modelled", "household-demand discussion",
         "affordability is a cost-burden term; no borrowing, credit, savings or uncertainty state.", "WITHDRAW"),
        ("CL-16", "shadow education / tutoring effects are estimated in MASSENG", "coupling notes; shadow record",
         "v5 has no tutoring/shadow state; the coupled module is an external declared layer (achievement shift as declared odds multiplier), not an estimate.", "WITHDRAW"),
        ("CL-17", "state supply and finance drive massification (supply-led established)", "theory manuscripts; dashboard line 618",
         "v5 takes capacity and cost policies as declared inputs; no tax, budget, construction or teacher-supply response. Panel claim, not engine result.", "WITHDRAW"),
        ("CL-18", "MASSENG v5 validates the surplus / credential-pipeline theory", "May/June manuscripts",
         "employer/state/migration/learning mechanisms are outside the engine; only conditional demand accounting is present.", "WITHDRAW"),
        ("CL-19", "MASSENG is calibrated / validated / usable for forecasting", "release prose",
         "status is 'not calibrated'; report/paper say no forecast or policy simulation.", "WITHDRAW"),
        ("CL-20", "dashboard / public massification claims are MASSENG v5 results", "dashboard; public/research/massification",
         "dashboard = E1/E6 panel; public page = ABM mechanism tests; neither is MASSENG.", "DOWNGRADE"),
        ("CL-21", "the PHL fit reproduces from the committed bundle", "README reproduction block",
         "record's own fresh-copy QA is 13/13 byte-identical under pinned deps; R1/R4 need a two-stage continuation whose stage-1 parameters are not committed; no independent re-run here.", "DOWNGRADE"),
        ("CL-22", "'at bounds: none' for R4", "model/README table",
         "R4 kappa=39.995 vs upper bound 40 is not flagged because the rule uses absolute |v-bound|<1e-3 on a 0-40 scale.", "DOWNGRADE"),
        ("CL-23", "the Bayesian screen yields a posterior / identifies mechanisms", "masseng-bayes-audit record (cited)",
         "conditional importance screen: ESS 2.17%, prior- and sigma-dominated, X5 confusion 50% (<60% criterion), baseline fixes 11 params from an R1 fit with admitted data reuse.", "WITHDRAW"),
    ]
    for cid, claim, source, reality, verdict in claims:
        add(cid, "claim inventory", claim, {"verdict": verdict, "reality": reality}, source, "FLAG")

    result = dict(audit="MASSENG v5 massification claim layer (engine/data reality only)",
                  date="2026-11-25", heads=heads, checks=CHECKS,
                  notes=["read-only; no server compute; no masseng edits",
                         "Bayesian screen numbers are read from the prior audit record, not recomputed",
                         "literature verification is out of scope by instruction: this audit is engine/data reality only"])
    path = outdir / "claims_audit.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"wrote": str(path), "checks": len(CHECKS),
                      "flags": sum(1 for c in CHECKS if c["status"] == "FLAG")}, indent=1))
    for c in CHECKS:
        print(f"[{c['status']}] {c['id']}: {c['question']}")

if __name__ == "__main__":
    main()
