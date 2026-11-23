"""Recompute the sequencing distribution of Paper N1 from the committed event dates.

Input:  results/event_dates.csv (copy of research/subsistence-v2-2026-11-23 @ ce66cfc results/event_dates.csv)
Output: results/sequencing_stats.json
Definitions: lead = release_date - schooling_date, so a positive lead means schooling came first.
"""
import csv, json, os, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)
rows = list(csv.DictReader(open(os.path.join(REC, "results", "event_dates.csv"))))

def num(x):
    try:
        return float(x)
    except Exception:
        return None

all3 = [r for r in rows
        if num(r["release"]) is not None and num(r["schooling"]) is not None and num(r["fertility"]) is not None]
pair = [r for r in rows if num(r["release"]) is not None and num(r["schooling"]) is not None]

def dist(dat):
    leads = [num(r["release"]) - num(r["schooling"]) for r in dat]
    fwd = sorted(x for x in leads if x > 0)
    q = st.quantiles(fwd, n=4)
    return dict(
        n=len(dat), forward=len(fwd), reverse=len(dat) - len(fwd),
        forward_pct=round(100 * len(fwd) / len(dat), 2),
        median_lead=st.median(fwd),
        q1=round(q[0], 1), q3=round(q[2], 1),
        share_gt10=round(100 * sum(1 for x in fwd if x > 10) / len(fwd), 2),
        share_gt15=round(100 * sum(1 for x in fwd if x > 15) / len(fwd), 2),
        still_forward_after_plus15_error=sum(1 for x in fwd if x > 15),
        still_forward_after_plus15_pct=round(100 * sum(1 for x in fwd if x > 15) / len(dat), 2),
        median_lead_all=st.median(leads))

out = dict(all_three=dist(all3), schooling_and_release=dist(pair),
           note="lead = release - schooling; positive = schooling first. all_three is the paper's 64-country panel.")
json.dump(out, open(os.path.join(REC, "results", "sequencing_stats.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
