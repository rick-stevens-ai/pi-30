"""JSON backend.

Implements the shared backend interface:
    parse(text: str) -> dict

Parses a JSON object string into a dict using only the standard library.
"""

import json


def parse(text: str) -> dict:
    """Parse a JSON object string into a dict.

    Args:
        text: A JSON object string, e.g. '{"x": 1, "y": [2, 3]}'.

    Returns:
        The decoded dict.

    Raises:
        json.JSONDecodeError: If the text is not valid JSON.
        TypeError: If the decoded value is not a JSON object/dict.
    """
    result = json.loads(text)
    if not isinstance(result, dict):
        raise TypeError(
            "json backend expects a JSON object, got %s"
            % type(result).__name__
        )
    return result