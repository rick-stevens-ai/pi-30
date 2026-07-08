"""Codec: fan-out to the three serializer backends."""

import importlib


def round_trip(fmt: str, obj) -> object:
    """Serialize *obj* with the *fmt* backend, then deserialize it back."""
    mod = importlib.import_module(f"work.{fmt}.backend")
    return mod.loads(mod.dumps(obj))
