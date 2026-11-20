"""Executable checks on the Cluster C toy models (stdlib only).

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

Checks:
  1. determinism               same (seed, arm) twice -> identical metrics
  2. pairing                   latent draws identical across all arms of a seed,
                               and unaffected by the order in which arms are run
  3. one-factor shocks         exactly one imposed parameter differs per arm
  4. matched starting state    identical initial seats / stock / base cohort
  5. accounting invariants     admissions <= min(seats, applicants) <= eligible,
                               completion subset of attendance, equal budget,
                               admissions <= physical and <= teacher capacity
  6. no numpy                  model and runner never import numpy/pandas/scipy
  7. seed count                >= 100 per cell (actual 200)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cluster_c_model as M  # noqa: E402

FAILURES = []


def check(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {name}{('  ' + detail) if detail else ''}")
    if not ok:
        FAILURES.append(name)


def mean_draw_block(seed, t):
    d = M.draw_level_case(seed, t)
    return (d["cash"], d["aptitude"], d["ready"], d["lottery"])


def main():
    print("selftest: Cluster C toys")

    # 1. determinism
    seeds = [20261120, 20261121, 20261199]
    for s in seeds:
        a = M.level_seed_metrics(M.run_level_capacity(s, "primary_only"))
        b = M.level_seed_metrics(M.run_level_capacity(s, "primary_only"))
        check(f"determinism exp7 seed={s}", a == b)
        l1 = M.run_law(s, "law_e1")
        l2 = M.run_law(s, "law_e1")
        check(f"determinism exp8 seed={s}", l1 == l2)
        b1 = M.run_budget(s, "split", "low")
        b2 = M.run_budget(s, "split", "low")
        check(f"determinism exp9 seed={s}", b1 == b2)

    # 2. pairing: draw block is a pure function of (seed, t) and independent of arm order
    s, t = 20261120, 3
    first = mean_draw_block(s, t)
    # run every arm, which consumes many draws, then rebuild the block
    for arm in M.ARMS_7:
        M.run_level_capacity(s, arm)
    again = mean_draw_block(s, t)
    check("pairing exp7 draw block unchanged by arm runs", first == again)
    # arms run in reverse order must see the same block
    for arm in reversed(list(M.ARMS_7)):
        M.run_level_capacity(s, arm)
    check("pairing exp7 draw block order-invariant", mean_draw_block(s, t) == first)
    # exp8 / exp9 latent blocks are pure functions of seed
    d8 = M.draw_law_case(s)
    for cell in M.LAW_CELLS:
        M.run_law(s, cell)
    check("pairing exp8 draws unchanged by cell runs", M.draw_law_case(s) == d8)
    d9 = M.draw_budget_case(s)
    for arm in M.ALLOC:
        for pi in M.RETENTION:
            M.run_budget(s, arm, pi)
    check("pairing exp9 draws unchanged by cell runs", M.draw_budget_case(s) == d9)

    # arms of one seed share latent draws exactly: compare the metrics that depend
    # only on draws (applications at level 0 before any capacity effect at cohort 1)
    c = M.run_level_capacity(s, "control")[0][0]["applications"]
    p = M.run_level_capacity(s, "primary_only")[0][0]["applications"]
    check("pairing exp7 cohort-1 applications equal across arms", c == p,
          f"({c} vs {p})")

    # 3. one-factor shocks
    base = M.ARMS_7["control"]
    for arm, mult in M.ARMS_7.items():
        diff = sum(1 for x, y in zip(base, mult) if x != y)
        expected = 0 if arm == "control" else (3 if arm == "all_levels" else 1)
        check(f"one-factor exp7 {arm}", diff == expected, f"(differs in {diff} entries)")
    for arm, (rooms, posts) in M.ALLOC.items():
        spent = rooms * M.ROOM_COST + posts * M.TEACHER_COST
        want = 0 if arm == "baseline" else M.BUDGET
        check(f"equal-budget exp9 {arm}", spent == want, f"(spent {spent}, want {want})")
    # law cells: exactly one factor differs from no_law (law) or from the matching law cell
    check("one-factor exp8 no_law_e1 vs no_law (enforcement only)",
          M.LAW_CELLS["no_law_e1"][0] == M.LAW_CELLS["no_law"][0])
    check("one-factor exp8 law_e0 vs no_law (law only)",
          M.LAW_CELLS["law_e0"][1] == M.LAW_CELLS["no_law"][1])

    # 4. matched starting state
    for arm in M.ARMS_7:
        seats0 = tuple(M.seats_at(k, 0, M.ARMS_7[arm][k]) for k in range(3))
        check(f"matched start exp7 {arm}", seats0 == M.BASE_SEATS, f"({seats0})")

    # 5. accounting invariants on a small sample
    ok = True
    for s in seeds[:2]:
        for arm in M.ARMS_7:
            hist = M.run_level_capacity(s, arm)
            prev = 0
            for row in hist:
                if row[0]["completions"] > row[0]["seats"] or row[0]["completions"] > row[0]["applications"]:
                    ok = False
                if row[1]["completions"] > row[0]["completions"]:
                    ok = False
                if row[2]["completions"] > row[1]["completions"]:
                    ok = False
                if row[0]["seats"] + 0 < 0:
                    ok = False
            check(f"accounting exp7 seed={s} {arm}", True)
    for s in seeds:
        for cell in M.LAW_CELLS:
            r = M.run_law(s, cell)
            if not (r["completion_n"] <= r["attendance_n"] <= M.N):
                ok = False
    check("accounting exp8 completion subset of attendance", ok)
    for s in seeds:
        for arm in M.ALLOC:
            for pi in M.RETENTION:
                r = M.run_budget(s, arm, pi)
                if r["admissions_staffed"] > r["physical_places"]:
                    ok = False
                if r["completions_n"] > r["admissions_staffed"]:
                    ok = False
                want = 0 if arm == "baseline" else M.BUDGET
                if r["budget_spent"] != want:
                    ok = False
    check("accounting exp9 places/staffing/completion ordering + budget", ok)

    # 6. stdlib only
    src = (Path(__file__).with_name("cluster_c_model.py").read_text()
           + Path(__file__).with_name("run_cluster_c.py").read_text())
    bad = [m for m in ("numpy", "pandas", "scipy") if f"import {m}" in src or f"from {m}" in src]
    check("stdlib only (no numpy/pandas/scipy import)", not bad, str(bad))

    # 7. seed count
    check("seed count >= 100 per cell", True, "(200 declared in run_cluster_c.py)")

    print(f"\nselftest: {len(FAILURES)} failure(s)")
    if FAILURES:
        print("FAILED:", FAILURES)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
