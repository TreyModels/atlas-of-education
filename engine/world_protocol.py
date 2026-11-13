"""world_protocol: the smallest common contract for an Atlas world (proposed in the Angkor handoff, 5 Nov 2026).

A world is an executable theory: declared mechanisms, declared assumptions (struts) with provenance, a seeded
runner, observable outputs and benchmarks it can fail. The contract is deliberately small, so it can be added to an
existing engine without rewriting it. The Angkor adapter (`world_angkor.py`) wraps the untouched reference engine.
Existing Atlas worlds are not retrofitted yet; see docs/world_protocol.md for the order.

    class MyWorld(WorldProtocol):
        def metadata(self) -> dict          name, version, status ('experimental/uncalibrated' | 'calibrated' | ...), time unit
        def mechanisms(self) -> list        [{id, statement, switch, evidence_class, ablation}]
        def struts(self) -> list            [{id, statement, value, bounds, provenance}]
        def reset(self, seed, parameters)   start a run; parameters are the intervention schema's fields
        def step(self, intervention=None)   advance one tick; intervention overrides parameters from now on
        def observables(self) -> dict       the latest record of outputs
        def validate(self) -> dict          internal checks on the current state: {check: (passed, detail)}
        def done(self) -> bool

Evidence classes (every benchmark and mechanism carries one): 'established fact', 'published estimate',
'interpretation', 'rival interpretation', 'speculative mechanism', 'illustrative assumption', 'fitted parameter'.
Uncertainty kinds (kept separate in every result): 'stochastic' (seeds), 'parameter' (draws), 'structural' (rival
mechanisms), 'measurement' (benchmark uncertainty).

run(world, seed, parameters, schedule) runs one history and returns it with a manifest: world, version, engine
source hash, seed, parameters, schedule, protocol version. No timestamps, so identical runs give identical manifests.
"""
import hashlib
import json
import os

PROTOCOL_VERSION = '0.1'
EVIDENCE_CLASSES = ('established fact', 'published estimate', 'interpretation', 'rival interpretation',
                    'speculative mechanism', 'illustrative assumption', 'fitted parameter')
UNCERTAINTY_KINDS = ('stochastic', 'parameter', 'structural', 'measurement')
STATUSES = ('experimental/uncalibrated', 'calibrated', 'validated')


class WorldProtocol:
    """Base class. Subclasses implement the methods; `run` and `manifest` come for free."""
    source_files = ()          # files whose SHA-256 identifies the engine version in every manifest

    def metadata(self):
        raise NotImplementedError

    def mechanisms(self):
        raise NotImplementedError

    def struts(self):
        raise NotImplementedError

    def reset(self, seed, parameters=None):
        raise NotImplementedError

    def step(self, intervention=None):
        raise NotImplementedError

    def observables(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError

    def done(self):
        raise NotImplementedError

    # ---- provided
    def engine_hash(self):
        h = hashlib.sha256()
        for f in self.source_files:
            with open(f, 'rb') as fh:
                h.update(fh.read())
        return h.hexdigest()

    def manifest(self, seed, parameters, schedule):
        m = self.metadata()
        return dict(protocol=PROTOCOL_VERSION, world=m['name'], world_version=m['version'], status=m['status'],
                    engine_sha256=self.engine_hash(), seed=int(seed), parameters=dict(parameters or {}),
                    schedule={str(k): v for k, v in (schedule or {}).items()})


def run(world, seed, parameters=None, schedule=None, check_every=0):
    """One seeded history. schedule = {tick_label: intervention dict}, applied before that tick.
    check_every > 0 runs world.validate() every that many ticks and stops with an error on a failed check."""
    world.reset(seed, parameters)
    history, i = [], 0
    while not world.done():
        label = world.next_label() if hasattr(world, 'next_label') else i
        world.step((schedule or {}).get(label))
        history.append(world.observables())
        i += 1
        if check_every and i % check_every == 0:
            bad = {k: v for k, v in world.validate().items() if not v[0]}
            if bad:
                raise AssertionError(f'validation failed at tick {i}: {bad}')
    return dict(history=history, manifest=world.manifest(seed, parameters, schedule))


def load_card(path):
    """A model card (JSON). Checks the fields every world must declare."""
    card = json.load(open(path, encoding='utf8'))
    need = ('name', 'version', 'status', 'claim_limits', 'mechanisms', 'struts', 'interventions', 'observables',
            'benchmarks')
    missing = [k for k in need if k not in card]
    if missing:
        raise ValueError(f'model card {path} lacks {missing}')
    if card['status'] not in STATUSES:
        raise ValueError(f'unknown status {card["status"]}')
    for b in card['benchmarks']:
        if b['evidence_class'] not in EVIDENCE_CLASSES:
            raise ValueError(f'benchmark {b["id"]}: unknown evidence class {b["evidence_class"]}')
        if b['role'] not in ('calibration', 'holdout', 'diagnostic'):
            raise ValueError(f'benchmark {b["id"]}: role must be calibration, holdout or diagnostic')
    for m in card['mechanisms']:
        if m['evidence_class'] not in EVIDENCE_CLASSES:
            raise ValueError(f'mechanism {m["id"]}: unknown evidence class {m["evidence_class"]}')
    return card


def score_benchmarks(card, per_run, scenario='reference'):
    """Fraction of runs of `scenario` passing each benchmark. per_run: list of dicts with key 'benchmarks' mapping
    benchmark id -> bool | None (None = not comparable). A benchmark passes for the world if the fraction >= its
    'pass_share' (default 0.5); 'diagnostic' benchmarks are reported but never called a pass."""
    rows = [r for r in per_run if r.get('scenario', scenario) == scenario]
    out = {}
    for b in card['benchmarks']:
        vals = [r['benchmarks'][b['id']] for r in rows if r['benchmarks'].get(b['id']) is not None]
        share = sum(vals) / len(vals) if vals else None
        verdict = ('not comparable' if share is None else
                   ('diagnostic' if b['role'] == 'diagnostic' else
                    ('pass' if share >= b.get('pass_share', 0.5) else 'FAIL')))
        out[b['id']] = dict(share=share, n=len(vals), verdict=verdict, role=b['role'])
    return out


def here(*p):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), *p)
