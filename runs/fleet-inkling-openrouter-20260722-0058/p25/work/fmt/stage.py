def fmt(d):
    return ' '.join(f"{k}={d[k]}" for k in sorted(d))
