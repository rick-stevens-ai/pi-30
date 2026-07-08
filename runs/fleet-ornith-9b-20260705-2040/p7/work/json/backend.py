def parse(text: str) -> dict:
    """Parse a JSON object string into a dict via stdlib json.

    The input must be a valid JSON value (object, array, number, etc.).
    Returns the parsed Python representation as a dict for objects.
    Raises ValueError/TypeError on invalid JSON.
    """
    import json
    return json.loads(text)
