def isqrt_newton(x):
    if x < 0:
        raise ValueError("Cannot compute square root of negative number")
    if x == 0:
        return 0.0

    # Initial guess: use 1.0, or x if x > 1 for faster convergence on large numbers
    g = max(1.0, x) / 2.0 if x > 0 else 1.0 
    tolerance = 1e-15  # Double precision relative error tolerance

    while True:
        # Newton's method iteration: g_new = 0.5 * (g + x / g)
        try:
            g_new = 0.5 * (g + x / g)
        except ZeroDivisionError:
             # Should not happen if x > 0 and initial guess is reasonable, but safe guard against it
             return float('inf')

        # Check for convergence using relative error
        if abs(g_new - g) < tolerance * max(abs(g_new), abs(g)):
            return g_new

        g = g_new
