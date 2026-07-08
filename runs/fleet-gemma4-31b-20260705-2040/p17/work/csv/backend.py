def dumps(obj):
    """Serializes a {'fields': [...]} dictionary to 'a,b,c' format."""
    return ",".join(obj["fields"])

def loads(s):
    """Deserializes 'a,b,c' format back to a {'fields': [...]} dictionary."""
    if not s:
        return {"fields": []}
    return {"fields": s.split(",")}
