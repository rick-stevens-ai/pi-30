"""CSV backend: obj {'fields':[...]} <-> 'a,b,c'"""


def dumps(obj: dict) -> str:
    """Serialize obj with 'fields' key to comma-separated string."""
    return ','.join(obj['fields'])


def loads(s: str) -> dict:
    """Deserialize comma-separated string to obj with 'fields' key."""
    return {'fields': s.split(',')} if s else {'fields': []}