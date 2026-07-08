"""KV backend: parse 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}"""


def parse(text: str) -> dict:
    """Parse a KV string into a dictionary."""
    result = {}
    if not text:
        return result
    for pair in text.split(';'):
        if '=' in pair:
            key, value = pair.split('=', 1)
            result[key] = value
    return result