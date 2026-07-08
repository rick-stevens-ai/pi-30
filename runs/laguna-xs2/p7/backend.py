"""kv backend: parse 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}"""


def parse(text: str) -> dict:
    """Parse a kv-formatted string into a dict.
    
    Args:
        text: String in format 'k1=v1;k2=v2'
        
    Returns:
        Dictionary like {'k1': 'v1', 'k2': 'v2'}
    """
    result = {}
    if not text:
        return result
    
    pairs = text.split(';')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            result[key] = value
    
    return result