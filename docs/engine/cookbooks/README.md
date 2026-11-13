# Cookbooks: practical recipes for working on the Atlas

Short, practical guides to doing one job on this project: goal, inputs, numbered steps with the exact commands,
what you should see, checks, and the failures we actually hit. They are written against the working tree of
6 November 2026 (the v0.11 run report); when the code moves, fix the affected recipe in the same change.

Read `START_HERE.md` first for what the project is. This folder is about *how to do things*, not what the project
claims. The claims live in `docs/` and are labelled in `docs/facts_register.md`; the last run's evidence is in
`RUN_REPORT.md`.

| # | Cookbook | Use it when |
|---|---|---|
| 01 | [Run and rebuild](01_run_and_rebuild.md) | You have the zip and want to check it, rebuild `index.html`, or read `RUN_REPORT.md`. Start here. |
| 02 | [Verify an input](02_verify_an_input.md) | A data value is flagged from memory (`m`), or you need to correct one and keep the provenance. |
| 03 | [Add a model or world](03_add_a_model_or_world.md) | A new engine, world or simulator, from the first test to a working page in the app. |
| 04 | [Monte Carlo and sensitivity](04_monte_carlo_and_sensitivity.md) | You need seeds, priors, matched policy effects, Sobol indices, ABC or a comparison of structures. |
| 05 | [AI-assisted research protocol](05_ai_assisted_research_protocol.md) | You are briefing an AI agent to do a bounded job on this repo, and you have to be able to check it. |
| 06 | [Run the to-do list](06_run_the_todo_list.md) | You are running the Lane A / Lane B plan, splitting work across agents, and packaging the finished run. |

## Conventions used in every recipe

- Run commands from the project root unless the step says otherwise. Where a command must run from `engine/`, it
  is written that way.
- `python` means the project's Python interpreter (a virtual environment on this machine), not the system Python.
  Recipe 01 sets one up.
- Node is optional for the tests, but the browser app is plain JavaScript: Node is needed for the Node test suite
  and for the parity checks. Recipe 01 says which steps `run_all.py` skips without it.
- Generated files are outputs, never sources: `index.html`, `web/data/atlas_data.js`, `web/data/camchild_runs.js`,
  and `RUN_REPORT.md`. Edit `web/*.js` and `web/style.css` and rebuild; recipe 01 has the CI rule.
- The commands in these cookbooks were run on 6 November 2026 with Python 3.11.17 and Node 18.12.1 and 26.12.0.
  `run_all.py` asks for Python 3.10+; CI uses Python 3.12 and Node 22.
- Write only where you are meant to. Recipes 05 and 06 cover the etiquette for splitting a job across people or
  agents: one owner per file, disjoint write scopes, and the acceptance test run by the person who asked.
