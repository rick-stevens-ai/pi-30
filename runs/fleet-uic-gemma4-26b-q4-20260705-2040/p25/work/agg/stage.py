def agg(nums):
    if not nums:
        return {'count': 0, 'sum': 0.0, 'mean': 0.0, 'min': 0.0, 'max': 0.0}
    
    cnt = len(nums)
    s = sum(nums)
    return {
        'count': cnt,
        'sum': float(s),
        'mean': float(s / cnt),
        'min': float(min(nums)),
        'max': float(max(nums))
    }
