def solve(f, y0, t0, t1, n):
    """
    Integrates dy/dt = f(t,y) from t0 to t1 using RK4 with n steps.
    Time at each step is computed as ti = t0 + i*h without accumulating error.
    Returns (final_time, final_y_approx).
    """
    h = (t1 - t0) / n
    y = y0
    for i in range(n):
        ti = t0 + i * h
        k1 = f(ti, y)
        k2 = f(ti + h/2.0, y + (h * k1) / 2.0)
        k3 = f(ti + h/2.0, y + (h * k2) / 2.0)
        k4 = f(ti + h, y + h * k3)
        y += h * (k1 + 2*k2 + 2*k3 + k4) / 6.0
    return t1, y