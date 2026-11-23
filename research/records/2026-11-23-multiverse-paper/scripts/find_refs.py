#!/usr/bin/env python3
"""Crossref bibliographic search to recover exact bibliographic records for entries whose DOI was uncertain.
Prints the top 2 hits for each query, so a human can pick and record the correct DOI. Not a content check."""
import json, urllib.request, urllib.parse
Q = [
 "Bareinboim Pearl Causal inference and the data-fusion problem",
 "Young Holsteen Model uncertainty and robustness computational framework multiverse analysis",
 "Del Giudice Gangestad A traveler's guide to the multiverse",
 "Hope A simplified Monte Carlo significance test procedure",
 "Hotz Imbens Mortimer Predicting the efficacy of future training programs using past experiences",
 "Bonhomme Lamadon Manresa Discretizing unobserved heterogeneity",
 "Munoz Young We ran 9 billion regressions nested p-values",
 "Rodrik Why we learn nothing from regressing economic growth on policies",
 "North Curtis Sham note calculation empirical P values Monte Carlo procedures",
 "Marriott Barnard's Monte Carlo tests how many simulations",
 "Gelman Loken garden of forking paths",
]
BASE="https://api.crossref.org/works?"
def q(s):
    url = BASE + urllib.parse.urlencode({"query.bibliographic": s, "rows": 2})
    req = urllib.request.Request(url, headers={"User-Agent":"atlas-ref-check/1.0 (mailto:trey@treymodels.com)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)["message"]["items"]
for s in Q:
    print(f"### QUERY: {s}")
    try:
        for it in q(s):
            au = "; ".join(f"{a.get('family','?')}, {a.get('given','')}" for a in it.get("author", []))
            print(f"  - {it.get('title',['MISSING'])[0][:120]}")
            print(f"    {au[:160]}")
            print(f"    {(it.get('container-title') or ['MISSING'])[0]} | {it.get('issued',{}).get('date-parts',[['?']])[0][0]} | vol {it.get('volume','?')}({it.get('issue','')}) p {it.get('page','?')} | DOI {it.get('DOI','?')}")
    except Exception as e:
        print("  FETCH FAILED:", e)
