# AUDIT — shadow education (codex assumption-audit item 5): what the corpus can and cannot distinguish

**LABEL: `DERIVED`** (mapping memo; no new run; every row points to a named file+row). Date 2026-11-21.
Codex's item-5 ask, as relayed: map to `04_data/TARGETS_SHADOW.csv`, `02_lit/COUNTRY_CARDS/KHM.md`,
`09_relations/data/shadow_gradients.csv`, the LEDGER (Bray/Kwok), and state **what the corpus can distinguish** —
who buys, stage/gate, provider, price, timing vs exams — and that **expenditure alone cannot separate catch-up from
exam-prep**.

## 1. What is on disk

| object | content (verified) |
|---|---|
| `04_data/TARGETS_SHADOW.csv` | **14 rows**; only **Hong Kong** carries rates (1996/2010 surveys, all **low confidence**; the source authors themselves say the surveys are not statistically robust): primary 45 (1996) / lower 26 (1996) / middle 34 (1996) / senior 40 (1996); lower 72 (2010) / middle 82 (2010) / senior 85 (2010); parents 58 (2010, press-reported). **PHL, KHM, CHN, KOR, JPN rows exist with empty rate fields** — no target. Provider mix **not reported** in any row. |
| `02_lit/COUNTRY_CARDS/KHM.md` | **Grade 9 tutoring 68.4%** (193/282, 2012-13, two schools — one urban, one rural; Brehm & Silova WP39, FULL-TEXT); **primary 41.3%** (67/162); urban primary teachers naming tutoring as out-of-school work **41.5%** (Benveniste et al. 2008, second-hand); tutoring earnings **~two-thirds** of base salary (second-hand). **Dominant provider = the own teacher selling the regular curriculum back** (*rien kuo*), not a commercial chain; monthly teacher-set subject tests are the gate architecture; **no nationally representative take-up**; **SEA-PLM 2024 has no shadow module** (full-text search empty — "do not invent one"). |
| `09_relations/data/shadow_gradients.csv` | HK 2003 (Bray & Kwok 2003, EER 22:611-620, Table 1): S1-3 **35.1%**, S4-5 **46.6%**, S6-7 **70.3%**; **gate gradient S6-7 − S1-3 = +35.2 pp**. |
| `LITERATURE_LEDGER.md` | Bray & Kwok 2003 **BLOCKED** (SSL); Bray et al. 2016 **BLOCKED** (403); Bray et al. 2014 **metadata-only** (the citation behind the "85% senior-secondary" figure is **unverified**); Jayachandran 2014 **FULL-TEXT** — teacher-sold tutoring, deliberate withholding (Nepal), identifying teacher incentive, not commercial shadow education. |

## 2. What the corpus can distinguish

| dimension | can distinguish? | on what evidence |
|---|---|---|
| **Who buys** | **partially** — by stage and (HK) parents vs students; by income, **no** (no income gradient on disk) | HK rows by stage; KHM grade-9 vs primary coverage (two schools only) |
| **Stage / gate** | **yes, descriptively** — HK stage gradient (+35.2 pp from S1-3 to S6-7); KHM grade-9 gate | `shadow_gradients.csv`; `COUNTRY_CARDS/KHM.md` |
| **Provider** | **only for KHM** (own-teacher dominant); **no provider mix for HK** | KHM card §1/§3; CSV notes "provider mix not reported" |
| **Price** | **almost not at all** — one second-hand ratio (earnings ≈ two-thirds of salary, KHM); no price series, no fee data | KHM card (second-hand) |
| **Timing vs exams** | **weakly** — HK gate gradient is consistent with gate competition, but no exam-date/timing data; KHM monthly teacher tests are the gate architecture, not a timing measure | HK gradient + KHM card |
| **Catch-up vs exam-prep** | **NO — not separable from expenditure or participation.** There is no motive-labelled series anywhere in the corpus. | see §3 |
| **Cross-country comparability** | **NO** — HK low-confidence 1996/2010 surveys; KHM two schools; PHL/CHN/etc. empty; UIS metadata unverified (HELD) | `TARGETS_SHADOW.csv`; D157 HELD list |

## 3. The binding limitation: expenditure alone cannot separate catch-up from exam-prep

Every number on disk is a **take-up rate** or a **stage gradient**. None records **why** the household bought (remedial
help vs gate competition), and none records expenditure separately from participation. A family that buys tutoring to
pass a subject and a family that buys it to win a selective place can produce the **same participation rate and the
same spend**; the two motives are only distinguishable with a motive-labelled survey, exam-timing data, or provider
type — **none of which is on disk** (Bray et al. 2016 is blocked; the HK 2010 survey is low-confidence; KHM is two
schools, teacher-sold). Therefore: **no claim of the form "x% of tutoring is catch-up" or "gate tutoring is y% of
spend" may be made from this record.** The corpus supports **descriptive** statements about stage gradients and
provider type in the two documented cases only.

## 4. Implication for the coevolve v0 model (not a result)

The v0 tutoring block (`coevolve_2026-11-21/PRE_DECLARATIONS.md` §5) carries **two declared motives** (catch-up and
gate) and makes **concentration an output** — the model can separate what the corpus cannot. The corpus **cannot
calibrate** those motives; v0 must be read as a **mechanism exploration** (`SIMULATED`), not as a fit to the HK/KHM
numbers. The two documented facts (HK stage gradient +35.2 pp; KHM own-teacher dominance at the Grade-9 gate) are the
only empirical anchors a future phase may use, and only as **context**, never as targets.
