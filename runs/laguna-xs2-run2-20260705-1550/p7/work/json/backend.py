import json


def parse(text: str) -> dict:
    """Parse a JSON object string into a dict using stdlib json."""
    return json.loads(text)