import json

def parse(text: str) -> dict:
    """Parse a JSON object string and return its corresponding Python dict."""
    return json.loads(text)