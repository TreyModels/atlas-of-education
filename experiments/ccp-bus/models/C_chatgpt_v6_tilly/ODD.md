# V6 Tilly extension: model definition

18 November 2026. Overview, Design concepts and Details, with design rationale and evaluation. Numerical behavior is specified in `model.py`, `tilly.py`, `observation.py` and `evidence.py`; the executed manifest stores their hashes.

## Purpose and scope

The question is whether resource access, recurring obligations and organizational routines can generate misconduct among initially clean appointees despite enforcement. The intended use is explanatory experimentation. Calendar years identify experimental timing and input vintages. Post-observation years are scenario labels.

The model operationalizes selected ideas associated with Charles Tilly: opportunity hoarding through access boundaries, appropriation of controlled resources, emulation of organizational routines, adaptation to repeated dependencies and the exchange of protection. These are model-specific interpretations. It does not reproduce the full theory of categorical inequality, European state formation, or an empirically estimated CCP hierarchy. Insider status is an office-specific supplier relationship; historically grounded social categories and coercive state formation are outside its scope.

The intervention places a synthetic clean outsider in every organizational head seat in 2013. No historical individual is represented. All regimes except `no_replacement` receive the same appointment shock, allowing comparisons conditional on replacement. `campaign` versus `no_replacement` estimates the total shock effect inside this model under otherwise identical policy rules.

## Entities and scales

The default population is 50,000: 40,000 official seats and 10,000 supplier agents. Sixty-four organizations each hold 625 seats in five ranks: 1, 3, 12, 64 and 545 seats. Reporting parents have a more senior rank and remain properties of seats. Individual identities move through promotions. New entrants receive unique identifiers. None of these counts has been fitted to actual party, state or PLA staffing.

Person-bound variables include integrity, competence, loyalty, tenure, misconduct, output, perceived detection, financial receipts, favor obligations, creditor identity, protection-provider identity and delivered promotion support. Each debtor can have one outstanding creditor. The creditor is a person ID; departure extinguishes unpaid obligations through a recorded write-off. A promoted creditor retains the same identity. Provider exit clears exchange protection. Cycles in favor obligations are possible after changes in roles; payments occur in one pass using only a debtor's own current diversion, preventing recirculating funds within the step.

Officials have four weighted directed contact slots with hidden flags. Contact rows travel with a surviving person, destinations are remapped to surviving identities, and separate office inheritance can retain contacts when incumbents change. Duplicate contact destinations are possible; self contacts are removed. Patron links form a separate graph and always point to a senior rank. A reserved supplier-index field named `broker` remains behaviorally inactive from the earlier version; explicit intermediary agents are outside this implementation.

Every official makes one normalized discretionary supplier allocation per step. This represents an opportunity to control a resource, rather than a literal procurement contract census. Firms have fixed cost, quality and integrity. Their repeated relationships with offices evolve. Office-bound supplier identity and relationship strength survive an ordinary appointment replacement. The `network_reset` intervention also resets supplier identity, accumulated supplier ties and organizational routines.

Organizations have a closure level between zero and one. An incumbent supplier defines insider status for that office. Closure sometimes excludes the other sampled suppliers. A closed award can be entirely legitimate; corrupt diversion requires a participating official and an offered bribe from the winning firm.

## Resource assignment and accounting

Seat weights are 9, 7, 5, 3 and 1 from most to least senior rank. They are normalized within each organization, so the mean official controls one normalized unit before the sector driver. The organization's allocation equals its official population times its normalized economic-flow factor. The equal-resource arm assigns weight one at every rank and equalizes the political-signal resource weights too. It preserves unequal numbers of subordinates and other rank differences.

Allocation is partitioned between public delivery and diversion. The default diversion share on a corrupt allocation is 0.25. At most the settlement fraction of the debtor's own diverted receipts can repay an obligation illicitly. The creditor must also participate in misconduct in that step. Payments redistribute the diverted pool; their sum cannot exceed diversion. Net private receipts equal initial diversion in aggregate. Public budget accounting and obligation-value accounting are separate ledgers.

Obligations use normalized favor-value units, with an explicit assumed conversion to the resource units available for repayment. Assistance creates value owed; competent lawful service can discharge it. Creation, lawful discharge, illicit discharge, policy/departure write-offs and closing value reconcile to opening value. Appointment shocks report extraordinary write-offs separately before the ordinary annual ledger begins.

## Appointment cohort

At the opening of 2013, one new person replaces each head incumbent. Their integrity is 2.2 by default, competence 0.8, loyalty 0.9 and tenure zero. They have no modeled pre-appointment misconduct or personal obligations. Their individual trust strength is reset and links to the departed incumbent are severed. Their offices retain supplier relationships and surrounding organizational routines unless the organizational-reset arm is selected.

Cohort membership is an immutable dictionary keyed by the new person ID. Successors never inherit membership. Records retain first misconduct, first true/false filing, first true/false sanction, first creditor exposure, first obligation owed, retirement and employment removal. True-case and false-case removals refer to the misconduct act associated with a filing, rather than a person's full history. Pending cases can resolve after retirement.

Annual overall exposure includes every current cohort member. The first-act risk set includes current members who had never acted at step opening. Conditional rates are undefined for an empty risk set. Ten-, twenty- and thirty-year cumulative event fractions retain every original appointee in the denominator, including a person who retires while clean. Because every cohort member is observed until the fixed horizon or a recorded competing departure, these fractions describe the closed synthetic cohort without silently dropping retirees. Raw event histories support alternative estimands.

## Scheduling

Each annual step performs these operations in sequence:

1. Apply the appointment shock when due, then draw fixed-size process-specific random opportunities.
2. Smooth center effort using previous reports and aggregate output. Read sector opportunity factors; compute visible political-network signals.
3. Allocate discretionary resources. Generate requests for implementation assistance. With probability 0.75 an eligible official approaches the reporting parent; otherwise a contact is approached. Heads approach contacts. Delivery depends on the provider's competence. Eligible assistance creates a favor obligation; lawful service discharges part of it.
4. Draw misconduct and calculate effort, supplier allocation, diversion and public output.
5. Generate complaints and internal reporting loss. Rank investigation targets using reported complaints, noisy performance, visible patron groups and the modeled leadership's loyalty protection. Hidden exchange shields do not enter the targeting score.
6. Acquire evidence after targeting, file true/false cases, resolve sufficiently old cases and identify sanctions and employment exits.
7. Update trust and contacts. Settle eligible corrupt obligations from actual diversion, supply protection for future periods and update organizational closure.
8. Record cohort events and aggregate activity before personnel turnover. Execute exits and retirement, promote identities and fill vacancies. Remap person-bound state and write off obligations involving departed counterparties.

Recorded annual activity precedes turnover; recorded career events occur at the end of the same step. Assistance exposure and creditor ties are captured before lawful discharge, so a relationship fulfilled in the same year remains an observed exposure.

## Decision rules and information

Misconduct is a logistic response to rent opportunity, sector opportunity, land-related pressure, integrity, trusted peers, expected sanctions and concealment costs. The extension adds:

`obligation_pressure × debt/(0.5 + debt) + resource_attraction × log(relative_control) + request_pressure × log(1 + incoming assistance)`.

These coefficients impose responses to incentives. Their positive effects under positive settings are conditional model implications. Request pressure varies from -0.4 to +0.6, and resource attraction from -0.2 to +0.8. Separate zero-attraction and equal-resource arms test different imposed pathways. Integrity does not guarantee permanent abstention, and the baseline logistic rule can produce misconduct without the new mechanisms. Thus eventual misconduct alone cannot establish the Tilly explanation or universal corruption.

Effort and public output depend on competence and productive patron support. Misconduct reduces output. The earlier kernel also permits political risk to discourage visible client appointments. Promotion scores use competence, lagged output, loyalty, familiarity and noise. The new payment-support term applies only when the candidate paid the actual, still-present appointing superior. The `payment_blind` arm removes this additional term; other patronage and loyalty channels remain.

Assistance requests are exogenous opportunities whose delivery creates favor obligations. This extension does not estimate task-specific benefits or labor costs from obtaining that help. Productive patronage remains in the earlier output channel. Consequently, the low-demand arm is a mechanism experiment rather than an estimated policy benefit from reducing legitimate coordination.

Trust strengthens after joint misconduct and otherwise decays. Weak contacts can rewire toward corrupt or competent people. This assumes local knowledge of misconduct in prospective contacts; it is a substantive information assumption. The center has no access to latent misconduct or hidden patron links when selecting targets. Investigation evidence can reveal an act after selection. Aggregate output is treated as publicly observable.

Protection from an actual illicit settlement affects subsequent reporting and evidence sensitivity. It is tied to a provider identity and expires when that provider leaves. Payment does not guarantee immunity. The model does not simulate independent local coercive organizations or a full political market in disciplinary authority.

## Adaptation and emulation

Adaptation smooths organizational closure toward a logistic function of request load, the closure-response coefficient and the preceding routine. Emulation compares a sampled peer organization's observable public output minus twice its filed-case rate per official. An organization can copy the preceding closure routine of a better-scoring peer. Filed cases can be true or false, as in the observation process; the imitation rule receives the observable filing rate. The new routine affects the next step.

The adaptation function has a positive baseline target even at zero request load. Initial closure is also positive. Persistence or reappearance of closure therefore follows partly from imposed baseline propensities. These experiments assess differences across interventions and coefficients; the mere existence of rebuilt closure is insufficient evidence for a dependency-driven explanation.

Imitation can copy productive arrangements or reproduce exclusion. Legal assistance and closure do not automatically enter the misconduct variable. This distinction allows competent, clean cooperation and successful enforcement as possible outcomes. The experiments quantify the consequences of the specified update rules rather than proving Tilly's general theory.

## Initialization and external inputs

Initial integrity is Normal(0.6, 0.7); competence is a clipped Normal(0.65, 0.18); loyalty is Beta(2,2). Initial misconduct probability is 0.25 and eligible patron links occur with probability 0.7. Initial organizational closure is Uniform(0.1,0.3). Initial favor balances and exchange protection are zero. Thirty burn-in steps under the 1998 regime precede 45 recorded steps labeled 1998–2042.

The evidence panel contains 65 official annual observations, 10 monitoring/budget records and 343 selected procurement notices. Land proceeds and incremental lending are normalized to the first verified observation. Prior years use a normalized assumption of one; factors remain flat after the last observation. The defense driver uses a 2026 central budget relative to its 2025 execution comparator. It is an opportunity scenario input, rather than observed procurement expenditure. Year-to-date flows never substitute for full-year execution. CSET notices provide a selected procurement sample without corruption labels.

## Experimental design and reproducibility

The 828-run design comprises 540 runs crossing twelve stratified parameter settings, three seeds and fifteen regimes; 120 reference runs with eight seeds; 112 Morris runs; 24 integrity-anchor runs; 24 scale runs; and eight initialization runs. Parameter ranges remain assumptions, with no posterior distribution or empirical frequency interpretation. The default cohort size is 64 per run. Scale checks retain the number of organizations and senior seats, changing rank proportions and therefore constituting structural sensitivity checks.

The Morris screen has thirteen factors, four trajectories, six grid levels, a normalized step of 0.6 and two seeds per point. Discrete cohort endpoints introduce noise into elementary effects. Paired seed differences and their MCSE are reported separately from quantiles across parameter settings. Small effects require greater replication. No empirical confidence interval is inferred from these quantities.

Independent random streams separate process families; new draws use fixed-size arrays. The organizational-reset supplier draw uses a separate keyed function to avoid shifting unrelated streams. Jobs save complete configurations, annual rows and cohort event records. Source/data hashes and the Python/NumPy/pandas environment bind reusable results to the same design. Atomic job files allow interruption and restart at the job boundary.

## Evaluation and limits

Implementation checks cover identity, budgets, obligation balances, corrupt settlement conditions, cohort clocks, competing exits, hidden-state exclusion and controlled mechanism switches. The requested gpt-6.1-terra agent reviewed the design and implementation; its findings and fixes are recorded in PEER_REVIEW.md. That review provides implementation scrutiny, without empirical validation.

Historical evaluation requires a dated cohort of documented appointments, positions at risk, conduct-specific allegations or findings, and observation/censoring rules. Changes in disciplinary jurisdiction and investigative capacity must be modeled before fitting national case counts. The existing evidence register is retained with those limitations. A later fitting exercise should define estimands and holdouts, check synthetic parameter recovery and distinguish identification failures from Monte Carlo error.

## References

- Tilly (1998), [Durable Inequality](https://www.ucpress.edu/books/durable-inequality/paper).
- Tilly (2003), [Changing Forms of Inequality](https://journals.sagepub.com/doi/10.1111/1467-9558.00173), author abstract and publisher record.
- Tilly (2005), [Trust and Rule](https://www.cambridge.org/core/books/trust-and-rule/DFDAC1971F4054E6183BE99EB94670FA).
- Tilly (1985), [War Making and State Making as Organized Crime](https://www.bmartin.cc/pubs/19sd/refs/Tilly1985.pdf).
- Grimm et al. (2020), [ODD second update](https://www.jasss.org/23/2/7.html).
- Edmonds et al. (2019), [Different Modelling Purposes](https://jasss.org/22/3/6.html).
- ten Broeke et al. (2016), [Sensitivity analysis for ABMs](https://jasss.org/19/1/5.html).
