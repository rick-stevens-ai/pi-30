"""
Codec module providing round_trip functionality using the three serializer backends.

The implementation mirrors other runs: it imports the appropriate backend from
``work.<fmt>.backend`` and performs ``loads(dumps(obj))``.
"""

from typing import Any


def round_trip(fmt: str, obj: Any) -> Any:
    """Serialize and then deserialize ``obj`` using the specified format.

    Args:
        fmt: One of ``"csv"``, ``"kv"`` or ``"pylit"``.
        obj: The object to be round‑tripped.
    Returns:
        The object after ``loads(dumps(obj))``.
    """
    if fmt == "csv":
        from work.csv.backend import dumps, loads
    elif fmt == "kv":
        from work.kv.backend import dumps, loads
    elif fmt == "pylit":
        from work.pylit.backend import dumps, loads
    else:
        raise ValueError(f"Unknown format: {fmt}")

    return loads(dumps(obj))
