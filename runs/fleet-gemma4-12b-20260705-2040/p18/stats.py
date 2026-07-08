# P18 SEED: use Welford's online algorithm for numerically stable sample
# variance calculation (M2 / (n - 1)). Avoids catastrophic cancellation
# and correctly handles constant streams by returning 0.0.
def running_variance(data):
    n = 0
    mean = 0.0
    m2 = 0.0
    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        m2 += delta * (x - mean)
    if n < 2:
        return 0.0
    return m2 / (n - 1)
