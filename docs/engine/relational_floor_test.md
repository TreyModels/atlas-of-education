# Does the relational floor show up in household data? A simulation test of H2

Results note, 5 November 2026. Model: `engine/relfloor.py`. Experiment: `engine/relfloor_mc.py` → `engine/results/relfloor_mc.md`. Paper tested: Menefee & Nordtveit, *Massification and Its Mechanisms* (revised June 2026), hypothesis H2.

## Design

Each Philippine household decides whether its child completes the terminal basic credential: 4 secondary years before 2016, 6 after K-12. The credential's value has three parts, mirroring the paper's typology:

- **Human capital:** the relative wage premium, scaled by the child's ability.
- **Positional:** a penalty for not holding the credential, which grows with the share of the previous cohort that holds it.
- **Relational:** a fixed eligibility value that does not depend on ability or saturation.

Every structure also includes these mechanisms:
- direct and foregone-earnings costs;
- real income growth;
- a liquidity constraint;
- rerouting to a cheaper legible credential (TESDA-style) on exit.

There are three structures:
- **M_HC:** human capital only.
- **M_POS:** human capital plus positional.
- **M_REL:** all three components.

The fit to history is checked against four patterns (draws are accepted only if all hold):
- completion about 62% in 2000;
- completion about 73% in 2024;
- the late-1990s income gradient: bottom 40% at 30–52%, top 60% at 62–85%;
- no collapse at K-12.

20,000 parameter draws per structure.

## Results

| | Fits history | Q3+ completion if the **relative** premium falls 40% (2024→35) | If only **absolute** wages compress | Share of exits from the bottom 40% | K-12 effect, Q1 / Q5 (2018) |
|---|---|---|---|---|---|
| Human capital only | 0.4% of draws | **−13.8 pts** [−19.7, −10.1] | 0 | **52%** [46, 62] | −2.4 / −2.8 pts |
| + positional | 0.3% | −9.8 pts [−17.0, −3.7] | 0 | 53% [46, 99] | −2.0 / −3.0 |
| + relational | 0.1% | **−0.9 pts** [−13.1, 0] | 0 | **94%** [48, 100] | −0.2 / −0.4 |

Brackets are 5–95% across accepted draws.

## What it means for the paper

1. **History does not discriminate.** All three structures reproduce the 62→73% climb and the 1990s gradient, and human capital alone does it most easily. Income growth against fixed costs is enough. The paper's statement that "the relational floor held" after K-12 is not evidence for the floor.
2. **Absolute compression is not a test.** When graduate wages fall but the relative premium holds (bumping down), no structure predicts that investment falls. The paper's puzzle as currently stated ("investment intensifies as absolute returns compress") does not contradict human-capital theory. H2 becomes a test only where the **relative** premium falls.
3. **Where the relative premium falls, the structures separate.** Human capital predicts the completion of means-capable households (Q3+) drops about 14 points. The relational floor predicts it barely moves. Positional value only slows the decline; **none of the structures produces intensification**. The paper should predict "persists", not "intensifies", unless it adds a mechanism that would raise investment.
4. **The cleanest observable is where exits come from.** Under human capital, exits are spread across incomes because low-ability children in rich households also leave: about half come from the bottom 40%. Under the relational floor, exits come almost entirely from below the liquidity line: a median of 94%. This is the paper's footnote 23 test, quantified. With FIES linked to school data, a share near 50% favours human capital; a share above 85% favours the floor.
5. **Rerouting does not discriminate.** All structures reroute about 60% of Q3+ exiters.
6. **The model does not reproduce the Trillanes gradient in percentage points.** The K-12 cost cut completion slightly and about evenly across quintiles. A widening gap at the bottom would need cost shocks concentrated on constrained households, such as transport to distant senior high schools. That is a testable addition, not a confirmation.

## Limits

- Stylised units.
- One credential decision per child, not grade-by-grade survival.
- The relational structure is accepted rarely (25 draws), so its bands are wide.
- The ability–income correlation is fixed at 0.3. Prediction 4 depends on it: a higher correlation pushes human-capital exits toward the poor too.

## Data to run the real test

- **PSA FIES 2023**, merged with **APIS** school attendance by age: the share of 16–17-year-old leavers by income quintile.
- The **relative** senior-high premium from the **LFS** wage data, 2016–2024.
