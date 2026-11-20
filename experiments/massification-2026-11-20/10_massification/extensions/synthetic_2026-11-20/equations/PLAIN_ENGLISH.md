# PLAIN ENGLISH — what each theory of school expansion actually says

*For a reader who does not work with statistics. One short paragraph per theory family. Jargon is translated in
brackets.*

**1. "World society".** Schools spread because being a modern country means having mass schooling. Governments copy
each other — the same global pledges, ministries and laws — because that is what a legitimate state looks like, often
*before* the economy needs it or the money exists to deliver it (decoupling = adopting the form of a policy without the
substance). In data this should look like countries at very different income levels expanding at the same time. **How
it is written down mathematically: nowhere.** A statistical model was run, but its equation and numbers were never
retrieved.

**2. Human capital.** Schooling is an investment. Each extra year makes a worker more productive, so employers pay
more — about **8.8 per cent more per year of school** worldwide. Families see that payoff and keep children in school
longer, so enrolment should rise with income and *slow down* when the payoff falls. When it keeps rising while the
payoff falls, this story is in trouble — which is what the project noticed. **This is one of the few pieces genuinely
written as an equation** (the "Mincer" earnings equation: log earnings = intercept + return × years of school). But
8.8 per cent is a *price*, and nobody in the retrieved literature says how much enrolment moves when the price moves.
That step is a plausible sentence, not an equation.

**3. Queue and credential.** Think of jobs as a queue ranked by how much training each needs, best jobs at the front.
Schooling moves you up the queue but does not make you more productive — its value is your *position*. So when
everyone gets the old diploma, it stops working and the requirement moves up a level (the ratchet). This family has the
best-written equations in the package — a pass mark set a fixed distance above the class average, tutoring as a contest
for a fixed bar, and a two-family game where paying becomes unavoidable once the prize is worth more than twice the cost.
But those equations are about *who wins the contest*, not how many children are in school.

**4. State capacity.** A law alone does nothing. What moves children into classrooms is the state's ability to deliver
and enforce: enough teachers (pupils per teacher), enough money (education spending as a share of national income), and
credible enforcement. Hong Kong passed free primary education in 1971 and crossed 90 per cent enrolment three years
later; the Philippines has had compulsory primary schooling on the books since at least 1987 (and a 1953 law that was
never funded) and its top level still sits at 75 per cent. **The literature gives this as a story with no equation**, so
the project wrote its own: effect = law × capacity-to-the-power-0.75. Those numbers were chosen by the team, and the
robustness check over the 0.75 was announced but never run.

**5. Demography.** Schooling is delivered to however many children were born six years earlier. Large cohorts mean
thinner resources per child; shrinking cohorts mean more. The pattern that survives is that higher fertility goes with
lower primary completion (estimate about −0.19; the project recorded only that the relation was "semi-log", so the
units must be re-read before reuse). The project's model builds the birth cohort from the fertility rate, ages it one
year at a time, and enters school at six. That arithmetic is a reasonable convention, but the constants (a 35-year
childbearing span, a 50/50 sex split, three survival rates) are declared assumptions, and the fertility effect is
graded "not verified" in the literature.

**6. The project's own push-pull model.** This is the machine the team built rather than found. Children enter at six;
a share move up each level each year; those shares rise with income and urbanisation, and in the "demand-led" version
also when jobs were plentiful a few years earlier. A second channel lets a better-educated workforce raise growth.
Three versions run by switching one channel off, which asks cleanly "does schooling follow jobs, or jobs follow
schooling?" — and the answer is that the data cannot tell. **Almost every equation here was invented by the project.**
Two things to know: the completion numbers it fits never touch the birth cohorts, and its enrolment ratios come out in
the hundreds of per cent, which makes its timing results unreliable.

**7. Scaling laws.** "Scaling laws" say: when X rises one per cent, Y rises *b* per cent, with *b* stable across many
settings. The reviewed literature has exactly **one** genuine example — city size and output, where patents rise 1.27
per cent per one per cent of population — and **no** education example. What exists for education is the project's own
estimates from 30 countries: a one per cent richer country has about 0.22 per cent higher secondary enrolment and 0.57
per cent higher tertiary enrolment; within a country over time tertiary is higher still (0.85) and secondary nearly
vanishes (0.09). Enrolment over time also looks like an S-curve — slow, fast, then flat — but whether that S is
logistic or asymmetric (Gompertz) is unresolved, and every curve form failed the project's held-out test.

**8. Sectoral change.** As countries get richer, farm employment shrinks and services grow. The project writes this as
simple formulas — farm share falls as a fixed exponential of log income, services take a fixed share of the non-farm
economy rising with income and education. The literature supplies the *pattern* (farm shares fall with income) but
**not the functional form for these countries**, so the constants (0.75, 0.35, 0.45, 0.55…) were chosen by the team; the
project's own audit calls the sector block a relabelled income term. Economic complexity (how sophisticated a country's
exports are) has no specified link to schooling anywhere in the reviewed material.

---

## What we can actually simulate today

1. **Cohort arithmetic** — births from fertility, one-year ageing, entry at six. Sound accounting; the constants are
   declared assumptions.
2. **S-curves** — logistic or Gompertz fitting returns a ceiling, a speed and a halfway year. Curve-fitting, not a test
   of any theory.
3. **Income gradients** — the 30-country exponents (0.22 secondary, 0.57 tertiary across countries; 0.09 and 0.85
   within) are real estimates, usable as a target the generator is *asked* for, never given.
4. **A capacity-gated push** — only with the index and the exponent declared as assumptions and swept.
5. **The push-pull test itself** — which runs, and returns the honest verdict: the two directions are observationally
   equivalent on this data.

## What is narrative only

1. **World society** — no equation, no coefficients, no series; a timing story only.
2. **The human-capital *response*** — the 8.8 per cent price is real; the rule turning it into an enrolment decision is
   absent. Anyone writing "enrolment responds to returns" is choosing a form, not reading one.
3. **The credential queue** — real equations, but about effort and winners, not expansion; requirement ratcheting, MMI
   and relative risk aversion have no equations.
4. **Enforcement** — no enforcement series exists anywhere in the package; anything said about it is inference.
5. **Sectoral forms and complexity** — the pattern is real, the formulas are the team's invention.

**One-line summary.** The literature gives solid equations about *prices, contests and gates*; the project has a machine
that produces *enrolment paths*; the bridge between them — how a price or a gate becomes a family's decision to keep a
child in school — is written down by no one in this package. That bridge is the choice a synthetic-data generator must
make explicitly, and declare.
