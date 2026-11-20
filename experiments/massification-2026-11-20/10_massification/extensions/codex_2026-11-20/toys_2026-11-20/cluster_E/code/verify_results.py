"""Independent re-derivation of every predeclared verdict from RESULTS.csv.

ILLUSTRATIVE TOY. Reads only the written results table; recomputes each
threshold rule from PRE_DECLARATIONS.md against the aggregate rows and asserts
that the recorded verdict agrees. Also prints the ratios and sensitivity
contrasts that are easier to read as derived quantities.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def load():
    rows = list(csv.DictReader(open(HERE / "RESULTS.csv")))
    return rows


def get(rows, exp, metric, group=None, cell=None):
    for r in rows:
        if r["experiment"] != exp or r["metric"] != metric:
            continue
        if group is not None and r["group"] != group:
            continue
        if cell is not None and r["cell"] != cell:
            continue
        return r
    raise KeyError((exp, metric, group, cell))


def main():
    rows = load()
    ok = 0
    bad = []
    checks = []

    # --- E13
    e = "E13_migration_remittance"
    v = lambda m: float(get(rows, e, m)["value"])  # noqa: E731
    c = [("T13-P1a", v("threshold_remit_apps") >= 4.0, "remit apps >= 4.0"),
         ("T13-P1b", v("threshold_remit_completion") >= 1.0, "remit completion >= 1.0 pp"),
         ("T13-P2", v("threshold_route_completion") >= 8.0, "route completion >= 8.0 pp"),
         ("T13-P3", v("threshold_local_jobs_flat") == 0.0, "local jobs exactly flat")]
    for tid, passed, rule in c:
        rec = get(rows, e, {"T13-P1a": "threshold_remit_apps",
                            "T13-P1b": "threshold_remit_completion",
                            "T13-P2": "threshold_route_completion",
                            "T13-P3": "threshold_local_jobs_flat"}[tid])["verdict"]
        checks.append((tid, rule, "PASS" if passed else "FAIL", rec))

    # --- E14
    e = "E14_sector_shock_field_access"
    v = lambda m: float(get(rows, e, m)["value"])  # noqa: E731
    open_apps = v("threshold_field_specificity")
    open_comp = v("threshold_field_specificity_completers")
    open_total = v("threshold_reallocation_not_general")
    closed_apps = v("threshold_gate_attenuation_apps")
    closed_comp = v("threshold_gate_attenuation_completers")
    ratio_apps = closed_apps / open_apps
    ratio_comp = closed_comp / open_comp
    pb = get(rows, e, "threshold_placebo_symmetry")
    pb_B = float(pb["value"])
    pb_A = float(get(rows, e, "apps_A", "placebo_open")["value"])
    vac_closed = v("threshold_vacancies_under_gate")
    vac_open = float(get(rows, e, "vacancies_A", "all",
                         "shock=targeted_A|access=open")["value"])
    checks += [
        ("T14-P1a", "open A apps >= 30", "PASS" if open_apps >= 30 else "FAIL",
         get(rows, e, "threshold_field_specificity")["verdict"]),
        ("T14-P1b", "open A completers >= 25", "PASS" if open_comp >= 25 else "FAIL",
         get(rows, e, "threshold_field_specificity_completers")["verdict"]),
        ("T14-P1c", "|total completers| <= 10", "PASS" if abs(open_total) <= 10 else "FAIL",
         get(rows, e, "threshold_reallocation_not_general")["verdict"]),
        ("T14-P2a", "closed/open apps ratio <= 0.5",
         "PASS" if ratio_apps <= 0.5 else "FAIL",
         get(rows, e, "threshold_gate_attenuation_apps")["verdict"]),
        ("T14-P2b", "closed/open completers ratio <= 0.5",
         "PASS" if ratio_comp <= 0.5 else "FAIL",
         get(rows, e, "threshold_gate_attenuation_completers")["verdict"]),
        ("T14-P3", "placebo B >= +30 and A <= -20",
         "PASS" if (pb_B >= 30 and pb_A <= -20) else "FAIL", pb["verdict"]),
        ("T14-P4", "closed vacancies >= 10 and open <= 3",
         "PASS" if (vac_closed >= 10 and vac_open <= 3) else "FAIL",
         get(rows, e, "threshold_vacancies_under_gate")["verdict"]),
    ]

    # --- E15
    e = "E15_neighbour_information_roads"
    v = lambda m: float(get(rows, e, m)["value"])  # noqa: E731
    r1 = v("info_effect_road1")
    r0 = v("info_effect_road0")
    diff = v("info_road_interaction")
    road = v("road_main_effect")
    teacher = v("teacher_main_effect_completion")
    info = v("info_main_effect")
    adm = v("info_effect_admissions")
    queue = v("threshold_queues_not_places")
    checks += [
        ("T15-P1", "diff >= 0.06 and r1 >= 0.10 and r0 <= 0.06",
         "PASS" if (diff >= 0.06 and r1 >= 0.10 and r0 <= 0.06) else "FAIL",
         get(rows, e, "threshold_info_interaction")["verdict"]),
        ("T15-P2", "road >= 0.05 and teacher >= 2.0 and info >= 0.03",
         "PASS" if (road >= 0.05 and teacher >= 2.0 and info >= 0.03) else "FAIL",
         get(rows, e, "threshold_main_effects")["verdict"]),
        ("T15-P3", "|adm| <= 0.02 and queue/hh >= 0.05",
         "PASS" if (abs(adm) <= 0.02 and queue >= 0.05) else "FAIL",
         get(rows, e, "threshold_queues_not_places")["verdict"]),
    ]

    print(f"{'ID':8s} {'expected':6s} {'recorded':8s}  rule")
    for tid, rule, exp_verdict, rec in checks:
        agree = exp_verdict == rec
        ok += agree
        if not agree:
            bad.append((tid, exp_verdict, rec))
        print(f"{tid:8s} {exp_verdict:6s} {rec:8s}  {rule}")

    print()
    print("derived ratios / contrasts:")
    print(f"  E14 closed/open application response ratio  = {ratio_apps:.4f}")
    print(f"  E14 closed/open completer  response ratio  = {ratio_comp:.4f}")
    print(f"  E14 placebo_open: B apps delta {pb_B:+.2f}, A apps delta {pb_A:+.2f}")
    print(f"  E14 vacancies after targeted shock: closed {vac_closed:.2f}, open {vac_open:.2f}")
    print(f"  E15 info effect road=1 {r1:+.4f}, road=0 {r0:+.4f}, diff {diff:+.4f}")
    print(f"  E15 main effects: road {road:+.4f}/hh, teacher {teacher:+.2f} pp, info {info:+.4f}/hh")
    print(f"  E15 info effect: admissions {adm:+.4f}/hh, queue {queue:+.4f}/hh")

    # sensitivity contrasts readable as differences of stored levels
    e = "E13_migration_remittance"
    half_eff = float(get(rows, e, "completion_rate_pp", "sensitivity")["value"])
    full_eff = float(get(rows, e, "threshold_route_completion")["value"])
    print(f"  E13 sensitivity: half-premium route effect on completion {half_eff:+.2f} pp "
          f"vs full-premium {full_eff:+.2f} pp (both paired vs closed/off)")

    s = [(r["cell"], r["metric"], float(r["value"])) for r in rows
         if r["experiment"] == "E15_neighbour_information_roads"
         and r["group"] == "sensitivity"]
    sens = {c: val for c, m, val in s if m == "apps_per_hh"}
    a00 = sens["info=0|road=0|teacher=0|roadcut=0.30"]
    a10 = sens["info=1|road=0|teacher=0|roadcut=0.30"]
    a01 = sens["info=0|road=1|teacher=0|roadcut=0.30"]
    a11 = sens["info=1|road=1|teacher=0|roadcut=0.30"]
    print(f"  E15 sensitivity (road cut 0.30): info effect road=1 {a11 - a01:+.4f}, "
          f"road=0 {a10 - a00:+.4f}, diff {(a11 - a01) - (a10 - a00):+.4f}")

    # --- falsifiers (re-derived from the same aggregates)
    e13 = "E13_migration_remittance"
    f13_trig = not (float(get(rows, e13, "threshold_route_completion")["value"]) >= 2.0
                    and float(get(rows, e13, "threshold_remit_apps")["value"]) > 0)
    e14 = "E14_sector_shock_field_access"
    f14_trig = (ratio_apps >= 1.0) or (ratio_comp >= 1.0) or (closed_comp >= open_comp)
    f15_trig = abs(diff) < 0.03
    for tid, trig, rec in (("F13", f13_trig, get(rows, "E13_migration_remittance", "falsifier_13_triggered")["verdict"]),
                           ("F14", f14_trig, get(rows, "E14_sector_shock_field_access", "falsifier_14_triggered")["verdict"]),
                           ("F15", f15_trig, get(rows, "E15_neighbour_information_roads", "falsifier_15_triggered")["verdict"])):
        expected = "FAIL" if trig else "PASS"   # PASS = falsifier not triggered
        agree = expected == rec
        ok += agree
        if not agree:
            bad.append((tid, expected, rec))
        print(f"{tid:8s} {'PASS' if not trig else 'FAIL':6s} {rec:8s}  not-triggered check")

    print()
    print(f"threshold verdicts re-derived: {ok}/{len(checks)+3} agree")
    if bad:
        raise SystemExit(f"DISAGREEMENT: {bad}")


if __name__ == "__main__":
    main()
