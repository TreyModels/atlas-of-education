# Same Score, Same Chance

James W. Menefee III, 27 November 2026.

Read paper.pdf for the paper. manuscript.md contains detailed methods, equations and exploratory diagnostics. FORMAL_AUDIT.md and RELEASE_CHECKS.md document checks and remaining limitations.

This is an exploratory simulation of synthetic cohorts. Model parameters are not calibrated to Guangzhou pupil records. The paired scenarios do not identify Double Reduction's causal effect.

Reproduce with Python 3 and NumPy:
- python sweep.py
- python summarize.py
- python repeats.py > repeats.csv

Check the stated mathematical propositions with Lean 4.36.0:
- lean Admission.lean

Build the PDF with Python, ReportLab, NumPy and Georgia/Arial or Liberation fonts:
- python illustrate.py

illustrate.py writes the paper to the parent directory. The release also includes paper.pdf at this directory's root for convenience. Charts are generated from the included draw-level outputs. ASSUMPTIONS.md documents the inputs and structural rules.

The 150-setting mechanism experiment and 1,024-setting principal experiment are documented separately. All experiments are exploratory. No interview transcript or personal pathway is included.

Please contribute source-linked corrections through issues or pull requests. Specify population, year, units, estimate, uncertainty and proposed parameter range.

Earlier release DOI: https://doi.org/10.5281/zenodo.24575246
Collection DOI: https://doi.org/10.5281/zenodo.24369167
Revision 1.1: https://github.com/TreyModels/atlas-of-education/releases/tag/v2026.11.27-guangzhou-r1

AI assistants helped draft code, text, figures and proofs. The author is responsible for the final scholarly interpretation. License follows the Atlas repository, CC BY-NC 4.0.
