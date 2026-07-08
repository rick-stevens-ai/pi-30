# P18 SEED: using Welford's online algorithm for sample variance (n-1).
# Numerically stable, avoids catastrophic cancellation, handles infinite streams.
def running_variance(data):
    count = 0
    mean = 0.0
    M2 = 0.0  # sum of squares of differences from current mean
    for x in data:
        count += 1
        delta = x - mean
        mean += delta / count
        delta2 = x - mean
        M2 += delta * delta2
    if count < 2:
        return 0.0
    # sample variance: divide by (count-1) for unbiased estimator
    return M2 / (count - 1)
