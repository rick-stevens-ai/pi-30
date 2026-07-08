def parse(text: str) -> dict:
    """Parse a simple key-value string.

    The input uses a semicolon-separated list of ``key=value`` pairs
    without surrounding quotes.  Values are returned as strings.
    """
    pairs = [p for p in text.split(';') if p]
    result = {}
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            result[key.strip()] = value.strip()
    return result
