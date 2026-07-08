def clean(rows):
    """Drop non- numeric entries and convert to float."""
    result = []
    for row in rows:
        try:
            val = float(row)
        except (ValueError, TypeError):
            continue
        else:
            result.append(val)
    return result