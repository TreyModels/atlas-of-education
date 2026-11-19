# CCP bus: contents and provenance

Stored model versions for the politics family page (`src/data/ccp-journey.ts`). All agents are synthetic. Nothing here estimates the actual prevalence of corruption in China, identifies any real official as corrupt, or describes anyone’s personal motives.

## Contents

| Folder | Model | Key fact |
|---|---|---|
| `models/A_claude_v1_three_models` | v1: three rival families (current incentives, social trap, bus) | Only models with complementarities show hysteresis; the memoryless model never kept a campaign effect (0 of 96 runs). |
| `models/B_claude_v3_economy_factions` | v3: adds land revenue, credit, PLA procurement, four sectors, faction dynamics | Pattern-oriented ABC against CCDI cases plus six qualitative patterns; 17 accepted fits. Not tested out of sample. |
| `models/C_chatgpt_v6_tilly` | v6: 50,000 agents, 64 organisations, 5 ranks, Tilly-labelled mechanisms | Well engineered (14 passing checks, exact accounting). Uncalibrated (42 hand-set parameters); several mechanisms inert; little memory. |
| `models/D_chatgpt_v7_identification` | v7: the three rival families on the v6 kernel, fitted 2013–19, scored 2020–25 | A retrospective test, not a genuinely untouched holdout: the 2020–25 outcomes were already known when the model was designed. Bus and social trap indistinguishable (log RMSE 0.1898 vs 0.1896). All three miss the 2024–25 surge. |

`BRIEFING.md` is the review briefing. `data/` holds the top-level archived series; model D keeps its own local split files.

## Provenance

- Imported at commit `2e19f07` from the Atlas of Education repository.
- 287 files imported; 3 excluded papers.
- Code downloads for the family page: `research/ccp-bus/ccp-bus-v1.zip`, `ccp-bus-v3.zip`, `ccp-bus-v6.zip`, `ccp-bus-v7.zip`.
- Notes and source links use the immutable import commit `2e19f07` under `experiments/ccp-bus/models/`.

## What none of this claims

No output estimates the actual prevalence of corruption in China, identifies any real official as corrupt, or describes anyone’s personal motives. All agents are synthetic.
