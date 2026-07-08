def parse(text: str) -> dict:
    """Parse a single CSV line into a dict with a 'fields' list."""
    # Remove trailing newline and carriage return
    line = text.rstrip('\n\r')
    # Split on comma, preserving empty fields
    fields = line.split(',')
    return {"fields": fields}