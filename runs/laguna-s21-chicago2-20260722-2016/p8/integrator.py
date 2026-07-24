"""RK4 ODE integrator with drift-free time-stepping.

solve(f, y0, t0, t1, n) integrates dy/dt = f(t, y) from t0 to t1 using
n classical 4th-order Runge-Kutta steps. Time is always computed from
the integer step index (t = t0 + i*h) to avoid floating-point drift.
"""


def solve(f, y0, t0, t1, n):
    """Integrate dy/dt = f(t, y) over [t0, t1] with n RK4 steps.

    Parameters
    ----------
    f : callable(t, y) -> float
        Right-hand side of the ODE.
    y0 : float
        Initial value at t0.
    t0, t1 : float
        Start and end times.
    n : int
        Number of RK4 steps (must be >= 1).

    Returns
    -------
    float
        Approximate solution y(t1).
    """
    h = (t1 - t0) / n
    y = y0
    for i in range(n):
        t = t0 + i * h            # drift-free current time
        t_mid = t0 + (i + 0.5) * h
        t_next = t0 + (i + 1) * h
        k1 = f(t, y)
        k2 = f(t_mid, y + 0.5 * h * k1)
        k3 = f(t_mid, y + 0.5 * h * k2)
        k4 = f(t_next, y + h * k3)
        y = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return y