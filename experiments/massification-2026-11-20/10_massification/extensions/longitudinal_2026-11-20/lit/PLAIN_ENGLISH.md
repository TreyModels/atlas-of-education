# Plain English — did schooling, or literacy, or complexity move growth?

*For a non-statistician. Companion to [`EXPECTATIONS.csv`](EXPECTATIONS.csv) and
[`SYNTHETIC_TARGETS.md`](SYNTHETIC_TARGETS.md).*

## What the literature actually says

The well-known claim (Hanushek and Woessmann) is that **what a population can actually do** — measured by test
scores — predicts growth, while **how many years people sat in school** does not. That is a claim about *learning*,
not about *attendance*.

The second robust number is the **wage premium**: one extra year of schooling is associated with about **8.8%**
higher earnings worldwide (Psacharopoulos and Patrinos 2018). That is about pay, not about national growth.

The complexity literature (Hidalgo and Hausmann) says countries that make a wider variety of sophisticated products
grow faster than their income alone would predict.

One warning first: **our own literature file contains none of the growth sources** — it is a ledger of
private-tutoring studies. The growth claims above are marked UNVERIFIED in `EXPECTATIONS.csv`, not read from our
shelf. Nothing on this question is currently verifiable in-house.

## Why the 2015 literacy result is unsurprising

You saw years of schooling flat and literacy moving with growth. Three things make that unsurprising rather than
strange.

**Literacy is measured as a stock of adults, and stocks move by generations.** Roughly **62–66%** of the measured
rise in adult literacy in our data is old illiterate cohorts dying and literate young cohorts arriving — not adults
learning. So literacy is a slow, generational index of how literate a workforce already is. Years of schooling is a
different thing: a proxy built from attainment shares, which we have to construct ourselves because true mean years
of schooling is not in our data.

**These are two vintages of human capital.** Complexity tracks the *recent flow* (primary completion ten years
earlier, coefficient 0.593); adult literacy is the *old stock*. Our own addendum records that ECI follows the
completion flow but not the adult-literacy stock (youth literacy does co-move, +4.49). Different vintages are not
substitutes, so finding one predictive and the other not is expected rather than contradictory.

**And the loud variable is thin.** Adult literacy exists for only 275 country-years across 28 countries, against 900
for GDP growth — a fifth of the coverage, so any literacy coefficient rests on far fewer cells than the growth series
it is compared with.

## What ECI is

ECI is the Economic Complexity Index: a country's place in a network of who exports what to whom. A high score means
the export basket needs many kinds of know-how that few other countries have. It is a *description of the productive
structure*, not a measure of schooling — which is why it is plausible that it conditions what education is worth.

## What would count as evidence, for and against

**For "literacy matters, years do not":** in our 30-country 1995–2024 panel with country fixed effects, literacy
positive with a confidence interval excluding zero, while the years proxy is insignificant or less than half its
standardized size. That is the pre-declared test.

**Against:** the years proxy is positive and significant while literacy is not; or both vanish; or the pattern only
appears in the simple cross-section and not with country fixed effects.

**For the "kickstarted economy" gating story:** the literacy–growth slope being at least 50% steeper in
high-complexity than low-complexity terciles.

**Against — and this is the uncomfortable part:** our own interaction estimates run the **opposite** way. Schooling's
growth association is stronger in *low*-complexity economies (completion × ECI −0.039; tertiary × ECI −0.077). At the
same time ECI itself does **not** predict 10-year growth here (−0.142, not significant), and tertiary enrolment
fifteen years earlier is *negatively* associated with growth (−1.035).

**What none of this establishes.** These are associations in thirty countries. They cannot show that schooling
*causes* growth: our identification audit shows the competing stories fit the same data equally well, so no
direction claim is permitted. A null here means "not supported in this sample", not "disproved".
