"""Run the Cluster D battery (#10, #11, #12) and write RESULTS.csv + RUN_MANIFEST.json.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

Usage:  python3 run_all.py [n_seeds]
Writes ../RESULTS.csv and ../RUN_MANIFEST.json. Does not touch anything outside cluster_D/.
"""
import csv
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import exp10_level_first as e10
import exp11_cohort_shock as e11
import exp12_temporary as e12
import toy_engine as eng

SEED_BASE = 20261120
DEFAULT_SEEDS = 240
LABEL = eng.LABEL
FIELDS = ["experiment", "level", "arm", "comparison", "window", "metric", "statistic",
          "value", "n", "threshold", "met", "rule", "note", "label"]


def seeds_for(n):
    return [SEED_BASE + i for i in range(1, n + 1)]


def run_experiment(mod, seeds):
    per_seed = {}
    for s in seeds:
        per_seed[s] = mod.run_seed(s)
    return per_seed


def to_rows(exp, summary_rows, threshold_rows):
    rows = []
    for r in summary_rows:
        row = dict(r)
        row.update(experiment=exp, label=LABEL)
        rows.append(row)
    for r in threshold_rows:
        row = dict(level="threshold", arm="", comparison="", window="", statistic="observed",
                   n="", **r)
        row.update(experiment=exp, label=LABEL)
        rows.append(row)
    return rows


def sha16(path):
    h = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return h[:16], h


def main():
    n_seeds = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SEEDS
    seeds = seeds_for(n_seeds)
    here = Path(__file__).resolve().parent
    out_dir = here.parent
    t0 = time.time()

    print(f"seeds={n_seeds} base={SEED_BASE}  (ILLUSTRATIVE TOY — not evidence)")
    t = time.time()
    per10 = run_experiment(e10, seeds)
    print(f"  #10 done {time.time()-t:.1f}s")
    t = time.time()
    per11 = run_experiment(e11, seeds)
    print(f"  #11 done {time.time()-t:.1f}s")
    t = time.time()
    per12 = run_experiment(e12, seeds)
    print(f"  #12 done {time.time()-t:.1f}s")

    v10, th10 = e10.thresholds(per10)
    v11, th11 = e11.thresholds(per11)
    v12, th12 = e12.thresholds(per12)

    rows = []
    for exp, mod, per, th in ((e10.EXPERIMENT, e10, per10, th10),
                              (e11.EXPERIMENT, e11, per11, th11),
                              (e12.EXPERIMENT, e12, per12, th12)):
        rows += to_rows(exp, mod.summarise(per), th)

    # Per-seed audit rows for the headline metrics of each experiment.
    audit = {
        e10.EXPERIMENT: ["X_M0", "X_M1", "X_M2", "X_M3", "U90", "S_M3_M0",
                         "primary_share_h", "upper_share_h", "upper_total"],
        e11.EXPERIMENT: ["X_M0", "X_M1", "primary_share_h", "lower_share_h",
                         "upper_share_h", "primary_seats_h"],
        e12.EXPERIMENT: ["DURING_upper_apps", "POST_upper_apps", "DECAY_upper_apps",
                         "DURING_hires", "POST_hires", "DECAY_hires",
                         "DURING_upper_comple", "POST_grad_hires"],
    }
    for exp, per in ((e10.EXPERIMENT, per10), (e11.EXPERIMENT, per11), (e12.EXPERIMENT, per12)):
        for s in seeds:
            for arm, m in per[s].items():
                for met in audit[exp]:
                    rows.append(dict(experiment=exp, level="seed", arm=arm,
                                     comparison="level", window="all", metric=met,
                                     statistic="value", value=m[met], n=1,
                                     threshold="", met="", rule="",
                                     note=f"seed={s}", label=LABEL))

    with (out_dir / "RESULTS.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})

    runtime = time.time() - t0
    h16, hfull = sha16(out_dir / "RESULTS.csv")
    pre16, prefull = sha16(out_dir / "PRE_DECLARATIONS.md")
    files = {}
    for p in sorted(out_dir.rglob("*")):
        # The manifest cannot contain its own hash; it is excluded and its hash is
        # reported in the run record instead.
        if p.is_file() and p.name != "RUN_MANIFEST.json":
            files[str(p.relative_to(out_dir))] = sha16(p)[0]

    manifest = dict(
        label=LABEL,
        battery="Cluster D toys #10, #11, #12 (COUNCIL_TOY_SPECS_015.md)",
        status="illustrative; not calibrated; not evidence; phase stays CLOSED",
        run_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        python=platform.python_version(),
        platform=platform.platform(),
        seeds=dict(count=n_seeds, first=seeds[0], last=seeds[-1], base=SEED_BASE,
                   paired=True,
                   note="paired counterfactuals share identical latent draws per (seed, cohort, slot)"),
        parameter_vector=dict(eng.DEFAULT_PARAMS),
        experiment_overrides=dict(
            exp10=dict(pv_budget_per_level=e10.PV_BUDGET, discount=e10.DELTA,
                       arms={a: (None if a == "control" else e10.WINDOWS[a]) for a in e10.ARMS}),
            exp11=dict(cohort_sizes=e11.SIZES, capacity_rules=list(e11.RULES),
                       investment_fixed=3, employer="responsive (per-child invariant)"),
            exp12=dict(seat0=e12.SEAT0, lease_seats=12, lease_cohorts=[2, 4],
                       investment_fixed=0, warm_stage=e12.PARAMS["warm_stage"],
                       init_readers=e12.PARAMS["init_readers"],
                       init_formal_share=e12.PARAMS["init_formal_share"],
                       init_skill_stock=e12.PARAMS["init_skill_stock"],
                       belief_memory=e12.PARAMS["belief_memory"],
                       placement_reference=e12.PARAMS["placement_reference"],
                       fee_waiver_upper=0.0, windows=e12.WINDOWS),
        ),
        verdicts={e10.EXPERIMENT: v10, e11.EXPERIMENT: v11, e12.EXPERIMENT: v12},
        runtime_seconds=round(runtime, 2),
        rows=int(len(rows)),
        predeclarations=dict(sha256_16=pre16, sha256=prefull,
                             note="thresholds frozen before the run; see PRE_DECLARATIONS.md"),
        results_sha256_16=h16,
        manifest_self_hash_excluded="RUN_MANIFEST.json is not hashed inside itself; its SHA-256-16 is reported in the run record",
        files_sha256_16=files,
        isolation=dict(
            writes_only_under="extensions_archive/toys_2026-11-20/cluster_D/",
            phase_files_touched=None,
            closed_anchor_files_touched=None,
            git_commit=None,
            icloud_writes=None,
        ),
    )
    (out_dir / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"\nverdicts: #10={v10}  #11={v11}  #12={v12}")
    print(f"wrote {out_dir/'RESULTS.csv'} ({len(rows)} rows, {runtime:.1f}s)")
    print(f"wrote {out_dir/'RUN_MANIFEST.json'}")


if __name__ == "__main__":
    main()
