def agg(nums):
    total = sum(nums)
    count = len(nums)
    return {
        "count": count,
        "sum": total,
        "mean": total / count,
        "min": min(nums),
        "max": max(nums),
    }
