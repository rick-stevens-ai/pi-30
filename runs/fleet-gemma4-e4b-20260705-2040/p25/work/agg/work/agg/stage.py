def agg(nums) -> dict[str, float | int]:
    """
    Aggregates statistics from a list of numbers.
    Calculates count, sum, mean, min, and max.
    """
    if not nums:
        return {
            'count': 0,
            'sum': 0.0,
            'mean': 0.0,
            'min': float('inf'), # Use infinity for min of an empty set if needed later, though usually handled by caller/context. Here, 0 might be safer depending on expected behavior. Let's use sensible defaults for stats.
            'max': float('-inf')
        }

    count = len(nums)
    total_sum = sum(nums)
    mean = total_sum / count
    minimum = min(nums)
    maximum = max(nums)

    return {
        'count': count,
        'sum': float(total_sum),
        'mean': mean,
        'min': minimum,
        'max': maximum
    }