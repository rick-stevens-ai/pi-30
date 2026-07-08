"""CSV backend for serialization.

Provides two simple functions:

* ``dumps(obj)`` – Convert a dictionary with a single key ``"fields"``
  containing a list of values into a comma‑separated string.  The values are
  converted to ``str`` before joining, matching the specification in
  ``PLAN.md`` where ``{"fields": [...]}`` serialises to ``"a,b,c"``.

* ``loads(s)`` – Parse a comma‑separated string back into the dictionary
  ``{"fields": [...]}``.  Empty fields (e.g. an empty input string) result in an
  empty list.

The implementation purposefully avoids any external dependencies and sticks
to the Python standard library only.
"""

from __future__ import annotations

from typing import Any, Dict, List

__all__ = ["dumps", "loads"]


def dumps(obj: Dict[str, List[Any]]) -> str:
    """Serialise ``obj`` to a CSV‑style string.

    Parameters
    ----------
    obj:
        Expected to be a mapping with a key ``"fields"`` whose value is an
        iterable of items.  Each item is converted to ``str`` before being
        joined with commas.

    Returns
    -------
    str
        Comma‑separated representation of the ``fields`` list.  If ``fields``
        is empty, an empty string is returned.
    """
    # Retrieve the fields list – raise a clear error if the contract is not
    # honoured, which helps debugging test failures.
    try:
        fields = obj["fields"]
    except KeyError as exc:
        raise KeyError("CSV backend expects a dict with a 'fields' key") from exc

    # Convert each field to its string representation and join.
    return ",".join(str(item) for item in fields)


def loads(s: str) -> Dict[str, List[str]]:
    """Parse a CSV‑style string back into the ``{"fields": [...]}`` form.

    Parameters
    ----------
    s:
        The comma‑separated string produced by :func:`dumps`.  Leading and
        trailing whitespace is stripped; individual fields are returned exactly
        as they appear (no further type conversion is performed).

    Returns
    -------
    dict
        ``{"fields": [...]}`` where the list contains the split string items.
    """
    # An empty string corresponds to an empty list of fields.
    if not s:
        return {"fields": []}

    # Split on commas – the specification does not require handling of quoted
    # commas or escaped characters, so a simple split is sufficient.
    fields = s.split(",")
    return {"fields": fields}
