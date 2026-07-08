# Codec module providing a unified round_trip interface for multiple backends.

"""Unified codec for CSV, KV, and Pylit serializers.

The function :func:`round_trip` selects the appropriate backend based on the
``fmt`` argument (``"csv"``, ``"kv"`` or ``"pylit"``) and returns the result of
``backend.loads(backend.dumps(obj))``.

The backends live in ``work/<fmt>/.../backend.py`` and each expose ``dumps``
and ``loads`` with the contract described in ``verify.py``.
"""

from importlib import import_module
from typing import Any


def _load_backend(fmt: str):
    """Import and return the backend module for *fmt*.

    Parameters
    ----------
    fmt:
        One of ``"csv"``, ``"kv"`` or ``"pylit"``.

    Returns
    -------
    module
        The backend module exposing ``dumps`` and ``loads``.
    """
    if fmt == "csv":
        # The CSV backend resides in work/csv/csv/backend.py
        return import_module("work.csv.csv.backend")
    if fmt == "kv":
        return import_module("work.kv.backend")
    if fmt == "pylit":
        return import_module("work.pylit.backend")
    raise ValueError(f"Unsupported format: {fmt!r}")


def round_trip(fmt: str, obj: Any) -> Any:
    """Serialize *obj* with the chosen backend and immediately deserialize it.

    This mirrors the contract used in ``verify.py`` – the function must return
    an object that is equal to the original after a full round‑trip.
    """
    backend = _load_backend(fmt)
    return backend.loads(backend.dumps(obj))

__all__ = ["round_trip"]
