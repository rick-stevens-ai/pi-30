# P26 SEED: fixed 5 Newton iterations from guess=1.0.
def isqrt_newton(x):
    """Full double precision sqrt using Newton's method."""
    if x == 0.0 or x == 1.0:
        return float(x)
    g = x
    while True:
        nxt = 0.5 * (g + x / g)      # Newton step
        rel_err = abs(nxt - g) / max(1e-20, abs(g))
        if rel_err < 1e-12:       # converge to double precision
            return nxt
        g = nxt

def sqrt(x):
    """Alias for isqrt_newton."""
    return isqrt_newton(x)