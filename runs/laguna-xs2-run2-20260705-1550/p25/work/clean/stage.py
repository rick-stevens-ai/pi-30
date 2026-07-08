def clean(rows):
    """Clean rows, converting to float and dropping non-convertible elements."""
    result = []
    for row in rows:
        try:
            result.append(float(row))
        except (ValueError, TypeError):
            pass
    return result