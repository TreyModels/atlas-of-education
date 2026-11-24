# DHS dataset request — confirmation snapshot (2026-11-24)

**Captured:** 2026-11-24 18:32 +08:00 from Safari on the Mac (AppleScript page source + full-screen capture).
**Page:** https://dhsprogram.com/data/dataset_admin/index.cfm — "Datasets Request Confirmation".
**Project title:** Atlas of Education. **Applicant:** Trey Menefee (email redacted here; present in the raw snapshot only).
**Status:** "Your request to download datasets for the above study has been received and is pending. You will receive an email notice after your request is reviewed."

## Pending request(s)

| Country | Survey | GPS | HIV | SPA |
|---|---|---|---|---|
| Cambodia | X | X | | |
| India | X | X | | |
| Indonesia | X | X | | |
| Myanmar | X | X | | |
| Nepal | X | X | | |
| Philippines | X | X | | |
| Sri Lanka | X | | | |
| Thailand | X | | | |
| Vietnam | X | | | |

GPS requested for 6 of 9: Cambodia, India, Indonesia, Myanmar, Nepal, Philippines.

## Special terms accepted (applicant report)

The applicant reports that some datasets required accepting **special terms, including sending copies** of the data/products. This matches the country-specific conditions documented in the acquisition plan: Cambodia requires 10 copies to NIS/MOH; Vietnam 2005 requires pre-publication approval by NIHE/GSO (ACQUISITION_PLAN.md §6/§8). The exact wording and which dataset triggered it are **UNVERIFIED** — the confirmation page does not display it. Action: capture the terms at the next opportunity (login/approval page or emailed approval) and append here.

Also displayed on the page: "NEPAL 2016 SPECIAL PERMISSION DATASET" — the Nepal 2016 Mixed Methods Data requires its own project request ("Using Nepal 2016 Mixed Methods Data"); it is not part of this request.

## Flag: requested set ≠ pre-registered set (P0)

The pre-registration fixes a 14-country panel: 8 sub-Saharan (MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA) + KHM, PHL, VNM + BEN, NAM, SWZ. The submitted request is **9 Asian countries** (table above). Consequences:

1. The pre-registered M0–M4 analysis cannot be run as written on this set.
2. Either amend the request to add the 14-country panel (recommended if the fertility test is to proceed as pre-registered), or write a new pre-registration for the acquired set **before any analysis is run**. No analysis will be run until one of these is decided.
3. GPS is not used by the pre-registered test; the GPS tick adds a Terms-of-Use scope (justification supplied separately in the application).

## Raw snapshot artifacts (kept outside the public repo; contain the applicant's email)

- PNG: `/Users/treymenefee/atlas-work-2026-11-23/snapshots/dhs-2026-11-24/safari_confirmation_20261124-183224.png` — sha256 `78534ec1acf9f29693208542e1f045b2876539527ed7f6d0e544a633cc3d468d`
- HTML: `/Users/treymenefee/atlas-work-2026-11-23/snapshots/dhs-2026-11-24/page_20261124-183152.html` — sha256 `199f59332501473ba6b9ebcf25a274e6ac3df9aac362f79aee6179d9647fa796`

Raw files are not committed because the repository is public; this transcription is the record.
