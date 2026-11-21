# v2 predeclaration — Yang-mapped factory/credential toy (BEFORE RUNNING)

**Status: ILLUSTRATIVE TOY — exploratory; not evidence; no calibration; no claims about any country.**
Corrects the inert Yang component of the v1 toy (`code/pathways_factory.cjs`) per the design fixes:

1. **Yang mapping made continuous.** Adopt Yang et al. (2026) `D(N) = 128·ln N + c` with c anchored so
   `D(10^6) = 500` (declared anchor; the paper's b=128 and R²=0.94 are adopted verbatim; no city data are read).
   Then define the **gated share** of the 12 factory posts as
   `g(N) = clip((D(N) − D(50k)) / (D(2m) − D(50k)), 0, 1)` — a declared, monotone mapping from occupational
   variety to credential gating. City sizes: 50k, 100k, 200k, 500k, 1m, 2m.
2. **Gate rule endogenised.** Four designs: `none` (q=0 gated posts), `all` (q=12), `yang` (q = round(12·g(N))),
   `yang_endog` (q starts at round(12·g(N)), then rises by 1 when applicants/post > 3, falls by 1 when
   applicants/post < 1; q ∈ [0,12]). Gated posts are the **top q** posts; a gated post requires 12 completed
   grades.
3. **Dynamic study rule.** Study value keeps the v1 static base and adds a **future term**:
   `studyValue = 0.9 + 0.8·school + 0.5·skill + (g<12 ? 0.45 : 0) + β·[p_dip·(g·factory + (1−g)·formal)
   + (1−p_dip)·informal − informal] − travel`, with β = 0.5, `p_dip = min(0.98, 0.70 + 0.20·skill)`,
   `factory = 2.3`, `formal = 2.0`, `informal = 1.4`, `farm = 1.0`.
4. **Travel cost and urban/rural split.** 50/50 arrivals; rural children bear `travel = 0.10 + 0.25·u`
   (u uniform via the toy's deterministic noise), urban 0.
5. **Grid:** 6 city sizes × 4 designs × 200 seeds; years 23–35 post-opening means; pre-shock y=20–22 must match
   across designs (same design-independent rule before y=23).

## Predeclared expectations and falsifier

- **Expectation:** `g(N)` rises from 0 (50k) to 1 (2m); therefore completion should rise and hires/leaving fall
  with city size under `yang`, relative to `none`, and `yang_endog` should raise q further where applicants/post
  is high (credential inflation).
- **Predeclared falsifier (the v1 failure repeated):** the Yang mapping counts as **ACTIVE** only if, for ≥3 of
  the 6 city sizes, the `yang` arm differs from `none` in mean secondary completion **or** mean leaving by
  ≥ 0.5 pp (toy units) over years 23–35. If fewer than 3 sizes move, record **INERT** and do not proceed.
- **Mini coexistence check (descriptive, no threshold):** report, by city size, unfilled posts (hires < 12) and
  applicants per gated post; note any cell where both are non-trivial (the coexistence the coevolution brief asks
  for).
- No tuning after results; all parameters declared above; failures reported. Deterministic; two runs must be
  byte-identical.

## Limits (declared)

The Yang law is an MSA fit for total occupation counts (hundreds); here it is used only to map a small local
slice (12 factory posts) of occupational variety into a gated share. The mapping g(N) is a declared link, not the
paper's estimate. The toy has no capacity, quality, commuting network, firm entry/exit, or learning; incomes are
illustrative units. Nothing here tests Yang's law; it tests whether a Yang-consistent gate margin changes the
toy's education outcomes.
