"""Run Cluster A toy experiments #1-#3 (entry hysteresis, net vs gross, entry lag).

ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence;
no historical test; phase closed; do not cite numbers as estimates.

Standard library only. Reads no external data. Writes RESULTS.csv and
RESULTS_SUMMARY.json (see --out).

Usage:
  python3 run_cluster_a.py                 # 200 seeds -> ../RESULTS.csv
  python3 run_cluster_a.py --smoke         # 6 seeds, stdout only, no files
"""

import argparse
import csv
import json
import platform
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import toy_market as tm  # noqa: E402

LABEL = ("ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence; "
         "no historical test; phase closed; do not cite numbers as estimates.")
SEED_BASE = 20261120
N_SEEDS = 200
PUBLIC_SEATS = 30
BASE_PREMIUM = tm.BASE_PREMIUM

# --------------------------------------------------------------------------- #
# Experiment 1 parameter vector (declared in PRE_DECLARATIONS.md)
# --------------------------------------------------------------------------- #
E1 = dict(cap=8, max_providers=4, public_seats=30, f_low=400, f_high=800)
E1_UP = [1.00, 1.20, 1.20, 1.00]
E1_DOWN = [1.00, 0.80, 0.80, 1.00]
E1_MODES = ["lump", "divisible"]          # lump = primary, divisible = robustness
E1_ARMS = []
for _mode in E1_MODES:
    for _fname, _fixed in (("F_low", E1["f_low"]), ("F_high", E1["f_high"])):
        for _direction, _path in (("shock_up", E1_UP), ("shock_down", E1_DOWN)):
            E1_ARMS.append(("{0}_{1}_{2}".format(_mode, _fname, _direction),
                            _mode, _fixed, _direction, _path))
E1_PERIOD_METRICS = ["applications", "customers", "public_admissions",
                     "private_seats", "private_admissions", "total_admissions",
                     "providers", "vacancy", "backlog"]

# --------------------------------------------------------------------------- #
# Experiment 2 parameter vector
# --------------------------------------------------------------------------- #
E2_CONFIGS = [
    dict(name="cap15", cap=15, max_providers=2, primary=True),
    dict(name="cap30", cap=30, max_providers=1, primary=False),
]
E2_F = [("F_low", 400), ("F_mid", 1200), ("F_high", 1500)]
E2_EXPANSIONS = [("exp30_50", 30, 50), ("exp38_39", 38, 39)]

# --------------------------------------------------------------------------- #
# Experiment 3 parameter vector
# --------------------------------------------------------------------------- #
E3 = dict(cap=4, max_providers=10, public_seats=30, fixed_cost_cents=400,
          periods=12, boom_start=2, boom_end=5)
E3_TEMP = [1.00] + [1.20] * 4 + [1.00] * 7      # boom t=2..5, back to 1.00 from t=6
E3_PERM = [1.00] + [1.20] * 11                  # boom from t=2 onward
E3_CELLS = [("L0_temp", 0, E3_TEMP), ("L2_temp", 2, E3_TEMP),
            ("L4_temp", 4, E3_TEMP), ("L0_perm", 0, E3_PERM),
            ("L2_perm", 2, E3_PERM), ("L4_perm", 4, E3_PERM)]
E3_PERIOD_METRICS = ["private_seats", "private_admissions", "total_admissions",
                     "vacancy", "backlog", "customers"]


def _num(value):
    if isinstance(value, float):
        return round(value, 6)
    return value


class Recorder(object):
    def __init__(self):
        self.rows = []
        self.by_arm = {}

    def add(self, experiment, arm, seed, metric, value):
        value = _num(value)
        self.rows.append((experiment, arm, seed, metric, value))
        self.by_arm.setdefault((experiment, arm), {}).setdefault(
            metric, []).append(value)

    def mean(self, experiment, arm, metric):
        vals = self.by_arm[(experiment, arm)][metric]
        return sum(vals) / len(vals)

    def share(self, experiment, arm, metric):
        vals = self.by_arm[(experiment, arm)][metric]
        return sum(1 for v in vals if v) / len(vals)


# --------------------------------------------------------------------------- #
# Experiment 1: entry-threshold hysteresis
# --------------------------------------------------------------------------- #
def experiment_1(rec, seeds):
    exp = "1_entry_hysteresis"
    for seed in seeds:
        cohort = tm.draw_cohort(seed)
        for arm, mode, fixed_cents, _direction, path in E1_ARMS:
            bk = tm.breakeven_seats(fixed_cents)
            recs = tm.simulate(cohort, path, E1["public_seats"], E1["cap"], bk,
                               E1["max_providers"], entry_lag=0, mode=mode)
            for r in recs:
                for name in E1_PERIOD_METRICS:
                    rec.add(exp, arm, seed,
                            "{0}_t{1}".format(name, r["period"]), r[name])
            s1, s2, s4 = (recs[0]["private_seats"], recs[1]["private_seats"],
                          recs[3]["private_seats"])
            exit_seats = max(0, s1 - s2)
            entry_seats = max(0, s2 - s1)
            exit_prov = max(0, recs[0]["providers"] - recs[1]["providers"])
            entry_prov = max(0, recs[1]["providers"] - recs[0]["providers"])
            scalars = dict(
                seats_t1=s1, seats_t2=s2, seats_t4=s4,
                exit_seats_impact=exit_seats, entry_seats_impact=entry_seats,
                exit_providers_impact=exit_prov,
                entry_providers_impact=entry_prov,
                exit_event=1 if exit_prov > 0 else 0,
                entry_event=1 if entry_prov > 0 else 0,
                recovery_ratio=(s4 / s1) if s1 > 0 else -999.0,
                customers_t1=recs[0]["customers"],
                customers_t2=recs[1]["customers"],
                customers_t4=recs[3]["customers"],
                served_t1=recs[0]["private_admissions"],
                served_t2=recs[1]["private_admissions"],
                served_t4=recs[3]["private_admissions"],
            )
            for name, value in scalars.items():
                rec.add(exp, arm, seed, name, value)

    agg = {}
    for arm, _, _, _, _ in E1_ARMS:
        for metric in sorted(rec.by_arm[(exp, arm)].keys()):
            agg["{0}.mean_{1}".format(arm, metric)] = _num(rec.mean(exp, arm, metric))
        for metric in ("exit_event", "entry_event"):
            agg["{0}.share_{1}".format(arm, metric)] = _num(rec.share(exp, arm, metric))

    def asymmetry(mode):
        down = "{0}_F_high_shock_down".format(mode)
        up = "{0}_F_high_shock_up".format(mode)
        exit_mean = rec.mean(exp, down, "exit_seats_impact")
        entry_mean = rec.mean(exp, up, "entry_seats_impact")
        ratio = (exit_mean / entry_mean) if entry_mean > 0 else -1.0
        return ratio, exit_mean, entry_mean

    for mode in E1_MODES:
        a_high, exit_high, entry_high = asymmetry(mode)
        down_low = "{0}_F_low_shock_down".format(mode)
        up_low = "{0}_F_low_shock_up".format(mode)
        exit_low = rec.mean(exp, down_low, "exit_seats_impact")
        entry_low = rec.mean(exp, up_low, "entry_seats_impact")
        a_low = (exit_low / entry_low) if entry_low > 0 else -1.0
        agg["{0}.A_high".format(mode)] = _num(a_high)
        agg["{0}.A_low".format(mode)] = _num(a_low)
        agg["{0}.A_diff".format(mode)] = _num(a_high - a_low)
        agg["{0}.mean_exit_seats_high".format(mode)] = _num(exit_high)
        agg["{0}.mean_entry_seats_high".format(mode)] = _num(entry_high)
        agg["{0}.mean_exit_seats_low".format(mode)] = _num(exit_low)
        agg["{0}.mean_entry_seats_low".format(mode)] = _num(entry_low)
        agg["{0}.mean_exit_providers_high".format(mode)] = _num(
            rec.mean(exp, "{0}_F_high_shock_down".format(mode), "exit_providers_impact"))
        agg["{0}.mean_entry_providers_high".format(mode)] = _num(
            rec.mean(exp, "{0}_F_high_shock_up".format(mode), "entry_providers_impact"))
    return agg


# --------------------------------------------------------------------------- #
# Experiment 2: public expansion, net vs gross
# --------------------------------------------------------------------------- #
def experiment_2(rec, seeds):
    exp = "2_public_expansion"
    for seed in seeds:
        cohort = tm.draw_cohort(seed)
        for cfg in E2_CONFIGS:
            for fname, fixed_cents in E2_F:
                bk = tm.breakeven_seats(fixed_cents)
                for ename, pre_seats, post_seats in E2_EXPANSIONS:
                    arm = "{0}_{1}_{2}".format(cfg["name"], fname, ename)
                    pre = tm.equilibrium_state(cohort, BASE_PREMIUM, pre_seats,
                                               cfg["cap"], bk, cfg["max_providers"])
                    post = tm.equilibrium_state(cohort, BASE_PREMIUM, post_seats,
                                                cfg["cap"], bk, cfg["max_providers"])
                    gross = post["public_admissions"] - pre["public_admissions"]
                    net = post["total_admissions"] - pre["total_admissions"]
                    exits = max(0, pre["providers"] - post["providers"])
                    scalars = dict(
                        public_pre=pre["public_admissions"],
                        public_post=post["public_admissions"],
                        total_pre=pre["total_admissions"],
                        total_post=post["total_admissions"],
                        gross_gain=gross, net_gain=net,
                        retention=(net / gross) if gross > 0 else -999.0,
                        private_admissions_pre=pre["private_admissions"],
                        private_admissions_post=post["private_admissions"],
                        private_seats_pre=pre["private_seats"],
                        private_seats_post=post["private_seats"],
                        providers_pre=pre["providers"],
                        providers_post=post["providers"],
                        private_exits=exits,
                        private_exit_event=1 if exits > 0 else 0,
                        private_seats_lost=max(0, pre["private_seats"] - post["private_seats"]),
                        private_admissions_lost=max(0, pre["private_admissions"] - post["private_admissions"]),
                        applications_pre=pre["applications"],
                        applications_post=post["applications"],
                        customers_pre=pre["customers"],
                        customers_post=post["customers"],
                    )
                    for name, value in scalars.items():
                        rec.add(exp, arm, seed, name, value)

    agg = {}
    for cfg in E2_CONFIGS:
        for fname, _ in E2_F:
            for ename, _, _ in E2_EXPANSIONS:
                arm = "{0}_{1}_{2}".format(cfg["name"], fname, ename)
                mean_net = rec.mean(exp, arm, "net_gain")
                mean_gross = rec.mean(exp, arm, "gross_gain")
                agg["{0}.mean_net_gain".format(arm)] = _num(mean_net)
                agg["{0}.mean_gross_gain".format(arm)] = _num(mean_gross)
                agg["{0}.R".format(arm)] = (_num(mean_net / mean_gross)
                                            if mean_gross > 0 else -1.0)
                for metric in ("private_exit_event", "private_exits",
                               "private_seats_lost", "private_admissions_lost",
                               "retention", "providers_pre", "providers_post",
                               "customers_pre", "customers_post",
                               "applications_pre", "applications_post",
                               "private_admissions_pre", "private_admissions_post",
                               "public_pre", "public_post", "total_pre",
                               "total_post"):
                    agg["{0}.mean_{1}".format(arm, metric)] = _num(rec.mean(exp, arm, metric))
    return agg


# --------------------------------------------------------------------------- #
# Experiment 3: entry lag and overshoot
# --------------------------------------------------------------------------- #
def experiment_3(rec, seeds):
    exp = "3_entry_lag"
    bk = tm.breakeven_seats(E3["fixed_cost_cents"])
    for seed in seeds:
        cohort = tm.draw_cohort(seed)
        served, seats = {}, {}
        for arm, lag, path in E3_CELLS:
            recs = tm.simulate(cohort, path, E3["public_seats"], E3["cap"], bk,
                               E3["max_providers"], entry_lag=lag)
            for r in recs:
                for name in E3_PERIOD_METRICS:
                    rec.add(exp, arm, seed,
                            "{0}_t{1}".format(name, r["period"]), r[name])
            seats_path = [r["private_seats"] for r in recs]
            served_path = [r["private_admissions"] for r in recs]
            served[arm], seats[arm] = served_path, seats_path
            cust_path = [r["customers"] for r in recs]
            peak_vacancy = max(max(0, s - c) for s, c in zip(seats_path, cust_path))
            peak_backlog = max(r["backlog"] for r in recs)
            cum_vacancy = sum(r["vacancy"] for r in recs)
            cum_backlog = sum(r["backlog"] for r in recs)
            tss = -999
            for t in range(2, E3["periods"] + 1):
                if (all(seats_path[k] == seats_path[-1] for k in range(t - 1, E3["periods"]))
                        and all(served_path[k] == served_path[-1]
                                for k in range(t - 1, E3["periods"]))):
                    tss = t
                    break
            scalars = dict(peak_vacancy=peak_vacancy, peak_backlog=peak_backlog,
                           cumulative_vacancy=cum_vacancy,
                           cumulative_backlog=cum_backlog,
                           time_to_steady_state=tss,
                           censored=1 if tss == -999 else 0,
                           final_seats=seats_path[-1],
                           peak_seats=max(seats_path),
                           peak_served=max(served_path),
                           total_admissions_sum=sum(r["total_admissions"] for r in recs))
            for name, value in scalars.items():
                rec.add(exp, arm, seed, name, value)

        for arm, lag, _path in E3_CELLS:
            base = arm.replace("L{0}".format(lag), "L0")
            if base == arm:
                rec.add(exp, arm, seed, "peak_admission_shortfall", 0)
                rec.add(exp, arm, seed, "peak_admission_excess", 0)
                continue
            shortfall = max(a - b for a, b in zip(served[base], served[arm]))
            excess = max(b - a for a, b in zip(served[base], served[arm]))
            rec.add(exp, arm, seed, "peak_admission_shortfall", shortfall)
            rec.add(exp, arm, seed, "peak_admission_excess", excess)

    agg = {}
    for arm, _, _ in E3_CELLS:
        for metric in ("peak_vacancy", "peak_backlog", "cumulative_vacancy",
                       "cumulative_backlog", "time_to_steady_state", "censored",
                       "peak_admission_shortfall", "peak_admission_excess",
                       "peak_seats", "peak_served", "final_seats",
                       "total_admissions_sum"):
            agg["{0}.mean_{1}".format(arm, metric)] = _num(rec.mean(exp, arm, metric))
    return agg


# --------------------------------------------------------------------------- #
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=N_SEEDS)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--out", default=str(HERE.parent / "RESULTS.csv"))
    args = parser.parse_args(argv)

    n = 6 if args.smoke else args.seeds
    if n < 2:
        raise SystemExit("need at least 2 seeds")
    seeds = [SEED_BASE + i for i in range(n)]

    rec = Recorder()
    agg1 = experiment_1(rec, seeds)
    agg2 = experiment_2(rec, seeds)
    agg3 = experiment_3(rec, seeds)

    summary = {
        "label": LABEL,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "seed_base": SEED_BASE,
        "seeds": {"first": seeds[0], "last": seeds[-1], "count": n},
        "exp1": {"params": E1, "modes": E1_MODES,
                 "paths": {"up": E1_UP, "down": E1_DOWN}, "agg": agg1},
        "exp2": {"params": {"configs": E2_CONFIGS, "fixed_costs": E2_F,
                            "expansions": E2_EXPANSIONS}, "agg": agg2},
        "exp3": {"params": E3,
                 "paths": {"temporary": E3_TEMP, "permanent": E3_PERM},
                 "agg": agg3},
    }

    if args.smoke:
        pick1 = [k for k in agg1 if ".A_" in k or "mean_exit_seats" in k
                 or "mean_entry_seats" in k]
        pick2 = [k for k in agg2 if k.endswith(".R") or k.endswith("mean_net_gain")
                 or k.endswith("mean_private_exits")]
        pick3 = [k for k in agg3 if "peak_vacancy" in k or "time_to_steady" in k
                 or "peak_backlog" in k or "peak_admission_shortfall" in k]
        print(json.dumps({"exp1": {k: agg1[k] for k in sorted(pick1)},
                          "exp2": {k: agg2[k] for k in sorted(pick2)},
                          "exp3": {k: agg3[k] for k in sorted(pick3)}},
                         indent=2, sort_keys=True))
        print("rows:", len(rec.rows))
        return 0

    out = Path(args.out)
    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["experiment", "arm", "seed", "metric", "value"])
        for experiment, arm, seed, metric, value in rec.rows:
            writer.writerow([experiment, arm, seed, metric, value])
    summary_path = out.parent / "RESULTS_SUMMARY.json"
    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")
    print(LABEL)
    print("wrote {0} rows to {1}".format(len(rec.rows), out))
    print("wrote {0}".format(summary_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
