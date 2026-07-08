def parse(text: str) -> dict:
    """Parses a string in 'k1=v1;k2=v2' format into a dictionary."""
    result = {}
    if not text:
        return result
    parts = text.split(';')
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            result[key] = value
    return result
