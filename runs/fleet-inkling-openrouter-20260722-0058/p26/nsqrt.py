def isqrt_newton(x):
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    g = x if x > 1.0 else 1.0
    while True:
        new_g = 0.5 * (g + x / g)
        if new_g == g:
            break
        g = new_g
    return g
