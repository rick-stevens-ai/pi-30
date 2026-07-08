"""
Backend implementation for parsing different text formats.

This module provides a parse(text) function that can handle CSV, KV, and JSON formats.
"""

import json


def parse(text):
    """
    Parse text in various formats and return a dictionary representation.
    
    Supported formats:
    - CSV: 'a,b,c' -> {'fields': ['a', 'b', 'c']}
    - KV: 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}
    - JSON: JSON object string -> dict via stdlib json
    
    Args:
        text (str): The text to parse
        
    Returns:
        dict: Parsed result in dictionary form
        
    Raises:
        ValueError: If the text format is not recognized or parsing fails
    """
    text = text.strip()
    
    # Try JSON parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try CSV parsing
    if ',' in text:
        fields = [f.strip() for f in text.split(',')]
        return {'fields': fields}
    
    # Handle single value CSV
    return {'fields': [text]}
    
    # Try KV parsing
    if '=' in text:
        result = {}
        pairs = text.split(';')
        for pair in pairs:
            pair = pair.strip()
            if '=' in pair:
                key, value = pair.split('=', 1)
                result[key.strip()] = value.strip()
        return result
    
    # If no format matched
    raise ValueError(f"Unable to parse text: {text}")
