# integrator.py
# Provides a simple ODE integrator using the classical 4th-order Runge-Kutta (RK4) method.
# The implementation follows the guidelines in converge_check.py: compute the current
# time as t = t0 + step * h (instead of accumulating floating‑point errors) and use a
# stable RK4 scheme so that the error decreases with the number of steps.

def solve(f, y0, t0, t1, n):
    """Integrate dy/dt = f(t, y) from t0 to t1 with n steps using RK4.

    Parameters
    ----------
    f : callable
        Function f(t, y) returning dy/dt.
    y0 : float
        Initial value y(t0).
    t0 : float
        Initial time.
    t1 : float
        Final time.
    n : int
        Number of integration steps (must be > 0).

    Returns
    -------
    float
        Approximation of y(t1).
    """
    if n <= 0:
        raise ValueError("Number of steps n must be positive")

    h = (t1 - t0) / n  # step size
    y = y0
    for step in range(n):
        t = t0 + step * h  # compute current time without accumulation
        k1 = f(t, y)
        k2 = f(t + h / 2.0, y + h * k1 / 2.0)
        k3 = f(t + h / 2.0, y + h * k2 / 2.0)
        k4 = f(t + h, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
    return y
"""
# End of file
"""
