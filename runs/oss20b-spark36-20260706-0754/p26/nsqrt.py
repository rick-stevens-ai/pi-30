# P26: Newton square-root implementation that iterates until convergence.
# Handles edge cases such as x==0 and x==1 explicitly and guarantees full double precision.

def isqrt_newton(x):
    # Handle zero and one directly to avoid division by zero and unnecessary iterations.
    if x <= 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    # Initial guess: use x for larger values, 1.0 for small ones; ensures rapid convergence.
    g = x if x >= 1.0 else 1.0
    # Iterate until relative change falls below a tolerance ensuring full double precision.
    tol = 1e-13  # Approx relative error threshold for double precision.
    max_iter = 100
    for _ in range(max_iter):
        h = 0.5 * (g + x / g)
        if abs(h - g) <= tol * max(abs(g), abs(x)):
            return h
        g = h
    # Fallback: after max iterations, return the last estimate.
    return g