# PRE-DECLARATIONS — MODEL-DEBUG MODE (ceiling-cap defect; benchmark hierarchy)

**LABEL: DEBUG.** This is a **defect-fix and audit** run, not a new experiment in the programme's
predeclared-experiment sense. It **adds no reproduction claim**, **predeclares no successor generator**, and
**does not reopen the closed line** (D150/D154/D167): the closed `v1.5`–`v1.7` family stays closed; only the
**named defect** below may be repaired. No threshold is changed. Nothing is fitted. Every fix must be justified by
the **defect**, never by a result. If a fix changes a published number, the change must be named exactly, with the
reason.

## 1. The defect (named in EXP-21 / D160)

`completion_uis` is capped at **1.0** in **35 of 6,720 cells**, exactly where `1.10 × cohort > 1`. Consequence
recorded in D160: `m = 1.10` appeared **CONSTANT** at 1e-9 on A17 (8.8395202269e-10) while **v1.3/v1.2 were
NOT-CONSTANT at 4.7043695535e-02**; the cap masks the real non-constancy and is an **implementation artefact**
(not a declared UIS convention unless the convention is explicitly declared and defended).

## 2. User directive (verbatim; recorded in the debug memo)

On the "lost to a straight line" framing:

> "Of course what happened last year predicts what happens next year… I'm questioning who the fuck cares — that
> doesn't identify any dynamic other than 'line goes up'."

The write-up's benchmark sentence is a **humility floor, not a dynamic test**; the programme's dynamic claims rest
on **transitions, asymmetries, crossing timing, and distributional change**, not on beating a trend. The
gate-passed write-up is **not retro-edited**; this is a **prospective amendment** the user can approve later.

## 3. Three debug cells (scope)

1. **CAP AUDIT (Agent 1):** enumerate every clamp/ceiling/floor in the pipeline (`completion_uis ≤ 1.0`, GER ≤ 105,
   the m = 1.10 clip, tier capacity, survival ≤ 1, share renormalisations, any `min()`/`max()` in model code) with
   **file:line**, **affected-cell counts**, and classify each as **declared convention vs implementation artefact**.
   The list is reported **before** any fix.
2. **FIX + RE-RUN (Agent 2, after the list):** repair the ceiling-cap implementation so the conversion can exceed
   1.0 under the **declared UIS convention** (state the convention explicitly; no threshold changes; no fitting);
   then **re-run the EXP-21 conversion register** and report: (a) is `m` still constant only on A17; (b) was the
   v1.3/v1.2 non-constancy **cap-induced or real**; (c) do the **12-cell interchangeability counts** change;
   (d) would any **level sentence in the write-up** change. Deterministic two runs; every number reported; no tuning.
3. **BENCHMARK NOTE (Agent 3):** the debug memo on the benchmark hierarchy — persistence/trend = **floor**; dynamic
   criteria = **transitions / asymmetry / crossings / distributions**; list which of the programme's actual results
   are **dynamic vs floor-only**, and what test would count as **identifying a dynamic**. Includes the verbatim
   user quote as the user directive.

## 4. Discipline

- Deterministic: one seed per run, floats `%.10g`, no wall-clock; **two runs byte-identical**.
- Labels: `DEBUG` on every artifact; `SYNTHETIC`/`OBSERVED`/`DERIVED` preserved where inherited.
- No self-justifying re-runs: the fix is licensed by the **defect**, not by any verdict it produces.
- No threshold changes; no fitting; no new behavioural parameter; no successor generator; the closed line stays closed.
- The gate-passed write-up is **not** retro-edited; any resulting amendment is a **prospective** memo item.
- Write scopes: this directory only, plus the repair in a **copy** of the affected model code inside the debug dir.
  No existing repo file is overwritten by the fix; the re-run writes into this directory.

## 5. Sequencing

Agent 1 (cap list) → **report** → Agent 2 (fix + re-run) → deltas; Agent 3 in parallel with Agent 1. Then package,
commit, ZIP, dashboard report.

## 6. AMENDMENT 1 (Lead correction, 2026-11-21 15:30) — measures are different objects with different denominators

The completion cap may **not** be treated as a generic "ceiling". The measures on disk are different objects:

- **GER** = all enrolment (including repeaters/over-age) ÷ official-age population → **can and does exceed 100**;
  a GER above 100 is **not a bug**.
- **NER** = official-age enrolment ÷ official-age population → **cannot exceed 100 by construction**; a cap there
  is **definitional**.
- **UIS completion rate (CR)** = share of the population **3–5 years above grade** that completed the level → its
  denominator is an **older cohort**, so it is **not bounded above by GER** and **can exceed GER**
  (PHL 2024: 98.3 completion on 94.0 GER). "Completion > GER" is a **denominator/definition issue, not an
  arithmetic impossibility**.

**Binding consequences for the audit and the fix:** the cap audit must **classify every clamp by measure**
(GER cap? NER cap? CR cap? m-conversion clip?) and say which are **definitional** vs **artefactual**; the fix must be
**measure-aware** — **never cap GER at 100 or 105 as if it were NER; keep NER ≤ 100 definitional; let CR exceed GER
where the denominators differ**; declare the convention explicitly (UIS CR 3–5-years-above-grade, repeaters across
years, over-age). The report must say which of the **35 capped `completion_uis` cells** are **legitimate CR > GER**
cases vs **model artefact**.

**User view relayed with this correction:** the experiments **may have to be redesigned**, and the handoff to a
stronger reviewer (Opus/Sol) will include (a) the paper's claims quoted **line-by-line** from
`00_handoff/papers/02_october_massification.md`, (b) what each experiment shows, (c) the programme's open questions,
(d) **the benchmark critique (trend = floor, not dynamics)**. Agent 3's memo is to be structured to feed that packet.
The gate-passed write-up remains **unedited** without the user's approval.
