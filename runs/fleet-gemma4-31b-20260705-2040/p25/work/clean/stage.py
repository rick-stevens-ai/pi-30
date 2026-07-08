def clean(rows):
    """
    Cleans the input rows by converting each element to a float.
    Elements that cannot be converted (e.g., None, empty strings, non-numeric strings) are dropped.
    """
    cleaned_data = []
    for row in rows:
        try:
            # Attempt to convert the row value to a float.
            # This handles numeric types and strings that look like numbers.
            # It will raise TypeError for None and ValueError for empty or non-numeric strings.
            val = float(row)
            cleaned_data.append(val)
        except (ValueError, TypeError):
            # Skip elements that are not convertible to float.
            continue
    return cleaned_data
