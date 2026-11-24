#!/usr/bin/env python3
"""E8 — Fisher randomization inference (placebo permutations) for the CS event study.

Pre-registration: research/records/2026-11-25-e8-fisher-ri/PRE_REGISTRATION.md (commit 4e466a3),
written and committed before any run. This script implements it verbatim.

Estimator (cited, not rebuilt): `att_cs` in
research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py @ commit
bd782be4d15c834f054b1ecc650e54565f6b292f — Callaway–Sant'Anna ATT(g,t) with universal base period g-1,
not-yet-treated controls (never-treated allowed, >=3 controls), event time -5..+6 (event -1 is skipped by
the cited code because t == g-1 == base), cohort-size-weighted event aggregation. The vectorised
re-implementation below is verified against the cited `att_cs` on the observed assignment to
max abs difference < 1e-10 before any permutation is run (results/e8_ri_results.json -> verifier).

Test statistics (fixed in the pre-registration):
  T0    = CS ATT at event time e = 0   (primary)
  Tpost = unweighted mean of event ATTs e = +1..+6 (secondary)

Permutation families (B = 10,000 each, master seed 20261125, per-permutation RNG
default_rng([20261125, family_code, i])):
  P1 placebo-date    (family_code=1): keep the 8 treated countries, redraw each date uniformly from its
                     feasible window W_c = {y in 1990..2010 : outcome non-missing in y-1 and y} minus
                     {g_c-2..g_c+2}; countries drawn independently in ascending ISO3 order.
  P2 placebo-country (family_code=2): keep the 8 dates, draw 8 never-treated SSA countries without
                     replacement (P sorted ascending ISO3) and apply a uniform random date bijection in
                     the ISO3 order of the drawn countries.

p-values: two-sided p2 = (1 + #{|T_perm| >= |T_obs|}) / (B_eff + 1);
          one-sided-positive p+ = (1 + #{T_perm >= T_obs}) / (B_eff + 1);
          Monte Carlo SE = sqrt(p(1-p)/(B_eff+1)); undefined permutations are excluded and B_eff reported.

Data: committed data/e8_primary_ger_panel.csv (WDI SE.PRM.ENRR, bulk vintage Last Updated 2026-11-11)
and data/wdi_region_map.csv; the reproduction gate scripts/repro_gate.py must pass first (it does).

Run:  /Users/treymenefee/neon-boot/venv/bin/python scripts/e8_ri.py
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import warnings
from collections import Counter

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)
BASE = os.path.abspath(os.path.join(RECORD, "..", "2026-11-25-e6e8-sequencing"))
WORKTREE = os.path.abspath(os.path.join(RECORD, "..", "..", ".."))
DATA = os.path.join(RECORD, "data")
RES = os.path.join(RECORD, "results")
CITED_COMMIT = "bd782be4d15c834f054b1ecc650e54565f6b292f"
PREREG_COMMIT = "4e466a316f4b219c256a45dbf5a1ce8ea8deb11b"
DATA_GATE_COMMIT = "263bef238e5ac7baffacecdf37c37c0c288abb02"
CITED_REL = "research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py"
PANEL = os.path.join(DATA, "e8_primary_ger_panel.csv")
REGION = os.path.join(DATA, "wdi_region_map.csv")
GATE = os.path.join(RES, "repro_gate.json")
OUT_JSON = os.path.join(RES, "e8_ri_results.json")
OUT_CSV = os.path.join(RES, "e8_ri_perms.csv.gz")
OUT_SUMMARY = os.path.join(RES, "e8_ri_summary.csv")

MASTER_SEED = 20261125
B = 10000
FAMILY = {"placebo_date": 1, "placebo_country": 2}
EVENTS = [-5, -4, -3, -2, 0, 1, 2, 3, 4, 5, 6]   # event -1 is not estimable in the cited att_cs
POST_EVENTS = [1, 2, 3, 4, 5, 6]
YEAR_LO, YEAR_HI = 1990, 2015
YEARS = list(range(YEAR_LO, YEAR_HI + 1))
YEAR_IX = {y: i for i, y in enumerate(YEARS)}
N_WORKERS = 8
_DATE_EXCLUDE = 2          # exclude true date +/- 2 in P1
_WINDOW = (1990, 2010)     # P1 feasible abolition years

# globals inherited by forked workers
G = {}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", WORKTREE] + list(args), capture_output=True, text=True, check=True).stdout.strip()


def is_ancestor(sha):
    return subprocess.run(["git", "-C", WORKTREE, "merge-base", "--is-ancestor", sha, "HEAD"],
                          capture_output=True).returncode == 0


# ----------------------------------------------------------------------------------------------
# data + observed assignment
# ----------------------------------------------------------------------------------------------
def load_inputs():
    panel = pd.read_csv(PANEL)
    reg = pd.read_csv(REGION)
    ssa = set(reg.loc[reg.Region.fillna("").str.contains("Sub-Saharan"), "iso3"])
    countries = sorted(set(panel.iso3) & ssa)
    cix = {c: i for i, c in enumerate(countries)}
    M = np.full((len(countries), len(YEARS)), np.nan)
    for iso, g in panel.groupby("iso3"):
        if iso in cix:
            for y, v in zip(g.year.astype(int), g.value.astype(float)):
                if y in YEAR_IX:
                    M[cix[iso], YEAR_IX[y]] = v
    fee = pd.read_csv(os.path.join(BASE, "data", "fee_dates.csv"))
    ver = fee[fee.status == "VERIFIED"].copy()
    coh_obs = {r.iso3: int(r.preferred_year) for r in ver.itertuples() if r.iso3 in cix}
    all12 = {r.iso3: int(r.script_date) for r in fee.itertuples()
             if r.iso3 in cix and pd.notna(pd.to_numeric(r.script_date, errors="coerce"))}
    return panel, countries, cix, M, coh_obs, all12


# ----------------------------------------------------------------------------------------------
# vectorised re-implementation of the cited att_cs, returning the two RI statistics
# ----------------------------------------------------------------------------------------------
def event_stats(cohort, M, cix):
    """CS event-time ATTs (universal base g-1, not-yet-treated controls) for one assignment.

    cohort: country -> abolition year. M: countries x years matrix (NaN missing). cix: country -> row.
    The never-treated mask and not-yet-treated rule are derived from `cohort` itself, so placebo
    assignments are evaluated with exactly the same control rule as the observed assignment.
    Returns dict: T0, Tpost, n_t0, n_post_events, event_atts {event: att}.
    """
    tcs = sorted(cohort)
    k = len(tcs)
    rows = np.array([cix[c] for c in tcs])
    gvec = np.array([cohort[c] for c in tcs], dtype=float)
    att_mat = np.full((len(EVENTS), k), np.nan)
    gyear_f = np.full(M.shape[0], np.nan)
    for c, g in cohort.items():
        gyear_f[cix[c]] = float(g)
    is_treated = ~np.isnan(gyear_f)
    for ei, e in enumerate(EVENTS):
        tvec = gvec + e
        bvec = gvec - 1.0
        thr = np.maximum(tvec, bvec)
        for j in range(k):
            ti = YEAR_IX.get(int(tvec[j])) if tvec[j] == int(tvec[j]) else None
            bi = YEAR_IX.get(int(bvec[j]))
            if ti is None or bi is None:
                continue
            dy = M[:, ti] - M[:, bi]
            valid = ~np.isnan(dy)
            ctrl = ((~is_treated) | (gyear_f > thr[j])) & valid
            ctrl[rows[j]] = False
            nctrl = int(ctrl.sum())
            if nctrl < 3:
                continue
            dy_g = dy[rows[j]]
            if np.isnan(dy_g):
                continue
            att_mat[ei, j] = dy_g - float(np.mean(dy[ctrl]))
    appears = ~np.all(np.isnan(att_mat), axis=0)
    sizes = Counter(int(gvec[j]) for j in range(k) if appears[j])
    tot = float(sum(sizes.values()))
    w = np.array([sizes[int(gvec[j])] / tot if appears[j] else np.nan for j in range(k)])
    event_atts, n_t0 = {}, 0
    agg = np.full(len(EVENTS), np.nan)
    for ei, e in enumerate(EVENTS):
        sel = ~np.isnan(att_mat[ei])
        ws = w[sel]
        if len(ws) == 0 or np.nansum(ws) == 0:
            continue
        agg[ei] = float(np.average(att_mat[ei, sel], weights=ws))
        if e == 0:
            n_t0 = int(sel.sum())
    for ei, e in enumerate(EVENTS):
        if not np.isnan(agg[ei]):
            event_atts[e] = float(agg[ei])
    i0 = EVENTS.index(0)
    T0 = float(agg[i0]) if not np.isnan(agg[i0]) else np.nan
    post_vals = [agg[EVENTS.index(e)] for e in POST_EVENTS if not np.isnan(agg[EVENTS.index(e)])]
    Tpost = float(np.mean(post_vals)) if post_vals else np.nan
    return dict(T0=T0, Tpost=Tpost, n_t0=n_t0, n_post_events=len(post_vals), event_atts=event_atts)


def cited_att_cs():
    """Import a byte-identical temp copy of the cited bd782be script (no writes to the cited record)."""
    src = os.path.join(WORKTREE, CITED_REL)
    tmp = tempfile.mkdtemp(prefix="e8_ri_cited_")
    os.makedirs(os.path.join(tmp, "scripts"), exist_ok=True)
    dst = os.path.join(tmp, "scripts", "e8_fee_event_study.py")
    shutil.copyfile(src, dst)
    spec = importlib.util.spec_from_file_location("e8_base_bd782be", dst)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["e8_base_bd782be"] = mod
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        spec.loader.exec_module(mod)
    return mod, src, tmp


def Y_from_matrix(M, countries):
    return {c: {YEARS[j]: float(M[i, j]) for j in range(len(YEARS)) if not np.isnan(M[i, j])}
            for i, c in enumerate(countries)}


# ----------------------------------------------------------------------------------------------
# permutation workers (forked; inherit G)
# ----------------------------------------------------------------------------------------------
def _perm_date(i):
    rng = np.random.default_rng([MASTER_SEED, FAMILY["placebo_date"], i])
    coh = {}
    for c in G["treated_sorted"]:
        W = G["windows"][c]
        coh[c] = int(W[int(rng.integers(0, len(W)))])
    return coh


def _perm_country(i):
    rng = np.random.default_rng([MASTER_SEED, FAMILY["placebo_country"], i])
    drawn = sorted(G["pool"][j] for j in rng.choice(len(G["pool"]), size=len(G["treated_sorted"]), replace=False))
    perm = rng.permutation(len(drawn))
    dates = G["dates_sorted"]
    return {c: int(dates[perm[j]]) for j, c in enumerate(drawn)}


def run_chunk(task):
    family, lo, hi = task
    draw = _perm_date if family == "placebo_date" else _perm_country
    out = []
    for i in range(lo, hi):
        st = event_stats(draw(i), G["M"], G["cix"])
        out.append((family, i, st["T0"], st["Tpost"], st["n_t0"], st["n_post_events"]))
    return out


# ----------------------------------------------------------------------------------------------
# p-values / distributions
# ----------------------------------------------------------------------------------------------
def perm_summary(obs, vals, B_eff, label):
    v = np.asarray(vals, dtype=float)
    v = v[~np.isnan(v)]
    B_eff = int(B_eff)
    if len(v) == 0:
        return dict(label=label, B_eff=B_eff, defined=0)
    T = float(obs)
    k2 = int(np.sum(np.abs(v) >= abs(T)))
    kp = int(np.sum(v >= T))
    p2 = (1 + k2) / (B_eff + 1)
    pp = (1 + kp) / (B_eff + 1)
    qs = np.quantile(v, [0.025, 0.05, 0.25, 0.5, 0.75, 0.95, 0.975]).tolist()
    return dict(label=label, B_eff=B_eff, defined=int(len(v)), T_obs=T,
                dist=dict(mean=float(np.mean(v)), sd=float(np.std(v, ddof=1)), min=float(np.min(v)),
                          max=float(np.max(v)), quantiles_2p5_5_25_50_75_95_97p5=qs,
                          n_ge_obs=kp, n_abs_ge_obs=k2),
                p_two_sided=float(p2), p_one_sided_positive=float(pp),
                mcse_two_sided=float(np.sqrt(p2 * (1 - p2) / (B_eff + 1))),
                mcse_one_sided_positive=float(np.sqrt(pp * (1 - pp) / (B_eff + 1))))


def classify(p2_date_T0, p2_country_T0, p2_date_Tpost, p2_country_Tpost):
    if (p2_date_T0 < 0.05 and p2_country_T0 < 0.05 and p2_date_Tpost < 0.05 and p2_country_Tpost < 0.05):
        return "robust"
    if p2_date_T0 < 0.05 and p2_country_T0 < 0.05:
        return "partially robust"
    return "not distinguishable from placebo"


# ----------------------------------------------------------------------------------------------
def main():
    t_start = time.time()
    warnings.filterwarnings("ignore")
    os.makedirs(RES, exist_ok=True)
    gate = json.load(open(GATE))
    if not gate.get("gate_pass"):
        sys.exit("reproduction gate did not pass — refusing to run permutations (pre-registered stop)")

    panel, countries, cix, M, coh_obs, all12 = load_inputs()
    gyear = np.full(len(countries), np.nan)
    for c, g in coh_obs.items():
        gyear[cix[c]] = g
    treated_sorted = sorted(coh_obs)
    dates_sorted = np.array([coh_obs[c] for c in treated_sorted])
    pool = sorted([c for c in countries if c not in coh_obs])

    # P1 windows
    windows = {}
    for c in treated_sorted:
        g = coh_obs[c]
        W = [y for y in range(_WINDOW[0], _WINDOW[1] + 1)
             if (y - 1 in YEAR_IX) and (y in YEAR_IX)
             and not np.isnan(M[cix[c], YEAR_IX[y - 1]]) and not np.isnan(M[cix[c], YEAR_IX[y]])
             and not (g - _DATE_EXCLUDE <= y <= g + _DATE_EXCLUDE)]
        windows[c] = W
    if any(len(w) == 0 for w in windows.values()):
        sys.exit("empty placebo-date window — pre-registered stop")

    # ---- observed statistics + verification against the cited att_cs ----
    obs = event_stats(coh_obs, M, cix)
    mod, cited_src, cited_tmp = cited_att_cs()
    Y = Y_from_matrix(M, countries)
    _, cited_ev = mod.att_cs(Y, coh_obs, YEARS)
    cited = {int(r.event): float(r.att) for r in cited_ev.itertuples()}
    diffs = {e: abs(obs["event_atts"][e] - cited[e]) for e in EVENTS if e in cited and e in obs["event_atts"]}
    cited_post = float(np.mean([cited[e] for e in POST_EVENTS if e in cited]))
    verifier = dict(cited_commit=CITED_COMMIT, cited_script_sha256=sha256_file(cited_src),
                    event_events_compared=sorted(diffs), max_abs_diff_event_atts=float(max(diffs.values())),
                    T0_vectorised=obs["T0"], T0_cited=cited[0], abs_diff_T0=float(abs(obs["T0"] - cited[0])),
                    Tpost_vectorised=obs["Tpost"], Tpost_cited=cited_post, abs_diff_Tpost=float(abs(obs["Tpost"] - cited_post)),
                    tolerance=1e-10,
                    pass_=bool(max(diffs.values()) < 1e-10 and abs(obs["T0"] - cited[0]) < 1e-10
                               and abs(obs["Tpost"] - cited_post) < 1e-10))
    shutil.rmtree(cited_tmp, ignore_errors=True)
    if not verifier["pass_"]:
        sys.exit("vectorised re-implementation does not match cited att_cs — pre-registered stop")
    print(f"observed T0={obs['T0']:.10f} Tpost={obs['Tpost']:.10f} "
          f"n_t0={obs['n_t0']} n_post={obs['n_post_events']} (verifier max|d|={verifier['max_abs_diff_event_atts']:.2e})")

    # ---- permutations ----
    G.update(M=M, cix=cix, gyear=gyear, treated_sorted=treated_sorted, windows=windows,
             pool=pool, dates_sorted=dates_sorted)
    import multiprocessing as mp
    ctx = mp.get_context("fork")
    n_chunks = 2 * N_WORKERS
    tasks = [("placebo_date", int(B * j / n_chunks), int(B * (j + 1) / n_chunks)) for j in range(n_chunks)]
    tasks += [("placebo_country", int(B * j / n_chunks), int(B * (j + 1) / n_chunks)) for j in range(n_chunks)]
    with ctx.Pool(N_WORKERS) as p:
        chunks = p.map(run_chunk, tasks)
    rows = [r for ch in chunks for r in ch]
    df = pd.DataFrame(rows, columns=["family", "perm", "T0", "Tpost", "n_t0", "n_post_events"])
    df = df.sort_values(["family", "perm"]).reset_index(drop=True)
    assert len(df) == 2 * B, len(df)
    df.to_csv(OUT_CSV, index=False, compression="gzip")
    print(f"permutations done in {time.time() - t_start:.1f}s; wrote {OUT_CSV}")

    # ---- determinism spot check: recompute a few perms serially in the parent ----
    spot = {}
    for fam in FAMILY:
        draw = _perm_date if fam == "placebo_date" else _perm_country
        sub = df[df.family == fam]
        for i in (0, B // 2, B - 1):
            st = event_stats(draw(i), M, cix)
            r = sub[sub.perm == i].iloc[0]
            spot[f"{fam}:{i}"] = dict(serial_T0=st["T0"], csv_T0=float(r.T0),
                                      abs_diff_T0=abs(st["T0"] - float(r.T0)),
                                      serial_Tpost=st["Tpost"], csv_Tpost=float(r.Tpost),
                                      abs_diff_Tpost=abs(st["Tpost"] - float(r.Tpost)))
    spot_ok = all(v["abs_diff_T0"] < 1e-12 and v["abs_diff_Tpost"] < 1e-12 for v in spot.values())

    # ---- family summaries ----
    fam_out = {}
    for fam in FAMILY:
        sub = df[df.family == fam]
        T0v = sub.T0.values.astype(float)
        Tpv = sub.Tpost.values.astype(float)
        fam_out[fam] = dict(
            B=B, B_eff_T0=int(np.sum(~np.isnan(T0v))), B_eff_Tpost=int(np.sum(~np.isnan(Tpv))),
            T0=perm_summary(obs["T0"], T0v, int(np.sum(~np.isnan(T0v))), "T0"),
            Tpost=perm_summary(obs["Tpost"], Tpv, int(np.sum(~np.isnan(Tpv))), "Tpost"),
            n_t0_dist=dict(mean=float(sub.n_t0.mean()), min=int(sub.n_t0.min()), max=int(sub.n_t0.max())),
            n_post_events_dist=dict(mean=float(sub.n_post_events.mean()), min=int(sub.n_post_events.min()),
                                    max=int(sub.n_post_events.max())))

    d = fam_out["placebo_date"]
    k = fam_out["placebo_country"]
    cls = classify(d["T0"]["p_two_sided"], k["T0"]["p_two_sided"],
                   d["Tpost"]["p_two_sided"], k["Tpost"]["p_two_sided"])

    # flat summary table (one row per family x statistic) for the claims -> source map
    summ = []
    for fam in FAMILY:
        n0 = fam_out[fam]["n_t0_dist"]
        for stat in ("T0", "Tpost"):
            s_ = fam_out[fam][stat]
            dd = s_["dist"]
            q = dd["quantiles_2p5_5_25_50_75_95_97p5"]
            summ.append(dict(family=fam, statistic=stat, T_obs=s_["T_obs"],
                             perm_mean=dd["mean"], perm_sd=dd["sd"], perm_min=dd["min"], perm_max=dd["max"],
                             q2_5=q[0], q5=q[1], q25=q[2], q50=q[3], q75=q[4], q95=q[5], q97_5=q[6],
                             n_abs_ge_obs=dd["n_abs_ge_obs"], n_ge_obs=dd["n_ge_obs"], B_eff=s_["B_eff"],
                             p_two_sided=s_["p_two_sided"], p_one_sided_positive=s_["p_one_sided_positive"],
                             mcse_two_sided=s_["mcse_two_sided"],
                             mcse_one_sided_positive=s_["mcse_one_sided_positive"],
                             n_t0_mean=n0["mean"], n_t0_min=n0["min"], n_t0_max=n0["max"]))
    pd.DataFrame(summ).to_csv(OUT_SUMMARY, index=False)

    def _fmt(x):
        return (f"T0 obs={x['T0']['T_obs']:.6f} p2={x['T0']['p_two_sided']:.6f} "
                f"p+={x['T0']['p_one_sided_positive']:.6f}")

    out = dict(
        meta=dict(record="research/records/2026-11-25-e8-fisher-ri",
                  prereg_commit=PREREG_COMMIT,
                  prereg_is_ancestor_of_head=is_ancestor(PREREG_COMMIT),
                  data_gate_commit=DATA_GATE_COMMIT,
                  data_gate_is_ancestor_of_head=is_ancestor(DATA_GATE_COMMIT),
                  git_head=git("rev-parse", "HEAD"), cited_commit=CITED_COMMIT,
                  master_seed=MASTER_SEED, B=B, families=FAMILY, events=EVENTS, post_events=POST_EVENTS,
                  workers=N_WORKERS, command="/Users/treymenefee/neon-boot/venv/bin/python scripts/e8_ri.py",
                  numpy=np.__version__, pandas=pd.__version__,
                  wdi_last_updated_date=open(os.path.join(DATA, "SHA256SUMS")).readline().strip().split("=")[-1],
                  reproducible_gate="results/repro_gate.json (gate_pass=true)",
                  reproduction_gate_summary={k: gate["estimator_reproduction"][k] for k in
                                             ["att0_reproduced", "att0_committed", "att0_absdiff",
                                              "se_boot0_reproduced", "se_boot0_committed", "se_boot0_absdiff",
                                              "max_abs_diff_att_11_events", "max_abs_diff_se_boot_11_events"]}),
        sample=dict(ssa_countries=len(countries), treated=coh_obs, treated_estranged=None,
                    placebo_country_pool=pool, n_pool=len(pool),
                    placebo_date_windows={c: windows[c] for c in treated_sorted}),
        observed=dict(T0=obs["T0"], Tpost=obs["Tpost"], n_t0=obs["n_t0"],
                      n_post_events=obs["n_post_events"],
                      event_atts=obs["event_atts"],
                      cited_att_cs_event_atts={str(e): cited[e] for e in sorted(cited)}),
        verifier=verifier,
        families=fam_out,
        decision=dict(classification=cls,
                      rule="PRE_REGISTRATION.md §9: robust = all four two-sided p<0.05; "
                           "partially robust = T0 both families <0.05 but not all four; else not distinguishable",
                      implies=({"robust": "consistent with a date-specific association; RI passes both placebo schemes",
                                "partially robust": "RI check is statistic/scheme-dependent; report as such",
                                "not distinguishable from placebo": "date-specific association NOT supported by randomization inference; E8 first-stage claim downgraded to descriptive"}[cls])),
        t_star=dict(status="NOT-ESTIMABLE", t_abolition_sourced="8/8", L_primary_sourced="0/8",
                     t_star_sourced="0/8", no_proxy=True,
                     citation="paper2/PREREGISTRATION_BULGE_ARRIVAL.md and paper2/BULGE_ARRIVAL_STATUS.md "
                              "@ origin/research/bulge-arrival-2026-11-25 @ 1b91a71"),
        determinism=dict(spot_checks=spot, pass_=spot_ok,
                         derivation="numpy.random.default_rng([20261125, family_code, i]); "
                                    "independent per permutation, parallel-order invariant"),
        files=dict(perms_csv=os.path.relpath(OUT_CSV, RECORD), perms_csv_sha256=sha256_file(OUT_CSV),
                   summary_csv=os.path.relpath(OUT_SUMMARY, RECORD),
                   summary_csv_sha256=sha256_file(OUT_SUMMARY),
                   results_json="results/e8_ri_results.json",
                   panel_sha256=sha256_file(PANEL)),
        runtime_seconds=round(time.time() - t_start, 1),
    )
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n== {_fmt(d)}; country {_fmt(k)}")
    print(f"== classification: {cls}")
    print(f"wrote {OUT_JSON}")

    # compact console summary
    for fam in FAMILY:
        for stat in ("T0", "Tpost"):
            s = fam_out[fam][stat]
            print(f"{fam:16s} {stat:5s} obs={s['T_obs']:9.4f} mean={s['dist']['mean']:9.4f} "
                  f"sd={s['dist']['sd']:8.4f} p2={s['p_two_sided']:.6f} p+={s['p_one_sided_positive']:.6f} "
                  f"B_eff={s['B_eff']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
