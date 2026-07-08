"""JSON backend: parse a JSON object string to a dict using stdlib json."""
import json


def parse(text: str) -> dict:
    """Parse a JSON object string to a dict."""
    return json.loads(text)
