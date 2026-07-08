def clean(rows):
    result = []
    for r in rows:
        if r is None or r == '':
            continue
        try:
            float_r = float(r)
            result.append(float_r)
        except (ValueError, TypeError):
            continue
    return result

def agg(nums):
    count = len(nums)
    sum_ = sum(nums)
    mean = sum_ / count if count > 0 else 0.0
    min_ = min(nums) if count > 0 else 0.0
    max_ = max(nums) if count > 0 else 0.0
    return {\"count\": count, \"sum\": sum_, \"mean\": mean, \"min\": min_, \"max\": max_}

def fmt(d):
    items = sorted(d.items())
    return ' '.join(f'\{k}\={v}' for k, v in items)