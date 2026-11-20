# External check-in — for Claude, Opus, or any other harness

Everything for this programme is on GitHub so another model can check in while the user is away.

## Where to look

- **Repo:** `https://github.com/TreyModels/atlas-of-education`
- **Branch:** `experiment/massification-2026-11-20` (never `main`)
- **Folder:** `experiments/massification-2026-11-20/`
- **Local mirror:** `/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20`
- **Bridge:** local append-only board at `DeepSeek/atlas-bridge/messages.jsonl`, CLI `DeepSeek/bridge-agent.sh`

## Read order (short)

1. `10_massification/README.md` — the **current first-order question** (massification/universalization,
   push–pull between schooling, government and markets, scaling laws; shadow education secondary).
2. `06_report/AGENT_PROTOCOL.md` — bridge grammar and authority (`NEW:`/`ACK:`/`COUNCIL:`/`OP:`/`ASK:`/`STOP:`).
3. `08_council/BIG_PICTURE_RULE.md` — the step-back the Council must do every cycle.
4. `08_council/brief_013/` — the Council's success criteria, stop rules and ranked slate (the current gate).
5. `LEAD_HANDOFF.md` + `LOOP_CLOSEOUT.md` — programme history and the **closed** shadow-education claims
   (do not reopen without a new predeclared test).
6. `10_massification/STATUS.md` — live task/artifact state.

## Rules you inherit

- Results only in `experiments/massification-2026-11-20/` on the branch; never `main`, `src/`, `public/`,
  `package.json`, `vite.config.ts`, `index.html`.
- Predeclare before running; label simulated vs observed; stored ≠ rerun; never fabricate; imputed cells are
  never observations; synthetic output labelled SYNTHETIC; no validation language for synthetic matches.
- External data requests, publishing, or spending need the user's approval.
- Council is the research authority; the executor coordinates; the op centre monitors.

## How to check in

- Read the branch and the bridge list. Post a `CHECKIN:` message with your party slug
  (`ATLAS_PARTY=claude` or `ATLAS_PARTY=opus`): what you read, one substantive question or finding, and
  whether you think the programme is on the big picture or in a niche.
- If you review results, use the Council's step-back vocabulary: is this on the critical path to a model of
  massification, or should it be killed/parked?
- Do not push to `main` and do not rewrite files others own without an `ASK:`.
