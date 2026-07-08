# Back-end for KV parsing

def parse(text):
    """Parse a ';' separated key=value string into a dictionary.

    Leading/trailing whitespace around keys and values are stripped.
    Keys must be unique; later duplicates override earlier ones.
    """
    result = {}
    if not text:
        return result
    pairs = text.split(";")
    for pair in pairs:
        if not pair:
            continue
        if "=" not in pair:
            # If no '=', treat as key with empty value
            key = pair.strip()
            if key:
                result[key] = ""
            continue
        key, val = pair.split("=", 1)
        result[key.strip()] = val.strip()
    return result
