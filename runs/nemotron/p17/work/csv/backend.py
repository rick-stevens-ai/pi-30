"""csv backend: serialize {"fields":[...]} <-> "a,b,c"."""


def dumps(obj: dict[str, list[str]]) -> str:
    """Serialize a dict with 'fields' key to CSV string."""
    fields = obj.get("fields", [])
    return ",".join(fields)


def loads(s: str) -> dict[str, list[str]]:
    """Deserialize CSV string to dict with 'fields' key."""
    if not s:
        return {"fields": []}
    fields = s.split(",")
    return {"fields": fields}
