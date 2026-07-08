"""JSON backend parser.

Provides a single function `parse` that takes a JSON object string and returns the
corresponding Python dictionary using the standard library `json` module.
"""

import json
from typing import Any, Dict


def parse(text: str) -> Dict[str, Any]:
    """Parse a JSON object string into a Python ``dict``.

    Parameters
    ----------
    text: str
        A JSON-encoded string representing an object (e.g., ``{"a": 1}``).

    Returns
    -------
    dict
        The resulting Python dictionary.

    Raises
    ------
    json.JSONDecodeError
        If the input string is not valid JSON.
    """
    # The problem statement expects only standard‑library JSON handling.
    # ``json.loads`` already returns the appropriate Python types.
    return json.loads(text)
