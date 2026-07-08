"""
KV backend parser.

Exposes:
    parse(text: str) -> dict

Parses key=value pairs separated by semicolons.
Example: "k1=v1;k2=v2" -> {"k1": "v1", "k2": "v2"}
"""


def parse(text: str) -> dict:
    """
    Parse a key=value string into a dictionary.
    
    Args:
        text: String of format "k1=v1;k2=v2;..."
    
    Returns:
        Dictionary with keys and values extracted from the input.
    """
    result = {}
    if not text:
        return result
    
    pairs = text.split(";")
    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            result[key.strip()] = value.strip()
    
    return result
