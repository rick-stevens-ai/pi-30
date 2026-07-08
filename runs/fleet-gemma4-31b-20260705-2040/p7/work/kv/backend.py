def parse(text):
    """
    Parses a KV string like 'k1=v1;k2=v2' into a dictionary {'k1': 'v1', 'k2': 'v2'}.
    """
    result = {}
    if not text:
        return result
    pairs = text.split(';')
    for pair in pairs:
        if '=' in pair:
            k, v = pair.split('=', 1)
            result[k] = v
    return result
