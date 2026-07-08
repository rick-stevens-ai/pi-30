"""Integrator codec: round_trip(fmt, obj) -> obj using backend dumps/loads."""

from importlib import import_module


def round_trip(fmt: str, obj) -> object:
    """Round-trip serialize and deserialize obj using the fmt backend."""
    backend = import_module(f"work.{fmt}.backend")
    serialized = backend.dumps(obj)
    return backend.loads(serialized)
