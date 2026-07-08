"""Dispatch module.

Provides ``dispatch(kind: str, text: str) -> dict`` which routes the
``text`` to the appropriate backend in :pycode:`work/{csv,kv,json}`.

Each backend exposes ``parse(text: str) -> dict``.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

# Mapping from kind to backend file location
_BACKEND_PATHS = {
    "csv": Path("work/csv/work/csv/backend.py"),
    "kv": Path("work/kv/backend.py"),
    "json": Path("work/json/backend.py"),
}

# Cache loaded parse functions to avoid re-importing repeatedly
_loaded_parsers = {}


def _load_parser(kind: str):
    """Load the ``parse`` function for the given ``kind``.

    Raises ``KeyError`` if the kind is unknown.
    """
    if kind in _loaded_parsers:
        return _loaded_parsers[kind]
    path = _BACKEND_PATHS.get(kind)
    if path is None or not path.is_file():
        raise KeyError(f"Unknown backend kind: {kind!r}")

    spec = importlib.util.spec_from_file_location(f"{kind}_backend", path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise ImportError(f"Cannot import backend for kind {kind!r}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    parser = getattr(module, "parse", None)
    if not callable(parser):  # pragma: no cover
        raise ImportError(f"Backend for kind {kind!r} does not expose a callable parse()")
    _loaded_parsers[kind] = parser
    return parser


def dispatch(kind: str, text: str) -> dict:
    """Dispatch ``text`` to the appropriate backend.

    Parameters
    ----------
    kind:
        One of ``"csv"``, ``"kv"`` or ``"json"``.
    text:
        Raw text input for the backend.

    Returns
    -------
    dict
        Result of the backend's :func:`parse` function.
    """
    parser = _load_parser(kind)
    return parser(text)

# If executed directly, run a small test suite to demonstrate usage.
if __name__ == "__main__":  # pragma: no cover
    assert dispatch("csv", "a,b,c") == {"fields": ["a", "b", "c"]}
    assert dispatch("kv", "k1=v1;k2=v2") == {"k1": "v1", "k2": "v2"}
    assert dispatch("json", '{"x": 1, "y": [2, 3]}') == {"x": 1, "y": [2, 3]}
    print("dispatch module works")
