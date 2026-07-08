def agg(nums):
    """Aggregate list of numbers into count, sum, mean, min, max."""
    if not nums:
        return {'count': 0, 'sum': 0.0, 'mean': 0.0, 'min': 0.0, 'max': 0.0}
    total = sum(nums)
    n = len(nums)
    mean_val = total / n
    min_val = min(nums)
    max_val = max(nums)
    return {'count': n, 'sum': total, 'mean': mean_val,
            'min': min_val, 'max': max_val}