"""
Codec module that provides round-trip serialization/deserialization
using different backend formats.

Exposes:
- round_trip(fmt, obj) -> obj: Serializes obj to string using the specified
  format's dumps function, then deserializes it back using loads.
"""

from typing import Any


def round_trip(fmt: str, obj: Any) -> Any:
    """
    Perform a round-trip serialization and deserialization using the
    specified format backend.
    
    Args:
        fmt: The format to use ('csv', 'kv', or 'pylit')
        obj: The object to serialize and deserialize
        
    Returns:
        The deserialized object after round-trip
        
    Raises:
        ValueError: If the format is unknown or serialization fails
    """
    if fmt == "csv":
        from work.csv.backend import dumps, loads
        serialized = dumps(obj, format="csv")
        return loads(serialized, format="csv")
    elif fmt == "kv":
        from work.kv.backend import kv_dumps, kv_loads
        serialized = kv_dumps(obj)
        return kv_loads(serialized)
    elif fmt == "pylit":
        from work.pylit.backend import dumps, loads
        serialized = dumps(obj)
        return loads(serialized)
    else:
        raise ValueError(f"Unknown format: {fmt}")
