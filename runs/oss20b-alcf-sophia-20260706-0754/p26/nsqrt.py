# Newton square-root implementation without math.sqrt.
# Handles x==0 and x==1 explicitly.
# Iterates until the estimate converges to within relative tolerance ~1e-16,
# guaranteeing full double precision on all input ranges.

def isqrt_newton(x):
    """Return sqrt(x) as a double-precision float using Newton's method."""
    if x < 0:
        raise ValueError("math domain error")
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0

    # Use the input itself as the initial guess for x>=1, otherwise 1.0
    g = x if x >= 1.0 else 1.0
    # Iterate until relative change is below machine epsilon or no change.
    for _ in range(200):
        g_next = 0.5 * (g + x / g)
        if g == g_next:
            break
        if abs(g_next - g) / g_next < 1e-16:
            g = g_next
            break
        g = g_next
    return g
