# ODE integrator using RK4 with drift-free time computation

def solve(f, y0, t0, t1, n):
    """
    Integrate dy/dt = f(t, y) from t0 to t1 using RK4.
    Uses n steps. Time computed as t = t0 + i*h (never accumulated).
    """
    h = (t1 - t0) / n
    y = y0
    for i in range(n):
        t = t0 + i * h  # drift-free time
        k1 = f(t, y)
        k2 = f(t + h/2, y + h/2 * k1)
        k3 = f(t + h/2, y + h/2 * k2)
        k4 = f(t + h, y + h * k3)
        y = y + h / 6.0 * (k1 + 2*k2 + 2*k3 + k4)
    return y