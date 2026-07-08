def clean(rows):
    """Clean rows by dropping any element not convertible to float.
    
    Args:
        rows: List of rows where each row is a list of elements
        
    Returns:
        List of floats after dropping non-convertible elements
    """
    cleaned = []
    for row in rows:
        if row is None:
            continue
        for element in row:
            try:
                cleaned.append(float(element))
            except (ValueError, TypeError):
                continue
    return cleaned


def agg(nums):
    """Calculate aggregation statistics.
    
    Args:
        nums: List of numbers
        
    Returns:
        Dictionary with count, sum, mean, min, and max
    """
    if not nums:
        return {'count': 0, 'sum': 0.0, 'mean': 0.0, 'min': 0.0, 'max': 0.0}
    
    count = len(nums)
    total = sum(nums)
    mean = total / count
    minimum = min(nums)
    maximum = max(nums)
    
    return {
        'count': count,
        'sum': total,
        'mean': mean,
        'min': minimum,
        'max': maximum
    }


def fmt(d):
    """Format dictionary as a single line with alpha-sorted keys.
    
    Args:
        d: Dictionary to format
        
    Returns:
        Single line string with 'k=v k=v ...' format
    """
    sorted_keys = sorted(d.keys())
    items = [f"{k}={v}" for k in sorted_keys]
    return ' '.join(items)
