'''Dispatch module for parsing different text formats.

Provides a single function ``dispatch(kind, text)`` that routes the
``text`` to the appropriate backend parser based on ``kind``. The supported
kinds are:

* ``"csv"`` – CSV parser located at :pymod:`work.csv.backend`
* ``"kv"``  – KV parser located at :pymod:`work.kv.backend`
* ``"json"`` – JSON parser located at :pymod:`work.json.backend`

If an unknown ``kind`` is supplied a ``ValueError`` is raised.
''' 

from __future__ import annotations

# Import the specific parse functions from each backend. Using absolute
# imports keeps the module independent of the current working directory.
from work.csv.backend import parse as _parse_csv
from work.kv.backend import parse as _parse_kv
from work.json.backend import parse as _parse_json

__all__ = ["dispatch"]


def dispatch(kind: str, text: str):
    """Route *text* to the appropriate parser based on *kind*.

    Parameters
    ----------
    kind:
        One of ``"csv"``, ``"kv"`` or ``"json"``.
    text:
        The input string to be parsed.

    Returns
    -------
    dict:
        The result of the corresponding backend's ``parse`` function.
    """
    if kind == "csv":
        return _parse_csv(text)
    if kind == "kv":
        return _parse_kv(text)
    if kind == "json":
        return _parse_json(text)
    raise ValueError(f"Unsupported kind: {kind!r}")
