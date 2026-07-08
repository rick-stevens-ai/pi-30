"""csv backend: {"fields":[...]} <-> 'a,b,c'."""


def dumps(obj):
    """Serialize {"fields": [...]} to comma-separated string."""
    return ",".join(str(v) for v in obj["fields"])


def loads(s):
    """Deserialize 'a,b,c' back to {"fields": ["a", "b", "c"]}."""
    fields = s.split(",") if s else []
    return {"fields": [f.strip() for f in fields]}
