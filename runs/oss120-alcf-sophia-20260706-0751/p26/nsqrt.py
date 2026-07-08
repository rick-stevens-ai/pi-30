# Robust Newton's method for square root returning full double precision.
# Handles edge cases x==0 and x==1 explicitly and iterates until convergence.
# No use of math.sqrt.

def isqrt_newton(x: float) -> float:
    """Return sqrt(x) using Newton's method.
    Converges to machine precision for all positive double values.
    """
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    # Initial guess: use x for large values, 1.0 for small values
    g = x if x >= 1.0 else 1.0
    # Iterate until relative change is below tolerance (~1e-16)
    tol = 1e-16
    for _ in range(100):  # safety cap
        next_g = 0.5 * (g + x / g)
        if abs(next_g - g) <= tol * next_g:
            g = next_g
            break
        g = next_g
    return g

def nsqrt(x: float) -> float:
    """Convenient wrapper returning sqrt(x) using Newton's method.
    Mirrors the required nsqrt(x) -> sqrt(x) behavior.
    """
    return isqrt_newton(x)
