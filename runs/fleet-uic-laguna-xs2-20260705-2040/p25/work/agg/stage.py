def agg(nums):
    """Aggregate numbers, returning statistics dictionary.

    Args:
        nums: Iterable of numbers

    Returns:
        dict: {"count":int,"sum":float,"mean":float,"min":float,"max":float}
    """
    result = list(nums)
    count = len(result)
    total = sum(result)
    mean = total / count if count > 0 else 0.0
    return {
        "count": count,
        "sum": float(total),
        "mean": float(mean),
        "min": float(min(result)) if count > 0 else 0.0,
        "max": float(max(result)) if count > 0 else 0.0,
    }