def clean(rows):
    """Drop any element not convertible to float; return list[float]."""
    result = []
    for row in rows:
        try:
            if isinstance(row, (int, float)):
                result.append(float(row))
            else:
                val = str(row).strip()
                if val == "":
                    continue
                fval = float(val)
                result.append(fval)
        except (TypeError, ValueError):
            continue
    return result
