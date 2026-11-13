# Lane C decisions: prepared briefs for Trey

6 November 2026, prepared during the to-do run. Every item in Lane C is a decision, a payment or a relationship, so none
of them can be completed by the agent. What the agent *can* do is gather the facts, draft the letter and put the choice in
one page. That is what this file is. Each section ends with **Decide:** and the exact thing to do.

---

## C1. The domain: educationatlas.com is taken, and so is .org (by another Education Atlas)

Checked 6 November 2026 by RDAP (the registry record) and DNS.

| Domain | Status | Evidence |
|---|---|---|
| **educationatlas.com** | **Registered**, not available at registration price | Registered 2005-05-14, expires 2027-05-14, registrar GoDaddy, name servers `PDNS11/12.DOMAINCONTROL.COM` (GoDaddy parking); the site redirects to a GoDaddy lander. It is a parked domain, not an active project. |
| **educationatlas.org** | **Taken, and active** — by a different project | Registered 2026-10-21, registrar Porkbun, name servers Porkbun. The site is live: "Атлас освіти України · Education Atlas" — an open catalogue of Ukrainian education data, maps and analytics (in Ukrainian). It is *not* ours. |
| educationatlas.net | Appears available | Verisign RDAP returns 404 (no registration object); no A record. |
| educationatlas.io | Appears available | Identity Digital RDAP 404; no A record. |
| educationatlas.study / .academy | Appear available | RDAP 404; no A record. |

Options, in order of the brief's preference:
1. **Publish under educationatlas.net** and point it at the GitHub Pages build. Cheap, immediately available, and the name
   still reads as the project. Add a note on the site explaining the relationship to the Ukrainian .org project so the
   two are not confused.
2. **Make an offer on educationatlas.com.** It has been parked for years with a 2027 expiry. A GoDaddy broker or a
   "make offer" route is the only way; expect a four-figure ask. Not worth it before the paper is submitted.
3. **Avoid the collision entirely** with a different name (e.g. `generativecomparative.education`, `atlas.education`).
   Check availability before registering; the exact spelling matters for citations.

**Decide:** register one domain (recommended: educationatlas.net) and point it at the GitHub Pages site; do not chase the
.com before submission.

---

## C2. Licences: the decision page

Full analysis in `LICENSES.md`. The three choices it asks Trey to make:

1. **Code licence.** The draft recommends **MIT**. Apache-2.0 is the alternative only if the "inspectable models" platform
   with outside contributors and institutional users becomes real; it is not the right call for a single-author research
   repo today. *Decide: MIT (recommended) or Apache-2.0.*
2. **Eight boundary datasets.** Of the 12 bundled CSVs, 4 are clearly reusable with attribution (PWT 10.0 CC BY 4.0,
   Maddison 2020 CC BY 4.0, World Bank HCI and LAYS per World Bank dataset terms) and **8 are boundary**: Barro-Lee /
   Lee-Lee ("all rights reserved, citation only"), Altinok-Angrist-Patrinos (World Bank WP 8314 — licence varies per
   Work), ILOSTAT 2017 (pre-3-May-2023 ILO datasets have no automatic CC licence), UN WUP 2018 and WPP 2015 (OWID
   records CC BY 3.0 IGO but the UN site terms are non-commercial), Szirmai/UNESCO-yearbook compilation, and the
   LIS-derived Gini. If the repository is public in its current form it redistributes all twelve.
   *Decide: (a) public repo with a `data/` split and download instructions for the boundary files (recommended; the repo
   stays legal and reproducible), or (b) seek written permission from each provider, or (c) keep the repo private.*
3. **Kimi's interface code** (`reference/education_worlds_react_v0.6/`, the design the app follows). Four questions in
   `LICENSES.md` §6: was it written by Kimi personally or under a client contract, is there an assignment of rights, what
   licence did it carry, and may it be redistributed as reference material. *Decide after asking Kimi — do not publish
   that folder until answered.*

**Decide:** approve MIT; choose data split vs permissions; send Kimi the four questions.

---

## C3. Bjørn: send the chapter map and set the "schools as protection" session

Attachment: `docs/book_chapter_map.md` (14 rows, each chapter tied to a world, a test and a result, with a proposed role
for Bjørn and five questions for him). A sendable covering note:

> Dear Bjørn,
>
> I have pulled the book into a one-page chapter map: each chapter now names the world that carries it, the test it rests
> on, and the honest failure it has to report. The map is attached. The chapters I would most like your hand in are the
> ones where the protection argument has to become rules — Chapter 4 (schools as protection, Cambodia) and Chapter 7
> (the household and the floor). Three things I would like to settle in a session:
>
> 1. The chapter split. I have proposed C/M/F/E marks (conceptual, methods, fieldwork, empirical); you may want to move
>    the fieldwork chapters depending on how much of your US Department of Labor material we can use.
> 2. The protection package's magnitudes. The simulator codes safety, feeding, OVC support, flexible timetables and
>    bridging classes, but the sizes are placeholders. What can we defend from Nordtveit (2010, 2016) and the fieldwork
>    countries (Cambodia, Myanmar, Rwanda, Benin, DRC)?
> 3. Chengdu. It is a small second case that tests the same architecture on documented fieldwork; does it belong in this
>    book or in a separate paper?
>
> For a time: any week in the next month works for me; 90 minutes over Zoom. I will bring the chapter map, the current
> Cambodia protection results (child labour roughly 14% in the model against 10.7% in the 2012 survey — a test the model
> does not pass yet) and the list of what would change our minds.
>
> Trey

**Decide:** send the note; book the session; after it, update `docs/book_chapter_map.md` with his roles and set the
protection magnitudes in `web/childlabour.js`.

---

## C4. Journal: CER vs IJED vs Comparative Education

The methods paper outline (`docs/methods_paper_outline.md`) already carries the fit notes. The comparison that matters:

| | **CER** (Comparative Education Review) | **IJED** (International Journal of Educational Development) | **Comparative Education** (UK) |
|---|---|---|---|
| Audience | comparative education scholars, theory + empirical | development and policy researchers | comparative education, humanities-leaning |
| Natural home for | the "generative comparative education" programme paper — it is a *comparative education* audience and the paper is about how to build comparative explanations | the China/Cambodia empirical papers, and the methods paper if framed as development policy | the book's theoretical chapters, and the Cambodia/China historical framing |
| Fit with a simulation + history-matching methods paper | good on framing, less on methods; reviewers may ask for conventional data | good on the development question, tolerant of methods, but wants policy implications | risky: methods-heavy computational work is atypical |
| Length (confirm against current author guidelines before submitting) | ~8,000–10,000 words | ~8,000–9,500 words | ~8,000 words |
| Open access | hybrid | hybrid | hybrid |

**Recommendation:** submit the methods paper to **CER** first (it is the programme's home audience and the contribution is
about comparative explanation), with **IJED** as the fallback after a revise-and-resubmit. Submit the China and Cambodia
empirical papers to IJED. Confirm exact word/format limits on the journals' own author pages before submission — the
numbers above are targets from the outline, not verified limits.

**Decide:** confirm the target order and the author list (Trey alone or with Bjørn) before submission.

---

## C5. Cambodia microdata: request letters

The four datasets and who holds them:
- **CSES 2019 (and 2021 if released)** — Cambodia Socio-Economic Survey, education spending by item, enrolment by age and
  quintile. National Institute of Statistics (NIS), Ministry of Planning.
- **LFS 2019** — labour force survey; the degree-holder informal share and occupation earnings.
- **2012 Cambodia Child Labour Survey** — the child-labour test data behind the 10.7% figure.
- **Education administrative data** (MoEYS EMIS) — by province, for the spatial board.

Draft request (adapt to the NIS form):

> Subject: Request for CSES 2019, LFS 2019 and the 2012 Child Labour Survey microdata for doctoral research
>
> Dear National Institute of Statistics,
>
> I am Dr James "Trey" Menefee (PhD, University of Hong Kong), an independent researcher working on a comparative study
> of education, child labour and labour markets. I would like to request access to the following microdata for
> non-commercial research: the Cambodia Socio-Economic Survey 2019 (and 2021 if available), the Labour Force Survey 2019,
> and the Cambodia Child Labour Survey 2012. The work studies how schooling decisions and child labour respond to
> household budgets and to the returns to credentials; the outputs will be academic papers and an open education-atlas
> model, with no re-identification and no redistribution of the microdata.
>
> I can provide my institutional details, a data-use undertaking, and a description of the security arrangements for the
> files. Please let me know the application form and fee, if any.
>
> Yours sincerely,
> James "Trey" Menefee
> trey.menefee@gmail.com · +852 6017 8306

Fallback while the request is pending: **Cambodia DHS 2021–22** (public, with wealth-quintile attendance) is the one table
that would settle the relational-floor test (`docs/relational_floor_test.md`), and it needs no request.

**Decide:** send the request in your own name with an institutional affiliation if you have one; meanwhile pull the DHS
2021–22 table.
