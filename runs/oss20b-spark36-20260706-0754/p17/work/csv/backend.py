"""
CSV backend.

Exposes dumps(obj)->str and loads(s)->obj for "csv" fmt which expects a dict with key 'fields' mapping to list of string column names.
"""

from __future__ import annotations

from typing import List, Dict, Any

__all__: list[str] = ["dumps", "loads"]


def dumps(obj: Dict[str, List[str]]) -> str:
    """Serialize the ``fields`` list to a comma‑separated string.
    Only the key ``'fields'`` is considered.  If the list is empty, an empty string is returned.
    """
    fields = obj.get("fields", [])
    return ",".join(map(str, fields))


def loads(s: str) -> Dict[str, List[str]]:
    """Deserialize a comma‑separated string into ``{"fields": [...]}``.
    An empty input yields an empty list of fields.
    """
    if not s:
        return {"fields": []}
    fields = [f.strip() for f in s.split(",")]
    return {"fields": fields}
