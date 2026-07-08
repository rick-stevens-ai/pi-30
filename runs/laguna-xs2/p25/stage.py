def agg(nums):
    """Aggregate numbers into statistics dict.
    
    Args:
        nums: list of floats
        
    Returns:
        dict with keys: count (int), sum (float), mean (float), min (float), max (float)
    """
    if not nums:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}
    
    total = sum(nums)
    count = len(nums)
    
    return {
        "count": count,
        "sum": total,
        "mean": total / count,
        "min": min(nums),
        "max": max(nums)
    }