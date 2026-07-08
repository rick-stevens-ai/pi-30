def agg(nums):
    if not nums:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": float('inf'), "max": float('-inf')}
    count = len(nums)
    total_sum = sum(nums)
    min_val = min(nums)
    max_val = max(nums)
    return {
        "count": count,
        "sum": float(total_sum),
        "mean": float(total_sum / count),
        "min": float(min_val),
        "max": float(max_val)
    }
