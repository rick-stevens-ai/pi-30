def clean(rows):
    """Clean rows, returning only elements convertible to float.

    Drops any element that isn't convertible to float (None, '', 'x', etc.).

    Args:
        rows: Iterable of elements to clean

    Returns:
        list[float]: List of floats from convertible elements
    """
    result = []
    for item in rows:
        try:
            result.append(float(item))
        except (TypeError, ValueError):
            pass
    return result