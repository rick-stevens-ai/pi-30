def clean(rows):
    """
    Drops any element not convertible to float (None, '', 'x' dropped).
    Returns a list of floats.
    """
    result = []
    for row in rows:
        try:
            if row is None:
                continue
            # Note: float('') raises ValueError, which is caught.
            val = float(row)
            result.append(val)
        except (ValueError, TypeError):
            continue
    return result
