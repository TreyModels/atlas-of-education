# Access status + the exact next action for Trey (2026-11-24, 23:40 +08:00)

**Purpose:** part 2 of task-36. What the DHS dataset requests' status is *as far as can be verified without
logging in*, what only Trey can check, and the exact, copy-paste next action. **Not a scraper:** every step below
is a normal registered-user action; no login is attempted by the agent, no credential is stored, and no gated
file is fetched.
**Branch:** `research/dhs-acquisition-2026-11-24`. **Related:** [`CONFIRMATION_2026-11-24.md`](CONFIRMATION_2026-11-24.md)
(the 18:32 snapshot), [`../ACQUISITION_PLAN.md`](../ACQUISITION_PLAN.md), [`../PRE_REGISTRATION.md`](../PRE_REGISTRATION.md).

---

## 1. Status summary

| Item | Status | Source / how verified |
|---|---|---|
| DHS account for the applicant | **exists**; approval state not visible without login | confirmation snapshot 2026-11-24 18:32 (`CONFIRMATION_2026-11-24.md`) |
| **Asian request** — 9 countries (includes the pre-registered KHM, PHL, VNM) | **PENDING** ("request … has been received and is pending") as of **18:32**; not re-checked since (login-gated) | same snapshot, page title "Datasets Request Confirmation" |
| **African request** — the 11-country panel (MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA, BEN, NAM, SWZ) | **NOT SUBMITTED.** The DHS form allows **one region per project request**, so the 14-country pre-registered panel requires this second request | applicant report, recorded in `CONFIRMATION_2026-11-24.md` (18:40 update) |
| GPS scope | requested for 6 of 9 Asian countries — **not needed** by the pre-registered test | snapshot |
| Special terms | applicant reports accepting terms that include sending copies; exact wording **UNVERIFIED** (not shown on the confirmation page) | snapshot |
| Public site state | registration, login, access-instructions and funding-FAQ pages all **HTTP 200**; **no suspension/closure notice** found in the page text | agent check 2026-11-24 **23:38** (read-only curl, no login) |
| Programme status | open for new registrations since Aug–Sep 2025 after the 2025 USAID funding end and the Gates stabilisation grant; **current processing speed/turnaround UNVERIFIED** | Aug/Sep 2025 third-party reports cited in `ACQUISITION_PLAN.md` §2.5; DHS pages carry no notice today |
| Any email/approval received | **UNKNOWN from here** — the agent cannot see the applicant's inbox | — |

**What changed since the 18:32 snapshot:** nothing verifiable. The site is healthy and shows no notice; the
pending request's status can only move inside the applicant's account. The 24–48 h review clock (Mon–Fri per DHS's
access-instructions page) started at submission on **Tuesday 24 Nov**, so the expected decision window is
**Wed 25 – Fri 27 Nov 2026**.

---

## 2. What only Trey can check (2 minutes, one login)

1. Log in at <https://dhsprogram.com/data/dataset_admin/login_main.cfm>.
2. Open the account home: <https://dhsprogram.com/data/dataset_admin/index.cfm>.
3. Copy the **verbatim status** of the 9-country request (e.g. "pending", "approved", "additional information
   needed") and the **date/time**, and any new message. Also record whether the country rows show the datasets as
   available.
4. Paste them into [`STATUS_LOG.md`](STATUS_LOG.md) (template committed alongside this file). That log is the
   only place the status may be asserted; until then the status is *pending as of the 18:32 snapshot*.

**Do not** share the password with any agent, paste it into chat, or commit any page capture that contains the
applicant's email or account details. The raw snapshot stays outside the public repo (as at 18:32).

---

## 3. The exact next action — in order

### Action 1 (today, ~10 min): submit the **second project request** for the 11 African countries

Because one project request can carry only one region, the pre-registered 14-country panel cannot be completed
from the existing 9-country Asia request. Submit a **second** request under the **same account** — same study,
African region, **no GPS and no HIV tickets** (the pre-registered test uses region fixed effects, not
coordinates; HIV is unrelated and carries extra terms).

- **Title (use exactly):** `The Atlas of Education — sub-Saharan Africa panel`
- **Description (use exactly):**
  > Research study of the individual-level association between women's education and children ever born in
  > sub-Saharan Africa, using DHS standard Individual Recode files for Malawi, Ethiopia, Uganda, Lesotho,
  > Tanzania, Kenya, Mozambique, Ghana, Benin, Namibia and Eswatini. The analysis compares births-based and
  > surviving-children-based fertility measures, uses survey weights and design-based standard errors, and is
  > observational; no causal claim is made. The study will submit resulting publications to The DHS Program and
  > will not redistribute microdata.
- **Countries to tick (11):** Malawi, Ethiopia, Uganda, Lesotho, Tanzania, Kenya, Mozambique, Ghana, Benin,
  Namibia, **Eswatini**.
- **Do not tick:** GPS datasets, HIV datasets (no need; extra terms), or any country outside the list (each
  additional country widens the request and slows review).
- **Survey datasets only** ("Survey Datasets" / unrestricted standard recodes), which is the default.
- If the form offers a free-text "region" or "countries" box that would let the same project request be amended
  instead, prefer **amending the existing project** over creating a second one — either satisfies coverage; the
  important thing is that the 11 African countries are requested under the same applicant account.

### Action 2 (same session, ~10 min): check the Asian request and record it

Use §2's method. If the Asian request shows **"additional information needed"**, supply it immediately (the page
shows how; do not open a new request for the same purpose). If it is approved, **stop and tell the Lead** — the
download phase can start for the 3 pre-registered Asian countries (KHM/PHL/VNM) while the African request is
pending.

### Action 3 (diary): watch the decision window

- Expected review: **Wed 25 – Fri 27 Nov 2026** (DHS states 24–48 h, Monday–Friday, per
  <https://dhsprogram.com/data/Access-Instructions.cfm>).
- Check email and the account home once per working day.
- **If nothing by Monday 30 Nov 2026**, send this email (plain text, no attachments):

> To: archive@dhsprogram.com
> Subject: Status of dataset access requests — "Atlas of Education" (submitted 24 Nov 2026)
>
> Dear DHS Program Data Archive,
>
> On 24 November 2026 I submitted dataset access requests under the project "Atlas of Education": one for
> Cambodia, India, Indonesia, Myanmar, Nepal, the Philippines, Sri Lanka, Thailand and Vietnam, and one for
> Malawi, Ethiopia, Uganda, Lesotho, Tanzania, Kenya, Mozambique, Ghana, Benin, Namibia and Eswatini. Both were
> submitted under the same account (the email address from which I am writing).
>
> Could you confirm whether either request needs additional information from me? The study is an observational
> analysis of women's education and children ever born using the standard Individual Recode files, and I will
> submit resulting publications to The DHS Program and will not redistribute microdata.
>
> Thank you,
> Trey Menefee

### Action 4 (only after **any** approval): download, verify, hand over

- Follow [`../ACQUISITION_PLAN.md`](../ACQUISITION_PLAN.md) §3 Tier 1 order (Tier 1 = 69 standard-DHS IR Stata
  ZIPs, 493.6 MB; then SWZ 2006 and VNM 1997/2002; MIS/AIS only if variables verified).
- Save **outside the public repo**, produce `sha256` manifest, log release code `v000` and download date.
- Then run the ready pipeline (part 3): `python3 scripts/ir_pipeline.py --datadir <dir> --check-only` → full run.
- **Never** commit microdata; the Atlas repo is public and DHS Terms forbid redistribution, including in any
  dashboard. Publications go to `references@dhsprogram.com`; Cambodia (10 copies to NIS/MOH) and Vietnam 2005
  (pre-publication approval by NIHE & GSO) conditions apply if those rounds are used.

### Action 5 (if refused, partial, or ambiguous)

Do **not** work around it: no second account, no shared credentials, no scraping of gated files, no "someone
else's copy". Record what was refused in `STATUS_LOG.md`, tell the Lead, and apply the pre-declared coverage rule
in [`../AMENDMENT_02_ACCESS_COVERAGE.md`](../AMENDMENT_02_ACCESS_COVERAGE.md) (which fixes, **before data
arrives**, what may and may not be analysed under partial approval).

---

## 4. Timeline (Asia time, +08:00)

| When | What | Who |
|---|---|---|
| Tue 24 Nov, 18:32 | Asian 9-country request submitted (snapshot) | applicant |
| Tue 24 Nov, 23:38 | public site re-checked: all pages 200, no notices; nothing new visible | agent (this record) |
| **Tue 24 Nov, tonight** | **submit African 11-country request**; record both statuses in `STATUS_LOG.md` | **Trey** |
| Wed 25 – Fri 27 Nov | DHS review window (24–48 h Mon–Fri, per DHS) | DHS |
| Mon 30 Nov | if no decision: email `archive@dhsprogram.com` (template above) | Trey |
| On approval | download Tier 1, sha256 manifest, run `ir_pipeline.py --check-only` → full preregistered test | Trey + agent |
| If partial | apply `AMENDMENT_02_ACCESS_COVERAGE.md`; no clever substitution | Lead |

---

## 5. UNVERIFIED / cannot be verified from here

- The **current** status of the Asian request (only the 18:32 snapshot is recorded; login-gated).
- Whether DHS has already emailed a decision (inbox is not visible to the agent).
- The **exact special-terms wording** accepted at 18:32, and which dataset triggered it (Cambodia's 10-copy and
  Vietnam-2005 pre-publication conditions are documented, but the page did not display the wording). Capture at
  next login/approval and append to this file.
- The claim that the form allows only **one region per request** — applicant-reported, consistent with the actual
  submitted set; not independently verifiable without logging in.
- DHS's **current** processing speed under interim funding (the 24–48 h figure is their documented norm, not a
  guarantee).

## 6. Standing prohibitions (unchanged)

No credential in the repo/logs/chat · no second account · no scraping or guessing of gated URLs · no
redistribution of microdata (including dashboards) · no causal language from observational data · no synthetic
or model data presented as the real test.
