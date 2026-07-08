def agg(nums: list[float]) -> dict:
    """
    Computes statistics for a list of numbers.
    Returns a dictionary with count, sum, mean, min, and max.
    """
    if not nums:
        return {
            "count": 0,
            "sum": 0.0,
            "mean": 0.0,
            "min": 0.0,
            "max": 0.0,
        }

    count = len(nums)
    total_sum = sum(nums)
    return {
        "count": count,
        "sum": float(total_sum),
        "mean": float(total_sum / count),
        "min": float(min(nums)),
        "max": float(max(nums)),
    }
