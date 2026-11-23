# Decision: what is genuinely novel, what carries a paper, and what to stop doing

**Council verdict, 25 Nov 2026 (revised after the auditor's diff).** After a 42-claim inventory, independent
Crossref verification of prior art for every candidate, and a five-perspective panel, the answer to Dr. Menefee's
question is blunt: **the programme contains no new correlation**. It contains one **conditional** methodological
contribution — the multiverse draw-count arithmetic, which counts as a rule only once the dependence /
effective-number-of-tests correction is formalised — two new assemblies that already have drafts, and one
model-based demonstration with a strong negative result. Everything else is a
replication, a null test of a known hypothesis, or an audit. The right response is to publish four things, fold
two into them, and stop three.

## The four that carry a paper

**1. "Schools before factories": schooling take-off precedes agricultural labour release — NEW ASSEMBLY (rank 1).**
Panel mean 3.8 (highest). Draft: Paper M, 17,371 words, branch `research/paper-massification-2026-11-25`
@ `753e102`. Closest competitor: Porzio, Rossi & Santangelo (2021, NBER w29390, W). Why publish: a systematic
multi-country sequencing with supply/demand decomposition and an agricultural floor that nobody has assembled in
this form — the panel's economic historian scored it 5. Binding conditions: (i) the retracted 68.75%/69% ordering figure must not appear — **already corrected at
`research/paper-massification-2026-11-25` @ `95dc135`, then `76d929a` (17,433 words), verified by run-lead's
independent recomputation**: on the **64 three-event countries** (schooling take-off, farm-exit and fertility
turning points all dated), the six corrected locations report strict schooling-first **37.5% (24/64, CI
26.6–50.0)**, simultaneous **31.25% (20/64)**, fertility-first **31.25% (20/64)**, median gap 0 (IQR −5/+8); the
all-81 variant with both dates is **35.8% (29/81)**; the 68.75% was 24 + 20 ties counted as schooling-first. The
source record is annotated at `subsistence-v2` @ `8caaeac`. Keep the two orderings separate: those are
**schooling-vs-fertility** figures; the **release-vs-fertility** metric is a different analysis on the 64 countries
with both a farm-exit and a fertility date — **60/64 = 93.75% fertility-first, 4/64 = 6.25% release-first (AFG,
LBR, MWI, ZMB)**, 0 ties; (ii) the paper
must frame the sequence as a dating-and-assembly result, not a causal claim, because schooling and agricultural
release are jointly determined by industrialisation; (iii) endogeneity/coarse-dating objections get a dedicated
paragraph, not a footnote.

**2. Paper F — the levels-vs-changes/transportability schooling–fertility audit — NEW ASSEMBLY, INCREMENTAL.**
Panel mean 3.2; already drafted and audited (branch `research/paper-fertility-2026-11-25` @ `f9dd325`, 17,310 words
before refs, 64 refs). Closest competitor: Liu & Raftery (2020, PDR, 10.1111/padr.12347, V). Why publish: the
field knows the within/between critique (Robinson 1950; Nickell 1981; Durlauf et al. 2005; Eberhardt & Teal 2011)
but has not had the systematic demonstration for this relation, with 13,800 random partitions and a future-schooling
placebo that measures the development-gradient caveat. Binding condition: never claim a new correlation — the
framing "quantified audit of a known correlation" is the contribution (the PREREGISTRATION.md artefact now exists
with provenance).

**3. The GPU full-transition counterfactual — NEW ASSEMBLY / DEMONSTRATION.** Panel mean 3.2.
**Status: the only paper-carrying candidate with no draft.** The evidence and a section draft exist
(`research/paper-boppart-2026-11-24` @ `90feb1e`, folded into Paper F §7.3), but no standalone paper exists; the
next session owns writing it. Evidence:
`research/transition-gpu` @ `f9f2f18`, `dose-gpu` @ `774085c`, `dose-tolerance` @ `baadfe6`; section drafted at
`90feb1e`. Closest prior: SOCSIM-era microsimulation (U) and the Galor–Weil/Doepke mortality mechanisms (V).
Why publish: the mortality-freeze removes only 3.2% of the collapse in a fitted individual-level engine, and the
individuation model does **not** beat development-only out of sample (+3.32 [−3.76,+11.14], 3/6) — a useful
negative result plus a demonstration. Binding conditions: model-structural framing in title, abstract and
conclusion; the unresolved tension with the country-level child-survival link gets its own section; the
pre-antibiotic arc's failure is reported as a scope limit, not hidden.

**4. The multiverse resolution arithmetic — INCREMENTAL / border-NEW design arithmetic (NOT a headline NEW METHOD).**
Panel mean 2.2 after the auditor's correction. Evidence: Paper N2 / methods paper
`research/methods-multiverse-paper-2026-11-23` @ `f9673a9`, novelty ledger `390db8d`. Closest competitors:
Patel, Burford & Ioannidis (2015, 10.1016/j.jclinepi.2015.05.029, V); Simonsohn, Simmons & Nelson (2020,
10.1038/s41562-020-0912-z, V; the 2015 SSRN version, 10.2139/ssrn.2694998, V); Steegen et al. (2016, V); Klau et
al. (2020, 10.1093/ije/dyaa164, V). What is new: the explicit draw-count rule applied to a random-partition
multiverse — nothing more. **Accepted referee kill shot:** random re-partitions are correlated, so BH's
independence/PRDS assumption fails and the 5,440/182 figures assume independent tests; the rule needs
Benjamini–Yekutieli (2001, 10.1214/aos/1013699998, V) or an effective-number-of-tests correction (Galwey 2009,
10.1002/gepi.20408, V; Cheverud 2001, 10.1046/j.1365-2540.2001.00901.x, V; Li & Ji 2005, 10.1038/sj.hdy.6800717, V).
Without that correction it is a methods-note observation; rank it below this paper and below Paper F.

## Folded, not standalone

- **Child-mortality level vs volatility (E1)**: level +0.0067 (0.0015) is 1976-vintage (Taylor et al. 1976,
  V; Preston 1978, V; Palloni & Rafalimanana 1999, V); the volatility null (MDE 0.0046/0.0056) is the new part.
  It belongs inside the mechanisms paper, not as its own paper.
- **DHS survey-level gradient and its contradicted dynamic predictions**: it is the reconciliation section of
  Paper F (§7.1), already integrated; the individual-level test needs the unobtainable DHS Individual Recodes and
  is future work, not a paper.

## Do not pursue (kill list)

| item | why kill |
|---|---|
| "Electricity does not drive schooling" | Micro literature is large and mostly positive; the result is the standard common-trend warning (grouping-multiverse-400 `1152cec`; prior novelty ledger `390db8d`). KNOWN. |
| "Child survival drives fertility" | Child-survival hypothesis is 1976 (Taylor et al., V). KNOWN. |
| "Individuation is refuted" | One poor-fitting model with unidentified strengths (dose-tolerance `baadfe6`); the defensible statement is the out-of-sample tie, already inside candidate 3. KNOWN/model-artefact. |
| Credential inflation | Positional-credential literature is old (Collins); the +0.81 audit correlation (care-credential `e626cb8`) does not carry a paper. KNOWN. |
| Threshold hinges at 6/9 years as a discovery | Hinges are conventional; no canonical DOI-verified threshold paper exists (auditor and our search agree). Grade shape S, hinges C — already done in Paper F. KNOWN. |
| Care-work loop / tipping point / diminishing returns as findings | Pre-registered nulls of known mechanisms (England & Folbre 1999; Scheffer et al. 2009, V; Dakos et al. 2012, V). Nulls are valuable inside Paper F; not a paper. |
| Scaling/Heaps/regime break | Audits of known scaling results, one new negative (no regime break); not a new law (scaling `fd691a6`). AUDIT. |
| Marriage-age / UN living-arrangements | Known UN data; the levels-vs-change artefact is a methods lesson (un-marriage `b2b18d5`). KNOWN. |
| The 69% "schooling precedes fertility" ordering | **RETRACTED, CORRECTION VERIFIED** — the source JSON's 68.75% counted ties as schooling-first; events-CSV recomputation gives 35.8%; Paper M corrected all six locations at `95dc135`/`76d929a` to strict schooling-first 37.5% (24/64, CI 26.6–50.0), simultaneous 31.25% (20/64), fertility-first 31.25% (20/64) on the **64 three-event countries** (median gap 0, IQR −5/+8; all-81 variant 35.8% = 29/81), and the source record is annotated at `subsistence-v2` @ `8caaeac`. No paper may cite the 69% figure. Do not conflate this with the separate **release-vs-fertility** analysis, on the 64 countries with both a farm-exit and a fertility date, where 60/64 = 93.75% fertility-first and 4/64 = 6.25% release-first (AFG, LBR, MWI, ZMB), 0 ties. |

## If forced to pick three

Keep **(1) schools before factories; (2) Paper F audit; (3) the GPU counterfactual** (the negative out-of-sample
result is the publishable part), and publish the multiverse arithmetic only as a methods note after a BY /
effective-number-of-tests correction — otherwise drop it from the paper list. There is no fifth paper.

## Immediate actions

1. Paper M: ordering correction **done and verified** at `95dc135`/`76d929a` (strict 37.5% [26.6–50.0];
   simultaneous 31.3%; fertility-first 31.3%; all-81 35.8%; source record annotated at `subsistence-v2` @
   `8caaeac`). Remaining: keep the schooling-vs-fertility and release-vs-fertility counts separate and keep the
   dating/endogeneity paragraph and the "late-industrialiser regularity, not universal law" framing.
2. Paper F: cover letter and abstract lead with the audit framing and the placebo caveat; the PREREGISTRATION.md
   provenance artefact is in place; close the auditor's four fixes (now pushed at f9dd325).
3. Methods paper: state the draw-count rule's assumptions; submit to a methods venue.
4. GPU counterfactual: retitle around the negative result (individuation does not beat development-only) and the
   identification limit; the 3.2% is a model-structural magnitude, not a headline.
5. DHS Individual Recode acquisition would be the single largest upgrade available: it would turn Paper F's
   §7.1 from an ecological reconciliation into an individual-level test (free DHS account + dataset request; the
   exact variables are listed in `research/dhs-micro-2026-11-23` `data/microdata_probe.txt`).
