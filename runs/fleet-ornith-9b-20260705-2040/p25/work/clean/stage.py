def clean(rows):
    """Drop any element not convertible to float (None, '', 'x' dropped)."""
    result = []
    for row in rows:
        try:
            val = float(row)
            result.append(val)
        except (TypeError, ValueError):
            pass
    return result
