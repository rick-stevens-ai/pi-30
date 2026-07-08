def agg(nums):
    """Aggregate numbers, returning count, sum, mean, min, max."""
    count = len(nums)
    return {
        "count": count,
        "sum": sum(nums),
        "mean": sum(nums) / count,
        "min": min(nums),
        "max": max(nums),
    }