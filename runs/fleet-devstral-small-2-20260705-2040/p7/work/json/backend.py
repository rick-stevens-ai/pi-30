"""JSON backend implementation."""
import json


def parse(text: str) -> dict:
    """Parse JSON text into a dictionary.
    
    Args:
        text: A JSON object string
        
    Returns:
        Parsed dictionary
        
    Raises:
        json.JSONDecodeError: If the text is not valid JSON
    """
    return json.loads(text)
