def parse(text: str) -> dict:
    """Parse a kv string like 'k1=v1;k2=v2' into a dict."""
    result = {}
    for pair in text.split(";"):
        if "=" not in pair:
            continue
        key, value = pair.split("=", 1)
        result[key] = value
    return result
