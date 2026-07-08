def dumps(obj):
    """Serialise a flat dict to 'k1=v1;k2=v2'."""
    return ';'.join(f'{k}={v}' for k, v in obj.items())


def loads(s):
    """Deserialise 'k1=v1;k2=v2' back to a flat dict."""
    if not s:
        return {}
    result = {}
    for pair in s.split(';'):
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key = pair
            value = ''
        result[key] = value
    return result
