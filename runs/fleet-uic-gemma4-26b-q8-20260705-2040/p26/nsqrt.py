def isqrt_newton(x):
    if x == 0:
        return 0.0
    g = 1.0
    while True:
        next_g = 0.5 * (g + x / g)
        if next_g == g:
            return g
        g = next_g
