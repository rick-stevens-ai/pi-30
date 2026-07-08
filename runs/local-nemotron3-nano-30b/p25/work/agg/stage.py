def agg(nums):
    count = len(nums)
    total = sum(nums)  # safe as nums is list of numbers convertible to float
    minimum = min(nums)
    maximum = max(nums)
    mean = total / count if count else float("nan")
    return {
        "count": count,
        "sum": total,
        "mean": mean,
        "min": minimum,
        "max": maximum,
    }