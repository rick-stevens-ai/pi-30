def parse(text: str) -> dict:
    """Parse a semicolon-separated key=value string into a dict.

    Example: 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}
    """
    result = {}
    for pair in text.split(";"):
        key, _, value = pair.partition("=")
        result[key] = value
    return result
