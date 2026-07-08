# P18 SEED: naive sum-of-squares variance (E[x^2]-E[x]^2). Catastrophically
# cancels for large-mean tiny-variance data -> can go negative. Loop must use
# Welford's online algorithm.
def running_variance(data):
    n = 0
    s = 0.0
    sq = 0.0
    for x in data:
        n += 1
        s += x
        sq += x * x
    if n < 2:
        return 0.0
    mean = s / n
    # sample variance via the unstable identity
    return (sq - n * mean * mean) / (n - 1)
