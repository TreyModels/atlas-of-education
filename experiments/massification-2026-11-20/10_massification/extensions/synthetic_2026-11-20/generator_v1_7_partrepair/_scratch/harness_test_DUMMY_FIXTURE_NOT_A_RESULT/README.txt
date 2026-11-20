PRE-FREEZE HARNESS ARTIFACT -- NOT A RESULT.

These files were produced by `code/sim_v1_7_partrepair.py --harness-test` BEFORE the
freeze, on (i) a demographic path reconstructed from the frozen v1.3 panel and (ii) a
constant 90.0 scoring fixture in 11 arbitrary years per level. The "observed" column here is
that fixture, NOT the PHL series; the "count" in observed_path_A17.csv is therefore
meaningless and must never be quoted. No observed file was opened and no real count was
computed. What the artifact does establish: the whole pipeline (arms, panels, scoring,
crossings, representation, G2/G3/G4/G7/G9, writers) runs end to end, the phase guard blocks,
and the identity guards hold on their declared column sets. See TUNE_LOG.md sec.1.
