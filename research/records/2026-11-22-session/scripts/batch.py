#!/usr/bin/env python3
"""Batch verify references against OpenAlex by title search; save full records to JSON."""
import sys, json, urllib.parse, urllib.request, time

MAIL = "researcher@example.org"

def inv2abs(inv):
    if not inv: return ""
    pos = []
    for w, idxs in inv.items():
        for i in idxs: pos.append((i, w))
    pos.sort()
    return " ".join(w for _, w in pos)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"litreview (mailto:{MAIL})"})
    for a in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            code = getattr(e, "code", None)
            if a == 2: return {"results": []}
            time.sleep(8 if code == 429 else 3)

def run(queries, outfile, mode="title.search", n=3, abslen=1200):
    recs = []
    for label, q in queries:
        filt = "title.search:" if mode == "title.search" else "search:"
        url = f"https://api.openalex.org/works?filter={filt}{urllib.parse.quote(q)}&per_page={n}&mailto={MAIL}"
        d = get(url)
        for w in d.get("results", []):
            src = (w.get("primary_location") or {}).get("source") or {}
            recs.append({
                "label": label, "query": q,
                "title": w.get("title"), "year": w.get("publication_year"),
                "venue": src.get("display_name"), "doi": w.get("doi"),
                "type": w.get("type"), "cites": w.get("cited_by_count"),
                "authors": [a["author"]["display_name"] for a in w.get("authorships", [])][:5],
                "abstract": inv2abs(w.get("abstract_inverted_index"))[:abslen],
            })
        time.sleep(1.2)
    with open(outfile, "w") as f: json.dump(recs, f, indent=1)
    for r in recs:
        print(f"[{r['label']}] {r['year']} | {r['title'][:95] if r['title'] else '?'} | {r['venue']} | {r['doi']}")

if __name__ == "__main__":
    qs = json.load(open(sys.argv[1]))
    run([tuple(x) for x in qs], sys.argv[2])
