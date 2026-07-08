# P26 SEED: fixed 5 Newton iterations from guess=1.0. Fine for x near 1, badly
# non-converged for large x; also no x==0 guard (division-friendly but inaccurate).
def isqrt_newton(x):
    if x == 0:
        return 0.0
    g = x if x > 1 else 1.0
    for _ in range(200):
        next_g = 0.5 * (g + x / g)
        if next_g == g:
            break
        g = next_g
    return g
