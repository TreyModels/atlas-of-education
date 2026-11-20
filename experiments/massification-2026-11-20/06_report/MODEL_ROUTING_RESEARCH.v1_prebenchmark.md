# Model routing brief — DeepSeek Flash vs GLM Flash for a cheap automated science workbench

**Date:** 2026-11-20 · **Prepared for:** Trey Menefee · **Purpose:** decide which model runs which stage of a
multi-agent research pipeline where **cost per completed task matters more than peak capability**.
**Verification:** vendor pricing pages fetched and quoted (URLs + access date below). Benchmarks are **not**
reproduced here; capability claims are labelled vendor/third-party/unverified. Prices change fast.

## Executive summary

1. **Both are genuinely cheap tiers**: DeepSeek `deepseek-flash` and Z.AI `glm-5.3-flash` list at about
   **$0.15 per 1M input** tokens; output is **$0.50–$0.60 per 1M**. At these prices the model choice is rarely
   the budget driver — retries, context bloat and human correction dominate.
2. **DeepSeek Flash has the better cache economics for agent loops**: cached input **$0.003/M** vs GLM's
   **$0.03/M** (10×). Multi-turn agents resend the same system prompt/tool schema/repo context constantly, so
   this is the single biggest structural cost difference.
3. **GLM-5.3-Flash is cheaper on output** ($0.50 vs $0.60/M) and is **natively multimodal** with a 1M context
   window; DeepSeek Flash is also 1M context, 384K max output, and supports vision.
4. **DeepSeek's built-in Search & Fetch API is a real differentiator for research agents**: server-side web
   search/fetch tools are integrated and token-billed (search API list $0.75/1k requests; server-side tool
   calls no longer separately billed as of 2026-11-18). This matches the user's practical experience that
   **DeepSeek is more reliable at web search**; treat that as a strong prior, not a benchmark result.
5. **DeepSeek peak pricing doubles** (input $0.30/M, output $1.20/M) on weekday peak hours (01:00–04:00 and
   06:00–10:00 UTC, Mon–Fri). GLM Flash has no comparable peak multiplier documented here; **during DeepSeek
   peak, GLM Flash can be the cheaper option**.
6. **Do not expect a universal capability winner at the Flash tier.** A third-party comparison of the larger
   siblings (DeepSeek V4 Pro vs GLM-5.3) found GLM leading several long-horizon software-engineering and
   agentic evals while DeepSeek did better on some repository/tool-use tests — no universal winner, and
   completed-task cost depends on retries and correction time.
7. **Practical routing for the workbench:** DeepSeek Flash = default worker/orchestrator (tool calls, web
   research, code-run loops, long-context with cache reuse); GLM-5.3-Flash = cheap output-heavy generation,
   image/multimodal inputs, and a fallback during DeepSeek peak; GLM-4.7-Flash (free tier per harness config)
   = trivial bulk tasks *only if* quality is verified on a sample; DeepSeek V4 Pro = escalation for hard
   debugging, adversarial review and final synthesis.
8. **Cheapest real lever is task design, not model choice**: short system prompts, stable prefixes (cache
   hits), bounded outputs, deterministic scripts for anything that can be computed instead of generated, and
   escalating only the ~10–20% of turns that genuinely need a stronger model.

## Specs and pricing (verified from vendor pages, accessed 2026-11-20)

| | **DeepSeek Flash** (`deepseek-flash`) | **GLM-5.3-Flash** (`glm-5.3-flash`) |
|---|---|---|
| Vendor / version | DeepSeek-V4.1-Flash-1017 | ZAI GLM-5.3-Flash (released Aug 2026; MIT license) |
| Context | **1M** | **1M** |
| Max output | **384K** | 1M per llm-stats provider table (131.1K on some providers) |
| Input $/1M | **$0.15** cache-miss, **$0.003** cache-hit (off-peak; peak doubles) | **$0.15**, cached **$0.03** |
| Output $/1M | **$0.60** off-peak; $1.20 peak | **$0.50** |
| Peak pricing | Yes — peak input $0.30 / output $1.20 | Not documented on the pages fetched |
| Multimodal | Vision ✓ (plus JSON, tool calls, Responses & Anthropic APIs, prefix & FIM) | Native multimodal input (text/image/video), text out |
| Search/fetch | **Built-in Search & Fetch API** (server-side tools; $0.75/1k requests list; server-side tool calls token-billed, not separately billed since 2026-11-18) | Not documented on the pages fetched (check Z.AI docs) |
| Concurrency | 2,500 (Flash) | Provider-dependent |
| Speed (third-party) | Not fetched | p95 latency **2.18 s**, throughput **69 char/s** (DeepInfra/FriendliAI); ZAI direct TTFT 8.70 s / 12 char/s |
| Free tier | — | `glm-4.7-flash` listed as free in the harness provider config (verify quality before relying) |

**Sources:** DeepSeek Models & Pricing — https://api-docs.deepseek.com/quick_start/pricing (accessed 2026-11-20);
LLM Stats GLM-5.3-Flash — https://llm-stats.com/models/glm-5.3-flash (accessed 2026-11-20); Z.AI pricing page
(JS-rendered; not machine-read) — https://open.bigmodel.cn/pricing; SiliconFlow comparison — 
https://www.siliconflow.com/id/blog/deepseek-v4-vs-glm-5-3 (17 Sep 2026). **Unverified** items are marked above.

## Cost math (illustrative; 20k input + 2k output per call, 50 calls per stage)

| | DeepSeek Flash off-peak | DeepSeek Flash peak | GLM-5.3-Flash |
|---|---|---|---|
| Input | $0.15 | $0.30 | $0.15 |
| Output | $0.06 | $0.12 | $0.05 |
| **Total/stage** | **≈$0.21** | **≈$0.42** | **≈$0.20** |

With **80% cache-hit input** (typical agent loop): DeepSeek ≈ **$0.03 + $0.06 = $0.09**/stage vs GLM ≈
$0.12 + $0.05 = **$0.17**/stage → **DeepSeek ~2× cheaper** in cache-heavy loops. With output-heavy generation
and little cache reuse, GLM is slightly cheaper. During DeepSeek peak, GLM wins unless cache hit rate is very high.

## Capability profile and known failure modes

| dimension | DeepSeek Flash | GLM-5.3-Flash (evidence) |
|---|---|---|
| Coding / repo work | Strong tool-calling and JSON support; large output budget (384K) | Vendor/third-party positioning emphasises long-horizon coding & agent execution; larger sibling GLM-5.3 leads several SWE/agent evals in the SiliconFlow comparison |
| Web research | **Built-in search/fetch tooling**, integrated billing; user reports better web-search behaviour | Web tooling not confirmed in fetched pages — **verify before routing web-heavy work** |
| Long context | 1M ctx; cache-friendly for repeated context | 1M ctx; third-party conversation-depth charts available on llm-stats |
| Multimodal | Vision supported | **Native multimodal input** (image/video) — stronger on paper |
| Reliability | Vendor API with 2.5k concurrency; **peak-hour price doubling** | Provider routing (DeepInfra/FriendliAI/Novita/ZAI) with variable TTFT/throughput; ZAI direct slower in third-party data |
| Cost risk | Peak hours double; unbounded retries expensive | Provider heterogeneity can affect latency/limits; free tier quality unverified |
| Hallucination/tool errors | Both are Flash-tier: expect tool-call reformatting errors, silent truncation on very long outputs, and weaker multi-step reasoning than Pro tiers. **Always validate structured outputs and re-run failed cells** | Same caveat |

## Task routing recommendation (cost-first)

| task class | recommended | why |
|---|---|---|
| Bulk extraction, table summarising, classification, log triage | **GLM-4.7-flash (free) or DeepSeek Flash** | low reasoning demand; verify a 20-sample quality gate before scaling free tier |
| Literature/source search, web-fetch-heavy research steps | **DeepSeek Flash** | built-in Search & Fetch API + user-reported reliability |
| Code scaffolding, routine Python analysis, plotting, file wrangling | **DeepSeek Flash** (or GLM-5.3-Flash) | both adequate; DeepSeek cache economics help long agent loops |
| Experiment design, adversarial review, conflicting-evidence reconciliation | **DeepSeek V4 Pro** (escalate) | Flash-tier misses subtle contradictions; cheap model here is false economy |
| Final synthesis / user-facing writing | **DeepSeek V4 Pro** or human-edited Flash draft | wording errors are expensive to correct downstream |
| Multimodal tasks (charts, scanned tables, images) | **GLM-5.3-Flash** (native multimodal) | native image/video input |
| Overflow/peak-hour work | **GLM-5.3-Flash** | DeepSeek peak doubles price |
| Monitoring/CI checks, mechanical reformatting | **deterministic scripts**, no LLM | cheapest and most reliable |

## Recommendation

**Default to DeepSeek Flash for research-agent work** (web search, code-run loops, long-context with stable
prefixes), **use GLM-5.3-Flash for output-heavy, multimodal, or DeepSeek-peak-hour work**, and **reserve
DeepSeek V4 Pro for the small set of judgment-heavy turns**. The user's prior that DeepSeek is better at web
search is consistent with the product design (integrated search/fetch) and should be treated as the default
until a head-to-head eval on this workbench's own tasks says otherwise.

## Suggested next evidence step

Run a small **paired task eval** (30 prompts: 10 search-and-cite, 10 code-run-and-report, 10 summarise-and-check)
on both models, scoring completion, factual error rate, tool-call validity, and wall-clock cost per completed
task. That converts this brief from vendor specs into a routing policy for this specific workbench.
