# Search strategy (Synthetic Council, task-42)

Layers, in order, with the recorded artefacts:

1. **Internal inventory.** Walked every verified branch (`git ls-tree` over all `research/*` branches) and read the
   dashboard (`2026-11-23-dashboard` @ `2f8993c`) plus every `research/records/2026-11-2[345]-*/README.md` and the
   paper drafts. 42 claims inventoried in `NOVELTY_INVENTORY.md`, each with branch @ commit.
2. **Independent prior-art verification.** New Crossref run: `lit/fetch_candidates.py`, 31 bibliographic queries
   (child-survival/mortality-fertility; structural transformation/sequencing; mass-education/world culture;
   rebound/lowest-low fertility; multiverse/vibration-of-effects; ABC methods; critical transitions; agricultural
   transformation), each query's top match then resolved by DOI against `api.crossref.org/works/{DOI}` and stored
   in `lit/candidate_refs.json` with a status. All 31 resolved (V); working-paper-only versions are marked W in
   `CANDIDATES.md`.
3. **Diff against prior audits, not substitution.** The earlier novelty ledger (`research/novelty-2026-11-23` @
   `390db8d`) and the independent lit audit (`research/lit-audit-2026-11-24` @ `83d2973`, plus its Paper F final
   read) were read and diffed. Where they name a candidate or a "not new" item, this record says whether it agrees
   (`CANDIDATES.md`), and no lead's `claims-prior-art.md` was used as evidence without re-checking its DOIs.
4. **Closest-competitor rule.** For each (a)/(b) candidate, one work is named as the closest competitor and the
   difference is stated in one sentence. Where no DOI-verified competitor exists (threshold hinges), the record
   says so rather than implying a literature.

**Limits.** Crossref bibliographic matching is title-oriented; books/chapters without DOIs are hand-cited and
marked U (notestein1945, Becker 1960, Trow 1974, Van Imhoff & Post 1998, Heaps 1975). Grey literature, non-English
work and very recent working papers are underrepresented; "not documented" in this record means "not found by
these queries", not an exhaustive census. The 69%/68.75% sequencing-ordering figure is treated as **UNRESOLVED**
and retracted by its own paper; Paper M's corrected strict ordering is 37.5% [26.6–50.0] with 31.3% simultaneous
and is the only ordering number any candidate may use.
