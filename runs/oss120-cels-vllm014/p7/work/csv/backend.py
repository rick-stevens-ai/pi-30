def parse(text: str) -> dict:
    """Parse a single CSV line into a dict with a single key ``fields``.

    The CSV format for this challenge is extremely simple: a single line
    consisting of comma‑separated values with no quoting or escaping. The
    result is a dictionary whose ``"fields"`` entry is a list of the values.

    Example
    -------
    >>> parse("a,b,c")
    {"fields": ["a", "b", "c"]}
    """
    # Split on commas. ``split`` always returns at least one element, even for
    # an empty string, which matches the expected behaviour for a CSV line.
    fields = text.split(",") if text else []
    return {"fields": fields}
