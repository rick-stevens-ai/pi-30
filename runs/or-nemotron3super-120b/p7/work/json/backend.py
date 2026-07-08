import json

def parse(text: str) -> dict:
    """
    Parse a JSON object string into a dict.
    """
    return json.loads(text)
