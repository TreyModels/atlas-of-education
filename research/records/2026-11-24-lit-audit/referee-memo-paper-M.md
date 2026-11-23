# Referee-attack memo — Paper M (massification omnibus)

Independent auditor: `novelty-review`, 24 November 2026. Drafted from the claims as scoped by the lead and from
Crossref-verified prior work (see `claims-map.md`, Paper M tables). The branch was not yet pushed at drafting time;
this memo will be checked against the lead's `claims-prior-art.md` when it appears.

## Objection 1 — "Schools before factories" is not a new finding
*"Sweden had mass literacy before industrialisation — Sandberg called it the 'impoverished sophisticate' in 1979.
England's literacy rose before the factory system (Mitch 1992). The world-polity school has argued since the 1980s
that mass schooling was supply-led and spread by institutional imitation, not by industrial demand
(Boli, Ramirez & Meyer 1985, *Comparative Education Review* 29(2), 10.1086/446504; Meyer, Ramirez & Soysal 1992,
*Sociology of Education* 65(2), 10.2307/2112679; Ramirez & Boli 1987, 10.2307/2112615). What is new here?"*

**Can the current evidence answer it?** Yes, but only by reframing. The defensible claim is not "schools came
before factories" (known) but **"we systematically code the sequence for 61/64 countries and run a supply-versus-demand
horse race on the coded data"**. The paper must cite Sandberg 1979 as the canonical case, the world-polity school as
the prior supply-led account, and claim the *systematic measurement*, not the direction. If the draft contains "we
are not aware of evidence that schooling preceded industrialisation", that sentence must go.

## Objection 2 — The dates and the coding are the paper
*"Your 61/64 result is only as good as your date choices. When is 'mass schooling' achieved — enrolment share,
compulsory laws, literacy? When does 'factory employment' begin — first mill, 10% of employment, steam? A different
coding gives a different count."* Referee ammunition: Benavot & Riddle 1988 (10.2307/2112627) and Meyer et al. 1992
for cross-national enrolment series; Lindert 2004 (10.1017/cbo9780511510717) for public-schooling dates; Goldin &
Katz (10.3386/w6439) for the US; Becker & Woessmann 2009 (10.1162/qjec.2009.124.2.531) for Prussia; Squicciarini &
Voigtländer 2015 (10.1093/qje/qjv025) and de Pleijt & van Zanden 2016 (10.1093/ereh/hew013) for the
human-capital-before-industry argument.

**Can the current evidence answer it?** Only with a **date-by-date source table** and a robustness exercise: recode
with alternative thresholds and report how many of the 61/64 flip. Without that, one spot-checked date (a referee
will pick two) can discredit the headline. This is the paper's central empirical vulnerability.

## Objection 3 — The supply-versus-demand horse race is under-identified
*"Both supply and demand correlate with development, state capacity and the demographic transition. A horse race
without exogenous variation is a decomposition, not a test."* Referee ammunition: the world-polity vs human-capital
debate is decades old; Galor & Moav 2006 (10.1111/j.1467-937x.2006.00370.x) and Becker & Woessmann 2009 provide the
demand-side theory; Acemoglu & Restrepo 2018 (10.1257/aer.20160696) for mechanisation/labour-demand channels.

**Can the current evidence answer it?** Partly. If the paper (a) calls it a decomposition, (b) reports the
correlates it cannot separate, and (c) names the natural experiment it would need (compulsory-schooling laws,
church-state competition, colonial schooling policy), it survives. If it claims "supply caused massification", the
objection lands. A referee will also note that the massification-drivers null (electricity, wage jobs) is a
different claim from the sequencing one and must not be used to imply demand does not matter.

## Two secondary referee risks

- **Scaling/θγ section.** Bettencourt et al. 2007 (10.1073/pnas.0610172104) and Yang et al. (2026, arXiv 2208.06487)
  are cited for scaling laws, but the project has **not fitted θ or γ**. Presenting the formalism as a tested claim
  will be rejected; it must be a diagnostic frame with the data gap stated (occupation depth, credential counts).
- **Credential inflation.** Collins (1979/2019, 10.7312/coll19234), Spence (1973, 10.2307/1882010) and Arrow (1973,
  10.1016/0047-2727(73)90013-3) have made this argument for fifty years. "We are not aware" fails outright; the
  contribution can only be the **2,000:1 credential-to-occupation measurement**.

## Verdict for this paper

The defensible claim is the **systematic 61/64 sequencing measurement plus the supply/demand decomposition**, framed
as systematising a known historical pattern (Sandberg 1979; world-polity school) — never as discovering it. The
paper is publishable as an economic-history/comparative-education audit if the date table and coding robustness are
in the paper (not the appendix) and if the scaling/θγ material is labelled diagnostic. The weakest parts are any
causal reading of the horse race and the scaling section.

## Citation-integrity watch list for when the branch pushes

Every date in the 61/64 table needs a named source; every refs.md DOI must be checked against Crossref metadata (not
just resolution) — Paper F's refs.json had seven entries resolving to the wrong paper, so Paper M gets the same
check. The sibling `paper-boppart-2026-11-24` refs.md is careful; the omnibus must not regress that standard.
