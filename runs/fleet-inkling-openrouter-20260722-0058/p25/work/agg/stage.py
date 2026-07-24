def agg(nums):
    count = len(nums)
    s = sum(nums)
    mean = s / count if count else 0.0
    return {
        'count': count,
        'sum': float(s),
        'mean': float(mean),
        'min': float(min(nums)) if nums else 0.0,
        'max': float(max(nums)) if nums else 0.0,
    }
