# EVENT_WINDOWS — state-push event windows for the anchor system and the HKG/CHN portability check

**Author:** `pattern-scout` · task-36 pivot · 2026-11-20 · write scope `10_massification/relations/`.
**Status: DESCRIPTIVE TIMING ARTEFACTS, NOT PARAMETERS.** These windows are never supplied to the model as schedules
(R4/R14). No direction claims (R13). No row is a causal estimate.

**Files:** `data/event_windows.csv` (event registry + computed windows), `data/UNIVERSALIZATION_TIMING.csv` (crossings
to align against, from my timing layer), `10_massification/data/POLICY_TIMELINE.csv` (data-hunter's policy dates, adopted).
**Policy sources:** data-hunter's `POLICY_TIMELINE.csv` (13 events; their own confidence labels are `fact (not re-verified
this pass)` or `workspace ledger`), `02_lit/COUNTRY_CARDS/*.md` §5, and the observed series in
`10_massification/data/UNIVERSALIZATION_SERIES.csv`. Where a date is not primary-verified, the row says so.

## 1. The event-window design (declared before looking at outcomes)

For each event: **date signed** vs **date effective** (policy → cohort lag), **affected level/cohorts**, **excluded
transition cohorts** (the cohorts whose treatment status is ambiguous and who are dropped: e.g. the K-12 bridge cohorts,
the 2012–13 HKG double-cohort years), **pre-window** (10 years, relaxed to 8 then 5 where the series is short),
**post-window** (6 years, relaxed to 5 then 4). The reported statistic is the **post-window mean minus the pre-window
linear trend**, in pp, with a naive standard error that ignores serial correlation (so it is optimistic and is NOT a
test of causality). `UNABLE` is recorded where the observed series does not span the window — that is a data finding,
not a zero.

**Data-quality ranks:** `A` = observed policy/law date (primary source not necessarily retrieved); `B` = inferred
effective cohort (policy date exists but the affected cohort is inferred); `C` = inferred expansion episode (the date is
found in the data, no policy document).

## 2. Anchor system (provisional: Philippines) — the mechanism evidence

| Event | Signed → effective | Level / cohorts | Series | Window result (descriptive) | Quality |
|---|---|---|---|---|---|
| RA 10533 K-12 (10→12 yrs) | 2013 → **2016** (SY2016-17; first SHS graduates 2018) | upper secondary; G11–12 from 2016; bridge cohorts excluded | completion_upper_secondary | **UNABLE**: completion series does not span the event | A |
| RA 10533 K-12, composition shift | 2013 → 2016 | secondary GER definition changes when G11–12 enter | ger_secondary | pre-slope +0.57 pp/yr; **shift +0.42 pp (se 0.83, t=0.50)** → no level shift beyond trend | A |
| RA 10931 free SUC tuition | 2017 → **2018** | tertiary entrants; K-12 transition cohorts confound | ger_tertiary | pre-slope +1.20 pp/yr; **shift −5.39 pp (se 1.80, t=−3.00)** → enrolment FELL relative to pre-trend; the K-12 cohort delay is the rival explanation | A |
| 4Ps CCT rollout | 2007 → 2008 (model-internal path only) | Q1–Q2 secondary pupils | ger_secondary | pre-slope +1.00; shift −2.49 (se 1.96, t=−1.27) | B |
| 1987 Constitution free public primary/secondary | 1987 → 1988 | all public cohorts | ger_primary | pre-slope +0.15; shift −0.22 (se 1.54, t=−0.15) | A |

**Alignment with the observed crossing years (from `UNIVERSALIZATION_TIMING.csv`):**
- PHL **primary universal** crossed **2017–2021** — *31 years after* the 1987 constitutional mandate. The crossing does **not** line up with the state-push date.
- PHL **lower-secondary universal** crossed **2023–2024** — no discrete policy event near it.
- PHL **upper-secondary mass** (50%) was already crossed **before the observed completion series begins (≤1999)** — i.e. *before* K-12 (2013/2016) and before free tuition (2018).
- PHL **tertiary mass** crossed **2024–2025**, ~6.5 years after free tuition; the event-window evidence at 2018 is negative, so free tuition is **not** the timing driver the series show.

**Anchor verdict (descriptive, not causal):** for the Philippines, the *discrete state-push dates do not align with the universalization crossing years*. Massification at upper-secondary preceded K-12; primary universalization followed the constitutional mandate by three decades; tertiary massification followed free tuition but the immediate window shows a decline. **The data cannot say which driver (state push, demand pull, supply push) produced the crossing** — the candidate mechanisms' timing is not separable with these series, and R13 forbids a direction claim. What the model must reproduce is the *crossing years and their spacing*, not the laws.

## 3. Portability check — HKG and CHN

| Country | Event | Effective | Result | Reading |
|---|---|---|---|---|
| HKG | 6-year free primary education | 1971 | UNABLE for NER (series starts 1971); crossing of primary NER **1978–79** | the crossing is 7.5 years after the law — plausible policy lag, not testable in-window |
| HKG | 9-year free compulsory (P6+S1–S3) | 1979 | UNABLE for lower-secondary NER (series starts 2001) | the NER-based crossing 2015–16 is a **measure artefact** (NER dips 99.2→93.8); the law-consistent date is ~1978–80 — see EVENT_WINDOWS.md §5 |
| HKG | **12-year free education (free senior secondary)** | **2009** | **shift +9.08 pp (se 1.75, t=5.20)** on upper-secondary NER — the largest computed event-window shift in the set | consistent with a real policy-driven level shift; still descriptive (no control group) |
| HKG | 3-3-4 structure reform / first HKDSE | 2012 | UNABLE (completion series absent) | the double-cohort years 2012–13 are excluded transition cohorts |
| CHN | Compulsory Education Law (9 yrs) | 1986 | UNABLE for completion (series starts 1996+); primary universal crossing **2012–14** = 27y later | the law is not the timing driver in the observed series |
| CHN | **Higher-education expansion (quota increase)** | **1999** | **shift +4.70 pp (se 0.59, t=7.94)** on tertiary GER | a large, well-dated supply expansion that shows in the window; the classic Chinese case |
| CHN | Free rural compulsory education | 2006 | UNABLE for completion | — |

**Portability note.** The two systems give *different* answers: HKG's state pushes are followed by level shifts at the
expected level (2009 senior-secondary free education), CHN's documented 1999 expansion shows strongly in tertiary GER,
but CHN's compulsory-education law does not time the primary universalization (27y gap). So a portability rule cannot be
"laws move levels"; the model should carry the *observed crossing years* as the portability target and treat the laws
as candidate timing markers only where they align (HKG 2009, CHN 1999).

## 4. Censored timing — JPN and KOR (explicit)

The near-universal systems cannot be dated from these series; their crossings are **one-sided bounds** (also in
`UNIVERSALIZATION_TIMING.csv` and data-hunter's `UNIVERSALIZATION_TIMING.csv`):

- **JPN**: in-school rate already above threshold at first observation — primary **"crossed before 1971"**, upper-secondary mass and universal **"before 1999"**; the 1947 compulsory law is far outside the window. Only tertiary mass is datable in-window.
- **KOR**: primary "before 1971"; lower-secondary universal "before 2003"; upper-secondary mass "before 2000"; tertiary mass "before 2000". Upper-secondary universal is datable (~2000).
- Consequence for the gate: for JPN/KOR the only admissible timing outcome is an inequality. A pre-1960/70 national series (MEXT/NIER, Bank of Korea, HK EDB) is required to date them — flagged as a data ASK.

## 5. What is a measure problem, not a policy finding

- **HKG lower-secondary NER** (see §3): the 2015–16 "crossing" comes from the series dipping after 1980; the 1978
  nine-year compulsory policy date is the policy-consistent crossing. This row must not be used as a portability test
  until a completion series for HKG exists.
- **PHL K-12 and GER**: GER is a *gross* ratio and the K-12 reform changes its denominator; the reform's real signature
  is at upper-secondary completion (UNABLE here because the completion series starts 1996 and the post-window is 2022–24).
- **PHL free tuition**: the 2018 window is confounded by the K-12 cohort delay (first SHS graduates enter tertiary only
  2018–19). The negative shift is consistent with the delay, not with a tuition effect.

## 6. Expansion episodes (quality C, inferred from data — not named programmes)

Derived as the median year of top-decile one-year log growth in the observed series (`data/event_windows.csv`):
PHL secondary teacher stock (1997), PHL primary teacher stock (2003), KHM primary teacher stock (1991), CHN tertiary
enrolment (1975). These are **inferred episodes**, useful as candidate supply-push timing markers, and explicitly not
policy dates. The `SCHOOL_EXPANSION.csv` named-programme file was not on disk at the time of writing; these rows are the
stand-in and are labelled C.

## 7. Files and reproduction

| File | Content |
|---|---|
| `data/event_windows.csv` | one row per event: dates, affected level/cohorts, excluded transition cohorts, windows, series, descriptive shift + se + t, data-quality rank, crossing alignment, source |
| `data/UNIVERSALIZATION_TIMING.csv` | crossing years + intervals to align against (my timing layer) |
| `scripts/event_windows.py` | reproduction |
| `10_massification/data/POLICY_TIMELINE.csv` | data-hunter's policy dates (adopted; ACKed) |

**Hard caveats.** (i) Policy dates are largely not primary-verified in this workspace — the country cards say so.
(ii) The naive SE ignores serial correlation, so t-values are optimistic. (iii) Most pre-1990 events are UNABLE because
the observed series do not span them — recorded as UNABLE, never imputed. (iv) There is no control group in any
single-country event window; these are timing artefacts for the anchor-system mechanism discussion and the portability
checkpoint, not causal estimates (R13/R4/R14).
