#!/usr/bin/env python3
import sys, json, urllib.parse, urllib.request, time

MAIL = "researcher@example.org"

def inv2abs(inv):
    if not inv: return ""
    pos = []
    for w, idxs in inv.items():
        for i in idxs:
            pos.append((i, w))
    pos.sort()
    return " ".join(w for _, w in pos)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"litreview (mailto:{MAIL})"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if attempt == 2: raise
            time.sleep(2)

def search(q, n=8, abslen=700, mode="search"):
    if mode == "search":
        url = f"https://api.openalex.org/works?search={urllib.parse.quote(q)}&per_page={n}&mailto={MAIL}&sort=relevance_score:desc"
    else:
        url = f"https://api.openalex.org/works?filter=title.search:{urllib.parse.quote(q)}&per_page={n}&mailto={MAIL}"
    d = get(url)
    out = []
    for w in d.get("results", []):
        src = (w.get("primary_location") or {}).get("source") or {}
        out.append({
            "title": w.get("title"),
            "year": w.get("publication_year"),
            "venue": src.get("display_name"),
            "doi": w.get("doi"),
            "type": w.get("type"),
            "cites": w.get("cited_by_count"),
            "authors": [a["author"]["display_name"] for a in w.get("authorships", [])][:4],
            "abstract": inv2abs(w.get("abstract_inverted_index"))[:abslen],
        })
    return out

if __name__ == "__main__":
    q = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    abslen = int(sys.argv[3]) if len(sys.argv) > 3 else 700
    mode = sys.argv[4] if len(sys.argv) > 4 else "search"
    for r in search(q, n, abslen, mode):
        print("=" * 90)
        print(f"TITLE: {r['title']}")
        print(f"YEAR: {r['year']} | VENUE: {r['venue']} | DOI: {r['doi']} | cites: {r['cites']}")
        print(f"AUTHORS: {', '.join(r['authors'])}")
        if abslen:
            print(f"ABS: {r['abstract']}")
