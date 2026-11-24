# STATUS — Atlas of Education, 24 Nov 2026 (final session status)

**Branch:** `research/handoff-2026-11-24`. **Written by:** port-commander (task-13, capstone).
**Purpose:** one-page state of the fleet at the end of the 24 Nov wave — what was done, what is verified, what
is unknown, and what the next session should do first. Companion to `HANDOFF.md` (repo root); if the two ever
disagree, the `git ls-remote` heads below win.

## 1. Fleet heads at write time (24 Nov 2026, ~18:55 local)

All heads fetched from `origin` at write time; every worktree was clean (see §4).

| Item | Branch | Head | Status |
|---|---|---|---|
| This handoff | `research/handoff-2026-11-24` | `9242214` (+ this commit) | ✓ current |
| Verification ledger | this branch, `research/records/2026-11-24-handoff/codex_wave_ledger.md` | — | ✓ |
| Hard-verified heads | port `apple-silicon-gpu-2026-11-24` | **`52d74ec`** | ✓ CUDA-kernel-verified; T4 off |
| Q1 mechanisms | `research/q1-mechanisms-2026-11-25` | `9b0cabe` | ✓ |
| Q2 pathways | `research/q2-pathways-2026-11-25` | **`9a4f586`** | ✓ errata (yardstick) |
| Q3 calibration | `research/q3-multiverse-calibration-2026-11-25` | `db7814d` | ✓ |
| E1 multiverse R=1200 | `research/e1-multiverse-1200-2026-11-25` | **`6a452a4`** | ✓ errata (136-parity) |
| E6/E8 sequencing | `research/e6e8-sequencing-2026-11-25` | **`bd782be`** | ✓ errata (18–33%, N3, controls, mean-post) |
| E11 fertility audit | `research/e11-fertility-audit-2026-11-25` | `e926575` | ✓ |
| Source verification | `research/codex-source-verification-2026-11-25` | **`ea6bc61`** | ✓ metadata erratum |
| Methods paper | `research/methods-multiverse-paper-2026-11-23` | `d7e8f9f` | ✓ |
| Paper F | `research/paper-fertility-2026-11-25` | **`23928e0`** | ✓ rounding applied (−0.227) |
| Paper M revision | `research/paper-massification-2026-11-25` | **`fb9f419`** | ✓ E6/E8 integrated |
| Paper N1 revision | `research/paper-sequencing-novel-2026-11-25` | **`62c27a3`** | ✓ |
| Suite audit | `research/suite-lit-review-2026-11-24` | **`4649cae`** | ✓ |
| Tie-breaker prereg | `research/suite-tiebreakers-2026-11-24` | **`e526c94`** | ✓ design only |
| Suite redesign (H1/H4) | `research/suite-redesign-2026-11-24` | **`1de7d33`** | ✓ H1 separable; H4 cannot test |
| Prose-data audit | `research/prose-data-audit-2026-11-24` | **`ff390fe`** | ✓ |
| Synthesis | `research/codex-wave-synthesis-2026-11-24` | **`f23f239`** (latest) | ✓ Paper F 23928e0 folded in |
| Dashboard | `research/dashboard-2026-11-23` | **`8fd2ec7`** (latest) | ✓ yardstick/errata folded in |
| DHS access path | `research/dhs-acquisition-2026-11-24` | **`77a2285`** | ⏳ waiting on human (no microdata) |
| DHS public-API sprint | `research/dhs-api-ecological-2026-11-24` | not pushed at write time | ⏳ task-16 in flight |

## 2. What was done today (24 Nov)

- **Codex wave closed and verified** (nine heads, ledger; all nine still recompute — see §4).
- **CUDA → Apple Silicon port finished**: CuPy shim + NumPy/MLX transcription; kernel **verified against 10 real
  CUDA launches** (0 integer mismatches, max abs 3.815e-6, max rel 1.192e-7); durable pinned env; T4 captured
  then shut down (关机, not release).
- **Suite audit** (the shipped exp1/exp2 cannot run their own H1/H4) and **tie-breaker design prereg**.
- **Suite redesign run** (pre-registered + one pre-run amendment): H1 = **separable** (real country-decade FE:
  slopes −0.155 / −0.027 / −0.270, joint p = 4.8e-25, no CI overlap); H4 = **cannot test (F3)** (all four
  measured tie-breakers are construction-implied transforms of the weights, R² 0.974–0.991; s=0 and
  algebraic-equivalence placebos exactly at chance).
- **DHS Individual Recode access route** documented (application pending; no data yet).
- **Papers M/N1 revised** (7% retraction, E6/E8 integration, softened framing); **Paper F** rounding fixed.
- **Synthesis + dashboard** updated with the audit correction and errata heads; **cross-record prose-data audit**
  landed, with the consolidated erratum pass annotating the flagged records.
- Human-facing artefacts: this STATUS, the updated `HANDOFF.md`, the bridge message board.

## 3. What is verified (checklist run 24 Nov, recorded in `HANDOFF.md` §11)

- `git ls-remote` heads match the table above.
- All fleet worktrees clean (0 dirty entries each).
- Ancestry: every research head is on a legitimate line — 5 branches fork at `94b612d4` (a main commit) and the
  rest descend from `55732f4`; no force-push/rewrite evidence in local records (remote reflogs are not public,
  so this is stated within that limit).
- No secrets found in `research/` paths of any fleet head (pattern scan for private keys, common token shapes,
  password/secret assignments).
- The nine ledger headlines: the synthesis recomputation script reproduces **all eight recompute groups
  byte-identically** from the committed source files (Q1 zero-signal, Q3, E1, E11, E6, Q2, Q2-yardstick,
  ordering).
- Labels: port artefacts are `PORT-*`; redesign artefacts are `SIMULATION`; observed-data records say
  `OBSERVED`; no simulation is presented as history.

## 4. What is unknown / open

- **DHS microdata**: nothing obtained; login-gated. The individual-level test is designed but unrun.
- **DHS public-API ecological sprint** (task-16) was still running at write time; no branch pushed.
- **T4 billing**: instance powered on no later than 13:14 and shut down 18:03:06 local (≤4 h 49 m); the exact
  AutoDL charge is not visible from the instance and is **not recorded** — treat as unknown.
- **The macro wall and the micro tie-breaker remain untested by simulation.** The redesign shows the wall does
  not follow from separable mechanisms (H1 separable) and that model-derived observables cannot serve as
  tie-breakers (H4 F3). That is a result about the model, not about the world.
- Paper-draft-dependent claims (E8 event ATTs, Q2 matching-sensitivity shares, Q3 design grid, methods-paper
  76/161 counts) are **UNVERIFIED (committed field only)** per the synthesis record §7 — do not quote as
  established.

## 5. What the next session should do first

1. **DHS second request**: submit the second African project request (the first application is pending), then
   download IR files under the DUA. This is the only route to a real individual-level tie-breaker; do not
   substitute model-imputed proxies.
2. **Read the redesign verdict before citing the suite**: `research/suite-redesign-2026-11-24` @ `1de7d33`,
   `ANALYSIS.md`. H1 is model-conditional "separable"; H4 is "cannot test (F3)". Do **not** analyse the old
   PORT-PRODUCTION exp2/exp3 outputs as evidence.
3. **Downstream errata**: if any paper or dashboard text still quotes 18–33%, N3 56–84%, controls "25–30",
   mean-post "18–29", Q2 52.4%/50.3%, E1 "BY 0/0/0", Paper F −0.228, or Paper F head `4f8a61c`, correct it to
   the annotated erratum value/head before publication.
4. **If a new simulation is attempted**, it needs a different model/observables (see redesign ANALYSIS §4), not
   another port or another run of the shipped code.
