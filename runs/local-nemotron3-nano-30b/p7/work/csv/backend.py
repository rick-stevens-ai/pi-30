def parse(text: str) -> dict:
    """
    Parse a CSV-like string of comma-separated values into a dictionary with a 'fields' key.

    The returned dict has the form {'fields': [...]} where each element is a stripped
    value from the input. Empty entries are ignored.
    """
    # Split on commas, strip whitespace, filter out empty strings
    fields = [field.strip() for field in text.split(',') if field.strip()]
    return {"fields": fields}