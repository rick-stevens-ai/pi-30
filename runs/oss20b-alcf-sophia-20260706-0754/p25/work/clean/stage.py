"""Clean stage: drop non-numeric rows and convert to float."""

def clean(rows):
    """Return a list of floats from rows, ignoring non-numeric values.

    Parameters
    ----------
    rows : Iterable of any
        Input rows may be strings, None, or other types.

    Returns
    -------
    List[float]
        Numeric values converted to float, preserving order.
    """
    cleaned = []
    for r in rows:
        try:
            cleaned.append(float(r))
        except Exception:
            # Skip non-numeric values
            continue
    return cleaned
