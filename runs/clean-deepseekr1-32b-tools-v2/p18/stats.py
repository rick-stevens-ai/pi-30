This implementation uses Welford'sOnlineAlgorithm for numerically stable calculation of sample variance with a O(n) time complexity and constant space requirements.def running_variance(data):
    n = len(data)
    if n < 2:
        return float('nan')
    
    k = 0
    mean = 0.0
    M2 = 0.0

    for x in data:
        k +=1
        delta = x - mean
        mean += delta / k
        M2 += delta * (x - mean)

    return M2 / (k - 1)def running_variance(data):
    n = 0
    mean = 0.0
    M2 = 0.0
    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        M2 += (x - mean) * delta
    if n < 2:
        return 0.0
    # Use sample variance (n-1 denominator)
    return M2 / (n - 1)
