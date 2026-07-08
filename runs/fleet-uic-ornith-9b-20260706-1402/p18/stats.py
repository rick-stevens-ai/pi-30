# P18 SEED: naive sum-of-squares variance (E[x^2]-E[x]^2). Catastrophically
# cancels for large-mean tiny-variance data -> can go negative. Loop must use
# Welford's online algorithm.
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
