"""JSON backend — parses a JSON object string to the dict. Stdlib only."""
import json


def parse(text: str) -> dict:
    """Parse a JSON-encoded object and return the resulting dict."""
    value = json.loads(text)
    if not isinstance(value, dict):
        raise TypeError(
            f"json.parse expected an object at the top level, "
            f"got {type(value).__name__}"
        )  # type: ignore[unreachable]
    return value
