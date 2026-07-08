def parse(text: str) -> dict:
    """Parses a string of key-value pairs separated by semicolons."""
    if not text.strip():
        return {}
    
    result = {}
    pairs = text.split(';')
    for pair in pairs:
        pair = pair.strip()
        if '=' in pair:
            k, v = pair.split('=', 1)
            result[k.strip()] = v.strip()
    return result
