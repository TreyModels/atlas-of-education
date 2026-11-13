"""Shared helpers for country packs: anchored enrolment targets come from the ledger's UIS completion series."""
import eduengine as ee
from eduengine import ledger as LG

LEVEL_NAMES = ['primary', 'lower', 'upper']


def targets(country, until=2015):
    """Completion series up to `until` (the training period) as anchored-enrolment targets."""
    out = {}
    for m, n in enumerate(LEVEL_NAMES):
        pts = sorted((o['year'], o['value']) for o in LG.OBS
                     if o['country'] == country and o['indicator'] == f'completion_{n}' and o['year'] <= until)
        if pts:
            out[m] = pts
    return out


def settled(country):
    """The least implausible context-variable setting from the last history match (results/context_map.json), or {}.
    This is what 'the model opens settled' means: the pack plus these values reproduces the record within its bands."""
    import json, os
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results', 'context_map.json')
    try:
        return dict(json.load(open(path))[country]['runs'][0]['prm'])
    except (OSError, KeyError, IndexError, ValueError):
        return {}


def modules(queue=False):
    return [ee.PublicSchools(), ee.PrivateSchools(), ee.TutoringMarket(), ee.FiscalState(), ee.QueueLabour()]
