def clean(rows: list) -> list[float]:
    """
    Cleans a list of mixed types by dropping any element that is not convertible to float.
    Drops None, "", and "x".
    """
    cleaned_list = []
    for item in rows:
        if item is None or item == '' or item == 'x':
            continue
        try:
            # Attempt to convert to float
            cleaned_list.append(float(item))
        except (ValueError, TypeError):
            # Drop if conversion fails for other reasons
            continue
    return cleaned_list
