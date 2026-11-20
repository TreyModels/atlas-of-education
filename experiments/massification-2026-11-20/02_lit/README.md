# 02_lit — audited literature & model-extraction package (task-1)

**Compiler:** lit-archivist · **Built:** 2026-11-20 · **Owner task:** task-1

## Read in this order
1. **`LITERATURE_LEDGER.md`** — all 20 core sources + the manuscripts' embedded references, one row per source in the house schema, with an explicit access status for every one.
2. **`MODEL_CARDS.md`** — the 7 formally load-bearing models in depth (agents, timing, exact LaTeX equations as recovered, parameters, identification), then 12 secondary cards. Every card carries a `FULL` / `ABSTRACT ONLY` / `LANDING` / `BLOCKED` flag.
3. **`CLAIM_REGISTER.csv`** — 68 numeric claims (18 June-only, 48 October-only, 2 shared) with source cited, verification status and an evidence note.
4. **`MANUSCRIPT_COMPARISON.md`** — June vs October vs the intermediate v1/v2 drafts: lineage, what was cut, which numbers vanished, which claims were softened, citation-integrity problems, and internal inconsistencies.
5. **`SOURCES.json`** — URL, HTTP status, content-type, bytes, UTC retrieval time, sha256 for all 26 retrieval attempts.
6. **`raw/`** (9.0 MB) — working copies: 8 PDFs + extracted `.txt`, 3 HTML pages + stripped `.txt`. **Licensing: verification copies only; quote short excerpts with page/eq citations, do not redistribute.**
7. **`notes/fetch_sources.py`** — re-runnable retrieval script (idempotent; rewrites `notes/fetch_manifest.json`). Edit `TARGETS` to add sources.
8. **`notes/fetch_manifest.json`** — raw machine record behind `SOURCES.json`.

## Headline counts
| | n |
|---|---|
| Core sources with a verified access status | **20 / 20** |
| Core sources read in full | **9** — of which 6 mined at equation level (Yoo, Kim, Kang, Jayachandran, GXL, Ostrovsky–Schwarz) and 3 mined at structure level (He 2024, Gee 2012, Edmonds–Moss 2005) |
| Core sources with a verified abstract but no equations | **2** (Yang 2026; Boudon 1974) |
| Core sources metadata-only | **3** (Yu–Ding, Saha–Saha, Bray et al. 2014) |
| Core sources landing-page only (no abstract) | **3** (Biswal, Ille–Peacey, Choi) |
| Core sources not retrievable | **3** (Bray et al. 2016, Bray–Kwok 2003, Suen–Xu). The Edmonds–Moss *URL* is broken, but the chapter was located inside the proceedings volume, so the source counts as read |
| Retrieval attempts recorded in `SOURCES.json` | **26** (17 × HTTP 200, 6 × 403, 2 × 404, 1 SSL failure) |
| Claim-register rows | **68** |
| Rows `verified` | **33** (27 are model outputs verified against the paper's own tables, 3 arithmetic, 1 cross-draft, 1 self-report, 1 mixed) |
| Rows `unresolved` / `partial` | **33** |

## The five things a downstream agent must not get wrong
1. **`03_model_architecture.md`'s Yang equation is unverified.** The CES `T(e,x)=A[λe^μ+(1−λ)x^μ]^{1/μ}` and the `ω` parameter do not come from a text anyone has read. Yang 2026 is abstract-only here (MDPI returned 403).
2. **The June draft's `Ng and Yip (2020)` citation is suspect** and the October revision did not fix it. Its printed subtitle is Gee's (2012) title. My guessed DOI was wrong and is recorded as wrong in `SOURCES.json` — do not reuse it.
3. **The Edmonds–Moss URL is the whole MABS 2004 proceedings.** The paper is pp. 130–144 of LNAI 3415. The file name `henein2004` belongs to a different paper in the same volume.
4. **Model outputs are not empirical facts.** 27 of the verified rows are simulated quantities from Triad/Massabm. They verify only that the manuscript reports its own tables correctly.
5. **Breen–Goldthorpe is in neither manuscript**, contrary to the brief. The Cambodia/*rien kuo* material is second-hand (neither Brehm & Silova 2014 nor Bray et al. 2016 was retrievable).

## Suggested next retrievals (in value order)
1. Yang (2026) full PDF — institutional MDPI access or author copy. **Unblocks the paper's novelty positioning.**
2. UNESCO UIS series for the Philippines (upper-secondary completion; tertiary GER) — the October paper's own note asks for a denominator-revision check.
3. Ng & Yip (2020) existence and DOI — or a decision to rest the intensification claim on Kang (2026) + Yoo (2003) and cite Gee (2012) only for framing.
4. Abarcar & Theoharides (2024) — the ≈9-nurses figure is the benchmark the project's own model fails against.
5. Stange (2012) — decide whether the option-value framing keeps a number or not.

---

## Iteration 2 additions (2026-11-20, task-10)
- **`COUNTRY_CARDS/{PHL,KHM,HKG,CHN,KOR,JPN}.md`** — six country cards (shadow education, gates, cohort flows, economy, policy timeline, disagreements). Every number carries source + access status; "NOT FOUND" is explicit throughout.
- **`SHADOW_TARGETS.csv`** — 21 rows, one per country x stage x provider, with `rate_pct / low / high / year / source / source_access / confidence / use_as_model_target / note`.
- **The 6 calibration targets** (use_as_model_target=YES): KOR 78.5% all levels 2023 (official, high); HKG 85% senior-secondary c.2011 (second-hand quote, medium-high); JPN 41.8% grade-6 juku (high); KHM 68.4% grade-9 and 41.3% primary, urban 60.5% vs rural 26.4% (case study); PHL 46.5% all basic 2010 (select sample, medium).
- **Data-thin: CHN** (no verified rate; IAFOR 403, CNKI paywall) **and PHL** (one 2010 select-sample survey; no national rate, no quintile gradient, nothing post-K-12).
- New full texts archived in `raw/`: Brehm & Silova WP39 (Cambodia), de Castro & de Guzman 2010 (Philippines), Rappleye & Komatsu 2020 (Japan), SEA-PLM 2024 Cambodia report (useful negative: no shadow-education module).
- Bridge status posted as party `deepseek-research` with `SHADOW_TARGETS.csv` attached.
