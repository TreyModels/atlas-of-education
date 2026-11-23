# Reference-defect closure (response to the independent lit audit, novelty-review)

The auditor identified 15 DOI-verified works missing from our independent list and 7 entries resolving to the
wrong paper. All are now fixed in `lit/build_refs.py` / `refs.md`; the corrected entries are marked below.
Crossref status: V = resolves with matching metadata; W = working-paper/pre-publication version; U = hand-cited.

## The 7 wrong-title entries — FIXED

| key | old resolution (wrong) | action taken | new entry / status |
|---|---|---|---|
| notestein1945 | "Population Problems of Palestine" (different Notestein 1945) | removed; classic cited by hand | Notestein (1945), "Population — the long view", in Schultz (Ed.), *Food for the World*, Univ. of Chicago Press — **U** |
| davis1963 | Davis & Blake (1956), "Social structure and fertility" | removed; correct paper added; 1956 paper kept separately | Davis (1963), *Population Index* 29(4) 345–366, **10.2307/2732014 — V**; Davis & Blake (1956), *EDCC* 4(3) 211–235, **10.1086/449714 — V** |
| becker1960 | Becker, Murphy & Tamura (1990) | removed; classic cited by hand | Becker (1960), "An economic analysis of fertility", in *Demographic and Economic Change in Developed Countries*, Princeton UP — **U** |
| schultz1961 | 1972 item | removed; classic cited by hand | Schultz (1961), "Investment in human capital", *AER* 51(1) 1–17 — **U** |
| trow1974 | year None | removed; cited by hand with year | Trow (1974), *Problems in the Transition from Elite to Mass Higher Education*, Carnegie Commission — **U** |
| chen2010 | 2026 paper (irrelevant) | removed | — |
| bongaarts2011 | duplicate of Bongaarts (1978) title | removed; 1978 entry retained | Bongaarts (1978), *PDR* 4(1) 105–132, **10.2307/1972149 — V** |

## The 15 missing DOI-verified works — ADDED (all V unless noted)

Cleland & Rodriguez (1988) 10.1080/0032472031000143566; Kravdal (2002) 10.2307/3088337; Kravdal (2012)
10.4054/demres.2012.27.22; Martín & Juárez (1995) 10.2307/2133523; Guinnane (2011) 10.1257/jel.49.3.589; Coale &
Watkins (1986) 10.1515/9781400886692 (reissue); Galor & Weil (2000) 10.1257/aer.90.4.806; Doepke (2005)
10.1007/s00148-004-0208-z; Lee (2003) 10.1257/089533003772034943; Granovetter (1978) 10.1086/226707; Scheffer et
al. (2009) 10.1038/nature08227; Sear, Mace & McGregor (2003) 10.1016/s1090-5138(02)00105-8; Coall & Hertwig (2010)
10.1017/s0140525x09991105; Beaumont, Zhang & Balding (2002) 10.1093/genetics/162.4.2025 and Beaumont, Cornuet,
Marin & Robert (2009) 10.1093/biomet/asp052; Del Moral, Doucet & Jasra (2012) 10.1007/s11222-011-9271-y.

Additional verified additions: Silberzahn et al. (2018) 10.1177/2515245917747646; Ainsworth, Beegle & Nyamete
(1996) 10.1093/wber/10.1.85; Breierova & Duflo (2004) 10.3386/w10513 (W); Baird, McIntosh & Özler (2011)
10.1093/qje/qjr032; Gauthier (2007) 10.1007/s11113-007-9033-x; Eberhardt & Teal (2011)
10.1111/j.1467-6419.2010.00624.x; Pearl & Bareinboim (2011) 10.1109/icdmw.2011.169; Corsi et al. (2012)
10.1093/ije/dys184.

## Hand-cited with no usable DOI (U)

Notestein (1945); Becker (1960); Schultz (1961); Trow (1974); Levine & Renelt (1992) *AER* 82(4) 942–963;
Thevenon (2011) *PDR* 37(1) 57–87; Rutstein & Johnson (2004) DHS Comparative Report 6; Thevenon & Gauthier (2011)
*Community, Work & Family* 14(4) 421–439; Razavi (2007) UNRISD; Folbre (2001) *The Invisible Heart*.

## Auditor framing point — accepted

The auditor is right that "levels vs changes is standard econometrics" and that a "we are not aware" claim cannot
carry the paper's novelty. Section 2 now frames the contribution as a **quantified audit** of a known correlation
(full specification space + 13,800-partition transportability + placebo + threshold location), cites the
principle as established (Robinson 1950; Nickell 1981; Brock & Durlauf 2001; Eberhardt & Teal 2011), and reserves
"we are not aware" for the specific combination of tests, with the search strategy recorded in
`SEARCH_STRATEGY.md`.
