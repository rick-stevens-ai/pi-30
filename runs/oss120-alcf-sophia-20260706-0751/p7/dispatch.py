"""Dispatch module for backend parsers.

Provides a single function ``dispatch(kind, text)`` that routes the
``text`` to the appropriate backend based on ``kind``. The supported kinds
are ``"csv"``, ``"kv"`` and ``"json"`` and each backend lives in
``work/<kind>/backend.py`` exposing a ``parse`` function.

The implementation imports the three parsers lazily to keep import time low
and to avoid unnecessary imports when a particular backend is not used.
"""

from importlib import import_module
from typing import Callable, Dict

# Mapping from kind to the dotted module path of the corresponding backend.
_BACKEND_MODULES: Dict[str, str] = {
    "csv": "work.csv.backend",
    "kv": "work.kv.backend",
    "json": "work.json.backend",
}

# Cache of the parsed ``parse`` callables so we import each backend only once.
_parsers: Dict[str, Callable[[str], dict]] = {}


def _get_parser(kind: str) -> Callable[[str], dict]:
    """Return the ``parse`` function for *kind*.

    Parameters
    ----------
    kind: str
        One of ``"csv"``, ``"kv"`` or ``"json"``.

    Raises
    ------
    ValueError
        If *kind* is not one of the supported back‑ends.
    """
    if kind not in _BACKEND_MODULES:
        raise ValueError(f"Unsupported backend kind: {kind!r}")
    if kind not in _parsers:
        module_path = _BACKEND_MODULES[kind]
        module = import_module(module_path)
        _parsers[kind] = getattr(module, "parse")
    return _parsers[kind]


def dispatch(kind: str, text: str) -> dict:
    """Dispatch *text* to the appropriate backend parser.

    Parameters
    ----------
    kind: str
        Identifier of the backend – ``"csv"``, ``"kv"`` or ``"json"``.
    text: str
        The raw input string to be parsed.

    Returns
    -------
    dict
        The dictionary produced by the selected backend's ``parse`` function.
    """
    parser = _get_parser(kind)
    return parser(text)
