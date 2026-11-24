#!/usr/bin/env python3
"""E8 Fisher RI — **EXPLORATORY POST-HOC** follow-up probes A1 and A2.

⚠ EXPLORATORY / POST-HOC. This script implements `PRE_REGISTRATION_FOLLOWUP.md` (commit 078dd7f), which was
committed before either probe was run. It does NOT change the confirmatory record (`PRE_REGISTRATION.md`,
`REPORT.md`, `results/e8_ri_results.json`).

Machinery is imported unchanged from `scripts/e8_ri.py` (same committed panel, same cited bd782be att_cs logic via
`event_stats`, same statistics T0 = CS ATT(e=0) and Tpost = mean CS ATT(e=+1..+6), same p-value/MCSE formulas, same
master seed 20261125 and per-permutation RNG derivation). Only the probe's window/pool changes:

  A1  placebo-country with P' = confirmatory 40-country never-treated pool MINUS {CMR, ZMB, RWA, BDI} (|P'|=36),
      family_code = 2 (same RNG streams as confirmatory P2), same draw rule.
  A2  local placebo-date: W_c^local = {g_c-3, g_c+3} ∩ W_c (confirmatory feasible window, true date +/-2 still
      excluded), family_code = 1 (same RNG streams as confirmatory P1), same draw rule.

B = 10,000 per probe; host-only fork Pool(8).

Run:  /Users/treymenefee/neon-boot/venv/bin/python scripts/e8_ri_followup.py
"""
import hashlib
import json
import os
import subprocess
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)
RES = os.path.join(RECORD, "results")
WORKTREE = os.path.abspath(os.path.join(RECORD, "..", "..", ".."))
sys.path.insert(0, HERE)
import e8_ri as base  # noqa: E402  (the confirmatory machinery, imported unchanged)

LABEL = "EXPLORATORY POST-HOC"
CONFIRMATORY_COMMIT = "3535e49da411946b969dfb978773eaee4928b835"
PREREG_FOLLOWUP_COMMIT = "078dd7f280250e1359837adc7f73f453e1f6fa0c"
UNRESOLVED = ["CMR", "ZMB", "RWA", "BDI"]
OUT_JSON = os.path.join(RES, "e8_ri_followup.json")
OUT_CSV = os.path.join(RES, "e8_ri_followup_perms.csv.gz")
B = base.B
N_WORKERS = 8


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", WORKTREE] + list(args), capture_output=True, text=True, check=True).stdout.strip()


def run_probe(family):
    """Run B permutations for one probe via the confirmatory harness (fork Pool, same run_chunk)."""
    import multiprocessing as mp
    n_chunks = 2 * N_WORKERS
    tasks = [(family, int(B * j / n_chunks), int(B * (j + 1) / n_chunks)) for j in range(n_chunks)]
    ctx = mp.get_context("fork")
    with ctx.Pool(N_WORKERS) as p:
        chunks = p.map(base.run_chunk, tasks)
    rows = [r for ch in chunks for r in ch]
    df = pd.DataFrame(rows, columns=["family", "perm", "T0", "Tpost", "n_t0", "n_post_events"])
    return df.sort_values("perm").reset_index(drop=True)


def summarize(df, label, obs):
    T0v = df.T0.values.astype(float)
    Tpv = df.Tpost.values.astype(float)
    b0 = int(np.sum(~np.isnan(T0v)))
    bp = int(np.sum(~np.isnan(Tpv)))
    return dict(
        label=label, B=len(df), B_eff_T0=b0, B_eff_Tpost=bp,
        T0=base.perm_summary(obs["T0"], T0v, b0, "T0"),
        Tpost=base.perm_summary(obs["Tpost"], Tpv, bp, "Tpost"),
        n_t0_dist=dict(mean=float(df.n_t0.mean()), min=int(df.n_t0.min()), max=int(df.n_t0.max()),
                       share_eq_8=float(np.mean(df.n_t0 == 8))),
        n_post_events_dist=dict(mean=float(df.n_post_events.mean()), min=int(df.n_post_events.min()),
                                max=int(df.n_post_events.max())))


def reading(summary):
    """Pre-registered follow-up reading rule (PRE_REGISTRATION_FOLLOWUP.md §5)."""
    p_t0 = summary["T0"]["p_two_sided"]
    p_tp = summary["Tpost"]["p_two_sided"]
    if p_t0 < 0.05 and p_tp < 0.05:
        return "unaffected"
    if p_t0 < 0.05:
        return "partially sensitive"
    return "sensitive"


def spot_check(df, draw_fn, probe_keys):
    out = {}
    for i in (0, B // 2, B - 1):
        st = base.event_stats(draw_fn(i), base.G["M"], base.G["cix"])
        r = df[df.perm == i].iloc[0]
        out[f"{probe_keys}:{i}"] = dict(
            serial_T0=st["T0"], csv_T0=float(r.T0), abs_diff_T0=abs(st["T0"] - float(r.T0)),
            serial_Tpost=st["Tpost"], csv_Tpost=float(r.Tpost), abs_diff_Tpost=abs(st["Tpost"] - float(r.Tpost)))
    return out


def main():
    t0 = time.time()
    os.makedirs(RES, exist_ok=True)
    gate = json.load(open(base.GATE))
    if not gate.get("gate_pass"):
        sys.exit("confirmatory reproduction gate is not passing — stop (follow-up pre-registration §7)")
    conf = json.load(open(base.OUT_JSON))
    panel, countries, cix, M, coh_obs, all12 = base.load_inputs()
    panel_sha = sha256_file(base.PANEL)
    if panel_sha != conf["files"]["panel_sha256"]:
        sys.exit("committed panel sha256 changed vs confirmatory record — stop (follow-up pre-registration §7)")
    treated_sorted = sorted(coh_obs)
    dates_sorted = np.array([coh_obs[c] for c in treated_sorted])
    obs = base.event_stats(coh_obs, M, cix)
    if abs(obs["T0"] - conf["observed"]["T0"]) > 1e-12 or abs(obs["Tpost"] - conf["observed"]["Tpost"]) > 1e-12:
        sys.exit("observed T0/Tpost do not match confirmatory JSON to 1e-12 — stop (follow-up pre-registration §7)")
    print(f"observed T0={obs['T0']:.10f} Tpost={obs['Tpost']:.10f}; panel sha {panel_sha[:12]}…")

    pool_full = sorted([c for c in countries if c not in coh_obs])
    pool_excl = [c for c in pool_full if c not in UNRESOLVED]
    if len(pool_excl) != 36:
        sys.exit(f"A1 pool is {len(pool_excl)}, pre-registered 36 — stop")

    # ---------------------------------------------------------------- A1
    base.G.update(M=M, cix=cix, treated_sorted=treated_sorted, pool=pool_excl, dates_sorted=dates_sorted)
    df1 = run_probe("placebo_country")
    assert len(df1) == B, len(df1)
    a1 = summarize(df1, "A1_placebo_country_pool36_excl_unresolved", obs)
    a1["pool_excluded"] = UNRESOLVED
    a1["n_pool"] = len(pool_excl)
    a1["pool"] = pool_excl
    a1["spot_checks"] = spot_check(df1, base._perm_country, "A1")
    print(f"A1 done ({time.time() - t0:.0f}s): p2(T0)={a1['T0']['p_two_sided']:.6g} "
          f"p2(Tpost)={a1['Tpost']['p_two_sided']:.6g} B_eff={a1['B_eff_T0']}/{a1['B_eff_Tpost']}")

    # ---------------------------------------------------------------- A2
    windows_local, sizes = {}, {}
    for c in treated_sorted:
        g = coh_obs[c]
        conf_W = set(conf["sample"]["placebo_date_windows"][c])
        W = [y for y in (g - 3, g + 3) if y in conf_W and not (g - 2 <= y <= g + 2)]
        windows_local[c] = W
        sizes[c] = len(W)
    if any(len(w) == 0 for w in windows_local.values()):
        sys.exit("empty local placebo-date window — stop (follow-up pre-registration §4)")
    base.G.update(windows=windows_local)
    df2 = run_probe("placebo_date")
    assert len(df2) == B, len(df2)
    a2 = summarize(df2, "A2_placebo_date_local_pm3", obs)
    a2["windows_local"] = windows_local
    a2["window_sizes"] = sizes
    a2["spot_checks"] = spot_check(df2, base._perm_date, "A2")
    print(f"A2 done ({time.time() - t0:.0f}s): p2(T0)={a2['T0']['p_two_sided']:.6g} "
          f"p2(Tpost)={a2['Tpost']['p_two_sided']:.6g} B_eff={a2['B_eff_T0']}/{a2['B_eff_Tpost']}")

    # ---------------------------------------------------------------- outputs
    perms = pd.concat([df1.assign(probe="A1"), df2.assign(probe="A2")], ignore_index=True)
    perms = perms[["probe", "perm", "T0", "Tpost", "n_t0", "n_post_events"]]
    perms.to_csv(OUT_CSV, index=False, compression="gzip")

    r1, r2 = reading(a1), reading(a2)
    overall = "unchanged" if (r1 == "unaffected" and r2 == "unaffected") else "flagged"
    out = dict(
        label=LABEL,
        caveat="Exploratory post-hoc probes; the confirmatory record (PRE_REGISTRATION.md, REPORT.md, "
               "results/e8_ri_results.json, classification 'robust') is NOT changed unless a probe is not 'unaffected'.",
        meta=dict(record="research/records/2026-11-25-e8-fisher-ri",
                  label=LABEL,
                  prereg_followup_commit=PREREG_FOLLOWUP_COMMIT,
                  prereg_followup_is_ancestor_of_head=subprocess.run(
                      ["git", "-C", WORKTREE, "merge-base", "--is-ancestor", PREREG_FOLLOWUP_COMMIT, "HEAD"],
                      capture_output=True).returncode == 0,
                  confirmatory_commit=CONFIRMATORY_COMMIT,
                  git_head=git("rev-parse", "HEAD"),
                  master_seed=base.MASTER_SEED, B=B, workers=N_WORKERS,
                  family_codes=dict(A1=2, A2=1),
                  command="/Users/treymenefee/neon-boot/venv/bin/python scripts/e8_ri_followup.py",
                  numpy=np.__version__, pandas=pd.__version__,
                  wdi_last_updated_date=open(os.path.join(base.DATA, "SHA256SUMS")).readline().strip().split("=")[-1],
                  runtime_seconds=None),
        data=dict(panel=os.path.relpath(base.PANEL, RECORD), panel_sha256=panel_sha,
                  confirmatory_results_json=os.path.relpath(base.OUT_JSON, RECORD),
                  confirmatory_gate_pass=True,
                  ssa_countries=len(countries), treated=coh_obs, n_pool_full=len(pool_full)),
        observed=dict(T0=obs["T0"], Tpost=obs["Tpost"], n_t0=obs["n_t0"], n_post_events=obs["n_post_events"]),
        confirmatory_baseline=dict(
            placebo_date=dict(p2_T0=conf["families"]["placebo_date"]["T0"]["p_two_sided"],
                              p2_Tpost=conf["families"]["placebo_date"]["Tpost"]["p_two_sided"]),
            placebo_country=dict(p2_T0=conf["families"]["placebo_country"]["T0"]["p_two_sided"],
                                 p2_Tpost=conf["families"]["placebo_country"]["Tpost"]["p_two_sided"])),
        A1=a1, A2=a2,
        reading=dict(rule="PRE_REGISTRATION_FOLLOWUP.md §5",
                     A1=r1, A2=r2,
                     overall_confirmatory_conclusion=overall,
                     statement=("Both probes leave the confirmatory reading unchanged: p2 < 0.05 for T0 and Tpost "
                                "in each probe, so the 'robust' classification is not driven by the four "
                                "contaminated-control candidates (A1) or by far placebo dates (A2)." if overall == "unchanged"
                                else "At least one probe is not 'unaffected'; see A1/A2 readings and exact p-values. "
                                     "The confirmatory record itself is left unchanged.")),
        files=dict(followup_json=os.path.relpath(OUT_JSON, RECORD),
                   perms_csv=os.path.relpath(OUT_CSV, RECORD), perms_csv_sha256=sha256_file(OUT_CSV),
                   prereg_followup=os.path.relpath(os.path.join(RECORD, "PRE_REGISTRATION_FOLLOWUP.md"), RECORD),
                   followup_md=os.path.relpath(os.path.join(RECORD, "FOLLOWUP.md"), RECORD)),
    )
    out["meta"]["runtime_seconds"] = round(time.time() - t0, 1)
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)

    for k, s in (("A1", a1), ("A2", a2)):
        for stat in ("T0", "Tpost"):
            v = s[stat]
            print(f"{k} {stat:5s} obs={v['T_obs']:8.4f} perm_mean={v['dist']['mean']:8.4f} "
                  f"sd={v['dist']['sd']:7.4f} p2={v['p_two_sided']:.6g} p+={v['p_one_sided_positive']:.6g} "
                  f"MCSE={v['mcse_two_sided']:.3g} B_eff={v['B_eff']}")
    print(f"readings: A1={r1} A2={r2}; confirmatory conclusion: {overall}")
    print(f"wrote {OUT_JSON} and {OUT_CSV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
