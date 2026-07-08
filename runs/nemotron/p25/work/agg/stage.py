def agg(nums):
    """Return dict with count, sum, mean, min, max from list of floats."""
    if not nums:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}
    return {
        "count": len(nums),
        "sum": sum(nums),
        "mean": sum(nums) / len(nums),
        "min": min(nums),
        "max": max(nums),
    }
