# clean stage: clean(input_rows) -> list[float]

def clean(rows):
    """
    Clean input rows by converting elements to float and dropping any
    element that isn't convertible (None, "", "x", etc. are dropped).
    
    Args:
        rows: List of values that might be strings or other types
    
    Returns:
        List of floats after filtering out non-convertible elements
    """
    cleaned = []
    for element in rows:
        try:
            # Try to convert the element to float and add it to the result
            converted = float(element)
            cleaned.append(converted)
        except (ValueError, TypeError):
            # Skip elements that can't be converted to float
            pass
    return cleaned
