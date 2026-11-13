# Education Atlas: comparative historical reconstruction

Start with CASEBOOK.md. The casebook connects the cases already present in the Atlas to primary research and explicit model tests. This is a researched first assembly, with unresolved identification and data requirements recorded.

Run `python3 reconstruct_cohorts.py` with Python 3.9 or later. No dependencies are required. It writes `cohort_results.json` beside the script and checks cohort conservation, the Philippine intake gap, Hong Kong's double cohort, and separate admission quotas. These are synthetic accounting benchmarks under stated assumptions; national historical outcomes remain research targets.

`philippines_enrolment.json` transcribes CHED's reported total, public and private higher-education headcounts for AY2015–16 through AY2019–20. `case_registry.json` records mechanisms and evidence status. Original Atlas files are unchanged. The scripts here are standalone, pending integration into the Atlas engine.
