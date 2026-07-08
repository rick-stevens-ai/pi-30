"""JSON backend: parse a JSON object string -> dict via stdlib json."""

import json


def parse(text: str) -> dict:
    """Parse a JSON object string into a dict.

    Args:
        text: A JSON object string (e.g., '{"key": "value"}')

    Returns:
        The parsed dict.
    """
    return json.loads(text)