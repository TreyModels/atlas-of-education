import json,urllib.parse,urllib.request,sys
def get(t,n=3):
    u=("https://api.openalex.org/works?filter=title.search:"+urllib.parse.quote(t)
       +f"&per_page={n}&mailto=research@example.org")
    try: d=json.load(urllib.request.urlopen(u,timeout=60))
    except Exception as e: return [("ERR",str(e))]
    r=[]
    for w in d.get("results",[]):
        ab=w.get("abstract_inverted_index") or {}
        pos={}
        for k,v in ab.items():
            for i in v: pos[i]=k
        r.append((w.get("publication_year"),w.get("title"),((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                  (w.get("doi") or "").replace("https://doi.org/","")," ".join(pos[i] for i in sorted(pos))[:700]))
    return r
for t in sys.argv[1:]:
    print("\n#####",t)
    for y,ti,v,doi,ab in get(t):
        if y=="ERR": print(ab); continue
        print(f"[{y}] {ti} — {v} — {doi}\n  {ab}\n")
