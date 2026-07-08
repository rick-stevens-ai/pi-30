"""Simple ODE integrator using the classical 4th-order Runge-Kutta method.

The `solve` function integrates dy/dt = f(t, y) from `t0` to `t1` using `n`
steps.  To avoid floating‑point drift we compute the time at each step as
`t = t0 + i * h` instead of accumulating `t += h`.
"""

def solve(f, y0, t0, t1, n):
    """Integrate dy/dt = f(t, y) from t0 to t1.

    Parameters
    ----------
    f : callable(t, y)
        The derivative function.
    y0 : float
        Initial value at t0.
    t0 : float
        Start time.
    t1 : float
        End time.
    n : int
        Number of integration steps.

    Returns
    -------
    float
        Approximation of y(t1).
    """
    if n <= 0:
        raise ValueError("Number of steps n must be positive")
    h = (t1 - t0) / n
    y = y0
    for i in range(n):
        t = t0 + i * h  # compute time without accumulation
        k1 = f(t, y)
        k2 = f(t + h / 2.0, y + h * k1 / 2.0)
        k3 = f(t + h / 2.0, y + h * k2 / 2.0)
        k4 = f(t + h, y + h * k3)
        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return y
