def clean(rows):
    """Drop any element that isn't convertible to float."""
    result = []
    for r in rows:
        try:
            result.append(float(r))
        except (TypeError, ValueError):
            pass
    return result
