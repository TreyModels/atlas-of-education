#!/usr/bin/env python3
"""Fetch and verify bibliographic records from Crossref for the Paper 1 claim tables.

Every candidate is a bibliographic query string. The script queries Crossref, keeps
the top match, verifies the DOI directly, and writes lit/refs.json with the full
metadata plus a verification status per record. Polite pool via mailto; retries on
429/5xx with backoff; cache to lit/refs_raw.json so reruns are cheap.

Run: python3 fetch_refs.py
"""
import json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "refs_raw.json")
OUT = os.path.join(HERE, "refs.json")
MAILTO = "trey@atlasofeducation.example"
UA = "atlas-paper-lit/1.0 (mailto:%s)" % MAILTO

QUERIES = [
 ("robinson1950", "Robinson 1950 ecological correlations and the behavior of individuals"),
 ("nickell1981", "Nickell 1981 biases in dynamic models with fixed effects"),
 ("angristpischke2009", "Angrist Pischke 2009 Mostly Harmless Econometrics"),
 ("belljones2015", "Bell Jones 2015 explaining fixed effects random effects modeling panel data"),
 ("hausmantaylor1981", "Hausman Taylor 1981 panel data and unobservable individual effects"),
 ("steegen2016", "Steegen Tuerlinckx Gelman Vanpaemel 2016 increasing transparency multiverse analysis"),
 ("simonsohn2020", "Simonsohn Simmons Nelson 2020 specification curve analysis"),
 ("delgiudice2021", "Del Giudice Gangestad 2021 traveler's guide multiverse"),
 ("silberzahn2018", "Silberzahn 2018 many analysts one data set"),
 ("vivalt2020", "Vivalt 2020 how much can we generalize from impact evaluations"),
 ("deaton2010", "Deaton 2010 instruments randomization and learning about development"),
 ("bareinboim2013", "Bareinboim Pearl 2013 general algorithm deciding transportability experimental results"),
 ("roth2022", "Roth 2022 pretest with caution event-study estimates parallel trends"),
 ("caldwell1980", "Caldwell 1980 mass education as a determinant of the timing of fertility decline"),
 ("caldwell1976", "Caldwell 1976 toward a restatement of demographic transition theory"),
 ("bongaarts1978", "Bongaarts 1978 framework for analyzing the proximate determinants of fertility"),
 ("bongaarts1996", "Bongaarts Watkins 1996 social interactions and contemporary fertility transitions"),
 ("cleland1987", "Cleland Wilson 1987 demand theories of the fertility transition iconoclastic view"),
 ("lutz2011", "Lutz KC 2011 global human capital integrating education and population"),
 ("skirbekk2008", "Skirbekk 2008 fertility trends by social status"),
 ("barrolee2013", "Barro Lee 2013 a new data set of educational attainment in the world 1950-2010"),
 ("barrolee1994", "Barro Lee 1994 sources of economic growth"),
 ("mincer1958", "Mincer 1958 investment in human capital and personal income distribution"),
 ("psach2004", "Psacharopoulos Patrinos 2004 returns to investment in education a further update"),
 ("psach2018", "Psacharopoulos Patrinos 2018 returns to investment in education a decennial review"),
 ("pritchett2001", "Pritchett 2001 where has all the education gone"),
 ("duflo2012", "Duflo 2012 women empowerment and economic development"),
 ("beckerlewis1973", "Becker Lewis 1973 on the interaction between the quantity and quality of children"),
 ("becker2010", "Becker Cinnirella Woessmann 2010 the trade-off between fertility and education"),
 ("becker2013", "Becker Cinnirella Woessmann 2013 does education matter for fertility evidence from Prussia"),
 ("hanushek1992", "Hanushek 1992 the trade-off between child quantity and quality"),
 ("black2005", "Black Devereux Salvanes 2005 the more the merrier family size and birth order"),
 ("herzer2012", "Herzer Strulik Vollmer 2012 the long-run determinants of fertility one century"),
 ("durlauf2001", "Durlauf 2001 manifesto for a growth econometrics"),
 ("brock2001", "Brock Durlauf 2001 growth empirics and reality"),
 ("durlauf2005", "Durlauf Johnson Temple 2005 growth econometrics handbook"),
 ("levine1992", "Levine Renelt 1992 a sensitivity analysis of cross-country growth regressions"),
 ("sala1997", "Sala-i-Martin 1997 I just ran two million regressions"),
 ("schofer2005", "Schofer Meyer 2005 the worldwide expansion of higher education in the twentieth century"),
 ("meyer1992", "Meyer Ramirez Soysal 1992 world expansion of mass education 1870-1980"),
 ("davis1945", "Davis 1945 the world demographic transition"),
 ("bongaarts1998", "Bongaarts Feeney 1998 on the quantum and tempo of fertility"),
 ("lesthaeghe2010", "Lesthaeghe 2010 the unfolding story of the second demographic transition"),
 ("basu2002", "Basu 2002 why does education lead to lower fertility critical review"),
 ("angeles2010", "Angeles 2010 human capital and fertility evidence from the stock of education"),
 ("kc2017", "KC Lutz 2017 the human core of the shared socioeconomic pathways"),
 ("chicoine2012", "Chicoine 2012 education and fertility evidence from a policy change Kenya"),
 ("duflo2001", "Duflo 2001 schooling and labor market consequences of school construction in Indonesia"),
 ("king1997", "King 1997 a solution to the ecological inference problem"),
 ("mankiw1992", "Mankiw Romer Weil 1992 a contribution to the empirics of economic growth"),
 ("benhabib1994", "Benhabib Spiegel 1994 the role of human capital in economic development"),
 ("temple1999", "Temple 1999 the new growth evidence"),
 ("rosenzweig1990", "Rosenzweig 1990 population growth and human capital investments theory and evidence"),
 ("schultz1997", "Schultz 1997 demand for children in low income countries"),
 ("bertrand2004", "Bertrand Duflo Mullainathan 2004 how much should we trust differences-in-differences estimates"),
 ("lutz2007", "Lutz 2007 reconstruction of populations by age sex and level of educational attainment"),
 ("freedman1999", "Freedman 1999 ecological inference and the ecological fallacy"),
 ("cochrane1979", "Cochrane 1979 fertility and education what do we really know"),
 ("trow1974", "Trow 1974 problems in the transition from elite to mass higher education"),
 ("angristkrueger1999", "Angrist Krueger 1999 empirical strategies in labor economics"),
 ("acemoglu2005", "Acemoglu Johnson Robinson 2005 institutions as a fundamental cause of long-run growth"),
 ("foster1997", "Foster Rosenzweig 1997 technical change and human capital returns"),
 ("schultz1961", "Schultz 1961 investment in human capital"),
 ("becker1960", "Becker 1960 an economic analysis of fertility"),
 ("davis1963", "Davis Blake 1956 social structure and fertility an analytic framework"),
 ("notestein1945", "Notestein 1945 population the long view"),
 ("bongaarts2011", "Bongaarts 2011 a framework for analyzing the proximate determinants of fertility"),
 ("lutz2014", "Lutz Butz KC Sanderson Scherbov 2014 population aging education"),
 ("striessnig2013", "Striessnig Lutz 2013 can above-replacement fertility be economically optimal"),
 ("murtin2013", "Murtin 2013 long-term determinants of the demographic transition 1870-2000"),
 ("chen2010", "Chen 2010 education and fertility evidence from China"),
 ("osili2008", "Osili Long 2008 does female schooling reduce fertility evidence from Nigeria"),
 ("bratti2003", "Bratti 2003 labour force participation and marital fertility of Italian women"),
]

def get(url, tries=4):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 * (t + 1))
                continue
            return None
        except Exception:
            time.sleep(1.5 * (t + 1))
    return None

def search(q):
    url = ("https://api.crossref.org/works?rows=3&select=DOI,title,author,issued,"
           "container-title,volume,issue,page,publisher,type,URL&mailto=" + MAILTO +
           "&query.bibliographic=" + urllib.parse.quote(q))
    d = get(url)
    if not d:
        return None
    items = d.get("message", {}).get("items", [])
    return items[0] if items else None

def fmt(it):
    def name(a):
        if a.get("family"):
            return (a.get("given", "") + " " + a["family"]).strip()
        return a.get("name", "")
    return dict(
        doi=it.get("DOI"), title=(it.get("title") or [""])[0],
        authors=[name(a) for a in (it.get("author") or [])],
        year=(it.get("issued", {}).get("date-parts") or [[None]])[0][0],
        journal=(it.get("container-title") or [""])[0],
        volume=it.get("volume"), issue=it.get("issue"), pages=it.get("page"),
        publisher=it.get("publisher"), type=it.get("type"), url=it.get("URL"))

def verify(doi):
    d = get("https://api.crossref.org/works/" + urllib.parse.quote(doi) +
            "?mailto=" + MAILTO)
    if not d:
        return None
    return fmt(d["message"])

if __name__ == "__main__":
    raw = json.load(open(RAW)) if os.path.exists(RAW) else {}
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for key, q in QUERIES:
        if key in out and out[key].get("status") == "verified":
            continue
        it = search(q)
        if not it:
            out[key] = dict(query=q, status="search_failed")
            raw[key] = None
            print(key, "SEARCH FAILED", flush=True)
            continue
        rec = fmt(it)
        v = verify(rec["doi"]) if rec["doi"] else None
        if v:
            rec.update(v)
            rec["status"] = "verified"
        else:
            rec["status"] = "doi_lookup_failed"
        rec["query"] = q
        raw[key] = it
        out[key] = rec
        print(key, rec["status"], rec["doi"], "|", rec["title"][:60], rec["year"], flush=True)
        json.dump(raw, open(RAW, "w"), indent=1)
        json.dump(out, open(OUT, "w"), indent=1)
        time.sleep(0.4)
    n_ok = sum(1 for v in out.values() if v.get("status") == "verified")
    print(f"\n{ n_ok }/{len(out)} verified; wrote {OUT}")
