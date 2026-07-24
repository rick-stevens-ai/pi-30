"""Codec integrator: round_trip(fmt, obj) -> loads(dumps(obj)) via matching backend.

Backends live in work/<fmt>/backend.py and each expose dumps(obj)->str and
loads(s)->obj for fmt in {csv, kv, pylit}. This module dynamically selects the
backend for the requested format and performs a serialize/deserialize round trip.
"""

import importlib


def _backend(fmt):
    """Load the backend module for the given format name."""
    return importlib.import_module("work.{}.backend".format(fmt))


def round_trip(fmt, obj):
    """Serialize obj with the matching backend's dumps, then deserialize with loads.

    Returns loads(dumps(obj)) for the backend at work/<fmt>/backend.py.
    """
    backend = _backend(fmt)
    return backend.loads(backend.dumps(obj))