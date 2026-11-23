# Candidates: four-way classification, independent prior art, and the killing

Every candidate below was checked against the inventory (`NOVELTY_INVENTORY.md`), the independent lit audit
(`research/lit-audit-2026-11-24` @ `83d2973`), the earlier novelty ledger (`research/novelty-2026-11-23` @
`390db8d`), and a fresh Crossref verification run (`lit/candidate_refs.json`, statuses V/W/U per work). The
leads' claims files were read and diffed, not trusted. Classification: **(a) NEW CORRELATION**, **(b) NEW
ASSEMBLY**, **(c) NEW METHOD**, **(d) KNOWN/REPLICATION**. No candidate is classified (a): nothing in the
programme is a relationship the field has not documented. DOI status: V = Crossref resolves matching metadata;
W = working-paper/pre-publication version; U = no DOI, hand-cited.

## Candidate 1 — Multiverse resolution arithmetic / the grouping-multiverse design rule — **(c) NEW METHOD**

**Claim.** How many random re-groupings a cross-national multiverse needs is a function of how many links pile
up at the p-value floor: a lone link needs ~5,440 draws; a cluster of ~30 links needs ~182; at 400 draws, 35
links were certified because a 30-link cluster cleared Benjamini–Hochberg. The accompanying methods paper
(`research/methods-multiverse-paper-2026-11-23` @ `f9673a9`, 12.3k words) turns this into a design rule.

**Independent prior art.** Patel, Burford & Ioannidis (2015) vibration of effects, 10.1016/j.jclinepi.2015.05.029,
**V** — the closest methodological ancestor, but it maps specification sensitivity, not the number of random
groupings needed to certify a link. Young & Holsteen (2017) model uncertainty/robustness,
10.1177/0049124115610347, **V** — computational framework for model uncertainty, not a re-partition power rule.
Steegen et al. (2016) multiverse analysis, 10.1177/1745691616658637, **V** — the multiverse method itself.
Simonsohn, Simmons & Nelson (2020) specification curve, 10.1038/s41562-020-0912-z, **V**. Del Giudice &
Gangestad (2021) multiverse guide, 10.1177/2515245920954925, **V**. Silberzahn et al. (2018) many analysts,
10.1177/2515245917747646, **V**. Benjamini & Hochberg (1995), 10.1111/j.2517-6161.1995.tb02031.x, **V**; Phipson
& Smyth (2010), 10.2202/1544-6115.1585, **V** (the two statistics the rule combines).

**Closest competitor:** Patel et al. (2015).
**What is new:** the explicit *draw-count* rule linking certifiable-link count to needed random groupings, and
the demonstration that the rule predicts what 400 draws certified — an unstated design rule rather than a new
statistic. **What is replicated:** every component statistic; the multiverse framing. **Verdict: NEW METHOD,
incremental-new.** Referee risk: the rule's dependence structure (cluster homogeneity) is an assumption to state.

## Candidate 2 — "Schools before factories": the schooling-before-agricultural-release sequence — **(b) NEW ASSEMBLY**

**Claim.** Across 61 of 64 country cases, mass schooling take-off precedes the release of labour out of
agriculture; the programme calls this a **late-industrialiser regularity, not a universal law**, and Paper M's
own corrected ordering figure is **strict schooling-first 37.5% [26.6–50.0], simultaneous 31.3%** (the source
JSON's 68.75% counted ties as schooling-first and is **not used**). The assembly combines supply/demand
decomposition, historical case sequencing, the agricultural floor/Boppart model, and the 400-grouping multiverse.

**Independent prior art.** Porzio, Rossi & Santangelo (2021) "The Human Side of Structural Transformation",
10.3386/w29390, **W** (NBER working paper; published version not verified in-session) — **closest competitor**:
human-capital accumulation and structural transformation, with a micro foundation; it does not assemble the
cross-country sequence of schooling before agricultural release that Paper M assembles. Herrendorf, Rogerson &
Valentinyi (2014) growth and structural transformation, 10.3386/w18996, **W** — the structural-transformation
survey. Lewis (1954), 10.1111/j.1467-9957.1954.tb00021.x, **V**; Timmer (1988) agricultural transformation,
10.1016/s1573-4471(88)01011-3, **V**; Galor & Moav (2006) "Das Human-Kapital",
10.1111/j.1467-937x.2006.00370.x, **V**. World-culture/institutionalism: Boli, Ramirez & Meyer (1985),
10.1086/446504, **V**; Soysal & Strang (1989), 10.2307/2112831, **V**; Benavot & Riddle (1988),
10.2307/2112627, **V**. Economic history: Sandberg (1979) impoverished sophisticate,
10.1017/s0022050700096418, **V**; Mitch (1992) popular literacy, 10.9783/9781512807189, **V**.

**Closest competitor:** Porzio, Rossi & Santangelo (2021).
**What is new:** the systematic multi-country sequencing of schooling take-off *before* agricultural labour
release, with a supply/demand decomposition and a quantified agricultural floor; the pieces are known but the
assembled sequence is not. **What is replicated:** each component (education demand, world culture, state
building, structural change). **Verdict: NEW ASSEMBLY, incremental-new** — but the candidate **must not** use
the retracted 69% figure; the corrected 37.5% strict ordering with 31.3% simultaneous is the number to carry,
and a referee will ask whether ties reflect genuine simultaneity or dating resolution.

## Candidate 3 — GPU full-transition counterfactual (mortality-freeze on the individuation model) — **(b)/(c) NEW ASSEMBLY / DEMONSTRATION**

**Claim.** A bit-exact GPU port of the individual-level dose model, with a calibrated child-mortality channel,
runs the 1930–1995 transition for eight countries and freezes mortality at pre-antibiotic levels. The collapse
survives: freezing removes 3.2% of the fall (range −1.8 to +8.2%), 0.9–4.7% under a ±50% channel band, 10% under
a 4.5× power check; the development-only arm loses 2.0%. The individuation scenario does not beat
development-only out of sample (24.43 vs 21.10, +3.32 [−3.76,+11.14], 3/6). The pre-antibiotic arc is
unreachable by the model (4.01→4.94→4.64; max 5.20/5.42).

**Independent prior art.** Transition theory: Notestein (1945) *Food for the World*, **U** (hand-cited); Davis
(1945), 10.1177/000271624523700102, **V**; Davis (1963), 10.2307/2732014, **V**; Lee (2003),
10.1257/089533003772034943, **V**; Caldwell (1976), 10.2307/1971615, **V**; Cleland & Wilson (1987),
10.1080/0032472031000142516, **V**; Bongaarts (1978), 10.2307/1972149, **V**; Coale & Watkins (1986),
10.1515/9781400886692, **V** (reissue); Guinnane (2011), 10.1257/jel.49.3.589, **V**. Mechanisms: Galor & Weil
(2000), 10.1257/aer.90.4.806, **V**; Doepke (2005), 10.1007/s00148-004-0208-z, **V**; Becker & Barro (1988),
10.2307/1882640, **V**. Microsimulation lineage: SOCSIM and demographic microsimulation (Van Imhoff & Post,
1998, *Population: An English Selection*), **U** — decades old.

**Closest competitor:** no single competitor; the closest is the historical-microsimulation tradition (SOCSIM)
plus Galor–Weil/Doepke mortality-led mechanisms. **What is new:** the counterfactual magnitude on a fitted
individual-level engine (3.2%), the demonstration that the collapse is schooling-led *within this model*, and
the negative out-of-sample result for individuation. **What is replicated:** every theoretical mechanism; the
simulation method. **Verdict: NEW ASSEMBLY/DEMONSTRATION**, incremental-new, weakest as a "new finding" because
the result is a property of the calibrated model (the paper says so). Referee risk: model dependence and the
unresolved tension with the country-level child-survival link.

## Candidate 4 — Levels-vs-changes/transportability schooling–fertility audit (Paper F) — **(b) NEW ASSEMBLY**

**Claim.** Levels: all 8 measures negative-significant (women's years −0.129 (0.029)); 336-spec curve 99.7%
negative / 91.3% negative-significant / median −0.475. Changes: weak or positive (+0.111 (0.045)), 0/8
negative-significant. Transportability: 13,800 random six-group partitions reproduce the level relation in
71–99% of groups vs 0–7% for changes. Placebo: future schooling 52.9% vs correct-time 58.8% (~90% as strong) →
development gradient, not causal.

**Independent prior art.** Liu & Raftery (2020) *PDR*, 10.1111/padr.12347, **V** — **closest competitor**, the
country-level education-fertility model with between-country structure; does not do the within-change
decomposition. Kravdal (2002), 10.2307/3088337, **V** — individual vs community decomposition, conceptual
ancestor. Cleland & Rodríguez (1988), 10.1080/0032472031000143566, **V**. Herzer, Strulik & Vollmer (2012),
10.1007/s10887-012-9085-6, **V**; Murtin (2013), 10.1162/rest_a_00302, **V**. Robinson (1950),
10.2307/2087176, **V**; Nickell (1981), 10.2307/1911408, **V**; Durlauf, Johnson & Temple (2005),
10.1016/s1574-0684(05)01008-7, **V**; Eberhardt & Teal (2011), 10.1111/j.1467-6419.2010.00624.x, **V**;
Patel et al. (2015), 10.1016/j.jclinepi.2015.05.029, **V**; Angrist & Pischke (2009), 10.1515/9781400829828, **V**.

**Closest competitor:** Liu & Raftery (2020).
**What is new:** the systematic demonstration that the standard change specification erases the country-level
schooling–fertility correlation, quantified across 13,800 arbitrary partitions, with a placebo that measures the
development-gradient caveat. **What is replicated:** the within/between critique (Nickell, Robinson, Durlauf,
Eberhardt–Teal) and the level correlation itself (Barro–Lee, Liu–Raftery, Herzer, Murtin). **Verdict: NEW
ASSEMBLY, incremental** — already audited as such; not re-ranked above Candidate 1 or 2.

## Candidate 5 — Rebound ceiling and the falsification of the strong "no-off-switch" — **(b) NEW ASSEMBLY**

**Claim.** Only 34 of 396 country-episodes (8.6%, upper 11.3%) show a sustained rebound; persistence fires in
5/38 within 10 years and 9/38 long-run; a ceiling of about 1.83 births per woman bounds the rebounds; the event
study is +0.035 (0.025) with MDE 0.070, so the strong claim is falsified and only a weak form survives.

**Independent prior art.** Goldstein, Sobotka & Jasilioniene (2009) end of lowest-low fertility,
10.4054/mpidr-wp-2009-029, **W**; Myrskylä, Kohler & Billari (2009) advances reverse fertility declines,
10.1038/nature08230, **V**; Frejka & Sobotka (2008), 10.4054/demres.2008.19.3, **V**; Sobotka (2011) re-emerging
diversity, 10.3917/pope.304.0451, **V**; Koytcheva & Philipov (2008), 10.4054/demres.2008.19.13, **V**; Zakharov
(2008), 10.4054/demres.2008.19.24, **V**; Lesthaeghe (2010), 10.1111/j.1728-4457.2010.00328.x, **V**.

**Closest competitor:** Goldstein et al. (2009) / Myrskylä et al. (2009) — both document rebounds; neither
tests a strong no-off-switch claim across 396 episodes with a ceiling. **What is new:** the systematic
falsification with placebos and the ceiling parameterisation. **What is replicated:** the existence of rebounds.
**Verdict: NEW ASSEMBLY, incremental**; a specialist referee may treat it as a replication-plus-extension.

## Candidate 6 — Child-mortality level vs volatility (E1) — **(b) NEW ASSEMBLY (weak)**

Level known since the child-survival hypothesis (Taylor, Newman & Fuchs, 1976,
10.1080/00324728.1976.10412734, **V**; Preston, 1978, 10.2307/2066891, **V**; Palloni & Rafalimanana, 1999,
10.2307/2648133, **V**; Doepke, 2005, **V**; Kalemli-Ozcan, 2003, 10.2139/ssrn.306528, **W**; Soares, 2005,
10.2139/ssrn.361461, **W**). **What is new:** the country-level volatility null (level +0.0067 (0.0015),
volatility +0.0020 (0.0020), MDE 0.0046/0.0056) with circular-shift and cluster-preserving placebos. **Verdict:
NEW ASSEMBLY, weak** — publishable only inside the mechanisms paper; not a standalone paper.

## Killed candidates (do not pursue as novelty)

| candidate | reason |
|---|---|
| "Electricity does not drive schooling" | The micro literature is large and mostly positive; the programme's result is the standard common-trend warning, and the cross-country prior art exists (earlier novelty ledger and multi-universe record). **KNOWN.** |
| "Child survival drives fertility" | The child-survival hypothesis is from 1976 (Taylor et al.); the level relation is a replication. **KNOWN.** |
| "Individuation is refuted" | One poor-fitting model with unidentified strengths; the correct statement is the out-of-sample tie. **KNOWN/model artefact.** |
| Credential inflation | Positional-credential literature is old (Collins 1979); the +0.81 correlation is an audit. **KNOWN.** |
| Threshold hinges at 6/9 years | Hinges are conventional, not literature-established; no canonical DOI-verified threshold paper (auditor and our search agree). **KNOWN/U.** |
| Care-work loop / tipping point / diminishing returns | Pre-registered mechanism tests that returned nulls; the mechanism hypotheses are known (England & Folbre 1999; Scheffer 2009; Dakos 2012). **KNOWN, null tests.** |
| Scaling laws / Heaps exponent / regime break | Audits of known scaling results with a new negative (no regime break); not a new law. **AUDIT.** |
| Marriage age / UN data | Known UN data; the levels-vs-change artefact is a methods lesson, not a finding. **KNOWN.** |
| "Schooling precedes fertility" as an ordering percentage | The 68.75%/69% figure is **UNRESOLVED and retracted**; Paper M's corrected strict ordering is 37.5% [26.6–50.0] with 31.3% simultaneous. No candidate may use the retracted number. **U.** |

## Ranking (before the panel)

1. Candidate 1 — multiverse resolution arithmetic (NEW METHOD; unstated design rule).
2. Candidate 2 — schools before factories (NEW ASSEMBLY; strongest empirical assembly, ordering figure must be corrected).
3. Candidate 3 — GPU transition counterfactual (NEW ASSEMBLY/DEMONSTRATION; model-structural).
4. Candidate 4 — Paper F audit (NEW ASSEMBLY; already audited incremental).
5. Candidate 5 — rebound ceiling (NEW ASSEMBLY; replication-plus-extension risk).
6. Candidate 6 — child-mortality volatility (weak assembly; inside mechanisms paper).
