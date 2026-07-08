def parse(text: str) -> dict:
    """
    Parses a key-value string in the format "k1=v1;k2=v2" into a dictionary.
    """
    result = {}
    # Split by semicolon to get individual pairs
    pairs = text.split(';')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1) # Use split(..., 1) in case values contain '='
            result[key] = value
    return result

# Example usage (for testing/demonstration):
# print(parse("k1=v1;k2=v2"))
