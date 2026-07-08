def agg(nums):
    """
    Aggregates a list of numbers into basic statistics.
    Returns a dictionary with keys: count, sum, mean, min, max.
    """
    if not nums:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}
    
    count = len(nums)
    total_sum = sum(nums)
    mean = total_sum / count
    minimum = min(nums)
    maximum = max(nums)
    
    return {
        "count": count,
        "sum": total_sum,
        "mean": mean,
        "min": minimum,
        "max": maximum
    }
