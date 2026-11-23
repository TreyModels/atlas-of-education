#!/usr/bin/env python3
"""Second Crossref batch: transition theory expansions, critical transitions, pronatalist
policy, care economy, DHS-survey literature, mortality-fertility models."""
import json, os, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "refs3_raw.json"); OUT = os.path.join(HERE, "refs3.json")
MAILTO = "trey@atlasofeducation.example"; UA = "atlas-paper-lit/1.0 (mailto:%s)" % MAILTO
QUERIES = [
 ("silberzahn2018b", "Silberzahn 2018 many analysts one data set making transparent how variations in analytic choices affect results"),
 ("lee2003", "Lee 2003 the demographic transition three centuries of fundamental change"),
 ("davis1963b", "Davis 1963 the theory of change and response in modern demographic history"),
 ("clelandrodriguez1988", "Cleland Rodriguez 1988 the effect of parental education on marital fertility in developing countries"),
 ("kravdal2012", "Kravdal 2012 further evidence of community education effects on fertility in sub-Saharan Africa"),
 ("coalewatkins1986", "Coale Watkins 1986 the decline of fertility in Europe"),
 ("granovetter1978", "Granovetter 1978 threshold models of collective behavior"),
 ("beaumont2002", "Beaumont Zhang Balding 2002 approximate Bayesian computation in population genetics"),
 ("beaumont2009", "Beaumont Cornuet Marin Robert 2009 adaptive approximate Bayesian computation"),
 ("delmoral2012", "Del Moral Doucet Jasra 2012 an adaptive sequential Monte Carlo method for approximate Bayesian computation"),
 ("eberhardt2011", "Eberhardt Teal 2011 econometrics for grumblers a guide to the literature on cross-country growth empirics"),
 ("pearl2011", "Pearl Bareinboim 2011 transportability of causal and statistical relations a general approach"),
 ("corsi2012", "Corsi Neuman Finlay Subramanian 2012 demographic and health surveys methodological reports"),
 ("duflo2001b", "Duflo 2001 schooling and labor market consequences of school construction in Indonesia evidence from an unusual policy experiment"),
 ("pritchett2001b", "Pritchett 2001 where has all the education gone World Bank Economic Review"),
 ("barrolee2013b", "Barro Lee 2013 a new data set of educational attainment in the world Journal of Development Economics"),
 ("psach2004b", "Psacharopoulos Patrinos 2004 returns to investment in education a further update Education Economics"),
 ("mankiw1992b", "Mankiw Romer Weil 1992 a contribution to the empirics of economic growth Quarterly Journal of Economics"),
 ("brock2001b", "Brock Durlauf 2001 growth empirics and reality World Bank Economic Review"),
 ("becker2010b", "Becker Cinnirella Woessmann 2010 the trade-off between fertility and education evidence from before the demographic transition"),
 ("becker2013b", "Becker Cinnirella Woessmann 2013 does education matter for fertility evidence from Prussia"),
 ("martinjuarez1995", "Martin Juarez 1995 the impact of women's education on fertility in Latin America searching for explanations"),
 ("king1997b", "King 1997 a solution to the ecological inference problem reconstructing individual behavior from aggregate data"),
 ("notestein1945b", "Notestein 1945 population the long view Food for the World"),
 ("schultz1961b", "Schultz 1961 investment in human capital American Economic Review"),
 ("becker1960b2", "Becker 1960 an economic analysis of fertility demographic and economic change in developed countries"),
 ("trow1974b", "Trow 1974 problems in the transition from elite to mass higher education"),
 ("henrich2010", "Henrich Heine Norenzayan 2010 the weirdest people in the world"),
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
