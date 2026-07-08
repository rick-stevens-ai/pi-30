# SAMPLE variance (n-1) using Welford's online algorithm (numerically stable, no catastrophic cancellation, constant streams -> 0)
def running_variance(data):
    count = 0
    mean = 0.0
    m2 = 0.0
    for x in data:
        count += 1
        delta = x - mean
        mean += delta / count
        delta2 = x - mean
        m2 += delta * delta2

    if count < 2:
        return 0.0
    # Sample variance (n-1)
    return m2 / (count - 1)
