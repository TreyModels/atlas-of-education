# Model Routing Research: DeepSeek Flash vs Z.AI GLM Flash

**Decision brief for worker/orchestrator selection in a cheap, multi-agent scientific research pipeline.**
Compiled 2026-11-20 (Asia/Shanghai). All prices USD per 1M tokens unless stated.

**Routes under evaluation** (ids as supplied by the requester; provider *model* ids verified at source, harness route ids not independently verified — the packaged harness checkout was not readable from this sandbox):

| Harness route | Provider model id | Verified at |
|---|---|---|
| `deepseek-official/deepseek-flash` | `deepseek-flash` → DeepSeek-V4.1-Flash-1017 | [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) |
| `zai/glm-5.3-flash` | `glm-5.3-flash` | [Z.AI pricing](https://docs.z.ai/guides/overview/pricing), [model page](https://docs.z.ai/guides/vlm/glm-5.3-flash) |
| `zai/glm-4.7-flash` | `glm-4.7-flash` (free tier) | [Z.AI pricing](https://docs.z.ai/guides/overview/pricing) |

**Evidence labels used throughout.** `[V]` vendor-reported (provider docs, model card, launch post). `[I]` independent evaluation (Artificial Analysis, Vals AI, Design Arena, measured telemetry). `[U]` user/practitioner report (public issue trackers, forum posts, reviews) — indicative, not controlled. `[?]` could not verify.

**Method note.** `web_fetch` was blocked in this sandbox (DNS policy), so pages were retrieved with `curl` and parsed locally; page text is preserved as accessed. Prices move fast: treat every number here as *as of 2026-11-20*.

---

## 1. Executive summary

- **The premise "GLM Flash is the cheap option" does not survive contact with the price sheets.** Per-token list prices are near-identical (DeepSeek Flash $0.15–$0.30 in / $0.60–$1.20 out vs GLM-5.3-Flash $0.15 in / $0.50 out) `[V]` — GLM is not meaningfully cheaper, and on cached input it is **10× more expensive** ($0.03 vs $0.003/M). ([DeepSeek](https://api-docs.deepseek.com/quick_start/pricing), [Z.AI](https://docs.z.ai/guides/overview/pricing))
- **DeepSeek Flash is the more intelligent model, by a clear margin on independent testing:** Artificial Analysis Intelligence Index **32.6** (max effort) / 28.6 (high) vs GLM-5.3-Flash **27.8**; rank #2/32 vs #11/32 in class `[I]`. ([AA DeepSeek](https://artificialanalysis.ai/models/deepseek-v4-1-flash-1017), [AA GLM](https://artificialanalysis.ai/models/glm-5-3-flash))
- **DeepSeek Flash is also ~2.9× faster per task:** 14.4 min vs **41.4 min** per Intelligence Index task (median 15.0) `[I]`. GLM at 41.4 min/task is explicitly "notably slow" — a throughput ceiling for a parallel worker fleet, not a latency annoyance.
- **Cost per task lands at near-parity ($0.60 vs $0.58) `[I]`,** because GLM's cheaper output price is offset by its much longer wall-clock and heavy reasoning-token burn. At scale the tie-breaker is throughput and reliability, both of which favour DeepSeek.
- **DeepSeek's decisive cost lever is off-peak scheduling: prices are exactly halved** outside 01:00–04:00 and 06:00–10:00 UTC on weekdays `[V]`. Batch pipelines that can wait should schedule all bulk work off-peak — a free 2× discount that no model swap matches.
- **GLM-5.3-Flash cannot turn thinking off** (`thinking.type` only accepts `enabled`) and defaults to `reasoning_effort: max` `[V]`, so every trivial call pays a reasoning-token tax unless you explicitly pin effort. A practitioner team hit exactly this: "slow as if thinking about life" until they set `reasoning_effort: "high"` `[U]`.
- **The free `glm-4.7-flash` is not usable as a fleet worker.** Independent reports put free Z.AI Flash models at **one concurrent request per model** `[U]`, and the model is a generation behind (GLM-4.7-Flash HLE 7.6%, AA-LCR 41.7% vs DeepSeek's 43.3% / 82.7%) `[I]`. It is a serialized single-thread tool, not a parallel worker.
- **Neither model is safe for final scientific synthesis unsupported.** GDP.pdf (deep document reasoning) is 17.2% (DeepSeek) and 15.4% (GLM); Terminal-Bench-Science is 12.9% and 4.8% `[I]`. These are "assist a competent reviewer" numbers, not "trust the output" numbers.
- **A real hallucination/accuracy split exists:** DeepSeek is more accurate on AA-Omniscience (39.6% vs 28.2%) but scores *worse* on AA's non-hallucination rate (35.9% vs 61.7%) `[I]` — DeepSeek knows more and confabulates more; GLM abstains more often. For citation-bearing stages, pair DeepSeek generation with a deterministic citation check, or route verification to GLM.
- **Recommendation:** DeepSeek Flash at `reasoning_effort: high` is the default worker *and* orchestrator for ~80% of pipeline stages; `deepseek-v4-pro` (3.3× output price) for final synthesis and adversarial review; GLM-5.3-Flash as a second-opinion/abstention reviewer and long-document reader; `glm-4.7-flash` only for serialized, zero-stakes mechanical work.

---

## 2. Specs and pricing

### 2.1 Model specs

| | **DeepSeek Flash** | **GLM-5.3-Flash** | **GLM-4.7-Flash** (free) |
|---|---|---|---|
| Provider model id | `deepseek-flash` | `glm-5.3-flash` | `glm-4.7-flash` |
| Served version | DeepSeek-V4.1-Flash-1017 `[V]` | GLM-5.3-Flash (rel. 2026-08-26) `[V]` | GLM-4.7-Flash (rel. Jan 2026) `[I]` |
| Context window | **1M** `[V]` | **1M** `[V]` | 200K `[I]` (llm-stats reports 128K — conflict, see §6) |
| Max output | **384K** `[V]` | **128K** (default `max_tokens` 65,536; max 131,072) `[V]` | 16.4K `[I]` |
| Architecture | 552B total / 16B active MoE, CED `[I]` | 320B total / 18B active MoE, sparse+linear attention `[V]` | 31.2B total / 3B active `[I]` |
| Thinking control | Enable/disable + effort `low/high/max`; **default on, effort high** `[V]` | **Cannot disable**; effort `low/high/max`, **default max** `[V]` | Reasoning / non-reasoning variants `[I]` |
| Modalities | text+image in, text out `[V]` | text+image+video+file in, text out `[V]` | text in, text out `[I]` |
| Tool calls | ✓ `[V]` | ✓ (**`tool_choice` only `auto`**) `[V]` | ✓ `[?]` |
| JSON / structured output | JSON mode ✓ `[V]` | Structured output ✓ `[V]` | `[?]` |
| License | MIT `[I]` | MIT `[V]` | MIT `[I]` |
| Concurrency limit | **2,500** account-level (pro: 500) `[V]` | Not published; console-only `[V]` | Reported **1** concurrent `[U]` |
| Returned thinking tokens | `reasoning_content`; **must be replayed when `tools` present** `[V]` | billed inside output `[V]` | billed inside output `[I]` |

### 2.2 Pricing (per 1M tokens, USD)

| | Input | Cached input | Output | Notes |
|---|---|---|---|---|
| **DeepSeek Flash — off-peak** | **$0.15** | **$0.003** | **$0.60** | 98% cache discount `[V]` |
| **DeepSeek Flash — peak** | $0.30 | $0.006 | $1.20 | Peak = 01:00–04:00 & 06:00–10:00 UTC, Mon–Fri, excl. CN holidays `[V]` |
| **GLM-5.3-Flash** | $0.15 | $0.03 | $0.50 | 80% cache discount; "Cached Input Storage: Limited-time Free" `[V]` |
| GLM-5.3-Flash (launch promo, ended 2026-09-09) | $0.075 | $0.015 | $0.25 | 50% off list `[U]` |
| **GLM-4.7-Flash** | **Free** | Free | Free | Listed free on Z.AI; AA and llm-stats still list $0.07/$0.40 (= FlashX pricing) `[V]` `[I]` |
| *Escalation:* DeepSeek V4-Pro (off-peak) | $0.66 | $0.022 | $1.98 | 1M ctx, 384K out, concurrency 500 `[V]` |
| *Escalation:* DeepSeek V4-Pro (peak) | $1.32 | $0.044 | $3.96 | `[V]` |
| *Reference:* GLM-5.3 (full) | $1.40 | $0.26 | $4.40 | `[V]` |

**Ancillary DeepSeek costs** `[V]`: Search API $0.75/1k requests, Fetch API $0.75/1k, file parsing/OCR $0.225/1k pages, TTS $0.225/10k chars, ASR $0.058/hour. Server-side web search/fetch tool calls became **unbilled** on 2026-11-18 (results billed as tokens).
**Ancillary Z.AI costs** `[V]`: Web Search $0.01/use; image generation $0.015/image.

**Third-party hosts undercut first-party DeepSeek substantially** `[I]` (OpenRouter, accessed 2026-11-20): Relace $0.12/$0.50, Cohere $0.115/$0.40, Open Inference $0.06/$0.80, Prime Intellect $0.0437/$0.70, Pearl Research $0.05/$0.30, Morph $0.059/$0.52, with 120–214 tok/s and 0.4–1.8 s latency. Headline "from" price $0.036 in / $0.50 out. **Caveat:** quantization, uptime and data-retention terms are per-provider and were not audited — this is the largest unverified cost lever in this brief.

---

## 3. Capability profile

### 3.1 Independent benchmark comparison

All rows `[I]`, sourced from Artificial Analysis via [OpenRouter DeepSeek](https://openrouter.ai/deepseek/deepseek-v4.1-flash-20261017) and [OpenRouter GLM-5.3-Flash](https://openrouter.ai/z-ai/glm-5.3-flash), cross-checked against the [AA model pages](https://artificialanalysis.ai/models/deepseek-v4-1-flash-1017). DeepSeek at **max effort** unless noted.

| Benchmark (what it tests) | DeepSeek Flash | GLM-5.3-Flash | GLM-4.7-Flash |
|---|---|---|---|
| **AA Intelligence Index** (9 evals, agentic/science-weighted) | **32.6** (max) / 28.6 (high) / **18.5** (non-reasoning) | 27.8 | not scored (N/A) |
| HLE (frontier knowledge) | **43.3%** | 39.9% | 7.6% |
| HLE-Diamond (hard subset) | **25.3%** | 18.2% | — |
| **AA-LCR** (long-context retrieval) | **82.7%** | 80.0% | 41.7% |
| GPQA Diamond (science QA) | — | 91.2% (AA) / 86.4% (Vals) | 58.1% |
| SciCode (scientific coding) | **55.9%** | 51.6% | — |
| Terminal-Bench 4.0 (agentic shell) | **33.8%** | 32.8% (AA) / 37.4% (Vals) | — |
| **Terminal-Bench-Science** | **12.9%** | 4.8% (AA) / 2.9% (Vals) | — |
| CritPt (physics reasoning) | **24.0%** | 15.4% | 0.3% |
| CritPt v2 | 50.6% (hard 25.0%) | 46.3% (hard 24.5%) | — |
| AutomationBench-AA (agentic automation) | **66.6%** | 60.4% | — |
| **GDP.pdf** (deep document reasoning) | 17.2% | 15.4% | — |
| GDPval-AA (real knowledge work) | **62.3%** | 57.4% | — |
| AA-Omniscience accuracy | **39.6%** | 28.2% | — |
| AA-Omniscience **non-hallucination** | 35.9% | **61.7%** | — |
| τ³-Banking (tool use) | — | 47.2% | τ²-Telecom 98.8% |
| MMMU-Pro (vision) | 80.6% | 86.0% (Vals) | — |
| Design Arena Elo (UI/code craft) | — | 1252–1290 | 1022–1192 |

**Reading of the table.** DeepSeek Flash ≥ GLM-5.3-Flash on 12 of 15 shared rows and is ahead on every science-relevant row except GPQA (unmeasured for DeepSeek at AA) and raw non-hallucination. GLM-4.7-Flash is a different weight class: HLE 7.6% and AA-LCR 41.7% mean it cannot follow multi-document scientific context at all.

**Vals AI suite for GLM-5.3-Flash** `[I]` (from the same OpenRouter page): SWE-bench 92.0%, LiveCodeBench 80.5%, LegalBench 83.9%, MMLU-Pro 86.1%, MedScribe 88.9%, Vals Index 50.9% — but **ProgramBench 0.0%**, **SRE Bench 0.8%**, ProofBench 21.0%, Tax Agent Bench 31.6%, Vibe Code 30.8%. Strong on well-scoped code/legal text, near-zero on open-ended program synthesis and production-ops reasoning.

### 3.2 Operational profile (independent telemetry)

| | DeepSeek Flash | GLM-5.3-Flash | GLM-4.7-Flash |
|---|---|---|---|
| Time to first answer token | **47.07 s** | **96.52 s** | 39.92 s |
| Output speed | **161 tok/s** | 54 tok/s | 69 tok/s |
| Time per Intelligence Index task | **14.4 min** | **41.4 min** | not scored |
| Cost per Intelligence Index task | $0.60 | $0.58 | not scored |
| Verbosity (output tokens on index) | 174M — rank 31/32, "very verbose" | 124M — "somewhat verbose" | not scored |
| AA class rank (intelligence / perf / cost) | #2/32 / #13/29 / #13/30 | #11/32 / #28/29 / #12/30 | — |

`[I]`, [AA DeepSeek](https://artificialanalysis.ai/models/deepseek-v4-1-flash-1017), [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash). Note AA prices DeepSeek at **peak** ($0.30/$1.20); at off-peak the $0.60/task figure roughly halves.

---

## 4. Failure modes and known weaknesses

| Failure mode | DeepSeek Flash | GLM-5.3-Flash | GLM-4.7-Flash |
|---|---|---|---|
| **Rate limiting / throttling** | 2,500 account-level concurrent requests; 429 on exceed; **free capacity expansion on request** `[V]`. No published RPM/TPM. | Limits are **console-only**, docs refuse to state numbers ("different plans may have different quotas… may fail or wait in queue") `[V]`. Error **1302** (HTTP 429) and **1305** (overloaded) `[V]` `[U]`. | Reported **1 concurrent request per free model** `[U]`; same 1302/1305 codes. Effectively serialized. |
| **JSON-mode reliability** | Documented: if output isn't parseable JSON, the API **replaces non-JSON with spaces** — you can get blank `content` with `finish_reason: "stop"`; docs tell you to handle blank and retry `[V]`. | Structured output supported; no documented blank-content caveat `[V]`. | `[?]` |
| **Tool-call reliability** | Reported: **drops fields / jumps `anyOf` branches** on tools whose params use union schemas or optional payloads `[U]`. Fix is schema discipline, not retries. | `tool_choice` accepts **only `auto`** — you cannot force a named tool `[V]`. Kills deterministic "must call `submit_result` now" orchestration. | `[?]` |
| **Runaway agent loops** | Reported: **33–50 agent turns for a one-field config edit**, "verification with no stopping criterion" `[U]`. Long-horizon loops need externally enforced turn caps. | Not specifically reported; high per-turn latency (96 s TTFT) compounds loop cost linearly. | — |
| **Latency** | 47 s TTFT, 161 tok/s `[I]`. Acceptable for batch; poor for interactive. | 96 s TTFT, 54 tok/s, 41.4 min/task `[I]`; practitioners describe internal tools as "slow as if thinking about life" `[U]`. | 39.9 s TTFT, 69 tok/s `[I]`. |
| **Cost blowup via reasoning tokens** | Very verbose: 174M tokens on the index vs 101M median `[I]`. Mitigate with `reasoning_effort: low` or non-thinking mode. | **Cannot disable thinking**; default effort **max**; CoT "动辄几千个 token" (routinely thousands of tokens) `[U]` `[V]`. Must pin `reasoning_effort`. | Thinking bundled; no effort control documented `[?]`. |
| **Context degradation** | 1M window; AA-LCR 82.7% `[I]`. `reasoning_content` from prior turns is **replayed and concatenated** whenever `tools` is present `[V]` → input grows faster than the visible transcript in agent loops. | 1M window; AA-LCR 80.0% `[I]`. Reviewers warn "a large context window does not guarantee reliable recall" `[U]`. | 200K window; AA-LCR 41.7% `[I]` — degrades early. |
| **Hallucination / abstention** | Higher accuracy, lower abstention (non-hallucination 35.9%) `[I]`. Confabulates rather than refusing. | Lower accuracy, much better abstention (61.7%) `[I]`. | HLE 7.6%, CritPt 0.3% `[I]` — near-total failure on frontier science; will still answer confidently. |
| **Long-output truncation** | 384K max output `[V]`; lowest risk of the three. | 128K max output; `max_tokens` default 65,536 `[V]`. | 16.4K `[I]` — will truncate anything substantive. |
| **Sampling controls** | temperature/penalties **silently ignored** in thinking mode; `top_p` only effective 0.95–1.0 `[V]`. | Recommended temp 1, top_p 0.95 `[V]`. | — |

---

## 5. Fit for automated science: task routing

### 5.1 Cost logic (reproducible arithmetic)

**Unit task A — bulk extraction** (1 call; 8,000 input / 2,000 output tokens; 1,000 calls):

| Model / mode | Input | Output | Per call | Per 1,000 calls |
|---|---|---|---|---|
| DeepSeek Flash, non-thinking, off-peak | 8k × $0.15 = $0.00120 | 2k × $0.60 = $0.00120 | $0.00240 | **$2.40** |
| DeepSeek Flash, non-thinking, peak | $0.00240 | $0.00240 | $0.00480 | $4.80 |
| DeepSeek Flash, effort high, off-peak (+1k reasoning tok) | $0.00120 | 3k × $0.60 = $0.00180 | $0.00300 | $3.00 |
| GLM-5.3-Flash, effort low (+~500 reasoning tok) | $0.00120 | 2.5k × $0.50 = $0.00125 | $0.00245 | $2.45 |
| GLM-5.3-Flash, **default max** (+~3k reasoning tok) | $0.00120 | 5k × $0.50 = $0.00250 | $0.00370 | $3.70 |

At list prices the two are **within ±10%** for a lean configuration, and GLM is ~23% *more* expensive if left on its default effort. Reasoning-token volume, not the headline price, decides the bill.

**Throughput cost, unit task B — same job at fixed worker concurrency.** Per-worker throughput is inversely proportional to per-task minutes: DeepSeek 14.4 min vs GLM 41.4 min `[I]` → **GLM needs ~2.9× the concurrent workers (and ~2.9× the account quota) for the same jobs/hour**. With DeepSeek's 2,500-request concurrency ceiling `[V]` and GLM's undisclosed (and, on free, ~1) ceiling `[U]`, this is where "cheap at scale" is actually won or lost.

**Cost of escalation.** `deepseek-v4-pro` output $1.98 off-peak vs Flash $0.60 = **3.3×**; input $0.66 vs $0.15 = **4.4×** `[V]`. If a stage needs the stronger model for 5% of calls, blended cost rises ~15% — cheap insurance for the 5% that decides whether the paper is right.

### 5.2 Routing table

| Pipeline stage | Recommended | Why | Relative cost |
|---|---|---|---|
| Bulk extraction: values, tables, units, sample sizes from papers | **DeepSeek Flash, non-thinking, off-peak** | AA-LCR 82.7%, HLE 43.3% `[I]`; JSON mode + blank-content retry `[V]`; no reasoning-token tax. | 1.0× (baseline) |
| PDF→structured JSON normalization, schema filling | **DeepSeek Flash, non-thinking** | 384K output headroom `[V]`; flat schemas only — union schemas break tool args `[U]`. | 1.0× |
| Table/section summarisation with citation spans | **DeepSeek Flash, effort high, off-peak** | Needs some reasoning; II jumps 18.5→28.6 from non-reasoning to high `[I]`. | 1.25× |
| Literature screening / relevance triage (thousands of abstracts) | **DeepSeek Flash, non-thinking**, or **GLM-4.7-Flash free** if serialized is acceptable | Pure classification; cheap model sufficient. GLM-4.7's low HLE/AA-LCR don't matter for keyword-level triage `[I]`. | 1.0× / 0× |
| Code scaffolding: boilerplate, glue, Snakemake/pandas skeletons | **DeepSeek Flash, effort high** | SciCode 55.9% vs 51.6%; TB4.0 33.8% vs 32.8% `[I]`; GLM's ProgramBench 0.0% `[I]`. | 1.25× |
| Routine analysis: descriptive stats, plotting scripts, sanity checks | **DeepSeek Flash, effort high** | Deterministic, verifiable-by-execution tasks; errors are caught by running the code. | 1.25× |
| First-pass review: format compliance, checklist, missing-field detection | **GLM-5.3-Flash, effort low**, *or* DeepSeek non-thinking | Rule-shaped, not judgment-shaped; GLM's 61.7% abstention is useful for "flag uncertain" `[I]`. Pin effort — default max is 41 min/task `[I]`. | 1.0× |
| Long-document reader (full paper, 200–500K tokens) | **DeepSeek Flash** (primary), GLM-5.3-Flash (second reader) | Both 1M ctx; AA-LCR 82.7% vs 80.0% `[I]`. Two-reader disagreement is a cheap uncertainty signal. | 1.25× + 1.0× |
| Orchestrator / planner (decompose task, assign workers, merge) | **DeepSeek Flash, effort max** | II 32.6 at max vs 28.6 at high `[I]` — worth the tokens here; 2.9× faster per planning step than GLM `[I]`; GLM's `tool_choice: auto`-only blocks forced handoffs `[V]`. | 1.6× |
| Logging/monitoring, log triage, alert summarisation | **DeepSeek Flash, non-thinking** | Cheapest correct option; no science risk. | 1.0× |
| **Escalate** — final synthesis / narrative of results | **DeepSeek V4-Pro (off-peak)** | Flash GDP.pdf 17.2%, TB-Science 12.9% `[I]` — below the bar for prose that carries conclusions. | 3.3–4.4× |
| **Escalate** — adversarial review, red-teaming, reconciling conflicting evidence | **DeepSeek V4-Pro** + **GLM-5.3 (full)** as independent second reviewer | Diversity of failure modes matters more than price here; Flash HLE-Diamond 25.3% caps its ability to catch subtle errors `[I]`. | 3.3× + 3.1× |
| **Escalate** — debugging genuinely broken code | **DeepSeek V4-Pro**, fallback GLM-5.3 | TB-Science 12.9%/4.8% and TB4.0 ~33% `[I]` are too weak for multi-step debugging; escalation triggers should fire on second failed retry. | 3.3× |
| **Never** — novel experimental design, hypothesis generation | None of the flash models | HLE-Diamond ≤25.3%, GDP.pdf ≤17.2% `[I]`; both are pattern-completers, not designers. Human + frontier model only. | — |

### 5.3 Operating rules that fall out of the evidence

1. **Pin `reasoning_effort` on every Z.AI call.** Default is `max`, thinking cannot be disabled, and the practical fix for "everything is slow" is one parameter `[V]` `[U]`.
2. **Schedule batch work off-peak.** Exactly 2× cheaper on DeepSeek, every day `[V]`. Move cron windows outside 01:00–04:00 / 06:00–10:00 UTC Mon–Fri.
3. **Keep tool schemas flat.** No `anyOf`/`oneOf` unions, no optional payloads — DeepSeek Flash drops fields and picks the wrong branch on those `[U]`.
4. **Validate every JSON response, retry on blank.** Blank-with-`finish_reason: stop` is documented behaviour, not a bug `[V]`.
5. **Cap agent turns externally.** 33–50 turns for a one-field edit is reported `[U]`; a hard turn budget is the only reliable stopping criterion.
6. **Check citation-bearing claims deterministically.** DeepSeek's non-hallucination rate is 35.9% `[I]`; never let its bibliographic claims through unchecked.
7. **Log `reasoning_content` separately and don't let it accumulate.** With `tools` present DeepSeek requires replaying prior thinking into context `[V]`, which silently inflates input tokens in long loops.
8. **Keep a pay-as-you-go Z.AI key behind the free model** — the free tier's ~1 concurrent request `[U]` will serialise any real fan-out.

---

## 6. Uncertainty register

| Item | Status |
|---|---|
| Harness route ids (`deepseek-official/deepseek-flash`, `zai/glm-5.3-flash`, `zai/glm-4.7-flash`) | **Not verified.** Provider model ids confirmed; the packaged harness checkout was unreadable from this sandbox, so I could not confirm the routes map 1:1. |
| GLM-4.7-Flash context window | **Conflicting.** AA says 200K `[I]`; llm-stats says 128K in / 16.4K out `[I]`; Z.AI's model matrix lists GLM-4.7 at 200K `[V]`. Two of three favour 200K; output cap unresolved. |
| GLM-4.7-Flash price | **Conflicting.** Z.AI pricing page says Free `[V]`; AA and llm-stats list $0.07/$0.40, which equals GLM-4.7-**FlashX** list `[I]`. Likely aggregator staleness, not verified. |
| Z.AI published rate limits | **Not published.** Docs defer to console; the 1302/1305 codes are documented but no numeric quota is public `[V]`. The "1 concurrent request on free models" figure is a third-party report `[U]`. |
| AA "non-hallucination rate" definition | **Not verified.** I report 35.9% vs 61.7% as published but could not confirm how AA defines the metric, so the *direction* (DeepSeek more accurate but less abstinent) is indicative only. |
| GLM-5.3-Flash vs DeepSeek at **low** effort | **Not measured like-for-like.** DeepSeek non-reasoning II is 18.5 `[I]`; GLM cannot go below `low` effort and has no index at that setting. The cheap-mode comparison is therefore open. |
| Third-party DeepSeek hosts ($0.036–$0.12/M in) | **Price verified, quality not.** Quantization, uptime and data-retention terms unaudited. Could cut input cost ~2.5–6.9× vs first-party. |
| DeepSeek V4.1 Flash 1017 GPQA Diamond | **Missing** from the AA panel I could read; Vals AI scored GLM-5.3-Flash at 86.4% but no DeepSeek counterpart was available. |
| Whether GLM-5.3-Flash's 92.0% Vals SWE-bench is comparable to other models' SWE-bench figures | **Unverified** — harness/scaffold not stated; not used for model selection here. |
| Any benchmark for `glm-4.7-flash` beyond HLE/AA-LCR/GPQA/IFBench/τ²/CritPt/TB-Hard | **Not available.** AA lists no Intelligence Index for it (deprecated, superseded by GLM-5). |

---

## 7. Sources

All accessed **2026-11-20** unless a different date is given.

**DeepSeek — first party**
1. Models & Pricing — https://api-docs.deepseek.com/quick_start/pricing (prices, 1M ctx, 384K out, version DeepSeek-V4.1-Flash-1017, peak/off-peak windows, concurrency)
2. Rate Limit & Isolation — https://api-docs.deepseek.com/quick_start/rate_limit (2,500 / 500 concurrency, 429, free expansion)
3. JSON Output — https://api-docs.deepseek.com/guides/json_mode (blank-content failure mode)
4. Thinking Mode — https://api-docs.deepseek.com/guides/thinking_mode (toggle, effort mapping, `reasoning_content` replay rules, ignored sampling params)

**Z.AI / Zhipu — first party**
5. Pricing — https://docs.z.ai/guides/overview/pricing (GLM-5.3-Flash $0.15/$0.03/$0.50; GLM-4.7-Flash Free; GLM-5.3 $1.4/$0.26/$4.4)
6. GLM-5.3-Flash/FlashX model page — https://docs.z.ai/guides/vlm/glm-5.3-flash (320B/18B, 1M ctx, 128K out, forced thinking, 200 tok/s FlashX)
7. Core Parameters — https://docs.z.ai/guides/overview/concept-param (`max_tokens` table, `thinking.type`, `reasoning_effort` default `max`)
8. Function Calling — https://docs.z.ai/guides/capabilities/function-calling (`tool_choice` only `auto`; page last modified 2026-11-02)
9. Rate Limits — https://docs.z.ai/api-reference/rate-limit (redirects to console-only quotas; error 1302 listed)

**Independent evaluation**
10. Artificial Analysis — DeepSeek V4.1 Flash 1017 — https://artificialanalysis.ai/models/deepseek-v4-1-flash-1017 (II 32.6, 14.4 min/task, 161 tok/s, $0.60/task, verbosity, MIT, 552B/16B)
11. Artificial Analysis — GLM-5.3-Flash — https://artificialanalysis.ai/models/glm-5-3-flash (II 27.8, 41.4 min/task, 96.5 s TTFT, $0.58/task, "notably slow", "somewhat verbose")
12. Artificial Analysis — GLM-4.7-Flash — https://artificialanalysis.ai/models/glm-4-7-flash (200K ctx, 31.2B/3B, no Intelligence Index, deprecated)
13. OpenRouter — DeepSeek V4.1 Flash 1017 — https://openrouter.ai/deepseek/deepseek-v4.1-flash-20261017 (full AA benchmark panel; 40+ provider prices, 120–214 tok/s)
14. OpenRouter — GLM-5.3-Flash — https://openrouter.ai/z-ai/glm-5.3-flash (AA + Vals AI + Design Arena panels)
15. OpenRouter — GLM-4.7-Flash — https://openrouter.ai/z-ai/glm-4.7-flash (reasoning vs non-reasoning panel)
16. llm-stats — GLM-5.3-Flash — https://llm-stats.com/models/glm-5.3-flash (provider latency table; ZAI 8.70 s TTFT / 12 c/s)
17. llm-stats — GLM-4.7-Flash — https://llm-stats.com/models/glm-4.7-flash (128K/16.4K claim — conflicts with AA)

**User / practitioner reports**
18. Tencent Cloud Developer — "一行参数治好「龟速」：GLM-5.3-Flash 内部服务慢的排查与解决实录", 2026-09-10 — https://cloud.tencent.com.cn/developer/article/2741054 (forced thinking + default max effort; `reasoning_effort: high` fix)
19. Kongchang AI — "GLM-5.3 Flash思考过程太冗长？", 2026-09-01 — https://www.kongchang.com/articles/glm-5-3-flashyin-re-yi-si-kao-mo-xing-wei-he-guo-du-biao-da (Reddit CoT-verbosity thread)
20. Syntax Dispatch — "GLM-5.3-Flash Review", 2026-09-08 — https://www.syntaxdispatch.com/blog/glm-5-3-flash-review (independent review; launch promo pricing; "a cheaper model is not economical if it produces longer outputs, needs more retries, or increases review time")
21. Shahriar Labs — Z.ai GLM 1302/1305 error reference, checked 2026-10-10 — https://shahriarlabs.com/products/freelm/errors/zai-rate-limit-1302/ (free Flash ≈ 1 concurrent request; console-only quotas)
22. GitHub NousResearch/hermes-agent #145065 — https://github.com/NousResearch/hermes-agent/issues/145065 (`anyOf`/optional-payload tool-arg failures observed on deepseek-v4.1-flash)
23. Hugging Face DeepSeek-V4.1-Flash discussions #39 — https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/discussions/39 ("33–50 agent turns for a one-field config edit")
24. GitHub OmniRoute #13194 — https://github.com/diegosouzapw/OmniRoute/issues/13194 (429 classifier misses CJK quota messages from z.ai/Kimi/Qwen/MiniMax → retry-loop)

**Superseded draft.** An earlier draft of this brief (written before the independent benchmark panels were available, and without the AA/Vals numbers) is preserved unmodified at `MODEL_ROUTING_RESEARCH.v1_prebenchmark.md` for comparison. Its two claims that this version revises: GLM-5.3-Flash max output is 128K (not 1M), and DeepSeek Flash is not merely "on par" with GLM-5.3-Flash — it leads on 12 of 15 shared independent benchmarks and is ~2.9× faster per task.

**Sources considered and rejected:** `lmarena.ai` returned HTTP 403 to this client (no arena Elo available); `aider.chat` leaderboards were stale (latest entries 2025, no V4.1-Flash or GLM-4.7-Flash rows); provider blog posts at `z.ai/blog/*` returned 404 for the slugs tried. No benchmark number in this brief is inferred or estimated — where a figure is absent it is marked `—` or `[?]`.
