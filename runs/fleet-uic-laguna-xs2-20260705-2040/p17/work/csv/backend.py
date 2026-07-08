# csv backend: obj {"fields":[...]} <-> "a,b,c"
# stdlib only

def dumps(obj: dict) -> str:
    """Serialize a dict with 'fields' key to comma-separated values."""
    if not isinstance(obj, dict):
        raise TypeError("csv.dumps expects a dict")
    if "fields" not in obj:
        raise ValueError("csv.dumps expects dict with 'fields' key")
    fields = obj["fields"]
    if not isinstance(fields, list):
        raise TypeError("csv.dumps expects 'fields' to be a list")
    return ",".join(str(f) for f in fields)


def loads(s: str) -> dict:
    """Deserialize comma-separated values to dict with 'fields' key."""
    if not s:
        return {"fields": []}
    fields = s.split(",")
    return {"fields": fields}