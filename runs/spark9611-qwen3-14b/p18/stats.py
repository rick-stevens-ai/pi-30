# P18 SEED: naive sum-of-squares variance (E[x^2]-E[x]^2). Catastrophically
# cancels for large-mean tiny-variance data -> can go negative. Loop must use
# Welford's online algorithm.
def running_variance(data):
    n = 0
    mean = 0.0
    sum_sq = 0.0
    for x in data:
        n += 1
        new_mean = mean + (x - mean)/n
        sum_sq += (x - mean) * (x - new_mean)
        mean = new_mean
    if n < 2:
        return 0.0
    return sum_sq / (n - 1)
