def running_variance(data):
    n = 0
    mean = 0.0
    M2 = 0.0
    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        M2 += delta * (x - mean)
    if n < 2:
        return 0.0
    return M2 / (n - 1)