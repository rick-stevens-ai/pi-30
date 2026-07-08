# P26 SEED: fixed 5 Newton iterations from guess=1.0. Fine for x near 1, badly
# non-converged for large x; also no x==0 guard (division-friendly but inaccurate).
def isqrt_newton(x):
    """Compute the square root of x using Newton's method with full double precision.
    Handles x == 0 and x == 1 exactly and iterates until convergence.
    """
    if x == 0.0:
        return 0.0
    # Initial guess: use x for large values, 1.0 for small values to avoid division by zero
    g = x if x >= 1.0 else 1.0
    # Iterate until the update is within machine precision relative to the estimate
    while True:
        next_g = 0.5 * (g + x / g)
        # Convergence check: relative change below 1e-15 (well within double precision)
        if abs(next_g - g) <= 1e-15 * abs(next_g):
            return next_g
        g = next_g
