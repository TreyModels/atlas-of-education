#!/usr/bin/env python3
"""Verify the paper's candidate references against the Crossref API and record DOI status.

For every candidate work: query api.crossref.org with a bibliographic string, keep the best match by
title similarity and year proximity, and record the DOI, matched title, container and a confidence flag.
Output: refs_crossref.json and a readable table. No citation is fabricated: entries with no adequate
Crossref match are marked NO_MATCH and are cited in the paper only if they are books/working papers
that Crossref does not index (status recorded per entry in refs.md).
"""
import json, difflib, time, urllib.parse, urllib.request

OUT = "/root/work/paper_sequencing" if False else "."
MAILTO = "trey@treymodels.com"

# key, authors, year, title, venue/type (venue is only a hint; Crossref match is title+year based)
REFS = [
    # --- human capital / education demand ---
    ("schultz1961", "Schultz, T. W.", 1961, "Investment in human capital", "American Economic Review"),
    ("becker1964", "Becker, G. S.", 1964, "Human capital: A theoretical and empirical analysis, with special reference to education", "Book"),
    ("becker1960", "Becker, G. S.", 1960, "An economic analysis of fertility", "Book chapter"),
    ("mincer1958", "Mincer, J.", 1958, "Investment in human capital and personal income distribution", "Journal of Political Economy"),
    ("mincer1974", "Mincer, J.", 1974, "Schooling, experience and earnings", "Book"),
    ("goldin1998", "Goldin, C.", 1998, "America's graduation from high school: The evolution and spread of secondary schooling in the twentieth century", "Journal of Economic History"),
    ("goldinkatz2008", "Goldin, C., & Katz, L. F.", 2008, "The race between education and technology", "Book"),
    ("acemogluautor2011", "Acemoglu, D., & Autor, D.", 2011, "Skills, tasks and technologies: Implications for employment and earnings", "Handbook of Labor Economics"),
    ("autor2014", "Autor, D. H.", 2014, "Skills, education, and the rise of earnings inequality among the other 99 percent", "Science"),
    ("nelsonphelps1966", "Nelson, R. R., & Phelps, E. S.", 1966, "Investment in humans, technological diffusion, and economic growth", "American Economic Review"),
    ("beckerlewis1973", "Becker, G. S., & Lewis, H. G.", 1973, "On the interaction between the quantity and quality of children", "Journal of Political Economy"),
    # --- world culture / institutionalist ---
    ("meyer1977", "Meyer, J. W.", 1977, "The effects of education as an institution", "American Journal of Sociology"),
    ("meyerramirezsoysal1992", "Meyer, J. W., Ramirez, F. O., & Soysal, Y. N.", 1992, "World expansion of mass education, 1870-1980", "Sociology of Education"),
    ("ramirezboli1987", "Ramirez, F. O., & Boli, J.", 1987, "The political construction of mass schooling: European origins and worldwide institutionalization", "Sociology of Education"),
    ("soysalstrang1989", "Soysal, Y. N., & Strang, D.", 1989, "Construction of the first mass education systems in nineteenth-century Europe", "Sociology of Education"),
    ("benavotriddle1988", "Benavot, A., & Riddle, P.", 1988, "The expansion of primary education, 1870-1940: Trends and issues", "Sociology of Education"),
    ("boliramirezmyer1985", "Boli, J., Ramirez, F. O., & Meyer, J. W.", 1985, "Explaining the origins and expansion of mass education", "Comparative Education Review"),
    ("schofermeyer2005", "Schofer, E., & Meyer, J. W.", 2005, "The worldwide expansion of higher education in the twentieth century", "American Sociological Review"),
    ("meyerrowan1977", "Meyer, J. W., & Rowan, B.", 1977, "Institutionalized organizations: Formal structure as myth and ceremony", "American Journal of Sociology"),
    ("dimaggiopowell1983", "DiMaggio, P. J., & Powell, W. W.", 1983, "The iron cage revisited: Institutional isomorphism and collective rationality in organizational fields", "American Sociological Review"),
    # --- state building / compulsory schooling ---
    ("soysal1994", "Soysal, Y. N.", 1994, "Limits of citizenship: Migrants and postnational membership in Europe", "Book"),
    ("floraalber1981", "Flora, P., & Alber, J.", 1981, "Modernization, democratization, and the development of welfare states in Western Europe", "Book chapter"),
    ("flora1983", "Flora, P., Kraus, F., & Pfenning, W.", 1983, "State, economy, and society in Western Europe 1815-1975: A data handbook", "Book"),
    ("lindert2004", "Lindert, P. H.", 2004, "Growing public: Social spending and economic growth since the eighteenth century", "Book"),
    ("alesinareich2013", "Alesina, A., & Reich, B.", 2013, "Nation building and education", "Working paper"),
    ("gradsteinjustman2002", "Gradstein, M., & Justman, M.", 2002, "Education, social cohesion, and economic growth", "American Economic Review"),
    ("gradsteinjustmanmeier2005", "Gradstein, M., Justman, M., & Meier, V.", 2005, "The political economy of education: Implications for growth and inequality", "Book"),
    ("bowlesgintis1976", "Bowles, S., & Gintis, H.", 1976, "Schooling in capitalist America: Educational reform and the contradictions of economic life", "Book"),
    ("sanderson1999", "Sanderson, M.", 1999, "Education and economic decline in Britain, 1870 to the 1990s", "Book"),
    ("mitch1984", "Mitch, D.", 1984, "Underinvestment in literacy? The potential contribution of government involvement in elementary education to economic growth in nineteenth-century England", "Journal of Economic History"),
    ("mitch1993", "Mitch, D.", 1993, "The role of human capital in the first industrial revolution", "Book chapter"),
    ("west1967", "West, E. G.", 1967, "The political economy of public school legislation", "Journal of Law and Economics"),
    # --- Prussia / France / US / Britain economic history ---
    ("schleunes1989", "Schleunes, K. A.", 1989, "Schooling and society: The politics of education in Prussia and Bavaria, 1750-1900", "Book"),
    ("diebolt2005", "Diebolt, C., Jaoul, M., & San Martino, G.", 2005, "The 'new economic history' and the reconstruction of education systems", "Book chapter/working paper"),
    ("goldinkatz2008b", "Goldin, C., & Katz, L. F.", 2008, "Education and income in the early twentieth century: Evidence from the prairies", "Journal of Economic History"),
    ("goldin2001", "Goldin, C.", 2001, "The human-capital century and American leadership: Virtues of the past", "Journal of Economic History"),
    # --- structural change / agriculture ---
    ("boppart2023", "Boppart, T., Kiernan, P., Krusell, P., & Malmberg, H.", 2023, "The macroeconomics of intensive agriculture", "NBER Working Paper"),
    ("restuccia2008", "Restuccia, D., Yang, D. T., & Zhu, X.", 2008, "Agriculture and aggregate productivity: A quantitative cross-country analysis", "Journal of Monetary Economics"),
    ("gollin2002", "Gollin, D., Parente, S., & Rogerson, R.", 2002, "The role of agriculture in development", "American Economic Review"),
    ("gollin2010", "Gollin, D.", 2010, "Agricultural productivity and economic growth", "Handbook of Agricultural Economics"),
    ("adamopoulos2014", "Adamopoulos, T., & Restuccia, D.", 2014, "The size distribution of farms and international productivity differences", "American Economic Review"),
    ("herrendorf2014", "Herrendorf, B., Rogerson, R., & Valentinyi, A.", 2014, "Growth and structural transformation", "Handbook of Economic Growth"),
    ("caselli2005", "Caselli, F.", 2005, "Accounting for cross-country income differences", "Handbook of Economic Growth"),
    ("schultz1964", "Schultz, T. W.", 1964, "Transforming traditional agriculture", "Book"),
    ("matsuyama1992", "Matsuyama, K.", 1992, "Agricultural productivity, comparative advantage, and economic growth", "Journal of Economic Theory"),
    ("buera2022", "Buera, F. J., Kaboski, J. P., & Rogerson, R.", 2022, "Skill-biased structural change", "Review of Economic Studies"),
    # --- demography relevant to the fertility framing ---
    ("doepke2005", "Doepke, M.", 2005, "Child mortality and fertility decline: Does the Barro-Becker model fit the facts?", "Journal of Population Economics"),
    ("galorweil2000", "Galor, O., & Weil, D. N.", 2000, "Population, technology, and growth: From Malthusian stagnation to the demographic transition and beyond", "American Economic Review"),
    ("preston1975", "Preston, S. H.", 1975, "The changing relation between mortality and level of economic development", "Population Studies"),
    # --- methods / inference ---
    ("pesaran2006", "Pesaran, M. H.", 2006, "Estimation and inference in large heterogeneous panels with a multifactor error structure", "Econometrica"),
    ("eberhardt2011", "Eberhardt, M., & Teal, F.", 2011, "Econometrics for grumblers: A new look at the literature on cross-country growth empirics", "Journal of Economic Surveys"),
    ("steegen2016", "Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W.", 2016, "Increasing transparency through a multiverse analysis", "Perspectives on Psychological Science"),
    ("simonsohn2020", "Simonsohn, U., Simmons, J. P., & Nelson, L. D.", 2020, "Specification curve analysis", "Nature Human Behaviour"),
    ("phipsonsmyth2010", "Phipson, B., & Smyth, G. K.", 2010, "Permutation p-values should never be zero: Calculating exact p-values when permutations are randomly drawn", "Statistical Applications in Genetics and Molecular Biology"),
    ("benjaminihochberg1995", "Benjamini, Y., & Hochberg, Y.", 1995, "Controlling the false discovery rate: A practical and powerful approach to multiple testing", "Journal of the Royal Statistical Society: Series B"),
    ("brockdurlauf2001", "Brock, W. A., & Durlauf, S. N.", 2001, "Growth empirics and reality", "World Bank Economic Review"),
    ("alesina2013", "Alesina, A., & Reich, B.", 2013, "Nation building and education", "Working paper"),
]


def query(ref):
    key, authors, year, title, venue = ref
    q = f"{authors.split(',')[0]} {year} {title}"
    url = ("https://api.crossref.org/works?query.bibliographic=" + urllib.parse.quote(q) +
           "&rows=5&select=DOI,title,author,issued,container-title,type&mailto=" + MAILTO)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "atlas-education/1.0 (mailto:%s)" % MAILTO}), timeout=40) as r:
                return json.load(r)["message"]["items"]
        except Exception as e:
            print("retry", key, e, flush=True)
            time.sleep(2 + 2 * attempt)
    return []


def best_match(items, title, year):
    best = None
    for it in items:
        t = (it.get("title") or [""])[0]
        if not t:
            continue
        sim = difflib.SequenceMatcher(None, title.lower(), t.lower()).ratio()
        yr = None
        try:
            yr = it["issued"]["date-parts"][0][0]
        except Exception:
            pass
        year_ok = yr is not None and abs(int(yr) - year) <= 3
        score = sim + (0.15 if year_ok else 0.0)
        if best is None or score > best[0]:
            best = (score, sim, it, yr)
    return best


if __name__ == "__main__":
    results = {}
    for ref in REFS:
        key, authors, year, title, venue = ref
        items = query(ref)
        m = best_match(items, title, year)
        if not m:
            results[key] = dict(status="NO_QUERY_RESULT", title=title, year=year, authors=authors)
            print("NO_RESULT", key, flush=True)
            continue
        score, sim, it, yr = m
        doi = it.get("DOI")
        mtitle = (it.get("title") or [""])[0]
        cont = (it.get("container-title") or [""])
        if sim >= 0.80 and yr is not None and abs(int(yr) - year) <= 2:
            status = "MATCH"
        elif sim >= 0.65:
            status = "WEAK_MATCH"
        else:
            status = "NO_MATCH"
        results[key] = dict(status=status, similarity=round(float(sim), 2), doi=doi,
                            matched_title=mtitle, matched_year=yr, container=cont[0] if cont else "",
                            authors=authors, year=year, title=title, venue_hint=venue)
        print(status, key, "sim=%.2f" % sim, "doi=", doi, "|", mtitle[:80], flush=True)
    json.dump(results, open("refs_crossref.json", "w"), indent=1)
    ok = sum(1 for v in results.values() if v["status"] == "MATCH")
    weak = sum(1 for v in results.values() if v["status"] == "WEAK_MATCH")
    no = sum(1 for v in results.values() if v["status"] not in ("MATCH", "WEAK_MATCH"))
    print(f"\nsummary: MATCH {ok}, WEAK {weak}, NO {no}, total {len(results)}")
    open("refs_crossref_summary.txt", "w").write(
        f"Crossref verification run 24 Nov 2026, api.crossref.org, query.bibliographic, "
        f"title-similarity + year filter.\nMATCH {ok}, WEAK {weak}, NO {no}, total {len(results)}\n")
