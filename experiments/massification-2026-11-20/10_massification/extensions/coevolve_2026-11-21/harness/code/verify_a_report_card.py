"""Item 1 — re-verify report card A (§7) from the delivered pupil-level files.

Three independent layers, reported separately so they are not conflated:

  L1 ALGEBRA   every delivered aggregates_*.csv cell must satisfy the declared
               definitions exactly (NER = in-band/all-band, GER = all-ages/band,
               out-of-school = band - in-band - higher, denominators = band width
               x declared location cohort size, 0 <= NER <= 1, GER >= NER).
  L2 EXACT     cohort completion / early leaving / transition shares / family
               means recomputed from panel_*.csv pupil records and compared with
               cohorts_*.csv and families_*.csv (tolerance TOL_EXACT).
  L3 SAMPLE    per-year NER/GER recomputed from the declared 1-in-32 pupil-year
               sample (pupilyear_*.csv) with the population frame recovered from
               pupil ids; agreement is tested statistically (z-scores), because
               the full pupil-year table was not delivered — only the sample.

Writes harness/out/A_*.csv and A_summary.json.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C


def f(x):
    """float; empty string = pandas NaN (undefined ratio on an empty age band)."""
    return float("nan") if x is None or str(x).strip() == "" else float(x)


def i(x):
    return int(float(x))


# ---------------------------------------------------------------------------
# L1 — algebra of the delivered aggregates
# ---------------------------------------------------------------------------
def check_algebra():
    checks = []
    worst = {}
    truncated = 0
    bad = []
    for arm in C.ARMS:
        for r in C.agg_rows(arm):
            t, L, loc = i(r["year"]), r["level"], r["location"]
            if L not in C.BAND:
                bad.append((arm, r["seed"], t, L, loc, "unknown level"))
                continue
            lo, hi = C.BAND[L]
            width = hi - lo + 1
            pop = i(r["pop_official_band"])
            enr_b = i(r["enrolled_in_band"])
            enr_a = i(r["enrolled_all_ages"])
            ner, ger = f(r["ner"]), f(r["ger"])
            oos, higher = i(r["out_of_school"]), i(r["at_higher_level"])
            # the population frame holds the burn-in cohorts (entries -11..23) only,
            # so an early-year band can be truncated: count the cohorts that exist
            n_ages = sum(1 for e in range(C.T0, C.N_COHORTS)
                         if lo <= 6 + t - e <= hi)
            expected_pop = n_ages * (C.TOWN_COHORT if loc == "town"
                                     else C.COHORT_SIZE - C.TOWN_COHORT)
            if n_ages < width:
                truncated += 1
            if pop == 0:
                # edge of the cohort frame (no child of that age exists): the ratios
                # must be undefined; no child can be enrolled *in band*, though
                # over-age pupils may still be enrolled at the level
                v = 0.0 if (math.isnan(ner) and math.isnan(ger) and enr_b == 0) else 1.0
                if v > worst.get("empty_cell", 0.0):
                    worst["empty_cell"] = v
                if v > C.TOL_IDENTITY:
                    bad.append((arm, r["seed"], t, L, loc, "empty_cell", v))
                continue
            tests = {
                "denominator": abs(pop - expected_pop),
                "ner_identity": abs(ner - (enr_b / pop)),
                "ger_identity": abs(ger - (enr_a / pop)),
                "oos_identity": abs(oos - (pop - enr_b - higher)),
                "ner_ceiling": max(0.0, ner - 1.0),
                "ger_ge_ner": max(0.0, ner - ger),
                "counts_nonneg": max(0.0, -min(enr_b, enr_a, oos, higher,
                                               i(r["repeaters"]), i(r["over_age"]))),
                "counts_bounded": max(0.0, i(r["over_age"]) - enr_a,
                                      i(r["repeaters"]) - enr_a,
                                      enr_b + higher - pop),
            }
            for k, v in tests.items():
                if v > worst.get(k, 0.0):
                    worst[k] = v
                if v > C.TOL_IDENTITY:
                    bad.append((arm, r["seed"], t, L, loc, k, v))
    checks.append(dict(item="L1 algebra of aggregates_*.csv", n_cells=8640,
                       worst=worst, n_violations=len(bad),
                       n_cells_with_truncated_age_band=truncated,
                       tolerance=C.TOL_IDENTITY,
                       verdict="PASS" if not bad else "FAIL"))
    return checks, bad, worst


# ---------------------------------------------------------------------------
# L2 — exact recomputation of cohort-level report card A from pupil records
# ---------------------------------------------------------------------------
COHORT_METRICS = [
    ("completed_primary_by_age_14", "completed_primary_year", 14),
    ("completed_lower_by_age_18", "completed_lower_year", 18),
    ("completed_upper_by_age_20", "completed_upper_year", 20),
    ("completed_post_non_tertiary_by_age_22", "completed_postsec_year", 22),
    ("completed_tertiary_by_age_26", "completed_tertiary_year", 26),
]


def recompute_cohorts(panel):
    out = {}
    for seed in C.SEEDS:
        rows = panel.seed_rows(seed)
        for c in range(6, 18):
            d = [r for r in rows if r["_entry"] == c]
            birth = c - 6
            rec = {"n_children": len(d)}
            for col, key, age in COHORT_METRICS:
                ok = sum(1 for r in d if r["_" + key] >= 0 and r["_" + key] - birth <= age)
                rec[col] = ok / len(d)
            ent = [r for r in d if r["_attended_secondary"]]
            rec["entered_secondary"] = len(ent) / len(d)
            rec["left_secondary_early_share"] = (
                sum(1 for r in ent if r["_completed_lower_year"] < 0) / len(ent)
                if ent else float("nan"))
            rec["mean_years_completed"] = sum(r["_yc"] for r in d) / len(d)
            out[(seed, c)] = rec
    return out


def check_cohorts():
    diffs = []
    worst = 0.0
    worst_where = None
    n = 0
    for arm in C.ARMS:
        panel = C.Panel(arm)
        re = recompute_cohorts(panel)
        for r in C.cohort_rows(arm):
            key = (i(r["seed"]), i(r["cohort_entry_year"]))
            rec = re[key]
            if i(r["n_children"]) != rec["n_children"]:
                diffs.append((arm, key, "n_children", i(r["n_children"]), rec["n_children"]))
            for col, _, _ in COHORT_METRICS:
                d = abs(f(r[col]) - rec[col])
                n += 1
                if d > worst:
                    worst, worst_where = d, (arm, key, col)
                if d > C.TOL_EXACT:
                    diffs.append((arm, key, col, f(r[col]), rec[col]))
            for col in ("entered_secondary", "left_secondary_early_share",
                        "mean_years_completed"):
                d = abs(f(r[col]) - rec[col])
                n += 1
                if d > worst:
                    worst, worst_where = d, (arm, key, col)
                if d > C.TOL_EXACT:
                    diffs.append((arm, key, col, f(r[col]), rec[col]))
    return dict(item="L2 cohort table recomputed from panel_*.csv", n_values=n,
                max_abs_diff=worst, worst=worst_where, tolerance=C.TOL_EXACT,
                n_disagreements=len(diffs),
                verdict="PASS" if not diffs else "FAIL"), diffs


# ---------------------------------------------------------------------------
# L2b — family means and gains (4 declared family types)
# ---------------------------------------------------------------------------
def recompute_families(panel):
    out = {}
    for seed in C.SEEDS:
        rows = panel.seed_rows(seed)
        for loc, poor in C.FAMILY_TYPES:
            sel = [r["_yc"] for r in rows if r["_rural"] == (1 if loc == "village" else 0)
                   and r["_poor"] == poor]
            out[(seed, loc, poor)] = sum(sel) / len(sel)
    return out


def check_families():
    base = recompute_families(C.Panel("baseline"))
    diffs = []
    n = 0
    worst = 0.0
    worst_where = None
    for arm in C.ARMS:
        re = recompute_families(C.Panel(arm))
        for r in C.family_rows(arm):
            key = (i(r["seed"]), r["loc_type"], i(r["poor"]))
            d = abs(f(r["mean_years_completed"]) - re[key])
            n += 1
            if d > worst:
                worst, worst_where = d, (arm, key, "mean_years_completed")
            if d > C.TOL_EXACT:
                diffs.append((arm, key, "mean_years_completed", f(r["mean_years_completed"]), re[key]))
            if arm != "baseline":
                gain = re[key] - base[key]
                d2 = abs(f(r["gain_vs_baseline"]) - gain)
                n += 1
                if d2 > worst:
                    worst, worst_where = d2, (arm, key, "gain_vs_baseline")
                if d2 > C.TOL_EXACT:
                    diffs.append((arm, key, "gain_vs_baseline", f(r["gain_vs_baseline"]), gain))
    return dict(item="L2b family means/gains recomputed from panel_*.csv", n_values=n,
                max_abs_diff=worst, worst=worst_where, tolerance=C.TOL_EXACT,
                n_disagreements=len(diffs),
                verdict="PASS" if not diffs else "FAIL"), diffs


# ---------------------------------------------------------------------------
# L3 — per-year NER/GER from the declared 1-in-32 pupil-year sample
# ---------------------------------------------------------------------------
def sample_frame():
    """(pupil_id -> (entry_year, loc)) for every sampled id in the population."""
    frame = {}
    for pid in range(0, (C.N_COHORTS + C.N_BURNIN) * C.COHORT_SIZE, C.SAMPLE_MOD):
        frame[pid] = (C.entry_of_ids([pid])[0], C.loc_of_ids([pid])[0])
    return frame


def check_sample():
    frame = sample_frame()
    zs = []
    cells = []
    for arm in C.ARMS:
        py_all = C.read_csv("pupilyear_%s.csv" % arm)
        for seed in C.SEEDS:
            py = [r for r in py_all if i(r["seed"]) == seed]
            by_year_level = {}
            for r in py:
                by_year_level.setdefault((i(r["year"]), r["level"]), set()).add(i(r["pupil_id"]))
            for a in [r for r in C.agg_rows(arm) if i(r["seed"]) == seed]:
                t, L, loc = i(a["year"]), a["level"], a["location"]
                if L not in C.BAND:
                    continue
                lo, hi = C.BAND[L]
                rural = 1 if loc == "rural" else 0
                band = [pid for pid, (e, l) in frame.items()
                        if l == rural and lo <= 6 + t - e <= hi]
                ids = by_year_level.get((t, L), set())
                k = sum(1 for pid in band if pid in ids)
                n = len(band)
                if not n:
                    continue
                est = k / n
                obs = f(a["ner"])
                if math.isnan(obs):
                    continue
                p = min(max(obs, 1e-9), 1 - 1e-9)
                se = max(math.sqrt(p * (1 - p) / n), 0.5 / n)
                z = (est - obs) / se
                zs.append(z)
                cells.append(dict(arm=arm, seed=seed, year=t, level=L, location=loc,
                                  n_sample_band=n, ner_file=obs, ner_sample=est,
                                  ner_z=z, ger_file=f(a["ger"])))
    mean_z = sum(zs) / len(zs)
    sd_z = math.sqrt(sum((z - mean_z) ** 2 for z in zs) / (len(zs) - 1))
    within3 = sum(1 for z in zs if abs(z) <= 3.0) / len(zs)
    within4 = sum(1 for z in zs if abs(z) <= 4.0) / len(zs)
    worst = max(cells, key=lambda c: abs(c["ner_z"]))
    # Pearson r between the sample estimate and the delivered NER
    xs = [c["ner_file"] for c in cells]
    ys = [c["ner_sample"] for c in cells]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs) ** 0.5
    vy = sum((y - my) ** 2 for y in ys) ** 0.5
    r = cov / (vx * vy)
    mad = sum(abs(x - y) for x, y in zip(xs, ys)) / len(xs)
    ok = (abs(mean_z) <= 0.30 and 0.70 <= sd_z <= 1.35
          and within4 >= 0.995 and r >= 0.95 and mad <= 0.05)
    return dict(item="L3 NER recomputed from 1-in-32 pupil-year sample",
                n_cells=len(cells), mean_z=mean_z, sd_z=sd_z,
                share_within_3sigma=within3, share_within_4sigma=within4,
                pearson_r=r, mean_abs_diff=mad,
                max_abs_z=abs(worst["ner_z"]),
                worst=dict(year=worst["year"], level=worst["level"],
                           location=worst["location"], arm=worst["arm"],
                           seed=worst["seed"], ner_file=worst["ner_file"],
                           ner_sample=worst["ner_sample"]),
                acceptance=("consistency band for a declared 1-in-32 sample: "
                            "|mean z|<=0.30; 0.70<=sd(z)<=1.35; >=99.5% within 4 sigma; "
                            "r>=0.95; mean|diff|<=0.05.  Exact reproduction is NOT "
                            "testable: the full pupil-year table was not delivered."),
                verdict="PASS-CONSISTENCY" if ok else "FAIL"), cells
    



def check_totals():
    """Total enrolment per year (all ages, all levels) vs 32 x sampled pupil-years."""
    rows = []
    ok = True
    for arm in C.ARMS:
        agg_all = C.agg_rows(arm)
        py_all = C.read_csv("pupilyear_%s.csv" % arm)
        for seed in C.SEEDS:
            agg = [r for r in agg_all if i(r["seed"]) == seed]
            py = [r for r in py_all if i(r["seed"]) == seed]
            tot = {}
            for a in agg:
                tot[i(a["year"])] = tot.get(i(a["year"]), 0) + i(a["enrolled_all_ages"])
            smp = {}
            for r in py:
                smp[i(r["year"])] = smp.get(i(r["year"]), 0) + 1
            for t in sorted(tot):
                ratio = tot[t] / smp[t] if smp.get(t) else float("nan")
                se = C.SAMPLE_MOD / math.sqrt(max(smp[t], 1))
                z = (ratio - C.SAMPLE_MOD) / se
                rows.append(dict(arm=arm, seed=seed, year=t, enrolled_all=tot[t],
                                 sample_rows=smp.get(t, 0), ratio=ratio, z=z))
                if abs(z) > 4.0:
                    ok = False
    ratios = [r["ratio"] for r in rows]
    return dict(item="L3b total enrolment = 32 x sampled pupil-years",
                n_years=len(rows), mean_ratio=sum(ratios) / len(ratios),
                min_ratio=min(ratios), max_ratio=max(ratios),
                n_outside_4sigma=sum(1 for r in rows if abs(r["z"]) > 4.0),
                verdict="PASS" if ok else "FAIL"), rows


# ---------------------------------------------------------------------------
# selective gate cross-check: panel admissions vs transitions_all_arms.csv
# ---------------------------------------------------------------------------
def check_gate_cross():
    """Gate accounting in transitions_all_arms.csv + admission structure in panel.

    (The panel carries no admission *year*, so admissions cannot be reconciled
    year-by-year to the gate log; what is checkable exactly is the gate
    arithmetic and the panel-side admission structure.)
    """
    P = C.params()
    tr = C.read_csv("transitions_all_arms.csv")
    diffs = []
    n = 0
    for r in tr:
        arm, gate = r["arm"], r["gate"]
        places, qual = i(r["places"]), i(r["qualified"])
        adm, away = i(r["admitted"]), i(r["turned_away"])
        app = i(r["applicants"])
        tests = {
            "admitted_le_qualified_places": max(0, adm - min(qual, places)),
            "turned_away": away - (qual - adm),
            "applicants_ge_qualified": min(0, app - qual),
            "admitted_le_places": min(0, places - adm),
        }
        for k, v in tests.items():
            n += 1
            if abs(v) > 0:
                diffs.append((arm, int(r["seed"]), int(r["year"]), gate, k, v))
        # declared place counts
        if gate == "selective":
            want = int(round(float(P["K_sel"]) *
                             (float(P["selective_expansion_multiplier"])
                              if arm == "selective_expansion" else 1.0)))
        else:
            want = int(P["K_uni"])
        n += 1
        if places != want:
            diffs.append((arm, int(r["seed"]), int(r["year"]), gate,
                          "places_vs_declared", places - want))
    # panel-side admission structure
    adm_panel = 0
    bad = []
    for arm in C.ARMS:
        panel = C.Panel(arm)
        for r in panel.rows:
            if r["_selective_admitted"]:
                adm_panel += 1
                if not r["_selective_attended"]:
                    bad.append((arm, r["seed"], r["pupil_id"], "admitted_not_entered"))
                if not r["_attended_secondary"]:
                    bad.append((arm, r["seed"], r["pupil_id"], "admitted_not_secondary"))
    return dict(item="gate accounting (transitions) + admission structure (panel)",
                n_gate_values=n, n_admissions_in_panel=adm_panel,
                n_structure_violations=len(bad),
                n_disagreements=len(diffs) + len(bad),
                verdict="PASS" if (not diffs and not bad) else "FAIL"), diffs + bad




def derived_portrait():
    """Report card A items with no delivered table to compare against: the
    level-to-level transition portrait and the rural-urban gap, recomputed from
    pupil records.  Reported as DERIVED (arithmetic on SIMULATED records)."""
    rows = []
    for arm in ("baseline",) + tuple(C.REPORT_B_ARMS):
        panel = C.Panel(arm)
        for seed in C.SEEDS:
            rs = panel.seed_rows(seed)
            prim = [r for r in rs if r["_completed_primary_year"] >= 0]
            low = [r for r in rs if r["_completed_lower_year"] >= 0]
            upp = [r for r in rs if r["_completed_upper_year"] >= 0]
            for label, grp in (("all", rs),
                               ("town", [r for r in rs if r["_rural"] == 0]),
                               ("village", [r for r in rs if r["_rural"] == 1])):
                g_prim = [r for r in grp if r["_completed_primary_year"] >= 0]
                g_low = [r for r in grp if r["_completed_lower_year"] >= 0]
                g_upp = [r for r in grp if r["_completed_upper_year"] >= 0]
                g_ent = [r for r in grp if r["_attended_secondary"]]
                rows.append(dict(
                    arm=arm, seed=seed, group=label, n=len(grp),
                    primary_completion=len(g_prim) / len(grp),
                    transition_primary_to_lower=(len(g_low & set()) if False else
                                                 sum(1 for r in grp
                                                     if r["_completed_lower_year"] >= 0
                                                     or r["_attended_secondary"]) / len(g_prim)
                                                 if g_prim else float("nan")),
                    transition_lower_to_upper=(len(g_upp) / len(g_low)
                                               if g_low else float("nan")),
                    transition_upper_to_postsec=(sum(1 for r in grp
                                                     if r["_completed_postsec_year"] >= 0) / len(g_upp)
                                                 if g_upp else float("nan")),
                    transition_upper_to_tertiary=(sum(1 for r in grp
                                                      if r["_completed_tertiary_year"] >= 0) / len(g_upp)
                                                  if g_upp else float("nan")),
                    selective_admission_rate=(sum(1 for r in grp if r["_selective_admitted"]) / len(g_low)
                                              if g_low else float("nan")),
                    mean_years=(sum(r["_yc"] for r in grp) / len(grp)),
                ))
    return rows

# ---------------------------------------------------------------------------
# coverage / definitional measurements (not pass-fail)
# ---------------------------------------------------------------------------
def coverage():
    ner_max, ger_max, n_ger_gt1, n_rows = 0.0, 0.0, 0, 0
    rep_max, over_max = 0, 0
    for arm in C.ARMS:
        for r in C.agg_rows(arm):
            n_rows += 1
            if math.isnan(f(r["ner"])) or math.isnan(f(r["ger"])):
                continue
            ner_max = max(ner_max, f(r["ner"]))
            ger_max = max(ger_max, f(r["ger"]))
            if f(r["ger"]) > 1.0:
                n_ger_gt1 += 1
            rep_max = max(rep_max, i(r["repeaters"]))
            over_max = max(over_max, i(r["over_age"]))
    # upper-secondary split: how much of the declared upper-secondary level is
    # reported under the separate "upper_selective" name
    split = []
    oos_share_selective = []
    base_agg = C.agg_rows("baseline")
    base_by = {(i(x["seed"]), i(x["year"]), x["location"], x["level"]): x for x in base_agg}
    for r in base_agg:
        if r["level"] == "upper_secondary":
            sel = base_by[(i(r["seed"]), i(r["year"]), r["location"], "upper_selective")]
            ner_u, ner_s = f(r["ner"]), f(sel["ner"])
            if ner_u + ner_s > 0:
                split.append(ner_s / (ner_u + ner_s))
            if i(r["out_of_school"]) > 0:
                oos_share_selective.append(i(sel["enrolled_in_band"]) / i(r["out_of_school"]))
    # out-of-school decomposition for lower secondary: children of the band still
    # enrolled BELOW the level are counted as out of school by the declared formula
    frame = sample_frame()
    py = [r for r in C.read_csv("pupilyear_baseline.csv") if i(r["seed"]) == 20261121]
    enrolled = {}
    for r in py:
        enrolled[(i(r["year"]), i(r["pupil_id"]))] = r["level"]
    below_share = []
    for a in [r for r in base_agg if i(r["seed"]) == 20261121
              and r["level"] == "lower_secondary"]:
        t, loc = i(a["year"]), a["location"]
        rural = 1 if loc == "rural" else 0
        lo, hi = C.BAND["lower_secondary"]
        band = [pid for pid, (e, l) in frame.items()
                if l == rural and lo <= 6 + t - e <= hi]
        below = sum(1 for pid in band
                    if enrolled.get((t, pid)) in ("primary",))
        if i(a["out_of_school"]) > 0:
            below_share.append(below / (i(a["out_of_school"]) / C.SAMPLE_MOD))
    return dict(
        item="coverage / definitional measurements (descriptive)",
        n_cell_rows=n_rows, max_ner=ner_max, max_ger=ger_max,
        n_ger_over_100=n_ger_gt1, max_repeaters=rep_max, max_over_age=over_max,
        upper_secondary_selective_share_of_level_mean=(
            sum(split) / len(split) if split else None),
        share_of_upper_secondary_oos_that_is_selective_mean=(
            sum(oos_share_selective) / len(oos_share_selective) if oos_share_selective else None),
        lower_secondary_oos_that_is_children_still_in_primary_share_mean=(
            sum(below_share) / len(below_share) if below_share else None),
        tertiary_band=(C.TERTIARY_BAND[0], C.TERTIARY_BAND[1]),
        tertiary_band_width=C.TERTIARY_BAND[1] - C.TERTIARY_BAND[0] + 1,
        declared_leaving_age=C.SECONDARY_LEAVING_AGE,
        verdict="DESCRIPTIVE")


# ---------------------------------------------------------------------------
def main():
    P = C.params()
    checks = []
    checks_l1, bad, worst = check_algebra()
    checks += checks_l1
    c2, d2 = check_cohorts()
    checks.append(c2)
    c3, d3 = check_families()
    checks.append(c3)
    c4, cells = check_sample()
    checks.append(c4)
    c5, tot = check_totals()
    checks.append(c5)
    c6, d6 = check_gate_cross()
    checks.append(c6)
    cov = coverage()
    checks.append(cov)
    portrait = derived_portrait()
    C.write_csv("A_transitions_derived.csv",
                ["arm", "seed", "group", "n", "primary_completion",
                 "transition_primary_to_lower", "transition_lower_to_upper",
                 "transition_upper_to_postsec", "transition_upper_to_tertiary",
                 "selective_admission_rate", "mean_years"],
                [[r["arm"], r["seed"], r["group"], r["n"]] +
                 ["%.10g" % r[k] for k in ("primary_completion", "transition_primary_to_lower",
                                          "transition_lower_to_upper", "transition_upper_to_postsec",
                                          "transition_upper_to_tertiary", "selective_admission_rate",
                                          "mean_years")] for r in portrait])

    C.write_csv("A_cell_sample_compare.csv",
                ["arm", "seed", "year", "level", "location", "n_sample_band",
                 "ner_file", "ner_sample", "ner_z", "ger_file"],
                [[c["arm"], c["seed"], c["year"], c["level"], c["location"],
                  c["n_sample_band"], "%.10g" % c["ner_file"], "%.10g" % c["ner_sample"],
                  "%.6g" % c["ner_z"], "%.10g" % c["ger_file"]] for c in cells])
    C.write_csv("A_year_totals.csv",
                ["arm", "seed", "year", "enrolled_all", "sample_rows", "ratio", "z"],
                [[r["arm"], r["seed"], r["year"], r["enrolled_all"], r["sample_rows"],
                  "%.10g" % r["ratio"], "%.4f" % r["z"]] for r in tot])
    if d2 or d3 or d6:
        C.write_csv("A_disagreements.csv", ["item", "arm", "key", "field", "file", "recomputed"],
                    [[x[0], x[1], str(x[2]), x[3], x[4], x[5]] for x in
                     ([(c2["item"],) + tuple(x) for x in d2] +
                      [(c3["item"],) + tuple(x) for x in d3] +
                      [(c6["item"],) + tuple(x) for x in d6])])
    C.write_json("A_summary.json", {"label": "SIMULATED", "checks": checks,
                                    "declared_bands": {k: list(v) for k, v in C.BAND.items()},
                                    "note": ("Every number is SIMULATED (model) or DERIVED "
                                             "(arithmetic on SIMULATED pupil records). "
                                             "No observed series is used.")})
    for c in checks:
        print("%-62s %s" % (c["item"], c.get("verdict")))
        for k, v in c.items():
            if k not in ("item", "verdict"):
                print("    %-42s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
