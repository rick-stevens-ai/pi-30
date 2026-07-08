def clean(rows):
    """Clean rows, returning only elements convertible to float."""
    result = []
    for item in rows:
        try:
            result.append(float(item))
        except (ValueError, TypeError):
            pass
    return result