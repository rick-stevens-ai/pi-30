def parse(text: str) -> dict:
    """
    Parses a single CSV line into a dictionary with a "fields" key.
    Example: 'a,b,c' -> {"fields": ["a", "b", "c"]}
    """
    if not text:
        return {"fields": []}
    fields = text.split(',')
    return {"fields": fields}
