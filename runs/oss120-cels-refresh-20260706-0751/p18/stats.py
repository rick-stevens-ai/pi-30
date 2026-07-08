# P18 SEED: naive sum-of-squares variance (E[x^2]-E[x]^2). Catastrophically
# cancels for large-mean tiny-variance data -> can go negative. Loop must use
# Welford's online algorithm.
def running_variance(data):
    """Compute the sample variance (denominator n-1) of *data* using
    Welford's online algorithm.

    This algorithm is numerically stable and returns 0.0 for a constant
    stream (zero variance)."""
    n = 0
    mean = 0.0
    M2 = 0.0
    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        M2 += delta * delta2
    if n < 2:
        return 0.0
    return M2 / (n - 1)
