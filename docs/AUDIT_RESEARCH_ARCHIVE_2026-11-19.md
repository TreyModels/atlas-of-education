# Research archive integrity audit — CCP "bus" import and research-rigor integration

- **Date:** 19 November 2026, ~20:15–21:05 Asia/Shanghai
- **Auditor:** DeepSeek Harness archive/compliance agent (`archive` teammate)
- **Branch:** `audit/research-archive`, based on `origin/main` @ `c3cc71c` ("Merge pull request #14 from TreyModels/rename/atlas-worlds")
- **Scope:** read-only verification of the landed CCP bus import and the research-rigor / research-track integrations, plus public download-link and provenance honesty. **No research content was edited, no experiment was run, nothing was uploaded (apart from this branch).**

## What this audit establishes, in one paragraph

The CCP "bus" import is **intact and byte-identical to its handover manifest**: all 287 declared files are on `main` with matching SHA-256, the four public download ZIPs are byte-for-byte copies of `experiments/ccp-bus/models/`, and no manuscript or paper from the handover was imported. The research-rigor and research-track content is also fully present: no file from either branch is missing from `main`, and the five earlier conflict files resolve coherently. The **serious problems are repo-wide, not in the CCP import**: the public repo still publishes third-party copyrighted papers — one as a standalone PDF and four inside the fertility download ZIPs — which directly contradicts the CCP package's own "papers excluded pending redistribution review" policy. On provenance, the CCP result tables are **reported, not reproduced by the Atlas team**: the repository contains the handover's model code and stored result tables, but no Atlas-run verification, run log or test executes them, and no document says so plainly. The claim boundary ("What none of this claims") is present and visible, and the disciplinary filing counts are correctly framed as filings, not corruption prevalence.

## Refs compared

| Ref | SHA | Commit date |
|---|---|---|
| `origin/main` (base of this branch) | `c3cc71c7a776ea21b2550e9e5a54c04009b482af` | 2026-11-19 20:01 |
| `origin/import/ccp-bus` | `2e19f0786a5ee5cd545a42472c453fb4ee05156c` | 2026-11-19 17:10 |
| `origin/integrate/research-rigor-2026-11-19` | `1b28be1010a9ced0ab942d0e2ce6afe3e69d6351` | 2026-11-19 16:14 |
| `origin/feat/research-track` | `94b612d482eab694a79dc7124efdc9e35470c5db` | 2026-11-15 23:38 |

None of the three source branches is an ancestor of `main` (`git merge-base --is-ancestor` fails for all three; all share base `fbc58cd`). Their content reached `main` through `feat/ccp-journey` / `angkor-journey` merges instead (e.g. import commit `851db3f` on `main` has a tree identical to `2e19f07` for `experiments/ccp-bus/`). **Consequence:** any URL pinned to the import commit is reachable only while the `import/ccp-bus` branch keeps the object alive — see finding B1.

## Verdict

| Area | Verdict | Notes |
|---|---|---|
| CCP import file completeness | **PASS** | 287/287 manifest files present, all SHA-256 match; 0 files from `import/ccp-bus` missing from `main` |
| CCP public ZIPs | **PASS (fidelity)** | 4/4 byte-identical to source dirs; 6/9/41/215 entries; no extra or foreign files |
| CCP paper/manuscript exclusion | **PASS with one inconsistency** | `Priest and the Bandit` manuscript and white paper absent; but one "excluded" literature review is byte-identical to a kept file and ships inside `ccp-bus-v6.zip` (A4) |
| Repo-wide third-party paper policy | **FAIL (high)** | Third-party published PDFs are published and linked (A1, A2); see also the co-authored working paper inside the fertility ZIPs (A3) |
| research-rigor + research-track integration | **PASS** | 0 files from either branch missing from `main`; five conflict files coherent (C3 explains the one evidence.js divergence) |
| Provenance labelling: reported vs verified | **GAP** | Results are reported, not reproduced; no document says so (B2); BRIEFING contradicts itself on the v7 "genuine holdout" (B3) |
| Claim boundary / prevalence framing | **PASS** | Boundary present at 6 locations and rendered on the family page; cases explicitly "not corruption prevalence" |
| Local download links | **PASS** | 36/36 unique local asset paths in `src/data/model-catalogue.ts` + 9 journey files exist under `public/`; repo's own link guard passes |
| External links | **PASS (with one bot-block)** | 20/21 return HTTP 200; `doi.org/10.1086/ahr.116.4.937` returns 403 to curl but the DOI handle resolves (valid link) |
| Checksum coverage of downloads | **GAP (low)** | `SHA256SUMS.json` does not list any CCP ZIP (C1) |

## 1. CCP import integrity

### 1.1 File set and hashes

`experiments/ccp-bus/IMPORT_MANIFEST.json` declares 287 imported files and 3 excluded papers, and records the source archive `CCP_bus_model_handover_2026-11-19.zip` (SHA-256 `c8f0e9df…b3c2b`, base commit `94b612d` = the research-track tip).

Verified against `origin/main`:

- 287/287 declared `repository_path` files exist.
- 287/287 SHA-256 values match the bytes in `main` (**zero mismatches**).
- Files on `main` under `experiments/ccp-bus/` = 289 = 287 imported + `IMPORT_MANIFEST.json` + `README.md` (the two files added by the Atlas team on `main`).
- Every file on `origin/import/ccp-bus` under `experiments/ccp-bus/` and `public/research/ccp-bus/` exists on `main`; **nothing is missing**.
- Content diff between `import/ccp-bus` and `main` for `experiments/ccp-bus/` is empty except the added 25-line `README.md`.

Retention policy in the manifest (`IMPORT_MANIFEST.json:1748`): "Original bytes preserved; package README renamed PACKAGE_README.md; papers excluded pending redistribution review. Archive not copied to public/."

### 1.2 Public CCP download ZIPs

All four exist on `main`, are valid ZIPs, and were built **only** from the corresponding model directory (no papers, no extra files, no renamed content).

| File | Bytes | SHA-256 | Entries | Fidelity vs `experiments/ccp-bus/models/` |
|---|---:|---|---:|---|
| `public/research/ccp-bus/ccp-bus-v1.zip` | 7,613 | `ee16602107eac0337b7b27c43bfec64be480dc16adfd59e5135465abf627e607` | 6 | 6/6 match, 0 extra |
| `public/research/ccp-bus/ccp-bus-v3.zip` | 278,638 | `fd3327fbee8219cf223dbb253093769f79b475e86c8394a35dab4e67de38ecfd` | 9 | 9/9 match, 0 extra |
| `public/research/ccp-bus/ccp-bus-v6.zip` | 1,717,396 | `ed8e69023e0391b5f26389424c8954aeee1e004c290698f1075e434b0b4b4077` | 41 | 41/41 match, 0 extra |
| `public/research/ccp-bus/ccp-bus-v7.zip` | 144,181 | `4322e22ba051bcb17c09fdef294854de4b887398927268068a429db58d86fc97` | 215 | 215/215 match, 0 extra |

Method: every ZIP member was hashed and compared with `git show origin/main:experiments/ccp-bus/models/<member>`. Downloaded-only files, altered files and paper/manuscript members: **none** (apart from the literature-review inconsistency in A4, which is a tracked file, not a ZIP smuggling issue).

### 1.3 What is *not* in the repo from the handover

The three excluded papers are declared at `IMPORT_MANIFEST.json:1731-1746`:

- `papers/CCP_corruption_literature_review_2026-11-18.md` (46,689 B) — **see A4: byte-identical copy is kept and published.**
- `papers/The_Priest_and_the_Bandit_user_manuscript_2026.md` (39,325 B) — absent; no tracked file has that size or that SHA-256.
- `papers/The_Bus_White_Paper_2026.md` (24,218 B) — absent; no tracked file has that size or that SHA-256.

So the confidential handover parts (Trey's unreviewed manuscript and white paper) **did not leak into the public repo**. That part of the policy worked.

## 2. research-rigor and research-track integration

### 2.1 File presence

- Files on `origin/integrate/research-rigor-2026-11-19` missing from `main`: **0** (49 paths changed by that branch, all present).
- Files on `origin/feat/research-track` missing from `main`: **0** (81 paths changed by that branch, all present).
- All the rigor machinery is on `main`: `research/rigor/*` (design/analyze/stats/adapters/protocols/tests), `research/tests/*`, `research/RUN_LOCAL.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/model-challenge.yml`, `engine/relfloor_gate.py`, `engine/firms/model.py` changes.
- All research-track content is on `main`: `research/GATE.md`, `research/PUZZLE_LOG.md`, `research/china-forecast-ledger/*`, `research/credential-floor/*`, `research/marriage-gap/*`, `research/methods-paper/*`, `REVAMP.md`, `teach/`.
- Internal link targets from `research/README.md` all exist on `main` (`RUN_LOCAL.md`, `rigor/README.md`, `rigor/protocols_rigor.json`, `GATE.md`, `PUZZLE_LOG.md`, `ISSUES.md`, `CHANGELOG.md`, `literature.json`, `protocols.json`, `CONTRIBUTING.md`).

### 2.2 The five earlier conflict files

| File | State on `main` | Verification |
|---|---|---|
| `research/README.md` | **Merged superset**: rigor/protocols sections (from integrate) **and** "Research projects and teaching materials" with the GATE/PUZZLE_LOG table (from track), with updated wording | Both branches' key sections present; diff vs each branch shows only additive/updated text |
| `public/evidence.js` | Identical to `src/models/evidence.js`; regenerated on `main` by `8da0922` (16:44, after the integrate branch) | Relfloor payload reproduces exactly from `public/reference/relfloor_countries_v2_smoothliq.json` via `scripts/build-relfloor-evidence.py::compact()` (run in memory; byte-identical values). Divergence from integrate branch explained in C3 — not a regression |
| `src/models/evidence.js` | Same file content as `public/evidence.js` (verified `cmp`) | Embedded `sha256` map has one stale entry — C2 |
| `src/models/source-hashes.json` | Current: 19 entries; `relfloor_countries.json` replaced by `relfloor_countries_v2_smoothliq.json` | All 19 values verified against the actual served inputs: 16 against `public/`+`src/models/`, `results.json` and `trajectories_100_seeds.csv` against `inputs/`, `model.js` against `public/reference/angkor/model.js`. **0 mismatches** |
| `src/data/ui-translations.json` | Superset of both branches (3,002 keys vs 2,041/2,011) | Only one branch-only key is absent on `main`: the pre-rewrite sentence "…how Angkor declined…"; `main` has the corrected sentence with `zh-Hans`, `vi` and `fr` translations. Coherent — C6 |

No lost content was found in any of the five files. In addition, `src/data/model-catalogue.ts` carries both branches' content: the `politics` family with the four CCP download entries, the `extension` family, the moved credential-floor entry (from `84dd31f`), the new family groupings, and the politics "mechanisms, not prevalence" description (`src/data/model-catalogue.ts:154`).

## 3. FINDINGS — third-party papers and manuscripts in the public repo

The CCP package excluded papers "pending redistribution review" (`IMPORT_MANIFEST.json:1748`) and the repo's licence notice says "Third-party materials retain their own terms" (`README.md:54`). **The same standard is not applied to the rest of the public repo.** These are the highest-priority findings.

### A1 — HIGH — Third-party peer-reviewed paper published as a standalone PDF

`public/research/provisioning-paper.pdf` (2,591,183 B, SHA-256 `5df86560…4b0006`) is *"Provisioning an Early City: Spatial Equilibrium in the Agricultural Economy at Angkor, Cambodia"* by Sarah Klassen, Scott Ortman, José Lobo and Damian Evans, published in the *Journal of Archaeological Method and Theory* (DOI [10.1007/s10816-021-09535-5](https://doi.org/10.1007/s10816-021-09535-5)). PDF metadata records author "Sarah Klassen"; the site itself calls it "Klassen, Ortman, Lobo and Evans's Provisioning an Early City".

It is redistributed in the repo and linked as a download:

- `src/data/angkor-journey.ts:90` — `{ label: 'The paper (PDF)', href: 'research/provisioning-paper.pdf' }`
- `src/components/Workbench.tsx:144` — "Download model paper" link
- `public/research/institutions/index.html:1` — `<a href="../provisioning-paper.pdf">Read the uploaded provisioning paper</a>`
- Listed in `SHA256SUMS.json:75,197` (both `dist/` and `public/` paths)

Risk: redistribution of a copyrighted Springer article without a licence. The correct object to publish is a DOI link and a PDF *only* if redistribution permission exists. `scripts/check-angkor-journey.mjs` does not check third-party rights, so the internal guard does not catch this.

### A2 — HIGH — Four third-party papers inside both public fertility download ZIPs

Both fertility packages on `main` contain a `fertility_handoff/reference/` folder with four third-party PDFs:

- `public/research/fertility/fertility-research-full.zip` (5,102,926 B, 120 entries)
- `public/research/fertility/fertility_research.zip` (5,022,726 B, 80 entries; linked from `public/research/fertility.html:115`)

Members and sizes in both:

| ZIP member | Bytes | Identity (PDF metadata / title page) |
|---|---:|---|
| `fertility_handoff/reference/stone_amish.pdf` | 694,606 | "Amish fertility…" — authors Lyman Stone, Cory Anderson & Stephanie Thiehoff |
| `fertility_handoff/reference/stone_marriage_report.pdf` | 4,869,840 | Lyman Stone report (InDesign-produced) |
| `fertility_handoff/reference/stone_test_pids.pdf` | 979,664 | Lyman Stone test report |
| `fertility_handoff/reference/stone_ultraorthodox.pdf` | 1,640,649 | "Ultra-Orthodox fertility and marriage in the United States…" — author Lyman Stone (published article) |

They are advertised as downloads in `src/data/model-catalogue.ts:74` and `:182` ("Fertility research bundle · code, data & findings"), and linked from `src/data/fertility-journey.ts:64,177,224,271,319,367,410,451` and `public/research/fertility.html:115`. Same redistribution problem as A1: copyrighted third-party publications inside a public download.

### A3 — MEDIUM — Manuscript policy is inconsistent across families

The same fertility ZIPs contain `fertility_handoff/reference/Massification_and_Its_Mechanisms.md` — Trey's co-authored working paper with Bjørn Nordtveit (the handover README calls it "the provided manuscript"). The CCP package excluded the analogous unreviewed manuscript and white paper "pending redistribution review" (A4 context), so the repo is applying the exclusion to one family and not another. Author-owned, so lower external risk, but it is a policy inconsistency and contradicts the plain reading of the CCP exclusion decision.

### A4 — MEDIUM — One "excluded" CCP paper is not actually excluded

`IMPORT_MANIFEST.json:1733` excludes `papers/CCP_corruption_literature_review_2026-11-18.md` with SHA-256 `362c5bdda0c81ef336e3e762060bfbb7571e61719315d8b117ca0a6d4a134ce2`. That exact content is:

- tracked on `main` as `experiments/ccp-bus/models/C_chatgpt_v6_tilly/LITERATURE_REVIEW.md` (SHA-256 verified identical), and
- shipped in the public download `public/research/ccp-bus/ccp-bus-v6.zip` as member `C_chatgpt_v6_tilly/LITERATURE_REVIEW.md`.

This is an original literature review, so the copyright exposure is low — but the manifest and the "3 excluded papers" statement in `experiments/ccp-bus/README.md:19` are **factually inconsistent with what is published**. Either reclassify this item as retained (and say so in the README/manifest) or remove it from the ZIP and repo. It should not be left ambiguous.

## 4. Provenance: reported, not verified

### 4.1 Plain statement for the record

**The CCP result tables are reported, not reproduced by the Atlas team.** They are the outputs of a third-party model-building handover (models built with Claude and ChatGPT, 17–19 November 2026, per `experiments/ccp-bus/BRIEFING.md:3`), imported as an archive. The repository contains the model source, the stored result files, and the handover's own documentation — but **no Atlas-run verification artifact**:

- No script, test, CI workflow or run log in the repo executes the four Python model versions. `scripts/check-angkor-journey.mjs` only validates journey structure, labels and links (it does execute: pass for all nine journeys).
- `scripts/check-all.sh` / `check-repairs.cjs` do not touch `experiments/ccp-bus/`.
- Git history after import is only packaging and prose (`851db3f` import, `781566c` journey page, `a578f40` merge, plus the two `main`-added files). No result file has been recomputed by the Atlas team.

So anywhere the repo presents v1/v3/v6/v7 numbers as "results", they should be read as **reported by the handover, unverified by Atlas**. This is not currently stated anywhere (`experiments/ccp-bus/README.md:18-19` says only "Imported at commit `2e19f07`"; `BRIEFING.md` is the handover's own text).

What *was* independently cross-checked in this audit (number-to-artifact consistency, not reproduction):

| Claim (journey / briefing) | Stored artifact | Match |
|---|---|---|
| CCDI cases 618/631/596/626/877/1,012 thousand (2020–25) | `experiments/ccp-bus/data/verified_observations.csv` | exact |
| v7 strict log RMSE 50k: 0.1955 / social trap 0.1896 / bus 0.1898 | `models/D_chatgpt_v7_identification/results/holdout_scores.csv` (0.19548 / 0.18959 / 0.18979) | exact after rounding |
| last-value MAE 115,667 vs bus 118,066 | same file (115666.67 / 118066.29) | exact |
| memory test step-1 gap 0.8332, ≈0 by step 10 | `models/D_chatgpt_v7_identification/results/memory_runs.json` (mean gap_1 = 0.8332 for social_trap and bus; gap_10 = 0.0) | exact |
| 17 accepted fits, 42 hand-set parameters, 14 passing checks | `models/B…/README.md`, `models/C…/RESULTS.md` | present as reported, not re-run |

### 4.2 B2 — MEDIUM — No "reported, not reproduced" label

Add one sentence to `experiments/ccp-bus/README.md` (e.g. under "Provenance") and to the v7/Journey sources: *"Result tables are reported by the external model-building handover; the Atlas team has not independently reproduced them."* Without it, a reader reasonably assumes the project verified its own tables. This is exactly the distinction the rest of this audit cares about.

### 4.3 B3 — LOW/MEDIUM — Handover briefing contradicts the corrected labelling

- `experiments/ccp-bus/BRIEFING.md:21` — "**The first genuine holdout test.**"
- `experiments/ccp-bus/README.md:12` — "A retrospective test, not a genuinely untouched holdout: the 2020–25 outcomes were already known when the model was designed."
- `src/data/ccp-journey.ts:82` — "this is a retrospective holdout, not an untouched forecast."

The website and the `main`-added README are correct; the imported briefing is not. Since `BRIEFING.md` is preserved as original-bytes (manifest policy), add an errata line in `experiments/ccp-bus/README.md` rather than editing the imported file. The same briefing also calls the v7 table "the most rigorous result so far" (line 23) and the "Honest bottom line" (line 42) is honest, but the holdout framing must be corrected.

### 4.4 B4 — LOW — ZIPs ship without a package-level provenance/licence/limits file

The four CCP ZIP roots contain only model directories; there is no top-level README, licence note, or "What none of this claims" text inside the download. A person who downloads `ccp-bus-v7.zip` gets code and model docs but no statement that results are unreproduced, no licence pointer, and no paper-exclusion note. Recommend adding a short `PACKAGE_PROVENANCE.md` at the root of each ZIP (or one shared file) and rebuilding the ZIPs.

## 5. Claim boundary and corruption-prevalence framing — PASS

The "What none of this claims" boundary is present, visible and consistent, in six places:

- `experiments/ccp-bus/README.md:23` — dedicated section: no prevalence estimate, no real official identified, no personal motives, all agents synthetic.
- `experiments/ccp-bus/BRIEFING.md:68` — same section, same wording.
- `src/data/ccp-journey.ts:65` (lede): "The manuscript is not peer reviewed, and nothing here treats its claims as established fact."
- `src/data/ccp-journey.ts:80`: "Cases are not corruption prevalence: they mix detection, reporting, enforcement capacity and the underlying behaviour."
- `src/data/ccp-journey.ts:208` (`bottomLine`): "…nothing here estimates the actual prevalence of corruption in China, identifies any real official as corrupt, or describes anyone's personal motives." — rendered by `src/components/AngkorJourney.tsx:152`.
- `src/data/family-stories.ts:295` and `src/data/model-catalogue.ts:154`: "They describe mechanisms, not the prevalence of corruption."; `src/data/site-status.ts:17`: "Synthetic agents only."
- The `why` intro is rendered at `src/components/AngkorJourney.tsx:66-67`, so the boundary is on the page, not only in repo docs.

Filing counts are never presented as prevalence in any of these surfaces; the 2020–25 series is labelled "Annual cases filed" and the difference between filings and underlying corruption is stated twice (`ccp-journey.ts:80`, `family-stories.ts:301`). The page is reachable through the shared journey component (`src/App.tsx:115`, `story-politics`), not a stray HTML file: no `public/research/ccp-bus/*.html` page duplicates the claims unlabelled.

## 6. Download links

### 6.1 Local targets — 36/36 resolve

Every unique local asset string in `src/data/model-catalogue.ts` and the nine `src/data/*journey*.ts` files (35 unique paths after stripping `#fragment`, 36 including fragment variants) exists under `public/`. This includes the four CCP ZIPs, `research/provisioning-paper.pdf` (**exists, but see A1**), `research/field-schools/*`, `research/fertility/*`, `research/shadow/*`, `research/out-of-africa/*`, `research/massification/*`, `research/*.html`, `engines/*.js`, `reference/*`.

Independent confirmation: the repo's own guard `node scripts/check-angkor-journey.mjs` passes (all nine journeys; every relative `href`/`engine`/`research` link resolved against `public/`):

```
shadowJourney: 6 chapters, 3 cards, links ok.
educationJourney: 6 chapters, 8 cards, links ok.
systemsJourney: 6 chapters, 9 cards, links ok.
extensionJourney: 6 chapters, 4 cards, links ok.
ccpJourney: 5 chapters, 4 cards, links ok.
fertilityJourney: 9 chapters, 9 cards, links ok.
deepHistoryJourney: 4 chapters, 1 cards, links ok.
planningJourney: 6 chapters, 12 cards, links ok.
Angkor journey: 6 chapters, 13 model cards, 27 links checked. Passed.
```

### 6.2 External targets — 20/21 return 200; DOI 403 is a bot-block

Checked sequentially with a polite `curl -L -A … --max-time 20` (one HEAD/GET per URL, ~0.4 s apart):

| Result | URLs |
|---|---|
| 200 | repo root, `archive/refs/heads/main.zip`, `blob/main/REVIEW_STATUS.md`, six `blob/main/experiments|research/.../README.md`, `blob/main/src/models/worlds.js`, `tree/main/research/shadow-education` |
| 200 | all seven `2e19f07`-pinned CCP source URLs: `tree/2e19f07/…/models/`, `blob/2e19f07/…/BRIEFING.md`, v1 tree, v3 README, v6 RESULTS, v7 RESULTS (see B1 for durability caveat) |
| 200 | `https://www.dhsprogram.com/pubs/pdf/FR377/FR377.pdf`, `https://doi.org/10.1007/s10816-021-09535-5`, `https://claude.ai/artifact/QQtWPZKMkUezRkVzx1YZeG` |
| 403 → **valid** | `https://doi.org/10.1086/ahr.116.4.937` — publisher (Chicago) blocks automated clients; the DOI resolver API returns `responseCode:1` with a URL, so the link resolves for a browser. No action needed |

`https://claude.ai/artifact/QQtWPZKMkUezRkVzx1YZeG` in `experiments/ccp-bus/PACKAGE_README.md:11` is a third-party, non-archival artifact link (returns 200 today). It is not a public site download, but the claim "Full write-up" depends on an account-bound claude.ai page. Recommend replacing it with a repo document or the DOI, or marking it "external, may expire" (C4).

### 6.3 ZIP sizes / checksums

CCP ZIP sizes and hashes are recorded in §1.2. `SHA256SUMS.json` (a repo-root manifest) covers only the three `institutions` ZIPs plus `provisioning-paper.pdf` — **none of the four new CCP ZIPs, and none of the fertility/shadow/field-schools/out-of-africa ZIPs**. Buyers of the "download all code" promise therefore have no published checksum for most research downloads (C1). The ZIPs themselves are byte-faithful today, so this is a coverage gap, not a corruption finding.

## 7. Consolidated findings register

| ID | Severity | File:line | Finding | Recommended action |
|---|---|---|---|---|
| A1 | **HIGH** | `public/research/provisioning-paper.pdf`; links `src/data/angkor-journey.ts:90`, `src/components/Workbench.tsx:144`, `public/research/institutions/index.html:1` | Third-party peer-reviewed article (Klassen et al., Springer JAMT, DOI 10.1007/s10816-021-09535-5) redistributed in the public repo and offered as a download | Remove the PDF; link the DOI instead; delete the two `SHA256SUMS.json` entries; regenerate `dist/` |
| A2 | **HIGH** | `public/research/fertility/fertility-research-full.zip` and `public/research/fertility/fertility_research.zip` (members `fertility_handoff/reference/stone_*.pdf`); links `src/data/model-catalogue.ts:74,182`, `src/data/fertility-journey.ts:64…451`, `public/research/fertility.html:115` | Four third-party (Lyman Stone) papers/reports redistributed inside public downloads | Remove the four PDFs from both ZIPs (keep a citation list), rebuild ZIPs, update checksums and any descriptions that promise the "reference" pack |
| A3 | MEDIUM | same fertility ZIPs, member `fertility_handoff/reference/Massification_and_Its_Mechanisms.md` | Trey/Bjørn working paper published inside a public download while the CCP package excluded the analogous manuscript | Decide and document one manuscript policy; if retained, label it as unpublished working paper; if not, remove from ZIP |
| A4 | MEDIUM | `experiments/ccp-bus/IMPORT_MANIFEST.json:1733`; `experiments/ccp-bus/models/C_chatgpt_v6_tilly/LITERATURE_REVIEW.md`; `public/research/ccp-bus/ccp-bus-v6.zip` member `C_chatgpt_v6_tilly/LITERATURE_REVIEW.md`; `experiments/ccp-bus/README.md:19` | "Excluded" literature review is byte-identical to a retained, published file; "3 excluded papers" is inaccurate | Reclassify (retained, original material) and correct README/manifest, or remove from ZIP+repo; rebuild ZIP |
| B1 | MEDIUM | `src/data/model-catalogue.ts:198`, `src/data/ccp-journey.ts:20-25` | Source/provenance URLs pinned to `2e19f07`, a commit **not reachable from `main`** (only via `import/ccp-bus`); 200 today but fragile if the branch is deleted | Repin to a `main` commit (`851db3f` has the identical `experiments/ccp-bus` tree) or a tag |
| B2 | MEDIUM | `experiments/ccp-bus/README.md:18-19`; handover docs | No statement that result tables are reported by the external handover and **not reproduced by the Atlas team** | Add the one-line disclosure to the README (and to the journey sources) |
| B3 | LOW/MED | `experiments/ccp-bus/BRIEFING.md:21` vs `experiments/ccp-bus/README.md:12` and `src/data/ccp-journey.ts:82` | Briefing calls v7 "the first genuine holdout test"; website/README correctly call it retrospective (outcomes known at design) | Add an errata note in the README; do not edit imported bytes |
| B4 | LOW | CCP ZIPs (`public/research/ccp-bus/*.zip`) | No package-level README/provenance/licence/limits file inside the downloads | Add `PACKAGE_PROVENANCE.md` to each ZIP (reported-not-reproduced, papers excluded, licence) |
| C1 | LOW | `SHA256SUMS.json` | No checksums for any CCP ZIP (or most other research ZIPs) | Add the four CCP hashes from §1.2 (and ideally all public ZIPs) |
| C2 | LOW | `public/evidence.js:1` and `src/models/evidence.js:1` (embedded `sha256.worlds.js` = `170af43…`) vs `src/models/source-hashes.json:15` (`5732383…`) | Embedded evidence bundle advertises a stale hash for `worlds.js` (actual `public/worlds.js` = `5732383…`); the in-app hash table used by React is correct | Regenerate `public/evidence.js` with `prepare-evidence.py` (note: that script currently hashes `dist/`, and would drop the `worlds.js` key — reconcile the two hash tables) |
| C3 | INFO | `public/evidence.js` / `src/models/evidence.js` | Relfloor payload differs from `integrate/research-rigor@1b28be1`; `main` is newer (commit `8da0922`, 16:44) and regenerated from `public/reference/relfloor_countries_v2_smoothliq.json` | None — verified: `compact()` reproduces `main`'s payload exactly; integrate branch carried the older, larger engine `relfloor_countries.json` rendering |
| C4 | INFO | `experiments/ccp-bus/PACKAGE_README.md:5,11` | References a `papers/` directory absent from the repo, and a claude.ai "full write-up" link (200 today, non-archival) | Annotate with a mapping to the excluded papers and replace the artifact link |
| C5 | INFO | `src/data/deephistory-journey.ts` (AHR DOI) | `10.1086/ahr.116.4.937` returns 403 to automated clients | None — DOI resolves (`doi.org/api/handles` 200); publisher bot-block only |
| C6 | INFO | `src/data/ui-translations.json` | Superset of both branches; the one branch-only sentence key was replaced by the corrected wording with complete `zh-Hans`/`vi`/`fr` translations | None |

## 8. Checks performed and not performed

**Performed (read-only):** git fetch/ancestry/ls-tree/diff/show; manifest hash re-verification (287 files); ZIP member hashing and fidelity comparison (4 ZIPs, 271 members total); source-hash re-verification (19 entries); evidence-bundle regeneration in memory (`scripts/build-relfloor-evidence.py::compact()`); journey link/structure guard (`node scripts/check-angkor-journey.mjs`); local target existence (36 paths); 21 external URLs via polite curl; ZIP paper-member scan across all 14 public ZIPs; PDF metadata/identity inspection; number-to-artifact cross-checks (cases series, holdout scores, memory gaps); paper/manuscript size- and hash-exclusion scan.

**Not performed (out of scope / forbidden by the task):** no Python experiment runs, no model re-execution, no download of third-party papers, no research-content edits, no uploads. `npm`/dependency installation was not run (node_modules is a symlink). The site was not rebuilt or redeployed.

**Environment:** Node v26.12.0 (`/opt/homebrew/bin` forced), worktree `wt-compliance` on `audit/research-archive`, base `origin/main` `c3cc71c`. Worktree otherwise clean (only the untracked `node_modules` symlink).

## 9. Bottom line for the Lead

1. **The CCP import and the research-rigor integration did land intact.** 287/287 manifest files and hashes, 4/4 faithful ZIPs, 0 missing files from either integration branch, all five conflict files coherent, all 36 local download targets resolve, 36/9 journey structure guard passes.
2. **Two high-severity paper-redistribution problems are repo-wide and pre-existing, not CCP-specific:** the Klassen PDF at `public/research/provisioning-paper.pdf` and four Lyman Stone PDFs inside both public fertility ZIPs. They should be taken down before any public launch/announcement that makes the repo's own "third-party materials" claim load-bearing.
3. **Provenance wording needs one honest sentence:** the CCP result tables are *reported, not reproduced by the Atlas team*; the repo says neither.
4. **Minor integrity follow-ups:** repin `2e19f07` links, add CCP ZIP checksums, regenerate `public/evidence.js` (stale `worlds.js` hash), and add a provenance file inside the CCP ZIPs.
