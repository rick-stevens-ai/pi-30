def dumps(obj: dict) -> str:
    """Serializes an object with a 'fields' key to a CSV string."""
    return ",".join(map(str, obj["fields"]))


def loads(s: str) -> dict:
    """Deserializes a CSV string into an object with a 'fields' key."""
    if not s:
        return {"fields": []}
    return {"fields": s.split(",")}
