"""Integrator codec: round_trip(fmt, obj) -> loads(dumps(obj))."""

import sys

# Ensure the work directory is importable from verify.py's location.
if "work" not in sys.path:
    sys.path.insert(0, str(__file__).replace("/codec", "") + "/..")


def _backend(fmt):
    mod = __import__(f"{fmt}.backend", fromlist=["dumps", "loads"])
    return mod.dumps, mod.loads


def round_trip(fmt, obj):
    dumps_fn, loads_fn = _backend(fmt)
    s = dumps_fn(obj)
    return loads_fn(s)
