# P26: Newton's method for sqrt, iterating until convergence.
def isqrt_newton(x):
    if x == 0:
        return 0.0
    if x == 1:
        return 1.0
    g = 1.0 if x < 2 else x  # better initial guess for large x
    while True:
        g_new = 0.5 * (g + x / g)
        if abs(g_new - g) < 1e-16 * g_new:
            return g_new
        g = g_new
