"""Experiment 15 - Neighbour information and roads (Cluster E). Stdlib only.

ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence.

Question (COUNCIL_TOY_SPECS_015 #15): do prestigious-neighbour information, road
access and teacher supply have separable effects on applications, and does
information raise applications MORE where accessibility is high?

Rules (all stipulated, all imposed). Base: diffusion.py distance/kin structure.
  * Two villages of 60 households per seed: untied (0) and kin-tied (1) to an
    urban elite school. Latents (cash, work cost, aptitude, distance, exposure
    draw, completion draws, lottery order) are drawn ONCE per seed and shared by
    all 8 factor arms, so every contrast is paired within seed.
  * Factors, varied one at a time in a 2x2x2 design: info {0,1} (a prestigious
    neighbouring school exists), road {0,1} (village road access), teacher {0,1}
    (extra teacher supply: +1 seat per level and +0.06 completion probability).
  * INFORMATION TRAVELS ON ROADS (explicit stipulated assumption): a household is
    exposed to the neighbour-school signal with probability 0.30 + 0.40*road when
    info=1, and never when info=0. The exposure draw is identical across all arms
    for a given household, so the interaction is not a re-draw artefact.
  * KIN TRANSMISSION IS A STIPULATED ASSUMPTION: tied villages receive +0.22 of
    signal for every household. Tied/untied results are reported for completeness
    and are labelled STIPULATED, not a test of the world.
  * Value_k = V0_k + 0.45*aptitude + SIGNAL_k*(0.16 + 0.34*exposed + 0.22*tied).
  * Travel cost = (0.10 + 0.55*distance)*(1 - 0.55*road)/(1 + seats_k/15), plus
    the level fee and a 0.12 indirect cost.
  * Apply at level k if cash >= cost and value >= cost + work*W_PEN_k.
  * Seats: base (16, 6, 2) for primary/secondary/tertiary, +1 per level with
    teacher supply. Admissions are limited by seats; only admitted pupils reach
    the next level (the diffusion.py within-period progression).
  * Completions = admitted x completion draw (0.78 + 0.06*teacher + 0.08*aptitude).

Because seats bind at every level in this design, the toy's expected pattern is
applications up / admissions flat: information moves queues, not places. That
prediction is predeclared (T15-P3) and reported, not hidden.

Arms: info x road x teacher = 8 factor cells, x 2 village tie types.
Sensitivity (auxiliary, no threshold test): road travel reduction 0.30 not 0.55.
"""
import random

from common import row, verdict

EXPERIMENT = "E15_neighbour_information_roads"

H = 60
LEVELS = ("primary", "secondary", "tertiary")
BASE_SEATS = (16, 6, 2)
TEACHER_SEATS = 1
FEE = (0.19, 0.34, 0.52)
INDIRECT = 0.12
V0 = (0.95, 1.55, 2.15)
APT_VALUE = 0.45
SIGNAL = (0.35, 0.70, 0.95)
SIGNAL_BASE = 0.16
SIGNAL_EXPOSED = 0.34
SIGNAL_TIED = 0.22
EXPOSE_BASE = 0.30
EXPOSE_ROAD = 0.40
ROAD_REDUCTION = 0.55
W_PEN = (0.80, 1.05, 1.30)
P_PASS_BASE = 0.78
P_PASS_TEACHER = 0.06
P_PASS_APT = 0.08

FACTORS = [(info, road, teacher)
           for info in (0, 1) for road in (0, 1) for teacher in (0, 1)]


def cell_label(f):
    return f"info={f[0]}|road={f[1]}|teacher={f[2]}"


def draw(seed):
    """Latents for the untied and tied villages; identical across all arms."""
    rng = random.Random(seed * 5077 + 15)
    villages = []
    for tied in (0, 1):
        hh = dict(
            tied=tied,
            cash=[0.25 + 0.34 * (i % 3) + 0.28 * rng.random() for i in range(H)],
            work=[0.45 + 0.75 * rng.random() for i in range(H)],
            apt=[rng.random() for _ in range(H)],
            dist=[rng.random() for _ in range(H)],
            expo_u=[rng.random() for _ in range(H)],
            pass_u=[[rng.random() for _ in range(H)] for _ in LEVELS],
        )
        order = list(range(H))
        rng.shuffle(order)
        hh["order"] = order
        villages.append(hh)
    return villages


def simulate(village, info, road, teacher, road_reduction=ROAD_REDUCTION):
    """Run the three-level progression for one village; return counts per household."""
    cash, work, apt, dist = (village["cash"], village["work"], village["apt"],
                             village["dist"])
    tie_signal = SIGNAL_TIED * village["tied"]
    expo_p = EXPOSE_BASE + EXPOSE_ROAD * road
    signal = [SIGNAL_BASE + SIGNAL_EXPOSED * (1 if (info and village["expo_u"][i] < expo_p) else 0)
              + tie_signal for i in range(H)]

    hh_apps = [0] * H
    hh_adm = [0] * H
    hh_comp = [0] * H
    apps_by_level = [0, 0, 0]
    prior = list(village["order"])
    for k in range(len(LEVELS)):
        seats = BASE_SEATS[k] + (TEACHER_SEATS if teacher else 0)
        fee = FEE[k] + INDIRECT
        denom = 1.0 + seats / 15.0
        app_set = set()
        for i in prior:
            travel = (0.10 + 0.55 * dist[i]) * (1.0 - road_reduction * road) / denom
            cost = fee + travel
            value = V0[k] + APT_VALUE * apt[i] + SIGNAL[k] * signal[i]
            if cash[i] >= cost and value >= cost + work[i] * W_PEN[k]:
                app_set.add(i)
        admitted = [i for i in village["order"] if i in app_set][:seats]
        for i in app_set:
            hh_apps[i] += 1
        for i in admitted:
            hh_adm[i] += 1
            p = P_PASS_BASE + P_PASS_TEACHER * teacher + P_PASS_APT * apt[i]
            if village["pass_u"][k][i] < p:
                hh_comp[i] += 1
        apps_by_level[k] = len(app_set)
        prior = admitted
        if not prior:
            break

    apps_total = sum(hh_apps)
    adm_total = sum(hh_adm)
    comp_total = sum(hh_comp)
    return dict(apps_total=float(apps_total), adm_total=float(adm_total),
                comp_total=float(comp_total),
                apps_primary=float(apps_by_level[0]),
                apps_secondary=float(apps_by_level[1]),
                apps_tertiary=float(apps_by_level[2]),
                queue_total=float(apps_total - adm_total),
                apps_per_hh=apps_total / H, adm_per_hh=adm_total / H,
                comp_per_hh=comp_total / H,
                completion_rate_pp=100.0 * comp_total / H,
                hh_apps=hh_apps, hh_adm=hh_adm, hh_comp=hh_comp)


METRICS = [
    ("apps_total", "applications", "Total applications across the three levels, pooled over the two villages (120 households)."),
    ("apps_per_hh", "applications/hh", "Applications per household, pooled over the two villages."),
    ("apps_primary", "applications", "Primary-level applications, pooled over the two villages."),
    ("apps_secondary", "applications", "Secondary-level applications (only admitted primary pupils progress)."),
    ("apps_tertiary", "applications", "Tertiary-level applications."),
    ("adm_total", "admissions", "Admissions, capped by seats at each level."),
    ("adm_per_hh", "admissions/hh", "Admissions per household."),
    ("comp_total", "completions", "Completions (admitted x completion draw)."),
    ("completion_rate_pp", "pp of households", "Completions per 100 households."),
    ("queue_total", "applications", "Unmet applications (applications minus admissions)."),
]

QUARTILES = ("q1_nearest", "q4_farthest")


def quartile_masks(village):
    ranked = sorted(range(H), key=lambda i: village["dist"][i])
    return {"q1_nearest": ranked[: H // 4], "q4_farthest": ranked[-(H // 4):]}


def run(seeds):
    n = len(seeds)
    pooled = {f: {m: [] for m, _, _ in METRICS} for f in FACTORS}
    by_tie = {f: {g: {m: [] for m in ("apps_per_hh", "adm_per_hh", "comp_per_hh")}
                  for g in ("untied", "tied")} for f in FACTORS}
    dist_q = {f: {q: {m: [] for m in ("apps_per_hh", "adm_per_hh")} for q in QUARTILES}
              for f in FACTORS}
    sens = {f: {m: [] for m in ("apps_per_hh", "adm_per_hh", "comp_per_hh")}
            for f in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)]}

    for seed in seeds:
        villages = draw(seed)
        masks = [quartile_masks(v) for v in villages]
        for f in FACTORS:
            outs = [simulate(v, f[0], f[1], f[2]) for v in villages]
            for m, _, _ in METRICS:
                pooled[f][m].append(sum(o[m] for o in outs) / 2.0)
            for vi, v in enumerate(villages):
                g = "tied" if v["tied"] else "untied"
                for m in ("apps_per_hh", "adm_per_hh", "comp_per_hh"):
                    by_tie[f][g][m].append(outs[vi][m])
            for q in QUARTILES:
                idx = masks[0][q] + masks[1][q]  # 30 households total (15 per village)
                apps = sum(outs[0]["hh_apps"][i] for i in masks[0][q]) + \
                    sum(outs[1]["hh_apps"][i] for i in masks[1][q])
                adm = sum(outs[0]["hh_adm"][i] for i in masks[0][q]) + \
                    sum(outs[1]["hh_adm"][i] for i in masks[1][q])
                dist_q[f][q]["apps_per_hh"].append(apps / len(idx))
                dist_q[f][q]["adm_per_hh"].append(adm / len(idx))
        for f in sens:
            outs = [simulate(v, f[0], f[1], f[2], road_reduction=0.30) for v in villages]
            for m in ("apps_per_hh", "adm_per_hh", "comp_per_hh"):
                sens[f][m].append(sum(o[m] for o in outs) / 2.0)

    rows = []
    for f in FACTORS:
        for m, unit, definition in METRICS:
            rows.append(row(EXPERIMENT, cell_label(f), "", m, "pooled", pooled[f][m],
                            unit, definition))
        for g in ("untied", "tied"):
            for m in ("apps_per_hh", "adm_per_hh", "comp_per_hh"):
                rows.append(row(EXPERIMENT, cell_label(f), "", m, g, by_tie[f][g][m],
                                "per household",
                                f"{m} for {'kin-tied' if g == 'tied' else 'untied'} villages; tied status is a STIPULATED assumption, reported for completeness."))
        for q in QUARTILES:
            for m in ("apps_per_hh", "adm_per_hh"):
                rows.append(row(EXPERIMENT, cell_label(f), "", m, q, dist_q[f][q][m],
                                "per household",
                                f"{m} among the {'nearest' if q == QUARTILES[0] else 'farthest'} distance quartile (30 households across the two villages)."))
    rows.extend(contrast_rows(pooled, n))
    for f in sens:
        for m in ("apps_per_hh", "adm_per_hh", "comp_per_hh"):
            rows.append(row(EXPERIMENT, cell_label(f) + "|roadcut=0.30", "", m, "sensitivity",
                            sens[f][m], "per household",
                            "Auxiliary sensitivity (NOT a threshold test): road travel reduction 0.30 instead of 0.55."))
    rows.extend(threshold_rows(pooled, n))
    return rows


def _effects(pooled, n):
    def series(fn):
        return [fn(k) for k in range(n)]

    info_r1 = series(lambda k: sum(
        pooled[(1, 1, t)]["apps_per_hh"][k] - pooled[(0, 1, t)]["apps_per_hh"][k]
        for t in (0, 1)) / 2.0)
    info_r0 = series(lambda k: sum(
        pooled[(1, 0, t)]["apps_per_hh"][k] - pooled[(0, 0, t)]["apps_per_hh"][k]
        for t in (0, 1)) / 2.0)
    road_eff = series(lambda k: sum(
        pooled[(i, 1, t)]["apps_per_hh"][k] - pooled[(i, 0, t)]["apps_per_hh"][k]
        for i in (0, 1) for t in (0, 1)) / 4.0)
    teacher_eff = series(lambda k: sum(
        pooled[(i, r, 1)]["completion_rate_pp"][k] - pooled[(i, r, 0)]["completion_rate_pp"][k]
        for i in (0, 1) for r in (0, 1)) / 4.0)
    info_main = series(lambda k: sum(
        pooled[(1, r, t)]["apps_per_hh"][k] - pooled[(0, r, t)]["apps_per_hh"][k]
        for r in (0, 1) for t in (0, 1)) / 4.0)
    adm_info = series(lambda k: sum(
        pooled[(1, r, t)]["adm_per_hh"][k] - pooled[(0, r, t)]["adm_per_hh"][k]
        for r in (0, 1) for t in (0, 1)) / 4.0)
    queue_info = series(lambda k: sum(
        pooled[(1, r, t)]["queue_total"][k] - pooled[(0, r, t)]["queue_total"][k]
        for r in (0, 1) for t in (0, 1)) / 4.0 / H)
    comp_info = series(lambda k: sum(
        pooled[(1, r, t)]["completion_rate_pp"][k] - pooled[(0, r, t)]["completion_rate_pp"][k]
        for r in (0, 1) for t in (0, 1)) / 4.0)
    return dict(info_r1=info_r1, info_r0=info_r0,
                diff=[info_r1[k] - info_r0[k] for k in range(n)],
                road_eff=road_eff, teacher_eff=teacher_eff, info_main=info_main,
                adm_info=adm_info, queue_info=queue_info, comp_info=comp_info)


def contrast_rows(pooled, n):
    e = _effects(pooled, n)
    rows = [
        row(EXPERIMENT, "info=1 vs 0 | road=1", "paired", "info_effect_road1",
            "interaction", e["info_r1"], "applications/hh",
            "Effect of neighbour information on applications per household where road access is high (averaged over teacher arms, paired within seed)."),
        row(EXPERIMENT, "info=1 vs 0 | road=0", "paired", "info_effect_road0",
            "interaction", e["info_r0"], "applications/hh",
            "Effect of neighbour information on applications per household where road access is absent."),
        row(EXPERIMENT, "road=1 vs 0 | info=1 minus info=0", "paired",
            "info_road_interaction", "interaction", e["diff"], "applications/hh",
            "Difference-in-differences: information effect at road=1 minus information effect at road=0."),
        row(EXPERIMENT, "road=1 vs 0", "paired", "road_main_effect", "main",
            e["road_eff"], "applications/hh",
            "Road main effect on applications per household, averaged over info and teacher arms."),
        row(EXPERIMENT, "teacher=1 vs 0", "paired", "teacher_main_effect_completion",
            "main", e["teacher_eff"], "pp of households",
            "Teacher-supply main effect on completions per 100 households."),
        row(EXPERIMENT, "info=1 vs 0", "paired", "info_main_effect", "main",
            e["info_main"], "applications/hh",
            "Information main effect on applications per household."),
        row(EXPERIMENT, "info=1 vs 0", "paired", "info_effect_admissions", "main",
            e["adm_info"], "admissions/hh",
            "Information effect on admissions per household (capacity-capped prediction)."),
        row(EXPERIMENT, "info=1 vs 0", "paired", "info_effect_queue", "main",
            e["queue_info"], "applications/hh",
            "Information effect on unmet applications (queue) per household."),
        row(EXPERIMENT, "info=1 vs 0", "paired", "info_effect_completions", "main",
            e["comp_info"], "pp of households",
            "Information effect on completions per 100 households."),
    ]
    return rows


def threshold_rows(pooled, n):
    e = _effects(pooled, n)
    out = []

    m_r1 = sum(e["info_r1"]) / n
    m_r0 = sum(e["info_r0"]) / n
    m_diff = sum(e["diff"]) / n
    c1 = m_diff >= 0.06 and m_r1 >= 0.10 and m_r0 <= 0.06
    out.append(row(EXPERIMENT, "road=1 interaction", "paired", "threshold_info_interaction",
                   "threshold", e["diff"], "applications/hh",
                   "T15-P1: the information effect on applications per household is >= 0.06 larger with road access than without; the road=1 effect is >= 0.10 and the road=0 effect is <= 0.06. Declared sign: positive interaction.",
                   "T15-P1", "diff >= 0.06; r1 >= 0.10; r0 <= 0.06", verdict([c1])))

    m_road = sum(e["road_eff"]) / n
    m_teacher = sum(e["teacher_eff"]) / n
    m_info = sum(e["info_main"]) / n
    c2 = m_road >= 0.05 and m_teacher >= 2.0 and m_info >= 0.03
    out.append(row(EXPERIMENT, "main effects", "paired", "threshold_main_effects", "threshold",
                   e["road_eff"], "applications/hh",
                   "T15-P2: separable independent effects with declared signs: road main effect on applications >= +0.05/hh, teacher main effect on completion >= +2.0 pp, info main effect on applications >= +0.03/hh (all positive).",
                   "T15-P2", "road >= 0.05; teacher >= 2.0 pp; info >= 0.03", verdict([c2])))

    m_adm = sum(e["adm_info"]) / n
    m_queue = sum(e["queue_info"]) / n
    c3 = abs(m_adm) <= 0.02 and m_queue >= 0.05
    out.append(row(EXPERIMENT, "info=1 vs 0", "paired", "threshold_queues_not_places",
                   "threshold", e["queue_info"], "applications/hh",
                   "T15-P3: information moves queues, not places. Row value = information effect on unmet applications per household; the rule requires that effect >= 0.05/hh AND the information effect on admissions <= 0.02/hh in absolute value (the admissions part is reported in info_effect_admissions). Seats bind at every level in this design.",
                   "T15-P3", "|adm| <= 0.02; queue >= 0.05", verdict([c3])))

    falsified = abs(m_diff) < 0.03
    out.append(row(EXPERIMENT, "falsifier check", "", "falsifier_15_triggered", "falsifier",
                   [1.0 if falsified else 0.0], "0/1",
                   "F15 falsifier 'no interaction': triggered if the difference-in-differences is smaller than 0.03 applications per household in absolute value; the diffusion story would then collapse to capacity.",
                   "F15", "0 = not triggered", verdict([not falsified])))
    return out
