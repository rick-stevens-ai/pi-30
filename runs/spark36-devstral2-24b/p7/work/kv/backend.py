import json

def parse(text: str) -> dict:
    """
    Parse a key-value string into a dictionary.
    
    Format: 'k1=v1;k2=v2'
    Example: 'name=John;age=30' -> {'name': 'John', 'age': '30'}
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
