# Literature anchors for the charter-fiscal model — round 1 notes

Purpose: attach the model's free parameters to something checkable. Written 2026-11-23.
Companion to `litreview.md`; this file is notes, not prose, and is deliberately blunt
about what is anchored and what is not.

## Anchored

**The temple economy exists as a distinct fiscal sector, and it is the mechanism the
model calls the ratchet.**
Piphal Heng, "The Temple Economy of Angkor", in *The Angkorian World* (Routledge, 2023),
DOI 10.4324/9781351128940-23. Religion was not decorative: temples held land, labour and
revenue rights, and the inscriptional record is largely a record of those transfers.
This supports modelling endowments as a permanent alienation of taxable base rather than
as consumption. It does **not** give a rate.

**The city is low-density and dispersed, so "population" is a modelling choice, not a fact.**
Roland Fletcher, "Angkor", *Oxford Handbook of Early Southeast Asia* (2022),
DOI 10.1093/oxfordhb/9780199355358.013.33. Consistent with the low-density urbanism
framing in §2 of litreview.md.

## Not anchored — these are the model's weakest links

1. **Endowment rate.** The model's single most influential parameter (`endowRate`; Morris
   score 7.0, everything else ≤ 2.2) has no empirical value. Nobody I could reach states
   "temples held X% of cultivated land by year Y". What would fix it: a systematic sum of
   land and labour grants across the dated inscription corpus, expressed as a share of a
   stated cultivated-area estimate — which requires the second quantity to be settled first.
2. **Plausible range for the cultivated area.** 1,110 km² is carried from the earlier
   model and is a derived figure (occupation density × mapped extent), not a measurement
   of planted fields. Every absolute number in the model scales with it.
3. **Timing of the fiscal peak.** The model wants ~1150; the parameter that delivers it
   (`endowRate` ≈ 0.00025/yr) is roughly an order of magnitude below what the inscription
   record implies qualitatively. This is the one place where the model is *falsifiably
   wrong* rather than merely uncertain, and it should be reported as such.

## Consequence for the next rounds

Do not tune `endowRate` to hit 1150 and then present the fit as a result. Either
(i) derive a rate from the corpus and report the peak year it implies, or
(ii) present the peak year as a function of the rate and state which rates are defensible.
Option (ii) is what `analysis_v8.json` E10 already does; keep it that way.

## Searches that failed (do not repeat blindly)

- Semantic Scholar has no record for the Routledge chapter DOI; Crossref has the book
  chapter but no abstract.
- A Crossref query combining "Khmer inscriptions corpus endowments labour" returned
  malformed JSON on this attempt (transient); retry with a plain-text query if needed.
- No source found that quantifies the fraction of Angkorian cultivated land under temple
  control in any century. If such a number exists it is buried in a thesis or in the
  Lustig & Lustig epigraphic corpus, not in an indexed article.
