# What we learned in this session — Angkor charter-fiscal modelling, 22 Nov 2026

A record of one long working session: what was asked, what was built, what survived, what
died, and what a reader should not repeat. Written after the compute server went down, so
everything here is either measured or explicitly marked as unverified.

---

## 1. The question

Why would a low-density agrarian polity such as Angkor (9th–15th c.) rise, peak and then
transform — and can that shape be produced from endogenous fiscal mechanisms alone, with no
scripted 1431 collapse and no imposed disaster?

A second question followed: what is this kind of polity called in the literature?
**Answer: a charter state** (Victor Lieberman, *Strange Parallels* vols. 1–2, 2003/2009) —
his own coinage, distinct from Wolters' *mandala* and Tambiah's *galactic polity* in one
specific way: legitimacy is an inherited, **relocatable** stock, so the polity survives losing
its capital. The settlement form is separately **low-density agrarian urbanism** (Roland
Fletcher; Lucero, Fletcher & Coningham 2015). These are two different objects — polity and
settlement — and conflating them is the field's most common error.

---

## 2. What was built

Nine engines, in order, each written because the previous one could not answer the question:

| engine | architecture | why it existed |
|---|---|---|
| v1.0 (pre-existing) | 140-cell grid, 30 parameters | the original; found to be structurally starved |
| v1.1 | + granary, + crown dues | proved the starvation was fixable, not diagnostic |
| charter v2–v4 | stocks: pop, charter, reach, grain | four rewrites; **all plateaued** |
| v5 | endowment ratchet alone | first mechanism that produced an interior peak |
| v6 | switchable mechanisms, 2⁵ factorial | found charter is necessary (+0.62) |
| v7 | space-explicit rings, endogenous reach | resolved a v6 contradiction |
| v8 | + maintenance-funded productivity | the coupling that makes climate matter |
| v9 | agent-based: 400 settlements, classes, rent, migration | "stand the society up" |
| v10–v12 | agent model with fiscal coupling, real budget, shock routing | the coupling fix that works |
| p1/p2 | priors with derivations; prior-predictive test | the test that refuted the calibration |

---

## 3. What survived

**Charter is necessary.** In a 2⁵ factorial (3,072 runs) every cell without a relocatable
legitimacy stock had P(rise–peak–relocation) = 0. Main effect +0.62. Without it a fiscal
crisis is terminal rather than a relocation.

**The fiscal-crossover mechanism works.** Revenue is a tax on the *non-alienated* share of
production, discounted by haul cost and net of garrison; obligations are stipends, upkeep and
defence. When revenue stops covering obligations, legitimacy erodes, and the capital moves.
This produces an interior peak and a lagged relocation with **no** climate shock and **no**
military defeat. In the agent model, closing the fiscal → water → harvest loop raised the
interior-peak rate from 0.00 to 0.99 of 672 runs; the ablation with that loop off returned
peak 1583 and zero relocations. **The coupling is the mechanism.**

**Raiding is harmful, not neutral.** Main effect −0.254. Capture adds population without
adding taxable land. The "Rome model" is not a rival explanation; in these engines it destroys
the shape.

**Yield is a scale parameter.** Morris score 0.013 against `endowRate` at 7.0 — a 500-fold
gap. The yield band changes absolute population size, not the timing of the peak or the
relocation. This settled a hypothesis the user raised (that Angkor's yields resembled
pre-Green-Revolution regional yields): the hypothesis is right about the *level* (1.0–1.6 t/ha
for a flood-recession regime) and irrelevant to the *dynamics*.

**Transport geometry does not drive aggregate dynamics.** With explicit rings, haul half-life
scores 0.000 in Morris. Reach becomes an output (~30–50 km) rather than a parameter.

**The endowment ratchet and elite overproduction are one axis, not two.** A 6×5 surface shows
raising elite growth pulls the peak earlier at every ratchet level. There is a single axis
from "slow squeeze" (peak 1600, no fall) to "fast squeeze" (peak 838).

**Charter erosion rate sets the lag, not the peak.** Varying it 0.001 → 0.02 moves the
relocation lag from 154 years to 17 while the peak stays at 913. Clean separation of *why it
peaked* from *how long it held on*.

---

## 4. What died — including claims made in this session

Listed because a record that only keeps the survivors is useless.

| claim | status |
|---|---|
| "Food is not the binding constraint" | **Wrong.** 750k × 200 kg ÷ 1.3 t/ha = 1,150 km², essentially the whole complex with no fallow. The identity is probably wrong somewhere, not the constraint absent. |
| "Over-extension (the Rome model) is excluded" | **Circular.** Reach was bounded by fiat, so over-extension could not occur by construction. |
| "Drought is excluded because the peak year does not move" | **Circular and worse.** There was no interior peak to move, *and* cultivation was reallocated each year to meet demand, so a harvest shock cancelled out before it could matter. The model could not express a drought. |
| "Charter and ratchet bracket 1150" | **Wrong.** One axis, not two. |
| "Transport attenuation can substitute for the ratchet" | **Artefact** of a scalar multiplier in v6 doing double duty; it vanished once rings were explicit. |
| "`Z5 pd4500` fits Angkor: peak 1099, pattern 1.00" | **Tuning artefact.** The same engine under derived priors peaks at 857. |
| v9 ABM "stands up a society" | **Half true.** It stands up classes, rent, distress sales and land concentration, but it is parameter-deaf: monument and upkeep spending returned bit-identical output because they never reached an agent. |

---

## 5. The robust negative result

Three *independent* architectures — v8 stock, v9 agent, v12 agent — were run on the same 300
prior draws:

| architecture | median peak year | P(peak 1000–1400) | P(full pattern) |
|---|---|---|---|
| v8 stock | 877 (CI 800–974) | 2% | 1% |
| v9 agent | 1600 (never peaks) | 0% | 0% |
| v12 agent | 857 (CI 833–876) | 2% | 0% |

At the **derived** endowment rate (0.00045–0.0026/yr, from "temples held 30–50% of cultivated
land by c.1300"): 876 and 857.

**Everything peaks roughly 300 years too early, and converges on that wrong answer from
different architectures.** That convergence is the point: it is not an implementation bug. The
land-endowment ratchet, at defensible rates, is too fast by about a factor of three.

---

## 6. The leading hypothesis, stated testably

**The ratchet cannot bite until the land frontier closes.** While unclaimed land remains,
alienating a holding costs the crown nothing because another can be cleared. The fiscal
squeeze should therefore begin when cultivated area approaches its ceiling — mid-12th century
— not at founding.

Prediction: **the fiscal crossover date should track the frontier-closure date, not the
founding date.** Frontier closure is guessable from the same identity that constrains
everything else (~1,150 km² at 750k people, 200 kg, 1.3 t/ha).

This is the single experiment worth running next, and it has a date attached, which is what
makes it falsifiable rather than another knob.

---

## 7. Method lessons that generalise

1. **Encode guesses as priors with derivations, not ranges.** `p1_priors.js` carries, per
   parameter, a distribution, a 90% interval, *why*, and *what evidence would replace it*.
   Two of the nine are derived from identities a reader can check.
2. **Detect dead parameters by bit-identical output.** If two different policies give the same
   trajectory to the last digit, that parameter never reaches an agent. This caught the
   monument/upkeep degeneracy and, earlier, an unbounded prestige term that pinned charter at
   1.0 forever.
3. **Prove a mechanism by ablating it.** The coupling claim rests on `swCouple=0` returning
   peak 1583 and zero relocations, not on the coupled model looking plausible.
4. **Never tune to the target and then report the fit.** A tuned model and a validated model
   produce identical output; only the prior-predictive run distinguishes them.
5. **Four rewrites of the same engine means the architecture is wrong.** v2–v4 all plateaued
   because every version had exactly one feedback loop (food → population). Interior peaks
   need a fiscal stock.

---

## 8. Infrastructure

- Compute: AutoDL container, 96 vCPU, RTX 2080 Ti (unused — all work was CPU-bound), Ubuntu
  22.04, Node 12. **Taken down at the end of the session.** Cloud root `/root/angkor`.
- Local: `/var/minis/workspace/angkor/` — `scripts/`, `research/`, `results/`, `rounds/`, `release/`.
- Record: branch `research/angkor-charter-2026-11` on `TreyModels/atlas-of-education`, parented
  on `main`, ~47 files.
- Scale: the experiment suites run in seconds on 90 cores; the agent model is ~0.2 s per run
  on x86 and ~8 s under emulation, which is why everything was sharded.

**Security note:** the SSH deploy key used during the session was pasted into a chat log and
should be treated as compromised and rotated. It is scoped to this one repository and cannot
create forks.

---

## 9. Open questions

1. Does frontier closure gate the ratchet? (The one experiment that matters.)
2. Two-way land market: dispossession is currently a one-way ratchet, which is why revenue
   decline overshoots (0.55–0.85 against a target of >0.30).
3. Why is elite land share so high (0.59–0.77) when the peak is reached? Plausible only if
   temple holdings are being counted as elite holdings.
4. Does anything in the inscription corpus give a *share* of cultivated land under temple
   control by century? No such number was found. Until one is, `endowRate` remains derived
   rather than measured.
5. Can a charter state be distinguished archaeologically from a collapsed one? If not, the
   relocation framing is unfalsifiable and the whole exercise is literary.

---

## 10. Local reproduction (server down)

Re-run after the compute server was taken down, single-core under emulation, to confirm the
headline numbers are not machine artefacts:

| run | n | median peak year | P(peak 1000–1300) | P(full pattern) |
|---|---|---|---|---|
| v8 stock, server (x86) | 300 | 877 | 2% | 1% |
| **v8 stock, local (emulated)** | **200** | **879** | **3%** | **1%** |
| v12 agent, server (x86) | 240 | 857 | 2% | 0% |
| **v12 agent, local (emulated)** | **8** | **859** | — | — |

The stock model reproduces to within 2 years and the agent model to within 2 years on 8 draws
(6.9 s per run emulated against ~0.2 s native). The negative result is a property of the
model, not of the machine.

Also measured locally: only **36%** of prior draws produce a land area that can feed the
700,000 people Carter et al. treat as a lower bound. That is a second, independent way of
saying the same thing — the land/yield/diet identity is at the edge of consistency across
most of the defensible parameter space.

Raw output: `results/p1_local.csv`, `results/p2_local.csv`.
