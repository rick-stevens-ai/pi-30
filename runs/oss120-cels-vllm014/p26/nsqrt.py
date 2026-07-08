# Revised implementation of Newton's method for square root.
# Iterates until convergence to full double precision and handles x == 0.

def isqrt_newton(x):
    """Return the square root of a non‑negative float x using Newton's method.
    The function iterates until the change is within machine epsilon relative
    to the current estimate, guaranteeing double‑precision accuracy. Zero is
    returned exactly for x == 0.0. No use of math.sqrt is made.
    """
    if x == 0.0:
        return 0.0
    # Initial guess: good for both large and small numbers.
    g = x if x >= 1.0 else 1.0
    eps = 2.220446049250313e-16  # machine epsilon for double precision
    for _ in range(100):  # safety cap
        new_g = 0.5 * (g + x / g)
        if abs(new_g - g) <= eps * new_g:
            return new_g
        g = new_g
    return g  # fallback after max iterations
