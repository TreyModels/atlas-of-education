# Changelog — Massification research package

All dates 2026 (Asia/Shanghai). This is the programme-level log; per-cell run records live in the experiment
manifests and error logs.

## 2026-11-20 (final) — PHASE CLOSEOUT COMMITTED; iCloud worktree retired as active checkout

- `06_report/MASSIFICATION_CLOSEOUT.md` committed as the phase's authoritative summary; pointers added to
  `LEAD_HANDOFF.md`, `NEXT_LEAD_PROMPT.md`, `06_report/EXTERNAL_CHECKIN.md` read order.
- iCloud worktree **retired as an active checkout** (canonical = GitHub branch; stable-root clone for checkpoints;
  iCloud package = read-only mirror with only the ZIP pair written back). Recorded rationale: iCloud file-loss incident.
- Final commit/ZIP hashes in the `OP: checkpoint … — phase closeout committed` bridge post; SHA256SUMS verified in
  `/tmp`, conflict scan 0. Data asks HELD; nothing external sent.

## 2026-11-20 (night, recovery) — DELIVERY INCIDENT + RECOVERY CHECKPOINT (outside iCloud)

- **Incident:** during the anchor-closure checkpoint the iCloud-synced package lost files mid-operation (directories
  emptied, truncated reads, git index timeouts). A checkpoint built against the incomplete stage (`fabe4cf`) deleted
  282 tracked files; it was pushed then **reverted on the remote by force-push to the last good commit `3e3f705`**
  (authoritative). No pre-`3e3f705` history was rewritten.
- **Recovery:** checkpoint rebuilt entirely in `/tmp` from the pre-incident ZIP extraction
  (`/tmp/massif_recover`, 1,184 files) overlaid with the uncommitted post-`3e3f705` content
  (`/tmp/massif_new_checkpoint`, 19 files); manifest/stage/SHA256SUMS/commit/ZIP built there; only the `.zip` +
  `.sha256` copied back to the iCloud package. Branch tip and ZIP hash are announced in the `OP:` checkpoint post.
- **Content now included:** Council-2 intake (D66–D78; D71–D78 bind), A1 addendum C1–C10 (C8 primary-2017 reporting
  gap; M4 not discriminable; constant back-fill + de jure enforcement disclosed; G(C)=C^0.75 text fix; M1 ≤1977;
  corrected accounting), A2d model-internal descriptive-negative, A6/A7 portability design notes (PARKED-ARMED),
  phase write-up shell with provenance block, closure STATUS §3q/§3r.
- **Provenance resolved:** linear-trend 4.35 / persistence 8.60 from `model/calib/calibration_table.csv`
  sha256-16 552e0cce04bd148d; repair fit 6.16–7.43 from `model/calib/repair_table.csv` sha256-16 34b0a5bc98e3d603.
- **Standing recommendations:** keep the iCloud package read-only until a reconciliation pass; use a stable-root copy
  (e.g. `/tmp/massif_work` or `~/massif_work`, cloned from GitHub) for future checkpoints and mirror to iCloud only at
  delivery boundaries. Data queue HELD; nothing external sent.

## 2026-11-20 (night) — ANCHOR CELL CLOSED; COUNCIL ROTATED TO COUNCIL-2

- **Council rotation executed** (context-rotation plan): expert-council → **council-2** (fresh-context subagent, party
  `deepseek-council2`); handoff `08_council/COUNCIL_STATE.md` + `10_massification/HANDOFF_expert-council.md`; authority
  persists via files; D66–D70 (first pass) kept and **D71–D78 bind**; old Council stood down.
- **PHL anchor cell CLOSED at PARTIAL/DESCRIPTIVE/EQUIVALENT (D76)**: A1 descriptive report (`model/anchor_out/`) =
  milestone timing miss (M2 2024 not reproduced in 9/12 arms; M4 = 1960 initialisation artefact/not discriminable;
  M3 non-crossing passes in-window but 2/12 arms overshoot after 2024), **A6 asymmetry unreproduced 0/3**, capacity-gated
  ties law-only → capacity-timing not supported (EQUIVALENT), A2d model-internal descriptive-negative (−0.427 lag 6),
  scaling criterion FAIL standing. Remaining PHL work = **A1 addendum C1–C10 + write-up**; re-openers C1–C4 only.
- **Phase headline (exact): "conditional level reproduction + observational equivalence + an unreproduced asymmetry"**;
  "reproduces universalization"/"capacity explains timing"/"portability holds"/direction words barred.
- **Capacity data reconciled**: three dimensions canonical (data-hunter), scout composite DERIVED only; tax/GDP provenance
  resolved; WGI blocked → 0.85; de jure ≠ de facto; BEPER DATA BLOCKED; asks held.
- **Publishable objects**: bounded negative on income-scaling (model class cannot generate positive income-scaling sign
  without exogenous supply channel, R27) + equivalence/identification map with the unreproduced asymmetry (D58); write-up
  shell assigned to lit-archivist.

## 2026-11-20 (late) — SINGLE-SYSTEM PIVOT + TIMING REGIME (A4)

- **User design pivot (logged):** (1) single-system first — stand up ONE education system (best data, actually
  massifies), show the mechanisms, then test portability to Hong Kong and China; (2) mechanisms to test, especially
  **state pushes** — compulsory-education-law changes, school/place expansion (construction, teacher supply,
  pupil-teacher ratios), fee abolition — against **demand-pull** (jobs/returns) and **supply-push** (cohorts);
  (3) researchers do **web searches** (UNESCO, World Bank, national sources) for baseline data on synthetic-fitting
  questions; (4) **test different researchers' models on the same system record**. Keeps the Council gate/acceptance
  rules and the Japan timing directive (A4/R19).
- **Board restructure:** task-37 becomes the **anchor-system model** (mechanisms + calibration) with a **portability
  checkpoint to HKG/CHN**; data-hunter gets the web-search baseline-data task; lit-archivist the UNESCO/WB + rival-model
  narrative; scout prepares **event windows** for compulsory-law/expansion/fee dates. The Council is asked to **name
  the anchor system and the single-system success criteria before the runner fits** (provisional candidate:
  Philippines — best observed coverage on disk, actually massified, dated state pushes 2013 K-12 / 2018 free tuition /
  4Ps; alternatives Korea, China).
- **Council Amendment A4 (timing regime) adopted:** milestones M0 massification ≥50%, M1 primary NER≥95 (or GER≥100),
  M2 lower-sec completion ≥90, M3 upper-sec completion/transition ≥90, M4 tertiary GER ≥50; crossing year = first
  observed year at/above threshold, band = adjacent observed years; **N = ±5 y (±3 y where band ≤2 y)**; JPN/KOR/HKG
  levels CHECK-ONLY ±5 pp; crossing years are HOLDOUT outcomes, **never fitted** (R4/R5; R19 timing miss = structural
  miss); left-censored = boundary constraint, right-censored = false-positive test. Censored ratios reconstruct only
  from observed headcounts + documented population denominators, labelled **"reconstructed (not UIS)"**, with
  method/uncertainty + two-denominator sensitivity. Slate re-rank: **E6 timing comparison #2; E9 crossing-year
  reconstruction #3**; E4 #4; E2 #5; E1 #6 parked/unfielded; E3 #7 DATA BLOCKED; E5 #8; E7 #9; E8 KILL.
- **Loop-5 adjudication (D19–D30):** phase headline = **conditional reproduction + observational equivalence**; E1
  killed as the identification gate as specified (redesigned/sign-only options defined, parked); A1 scaling capped
  PARTIAL; income-scaling repair accepted for intake, timeboxed one cell/cycle; E2 accepted with claim cap/MDE;
  E3 DATA BLOCKED; M2c retro-accepted; M2b estimator range; data D16 accepted; E4 elevated to KEEP.
- **Timing artifacts landed:** scout crossing-year reconstruction (`relations/data/UNIVERSALIZATION_TIMING.csv`,
  pattern, E6 timing comparison) and exp1 timing-check predeclaration for JPN/KOR/HKG (not run, DATA BLOCKED pending
  crossing-year series); data-hunter asked for `UNIVERSALIZATION_TIMING.csv` (crossing years + intervals).

## 2026-11-20 (evening) — FIRST-ORDER PHASE: massification/universalization + schooling-jobs push-pull

- **Reorientation (user request):** the first-order question is now massification/universalization of schooling
  across countries and sectors, and the push-pull dynamics between schooling and jobs/markets; shadow education is
  demoted to secondary. The previous phase's close-out remains valid for shadow education and is not re-fit.
- **New scope:** `10_massification/` with disjoint workstreams — `data/` (jobs/markets panel, ILO/OECD corpus,
  universalization series), `lit/` (massification theory, push-pull rivals, scaling laws), `relations/`
  (universalization curves, scaling exponents, lead-lag tests), `model/` (cohort-flow push-pull model),
  `model2/` (independent scaling + rival recovery/identification), Council brief 013 (design gate).
- **Governance:** Council of Experts is authority for research direction; Lead executes and enforces the bridge
  protocol. `06_report/AGENT_PROTOCOL.md` live (`NEW:`/`ACK:`/`COUNCIL:`/`OP:`/`STOP:`/`ASK:` grammar).
  `08_council/DECISIONS.md` created (D1–D5).
- **Gate:** task-37 (model calibration) blocked until brief 013 defines "reproducing universalization" operationally
  and the stop rules (D4).
- **Follow-on from the shadow phase (same day, closed):** T1 Korea decomposition amended (M1 resolved: KEDI hours
  are per all students; one-margin arms-race participation description withdrawn; price escalation not established);
  loop 8 + loop 8b synthetic frontier (relations/ECI wired; empty support persists for the KOR gradient; HKG
  0→2/256 only); C access requests drafted and held.

## 2026-11-20 (afternoon) — shadow-education phase closed

- 40+ predeclared cells across iterations 1–8; reproduction audit (5/7 headline results reproduced); literature
  ledger (20 core sources, 68-claim register); six country cards; shadow target register (21 rows); WDI/UIS/national
  data layer with documented-imputation panel; economic-complexity panel (ECI); ranked-relation register (49 rows);
  synthetic assumption-space analysis (empty support); Council briefs 001–012.
- **Final adjudication:** five claim classes excluded by predeclared tests (gate architecture, provider technology as
  missing channel, cross-country shadow incidence, mechanism classification, country completion forecasting);
  8/9 stop rules fired; cohort conservation passed exactly. Publishable objects: negative/identification map,
  measurement programme, Korean provider/fee descriptive note.

## 2026-11-20 (evening) — synthetic workbench v1, longitudinal battery, external literature review

- **Synthetic workbench packaged** (`10_massification/extensions/synthetic_2026-11-20/`): equations register (43
  relationships; 10 `equation-in-literature` tags) + fact register (53 facts; 35 VERIFIED-FROM-DISK) + generator v0
  (7,040-row panel) + generator v1 (6,720-row tiered occupation-aware panel; authoritative worker delivery,
  controller-verified byte-identical on two clean re-runs). v1's predeclared checks: **A PASS but target-encoded · B
  FAIL (non-diagnostic: association survives both ablations) · C PASS (half structural) · D PASS · E PASS · F PASS**;
  the load-bearing object is the **stipulated upper-secondary seat cap**, so v1 reproduces the anchor asymmetry
  substantially by assuming it. An earlier same-day intermediate run (A–D FAIL) is withdrawn; the full audit trail is
  `generator_v1/TUNE_LOG.md`. **v1.1 predeclaration must** add the education→complexity channel, remove the per-level
  anchor interpolation, adopt the ablation-fail diagnostic rule, and derive the seat cap from the economy side.
- **Amendment A2 (user directive) recorded + v1.2 spec frozen:** demographic overflow (baby boom) + lagged
  capacity → congestion/quality collapse + **childworld four-state child-labour block** (structural borrow only,
  `engine/childworld.py` sha256 `ae73adb2…`; no calibrated values; caveats carried). `synthetic_2026-11-20/v1_2/
  PRE_DECLARATIONS.md` freezes the five v1.2 checks, including "PHL asymmetry from the mechanism **without per-level
  anchor interpolation**" and "no passive neither sink". v1.2 build is the next worker-sized job.
- **Measurement insight recorded:** completion can exceed GER (UIS completion uses a 3–5-years-above-grade
  denominator) — verified PHL 2024 primary **98.30 vs 94.03**; note added to `facts/STYLIZED_FACTS.md` §12 and
  `10_massification/data/DATA_NOTES_MASSIFICATION.md`. This explains part of the old model's over-scale GER artefact
  and makes "universalisation" measure-dependent.
- **Longitudinal battery corrected to final verdicts:** H1 PARTIAL, **H2 NOT SUPPORTED** (ECI S3 −2.589,
  CI −4.112…−1.067, negative-significant, opposite the canon; raw within-country r = −0.153), H3 NOT SUPPORTED,
  H4 SUPPORTED (descriptive co-movement only); "growth is the weakly-attached variable" (all nine growth pairs
  |r| < 0.21 and negative). Package rebuilt (3 stale hashes fixed; 23/23 verify). No causal/direction/Africa claims.
- **External literature review DELIVERED** (Priority 1, user ask): `10_massification/lit/external_review_2026-11-20/`
  — memo + **76 claim rows / 63 unique sources** (38 VERIFIED-FULLTEXT, 10 VERIFIED, 14 VERIFIED-ABSTRACT, 4
  VERIFIED-METADATA, 10 UNVERIFIED flagged) + citation index + repo literature audit + deterministic assembler;
  packaged 13/13 SHA256 verify. Verdicts: (a) schooling-vs-skills settled — skills not attainment (HW 2012 1 SD ≈
  1.2–2.0 pp/yr; Pritchett 2001 no association vs 0.21–0.42 benchmark; Krueger–Lindahl initial-stock reconciliation;
  Barro 2013 counterexample 0.44 pp); (b) ECI→growth modest/contested, education→complexity is capability theory with
  R=0.13 between ECI and schooling in the field's own data; (c) absorptive/threshold frame canonical but absent
  internally; (d) credential/queue theory settled and the Philippines already measured (39% overeducated, 1-in-5
  vertical mismatch, BPO 1.9M jobs/80k net adds); (e) projection models absent internally — **WIC multi-state model
  with CC BY 4.0 2023 data is directly reusable; do not rebuild the demographic engine**. Ledger audit: 0 hits for
  growth/complexity/ECI; only 10/43 equations are literature equations. "What we do NOT need to redo" (§8) and
  "what remains open" (§9) in the memo. `web_fetch` DNS-blocked; retrieval via curl, every status reflects text read.
- **Education → ECI predeclared panel analysis run** (`10_massification/extensions/edu_eci_2026-11-20/`): 272-row
  matrix, frozen rule → **1 SUPPORTED · 5 PARTIAL · 8 NOT SUPPORTED** (12/14 robust to `eci_hs92`). Primary
  completion PARTIAL at 5 and 10 years and robust (+0.003–0.008 ECI points/pp, halved by income control); adult
  literacy stock null at 10y; upper-secondary nothing; tertiary attainment negative-significant (S2, −0.0155,
  p=0.006); no low-base heterogeneity. Existing E5 **replicated exactly** (0.5932271376, se 0.1757698583, n=253,
  23 cty; true-year-lag version 0.5691, n=320, 27 cty) — real but specification-dependent (log spec, `eci_hs92`, no
  income control). Descriptive only; no causal/direction claim. Deterministic, two runs byte-identical.
- **New user directive recorded:** hypothesis is **education → economic complexity (ECI)** (growth is a different
  outcome). `synthetic_2026-11-20/MODEL_ARCHITECTURE.md` Amendment A1 requires v1.1 to encode schooling flow → X;
  a predeclared education→ECI panel analysis is queued on the existing 30-country data
  (`09_relations/LITERACY_ECI_DEMOGRAPHY.md`: literacy STOCK 0.001 ns vs primary completion lagged 10y **0.593**,
  p=0.001 — the flow tracks complexity).
