def agg(nums):
    count = len(nums)
    sum_val = sum(nums) if count else 0.0
    mean_val = (sum_val / count) if count else 0.0
    min_val = min(nums) if count else 0.0
    max_val = max(nums) if count else 0.0
    return {
        'count': count,
        'sum': sum_val,
        'mean': mean_val,
        'min': min_val,
        'max': max_val
    }