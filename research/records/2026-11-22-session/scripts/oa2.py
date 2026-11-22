import json,urllib.parse,urllib.request,sys
def q(s,n=15):
    u=("https://api.openalex.org/works?filter=title_and_abstract.search:"
       +urllib.parse.quote(s)+f"&per_page={n}&sort=cited_by_count:desc&mailto=research@example.org")
    try: d=json.load(urllib.request.urlopen(u,timeout=60))
    except Exception as e: return [("ERR",str(e))]
    out=[]
    for w in d.get("results",[]):
        ab=w.get("abstract_inverted_index") or {}
        pos={}
        for word,idxs in ab.items():
            for i in idxs: pos[i]=word
        txt=" ".join(pos[i] for i in sorted(pos))[:330]
        out.append((w.get("publication_year"),(w.get("title") or "")[:130],
            ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
            w.get("cited_by_count"),(w.get("doi") or "").replace("https://doi.org/",""),txt))
    return out
for s in sys.argv[1:]:
    print("\n===== "+s)
    for r in q(s):
        if r[0]=="ERR": print(r); continue
        print(f"[{r[0]}] {r[1]} — {r[2]} (cites {r[3]}) {r[4]}\n   {r[5]}\n")
