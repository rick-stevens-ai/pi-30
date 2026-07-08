import json
from typing import Dict, Any

def parse(text: str) -> Dict[str, Any]:
    """
    Parses a JSON object string into a Python dictionary.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Handle decoding errors if necessary, though the prompt implies successful parsing for valid input
        raise ValueError(f"Invalid JSON format: {e}")

if __name__ == '__main__':
    # Example usage (for testing purposes)
    json_string = '{"key": "value", "number": 123}'
    try:
        result = parse(json_string)
        print(f"Parsed successfully: {result}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")