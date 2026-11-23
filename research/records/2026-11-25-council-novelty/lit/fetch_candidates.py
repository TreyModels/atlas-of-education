#!/usr/bin/env python3
"""Crossref verification for Synthetic Council candidate lit reviews."""
import json, os, time, urllib.parse, urllib.request
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"candidate_refs.json")
MAILTO="trey@atlasofeducation.example"; UA="atlas-council-lit/1.0 (mailto:%s)"%MAILTO
QUERIES=[
 ("liu_raftery2020","Liu Raftery 2020 how do education and family planning accelerate fertility decline"),
 ("taylor1976","Taylor Newman Fuchs 1976 the child survival hypothesis"),
 ("palloni1999","Palloni Rafalimanana 1999 the effects of infant mortality on fertility revisited"),
 ("kalemli2003","Kalemli-Ozcan 2003 stochastic model mortality fertility human capital investment"),
 ("soares2005","Soares 2005 mortality decline human capital investment economic growth"),
 ("doepke2005","Doepke 2005 child mortality and fertility decline Barro-Becker model fit the facts"),
 ("porzio2021","Porzio Rossi Santangelo 2021 the human side of structural transformation"),
 ("herrendorf2014","Herrendorf Rogerson Valentinyi 2014 growth and structural transformation"),
 ("boli1985","Boli Ramirez Meyer 1985 explaining the origins and expansion of mass education"),
 ("soysal1989","Soysal Strang 1989 construction of the world education regime"),
 ("benavot1988","Benavot Riddle 1988 the expansion of primary education 1870-1940"),
 ("sandberg1979","Sandberg 1979 the case of the impoverished sophisticate human capital Swedish economic growth"),
 ("mitch1992","Mitch 1992 the rise of popular literacy in Europe"),
 ("goldstein2009","Goldstein Sobotka Jasilioniene 2009 the end of lowest-low fertility"),
 ("myrsky2009","Myrskyla Kohler Billari 2009 advances in development reverse fertility declines"),
 ("sobotka2011","Sobotka 2011 fertility in Central and Eastern Europe after 1989"),
 ("frejka2008","Frejka Sobotka 2008 fertility in Europe diverse delayed and below replacement"),
 ("benjamini1995","Benjamini Hochberg 1995 controlling the false discovery rate"),
 ("phipson2010","Phipson Smyth 2010 permutation p-values should never be zero"),
 ("patel2015","Patel Burford Ioannidis 2015 assessment of vibration of effects due to model specification"),
 ("young2017","Young Holsteen 2017 model uncertainty and robustness a computational framework"),
 ("beaumont2019","Beaumont 2019 approximate Bayesian computation annual review of statistics"),
 ("csillery2010","Csillery Blum Gaggiotti Francois 2010 approximate Bayesian computation in ecology and evolution"),
 ("marin2012","Marin Pudlo Robert Ryder 2012 approximate Bayesian computation in practice"),
 ("scheffer2012","Scheffer 2012 anticipating critical transitions"),
 ("dakos2012","Dakos 2012 methods for detecting early warnings of critical transitions in time series"),
 ("kefi2014","Kefi 2014 early warning signals of ecological transitions methods for spatial patterns"),
 ("lewis1954","Lewis 1954 economic development with unlimited supplies of labour"),
 ("timmer1988","Timmer 1988 the agricultural transformation"),
 ("galor2006","Galor Moav 2006 das human-kapital a theory of the demise of the class structure"),
 ("preston1978","Preston 1978 the effects of infant and child mortality on fertility"),
]
def get(u,tries=4):
    for t in range(tries):
        try:
            r=urllib.request.Request(u,headers={"User-Agent":UA})
            return json.load(urllib.request.urlopen(r,timeout=25))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504): time.sleep(3*(t+1)); continue
            return None
        except Exception: time.sleep(2*(t+1))
    return None
def fmt(it):
    def nm(a): return (a.get("given","")+" "+a.get("family","")).strip() if a.get("family") else a.get("name","")
    return dict(doi=it.get("DOI"),title=(it.get("title") or [""])[0],authors=[nm(a) for a in it.get("author",[])],
      year=(it.get("issued",{}).get("date-parts") or [[None]])[0][0],journal=(it.get("container-title") or [""])[0],
      volume=it.get("volume"),issue=it.get("issue"),pages=it.get("page"),publisher=it.get("publisher"),type=it.get("type"),url=it.get("URL"),status="verified")
if __name__=="__main__":
    out=json.load(open(OUT)) if os.path.exists(OUT) else {}
    for key,q in QUERIES:
        if key in out and out[key].get("status")=="verified": continue
        d=get("https://api.crossref.org/works?rows=3&select=DOI,title,author,issued,container-title,volume,issue,page,publisher,type,URL&mailto="+MAILTO+"&query.bibliographic="+urllib.parse.quote(q))
        items=(d or {}).get("message",{}).get("items",[])
        if not items: out[key]=dict(query=q,status="search_failed"); print(key,"FAILED",flush=True); continue
        rec=fmt(items[0]); v=get("https://api.crossref.org/works/"+urllib.parse.quote(rec["doi"])+"?mailto="+MAILTO) if rec["doi"] else None
        if v: rec.update(fmt(v["message"])); rec["status"]="verified"
        else: rec["status"]="doi_lookup_failed"
        rec["query"]=q; out[key]=rec
        print(key,rec["status"],rec["doi"],"|",rec["title"][:55],rec["year"],flush=True)
        json.dump(out,open(OUT,"w"),indent=1); time.sleep(0.6)
    print("done",sum(1 for v in out.values() if v.get("status")=="verified"),"/",len(out))
