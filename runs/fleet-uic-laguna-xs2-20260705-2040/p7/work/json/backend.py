"""JSON backend: parse a JSON object string -> dict via stdlib json."""

import json


def parse(text: str) -> dict:
    """Parse a JSON object string and return the resulting dict.
    
    Args:
        text: A JSON object string
        
    Returns:
        dict: The parsed JSON object
    """
    return json.loads(text)