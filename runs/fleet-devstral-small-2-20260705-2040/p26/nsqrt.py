def nsqrt(x):
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0
    g = x  # Initial guess
    while True:
        g_next = 0.5 * (g + x / g)
        # Converge when relative error is below machine epsilon
        if abs(g_next - g) < 1e-15 * abs(g):
            return g_next
        g = g_next
