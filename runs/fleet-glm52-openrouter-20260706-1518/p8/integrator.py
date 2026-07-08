"""RK4 ODE integrator with drift-free time grid."""
import math


def solve(f, y0, t0, t1, n):
    """Integrate dy/dt = f(t, y) from t0 to t1 using n steps of classic RK4.

    Time is computed as t = t0 + step*h (never accumulated) to avoid
    floating-point drift. Final step is pinned to t1 as a guard.
    """
    n = max(1, int(n))
    h = (t1 - t0) / n
    y = y0
    for step in range(n):
        t = t0 + step * h
        t_next = t0 + (step + 1) * h
        if step == n - 1:
            t_next = t1  # pin final time, guard against drift
        k1 = f(t, y)
        k2 = f(t + h / 2.0, y + h / 2.0 * k1)
        k3 = f(t + h / 2.0, y + h / 2.0 * k2)
        k4 = f(t_next, y + h * k3)
        y = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return y
