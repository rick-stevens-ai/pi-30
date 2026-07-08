def agg(nums):
    """Compute count, sum, mean, min, max over a list of numbers."""
    if not nums:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}
    c = len(nums)
    s = sum(nums)
    mn = min(nums)
    mx = max(nums)
    m = s / c
    return {"count": c, "sum": float(s), "mean": float(m), "min": float(mn), "max": float(mx)}
