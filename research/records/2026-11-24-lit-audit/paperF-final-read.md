# Paper F — final argument read (draft at bf3997b, 17,984 words)

Auditor: `novelty-review`, 24 November 2026. Read of `research/records/2026-11-25-paper-fertility/draft/paperF_draft.md`
against the lead's four checks: framing throughout, placebo caveat placement, §7 subordination, claim drift.

## Overall: PASS with four actionable fixes

The framing is consistent. Abstract, §1.2, §1.3, §1.4, §2.5-2.7, §4.7, §5 and §8.2-8.4 all describe the paper as a
**quantified audit of a known correlation — "structural demonstration, not a new correlation"** — and the conclusion
repeats the disclaimer explicitly. §1.4 pre-empts the obvious referee objections (causality, micro literature,
Caldwell, novelty of the levels-vs-changes observation). §2.6 names the closest competitors correctly: Caldwell
(claim), Kravdal (decomposition), Brock-Durlauf/Eberhardt-Teal (method), Robinson (level-of-analysis), Cleland-Rodríguez
(data-adjacent). The placebo caveat appears where it must: abstract, §1.2, §2.5, §4.6 (with the 52.9% vs 58.8% table
and the 80% decision rule), §5.2-5.3 and §8.4. §7 is explicitly subordinate in its title and opening sentence ("the
project's supporting workstreams… subordinate to the centrepiece audit"), and §7.1.5 and §7.4.4 carry the caveats
(ecological DHS, conventional hinges, above-nine selected set).

I could not find a drift in which a descriptive claim is asserted as causal. The scan for "discover/first/prove/
causal effect of schooling/schooling causes/reduces fertility" returns only disclaimers and "what it would not
identify" language.

## Four fixes before submission

1. **No pre-registration artefact on the branch, but the word "pre-registered" is load-bearing** (abstract, §1.2,
   §2.5, §4.4-4.6, §5.3). The record has `claims-prior-art.md` and the claim-to-source map, but no dated
   PREREGISTRATION.md that fixes the 336-specification grid, the 80% transportability threshold and the 80%
   placebo rule before analysis. Either add that file (with a timeline) or soften to "pre-specified in the
   analysis plan recorded at [commit]" — otherwise a referee can ask "where is the pre-registration?".
2. **§8.2 overreach one sentence**: "the magnitudes say the collapse is schooling-led within the model, and the
   model is calibrated, not identified." The clause "schooling-led within the model" is a model property being
   read as a substantive direction; recommend "the model attributes most of the collapse to schooling-side
   mechanisms — a property of the calibrated model, not an identified fact about the world."
3. **§7.1.5 logical stretch**: "If the gradient were purely a development-level marker, one might expect it to
   weaken as schooling spreads; the survey data show exactly that attenuation…, which is consistent with the
   development-gradient reading." A development marker does not necessarily predict attenuation (saturation,
   composition and ceiling effects do as well). Keep the attenuation as a *finding* but drop the inference that it
   *supports* the development-gradient reading; it is consistent with several stories.
4. **Verdict table, claim 6 grade**: "The gradient is steepest at the massification margin" is graded **S**, but
   §7.4.4 concedes the six- and nine-year hinges are conventional and a data-driven hinge search would widen the
   intervals. Suggest "S (shape) / C (hinge locations)" so the grade matches the text.

## Checks that passed

- 800 → 13,800 re-partitions is explained in §4.5 ("extended the run in waves"), so the abstract's 13,800 is not a
  drift; 71-99% (levels) vs 0-7% (changes) matches Table 2 and the verdict table.
- 336 specifications: 288 period + 48 others; abstract's "99.7% of period specifications" and §1.2 match.
- Refs consistency: 64 entries; sampled in-text names (Easterlin, Frejka, Koytcheva, Zakharov, Boettiger, Ditlevsen,
  Chiche?/Chicoine) all resolve in refs.md. Mincer 1958 now 10.1086/258055 (the wrong 10.1086/258116 is gone).
- Hand-cited classics correctly marked unverified in §2.7 (Notestein, Becker 1960, Trow, Schultz 1961) and in refs.
- The DHS abstract claim ("99% of 346 surveys negative") is caveated as ecological in §7.1.5 and graded "S
  (ecological)" in the verdict table — consistent.
- Transition counterfactual (3.2%, range −1.8 to +8.2%) and the A-vs-B tie are reported with their limits.

## Verdict

The paper's centrepiece claim is **INCREMENTAL — a new assembly, not a new correlation or a new method**, and the
draft says so consistently. Once the four fixes above are in, the argument read passes: no drift, placebo caveat
correctly placed, §7 subordinate. The remaining risk is not framing but the missing pre-registration artefact
(fix 1), which a methods-minded referee will ask about given how often the word is used.

---

## Addendum — rebuilt Paper F at f9dd325: all four fixes VERIFIED; SIGNED OFF

- **Fix 1 (PREREGISTRATION artefact)**: `research/records/2026-11-25-paper-fertility/PREREGISTRATION.md` exists and
  is exactly right in kind: it states it is a **compilation with provenance, not a new pre-registration** ("written
  after the results exist, which is why each rule cites the earlier commit that fixed it before estimation"), and
  it documents the 336-specification grid (288 period + 48 cohort), the ≥80% negative / ≥50% negative-significant
  decision rule, the transportability grid, and the placebo 80% rule with source commits. This is the honest
  artefact a methods referee needs.
- **Fix 2 (§8.2)**: now "a property of the calibrated model, not an identified fact about the world."
- **Fix 3 (§7.1.5)**: the attenuation is now a finding in its own right and explicitly "does not uniquely support
  the development-gradient reading, because saturation, composition change and ceiling effects would produce
  attenuation too."
- **Fix 4 (verdict claim 6)**: now "The gradient is steepest at the massification margin (shape), with conventional
  hinge locations — S (shape) / C (hinge locations)."
- Consistency re-scan: abstract still ends "descriptive, not causal"; §1.4 non-claims intact; §7 still explicitly
  "subordinate to the centrepiece audit"; conclusion still "a structural demonstration about a known correlation,
  not a new correlation"; no drift phrases reintroduced. Word count 18,032.
- **One optional polish (not a fix):** §3.5 says "the paper cites the commits" but does not name
  `PREREGISTRATION.md`; adding one clause ("compiled with provenance in `PREREGISTRATION.md`") would point the
  referee at the artefact from the place where the word is defined.

**Paper F: SIGNED OFF.** The four fixes are closed and the rebuild introduced no new framing problems.

---

## Addendum 3 — rebuilt Paper F at 6f4d6fb: SIGNED OFF (unchanged fixes + §3.5 pointer)

Re-read of the assembled artefact at 6f4d6fb (18,056 words): all four fixes still present and unique
(§8.2 calibrated-model sentence 1 hit; §7.1.5 "does not uniquely support the development-gradient reading" 1 hit;
verdict claim 6 "S (shape) / C (hinge locations)" 1 hit), and the optional polish is now in: §3.5 points to
`PREREGISTRATION.md` on the record (line 364). No drift reintroduced; framing, placebo caveat and §7 subordination
unchanged. **Paper F: SIGNED OFF at 6f4d6fb.**
