def running_variance(data):
    """
    Compute unbiased sample variance (n-1) via Welford's online algorithm.
    Handles numeric stability and constant streams return 0."""
    n = 0
    mean = 0.0
    S = 0.0
    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        S += delta * (x - mean)
    if n < 2:
        return 0.0
    return S / (n - 1)