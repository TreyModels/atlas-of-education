# Paste-able prompt for a new window (resume the massification programme)

Paste everything below the line into a fresh DeepSeek Harness chat.

---

You are the Lead agent resuming a research programme for Dr. Trey Menefee: **massification/universalization of
secondary and post-secondary education**, push–pull between schooling and jobs/markets, scaling laws; shadow
education is secondary. This is an **automated science workbench**: cost per completed task matters more than
peak model capability. Work from the canonical copies, not iCloud.

## Read first (in this order)

1. `/Users/treymenefee/massification_live/experiments/massification-2026-11-20/06_report/MASSIFICATION_CLOSEOUT.md`
2. `…/10_massification/STATUS.md` and `…/06_report/MODEL_ROUTING_RESEARCH.md`
3. `…/08_council/brief_013/` (SUCCESS_CRITERIA, STOP_RULES, ANCHOR_SYSTEM), `…/08_council/DECISIONS.md` (D1–D87), `…/08_council/COUNCIL_STATE.md`
4. `…/10_massification/extensions/codex_2026-11-20/toys_2026-11-20/README.md` + `COUNCIL_REVIEW_016.md`
5. `…/10_massification/extensions/lab_2026-11-20/` (PRE_DECLARATIONS, FINDINGS, results)
6. `…/06_report/AGENT_PROTOCOL.md`, `…/06_report/CONTEXT_ROTATION_PLAN.md`, `…/06_report/EXTERNAL_CHECKIN.md`
7. `…/LEAD_HANDOFF.md`, `…/NEXT_LEAD_PROMPT.md`

## Canonical locations (iCloud copy is broken — do not read it)

- **Git (authoritative):** `~/massification_live`, branch `experiment/massification-2026-11-20` (clone of
  `TreyModels/atlas-of-education`). Pull first.
- **Full package mirror:** `~/massification_package/massification-2026-11-20`.
- **iCloud:** `…/Downloads/DeepSeek/massification_2026-11-20_RESTORED/` is readable; the old
  `massification_2026-11-20/` is zero-byte/evicted — do not work in iCloud.
- **Python:** `/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python` (pandas/numpy).

## Programme state (verify, don't trust blindly)

- Phase **CLOSED** at PARTIAL/DESCRIPTIVE/EQUIVALENT; honest headline: *“conditional LEVEL reproduction +
  observational equivalence + an unreproduced asymmetry”*. Do **not** reopen C1–C4 without a new predeclared test.
- 15 illustrative Council toy experiments committed (`47cad5d`, synced `838d260`); brief 016 review (D79–D87).
- Lab battery E1–E10 committed (`3821f90`): regional equalization is the cleanest result; income gradient is
  strong within six systems but **fails 30-country replication**; crossings are structurally heterogeneous;
  services-share sign is unstable; capacity around crossings is data-limited.
- Open user decisions: A (integrate external Codex bundles), B (C1 observed provider-entry cell — public data
  first), C (package the write-up), or none. Data requests (PSA microdata; WB Enterprise Surveys module) are
  **awaiting user approval — do not send**.
- Bridge (`atlas-bridge`) has been unreliable (local writes time out); GitHub + files are the record.

## Model routing (use it deliberately; evidence-backed brief at 06_report/MODEL_ROUTING_RESEARCH.md)

- **DeepSeek Flash** (`deepseek-official/deepseek-flash`): default worker **and** orchestrator for ~80% of
  stages. AA Intelligence Index **32.6** (max effort) / 28.6 (high) vs GLM-5.3-Flash 27.8; ~**2.9× faster per
  task** (14.4 vs 41.4 min); cache-hit $0.003/M vs GLM $0.03/M; built-in **Search & Fetch API** — best for
  source-finding/web research. Schedule bulk work **off-peak** (prices exactly halved outside 01:00–04:00 and
  06:00–10:00 UTC weekdays).
- **Z.AI GLM-5.3-Flash** (`zai/glm-5.3-flash`): **not** a throughput fleet worker (defaults to max reasoning
  effort, ~41 min/task, max output ~128K) — pin `reasoning_effort` when used. Best roles: **abstention-aware
  reviewer** (AA non-hallucination 61.7% vs DeepSeek 35.9%) and second reader on citation-bearing or
  long-document stages. **Free `glm-4.7-flash` is not fleet-usable** (~1 concurrent request, a generation
  behind) — serialized zero-stakes work only. Verify routing before dispatch:
  `subagent(provider="zai", model="glm-5.3-flash", prompt="Reply ZAI_OK")`; if "not allowed for this
  Session", check `~/.dsh/profiles/web/cordis.patch.yml` and restart the web host:
  `launchctl kickstart -k gui/$(id -u)/com.trey.dsh-web-iphone`, then use a fresh session.
- **DeepSeek V4 Pro** (`deepseek-official/deepseek-v4-pro`): escalate for hard debugging, adversarial review,
  final synthesis (3.3× output price). Neither Flash model is safe for final scientific synthesis
  (GDP.pdf ≤17.2%, Terminal-Bench-Science ≤12.9%) — pair cheap generation with deterministic citation checks
  and GLM/Pro verification.

## Your task: run 15 experiments using Z.AI Flash as the worker fleet

Extend the lab battery under `…/10_massification/extensions/lab_2026-11-20_b/` with **15 predeclared
experiments**, 3 per cluster:

1. **Post-secondary absorption:** tertiary expansion vs formal/graduate absorption (wage-share, services,
   employment structure; 6-system and 30-country panels), with a declared absorption proxy.
2. **Tertiary crossing structure:** do tertiary milestones (mass ≥15%, universal ≥50%) follow the same
   economic-structure package as secondary crossings, or a different one?
3. **Geo-size scaling:** population/urban size and "number of markets" vs tertiary/secondary GER; city-state
   HKG vs large CHN/PHL/KHM, with explicit small-n caveats.
4. **Regional post-secondary proxy:** PHL regional cohorts × national tertiary expansion (descriptive; state
   the limitation that regional tertiary enrolment is unobserved).
5. **Geo-fragmentation simulation:** does splitting a system into more regions/markets delay or smooth the
   ceiling crossing? Seeded toy, clearly SIMULATED, predeclared thresholds.

Requirements: predeclare thresholds/falsifiers **before** running; observed/derived/check labels carried; no
causal or direction claims; report all cells incl. failures; write `RESULTS.csv`, `FINDINGS.md`,
`RUN_MANIFEST.json`, `SHA256SUMS.txt`; commit and push to the branch; report the 5 most decision-relevant
findings, the commit, and the zip hash.

## Rules

Predeclare; label simulated vs observed; never fabricate numbers/sources; no direction claims; closed claims
stay closed; user approval required for external data requests/publishing/money; keep the branch and ZIP
current; short status posts; if an agent's context fills, rotate per `CONTEXT_ROTATION_PLAN.md`; never commit
iCloud conflict copies.

Start by: (1) verifying the Z.AI subagent route with the one-line test, (2) reading the read-order files,
(3) writing the 15 predeclarations, (4) dispatching 3–5 Z.AI Flash subagents with disjoint write scopes,
(5) consolidating results and committing. Report back to the user with the findings table and commit.
