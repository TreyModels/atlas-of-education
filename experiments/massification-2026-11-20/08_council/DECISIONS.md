# Council decision log — massification-first phase

**Owner:** Synthetic Council of Experts (authority for research direction while the user is away). Created by the
Lead as a proxy on 20 Nov 2026; the Council maintains it from here. Append new decisions at the top of §"Decisions".

## Decisions

| # | date/time | decision | rationale | owner / next |
|---|---|---|---|---|
| D1 | 2026-11-20 14:10 | **Governance:** Council of Experts is the authority for research direction; Lead executes/coordinates; Lead veto only on fabrication, closed-claim reopening, site safety, external actions needing user approval | user away; direction owned by the adversarial body, execution by a single accountable executor | Council |
| D2 | 2026-11-20 14:10 | **Protocol:** `06_report/AGENT_PROTOCOL.md` live — workers post `NEW:` (path, key number, hash, what it changes); consuming parties post `ACK:`; Council posts `COUNCIL:`; Lead posts `OP:`; no artifact counts until ACKed; `STOP:`/`ASK:` for escalations | makes the bridge the research board and prevents silent artifacts | all agents |
| D3 | 2026-11-20 14:10 | **Reorientation:** first-order question is massification/universalization + schooling-jobs push-pull + scaling; **shadow education demoted to secondary**; the shadow close-out (`LOOP_CLOSEOUT.md`, brief 008) remains valid and is not re-fit | user request; new question on the same evidence base | all agents |
| D4 | 2026-11-20 14:12 | **Gate:** task-37 (model + calibration) may not fit until Council brief 013 states the operational definition of "reproducing universalization" (series, countries/sectors, tolerance, holdout) and stop rules | prevents fit-first re-parameterisation (the failure mode of the previous phase) | Council; model runner |
| D5 | 2026-11-20 14:12 | **First-order workstreams assigned:** task-34 data-hunter (`10_massification/data/`), task-35 lit-archivist (`lit/`), task-36 pattern-scout (`relations/`), task-37 experiment-runner (`model/`), task-38 experiment-runner-2 (`model2/`), task-39 Council (`08_council/brief_013/`) | disjoint scopes; theory+data before empirics before model | Lead assigned; agents to ACK |
| D6 | 2026-11-20 14:12 | **Design gate REGISTERED:** `brief_013/SUCCESS_CRITERIA.md` (operational definition: series, roles, tolerances, holdout; PASS/PARTIAL/FAIL/EQUIVALENT) + `brief_013/STOP_RULES.md` (R1–R12) declared before fitting. **task-37 and task-38 cleared to fit under these terms** | the previous phase failed by fitting before defining success; gate prevents fit-first re-parameterisation | Council; deepseek-exp1/exp2 must ACK and copy §2–§4 into their predeclaration |
| D7 | 2026-11-20 14:12 | **Intake (provisional, NEW/ACK loop):** `10_massification/relations/data/universalization_fits.csv` (logistic/Gompertz fits, PHL/CHN etc.; e.g. PHL GER-secondary holdout RMSE 5.98, mape 5.5) and `universalization_common_shape.csv` (secondary/tertiary country-specific slopes REJECT common shape, p≤0.0024/0.0; upper-secondary and NER primary not rejected) — on disk, no `NEW:` post seen yet → provisional until ACKed | scaling section needs the empirical shape evidence | exp2/scout to post `NEW:` with hash; runners to ACK |
| D8 | 2026-11-20 14:12 | **Next:** Council posts the full brief-013 design review + ranked 8-experiment slate (task ids/owners/deadlines/falsifiers) via `COUNCIL:`; intake cycles every ~10–15 min on `NEW:` batches | user away; fleet needs direction | Council |

## Open questions for the Council

- Operational definition of universalization success (D4) — pending brief 013 preliminary section.
- Whether any shadow-education work continues in parallel (default: frozen unless the Council reopens it with a
  predeclared test).
- Data-first external requests: drafted and held (`06_report/access_requests/`); user approval required.
