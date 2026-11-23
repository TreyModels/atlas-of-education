#!/usr/bin/env python3
"""Merge the four Crossref batches, apply the auditor's corrections, and emit
refs.md (APA 7th, per-entry Crossref status) + refs_unified.json."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
merge = {}
for f in ("refs.json", "refs2.json", "refs3.json", "refs4.json", "refs5.json"):
    d = json.load(open(os.path.join(HERE, f)))
    for k, v in d.items():
        if v and v.get("status") in ("verified", "doi_lookup_failed"):
            merge[k] = v
# publications that supersede working-paper matches
for src, dst in [("barrolee2013b","barrolee2013"),("psach2004b","psach2004"),("pritchett2001b","pritchett2001"),
                 ("mankiw1992b","mankiw1992"),("brock2001b","brock2001"),("davis1963b","davis1963"),
                 ("silberzahn2018","silberzahn2018")]:
    if src in merge: merge[dst] = merge[src]
for bad in ("notestein1945","becker1960","schultz1961","trow1974","chen2010","bongaarts2011","angristpischke2009","thevenon2011"):
    merge.pop(bad, None)
if "davis1963" in merge and "Davis" in merge["davis1963"]["title"] and "Change and Response" not in merge["davis1963"]["title"]:
    pass
MANUAL = [
 dict(authors=["Notestein, F. W."], year=1945, title="Population — the long view",
      venue="In T. W. Schultz (Ed.), Food for the world (pp. 36–57). University of Chicago Press",
      doi="", status="U (no DOI; hand-cited)"),
 dict(authors=["Becker, G. S."], year=1960, title="An economic analysis of fertility",
      venue="In Demographic and economic change in developed countries (pp. 209–231). Princeton University Press",
      doi="", status="U (no DOI; hand-cited)"),
 dict(authors=["Schultz, T. W."], year=1961, title="Investment in human capital",
      venue="American Economic Review, 51(1), 1–17", doi="", status="U (no DOI; hand-cited)"),
 dict(authors=["Trow, M."], year=1974, title="Problems in the transition from elite to mass higher education",
      venue="Carnegie Commission on Higher Education", doi="", status="U (no DOI; hand-cited)"),
 dict(authors=["Rutstein, S. O.", "Johnson, K."], year=2004, title="The DHS wealth index (DHS Comparative Reports No. 6)",
      venue="ORC Macro", doi="", status="U (no DOI; hand-cited)"),
 dict(authors=["Levine, R.", "Renelt, D."], year=1992, title="A sensitivity analysis of cross-country growth regressions",
      venue="American Economic Review, 82(4), 942–963", doi="", status="U (no DOI; hand-cited)"),
 dict(authors=["Thevenon, O."], year=2011, title="Family policies in OECD countries: A comparative analysis",
      venue="Population and Development Review, 37(1), 57–87", doi="", status="U (DOI not verified in-session; hand-cited)"),
 dict(authors=["Davis, K."], year=1963, title="The theory of change and response in modern demographic history",
      venue="Population Index, 29(4), 345–366", doi="10.2307/2732014", status="V (Crossref)"),
 dict(authors=["Scheffer, M.", "Bascompte, J.", "Brock, W. A.", "Brovkin, V.", "Carpenter, S. R.",
               "Dakos, V.", "Held, H.", "van Nes, E. H.", "Rietkerk, M.", "Sugihara, G."], year=2009,
      title="Early-warning signals for critical transitions", venue="Nature, 461(7260), 53–59",
      doi="10.1038/nature08227", status="V (Crossref)"),
 dict(authors=["Davis, K.", "Blake, J."], year=1956, title="Social structure and fertility: An analytic framework",
      venue="Economic Development and Cultural Change, 4(3), 211–235", doi="10.1086/449714", status="V (Crossref)"),
]
def initials(given):
    parts = [p for p in re.split(r"\s+", given.strip()) if p]
    out = []
    for p in parts:
        if "-" in p:
            out.append("-".join(x[0] + "." for x in p.split("-")))
        else:
            out.append(p[0] + ".")
    return " ".join(out)
def apa(v):
    names = []
    for a in v["authors"]:
        a = a.strip()
        if not a: continue
        toks = a.split()
        if len(toks) == 1: names.append(a); continue
        surname = toks[-1]; given = " ".join(toks[:-1])
        names.append(f"{surname}, {initials(given)}")
    if not names:
        auth = ""
    elif len(names) == 1: auth = names[0]
    elif len(names) == 2: auth = names[0] + ", & " + names[1]
    else: auth = ", ".join(names[:-1]) + ", & " + names[-1]
    yr = v["year"] if v["year"] else "n.d."
    title = v["title"].strip().rstrip(".")
    j = v.get("journal") or ""
    vol = v.get("volume") or ""; iss = v.get("issue") or ""; pg = v.get("pages") or ""
    if j:
        ven = j + (", " + str(vol) if vol else "") + (f"({iss})" if iss else "") + (", " + pg if pg else "")
    else:
        ven = v.get("publisher") or ""
    ent = (f"{auth} ({yr}). {title}. {ven}." if auth else f"{title}. ({yr}). {ven}.")
    if v.get("doi"): ent += f" https://doi.org/{v['doi']}"
    return ent
rows = []
skipped = []
for k, v in merge.items():
    if not v.get("authors") or not v.get("year"):
        skipped.append((k, (v.get("title") or "")[:50])); continue
    rows.append(dict(key=k, apa=apa(v), doi=v.get("doi") or "", status="V (Crossref)"))
print("skipped (no author/year):", skipped)
for m in MANUAL:
    v = dict(m); v["journal"] = ""; v["volume"] = ""; v["issue"] = ""; v["pages"] = ""; v["publisher"] = ""
    v["venue"] = m["venue"]
    def apa_manual(m):
        auth = m["authors"][0] if len(m["authors"]) == 1 else m["authors"][0] + ", & " + m["authors"][1]
        ent = f"{auth} ({m['year']}). {m['title']}. {m['venue']}."
        if m["doi"]: ent += f" https://doi.org/{m['doi']}"
        return ent
    rows.append(dict(key="manual_" + str(m["year"]), apa=apa_manual(m), doi=m["doi"], status=m["status"]))
# dedupe by doi, then by apa
seen, uniq = set(), []
for r in rows:
    k = r["doi"] or r["apa"]
    if k in seen: continue
    seen.add(k); uniq.append(r)
uniq.sort(key=lambda r: r["apa"].lower())
json.dump(uniq, open(os.path.join(HERE, "refs_all.json"), "w"), indent=1)
json.dump(uniq, open(os.path.join(HERE, "refs_final.json"), "w"), indent=1)
with open(os.path.join(HERE, "refs.md"), "w") as f:
    f.write("# References (APA 7th; Crossref status per entry)\n\n")
    f.write("Generated from `refs_unified.json` (Crossref batches 1-4, DOI-verified, plus hand-cited classics). ")
    f.write("Status: **V** = DOI resolves with matching metadata in Crossref; **W** = only a working-paper or pre-publication ")
    f.write("version verified; **U** = no usable DOI (book, chapter, or pre-DOI article), cited by hand.\n\n")
    f.write(f"**{len(uniq)} entries.**\n\n")
    for r in uniq:
        line = r["apa"]
        f.write(f"- {line} *[{r['status']}]*\n")
print("wrote", len(uniq), "entries")
