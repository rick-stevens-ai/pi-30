"""csv backend: {\"fields\":[...]} <-> 'a,b,c'"""


def dumps(obj: dict) -> str:
    """Serialize a fields dict to a comma-separated string."""
    return ",".join(obj["fields"])


def loads(s: str) -> dict:
    """Deserialize a comma-separated string to a fields dict."""
    return {"fields": s.split(",")}
