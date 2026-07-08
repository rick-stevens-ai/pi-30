"""CSV backend implementation.

Provides two functions:
- dumps(obj) -> str: Serialize an object of the form {"fields": [...]} into a comma-separated
  string.
- loads(s) -> obj: Deserialize a comma-separated string back into the object format.

The implementation follows the specification in ../../PLAN.md and uses only the
standard library.
"""

from __future__ import annotations

from typing import Any, Dict, List

__all__ = ["dumps", "loads"]


def dumps(obj: Dict[str, Any]) -> str:
    """Serialize ``obj`` to a CSV string.

    ``obj`` must be a mapping containing a ``"fields"`` key whose value is an
    iterable of objects that can be converted to ``str``. The resulting string
    joins the stringified items with commas, without any surrounding whitespace.
    """
    if not isinstance(obj, dict):
        raise TypeError("CSV backend expects a dict with a 'fields' key")
    if "fields" not in obj:
        raise KeyError("Missing required key 'fields' in object for CSV backend")
    fields = obj["fields"]
    # Accept any iterable (list, tuple, etc.)
    try:
        iterator = iter(fields)
    except TypeError as exc:
        raise TypeError("'fields' must be iterable") from exc

    # Convert each element to string; ``str`` is sufficient for CSV as per spec.
    return ",".join(str(item) for item in iterator)


def loads(s: str) -> Dict[str, List[str]]:
    """Deserialize a CSV string ``s`` into the backend object.

    An empty string yields an empty ``fields`` list. Otherwise the string is split
    on commas. No special quoting or escaping is required by the specification.
    """
    if not isinstance(s, str):
        raise TypeError("Input to CSV backend loads must be a string")
    # Preserve empty string as empty list; ``split`` on an empty string would
    # return [''], which is not desired.
    fields: List[str] = [] if s == "" else s.split(",")
    return {"fields": fields}
