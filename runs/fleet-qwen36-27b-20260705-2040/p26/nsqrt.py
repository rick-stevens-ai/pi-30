def isqrt_newton(x):
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    # Initial guess: scale to a reasonable starting point
    g = x if x >= 1.0 else 1.0
    # Newton iterations until full double-precision convergence
    while True:
        g_next = 0.5 * (g + x / g)
        # Check relative change against machine epsilon
        if abs(g_next - g) / g < 1e-16:
            return g_next
        g = g_next
