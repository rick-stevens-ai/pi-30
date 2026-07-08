def parse(text: str) -> dict:
    """
    Parses a string of key-value pairs separated by semicolons into a dictionary.
    Example: 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}
    """
    result = {}
    if not text:
        return result
    pairs = text.split(';')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            result[key] = value
    return result
