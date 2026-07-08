def parse(text: str) -> dict:
    """Parse 'k1=v1;k2=v2' style key=value pairs into a dict.

    Keys and values are plain strings (no escaping). Pairs are separated
    by semicolons. Returns an empty dict for empty input.
    """
    result = {}
    if not text:
        return result
    for pair in text.split(";"):
        pair = pair.strip()
        if not pair:
            continue
        key, _, value = pair.partition("=")
        result[key] = value
    return result
