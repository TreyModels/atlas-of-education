# The Minis harness: who wrote which number

Status: `infrastructure`, not a research model. It does not answer a gate question and must not appear in the
catalogue until it has a family folder that does. Its job is bookkeeping: every number that enters `research/`
from an agent run carries a record of the actor, the model, the harness version and the source digest that
produced it.

This folder exists because the site's other artefacts already name those four things informally (`CHANGES.md`,
`research/CHANGELOG.md`, `research/lab.py`'s `environment()` block). An agent running in a chat interface — Minis,
Claude, a DSH session — has no git history of its own, so its outputs can currently only be attributed by
paraphrase. The harness fixes that with three files per run and no new dependency.

## The four nouns

| Noun | Meaning here | Where it is recorded |
|---|---|---|
| **actor** | the human accountable for the run (`trey`) | `run.json` → `actor` |
| **operator** | what initiated the change: `human`, `agent`, `script`, `ci` | `run.json` → `operator` |
| **model** | the model id, verbatim, e.g. `minis/agent-loop`, `deepseek-v4-pro`. Empty for `human` and `script`. | `run.json` → `model` |
| **harness** | the tool that carried the operator's edits: `minis`, `claude-code`, `dsh`, `hand`, `lab.py` | `run.json` → `harness` |

`operator` and `harness` are separate on purpose. A human using Minis is `operator=human, harness=minis`; an
agent in a Claude extension is `operator=agent, harness=claude-code`. Collapsing them makes "did the model or
the person decide this" unanswerable after the fact.

## Record layout

A run is one directory under `records/`, named `<UTC date>T<UTC time>Z-<actor>-<six hex>`:

```
records/2026-11-22T150100Z-trey-9f3a1c/
    run.json        # identity, source digests, declared scope — written before any output exists
    outputs.json    # sha256 of every file the run added or changed, with its byte size
    RUN.md          # what was done, what was not, and what would falsify it — written by make_run_md.py
```

`run.json` is written **first**, by `harness.py open`. Refusing to open a run after output exists is deliberate:
a manifest written afterwards can always be made to look tidy.

### run.json

```json
{
  "schema": 1,
  "run_id": "2026-11-22T150100Z-trey-9f3a1c",
  "started_utc": "2026-11-22T15:01:00Z",
  "actor": "trey",
  "operator": "agent",
  "model": "minis/agent-loop",
  "harness": "minis",
  "harness_version": "2026-11-22",
  "session": "9C92A7CD-AF1D-42B4-AE5D-44401652CA4C",
  "intent": "one declarative sentence, past tense on completion",
  "scope": ["research/minis-harness/"],
  "repo_head": "55732f4728a13adb3aec5173d8bc7f3a4ac7f926",
  "source_digest": "<sha256 over tracked file hashes, see source_digest.py>",
  "network": ["api.github.com", "raw.githubusercontent.com"],
  "notes": "free text; never a place for results"
}
```

Fields that are unknown stay `null`, never guessed. `session` is the chat or terminal identifier when one
exists; it lets a reader find the transcript, which is the only record of *why* the run did what it did.

### outputs.json

```json
{
  "schema": 1,
  "run_id": "2026-11-22T150100Z-trey-9f3a1c",
  "files": [
    {"path": "research/minis-harness/HARNESS.md", "sha256": "…", "bytes": 4821, "kind": "authored"},
    {"path": "research/minis-harness/records/…/RUN.md", "sha256": "…", "bytes": 1330, "kind": "generated"}
  ]
}
```

`kind` is `authored` (a model or person wrote prose), `generated` (a script wrote it), or `copied` (bytes came
from elsewhere unchanged; the record must then name where). A path may appear once per run. Two runs claiming the
same path is a conflict that `harness.py verify` reports and a reviewer resolves; it is not overwritten silently.

## Commands

```
python3 research/minis-harness/harness.py open   --actor trey --operator agent --model minis/agent-loop --intent "..."
python3 research/minis-harness/harness.py close  --run <run_id>
python3 research/minis-harness/harness.py verify [--run <run_id>]
python3 research/minis-harness/harness.py list
```

`close` computes `outputs.json` from the files the run changed (git-aware: staged, unstaged and untracked inside
`scope`) and then writes `RUN.md` through `make_run_md.py`. `verify` re-hashes every claimed file and fails on a
mismatch, a missing file, or two open runs touching the same path. Exit code 0/1, so it can sit in CI next to
`scripts/check-all.sh`.

## What this does not do

- It does not establish that an agent's output is correct. It only makes the claim attributable and the file
  traceable. `scripts/check-run-lifecycle.cjs` still governs what happens to numbers.
- It does not hash the model weights or the transcript; a model id is an assertion by the operator.
- It does not retroactively attribute the 2026-11-22 panel work. That session's outputs went to
  `research/records/2026-11-22-massification-panel/` without a run record; `RUN.md` for it stays absent rather
  than being reconstructed from memory. Absence is a fact worth keeping.
