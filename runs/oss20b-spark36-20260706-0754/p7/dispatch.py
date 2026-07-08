"""
Dispatch backends for CSV, KV and JSON parsing.

The top‑level :func:`dispatch` function selects the appropriate backend based on
``kind`` and forwards ``text`` to the underlying :func:`parse` implementation.
"""

from __future__ import annotations

import importlib
from types import ModuleType

# Mapping from kind string to fully‑qualified module path containing a `parse` symbol.
_BACKEND_MAP: dict[str, str] = {
    "csv": "work.csv.backend",
    "kv": "work.kv.backend",
    "json": "work.json.backend",
}

# Cache imported modules so we import each backend only once.
_imported_backends: dict[str, ModuleType] = {}


def _get_backend(kind: str) -> ModuleType:
    """Import and return the backend module for *kind*.

    Parameters
    ----------
    kind : str
        One of ``"csv"``, ``"kv"`` or ``"json"``.

    Returns
    -------
    types.ModuleType
        The imported backend module.
    """
    if kind not in _BACKEND_MAP:
        raise ValueError(f"Unsupported kind {kind!r}. Expected one of {_BACKEND_MAP.keys()}")
    if kind not in _imported_backends:
        mod = importlib.import_module(_BACKEND_MAP[kind])
        _imported_backends[kind] = mod
    return _imported_backends[kind]


def dispatch(kind: str, text: str) -> dict:
    """Dispatch ``text`` to the appropriate backend based on *kind*.

    Parameters
    ----------
    kind : str
        One of ``"csv"``, ``"kv"`` or ``"json"``.
    text : str
        The raw string to parse.

    Returns
    -------
    dict
        Result from the backend's :func:`parse` function.
    """
    backend = _get_backend(kind)
    if not hasattr(backend, "parse"):
        raise AttributeError(f"Backend {kind!r} lacks a 'parse' function")
    return backend.parse(text)

# The module's public names
__all__ = ["dispatch"]
