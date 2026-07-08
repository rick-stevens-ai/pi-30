def solve(f, y0, t0, t1, n):
    """Integrate dy/dt = f(t, y) from t0 to t1 using classical RK4 with n steps."""
    h = (t1 - t0) / n
    y = y0
    for i in range(n):
        t = t0 + i * h  # never accumulate t
        k1 = f(t, y)
        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(t + h, y + h * k3)
        y += (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return y
