def parse(text: str) -> dict:
    """
    Parse a string of the form "k1=v1;k2=v2" into a dict.
    Empty string returns empty dict.
    Empty pairs are ignored.
    If a pair lacks '=', the key is taken as the whole pair with an empty value.
    """
    result = {}
    if not text:
        return result
    pairs = text.split(';')
    for pair in pairs:
        if not pair:
            continue
        if '=' in pair:
            key, value = pair.split('=', 1)
            result[key] = value
        else:
            # No equals sign: treat as key with empty value
            result[pair] = ''
    return result
