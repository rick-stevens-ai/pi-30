def clean(rows) -> list[float]:
    """
    Drops any element not convertible to float (None, "", "x" dropped).
    """
    cleaned_list = []
    for item in rows:
        try:
            # Attempt conversion. This handles strings like '1.2', ints, and floats.
            # It will fail for None or non-numeric strings like 'x'.
            float_val = float(item)
            cleaned_list.append(float_val)
        except (TypeError, ValueError):
            # Drop elements that cannot be converted to float
            continue
    return cleaned_list

def agg(nums: list[float]) -> dict:
    """
    Aggregates a list of numbers into statistics.
    Assumes nums contains only valid floats based on the pipeline flow.
    """
    count = len(nums)
    if count == 0:
        return {'count': 0, 'sum': 0.0, 'mean': 0.0, 'min': float('inf'), 'max': float('-inf')}

    total_sum = sum(nums)
    average = total_sum / count
    minimum = min(nums)
    maximum = max(nums)

    return {
        'count': count,
        'sum': total_sum,
        'mean': average,
        'min': minimum,
        'max': maximum
    }

def fmt(d: dict) -> str:
    """
    Formats a dictionary into a single line 'k=v k=v ...' with keys ALPHA-sorted.
    Stdlib only.
    """
    if not d:
        return ""

    # Sort keys alphabetically
    sorted_keys = sorted(d.keys())

    # Create the formatted string parts
    parts = [f"{key}={d[key]}" for key in sorted_keys]

    # Join them into a single space-separated line
    return " ".join(parts)

if __name__ == '__main__':
    # Example usage and testing (optional, but good practice)
    print("--- Testing clean ---")
    test_rows = [1.0, '2', None, '', 'x', 3.5]
    cleaned = clean(test_rows)
    print(f"Input: {test_rows}")
    print(f"Cleaned: {cleaned}")

    print("\n--- Testing agg ---")
    test_nums = [1.0, 2.0, 3.0]
    aggregated = agg(test_nums)
    print(f"Input: {test_nums}")
    print(f"Aggregated: {aggregated}")

    print("\n--- Testing fmt ---")
    test_dict = {'max': 5.0, 'count': 3, 'sum': 6.0, 'mean': 2.0}
    formatted = fmt(test_dict)
    print(f"Input: {test_dict}")
    print(f"Formatted: {formatted}")