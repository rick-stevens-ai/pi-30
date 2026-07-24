# P18 SEED: naive sum-of-squares variance (E[x^2]-E[x]^2). Catastrophically
# cancels for large-mean tiny-variance data -> can go negative. Loop must use
# Welford's online algorithm.

def running_variance(data):
    # Welford's online algorithm: numerically stable, no catastrophic
    # cancellation, constant streams -> 0 exactly (no NaN). Computes the
    # SAMPLE variance (denominator n-1).
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
    return m2 / (n - 1)