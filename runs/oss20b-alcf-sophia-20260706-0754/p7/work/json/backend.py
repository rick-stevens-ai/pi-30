import json


def parse(text: str) -> dict:
    """Parse a JSON object string into a Python dict.

    The function relies solely on the standard library ``json`` module.
    """
    return json.loads(text)
