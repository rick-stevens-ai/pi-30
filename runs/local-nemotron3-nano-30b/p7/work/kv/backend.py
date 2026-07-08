def parse(text: str) -> dict:
    """
    Parse a KV string of the form 'k1=v1;k2=v2...' into a dictionary.

    Each key-value pair is separated by ';' and each pair must contain a
    single '=' separating the key from the value. Whitespace around keys,
    values, and separators is ignored.
    """
    result = {}
    # Split on semicolons to get individual pairs
    for pair in text.split(';'):
        pair = pair.strip()
        if not pair:
            continue  # skip empty segments (e.g., trailing ';' )
        if '=' not in pair:
            continue  # ignore malformed pieces
        key, value = pair.split('=', 1)
        result[key.strip()] = value.strip()
    return result