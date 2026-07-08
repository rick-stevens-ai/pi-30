# P26 SEED: fixed 5 Newton iterations from guess=1.0. Fine for x near 1, badly
# non-converged for large x; also no x==0 guard (division-friendly but inaccurate).
def isqrt_newton(x):
    g = 1.0
    for _ in range(5):
        g = 0.5 * (g + x / g) if g != 0 else g
    return g
