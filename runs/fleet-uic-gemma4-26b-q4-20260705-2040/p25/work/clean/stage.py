def clean(rows):
    """Drops any element not convertible to float."""
    result = []
    for row in rows:
        try:
            if row is None:
                continue
            result.append(float(row))
        except (ValueError, TypeError):
            continue
    return result
