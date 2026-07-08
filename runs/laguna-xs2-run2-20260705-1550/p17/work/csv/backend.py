# CSV backend: obj {"fields":[...]} <-> "a,b,c"

def dumps(obj):
    """Serialize {"fields":[...]} to "a,b,c"."""
    return ",".join(obj["fields"])

def loads(s):
    """Deserialize "a,b,c" to {"fields":[...]}."""
    return {"fields": s.split(",") if s else []}