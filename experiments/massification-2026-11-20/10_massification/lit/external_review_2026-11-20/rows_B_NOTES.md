# Strands (c) and (d) — what the external literature already settles

**Prepared:** 2026-11-20 · **Companion file:** `rows_B_absorption_credential.csv` (27 rows: 16 strand c, 11 strand d).
**Verification:** 14 VERIFIED-FULLTEXT, 6 VERIFIED-ABSTRACT, 7 UNVERIFIED.

**Method note (read before trusting the URL column).** `web_fetch` is non-functional in this session: every hostname, including `example.com`, resolves to a non-routable 198.18.x.x address and the fetch aborts. Retrieval was done with `curl` (which routes correctly), text extracted with `pypdf`, and identity cross-checked against the Crossref and OpenAlex APIs. "VERIFIED-FULLTEXT" = I read the body text at that URL; "VERIFIED-ABSTRACT" = I read the abstract (sometimes the publisher's Crossref deposit, which is *not* the publisher's landing page); "UNVERIFIED" = not read, do not cite. Two items a referee would most expect — Nelson & Phelps (1966) and Vandenbussche, Aghion & Meghir (2006) — fall in that last category.

---

## Strand (c) — absorptive capacity, thresholds, dual-economy structure

### ESTABLISHED

Dual economy remains the default. Lewis (1954, [full text](https://www.depfe.unam.mx/doctorado/teorias-crecimiento-desarrollo/lewis_1954.pdf)) gives the mechanism: modern-sector expansion draws labour at a constant subsistence wage, growth being the reinvested surplus; his "central problem" is the move from "4 or 5 per cent" to "12 to 15 per cent. of national income or more". Harris & Todaro (1970, [full text](https://www.aeaweb.org/aer/top20/60.1.126-142.pdf)) add: migration responds to the *expected* wage, so urban unemployment is an equilibrium and job creation below migration *raises* unemployment.

Absorption is conditional. Abramovitz (1986, [abstract](https://api.crossref.org/works/10.1017/S0022050700046209)) makes catch-up depend on "social capability"; McMillan & Rodrik (2011, [full text](https://www.nber.org/system/files/working_papers/w17143/w17143.pdf)) show structural change has been growth-*reducing* in Africa and Latin America since 1990; Rodrik (2015, [full text](https://www.nber.org/system/files/working_papers/w20935/w20935.pdf)) shows the industrialization hump shifted down. Technology is skill-biased by income level (Caselli & Coleman 2006, [full text](http://personal.lse.ac.uk/casellif/papers/wtf.pdf)); complementarity belongs to particular production regimes, not to technology as such (Goldin & Katz 1998, [full text](https://www.nber.org/system/files/working_papers/w5657/w5657.pdf); Autor, Levy & Murnane 2003, [full text](http://www.frbsf.org/economics/conferences/0311/alm-skillcontent-qje.pdf)).

More schooling has not bought growth on average: Pritchett (2001, [abstract](https://api.openalex.org/works/doi:10.1093/wber/15.3.367)) finds "no association" with output per worker and a negative TFP association; Krueger & Lindahl (2001, [full text](https://www.nber.org/system/files/working_papers/w7591/w7591.pdf)) reconcile macro and micro — the *initial stock* matters, not the change, and secondary/tertiary matter more than primary. The middle-income slowdown is a regularity, not a law (Eichengreen, Park & Shin 2012, [full text](https://www.nber.org/system/files/working_papers/w16919/w16919.pdf): "around $17,000").

### CONTESTED

Whether the threshold is a threshold at all: the frontier-conditional result (Vandenbussche et al. 2006) is the canonical formalisation, but I could not read it and distance-to-frontier measures carry weak identification. Whether structural change is cause or residual is a deflation question. Whether the "trap" is a trap — selection can mimic it. And the premise that returns fall with income level is *not* established by what I read: Psacharopoulos & Patrinos (2018, [abstract](https://api.openalex.org/works/doi:10.1596/1813-9450-8402)) give "9 percent a year", with no income gradient stated.

### WHAT A CAREFUL PROGRAMME STILL CANNOT ASSUME

No threshold *value* for the Philippines: none estimates one, and importing "$17,000" would reify what the literature warns against. No zero return below a line — Pritchett's are explicitly "on average" results. "Absorptive capacity" is a placeholder, not a measured index. And the dual-economy frame is neither obsolete nor directly portable: Harris-Todaro is the cleanest theory of educated unemployment as equilibrium, but Lewis's constant-wage mechanism may not survive a remittance- and BPO-driven labour market. Treat the threshold as a hypothesis to locate in Philippine data, with level-composition (tertiary vs. primary) as the discriminating observable.

---

## Strand (d) — expansion, educated unemployment, credential/queue, matching

### ESTABLISHED

Freeman (1976) named the phenomenon and Collins (1979) gave it its mechanism (credential inflation as status closure); Spence (1973) and Arrow (1973) supplied screening. None of those four could be read here, so the magnitudes come from modern sources. The World Bank's 2026 Philippines assessment ([full text](https://openknowledge.worldbank.org/server/api/core/bitstreams/1e48613c-2045-441f-aa91-b9f92484b91b/content)) reports "39 percent" of workers overeducated, "real wages for college graduates were flat" against "nearly 50 percent" growth for below-secondary workers, and "college graduates in their twenties face higher unemployment rates than any other group". PIDS ([full text](https://pidswebs.pids.gov.ph/CDN/document/pidsdps2532.pdf)) reports "one in five workers with tertiary education credentials engaged in occupations that primarily require basic skills", with licence premia only where education and occupation match.

Theory has been disciplined by data. Leuven & Oosterbeek (2011, [full text](https://docs.iza.org/dp5523.pdf)) find surplus-schooling returns "only around 45%" of required-schooling returns, rejecting both pure human capital and pure job competition; McGuinness (2006, [abstract](https://api.openalex.org/works/doi:10.1111/j.0950-0804.2006.00284.x)) shows incidence is largely a measurement artefact. The queue has a real absorber: IT-BPM at "1.9 million jobs", "more than 8 percent" of GDP, adding "around 80,000 jobs" at "4 percent" growth (IBPAP, via [Daily Tribune](https://tribune.net.ph/2026/01/01/it-bpm-sector-posts-strong-growth-in-2025-eyes-nearly-2m-jobs)).

### CONTESTED

Whether graduate unemployment is mismatch or reservation wages: the World Bank asserts both in a single sentence, i.e. the available data cannot separate them. How much of the return is signal versus skill. Whether overeducation is a persistent state or a career stage — Leuven & Oosterbeek pose this explicitly ("Is 30 percent of the workforce permanently overschooled ...?").

### WHAT A CAREFUL PROGRAMME STILL CANNOT ASSUME

That Philippine graduate unemployment proves excess supply — the reservation-wage channel is live and unidentified. That BPO absorption continues: 80,000 jobs a year is an order of magnitude below the graduate flow, a ratio to compute rather than assume. That the "seven in 10 graduates not employable in their chosen occupation" figure is Philippine — PIDS cites it to Aspiring Minds (2017), an India-based assessment; use the one-in-five vertical-mismatch figure instead. And no magnitudes from Freeman, Collins, Arrow or Thurow: those four rows are placeholders, with the verifiable equivalents in the World Bank, PIDS and Leuven & Oosterbeek rows.

---

## URLs fetched

Status key: **FT** = full text read; **ABS** = abstract read; **META** = record/metadata only (no substantive text); **FAIL** = attempted, blocked or unusable.

### Strand (c)
- https://www.depfe.unam.mx/doctorado/teorias-crecimiento-desarrollo/lewis_1954.pdf — FT (Lewis 1954, 31pp retyped)
- https://www.aeaweb.org/aer/top20/60.1.126-142.pdf — FT (Harris & Todaro 1970, 17pp)
- https://www.aeaweb.org/aer/top20/56.1-2.69-75.pdf — FAIL (404; Nelson & Phelps not in AEA top-20 archive)
- https://www.aeaweb.org/aer/top20/56.1.69-75.pdf — FAIL (404)
- https://www.aeaweb.org/aer/top20/56.2.69-75.pdf — FAIL (404)
- https://cowles.yale.edu/sites/default/files/files/pub/d01/d0189.pdf — FAIL (returns HTML search page)
- https://www.rand.org/content/dam/rand/pubs/papers/2008/P3295.pdf — FAIL (404)
- https://api.crossref.org/works/10.1017/S0022050700046209 — ABS (Abramovitz 1986)
- https://research.rug.nl/en/publications/86407a2f-5d6e-4ace-9899-27c9bdf6baf2 — ABS (Timmer, de Vries & de Vries 2015)
- https://www.nber.org/system/files/working_papers/w17143/w17143.pdf — FT (McMillan & Rodrik 2011)
- https://www.wider.unu.edu/sites/default/files/wp2011-056.pdf — FT (McMillan & Rodrik 2011, WIDER version)
- https://www.nber.org/system/files/working_papers/w20935/w20935.pdf — FT (Rodrik 2015)
- http://personal.lse.ac.uk/casellif/papers/wtf.pdf — FT (Caselli & Coleman 2006)
- http://dash.harvard.edu/bitstream/handle/1/12490648/Distance%20to%20Frontier,%20Growth,%20and%20the%20Composition%20of%20Human%20Capital.pdf — FAIL (HTTP 429, three attempts)
- http://www.ifs.org.uk/wps/wp0431.pdf — FAIL (404)
- https://api.openalex.org/works/doi:10.1093/wber/15.3.367 — ABS (Pritchett 2001)
- https://openknowledge.worldbank.org/bitstreams/cfee8052-482f-5b11-93fa-aada2fb5fa6e/download — FAIL (2.4 KB HTML gate)
- https://www.nber.org/system/files/working_papers/w7591/w7591.pdf — FT (Krueger & Lindahl 2001)
- https://dataspace.princeton.edu/bitstream/88435/dsp011831cj939/1/429revised.pdf — FAIL (HTTP 401)
- https://api.openalex.org/works/doi:10.1596/1813-9450-8402 — ABS (Psacharopoulos & Patrinos 2018)
- http://documents.worldbank.org/curated/en/442521523465644318/pdf/WPS8402.pdf — FAIL (301 into blocked documents1 host)
- https://www.nber.org/system/files/working_papers/w16919/w16919.pdf — FT (Eichengreen, Park & Shin 2012)
- http://www.frbsf.org/economics/conferences/0311/alm-skillcontent-qje.pdf — FT (Autor, Levy & Murnane 2003)
- https://www.nber.org/system/files/working_papers/w8337/w8337.pdf — FAIL (unreadable text layer)
- https://www.nber.org/system/files/working_papers/w5657/w5657.pdf — FT (Goldin & Katz 1998)

### Strand (d)
- https://openlibrary.org/search.json?q=The+Overeducated+American+Freeman — META (Freeman 1976; text not read)
- https://openlibrary.org/search.json?q=The+Credential+Society+Collins — META (Collins 1979; text not read)
- https://api.crossref.org/works/10.1016/0047-2727(73)90013-3 — META (Arrow 1973; no abstract in deposit)
- https://api.crossref.org/works/10.2307/1882010 — ABS (Spence 1973; abstract field is the table of contents)
- https://docs.iza.org/dp5523.pdf — FT (Leuven & Oosterbeek 2011)
- https://api.openalex.org/works/doi:10.1111/j.0950-0804.2006.00284.x — ABS (McGuinness 2006)
- https://pidswebs.pids.gov.ph/CDN/document/pidsdps2532.pdf — FT (PIDS DP 2025-32)
- https://openknowledge.worldbank.org/server/api/core/bitstreams/1e48613c-2045-441f-aa91-b9f92484b91b/content — FT (World Bank 2026, 115pp)
- https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@asia/@ro-bangkok/@ilo-manila/documents/publication/wcms_742036.pdf — FT (ILO 2020, 2pp)
- https://tribune.net.ph/2026/01/01/it-bpm-sector-posts-strong-growth-in-2025-eyes-nearly-2m-jobs — FT (IBPAP figures)
- https://documents1.worldbank.org/curated/en/099085003172324737/pdf/P173234007c9e00ad08b7b0200872373c69.pdf — FAIL (host unreachable)
- https://documents1.worldbank.org/curated/en/333521498727263689/pdf/Developing-socioemotional-skills-for-the-Philippines-labor-market.pdf — FAIL (host unreachable; snippet only)
- https://psa.gov.ph — FAIL (HTTP 403; no Philippine LFS retrievable here)
- https://www.ibpap.org/knowledge-hub — FAIL (JS-rendered; no figures in HTML)
- https://www.adb.org/publications?keywords=middle-income%20trap — FAIL (JS-rendered)

### Infrastructure used for verification
- https://api.crossref.org/works/{DOI} — bibliographic verification of every DOI in the CSV
- https://api.openalex.org/works/doi:{DOI} — abstracts and open-access location discovery
- https://openlibrary.org/search.json — existence/author/year check for the three monographs
