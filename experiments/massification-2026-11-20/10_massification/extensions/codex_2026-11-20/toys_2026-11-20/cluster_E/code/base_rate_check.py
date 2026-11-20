"""Design-time check: base rates of the CONTROL arms only.

ILLUSTRATIVE TOY. This script is NOT the experiment and writes no results file.
It fixes the stipulated constants so that the control arm is non-degenerate
(neither floor nor ceiling). It deliberately prints control arms only, so that
no threshold can be set from a treatment effect size.
"""
import common
import exp13_migration as e13
import exp14_sector as e14
import exp15_diffusion as e15

SEEDS = [20261120, 20261121, 20261122]
METRICS_13 = ["apps_per_cycle", "app_rate_pp", "adm_per_cycle", "comp_per_cycle",
              "completion_rate_pp", "unique_migrants", "remit_income_per_hh",
              "household_resources", "local_jobs_filled", "local_output_per_cycle"]
METRICS_14 = ["apps_A", "apps_B", "apps_total", "completers_A", "completers_total",
              "vacancies_A"]


def show(tag, values):
    print(f"{tag:46s} " + "  ".join(f"{k}={v:.3f}" for k, v in values.items()))


def main():
    print("--- E13 control arm: route=closed|remit=off (200 households, 20 cycles)")
    acc = {m: [] for m in METRICS_13}
    for seed in SEEDS:
        lat = e13.draw(seed)
        out = e13.simulate(lat, route_open=False, remit_on=False)
        for m in METRICS_13:
            acc[m].append(out[m])
    show("closed/off", {m: common.mean(acc[m]) for m in METRICS_13})

    print("--- E14 control arms (no shock), 200 leavers")
    for access in ("open", "closed"):
        acc = {m: [] for m in METRICS_14}
        for seed in SEEDS:
            lat = e14.draw(seed)
            out = e14.simulate(lat, None, access)
            for m in METRICS_14:
                acc[m].append(out[m])
        show(f"no shock / access={access}",
             {m: common.mean(acc[m]) for m in METRICS_14})

    print("--- E15 control arm: info=0 road=0 teacher=0 (60 hh per village)")
    for tied in (0, 1):
        acc = {m: [] for m in ("apps_total", "apps_primary", "apps_secondary",
                               "apps_tertiary", "adm_total", "comp_total",
                               "completion_rate_pp")}
        for seed in SEEDS:
            villages = e15.draw(seed)
            out = e15.simulate(villages[tied], 0, 0, 0)
            for m in acc:
                acc[m].append(out[m])
        show(f"control, {'tied' if tied else 'untied'} village",
             {m: common.mean(acc[m]) for m in acc})


if __name__ == "__main__":
    main()
