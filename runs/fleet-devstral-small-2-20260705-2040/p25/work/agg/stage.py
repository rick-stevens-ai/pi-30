def clean(rows):
    """Convert rows to list of floats, dropping non-convertible elements."""
    nums = []
    for row in rows:
        try:
            val = float(row)
            nums.append(val)
        except (ValueError, TypeError):
            continue
    return nums


def agg(nums):
    """Compute aggregation statistics."""
    if not nums:
        return {
            'count': 0,
            'sum': 0.0,
            'mean': 0.0,
            'min': 0.0,
            'max': 0.0
        }
    
    total = sum(nums)
    count = len(nums)
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
    """Format dictionary as single line with alpha-sorted keys."""
    items = sorted(d.items(), key=lambda x: x[0])
    parts = [f"{k}={v}" for k, v in items]
    return " ".join(parts)
