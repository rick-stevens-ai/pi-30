def dumps(obj):
    """Serialise obj {'fields':[...]} to 'a,b,c'."""
    return ','.join(str(f) for f in obj['fields'])


def loads(s):
    """Deserialise 'a,b,c' back to obj {'fields':[...]}."""
    fields = s.split(',') if s else []
    return {'fields': list(fields)}
