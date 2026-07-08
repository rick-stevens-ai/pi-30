"""CSV backend parser.

Implements the shared interface defined in PLAN.md:
    parse(text: str) -> dict

For CSV backend the expected output is a dictionary with a single key
"fields" whose value is a list of the comma‑separated values from the
input line.

The implementation is intentionally minimal and uses only the Python
standard library.
"""

def parse(text: str) -> dict:
    """Parse a single CSV line.

    Args:
        text: A string representing one CSV record, e.g. "a,b,c".

    Returns:
        dict: ``{"fields": ["a", "b", "c"]}``.  An empty input returns
        ``{"fields": []}``.
    """
    # Split on commas – CSV is defined loosely for this exercise, we do
    # not need full RFC 4180 handling (quotes, escapes, etc.).
    # Preserve the raw field strings, including any surrounding whitespace.
    if not text:
        fields = []
    else:
        fields = text.split(',')
    return {"fields": fields}
