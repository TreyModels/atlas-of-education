"""eduengine: a modular engine for education supply, demand, shadow education and SDG 4 outcomes."""
from .core import Engine, Module, CORE_DEFAULTS
from .modules.labour import QueueLabour, CompetitiveLabour
from .modules.schools import PublicSchools, PrivateSchools
from .modules.tutoring import TutoringMarket
from .modules.state import FiscalState
from .modules.sdg4 import SDG4
from .modules.anchor import Anchor

ORDER = ['public_schools', 'private_schools', 'tutoring', 'fiscal_state', 'queue_labour', 'competitive_labour', 'anchor', 'sdg4']


def build(modules, **params):
    """Assemble an engine; modules are sorted into the order their phases require (public before private)."""
    mods = sorted(modules, key=lambda m: ORDER.index(m.name) if m.name in ORDER else 50)
    if not any(m.name == 'sdg4' for m in mods):
        mods.append(SDG4())
    # parameters of modules not in this build are dropped (so one parameter file can serve many module mixes);
    # anything no module knows is an error
    known_all = set(CORE_DEFAULTS)
    for cls in (QueueLabour, CompetitiveLabour, PublicSchools, PrivateSchools, TutoringMarket, FiscalState, Anchor):
        known_all |= set(cls.defaults)
    bad = [k for k in params if k not in known_all]
    if bad:
        raise KeyError(f'unknown parameters: {bad}')
    here = set(CORE_DEFAULTS).union(*[set(m.defaults) for m in mods])
    return Engine(mods, **{k: v for k, v in params.items() if k in here})

# Optional read-only planning comparison; importing does not require Node.
from .planning import audit as planning_audit
