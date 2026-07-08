def dumps(obj: dict) -> str:
    """
    Serializes a CSV object {'fields': [...]}.
    Input obj must have a 'fields' key containing an iterable of field values.
    Output is a comma-separated string.
    Example: {'fields': ['a', 'b', 'c']} -> 'a,b,c'
    """
    if 'fields' not in obj or not isinstance(obj['fields'], list):
        raise ValueError("Input object must be of the form {'fields': [...]}")
    return ",".join(map(str, obj['fields']))

def loads(s: str) -> dict:
    """
    Deserializes a CSV string into a CSV object {'fields': [...]}.
    Example: 'a,b,c' -> {'fields': ['a', 'b', 'c']}
    """
    try:
        fields = s.split(',')
        return {'fields': fields}
    except Exception as e:
        raise ValueError(f"Failed to parse CSV string: {e}")

# Note: The KV and Pylit backends are not implemented here, focusing ONLY on 'csv' backend implementation per instructions.