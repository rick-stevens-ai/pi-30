def dumps(obj: dict) -> str:
    """Dumps {"fields": [...]} to "a,b,c" string."""
    return ",".join(map(str, obj["fields"]))

def loads(s: str) -> dict:
    """Loads "a,b,c" string to {"fields": [...]} dict."""
    if not s:
        return {"fields": []}
    return {"fields": s.split(",")}
