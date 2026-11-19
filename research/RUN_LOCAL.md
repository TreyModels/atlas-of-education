# Run locally

Use Python 3.10+ and Node 20+. A local coding agent, including one using DeepSeek, can follow these commands; an LLM service is optional. Keep source bytes unchanged during a planned batch, and record amendments in a new directory.

## Setup and verification

Extract the supplied ZIP. It contains sibling `atlas-of-education` and `ooa-coast-vs-herds` folders. Open a terminal in the Atlas folder:

```bash
cd atlas-of-education
python -m venv .venv
```

Activate `.venv` (`source .venv/bin/activate` on Linux/macOS, or `.venv\Scripts\activate` in Windows Command Prompt), then:

```bash
python -m pip install -r research/requirements.txt
python -m unittest discover -s research/tests -p 'test_*.py' -v
node --test research/tests/test_node.cjs
node test-worlds.cjs
```

## Execution check

Planning records the design and source/input hashes. Execution requires `run`. Smoke uses small populations and short optimization budgets; its numerical results have no substantive interpretation.

```bash
python research/lab.py plan --profile smoke --out research/runs/smoke
python research/lab.py run --out research/runs/smoke --jobs 2 --timeout 600
python research/lab.py report --out research/runs/smoke
```

Inspect `REPORT.md`, `summary.json`, optimizer diagnostics and failed trial records. Process success can coexist with scientific nonconvergence. Fix execution errors before extending a batch. Execution failures produce a nonzero exit code.

## Initial substantive batches

Budget from recorded pilot durations. Default main has 32 nuisance draws and eight seed repetitions across many structural cells; shadow education is especially costly. These smaller examples establish a starting budget, not sufficient precision:

```bash
python research/lab.py plan --profile main --families credential --draws 16 --replicates 4 --out research/runs/credential-pilot
python research/lab.py run --out research/runs/credential-pilot --jobs 4 --timeout 3600
python research/lab.py plan --profile main --families shadow --draws 4 --replicates 2 --out research/runs/shadow-pilot
python research/lab.py run --out research/runs/shadow-pilot --jobs 4 --timeout 3600
python research/lab.py plan --profile main --families camchild angkor schools fertility --draws 16 --replicates 4 --out research/runs/mechanism-pilot
python research/lab.py run --out research/runs/mechanism-pilot --jobs 4 --timeout 3600
python research/lab.py plan --profile main --families youth --draws 8 --out research/runs/youth-profiles
python research/lab.py run --out research/runs/youth-profiles --jobs 4 --timeout 7200
```

Youth `--draws` means optimizer starting points, retained independently, not posterior draws. School and fertility checks are deterministic and ignore draw/replicate counts. Increase nuisance draws and seed repetitions according to their different uncertainty roles, checking comparison stability and Monte Carlo error.

Shadow's adapter explores prior draws using corrected targets; it does not produce calibrated policy results. Recalibration is a separate expensive step:

```bash
cd experiments/shadow-abm/src/tutoring_abm
python smc.py --particles 200 --gens 16 --procs 4 --mh-sweeps 3 --evidence-n 10000 --max-proposals 1000000 --out ../../../../research/runs/shadow-recalibration
```

That working directory is four levels below the repository root. Inspect reached tolerance, importance ESS, distinct particles, proposal budget, positive evidence terms and fresh-school sensitivity. Preserve old posteriors. The probability of passing a prior-based screen does not estimate the probability that a theory is true. This standalone SMC command lacks the common runner's automatic manifest; preserve its log, exact command and installed versions, and pair it with a `lab.py plan` source-hash record before publishing. Its default subject and school mapping also need the protocol's structural sensitivity checks.

## Out of Africa

The ZIP already includes the companion checkout beside Atlas. Install its extra dependencies:

```bash
python -m pip install -r ../ooa-coast-vs-herds/requirements.txt
python research/lab.py plan --profile main --families ooa --draws 16 --ooa-root ../ooa-coast-vs-herds --out research/runs/ooa-pilot
python research/lab.py run --out research/runs/ooa-pilot --jobs 2 --timeout 7200
```

The adapter uses the companion engine/grid directly, and creates a hash-keyed sea-crossing cache beside the checkouts. Set `ATLAS_OOA_CACHE` for another writable location. Initial cache creation and JIT compilation add overhead. The alternative 1-2 km/year bracket is a sensitivity range, not a newly estimated prior. Geography, dating and preservation gaps remain in the protocol.

## Resume and review

Repeat `run` to resume: successful trials are reused and failures retried. `--limit 10` executes the first ten trials for debugging, leaving the rest pending. Edited plans or source/input drift require a new plan. Changing concurrency preserves task seeds. Use a new directory when checking dependency-version sensitivity.

`RUNNING.lock` prevents concurrent writers. Following a crash, confirm the old process has stopped before removing a stale lock. Interrupted machines can require cleanup of compiler or Node subprocesses.

Outputs contain the plan, hashes, environments, atomic trial records, summary and Markdown report. Failed solvers and nonfinite fields remain visible. The runner does not update web-page headlines. It averages seed repetitions within each draw before computing Monte Carlo error, and reports within-draw variance separately. Partial batches and variable numbers of valid equilibria can select observations; inspect completion before interpreting means.

For publication, commit the design and reviewed summary, archive raw trials persistently, identify already-inspected data and link the exact source commit. Retain contradictory outcomes. Never include secrets or personal data in a run archive.

## Rigor families

Mechanism recovery, placebo, rolling-origin, spurious-regression and external-check experiments run through the same runner. Commands, budgets and the meaning of each verdict are in [rigor/README.md](rigor/README.md). After a batch:

```bash
python research/rigor/analyze.py --run research/runs/<run-dir> [--run another-run-dir ...]
```

writes `ANALYSIS_RIGOR.md` with verdicts against the thresholds in `rigor/protocols_rigor.json`. The Cambodia target band is a placeholder until the Filmer & Schady (2011) table values are copied in.
