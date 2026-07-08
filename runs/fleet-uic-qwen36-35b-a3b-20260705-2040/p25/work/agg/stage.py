
def agg(nums):
    return {
        "count": len(nums),
        "sum": float(sum(nums)),
        "mean": float(sum(nums) / len(nums)) if nums else 0.0,
        "min": float(min(nums)) if nums else 0.0,
        "max": float(max(nums)) if nums else 0.0,
    }
