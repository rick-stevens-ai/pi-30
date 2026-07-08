def agg(nums):
    """Compute count, sum, mean, min, max from a list of floats."""
    count = len(nums)
    s = sum(nums)
    return {
        "count": count,
        "sum": s,
        "mean": s / count,
        "min": min(nums),
        "max": max(nums),
    }
