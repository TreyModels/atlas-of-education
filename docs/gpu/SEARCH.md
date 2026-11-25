# Gate-1 external prior-art search — top-K Plackett–Luce win probabilities, CPU + GPU

**Task:** `task-1` · **Author:** `prior-art` · **Date:** 2026-11-25
**Target hot path:** `engine/eduengine/contest_math.py` @ `e0508f3` (branch `research/gpu-port-2026-11-25`), `_quadrature_win_probs` (L342–L415).
**Scope:** *external* prior art only. In-repo / worktree prior art is `task-2`'s job (`docs/gpu/FEASIBILITY.md`).

---

## 1. Bottom line

**Recommendation: ADAPT + IMPLEMENT. REUSE is not available for this gate.**

1. **ADAPT** [`Knyazev & Oosterhuis 2026` (MPL), MIT, Zenodo `10.5281/zenodo.17352314`](https://zenodo.org/records/17352314) — the closest published artifact by a wide margin: it is a **batched PyTorch, GPU-capable, deterministic (quadrature, not Monte-Carlo) top-K Plackett–Luce placement-probability routine built on exactly the same Poisson-binomial/exponential-race integral** that our hot path uses, with the same prefix–suffix leave-one-out scheme. It is MIT, so we can legally lift `conv_stable` (the Poisson-binomial DC convolution) almost verbatim. It **cannot** satisfy the 1e-12 gate (it works in log-space with `logaddexp`; see §5).
2. **ADAPT** (as an independent numerical oracle, not as a hot path) [`Wolters 2026` (LAQI), MIT, `curesive/log-age-quadrature-icm`](https://github.com/curesive/log-age-quadrature-icm) — a released, MIT-licensed reference implementation of the same integral representation. It returns *equities only*, not individual placement probabilities, so it cannot validate P_i directly, but it is a clean second implementation to differential-test the maths against.
3. **IMPLEMENT** the bit-exact float32 kernel by hand. **No library in this search can meet max-abs-diff ≤ 1e-12 against the float32 CPU reference**, because that gate is not an accuracy gate — it is a *bit-reproduction* gate. The decisive fact is in §5: a reordered float32 implementation lands at ~1e-6–1e-5, i.e. **6–7 orders of magnitude above 1e-12**. Only a hand-written kernel that reproduces the reference's exact mul-then-add sequence, its sequential `cumsum`, and numpy's empirical `einsum` accumulation order can pass.

**The finding that most affects go/no-go:** the state of the art (DE-ICM, §3.2) reaches **1.1e-14 absolute placement-probability error** on the same mathematics with a **0.2 s CPU** full matrix at n=1000. That is roughly **2 orders of magnitude better accuracy and ~2 orders of magnitude less CPU time** than the current path, and it is *incompatible with the 1e-12 gate* precisely because it is accurate in float64. If the gate is meant to protect correctness, the published literature says the gate is testing the wrong thing; if the gate is meant to protect reproducibility, then it is a bit-emulation requirement and must be stated as such. **Recommend the human decide this explicitly before the port starts.**

---

## 2. Method

- GitHub REST API (`/repos`, `/license`, `/contents`, `/git/trees`) + `raw.githubusercontent.com` for licenses read off the actual repos; PyPI/CRAN/Zenodo APIs for package metadata.
- Web search for the required angles; HTML/PDF fetched with `curl` and text-extracted locally.
- **No rate-limiting was hit** (60 req/h unauthenticated; I used ~25). All license values below were read from the repo's own license file or registry metadata, not from memory. Where a repo has **no** detectably-licensed file this is called out explicitly — it is a legal blocker, not a stylistic note.
- Fetched page text was treated strictly as data.

---

## 3. Shortlist — the three artifacts that matter

### 3.1 MPL — Knyazev & Oosterhuis, ECIR 2026 ⭐ closest match

| | |
|---|---|
| URL | https://zenodo.org/records/17352314 (DOI `10.5281/zenodo.17352314`); paper https://link.springer.com/chapter/10.1007/978-3-032-21289-4_11 |
| Title | *Sample-Free Almost-Exact Estimation of Plackett-Luce Propensities for Off-Policy Ranking* |
| License | **MIT** (verified: Zenodo record `metadata.license.id = mit-license`; also stated in the repo README: "The contents of this repository are licensed under the MIT license") |
| Language / stack | Python, **PyTorch 2.7.1** (`mpl_env.yml`), CUDA channel in conda env; device-agnostic torch code (`logits.device`) ⇒ runs on GPU unmodified |
| Code size | 56 files; core file `mpl/mpl/mpl.py` (233 lines) |
| What it solves | `(batch_size, n_docs)` logits → `(batch_size, n_docs, K)` **top-K Plackett–Luce placement probabilities**, deterministic, no sampling |
| Exact or MC? | **Deterministic quadrature** (Gauss–Legendre), "almost-exact", not Monte-Carlo |
| Batched? | **Yes — first-class batch dimension**, plus batch across quadrature nodes (`lp.view(bs*N, n_docs)`) |
| Bit-exact vs our float32 ref? | **Fatal.** Log-space (`logaddexp`, `logsumexp`, `torch.cumsum`); on CUDA `torch.cumsum` is a *parallel scan* (different association), and `logsumexp`/`logaddexp` are composed differently from our `multiply`+`+=`. Expected gap ~1e-6 rel (single precision), i.e. ~1e6× the gate. |
| Verdict | **ADAPT.** Best structural template and a legal (MIT) source for the Poisson-binomial DC convolution. Cannot be the gate-passing path. |

What it actually does (read from `mpl/mpl/mpl.py`):

- Integration limits from Gumbel quantiles: `b = max(logits) - (-(1-l).log()).log()`, `a = min(logits) - (-l.log()).log()`, `l` a "standard Gumbel quantile" margin (L107–L112).
- Gaussian–Legendre nodes/weights from `np.polynomial.legendre.leggauss(N)` cast to the logits dtype (L100–L105) — **`N` quadrature nodes, `K-1` Poisson-binomial order**, compared with our 266 Simpson nodes and `d` = min(K−1, n−K−1).
- `lp = -exp(logits - x)` → `conv_stable(log_p, M=K-1)` computes the Poisson-binomial probabilities of "how many docs beat doc d at node x" via **forward/backward state arrays and a pairwise sum of products** (`abcd, edcb = lSk_padded[...,0], lSk_padded[...,1].flip(-2)`; `pairwise = abcd.unsqueeze(-1) + edcb.unsqueeze(-2)`; `logsumexp_diagonal`) — this is the **same prefix⋈suffix avoid-the-division trick** our code uses (`Pre` / `Suf[i+1][::-1]`), just in log space.
- It explicitly cites the **DC algorithm of Biscarri, Zhao & Brunner (2018)** (docstring, L152) — the same reference DE-ICM uses for its Poisson-binomial step.
- Rank-1 probability is special-cased to `logits.softmax(-1)` (L135).
- Cost per node `O(n K²)` (per DE-ICM Table 6), vs our `O(n·d·m)` total for the whole integral.

Performance datapoint (secondary, from DE-ICM §5.4): *"MPL reports about 2 ms per query for K=10 places with 200 nodes on a GPU in single precision."*

### 3.2 DE-ICM — Inariba, arXiv 2610.06028 (5 Oct 2026) ⭐ the algorithmic state of the art

| | |
|---|---|
| URL | https://arxiv.org/abs/2610.06028 (*Near-Exact Computation of Independent Chip Model Placement Probabilities for Thousands of Players*) |
| License / code | Paper: **CC BY 4.0** (arXiv). **Code: NOT RELEASED.** |
| Explicit statement | *"The implementation used in the paper is independent of the production code; neither is released."* (Reproducibility paragraph) |
| What it solves | Placement probabilities of **all n** players for **all** places, `O(M n²)`, deterministic |
| Exact or MC? | Deterministic quadrature — double-exponential (exp–exp) lattice, closed-form truncation bounds |
| Accuracy | worst observed equity rel. error **4.0e-14**, worst placement-probability abs. error **1.1e-14**, validated to **n = 4,000** |
| Runtime | **0.2 s** full matrix, n=1000, one CPU core (36.8 ms on 8 threads); 104.7 ms for m=0.15n places, one thread |
| GPU? | No. Cites MPL's GPU figure as the only GPU datapoint. |
| Bit-exact vs our float32 ref? | **No** — double precision, different scheme. Would differ from our float32 reference by *the reference's own float32 error*, ~1e-6, and fail the gate. |
| Verdict | **ADAPT (algorithmically), do not expect gate compatibility.** This is the paper that proves the current path is a 2026 re-derivation of a solved problem, and it dominates it on both axes. |

Why it matters here, in its own words: *"the same mathematics appears in other fields; for instance, the ICM is a Plackett-Luce ranking model with stacks as weights."* Our problem **is** the ICM placement-probability problem with `K` seats; `n≈300, K≈36–69` sits comfortably inside its validated range.

Three transferable tricks (all *incompatible* with bit-equality, all valuable if the gate is relaxed):
- **exp–exp (double-exponential) lattice** instead of composite Simpson in `u=log t`: far fewer nodes for the same truncation error, with **closed-form truncation bounds**. Our path needs `m≈266` nodes; DE-ICM's `M` is fixed per input class, e.g. `M=500` at n=100, `M=1000` at n=1000 (Table 5) — but its cost is `O(M n²)` with no `d` factor and no 22 MB suffix array.
- **`O(n)` stable leave-one-out deconvolution** (synthetic division / polynomial deflation, direction chosen by root modulus, with a clamp) instead of materialising a prefix and a suffix DP. This directly attacks the memory traffic that makes our path bandwidth-bound: DE-ICM §4.3 notes the cached prefix–suffix scheme costs `O(n m²)` per node, and that deconvolution "lowers its cost for the placement matrix with m ≳ √n". **Our `m=266 ≫ √300≈17`, so by DE-ICM's own analysis we are in the regime where deconvolution wins.**
- **Error budget derived from the instance**, instead of our fixed `h=0.1`, fixed `t_lo=1e-5`, fixed `C=14`.

### 3.3 LAQI — Wolters 2026 ⭐ the only released implementation

| | |
|---|---|
| URL | https://github.com/curesive/log-age-quadrature-icm · Zenodo (software, v1.0.0 per its CFF) |
| License | **MIT** (verified: `/repos/.../license` → `spdx_id = MIT`; repo `LICENSE` 1065 bytes) |
| Language | JavaScript (Node), MIT; ~1 star, but with a paper, CITATION.cff, provenance docs, tests and result JSONs |
| What it solves | **Equities** (expected prize) for poker ICM — the *same* integral representation, log-age Gauss–Legendre quadrature, 192 nodes / 32 panels |
| Exact or MC? | Deterministic quadrature |
| Returns placement probabilities? | **No — equities only.** Cannot validate P_i directly. |
| Batched? | No. Per-target loop, `O(n²·rank·nodes)`. |
| Bit-exact vs our float32 ref? | **No** — float64 JS, different quadrature, different integrand assembly. |
| Verdict | **ADAPT as oracle only.** Useful as a fully-released, MIT, independent implementation of the same mathematics to differential-test a new float32/float64 engine against. Not a hot path. |

Its core loop (`paper/log-age-quadrature-icm-snippet.js`) is the cleanest 100-line statement of the mathematics anywhere in this search:
`aheadProbability(rate, age) = 1 - exp(-rate*age)` → product-polynomial `distribution[k] = distribution[k]*(1-q) + distribution[k-1]*q` (leave-one-out Poisson-binomial) → integrate `λ_i exp(-λ_i y) · payout·distribution` over `y = exp(u)-1` with Gauss–Legendre nodes in `u`. Compare our `_quadrature_win_probs` L405–L415: same structure, `p_below = 1-expm1(-w t)`, same stay/inc DP, same `w_i exp(-w_i t)` density factor.

---

## 4. Candidate table

Legend — **bit-exact risk** is the risk of *failing the 1e-12 gate*, not the risk of being wrong: **fatal** = mathematically different arithmetic, cannot pass; **high** = would need op-by-op re-derivation; **n/a** = not a hot-path candidate.

| # | Artifact | URL | License (verified) | Lang/stack | Solves | Exact vs MC | Batched | Bit-exact risk | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **MPL** (Knyazev & Oosterhuis, ECIR 2026) | [zenodo 17352314](https://zenodo.org/records/17352314) | **MIT** | PyTorch 2.7, GPU | top-K PL placement probs (n_docs, K) | **deterministic quadrature** | **yes** (batch + node batch) | **fatal** (log-space; CUDA `cumsum` is a parallel scan) | **ADAPT** — template + MIT `conv_stable` |
| 2 | **DE-ICM** (Inariba 2026) | [arXiv 2610.06028](https://arxiv.org/abs/2610.06028) | paper CC BY 4.0; **code not released** | — | all placement probs, `O(Mn²)`, n≤4000 | deterministic, ~1e-14 | no (CPU) | **fatal** (float64, different scheme) | **ADAPT ideas only** |
| 3 | **LAQI** (Wolters 2026) | [curesive/log-age-quadrature-icm](https://github.com/curesive/log-age-quadrature-icm) | **MIT** | JavaScript | ICM **equities** (not places) | deterministic | no | **fatal** | **ADAPT as oracle** |
| 4 | choix (Maystre) | [lucasmaystre/choix](https://github.com/lucasmaystre/choix) | **MIT** | Python/NumPy | PL **model inference** (MM, EP, Bayesian) + samplers | inference on observed rankings | no | n/a | **no-fit** — no marginal top-K propensity routine; it fits weights, we already have weights |
| 5 | PlackettLuce (R) | [CRAN PlackettLuce 0.4.5](https://cran.r-project.org/package=PlackettLuce) | **GPL-3** | R | PL/BT model fitting (MM), rank aggregation | inference | no | n/a | **no-fit** — GPL-3 blocks linking; no marginals |
| 6 | torch-choice (Liang) | [yuxing-liang/torch-choice](https://github.com/yuxing-liang/torch-choice) | **NONE** — no `LICENSE` file in repo root (contents listing: only `.github .gitignore README.md docs docs_src mkdocs.yml requirements*.txt setup.py tests torch_choice tutorials`) | PyTorch | PL logit likelihood for **observed** choices | likelihood | yes | n/a | **blocked** — unlicensed ⇒ not legally reusable |
| 7 | TF-Ranking | [tensorflow/ranking](https://github.com/tensorflow/ranking) | **Apache-2.0** | TF | listwise losses incl. PL loss | likelihood of a given ranking | yes (TF GPU) | n/a | **no-fit** — needs the realised ranking; no marginal top-K |
| 8 | allRank | [allegro/allRank](https://github.com/allegro/allRank) | **Apache-2.0** | PyTorch | listwise PL / LambdaLoss training | likelihood | yes | n/a | **no-fit** — same reason |
| 9 | choice-learn | [artefactory/choice-learn](https://github.com/artefactory/choice-learn) | **MIT** | Python | discrete choice (logit / nested logit) | likelihood | partial | n/a | **no-fit** — not Plackett–Luce top-K |
| 10 | erdman/plackett-luce | [erdman/plackett-luce](https://github.com/erdman/plackett-luce) | **NONE** (API `/license` → 404; no LICENSE file) | Python | PL inference on NASCAR data | inference | no | n/a | **blocked / no-fit** |
| 11 | BayesPL (Guiver & Snelson) | [`guillaumegenthial/BayesPL`](https://github.com/guillaumegenthial/BayesPL) — **API 404 at queried path, NOT VERIFIED** | **unverified** | R | Bayesian PL | inference | no | n/a | **dropped** — could not confirm existence/licence in timebox; do not cite |
| 12 | pyPL | — | — | — | — | — | — | — | **dropped** — no maintained package found under that name in this search |
| 13 | Kool, van Hoof & Welling 2019 (perturb-and-max / Gumbel top-k) | [arXiv 1903.06059](https://arxiv.org/abs/1903.06059) | paper; no single canonical repo | — | exact **sampler** of PL without replacement via Gumbel top-k | **MC / sampling** | — | n/a | **no-fit for probabilities**; this *is* the published justification for `pl_realize` (L620–L672) |
| 14 | vLLM Gumbel-sampling kernel work | [vllm PR #29210](https://github.com/vllm-project/vllm/pull/29210) | **Apache-2.0** | CUDA/C++ | categorical Gumbel sampling for token decode | MC sampling | yes | n/a | **no-fit** — samples one categorical draw, does not produce top-K marginals |
| 15 | RAFT / cuML `select_k`, `topk` | [rapidsai/raft](https://github.com/rapidsai/raft) · [rapidsai/cuml](https://github.com/rapidsai/cuml) | **Apache-2.0** (verified from `LICENSE`) | CUDA | radix/bitonic top-k **selection** | exact selection | yes | n/a | **no-fit for the hot path**; possible building block for `pl_realize`'s argpartition (which is only O(n)) |
| 16 | Triton | [triton-lang/triton](https://github.com/triton-lang/triton) | **MIT** | Python DSL→PTX | kernel language | — | yes | **high** — Triton does not promise any FP reduction order; scans/reductions are its own | **tooling only** |
| 17 | JAXopt / jax | [google/jaxopt](https://github.com/google/jaxopt) | **Apache-2.0** | JAX | optimisation | — | yes | **high** — XLA reassociates reductions freely | **no-fit** |
| 18 | numba.cuda | [numba/numba](https://github.com/numba/numba) | **BSD-2-Clause** | Python→CUDA | raw CUDA kernel authoring | — | yes | **low — best option**, you own the exact op order | **ADAPT** as the implementation vehicle if a Python-native kernel is wanted |
| 19 | poibin / PoissonBinomial (R, Hong 2013) | https://cran.r-project.org/package=poibin | GPL | R | Poisson-binomial **PMF/CDF**, one item set | exact | no | n/a | **no-fit** — no per-item leave-one-out, no batch, no GPU |
| 20 | Biscarri, Zhao & Brunner 2018 (DC algorithm) | https://www.sciencedirect.com/science/article/pii/S0167947318300082 | paper | — | `O(n²)` Poisson-binomial DF, the algorithm behind MPL's `conv_stable` | exact | — | n/a | **cited by both MPL and DE-ICM**; this is the canonical Poisson-binomial reference |
| 21 | **ReproBLAS** (Demmel & Nguyen 2015) | https://www2.eecs.berkeley.edu/Pubs/TechRpts/2015/EECS-2015-229.pdf | (paper/tech report; repo BSD-style) | C++/MPI | **bit-reproducible** summation and BLAS | — | yes | **n/a by construction** — reproducibility *of its own* order | **no-fit**: gives a canonical order, *not* numpy's legacy order |
| 22 | **FPRev** (Xie et al. 2024) | https://arxiv.org/abs/2411.00442 · https://github.com/peichenxie/FPRev | repo (see URL) | Python | **reveals the accumulation order** of NumPy/PyTorch on CPU/GPU | diagnostic | — | — | **ADOPT — step 0 of the bit-exact port** |

---

## 5. Bit-exactness: why ≤1e-12 is a bit-reproduction problem, not an accuracy problem

This section is the crux of the whole gate and is grounded in the actual lines of `contest_math.py`.

### 5.1 Where the float32 actually is

The reference is **not** float32 end-to-end. float64 is used for all closed forms; only the DP storage and the two order-sensitive reductions are float32:

| Line | Op | Dtype | Order-sensitive? |
|---|---|---|---|
| L376–L378 | `p_below = (-np.expm1(-(wn*t))).astype(float32)`, `q_above = np.exp(-(wn*t)).astype(float32)` | float64 compute → **float32 cast** | **No** — double→float32 is a single correctly-rounded conversion; a GPU doing `exp` in double then casting gets the identical float32 value. A GPU doing `expf` in float32 gets a *different* value. **Rule: compute in double, cast once.** |
| L387–L389 | `Suf = np.empty((n+1, d+1, m+1), float32)`; `Suf[n,:,:]=0`, `Suf[n,0,:]=1` | **float32** | seed is exact |
| L390–L394 | `np.multiply(cur, f_stay[i], out=nxt)` then `nxt[1:] += f_inc[i]*cur[:-1]` | **float32 mul, then float32 add** | **YES — two separate roundings.** 300 sequential steps. |
| L397 | `np.cumsum(Suf, axis=1, out=Suf)` | **float32**, scan along `m+1 = 267` | **YES — sequential accumulation.** |
| L407 | `np.einsum("am,am->m", Pre, Suf[i+1][::-1])` | **float32**, 69-term reduction per `m` | **YES — and the order is an undocumented numpy implementation detail.** |
| L399–L402, L412–L414 | prefix DP `Pre`, same mul/add pattern | **float32** | YES (same as L390–L394) |
| L409–L410 | `kernel = wn[i]*t*q_above[i].astype(float64)`; `np.dot(sw, kernel*G)` | float64 (BLAS dot, 267 terms) | **NO at this gate** — float64 reorder error ~ε₆₄·√267 ≈ 1e-15, below 1e-12. |
| L192–L217, L537 | `_renormalize_to_seats` | float64 | No (1e-15 scale) |

So the gate reduces to **three** float32 order-sensitive sites: the **DP recurrence (L390–394, L412–413)**, the **`cumsum` (L397)**, and the **`einsum` (L407)**.

### 5.2 How far off a reordered implementation lands

For float32, `ε = 2⁻²⁴ ≈ 5.96e-8`.

- **DP recurrence:** ~300 sequential mul+add steps. Typical (random-walk) error ≈ `√300·ε ≈ 1.0e-6` relative; worst case ≈ `300·ε/2 ≈ 9e-6`.
- **`cumsum`:** 267-term sequential accumulation. Typical ≈ `√267·ε ≈ 1.0e-6`; worst ≈ `8e-6`.
- **`einsum`:** 69-term reduction. Typical ≈ `5e-7`.

`tail` feeds `G = clip(offset + sign*tail, 0, 1)` (L408), and `P[i] = dot(sw, kernel*G)` (L410) — **G's error passes through 1:1 into P_i**. A perturbed float32 path therefore produces

> **|ΔP| ~ 1e-6 to 1e-5, i.e. 10⁶–10⁷ × the 1e-12 gate.**

This is exactly the generic `ε₃₂·√n` estimate and it is confirmed by the repo's own audit (per `task-2`'s brief: re-association changed outputs by ≤1.4e-15 in *float64* experiments and was still reverted for not being bit-identical). **No amount of careful GPU programming closes a 10⁶ gap by improving accuracy — the only way is to reproduce the exact rounding sequence.** Note the corollary: an *accurate* reimplementation (float64, or the DE-ICM scheme) fails this gate **by definition**, because it differs from the float32 reference by the reference's own error.

### 5.3 What "reproduce the exact sequence" requires on GPU

1. **Disable FMA contraction.** The reference does `mul` then `add` as two roundings (numpy never fuses). `nvcc` fuses `a*b+c` into a single-rounding `FFMA` **by default** (`-fmad=true`). That alone changes results by 1 ulp per operation and accumulates. Either compile with `-fmad=false`, or write `__fmul_rn` + `__fadd_rn` explicitly, or check the PTX for `fma.rn`. This is the single most common silent bit-exactness breaker.
2. **Re-implement `cumsum` as a genuinely sequential scan.** numpy's `np.cumsum` along an axis is an *accumulate* — inherently left-to-right. `torch.cumsum` on CUDA is a **parallel scan** (different association ⇒ different rounding); so are CUB `DeviceScan` and Triton's `tl.cumsum`. The fix is cheap here: each row of the `axis=1` scan has length `m+1 = 267`, and there are `(n+1)·(d+1) ≈ 20,769` independent rows. **Assign one thread per row and loop 267 times.** Total serial work 5.5M adds, fully parallel across 20,769 rows → bit-identical, and fast.
3. **Determine numpy's `einsum` accumulation order empirically — do not assume it.** `np.einsum("am,am->m", Pre, Suf)` with the default `optimize=False` does *not* go through BLAS; its inner-loop order/vectorisation is a numpy implementation detail that can vary with numpy version and CPU SIMD dispatch (SSE2/AVX2/AVX-512). **This is the #1 unknown of the whole port.** Use [FPRev](https://github.com/peichenxie/FPRev) — *designed exactly for this* — to extract the accumulation order on the machine and numpy build that produced the fixtures, then hard-code that order (a fixed reduction tree over 69 terms is trivial to emit). The same tool answers whether `cumsum` is a pure sequential accumulate in your numpy build.
   - Caveat this creates: **the "reference" may not be portable.** If the fixtures were produced on a different numpy/CPU than the port's verification machine, the *reference itself* can move by ~1e-6 and the gate becomes unsatisfiable by any implementation. Pin numpy version + CPU in the gate definition, or re-baseline.
4. **float64 sites are free.** As computed above, the `np.dot` (L410) and renormalisation (L192–217) are safe to reorder at the 1e-12 level. Only the three float32 sites need bit-emulation — this is a much smaller problem than "make the whole thing bit-exact", and it is the reason a bit-exact port is plausible at all.

### 5.4 The published state of the art on reproducible reductions

- **ReproBLAS / Demmel & Nguyen, "Efficient Reproducible Floating Point Summation and BLAS"** ([PDF](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2015/EECS-2015-229.pdf)) — demonstrates that *reproducible* (same-answer-everywhere) summation is achievable and cheap. But it achieves reproducibility by **imposing its own canonical order**; it does not reproduce numpy's legacy order. **Wrong tool for our gate, important precedent for the underlying claim.**
- **"Revealing Floating-Point Accumulation Orders in Software/Hardware Implementations"** ([arXiv 2411.00442](https://arxiv.org/abs/2411.00442), FPRev, [code](https://github.com/peichenxie/FPRev)) — the abstract states the problem precisely: *"their accumulation orders are often undocumented in existing software and hardware implementations, making it difficult for developers to ensure consistent results across systems"*, and the paper *"showcase[s] the accumulation orders of popular libraries (such as NumPy and PyTorch) on CPUs and GPUs"*. **This is direct evidence that NumPy's CPU order and PyTorch's GPU order differ, and the only tool found that can measure the target order.**
- **CUDA C++ Programming Guide**, floating-point section — documents that FMA contraction is on by default and that FP arithmetic is non-associative; [docs.nvidia.com](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html). *Verify the `-fmad` default for your exact toolkit version before relying on it.*
- **PyTorch reproducibility notes** — [docs.pytorch.org/docs/stable/notes/randomness.html](https://docs.pytorch.org/docs/stable/notes/randomness.html) — documents that several CUDA ops are non-deterministic and that results are not guaranteed identical across devices/runs. (The docs site is JS-rendered; I could not machine-verify exact wording in this timebox, so treat this as a pointer, not a quoted claim.)
- **Triton**: no bit-reproducibility guarantee for reductions/scans; reduction order is an implementation detail of the compiler. Treat any Triton reduction as **reassociation-uncontrolled**.

---

## 6. What does NOT exist

A documented absence is part of the answer. As of 2026-11-25, I found **no** artifact for any of the following:

1. **No released implementation of our specific float32 Simpson-in-`log t` / prefix–suffix quadrature path.** The exact bit-order target of the 1e-12 gate has no upstream. Nothing to reuse; nothing to diff against for bit-equality. This is the strongest argument that the gate is bespoke and must be owned in-house.
2. **No released code for DE-ICM**, the algorithmic state of the art (1e-14 accuracy, `O(Mn²)`). The paper's reproducibility section says the implementation is not released. Anything we do with it is a reimplementation from the paper.
3. **No library that computes *exact* top-K Plackett–Luce win probabilities at n≈300.** Exact means `O(n 2ⁿ)`; every candidate is quadrature/approximate (MPL, DE-ICM, LAQI) or log-likelihood-only on observed rankings (choix, PlackettLuce, torch-choice, TF-Ranking, allRank, choice-learn). The `n ≤ 20` subset DP in our repo is at the practical edge of exactness and is not the bottleneck.
4. **No GPU Poisson-binomial engine with per-item leave-one-out other than MPL.** MPL is the only batched/GPU-aware code found for marginal top-K propensities. Notably, DE-ICM's Table 6 lists only three numerical implementations of this integral representation in existence — **DE-ICM, MPL, LAQI** — and of these, only **MPL** returns per-item top-K probabilities, and only **MPL** and **LAQI** have any release at all (MIT both).
5. **No GPU implementation that returns individual *placement probabilities* beyond MPL.** LAQI returns equities; DE-ICM has no code. MPL's validated/experimental range was `K ≤ 30` in their experiments — **our K up to 69 is outside that range**, so even if reused its numerics would need re-validation at our K.
6. **No artifact that reproduces NumPy's float32 reduction order on a GPU.** Not torch, not Triton, not CUB, not JAX, not RAFT/cuML, not numba.cuda, not ReproBLAS. There is no "numpy-compatible float32 reduction" library. The only asset is a *measurement* tool (FPRev) that lets you reverse-engineer the order yourself.
7. **No bit-exact float32 PL/ICM implementation at all, on any hardware.** The entire literature (DE-ICM, MPL, LAQI) works in double or in log-space-single and targets ~1e-6–1e-14 *accuracy*; reproducibility-across-implementations is not a goal anyone has pursued for this problem. There is no prior art to lean on for the gate.
8. **No GPU ICM solver.** LAQI is Node/CPU; DE-ICM is CPU; MPL is the only GPU datapoint in the literature (2 ms/query, K=10, 200 nodes, single precision, as reported second-hand by DE-ICM §5.4).
9. **No maintained package named `pyPL`**, and **BayesPL could not be verified** at the queried GitHub path. Both should be dropped from the library list rather than cited.
10. **No licensed implementation in three of the classic candidates**: `torch-choice` has **no LICENSE file**, `erdman/plackett-luce` has **no license**, and `BayesPL` is unverified. Unlicensed ⇒ cannot reuse regardless of technical fit. This surprised me and is worth recording so nobody re-checks it.

---

## 7. What this means for go/no-go

Facts that should move the decision, in descending order of impact:

1. **The algorithm is not novel, and the published version is both faster and vastly more accurate.** DE-ICM (Oct 2026) does the same integral in `O(Mn²)` with ~1e-14 error and 0.2 s for n=1000 on one core. We should not claim novelty for the quadrature approach; we should cite it. If the 18.4 s is the pain point, **the cheapest win might be algorithmic (DE-ICM's exp–exp lattice + `O(n)` deconvolution), not GPU** — and it stays on CPU.
2. **The 1e-12 gate is not an accuracy gate, it is a bit-emulation gate, and the literature says it is ~10⁶–10⁷× tighter than float32 can support under any reassociation.** Either (a) declare the gate as "bit-identical to the pinned CPU reference, verified op-by-op", in which case the GPU port is a numpy-order emulation exercise (feasible: only 3 float32 sites, §5.3), or (b) re-baseline the reference in float64 / relax to a tolerance consistent with float32 (~1e-6 abs), in which case **MPL (MIT, PyTorch, batched, GPU) becomes directly reusable** and the GPU case is easy.
3. **The gate's *reference* is itself machine-dependent unless pinned.** numpy's `einsum` float32 accumulation order is not specified (§5.3), so the same source can produce different float32 fixtures on different numpy builds/CPUs. Any gate defined against stored fixtures must pin the numpy version and CPU, or it is unsatisfiable by construction.
4. **Licensing is clear for the good options and bad for the popular ones.** MPL **MIT**, LAQI **MIT**, TF-Ranking **Apache-2.0**, allRank **Apache-2.0**, choice-learn **MIT**, choix **MIT**, RAFT/cuML **Apache-2.0**, Triton **MIT**, numba **BSD-2**, PlackettLuce **GPL-3** (blocking), torch-choice and erdman/plackett-luce **unlicensed** (blocking). There is no licence obstacle to ADAPTing MPL.
5. **K=69–300 is outside MPL's validated range** (K≤30 in their experiments, n_docs in the tens for LTR). Reusing MPL means re-validating its numerics at our scale anyway.

**Bottom line for the decision-maker:** the GPU port is technically defensible only if the gate is re-specified. Under the literal 1e-12 gate the project is "write a NumPy-float32-order emulator on a GPU", for which there is no prior art, no reusable library, and no way to validate except against the one pinned CPU build. Under a float32-appropriate tolerance the project is "reuse MIT-licensed MPL-style torch code and batch it", which is a day, not a project. **Get the gate re-specified before writing any kernels.**

---

## Appendix A — search log (required angles → outcome)

| Required angle | Outcome |
|---|---|
| "Plackett-Luce exact probabilities" | Exact marginals = `O(n2ⁿ)`; no library does it above n≈20. → §6.3 |
| "Plackett-Luce GPU" | Only **MPL** (candidate 1); otherwise training/ranking libs. |
| "differentiable Plackett-Luce" | torch-choice, choix, allRank, TF-Ranking — likelihoods, no marginals. Candidates 4–9. |
| "top-k Gumbel-max sampling CUDA" | Kool et al. 2019 (candidate 13), vLLM PR #29210 (14) — samplers, not marginals. |
| "Gumbel top-k torch triton" | Triton (16), generic kernels; no PL marginal kernel. |
| "exponential race sampling GPU" | Leads back to the ICM literature → **DE-ICM** (2), **LAQI** (3). |
| "Poisson binomial PMF GPU" | No GPU Poisson-binomial found; CPU `poibin` (19), Biscarri et al. DC algorithm (20) is what MPL implements. |
| "rank aggregation GPU" | No hit bearing on marginals; PL clustering/aggregation code is CPU. |
| "sequential choice model GPU likelihood" | torch-choice (6), choice-learn (9) — likelihoods only. |

## Appendix B — provenance of each load-bearing claim

- MPL licence/stack/core algorithm: Zenodo API `records/17352314` (`license.id = mit-license`, `resource_type = software`, file `plpropensitiesecir2026-main.zip`); local read of `mpl/mpl/mpl.py` (233 lines) and `mpl_env.yml` (torch 2.7.1).
- DE-ICM quotes (1.1e-14, 4.0e-14, 0.2 s, `O(Mn²)`, "neither is released", "the same mathematics appears in other fields", Table 5 runtimes, Table 6 design choices, the 2 ms/GPU/MPL datapoint): https://arxiv.org/abs/2610.06028 (HTML v1, fetched and text-extracted).
- LAQI licence/behaviour: `/repos/curesive/log-age-quadrature-icm` (`spdx_id = MIT`), local read of `paper/log-age-quadrature-icm-snippet.js` (184 lines).
- Licences: GitHub `/repos/{owner}/{repo}/license` or the repo's own `LICENSE`, or CRAN `DESCRIPTION`; queried 2026-11-25.
- float32 analysis: line numbers are from `engine/eduengine/contest_math.py` @ `e0508f3` as read in this worktree.
