# P18 SEED: Welford's online algorithm for sample variance (n-1 denominator).
# Numerically stable, no catastrophic cancellation, handles constant streams.
def running_variance(data):
    n = 0
    mean = 0.0
    m2 = 0.0
    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        m2 += delta * delta2
    if n < 2:
        return 0.0
    return m2 / (n - 1)  # sample variance (n-1)
