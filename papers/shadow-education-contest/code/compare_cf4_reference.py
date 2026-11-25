#!/usr/bin/env python3
"""Compare a reproduced HK/Korea CF4 run against the supplied bundle reference output.

Usage:
    python compare_cf4_reference.py REFERENCE.json REPRODUCED.json [--md]

Prints a JSON report to stdout (or a Markdown summary with --md).

The comparison is numeric-field by numeric-field. Two kinds of "match" are
distinguished, because they mean different things:

  * exact equality of the stored double (what a bit-for-bit reproduction means);
  * last-bit differences: |a-b| <= 4 ulp-ish (we report max absolute and
    relative differences). These arise from different libm/BLAS builds and do
    not change any reported (2-dp) summary value.

CF4 evaluation uses the criterion stated in NEXT_EXPERIMENTS.md Exp 7:
    Win-Win = total spend index < 80 AND Q5 elite share below the same
              jurisdiction's Baseline, and it must hold in BOTH HK and KR.
"""
import json
import sys

SEED_SCALARS = [
    "k12_spend", "k12_rate_pct", "g12_pct", "q5_q1_gap_pp",
    "q5_q1_spend_ratio", "elite_q5_share_pct", "contest_e_mean",
]
SEED_LISTS = ["k12_rate_by_q", "k12_spend_by_q"]
SPEND_INDEX_CUTOFF = 80.0


def flatten(d, prefix=""):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else k)
    else:
        yield prefix, d


def diff_pair(a, b):
    """Return (abs_diff, rel_diff) for two floats."""
    d = abs(a - b)
    r = d / max(abs(a), abs(b), 1e-300)
    return d, r


def compare_metadata(ref, run):
    out = {}
    for k, v in ref["metadata"].items():
        got = run["metadata"].get(k)
        out[k] = {"reference": v, "reproduced": got, "equal": v == got}
    out["_extra_keys_reproduced"] = sorted(set(run["metadata"]) - set(ref["metadata"]))
    return out


def compare_seeds(ref, run):
    rs, us = ref["seeds"], run["seeds"]
    store = {"n_values": 0, "n_exact": 0, "max_abs": 0.0, "max_rel": 0.0,
             "max_abs_at": None, "max_rel_at": None, "changed_rows": [],
             "row_key_mismatch": [], "extra_keys": set()}
    for i, (a, b) in enumerate(zip(rs, us)):
        if (a.get("jurisdiction"), a.get("arm_id"), a.get("seed")) != \
           (b.get("jurisdiction"), b.get("arm_id"), b.get("seed")):
            store["row_key_mismatch"].append(i)
        store["extra_keys"] |= set(a) ^ set(b)
        diffs = []
        for f in SEED_SCALARS:
            d, r = diff_pair(a[f], b[f])
            store["n_values"] += 1
            if d == 0.0:
                store["n_exact"] += 1
            else:
                diffs.append(f)
            if d > store["max_abs"]:
                store["max_abs"], store["max_abs_at"] = d, (i, f, a[f], b[f])
            if r > store["max_rel"]:
                store["max_rel"], store["max_rel_at"] = r, (i, f, a[f], b[f])
        for f in SEED_LISTS:
            for j, (x, y) in enumerate(zip(a[f], b[f])):
                d, r = diff_pair(x, y)
                store["n_values"] += 1
                if d == 0.0:
                    store["n_exact"] += 1
                else:
                    diffs.append(f"{f}[{j}]")
                if d > store["max_abs"]:
                    store["max_abs"], store["max_abs_at"] = d, (i, f"{f}[{j}]", x, y)
                if r > store["max_rel"]:
                    store["max_rel"], store["max_rel_at"] = r, (i, f"{f}[{j}]", x, y)
        if diffs:
            store["changed_rows"].append(
                {"row": i, "jurisdiction": a["jurisdiction"], "arm_id": a["arm_id"],
                 "seed": a["seed"], "fields": diffs})
    store["n_diff"] = store["n_values"] - store["n_exact"]
    store["extra_keys"] = sorted(store["extra_keys"])
    store["seed_rows_match"] = (len(rs) == len(us) and not store["row_key_mismatch"]
                                and not store["extra_keys"])
    store["exact"] = (store["n_diff"] == 0 and store["seed_rows_match"])
    store["max_abs_at"] = list(store["max_abs_at"]) if store["max_abs_at"] else None
    store["max_rel_at"] = list(store["max_rel_at"]) if store["max_rel_at"] else None
    store["n_rows"] = {"reference": len(rs), "reproduced": len(us)}
    return store


def compare_summary(ref, run):
    ref_flat = dict(flatten(ref["summary"]))
    run_flat = dict(flatten(run["summary"]))
    out = {"n_numeric": 0, "n_exact": 0, "max_abs": 0.0, "max_rel": 0.0,
           "max_abs_at": None, "max_rel_at": None,
           "mismatched_non_numeric": [], "missing_in_reproduced": []}
    for path, a in ref_flat.items():
        if path not in run_flat:
            out["missing_in_reproduced"].append(path)
            continue
        b = run_flat[path]
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            d, r = diff_pair(a, b)
            out["n_numeric"] += 1
            if d == 0.0:
                out["n_exact"] += 1
            if d > out["max_abs"]:
                out["max_abs"], out["max_abs_at"] = d, [path, a, b]
            if r > out["max_rel"]:
                out["max_rel"], out["max_rel_at"] = r, [path, a, b]
        elif a != b:
            out["mismatched_non_numeric"].append(path)
    out["n_diff"] = out["n_numeric"] - out["n_exact"]
    # 2-dp published fields: every total_spend_index
    out["total_spend_index_all_equal"] = all(
        ref["summary"][j][a]["total_spend_index"] == run["summary"][j][a]["total_spend_index"]
        for j in ref["summary"] for a in ref["summary"][j])
    out["exact"] = (out["n_diff"] == 0 and not out["mismatched_non_numeric"]
                    and not out["missing_in_reproduced"])
    return out


def evaluate_cf4(summary):
    """Per-jurisdiction per-arm CF4/Win-Win evaluation plus single-lever pairing."""
    table = {}
    for jur in ("HK", "KR"):
        base_spend = summary[jur]["Baseline"]["total_spend_index"]
        base_elite = summary[jur]["Baseline"]["elite_q5_share_pct"]["mean"]
        tbl = {}
        for arm, v in summary[jur].items():
            spend = v["total_spend_index"]
            elite = v["elite_q5_share_pct"]["mean"]
            d_elite = v["delta_vs_baseline"]["elite_q5_share_pp"]["mean"]
            tbl[arm] = {
                "spend_index": spend,
                "spend_index_delta_pts": v["delta_vs_baseline"]["total_spend_index_pts"],
                "spend_below_80": spend < SPEND_INDEX_CUTOFF,
                "elite_q5_share_pct": elite,
                "baseline_elite_q5_share_pct": base_elite,
                "elite_delta_pp": d_elite,
                "elite_below_baseline": elite < base_elite,
                "win_win": (spend < SPEND_INDEX_CUTOFF) and (elite < base_elite),
            }
        table[jur] = {"baseline_spend_index": base_spend,
                      "baseline_elite_q5_share_pct": base_elite,
                      "arms": tbl}
    win_both = {}
    for arm in table["HK"]["arms"]:
        win_both[arm] = {"HK": table["HK"]["arms"][arm]["win_win"],
                         "KR": table["KR"]["arms"][arm]["win_win"],
                         "BOTH": table["HK"]["arms"][arm]["win_win"]
                                 and table["KR"]["arms"][arm]["win_win"]}
    single_lever = {}
    for combo, levers in {"CF4a": ["CF3b", "CF1b"], "CF4b": ["CF3b", "CF2b"]}.items():
        row = {"levers": levers}
        for jur in ("HK", "KR"):
            row[jur] = {"combo": {k: table[jur]["arms"][combo][k]
                                  for k in ("spend_index", "elite_q5_share_pct", "win_win")},
                        "levers": {l: {k: table[jur]["arms"][l][k]
                                       for k in ("spend_index", "elite_q5_share_pct", "win_win")}
                                   for l in levers}}
        single_lever[combo] = row
    return {"criterion": {"spend_index_below": SPEND_INDEX_CUTOFF,
                          "elite_q5_share": "below same-jurisdiction Baseline mean",
                          "requires_both_jurisdictions": ["HK", "KR"]},
            "per_jurisdiction": table, "win_win_both_jurisdictions": win_both,
            "single_lever_comparison": single_lever}


def fmt(x, nd=2):
    return f"{x:.{nd}f}"


def render_markdown(rep):
    c = rep["comparison"]
    out = []
    out.append(f"# CF4 reference comparison (SIMULATION)\n")
    out.append(f"reference: `{rep['reference']}`  \nreproduced: `{rep['reproduced']}`\n")
    out.append("## Metadata\n")
    for k, v in c["metadata"].items():
        if k.startswith("_"):
            continue
        out.append(f"- `{k}`: {'EQUAL' if v['equal'] else 'DIFF'} "
                   f"(ref={v['reference']!r}, run={v['reproduced']!r})")
    s = c["seeds"]
    out.append("\n## Seeds\n")
    out.append(f"- rows: reference {s['n_rows']['reference']}, reproduced {s['n_rows']['reproduced']}")
    out.append(f"- numeric values compared: {s['n_values']}; exactly equal: {s['n_exact']}; "
               f"differing: {s['n_diff']}")
    out.append(f"- max abs diff: {s['max_abs']:.3e}; max rel diff: {s['max_rel']:.3e}")
    for r in s["changed_rows"]:
        out.append(f"- row {r['row']}: {r['jurisdiction']} {r['arm_id']} seed={r['seed']} — {r['fields']}")
    out.append(f"- seeds bit-identical: {s['exact']}")
    sm = c["summary"]
    out.append("\n## Summary\n")
    out.append(f"- numeric fields: {sm['n_numeric']}; exactly equal: {sm['n_exact']}; "
               f"differing: {sm['n_diff']}")
    out.append(f"- max abs diff: {sm['max_abs']:.3e}; max rel diff: {sm['max_rel']:.3e}")
    out.append(f"- all `total_spend_index` (2 dp) equal: {sm['total_spend_index_all_equal']}")
    out.append(f"- summary bit-identical: {sm['exact']}")
    return "\n".join(out) + "\n"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_md = "--md" in sys.argv[1:]
    if len(args) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    ref = json.load(open(args[0]))
    run = json.load(open(args[1]))
    rep = {
        "reference": args[0], "reproduced": args[1],
        "comparison": {
            "metadata": compare_metadata(ref, run),
            "seeds": compare_seeds(ref, run),
            "summary": compare_summary(ref, run),
        },
        "cf4": {"reference": evaluate_cf4(ref["summary"]),
                "reproduced": evaluate_cf4(run["summary"])},
    }
    if as_md:
        print(render_markdown(rep))
    else:
        print(json.dumps(rep, indent=2, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
