# FINDINGS — WT1–WT5 predeclared battery (brief 019 / D98–D101)

**Worker:** WT · directory `10_massification/extensions/wt_2026-11-20/`
**Predeclaration:** `PRE_DECLARATIONS.md`, sha256 `d3ad365e7a0f71fd1b187f24fe4cb4e9a4a07f2b1827a253bbbe19e016b1a350`
(written before any run; thresholds, falsifiers, qualifying rules and verdict words unchanged after results).
**Script:** `code/run_wt.py` (one deterministic battery; no RNG, seed = null).
**Labels:** every input row is **OBSERVED**; every statistic is **DERIVED**; **HELD** cells carry no number.

> **A WT PASS is a descriptive footprint, not validation of the paper.** Nothing below validates the
> hysteresis paper, and nothing below is a causal or push/pull direction claim.

## Scoreboard (one line per test)

| test | statistic | threshold | verdict | what it turns on |
|---|---|---|---|---|
| **WT1** | fall-runs/rise-runs = **0.443** | ≤ 0.50 | **NOT SUPPORTED** | count leg passes, **depth leg fails** (0.601 > 0.50) |
| **WT2** | decoupled share = **1.000** | ≥ 0.50 | **NOT SUPPORTED** | decoupling leg is near-vacuous; **reversal leg fails** (4/10 = 0.40 > 1/3) |
| **WT3** | income-partial ρ = **−0.520** | ≥ +0.40 | **NOT SUPPORTED** | raw ρ 0.073 → **sign flips negative** on income control |
| **WT4** | exit episodes = **0** | 0 + tertiary ≥50 by 2025 | **SUPPORTED** (descriptive) | zero episodes; but the 2022 dip came close |
| **WT5** | gate ratio 85/45 = **1.889** | ≥1.50 (design-only) | **DESIGN-ONLY**, not scored | the 1.889 is **cross-year**; same-year = 0.889 |

**Net decision-relevant result: the D101 gate is not met.** WT1 and WT3 — the two tests whose conjunction
would license a declared complementarity→persistence term — both return **null** (a formed statistic missing its
predeclared bar). Per D101 the exit-cost/complementarity layer stays **PARKED**; the paper remains a **scored
rival with no demonstrated on-disk footprint**. WT4's pass is a descriptive confirmation of a known
non-response, not evidence for the paper's mechanism.

---

## WT1 — Asymmetric adjustment: adoption fast, exit slow (Prediction 1)

**Plain answer.** Across 96 qualifying series (29 countries, 1970–2024), **starts of decline are fewer than
starts of advance, but not "fewer and shallower" by the predeclared two-to-one margin.** 117 fall-runs against
264 rise-runs gives a count ratio of **0.443** (passes ≤0.50). Median rise depth is **11.128 pp** and median fall
depth **6.686 pp**, ratio **0.601** — above the 0.50 bar. The block's falsifier is "either ratio > 0.5", so the
verdict is **NOT SUPPORTED**.

**The discriminating action's reading — NEGATIVE** (the block's negative arm): *"symmetric rise/fall dynamics →
the paper adds nothing at this granularity and is parked as a rival with no empirical footprint."* We record the
negative reading **with a qualification the block's binary does not carry**: both ratios point in the predicted
direction (falls are ~44% as frequent and ~60% as deep), so the failure is a **margin** failure, not a reversal
of sign. The predeclared test asked for a factor of two; the data deliver about 1.7× on depth and 2.3× on
count. That is a directional hint, **not** a footprint, and the verdict word stays NOT SUPPORTED.

**Why the aggregate hides a lot (reported, does not change the verdict).** The pooling is heterogeneous:

| indicator | qualifying series | rise-runs | fall-runs | fall/rise |
|---|---|---|---|---|
| `SE.ADT.LITR.ZS` literacy | 8 | 12 | **0** | 0.000 |
| `SE.SEC.CUAT.UP.ZS` upper-sec attainment | 15 | 37 | 2 | 0.054 |
| `SE.TER.ENRR` tertiary GER | 27 | 66 | 22 | 0.333 |
| `SE.SEC.CMPT.LO.ZS` lower-sec completion | 22 | 74 | 40 | 0.541 |
| `SE.PRM.CMPT.ZS` primary completion | 24 | 75 | **53** | **0.707** |

The asymmetry the paper predicts is visible in attainment/tertiary/literacy and **absent in the completion-rate
series**, which carry most of the noise (45% of all fall-runs are primary-completion two-year wiggles). 42 of 96
series have zero fall-runs at all. A single pooled ratio is therefore a weak summary; the honest statement is
*"the direction is as the paper says, the magnitude is not, and it is indicator-dependent."*

**Integrity note.** The PHL detail series that motivate the whole test — `completion_upper_secondary`,
`completion_primary`, `completion_lower_secondary` (11 observed years each) — are **excluded by the predeclared
n≥15 rule**. WT1 therefore never sees the 2017→2022 PHL fall; WT4 handles that series separately. This is the
frozen rule working as written, and it is why WT1 must not be described as a PHL result.

**What would have changed the verdict.** A depth ratio ≤0.50. It was 0.601.

---

## WT2 — Credential decoupling: adoption continues after the destination saturates

**Plain answer.** Among the **10 of 30** countries that have both endpoints observed (1995 and 2024) and ≥15
years of both series, **all 10 (100%)** are "decoupled" in the block's sense: tertiary GER grew while the
formal-non-agricultural employment share grew by less. But **4 of those 10 (40%)** contain a ≥5 pp tertiary-GER
reversal sustained ≥3 observed years (MNG, MYS, PHL, THA), which breaches the block's "≤1/3" condition. The
falsifier "reversal in >1/3 of decoupled countries" therefore fires: **NOT SUPPORTED**.

**Why the headline 100% must not be quoted as a finding (M7 caveat, predeclared).** The block's decoupling
criterion compares a **percent growth** (D_cred, e.g. CHN +1550%) with a **percentage-point change** (D_dest,
e.g. CHN +30.0 pp). Almost any growing credential series satisfies `D_dest < D_cred` by unit mismatch alone. The
test as written is therefore **nearly vacuous on its first leg**; the information is entirely in the reversal
leg, which fails. Secondarily, the countries that qualify are the fast-expanders (CHN, IND, KHM, MAR, MNG, MYS,
NPL, PHL, THA, VNM) — the panel's strict endpoint requirement selects on growth.

**The discriminating action's reading — NEGATIVE** (block's negative arm): *"enrolment tracks the destination —
stalls/reverses when the rung fills → the credential-queue reading has no on-disk footprint and the ceiling must
be explained by something else."* Caveat attached: 40% of the decoupled countries showing a sustained ≥5 pp
tertiary reversal is evidence of **reversibility in the enrolment series**, which is the opposite of the
"adoption does not reverse" corollary. It is *not* evidence about wage premia or queue saturation — that is
**HELD** (no PSA/Enterprise Surveys wage series on disk) and the C3 claim is **not reopened**.

**HELD.** `WT2.HELD-1` — credential wage-premium series (PSA FIES/LFS; WB Enterprise Surveys). No number is
reported. The external "39% overeducated / flat graduate wages" facts are cited not measured (D49).

**What would have changed the verdict.** Reversal in ≤3 of 10 decoupled countries (≤1/3).

---

## WT3 — Complementarity → persistence (Prediction 4)

**Plain answer.** In the **14 countries** with ≥15 in-window observations of upper-secondary attainment, the
predeclared primary combination (saturation ceiling × median ECI) gives a **raw Spearman ρ of 0.073** and an
**income-partial ρ of −0.520**. The association does not merely weaken under income control — **it flips sign**.
The block's falsifier is "|income-partial ρ| < 0.40 **or sign flips** on income control"; both fire.
**NOT SUPPORTED**.

Robustness (reported in `results/DETAIL.csv`, not used for the verdict):

| combination | raw ρ | income-partial ρ |
|---|---|---|
| P1 saturation ceiling × C1 median ECI (**primary**) | 0.073 | **−0.520** |
| P1 × C2 median formal-non-agric share | **0.429** | 0.046 |
| P2 reversal count × C1 | −0.445 | −0.459 |
| P2 reversal count × C2 | −0.282 | −0.210 |

This is a clean instance of **the Y1 lesson repeating**: the one raw association large enough to matter
(P1 × C2 = 0.429) is **almost entirely absorbed by income** (partial 0.046). Nothing here supports a
complementarity→persistence layer.

**The discriminating action's reading — NEGATIVE** (block's negative arm): *"no partial association, or it is
absorbed by income — the Y1 lesson → Prediction 4 has no on-disk footprint; complementarity is parked."*

**Two honest limits on the negative too.** (i) The saturation-ceiling proxy is partly an artefact: for countries
still expanding, "max 1995–2024" is just *today's level*, so high-ECI countries that were already near
saturation in 1995 mechanically look "persistent" while high-ECI countries that expanded hard look "low-ceiling".
The sign flip is consistent with that artefact, not necessarily with the paper being wrong. (ii) n = 14,
cross-sectional, one observation per country — this is a descriptive association, never a law.

---

## WT4 — The PHL ceiling as a scaffold that cannot be exited

**Plain answer.** **Zero exit episodes.** Upper-secondary completion never falls ≥5 pp below its 2017 peak
(76.433) for ≥3 consecutive observed years — the 2022 value (68.277) is a **single** observed year below the
71.433 threshold, and by 2024 the series is back to 75.025, inside the 2 pp recovery band. Tertiary GER dips
**−10.228 pp** in 2018 but is back above 50 by 2025 (51.072, observed), so the second clause is met.
**SUPPORTED** — descriptively.

**The discriminating action's reading — POSITIVE** (block's positive arm): *"the 'cannot be exited' reading is
consistent with the record and the paper's account survives as the leading (still-undemonstrated) candidate for
the D63 ceiling residual."* Note the block's own word: **consistent**. This test cannot distinguish the paper's
account from any other account that implies no exit; it only rules out an exit episode on this record.

**Where the pass is fragile (reported because it is decision-relevant).**
1. **2022 is a near-miss.** The fall from 2017 (76.433) to 2022 (68.277) is a **−8.156 pp drawdown** — well past
   the 5 pp trigger. It does not become an episode only because the series is observed in **gaps** and 2023
   (71.929) is already above the 71.433 threshold. One more year of data at 2022 levels would have produced an
   exit episode and flipped the verdict.
2. **The tertiary "recovery" gate is doing real work.** Tertiary GER is below the 2016−5 = 33.345 line for three
   consecutive years (2018–2020: 28.117, 30.055, 31.632). Under a literal "≥5 pp below 2016 for ≥3 years" reading
   that *is* an episode; it is excluded only by the block's "without recovery" clause, since the series recovers
   to 47.414 by 2024 and 51.072 by 2025. Both facts are in the components so a reader can apply their own
   reading. The predeclared reading is the one that governs: no episode.
3. The series is **observed only 11 times in 26 years** (1999, 2000, 2003, 2004, 2008, 2010, 2013, 2017, 2022,
   2023, 2024). "Consecutive years" therefore means consecutive *observations*; interpolating the gaps would
   fabricate data.

**HELD, not reopened.** The *discriminating* queue/ceiling test remains **C3/HELD**. WT4 formalises a known
non-response; it does not explain it.

---

## WT5 — Shadow education as a positional scaffold at the gates — **DESIGN-ONLY, NOT SCORED**

**Plain answer: the predeclared number does not survive contact with the disk.** The block states
"HKG: 85/45 = 1.89". On disk **45 is the 1996 HKG primary rate, not a 2010 rate** — the 2010 survey has no
primary row. The 1.889 is a **cross-year** ratio (2010 senior-secondary 85 ÷ 1996 primary 45).

| reading | value | source |
|---|---|---|
| block's ratio (cross-year) | **1.889** | 85 @2010 ÷ 45 @1996 |
| **same-year 1996** (senior ÷ primary) | **0.889** | 40 ÷ 45, HKFYG telephone survey |
| same-year 2010 (senior ÷ lower-secondary) | 1.181 | 85 ÷ 72 |
| 2003 stage gradient (S6-7 ÷ S1-3) | 2.003 | 70.3 ÷ 35.1, Bray & Kwok (2003) |
| KOR 2023 participation elementary → high | 86.0 → 66.4 (−19.6 pp) | MODS/KEDI 2023 |
| KOR 2023 spend high ÷ elementary | **1.234** (+23.4%) | 491 ÷ 398 thousand KRW/month |

Only **one** survey on disk observes primary *and* senior-secondary shadow participation in the same year
(HKG 1996), and it shows **no gate gradient at all (0.889)**. The block's support clause ("≥1.5× in every system
where both are observed") therefore cannot be evaluated as stated; the 2003 and 2010 gradients are
**within-secondary** gradients (S1-3→S6-7, lower→senior), not primary→senior. The KOR pattern (participation
falls, per-student spend rises at the gate) is on disk and is exactly the sign the paper expects — but it is a
**different quantity** from the ratio in the support clause.

**Verdict: DESIGN-ONLY / NOT SCORED**, with the cross-system claim **DATA LIMITED** (one system, one same-year
pair, and that pair is negative). No support or falsifier verdict is returned. Near-circularity caveat stands:
this re-tabulates a gradient already held (Bray & Kwok 2003; Kwo & Bray 2011) and cannot change the model.
**HELD:** `WT5.HELD-2` — PHL/KHM/CHN/JPN participation rates; the `TARGETS_SHADOW.csv` rows are `unresolved`
with empty values and **no number is imputed**.

---

## What this cannot claim

1. **It does not validate the paper.** Four of five tests return null or unscored; the one pass is a descriptive
   confirmation of a known non-response. No WT result is evidence that scaffold-exit costs, credential
   hysteresis, or dependency transformation operate.
2. **No causal claim, no direction claim.** Everything is a descriptive association or episode count on
   OBSERVED series. Nothing here identifies a mechanism, a sign of causation, or a push/pull direction. R13-safe.
3. **No model change.** The D101 conditional (a *declared*, ablation-tested complementarity→persistence term only
   if WT1 **and** WT3 are both non-null) is **not met**. The exit-cost layer is **PARKED**; the paper stays a
   **sixth scored rival with no empirical footprint**, still the *candidate* (not the confirmed) account for the
   D63 ceiling residual.
4. **No C1–C4 reopening.** The wage-premium/queue discriminating tests remain C3/HELD. WT4 is not that test.
5. **No population, no law, no forecast.** n = 96 series / 29 countries (WT1); 10 countries (WT2); 14 countries
   (WT3); 1 country (WT4, WT5). WT3's n=14 and WT5's n=1 system are far too small for inference beyond the
   descriptive.
6. **No repair of the two specification problems found** (WT2's unit mismatch; WT5's cross-year ratio). They are
   reported as findings about the tests. Fixing them would be a new predeclaration, not this battery.
7. **WT1's "falls are rare" is partly exogenous.** The 30-country panel is an expansion era; a low fall count is
   partly a property of the era, not of exit costs. The block records this; so do we.
8. **Nothing here is a HELD number.** Wage premia (HELD-1) and PHL/KHM/CHN/JPN shadow participation (HELD-2)
   remain unknown; no value is reported or imputed for them.

---

## Files

| file | what it is |
|---|---|
| `PRE_DECLARATIONS.md` | five blocks verbatim + frozen mechanics M1–M16 (sha256 in manifest) |
| `code/run_wt.py` | the single deterministic battery |
| `code/build_predeclarations.py` | rebuilds the verbatim-extract predeclaration (hash-stable) |
| `code/build_manifest.py` | rebuilds `RUN_MANIFEST.json` from the on-disk files |
| `results/RESULTS.csv` | one row per test (+2 HELD rows), all cells reported |
| `results/DETAIL.csv` | 996 per-series / per-country component rows |
| `results/run_info.json` | thresholds, input/output hashes, verdict map emitted by the run |
| `_determinism/run_b/` | second independent run; byte-identical outputs |
| `RUN_MANIFEST.json` | sha256 of predeclaration, code, inputs, results + determinism evidence |

---

## Council record corrections (cycle 13, D108 — Lead-applied; no re-execution)

1. **WT4 fragility sentence corrected.** The earlier sentence "one more year at 2022 levels would flip it" is **false**
   under the frozen ≥3-consecutive-observed-years rule: only 2022 is below the 71.433 threshold, so it would take
   **two** more observed years. The correct fragility statement is: **2023 clears the 5 pp trigger by 0.496 pp** and
   **2024 clears the 2 pp recovery band by 0.592 pp** — the SUPPORTED verdict is descriptively correct but sits on thin
   margins.
2. **WT2 annotated VOID as a test of the paper** (verdict NOT SUPPORTED stands as scored): the decoupling leg compares
   % growth with a pp change, so it is near-vacuous; on a common pp metric decoupling holds 7/10 (KHM, PHL, VNM reverse);
   the reversal leg counts dips, not exits (PHL's 2018 tertiary dip recovers to 51.072 by 2025). No interpretive weight
   either way.
3. **WT5 NOT SCORED corrected to a Council-side authoring error**: the brief-019 block's 1.889 is cross-year
   (HKG 2010 senior ÷ 1996 primary); the only same-year primary+senior pair on disk is HKG 1996 = 40/45 = 0.889.
   The worker's NOT SCORED is upheld; the real shadow test is the v1.3 module (EXP-4 A3-S).
