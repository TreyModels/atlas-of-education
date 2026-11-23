# 5. Implications: how the field should estimate and read the relation

## 5.1 For estimation practice

The first implication is a design-reporting rule: **state which parameter the design identifies, and do not
report a change coefficient as an estimate of the level relation** (or vice versa). The two designs answer
different questions, and the paper's numbers make the difference concrete. A levels coefficient of −0.129 is a
between-country gradient; a change coefficient of +0.111 is a within-country association between increments. The
field's habit of treating the second as a robustness check on the first is the source of the apparent
contradiction. A paper that reports both, with the level explicitly named, is not hedging; it is being precise.
Concretely: report the between-country coefficient when the question is "where do high-fertility countries
sit?", report the within-country coefficient when the question is "does a country's extra schooling predict a
faster fall?", and do not use the latter to dismiss the former.

The second implication concerns **attenuation**. The change design is not an unbiased estimator of a causal
effect that happens to be small; it is an estimator that removes the between-country variation in which the
gradient lives. If the relation is a development gradient — and the placebo says it is — then the within
coefficient is attenuated toward zero by construction, and the attenuation is a property of the design, not
evidence about the world. The literature that reads small within-country coefficients as "education does not
matter" is reading design-induced attenuation as a substantive null. The correct inference from a small within
coefficient is that the short-run within-country association is small, not that the between-country gradient is
illusory. Symmetrically, the correct inference from a large between coefficient is that countries differ, not
that a schooling programme would work.

The third implication is about **specification reporting**. The paper's specification curve is a practical
template: pre-register the space, report every cell, and let the distribution be the result. The contrast
between the levels and changes distributions (99.7 per cent negative-significant versus a sign-mixed,
mostly-insignificant grid) is the kind of evidence that a single coefficient cannot provide, and it is what
makes the audit credible to a reader who suspects a selected specification. Journals and referees can ask for
the distribution at modest cost; the code and records here are public.

## 5.2 For interpreting the existing within-country literature

The existing within-country schooling–fertility literature is not wrong, and the paper should not be read as
saying so. The individual and micro-econometric literature identifies effects of schooling on fertility using
policy changes, school construction, cash transfers, and sibling/cohort comparisons (Duflo, 2001; Chicoine,
2012, 2021; Osili & Long, 2008; Baird, McIntosh, & Özler, 2011; Breierova & Duflo, 2004; Ainsworth, Beegle, &
Nyamete, 1996), and it finds effects. Those designs identify local causal effects of specific schooling changes
on specific populations; they do not identify the between-country gradient, and the between-country gradient
does not identify them. The macro panel change literature is the ambiguous case: its estimates are attenuated by
design for the reasons above, and the paper's decomposition suggests that its nulls should be read as
"short-run within-country association is weak", not as "schooling does not affect fertility". The survey-level
section (7.1) adds the missing middle: the DHS ecological gradient is large and negative in every pipeline
tercile, which is consistent with the micro literature and cannot confirm it; the individual-level test requires
the microdata that were not obtainable.

For policy, the implication is a warning about **reading change-designed estimates as programme effects**. A
policy evaluation that finds no effect of a schooling expansion on fertility within a decade may be correctly
estimated and still say nothing about the long-run development gradient; a cross-country association that is
large in levels may be a development marker and still say nothing about a programme. The paper's placebo result
is the formal statement of the second half of that warning, and the attenuation argument is the first half.

## 5.3 For the "development gradient versus causal lever" distinction

The paper's central interpretive distinction is between a gradient and a lever. A gradient describes where
countries sit; a lever describes what moves them. The schooling–fertility relation is a gradient: global,
robust, steepest at the massification margin, and — the placebo says — not identified as a lever. This is not a
deflationary conclusion. Gradients are what comparative demography is good at measuring, and knowing where a
country sits relative to the schooling–fertility frontier is useful for description, forecasting, and for
framing questions about mechanism. What a gradient cannot do is license the claim that expanding schooling will
produce the fertility decline that the cross-section associates with it. That claim requires a design in which
schooling changes for reasons unrelated to fertility, and the paper's future-research section names the designs
and data that could supply one.

The distinction also resolves a puzzle in the policy literature. Pronatalist and anti-natalist policies are
often justified by reference to cross-country associations, and often evaluated with within-country change
designs; the two literatures then appear to contradict each other. They do not. The cross-country association
is a gradient; the policy evaluation is a lever estimate; the first is informative about where the second is
likely to be found, and neither substitutes for the other. The care-work nulls in Section 7.2 make the same
point on the policy side: a mechanism that looks plausible in cross-section (care burdens, credit constraints)
can be absorbed by income and urbanisation, and the paper reports that absorption as a finding rather than
burying it.
