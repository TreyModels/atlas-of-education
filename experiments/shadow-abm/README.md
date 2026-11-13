# Shadow-education ABM: review reruns (14 Nov 2026)

Code: `src/tutoring_abm/` (updated) and `src/fresh_tutoring/` (unchanged). Old outputs are in `src/tutoring_abm/results_v1/`, new ones in `results/`. ODD protocol: `src/tutoring_abm/ODD.md`, written from the code.

| Review item | Change | Result |
|---|---|---|
| 3.1 One calibration world | Each parameter set is scored on 10 worlds; distance = 7th-smallest per-world max-z, so a set must fit about 7 of 10 | On 20 fresh worlds per particle (new seeds), the pair fit rate is **37–44%** (old posteriors on the same seeds: 17–19%). The share of particles fitting at least 70% of fresh worlds is only **1–7%** (old: 0–1%). |
| 3.2 Low ESS in favour | ABC-SMC with resampling and 3 Metropolis moves per generation | Favour final importance ESS **121 of 200** (old 71 of 400). The other variants end at 37–99 of 200. The final tolerance reached is 1.0–1.07; at ε = 1, 0–4% of proposals fit. |
| 3.3 Agreement from shared code | Code overlap measured; shared components ablated | The variants share one `model.py`; only 6 of about 215 lines and 2 of 15 priors differ. Removing the thin-market channel or alternative providers shifts every variant's policy effects together (ban effect on participation −0.35 → −0.51 without alternative providers), and the fit collapses. Changing the diversion-specific withholding cost or convexity changes nothing. **The policy agreement comes from shared code and is not independent evidence.** |
| 3.4 Dropout and household work | `dropout_channel` flag (default off) | Sensitivity only; not calibrated. Flag off reproduces the original outputs on 1,240 values. |
| 3.5 ODD | `ODD.md` | Written. Not externally reviewed. |

**Evidence at ε = 1** (10 worlds per set, 2,000 proposals): thin 2.5e-7 [4e-8, 5e-7], full 7.9e-9, favour 2.1e-8, diversion 0. Thin fits most often, but every estimate rests on a handful of fitting proposals.

**Withholding** (fresh worlds): the median is 0% in every variant. Diversion settings withhold more than 1% in 21% of worlds (95th percentile 9%).

**Headlines.** "No single explanation can be crowned": still true; the evidence is too thin. "All surviving explanations point at the same policy levers": true, but only because the levers act through shared code. "Teachers withhold ~0%": true as a median, but not in every diversion setting.
