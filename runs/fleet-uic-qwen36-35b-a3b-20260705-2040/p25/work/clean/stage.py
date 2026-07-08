def clean(rows):
    """Drop any element not convertible to float, return list[float]."""
    result = []
    for row in rows:
        if row is None or (isinstance(row, str) and row.strip() == ""):
            continue
        try:
            val = float(row)
            # reject NaN / Inf
            if val != val or val == float('inf') or val == float('-inf'):
                continue
            result.append(val)
        except (ValueError, TypeError):
            continue
    return result
