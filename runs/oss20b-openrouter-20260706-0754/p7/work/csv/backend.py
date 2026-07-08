# Back-end for CSV parsing

def parse(text):
    """Parse a comma-separated string into a dictionary.

    The tests expect a ``{"fields": [<list of fields>]}`` return value.
    Empty fields are preserved; leading/trailing whitespace is stripped.
    """
    # Split on commas. For an empty string we return an empty list.
    if not text:
        return {"fields": []}
    fields = [f.strip() for f in text.split(",")]
    return {"fields": fields}
