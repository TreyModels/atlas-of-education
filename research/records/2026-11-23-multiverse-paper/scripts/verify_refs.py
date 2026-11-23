#!/usr/bin/env python3
"""Verify bibliography entries against Crossref (bibliographic fields only, not content).
Prints one compact record per DOI. Nothing is inferred: fields that Crossref omits are printed as MISSING.
Usage: python3 verify_refs.py
"""
import json, sys, urllib.request

DOIS = [
 ("Steegen et al 2016 multiverse", "10.1177/1745691616658637"),
 ("Simonsohn et al 2020 spec curve", "10.1038/s41562-020-0912-z"),
 ("Gelman & Loken 2014 American Scientist", "10.1511/2014.111.460"),
 ("Simmons et al 2011 false-positive", "10.1177/0956797611417632"),
 ("Wicherts et al 2016 degrees of freedom", "10.3389/fpsyg.2016.01832"),
 ("Bonhomme & Manresa 2015", "10.3982/ECTA11319"),
 ("Benjamini & Hochberg 1995", "10.1111/j.2517-6161.1995.tb02031.x"),
 ("Pearl & Bareinboim 2014", "10.1214/14-STS486"),
 ("Bareinboim & Pearl 2016 PNAS", "10.1073/pnas.1510506113"),
 ("Cameron & Miller 2015", "10.3368/jhr.50.2.317"),
 ("Bertrand et al 2004", "10.1162/003355304772839588"),
 ("Young & Holsteen 2017 SMR", "10.1177/0049124115626179"),
 ("Del Giudice & Gangestad 2021", "10.1177/2515245920974622"),
 ("Lipsitch et al 2010 negative controls", "10.1097/EDE.0b013e3181d61eeb"),
 ("Ernst 2004 permutation", "10.1214/088342304000000396"),
 ("Phipson & Smyth 2010", "10.2202/1544-6115.1585"),
 ("Hope 1968 Monte Carlo", "10.1111/j.2517-6161.1968.tb00742.x"),
 ("Hotz Imbens Mortimer 2005", "10.1016/j.jeconom.2004.05.007"),
 ("Bonhomme Lamadon Manresa 2022", "10.3982/ECTA17550"),
 ("Sala-i-Martin 1997", "10.1257/aer.87.2.178"),
 ("Brock & Durlauf 2001", "10.1093/wber/15.2.229"),
 ("Young 2019 Channeling Fisher", "10.1093/qje/qjy029"),
 ("Abadie et al 2023 clustering", "10.1093/qje/qjac038"),
 ("Munoz & Young 2018 nested p", "10.1177/0081175018783976"),
 ("Tipton 2013 generalization", "10.3102/1076998612441947"),
 ("Cameron Gelbach Miller 2008", "10.1162/rest.90.3.414"),
 ("Orben & Przybylski 2019", "10.1038/s41562-018-0506-1"),
 ("Rodrik 2012 regressing growth", None),
]

BASE = "https://api.crossref.org/works/"

def get(doi):
    req = urllib.request.Request(BASE + doi, headers={"User-Agent": "atlas-ref-check/1.0 (mailto:trey@treymodels.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["message"]

def authors(m):
    out = []
    for a in m.get("author", []):
        out.append((a.get("family", "?"), a.get("given", "")))
    return out

for label, doi in DOIS:
    if doi is None:
        print(f"== {label}: NO DOI IN LIST (fill manually; see notes)")
        continue
    try:
        m = get(doi)
        au = authors(m)
        print(f"== {label}\n   DOI {doi}\n   title: {m.get('title',['MISSING'])[0]}\n"
              f"   authors: {'; '.join(f'{f}, {g}' for f,g in au) if au else 'MISSING'}\n"
              f"   container: {(m.get('container-title') or ['MISSING'])[0]}\n"
              f"   year: {(m.get('issued',{}).get('date-parts') or [['MISSING']])[0][0]}  volume: {m.get('volume','MISSING')}  issue: {m.get('issue','')}  page: {m.get('page','MISSING')}\n"
              f"   publisher: {m.get('publisher','MISSING')}")
    except Exception as e:
        print(f"== {label}\n   DOI {doi}\n   FETCH FAILED: {e}")
