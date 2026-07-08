def clean(rows):
    """clean(rows)->list[float] dropping any element not convertible to float."""
    result = []
    for row in rows:
        try:
            result.append(float(row))
        except (TypeError, ValueError):
            pass
    return result