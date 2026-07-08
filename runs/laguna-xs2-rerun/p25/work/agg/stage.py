def agg(nums):
    """Aggregate numbers, returning count, sum, mean, min, max."""
    count = len(nums)
    total = float(sum(nums))
    mean = total / count if count > 0 else 0.0
    minimum = float(min(nums)) if nums else 0.0
    maximum = float(max(nums)) if nums else 0.0
    return {"count": count, "sum": total, "mean": mean, "min": minimum, "max": maximum}