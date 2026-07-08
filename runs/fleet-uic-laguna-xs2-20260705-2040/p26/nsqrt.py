# P26: Newton's method iterating until relative convergence, handles x==0 and x==1, seeds with x.
def isqrt_newton(x):
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    g = x  # seed with x for faster convergence
    while True:
        g_new = 0.5 * (g + x / g)
        if abs(g_new - g) < 1e-15 * abs(g_new):
            return g_new
        g = g_new