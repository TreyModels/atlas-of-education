#!/usr/bin/env python3
import sys, json, urllib.parse, urllib.request, time, re

MAIL = "researcher@example.org"

def cr(q, n=3):
    url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(q)}&rows={n}&select=title,issued,container-title,DOI,author,abstract,type&mailto={MAIL}"
    req = urllib.request.Request(url, headers={"User-Agent": f"litreview/1.0 (mailto:{MAIL})"})
    for a in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode())["message"]["items"]
        except Exception as e:
            if a == 2: return []
            time.sleep(3)

if __name__ == "__main__":
    qs = json.load(open(sys.argv[1]))
    out = []
    for label, q in qs:
        for it in cr(q):
            ab = re.sub(r"<[^>]+>", " ", it.get("abstract", "") or "")
            ab = re.sub(r"\s+", " ", ab).strip()
            out.append({"label": label, "title": (it.get("title") or [""])[0],
                        "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
                        "venue": (it.get("container-title") or [""])[0],
                        "doi": it.get("DOI"), "abstract": ab[:1400],
                        "authors": [f"{a.get('given','')} {a.get('family','')}" for a in it.get("author", [])][:5]})
        time.sleep(0.6)
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    for r in out:
        print(f"[{r['label']}] {r['year']} | {r['title'][:90]} | {r['venue'][:45]} | {r['doi']}")
