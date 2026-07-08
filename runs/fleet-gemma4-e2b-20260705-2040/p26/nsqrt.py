def isqrt_newton(x):
    """Computes the square root of x using Newton's method until convergence."""
    if x < 0:
        # In a real scenario, we might raise an error or return NaN.
        # For this fix focusing on positive inputs for sqrt approximation.
        return float('nan')
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0

    # Newton's method iteration: g_next = 0.5 * (g_current + x / g_current)
    # Initial guess: A reasonable starting point helps convergence speed, but 1.0 is safe.
    g = 1.0
    tolerance = 1e-15  # Sufficient for double precision accuracy

    for _ in range(100):  # Use a fixed high number of iterations for guaranteed convergence within float limits
        next_g = 0.5 * (g + x / g)
        if abs(next_g - g) < tolerance:
            return next_g
        g = next_g

    return g
