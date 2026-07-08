"""Dispatcher for parser backends.

Each backend lives in a subdirectory (``csv``, ``kv``, ``json``) and
exposes a ``parse(text: str) -> dict`` function. This module provides a single
``dispatch`` function that selects the appropriate backend based on the ``kind``
argument and forwards the ``text`` to its ``parse`` implementation.
"""

from __future__ import annotations
import importlib
from typing import Callable, Dict

# Mapping from backend name to module path relative to this file.
_BACKEND_MODULES: Dict[str, str] = {
    "csv": "csv.backend",
    "kv": "kv.backend",
    "json": "json.backend",
}

def _load_parser(kind: str) -> Callable[[str], dict]:
    """Load the ``parse`` function for *kind*.

    Parameters
    ----------
    kind:
        One of ``"csv"``, ``"kv"`` or ``"json"``.

    Returns
    -------
    Callable[[str], dict]
        The ``parse`` function provided by the backend.

    Raises
    ------
    KeyError
        If *kind* is not a recognized backend.
    ImportError
        If the backend module cannot be imported.
    AttributeError
        If the module does not define a ``parse`` callable.
    """
    module_name = _BACKEND_MODULES[kind]
    module = importlib.import_module(module_name)
    parser = getattr(module, "parse")
    if not callable(parser):
        raise AttributeError(f"Backend '{kind}' does not expose a callable parse()")
    return parser


def dispatch(kind: str, text: str) -> dict:
    """Dispatch *text* to the appropriate backend parser.

    Parameters
    ----------
    kind:
        Identifier of the backend – ``"csv"``, ``"kv"`` or ``"json"``.
    text:
        Input string to be parsed.

    Returns
    -------
    dict
        The parsed representation returned by the selected backend.
    """
    parser = _load_parser(kind)
    return parser(text)
