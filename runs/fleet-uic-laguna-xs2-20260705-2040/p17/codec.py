"""Codec module that provides a unified interface to serializer backends."""

import importlib


def round_trip(fmt: str, obj) -> object:
    """Serialize and deserialize obj using the backend for format fmt.
    
    Args:
        fmt: Format name (csv, kv, or pylit)
        obj: Object to serialize/deserialize
        
    Returns:
        The deserialized object after round-trip through the backend.
    """
    backend = importlib.import_module(f"work.{fmt}.backend")
    return backend.loads(backend.dumps(obj))