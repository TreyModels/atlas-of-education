# Search strategy and databases (Paper F, recorded 2026-11-25)

The prior-art review was built in two layers. First, a structured Crossref search: 73 bibliographic
queries (`lit/fetch_refs.py`, query strings in that file) covering the schooling–fertility literature,
the aggregation/ecological-fallacy critique, the within–between/fixed-effects literature, specification
curves and multiverses, transportability/external validity, the demographic transition, quantity–quality,
massification, and pronatalist policy. Each query's top Crossref match was then **verified by DOI lookup**
(`api.crossref.org/works/{DOI}`), and the full metadata stored in `lit/refs.json` with a status per record.
Second, a narrative/web search layer (Web search and Google Scholar snippets, 24-25 Nov 2026) to find
papers whose titles are not standard classics; candidate titles were then fed through the same Crossref
verification. Section owners (panel-matrix, multiverse-400, gpu-dose) supplied their own prior-art lists
with DOI status, which were independently checked against Crossref before being merged.

Limits of the search: Crossref's bibliographic matching is title-oriented, so a few books/chapters have no
DOI (recorded as such in `refs.md`); grey literature and non-English work are underrepresented; and the
search is not a systematic review (no PRISMA-style screening), so "we are not aware of" statements in the
draft are tied to the specific query list in `lit/fetch_refs.py`, not to an exhaustive census.
