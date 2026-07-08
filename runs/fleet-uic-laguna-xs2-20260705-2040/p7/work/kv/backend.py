"""
Backend module for parsing text into dictionaries.
Supports CSV, KV, and JSON formats.
"""

import json


def parse(text: str) -> dict:
    """
    Parse text into a dictionary based on format detection.
    
    Formats:
    - csv: 'a,b,c' -> {'fields': ['a', 'b', 'c']}
    - kv: 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}
    - json: JSON object string -> dict (via stdlib json)
    
    Args:
        text: Input string to parse
        
    Returns:
        dict: Parsed result
    """
    text = text.strip()
    
    # Try JSON first (starts with {)
    if text.startswith('{') and text.endswith('}'):
        try:
            result = json.loads(text)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass
    
    # Try KV format (contains = and ;)
    if '=' in text and ';' in text:
        result = {}
        pairs = text.split(';')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                result[key.strip()] = value.strip()
        if result:
            return result
    
    # Try KV format with single pair (key=value without ;)
    if '=' in text and ';' not in text:
        if text.count('=') == 1:
            key, value = text.split('=', 1)
            return {key.strip(): value.strip()}
    
    # Try CSV format (comma-separated values)
    if ',' in text:
        fields = [field.strip() for field in text.split(',')]
        return {'fields': fields}
    
    # Default: return as single field
    return {'fields': [text]}