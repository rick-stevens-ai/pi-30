"""Dispatcher for parser backends.

Each backend lives in a subdirectory (``csv``, ``kv``, ``json``) and
exposes a ``parse(text: str) -> dict`` function. This module provides a single
``dispatch`` function that selects the appropriate backend based on the ``kind``
argument and forwards the ``text`` to its ``parse`` implementation.
"""

from __future__ import annotations
import importlib
from typing import Callable, Dict

_BACKEND_MODULES: Dict[str, str] = {
    "csv": "work.csv.backend",
    "kv": "work.kv.kv.backend",
    "json": "work.json.backend",
}

def _load_parser(kind: str) -> Callable[[str], dict]:
    module_name = _BACKEND_MODULES[kind]
    module = importlib.import_module(module_name)
    parser = getattr(module, "parse")
    if not callable(parser):
        raise AttributeError(f"Backend '{kind}' does not expose a callable parse()")
    return parser

def dispatch(kind: str, text: str) -> dict:
    parser = _load_parser(kind)
    return parser(text)
