"""Item 7 (support) — integrity and reproducibility evidence for the delivered v0.

  F1  frozen predeclaration hash, parameter hash, model hash: unchanged
  F2  every file listed in SHA256SUMS.txt matches the file on disk
  F3  RUNS.json headline metrics recomputed from the delivered tables
  F4  D0_CHECK.json internal consistency and the no-observed-input read audit
  F5  labels, absence of wall-clock, run/seed/arm count, runtime
  F6  closed 2026-11-20 records untouched (git index)
  F7  determinism evidence: accepted from DETERMINISM.json, NOT re-run here

Nothing here re-runs the model.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C


def f(x):
    return float("nan") if x is None or str(x).strip() == "" else float(x)


def i(x):
    return int(float(x))


FROZEN = "7d25e17631a39f556a17ac62a53de12701d60dca6d09a05e2b080d8d3184799d"


def check_hashes():
    man = C.read_json("RUN_MANIFEST.json") if False else json.load(open(os.path.join(C.EXT, "RUN_MANIFEST.json")))
    rows = []
    ok = True
    files = {x["path"]: x["sha256"] for x in man["files"]}
    for rel, want in sorted(files.items()):
        got = C.sha256_file(os.path.join(C.EXT, rel))
        rows.append((rel, want, got, want == got))
        ok = ok and (want == got)
    pre = C.sha256_file(C.PREDECL_PATH)
    rows.append(("PRE_DECLARATIONS.md vs frozen hash", FROZEN, pre, pre == FROZEN))
    ok = ok and pre == FROZEN
    return dict(item="F1/F2 hashes: manifest + frozen predeclaration",
                n_files=len(rows), n_mismatch=sum(1 for r in rows if not r[3]),
                predeclaration_sha256=pre, frozen=FROZEN,
                verdict="PASS" if ok else "FAIL"), rows


def check_runs_metrics():
    runs = C.read_json("RUNS.json")
    bad = []
    n = 0
    panels = {a: C.Panel(a) for a in C.ARMS}
    for r in runs["runs"]:
        arm, seed, m = r["arm"], r["seed"], r["metrics"]
        rows = panels[arm].seed_rows(seed)
        calc = {
            "mean_years_completed": sum(x["_yc"] for x in rows) / len(rows),
            "completion_primary": sum(1 for x in rows if x["_completed_primary_year"] >= 0) / len(rows),
            "completion_lower_secondary": sum(1 for x in rows if x["_completed_lower_year"] >= 0) / len(rows),
            "completion_upper_secondary": sum(1 for x in rows if x["_completed_upper_year"] >= 0) / len(rows),
            "completion_tertiary": sum(1 for x in rows if x["_completed_tertiary_year"] >= 0) / len(rows),
        }
        coh = [x for x in C.cohort_rows(arm) if i(x["seed"]) == seed]
        cx = [x for x in C.coex_rows(arm) if i(x["seed"]) == seed]
        calc["left_secondary_early_share_mean"] = sum(f(x["left_secondary_early_share"]) for x in coh) / len(coh)
        calc["unused_accessible_share_mean"] = sum(f(x["unused_accessible_share"]) for x in cx) / len(cx)
        ratio = [f(x["gate_to_catchup_ratio"]) for x in cx if f(x["gate_to_catchup_ratio"]) == f(x["gate_to_catchup_ratio"])]
        calc["gate_to_catchup_ratio_mean"] = sum(ratio) / len(ratio)
        calc["gate_household_share_mean"] = sum(f(x["gate_household_share"]) for x in cx) / len(cx)
        qpp = [f(x["qualified_per_place"]) for x in cx if f(x["qualified_per_place"]) == f(x["qualified_per_place"])]
        calc["selective_qualified_per_place_mean"] = sum(qpp) / len(qpp)
        calc["selective_turned_away_total"] = sum(i(x["selective_turned_away"]) for x in cx)
        for k, v in calc.items():
            n += 1
            if abs(v - f(m[k])) > 1e-8 * max(1.0, abs(v)):
                bad.append((arm, seed, k, v, m[k]))
    return dict(item="F3 RUNS.json metrics recomputed from delivered tables",
                n_values=n, n_disagreements=len(bad),
                verdict="PASS" if not bad else "FAIL"), bad


def check_d0():
    d = C.read_json("D0_CHECK.json")
    stages = d["stages"]
    all_ok = all(v.get("ok") for v in stages.values())
    reads = stages["pre_run"]["checks"]["source_reads"]["detail"]
    bad_reads = [x for x in reads if not x.get("allowed")]
    return dict(item="F4 D0_CHECK internal consistency + read audit",
                verdict_field=d["verdict"], all_stages_ok=all_ok,
                release_blocking=d["release_blocking"],
                n_source_reads=len(reads), n_disallowed_reads=len(bad_reads),
                predeclaration_field_matches=d["predeclaration_sha256"] == FROZEN,
                verdict="PASS" if (d["verdict"] == "PASS" and all_ok and not bad_reads
                                   and d["predeclaration_sha256"] == FROZEN) else "FAIL")


def check_labels():
    bad_label = []
    n = 0
    date_re = re.compile(r"\b20\d\d-\d\d-\d\d\b")
    dated = []
    for name in sorted(os.listdir(C.RES)):
        if not name.endswith(".csv"):
            continue
        n += 1
        with open(os.path.join(C.RES, name)) as fh:
            fh.readline()          # header
            first = fh.readline()  # first data row
            body = fh.read()
        if not first.startswith("SIMULATED"):
            bad_label.append(name)
        if date_re.search(body):
            dated.append(name)
    runs = C.read_json("RUNS.json")
    man = json.load(open(os.path.join(C.EXT, "RUN_MANIFEST.json")))
    suite = man["suite"]
    return dict(item="F5 labels / no wall-clock / suite shape",
                n_csv=n, n_missing_label=len(bad_label), n_with_date_string=len(dated),
                runs=suite["runs"], arms=len(suite["arms"]), seeds=suite["seeds"],
                runtime_seconds=suite["runtime_seconds"],
                runtime_under_limit=suite["within_limit"],
                verdict="PASS" if (not bad_label and not dated and suite["runs"] == 24
                                   and suite["runtime_seconds"] < 120) else "FAIL")


def check_closed():
    root = C.EXT
    for _ in range(3):
        root = os.path.dirname(root)
    try:
        out = subprocess.run(["git", "-C", root, "status", "--porcelain"],
                             capture_output=True, text=True, timeout=30)
        lines = [x for x in out.stdout.splitlines() if x.strip()]
    except Exception as e:  # pragma: no cover
        return dict(item="F6 closed 2026-11-20 records untouched", error=str(e),
                    verdict="NOT-CHECKED")
    modified = [x for x in lines if not x.startswith("??")]
    untracked = [x for x in lines if x.startswith("??")]
    return dict(item="F6 closed 2026-11-20 records untouched",
                git_root=root, n_modified_tracked=len(modified),
                modified_tracked=modified[:5], untracked_new=untracked,
                note="only untracked new directories; no tracked file modified",
                verdict="PASS" if not modified else "FAIL")


def main():
    checks = []
    c1, _ = check_hashes()
    checks.append(c1)
    c3, bad = check_runs_metrics()
    checks.append(c3)
    checks.append(check_d0())
    checks.append(check_labels())
    checks.append(check_closed())
    det = C.read_json("DETERMINISM.json")
    checks.append(dict(item="F7 determinism evidence (delivered, not re-run)",
                       identical=det["identical"], files_compared=len(det["files"]),
                       seed=det["seed"],
                       note="the harness did not re-run the simulator; the two _det_* "
                            "directories are not delivered, so byte-identity is accepted "
                            "from DETERMINISM.json only",
                       verdict="ACCEPTED-EVIDENCE"))
    runs = C.read_json("RUNS.json")
    checks.append(dict(item="F8 verdicts recomputed vs delivered",
                       delivered=runs["verdicts"]["D0"], endogeneity=runs["verdicts"]["ENDOGENEITY"],
                       ner_ceiling=runs["verdicts"]["NER-CEILING"],
                       coexistence=runs["verdicts"]["COEXISTENCE"],
                       different_families=runs["verdicts"]["DIFFERENT-FAMILIES"],
                       spillback=runs["verdicts"]["SPILLBACK"],
                       note="each verdict is re-derived in checks A/B/C/D; this row restates "
                            "the delivered label for the report",
                       verdict="SEE-INDIVIDUAL-CHECKS"))
    if bad:
        C.write_csv("F_metric_disagreements.csv", ["arm", "seed", "metric", "recomputed", "runs_json"],
                    [[x[0], x[1], x[2], "%.12g" % x[3], "%.12g" % f(x[4])] for x in bad])
    C.write_json("F_summary.json", {"label": "SIMULATED", "checks": checks})
    for c in checks:
        print("%-58s %s" % (c["item"], c.get("verdict")))
        for k, v in c.items():
            if k not in ("item", "verdict"):
                print("    %-40s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
