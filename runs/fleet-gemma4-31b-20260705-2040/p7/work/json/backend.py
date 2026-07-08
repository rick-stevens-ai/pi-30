import json

def parse(text: str) -> dict:
    """Parses a JSON object string into a dictionary."""
    return json.loads(text)
