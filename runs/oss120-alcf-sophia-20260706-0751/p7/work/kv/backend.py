'''kv backend parser
Parse a simple key-value string.
Expected format: "k1=v1;k2=v2" where pairs are separated by ';' and each pair
contains a key and a value separated by '='. Whitespace around keys and values
is stripped.
Returns a dict mapping keys to values. An empty input returns an empty dict.
''' 

def parse(text: str) -> dict:
    """Parse a kv‑style string into a dictionary.

    Args:
        text: Input string like ``"k1=v1;k2=v2"``.

    Returns:
        ``dict`` – mapping of keys to values.
    """
    result = {}
    if not text:
        return result
    # Split on ';' – ignore empty segments that may arise from a trailing ';'
    pairs = [p for p in text.split(';') if p]
    for pair in pairs:
        # Only split at the first '=', allowing '=' in the value.
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            # No '=', treat whole segment as a key with empty value.
            key, value = pair, ''
        result[key.strip()] = value.strip()
    return result
