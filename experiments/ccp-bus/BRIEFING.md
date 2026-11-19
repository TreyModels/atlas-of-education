# The bus model: briefing for review (19 November 2026)

James W. Menefee III. Models built with Claude (Anthropic) and ChatGPT (OpenAI), 17–19 November 2026.

## The question

*The Priest and the Bandit* argues that CCP corruption is the payroll of a clergy, not deviance, and that
anti-corruption campaigns discipline the clergy without dismantling the benefice system. The "bus" is the
mechanism: entry by sponsorship creates obligations and shared exposure that keep corruption going after
enforcement changes. **In modelling terms, the claim is path dependence**: inherited networks should keep
corruption high, or bring it back, after a campaign. A model in which this year's incentives fully determine
this year's corruption assumes the claim is false.

## What exists

| Folder | Model | Key fact |
|---|---|---|
| `models/A_claude_v1_three_models` | Three small rival models (current incentives, social trap, bus) set to the same 30% snapshot | Only models with complementarities (finite investigators, peer reporting) show hysteresis; the memoryless model never kept a campaign effect (0 of 96 runs). |
| `models/B_claude_v3_economy_factions` | Adds land revenue, credit, PLA procurement, four sectors, faction dynamics (patron protection, encirclement, hiding, bandwagoning, succession) | Pattern-oriented ABC against CCDI cases plus 6 qualitative patterns; 17 accepted fits; faction status predicts removal about as well as corruption (AUC 0.67 vs 0.66). Not tested out of sample. |
| `models/C_chatgpt_v6_tilly` | 50,000 agents, 64 organisations, 5 ranks, Tilly-labelled mechanisms | Well engineered (14 passing checks, exact accounting). Uncalibrated (42 hand-set parameters); several mechanisms inert; little memory. |
| `models/D_chatgpt_v7_identification` | The three rival families on the v6 kernel, fitted to 2013–19 cases, scored on 2020–25 | The first genuine holdout test. See below. |

## What v7 shows (the most rigorous result so far)

Fitted on 2013–2019 discipline filings only, then asked to forecast 2020–2025:

| | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|---:|---:|
| Actual cases filed (thousands) | 618 | 631 | 596 | 626 | 877 | 1,012 |
| Current incentives (50k agents) | 708 | 722 | 745 | 732 | 750 | 745 |
| Social trap | 649 | 672 | 687 | 685 | 697 | 707 |
| Bus | 647 | 672 | 689 | 686 | 695 | 709 |

- **All three miss the 2024–25 surge**, and beat a "last value" forecast (log RMSE 0.19 vs 0.25) mainly
  because last-value misses it by even more.
- **Bus and social trap are indistinguishable** (0.1898 vs 0.1896). At the fitted settings the extra bus
  mechanisms do nothing for case counts.
- **The memory test finds no lasting memory**: runs started at 5% and 95% misconduct converge within 10 years.
- **Seven training points cannot identify the parameters.** Fitted values swing widely (rent −0.67 to 0.84,
  peer effect 0.17 to 4.0) with near-identical fit.

**Honest bottom line:** national case counts cannot tell the bus apart from simpler mechanisms. The model is a
coherent, testable theory instrument, not yet evidence for the bus.

## On building an expansive model

The worry that a full political-economy model breaks computational-sociology norms is real but answerable.
"Keep it simple" (Axelrod) and "keep it descriptive" (Edmonds & Moss, *From KISS to KIDS*, 2005) are both
recognised strategies. The rule shared by both is that **each added mechanism must earn its place against a
pattern in data** (Grimm et al. 2005, pattern-oriented modelling). v7 shows the bus mechanisms have not yet
earned theirs on case counts. The defensible design is a modular "model of models" (Page, *The Model
Thinker*): a broad framework whose pieces switch on and off, each tested against the data it bears on.

## Experiments still worth running (in order)

1. **Forecast 2026 now, before the January 2027 CCDI report.** January–September 2026 already shows about
   800,000 cases (`data/monitoring_2026.csv`). A frozen forecast scored in January is the first untouched test.
2. **The provincial land-collapse test.** Land revenue fell much more in some provinces. The v3 model predicts
   predatory fines and fees rose most where land fell most. Provincial fiscal reports can confirm or kill this.
3. **Individual-level faction test.** Use appointment and patron histories (ccporg.org tracker; the Chinese
   Political Elite Database) with co-defendant links in CCDI case reports: does faction predict investigation
   once corruption evidence is accounted for?
4. **v7's outstanding memory tests** (head replacement, full network reset), which its own spec lists as not run.
5. **Explain 2024–25.** Test whether the 2024 disciplinary-regulation revision and the campaign on misconduct
   "around the masses" account for the surge, labelled as a conditional, after-the-fact analysis.
6. **Reduce to the identifiable core**: profile which parameters the data constrain and drop the rest.

## What none of this claims

No output estimates the actual prevalence of corruption in China, identifies any real official as corrupt,
or describes anyone's personal motives. All agents are synthetic.
