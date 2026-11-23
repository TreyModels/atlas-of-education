# Paper N4 — final argument read (draft at 685c34c, 7,167 words)

Auditor: `novelty-review`, 24 November 2026. Read of `research/records/2026-11-25-paper-shape/PAPER.md` against the
lead's five checks: shape-claim discipline, cluster framing, determinants causality, "no first", and
implications/future-research sections.

## Overall: PASS with three fixes (one substantive, two minor)

The paper is disciplined where it matters. The claim that the exponential-to-floor form beats the logistic is
stated as a **measurement result about annual 1960–2023 series**, with the explicit sentence "This is a
descriptive result, not an argument against using logistic models in projection" (§5.1), and §1 and §2 frame the
paper as measurement/replication, not refutation. The cluster result is exactly as required: "two poles, not a
taxonomy", silhouette **0.275**, **0 of 500** random partitions reaching the real silhouette (p < 0.01 by the
1/(500+1) rule), and an explicit paragraph saying a silhouette of 0.28 is weak and "the continuum reading is the
correct one" (§5.4). The determinants section is associations throughout — mortality timing "strongest correlate"
with 0.24 (SE 0.036, n=101), "correlations, not causal effects" in the methods, and §9's "(v) No causal
identification". "No first" is explicit in §2.5 ("we do not claim to be first to notice that transitions differ").
Implications (§7: forecasting, model-country, policy timing, terminal enclosure, what would change our mind) and
Future research (§8: cohort fertility by education, subnational shapes, historical series, forecasting horse race)
are own sections and adequate.

## Fix 1 (substantive) — state that the logistic may be unidentified on the observed window, not refuted

The lead's test is whether "exponential-to-floor beats logistic" can be read as "the S-curve is wrong". As
drafted, §5.1's "The S-curve picture does not survive contact with the annual data", §1's "the S-curve is
over-claimed", and the conclusion's "the shape is not the one usually drawn" are all defensible **only with a
caveat that is currently missing**: with a 1960 start, many transitions are left-censored or still incomplete, so
a logistic fitted to this window is arguably misspecified or poorly identified rather than refuted. §9 notes
period-TFR and left-censoring generally, but the specific inference is never drawn.

Add two sentences — one in §5.1 after the "descriptive result" paragraph, one in §9:
> "The comparison is a goodness-of-fit statement about the observed 1960–2023 window, not a refutation of the
> S-curve as a description of complete transitions. Because the series start in 1960, many transitions are
> left-censored (the pre-decline plateau is unseen) and some are incomplete; a logistic fitted over the full
> transition, including the plateau, could fit better than it does on this window. The result is that the S-curve
> is not the best description of the annual series we can observe — not that the transition has no S-shaped phase."

That preserves the finding and removes the weakest referee attack. It also aligns with the paper's own §8
"historical series for the earliest transitions" extension.

## Fix 2 (literature gap) — five classic transition/shape works are absent

`git grep` across the N4 record finds no citation of these, and they are the standard props for a shape paper:
| Work | Why it is needed |
|---|---|
| **Thompson (1929)**, "Population", *American Journal of Sociology* 34(6) — the original three-stage transition statement | the classic S-curve origin; Notestein/Davis are cited but Thompson is the prior of priors |
| **Landry (1934)**, *La révolution démographique* | the other classic origin of the three-stage scheme |
| **Chesnais (1992)**, *The Demographic Transition: Stages, Patterns and Economic Implications* (Oxford UP) | the canonical book on transition **stages/patterns** and fast-vs-slow typology — directly the §5.4 subject |
| **Coale & Watkins (1986)**, *The Decline of Fertility in Europe* (Princeton UP; reissue DOI 10.1515/9781400886692) | the classic **shape-clustering precedent** (European provinces grouped into fertility regions) — exactly the k=2/two-pole comparison a referee will demand |
| **Bongaarts & Watkins (1996)**, *PDR* 22(4), 10.2307/2137804 | diffusion/social-interaction account of timing — the paper tests mortality timing; the diffusion rival should be cited |

These are missing rather than wrong, and all are book/no-DOI or DOI-verifiable as marked (Coale & Watkins reissue
10.1515/9781400886692; Bongaarts & Watkins 10.2307/2137804). Add them to §2.1-2.3 and refs.md with Crossref status,
marking books as standard citations. (Easterlin is optional; the five above are the referee-visible ones.)

## Fix 3 (minor) — the PC1 sentence reads as a tautology

§5.3: "the first principal component of the aligned curves explains essentially all of their variance (the second
component is numerically zero)". For curves that are nearly identical by construction, PC1 will dominate; the
paper's own alignment caveat covers this, but the sentence should say so: add "which is unsurprising once the
curves are aligned on the same endpoints; the informative number is the 0.017 spread, not the variance share."

## Checks that passed

- (b) Cluster: 0/500 stated, silhouette 0.275 stated, continuum framing explicit, k=3 shown to split the same
  continuum. Exactly the required honesty.
- (c) Determinants: "strongest correlate" is used with n=101 and §9's no-causal-identification; schooling-level
  results flagged as hypothesis (n=30); income coverage (n=18) reported, not imputed. No causal slide.
- (d) No priority claim; §2.5 explicit; scan of "first" finds only ordinal uses.
- (e) Implications and Future research are own sections and substantively adequate.
- Prior art otherwise strong: Notestein, Davis, Coale, Coale-Trussell, Alkema, Raftery, Cleland-Wilson, Reher,
  Bongaarts (2008), Bongaarts-Casterline (2013), Lesthaeghe, Dyson, Montgomery-Casterline, Lee, Soares — all
  present and Crossref-marked where applicable.

## Verdict

The paper's headline is **INCREMENTAL — a measurement/replication contribution** (better-fitting functional
forms on the observed window; path uniformity once aligned; two poles of a continuum; associations only), and the
draft says so consistently. With Fix 1 and Fix 2 it survives a demography referee; Fix 3 is polish.

---

## Addendum — fix (1) VERIFIED at 657877a (24 Nov)

Re-read of `PAPER.md` at 657877a confirms fix (1) is applied and coherent:
- **Abstract** now states the truncated-window caveat verbatim: "With truncated 1960–2023 series we cannot
  distinguish a genuinely non-logistic form from a logistic that the window leaves unidentified; the claim is that
  the exponential-to-floor family describes the available transition data better, **not that the S-curve is
  refuted**."
- **§5.1** opens with a dedicated "Identification caveat, stated first because it bounds every claim in this
  subsection": a logistic fitted to this window "can be *unidentified* rather than wrong"; the comparison is "a
  statement about the **estimable window** … not as a refutation of the S-curve as a description of the underlying
  process"; the caveat is explicitly extended to Gompertz and linear-kink; and the closing paragraph adds "the
  window cannot tell 'not logistic' from 'logistic left unidentified'".
- **§2.4** states the unidentified-vs-wrong distinction; **§1** and the **conclusion** are softened ("usually
  assumed rather than tested", "not the best description of the available annual data").
- The old drift phrases ("S-curve is over-claimed", "does not survive contact with the annual data", "not the one
  usually drawn") are gone from the record.
Fixes (2) five classic works and (3) the PC1 tautology clause were not yet in 657877a at re-read; cuda-scale is
applying them. Fix (1): **CLOSED**.

---

## Addendum 2 — fixes (2) and (3) VERIFIED at 3b73bc1; N4 SIGNED OFF

- Fix (2): the five classics are in. PAPER.md §2.1–2.3 cites Thompson (1929), Landry (1934), Chesnais (1992),
  Coale and Watkins (1986), and Bongaarts and Watkins (1996); refs.md entries 20–24 and claims-prior-art
  Claims 1/2/4/7 carry them with statuses. I independently verified two of the DOIs: Thompson 1929 AJS
  "Population" **10.1086/214874 V**; Chesnais 1992 **10.1093/oso/9780198286592.001.0001 V**. Coale & Watkins
  reissue 10.1515/9781400886692 and Bongaarts & Watkins 10.2307/2137804 were verified earlier in this audit.
- Fix (3): §5.3 now says "The variance share is unsurprising once the curves are aligned on the same endpoints;
  the informative number is the 0.017 cross-country spread, not the variance share."
- Fix (1) re-confirmed at 3b73bc1, now also explicit in §9 limitations ("a logistic fitted to it may be
  misspecified or poorly identified; the model comparison is a goodness-of-fit statement about the observed
  window, not a refutation of the S-curve as a description of complete transitions").
- Word count 7,657; numbers and SOURCES map unchanged. **N4: SIGNED OFF, all three fixes closed.**
