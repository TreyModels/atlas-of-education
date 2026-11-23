#!/usr/bin/env python3
"""Second Crossref batch: transition theory expansions, critical transitions, pronatalist
policy, care economy, DHS-survey literature, mortality-fertility models."""
import json, os, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "refs2_raw.json"); OUT = os.path.join(HERE, "refs2.json")
MAILTO = "trey@atlasofeducation.example"; UA = "atlas-paper-lit/1.0 (mailto:%s)" % MAILTO
QUERIES = [
 ("easterlin1966", "Easterlin 1966 on the relation of economic factors to recent and projected fertility changes"),
 ("beckerbarro1988", "Becker Barro 1988 a reformulation of the economic theory of fertility"),
 ("galorweil2000", "Galor Weil 2000 population technology and growth long-run growth from Malthus to Solow"),
 ("doepke2004", "Doepke 2004 accounting for fertility decline during the transition to growth"),
 ("doepke2005", "Doepke 2005 child mortality and fertility decline does the Barro-Becker model fit the facts"),
 ("guinnane2011", "Guinnane 2011 the historical fertility transition a guide for economists"),
 ("lesthaeghe1983", "Lesthaeghe 1983 a century of demographic and cultural change in Western Europe"),
 ("scheffer2009", "Scheffer 2009 early-warning signals for critical transitions"),
 ("dakos2012", "Dakos 2012 methods for detecting early warnings of critical transitions in time series"),
 ("scheffer2012", "Scheffer 2012 anticipating critical transitions"),
 ("gauthier2007", "Gauthier 2007 the impact of family policies on fertility in industrialized countries"),
 ("thevenon2011", "Thevenon 2011 family policies in OECD countries a comparative analysis"),
 ("thevenongauthier2011", "Thevenon Gauthier 2011 family policies in developed countries a fertility-booster with side-effects"),
 ("englandfolbre1999", "England Folbre 1999 the cost of caring"),
 ("folbre2001", "Folbre 2001 the invisible heart economics and family values"),
 ("razavi2007", "Razavi 2007 the political and social economy of care in a development context"),
 ("kravdal2002", "Kravdal 2002 education and fertility in sub-Saharan Africa individual and community effects"),
 ("kravdal2004", "Kravdal 2004 fertility effects of school reform in Norway"),
 ("castromartin2015", "Castro Martin 2015 educational expansion fertility developing countries"),
 ("soares2005", "Soares 2005 mortality decline human capital investment and economic growth"),
 ("kalemliozcan2002", "Kalemli-Ozcan 2002 mortality decline and economic growth"),
 ("galor2011", "Galor 2011 unified growth theory"),
 ("durante2019", "Durante 2019 the persistent effects of education on fertility"),
 ("bongaarts1978b", "Bongaarts 1978 A framework for analyzing the proximate determinants of fertility"),
 ("lutzskirbekk2005", "Lutz Skirbekk 2005 policies addressing the tempo effect in low fertility countries"),
 ("ni2018", "Ni 2018 education and fertility decline China"),
 ("borbely2015", "Borbely 2015 education and fertility in Europe"),
 ("murtin2013b", "Murtin 2013 long-term determinants demographic transition 1870 2000"),
 ("cinnirella2017", "Cinnirella 2017 fertility transition education Prussia"),
 ("becker1960b", "Becker 1960 an economic analysis of fertility demographic and economic change in developed countries"),
]
def get(url, tries=4):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(3 * (t + 1)); continue
            return None
        except Exception: time.sleep(2 * (t + 1))
    return None
def fmt(it):
    def name(a):
        if a.get("family"): return (a.get("given", "") + " " + a["family"]).strip()
        return a.get("name", "")
    return dict(doi=it.get("DOI"), title=(it.get("title") or [""])[0],
        authors=[name(a) for a in (it.get("author") or [])],
        year=(it.get("issued", {}).get("date-parts") or [[None]])[0][0],
        journal=(it.get("container-title") or [""])[0], volume=it.get("volume"),
        issue=it.get("issue"), pages=it.get("page"), publisher=it.get("publisher"),
        type=it.get("type"), url=it.get("URL"))
if __name__ == "__main__":
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for key, q in QUERIES:
        if key in out and out[key].get("status") == "verified": continue
        url = ("https://api.crossref.org/works?rows=3&select=DOI,title,author,issued,container-title,volume,issue,page,publisher,type,URL&mailto=" + MAILTO + "&query.bibliographic=" + urllib.parse.quote(q))
        d = get(url)
        items = (d or {}).get("message", {}).get("items", [])
        if not items:
            out[key] = dict(query=q, status="search_failed"); print(key, "FAILED", flush=True); continue
        rec = fmt(items[0]); v = get("https://api.crossref.org/works/" + urllib.parse.quote(rec["doi"]) + "?mailto=" + MAILTO) if rec["doi"] else None
        if v: rec.update(fmt(v["message"])); rec["status"] = "verified"
        else: rec["status"] = "doi_lookup_failed"
        rec["query"] = q; out[key] = rec
        print(key, rec["status"], rec["doi"], "|", rec["title"][:55], rec["year"], flush=True)
        json.dump(out, open(OUT, "w"), indent=1); time.sleep(0.6)
    print("done", sum(1 for v in out.values() if v.get("status") == "verified"), "/", len(out))
