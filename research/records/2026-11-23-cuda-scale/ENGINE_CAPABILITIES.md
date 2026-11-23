# What the GPU life-course engine can do

*One page, plain words, for readers who will not read the code. Measured 23 November 2026 on one
NVIDIA RTX 2080 Ti (a consumer graphics card with 11 GB of memory). Full detail and every raw number
are in `README.md` and the `results/` files.*

## What it does

The engine follows the life course of synthetic women, one at a time: whether they go to school and
for how long, whether and when they marry, and how many children they have by when. Each simulated
woman belongs to a birth cohort, a town or country setting, and a wealth group. Thousands of women
are simulated at once on the graphics card, and many complete "what-if" settings can be run side by
side in the same pass. It is the same kind of model as the published CPU version, but it is a
**different engine** in how the marriage market is settled; the differences are documented elsewhere
and no claim is made here that it reproduces the published model.

## How fast, at what scale

| Question | Answer |
|---|---|
| How many women at once? | **66.8 million** in a single run of the card (11 GB of memory filled) |
| How fast? | about **5 million women per second**; 10 million women take about 2 seconds |
| 100 million women? | two runs back to back: **18 seconds** of computing, about **51 seconds** end to end |
| How much memory per woman? | about **165 bytes** — this is the hard ceiling: memory ÷ 165 = maximum women |
| How long a real analysis? | a fit that needs 10,000 parameter settings is about 400 million woman-records, roughly 75 seconds of engine time; 100 million women is a coffee break |

These are measured, not estimated. Each was timed several times and the spread is about 4%, so
treat small differences as noise. The largest single run was pushed until the card ran out of
memory, to establish the ceiling honestly.

## What is reliable, and what is not

- **Reliable:** run the same settings twice with the same seed and the same batch size, and every
  simulated woman gets exactly the same life. The raw outputs are identical to the last digit.
- **Reliable:** turning the graphics-card optimization on or off does not change any woman's life.
- **NOT reliable:** changing how many women are bundled into one pass changes the answers — by up to
  1.1 births per woman and 1.7 years of marriage age in a controlled test. The random numbers are
  tied to position inside the pass. **A reproducible analysis must fix the pass size.** This is a
  real limitation, found by this audit, and it contradicts a comment in the engine's own notes; the
  note should be corrected.
- **Stable:** the card does not overheat or slow down across repeated runs (temperature 39–46 °C, no
  downward trend; variation is 4%, from start-up and copying results, not heat).

## Limits, plainly

- **One card, not a supercomputer.** Everything here is a single 11 GB consumer GPU. Wanting more
  women than 67 million means running several passes, not one bigger pass.
- **The 100-million figure is two passes**, not one; the second pass repeats the whole run.
- **No mid-run save.** A pass either finishes or is restarted.
- **The memory ceiling is fixed by the model's state**, not a tuning knob: about 165 bytes per woman.
- **The engine does not validate the science.** Size gives precision and the ability to ask many
  questions at once; it does not make the model's assumptions more true.

## Ready to be called from a larger pipeline?

Yes, with one condition: fix the batch size in the configuration. The engine is called like an
ordinary function — settings in, results out — and the caller needs no graphics-card knowledge. It
was repeatedly started fresh, given different amounts of memory, and asked for the same answers; it
delivered them exactly. The batch-size caveat is the one thing a caller must respect to get
reproducible results.
