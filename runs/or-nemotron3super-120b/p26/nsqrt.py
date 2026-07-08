def isqrt_newton(x):
    """Compute square root of x using Newton's method with convergence tolerance."""
    if x == 0 or x == 1:
        return float(x)
    # Initial guess: x > 0 because x > 0 and x != 1 (if x==1 handled above)
    g = x / 2.0
    # machine epsilon for double precision
    eps = 2.0 ** -52
    while True:
        new_g = 0.5 * (g + x / g)
        if abs(new_g - g) < eps * abs(new_g):
            break
        g = new_g
    return new_g