"""
KV backend parser.

Parses strings of the form ``k1=v1;k2=v2`` into a dictionary.
If empty or malformed parts are present they are ignored.
The function is intentionally simple and uses only stdlib.
"""

def parse(text):
    """Return a mapping parsed from *text*.

    Parameters
    ----------
    text : str
        Input in the format ``k1=v1;k2=v2``.  Keys and values are returned as-is,
        with leading/trailing whitespace preserved exactly as appears in the
        input. Empty parts (e.g. a trailing semi‑slash or two semicolons back to back)
        are ignored.
    """
    result = {}
    # Split on ';' and ignore empty tokens produced by a trailing separator
    for token in text.split(';'):
        if not token:
            continue
        try:
            key, value = token.split('=', 1)
        except ValueError:
            # If there is no '=', ignore this fragment – the specification only
            # mentions correctly formatted k=v pairs.
            continue
        result[key] = value
    return result
