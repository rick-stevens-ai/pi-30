'''CSV backend serializer.

Provides two simple functions:

* ``dumps(obj)`` – Convert a Python object into a CSV string.
* ``loads(s)`` – Parse a CSV string back into a Python object.

The expected object format (as defined in ``PLAN.md``) is a mapping with a single
key ``"fields"`` whose value is a list of strings.  ``dumps`` joins the list with
commas (no surrounding whitespace) and ``loads`` performs the inverse operation,
returning a new dict with the ``"fields"`` key.

The implementation is deliberately minimal – it does not attempt to handle
quoted fields, escaped commas, or any CSV nuances because the contract for this
exercise only requires flat, comma‑separated values.
'''  # noqa: D401

from __future__ import annotations

from typing import Any, Dict, List

__all__ = ["dumps", "loads"]


def dumps(obj: Dict[str, List[Any]]) -> str:
    """Serialize *obj* to a CSV string.

    The function expects *obj* to be a mapping with a ``"fields"`` key holding an
    iterable of values.  Each value is converted to ``str`` and then joined by
    commas.  An empty ``fields`` list results in an empty string.
    """
    if not isinstance(obj, dict):
        raise TypeError("CSV backend expects a dict with a 'fields' key")
    if "fields" not in obj:
        raise KeyError("Missing required key 'fields' in object for CSV backend")
    fields = obj["fields"]
    # Ensure we can iterate over the collection; convert each element to str.
    return ",".join(str(item) for item in fields)


def loads(s: str) -> Dict[str, List[str]]:
    """Deserialize *s* – a CSV string – back to the backend's object format.

    An empty input string yields an empty ``fields`` list.  Whitespace surrounding
    each token is stripped to provide a tolerant round‑trip, matching the simple
    ``dumps`` implementation.
    """
    if not isinstance(s, str):
        raise TypeError("CSV backend loads expects a string")
    # ``split`` on commas; an empty string should result in [] rather than [''].
    if s == "":
        fields: List[str] = []
    else:
        fields = [token.strip() for token in s.split(",")]
    return {"fields": fields}
