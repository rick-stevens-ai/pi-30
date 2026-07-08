def solve(f, y0, t0, t1, n):
    """Integrate dy/dt = f(t, y) using 4th-order Runge‑Kutta.

    Parameters
    ----------
    f : callable
        Function accepting (t, y) and returning dy/dt.
    y0 : float
        Initial condition y(t0) = y0.
    t0 : float
        Initial time.
    t1 : float
        Final time.
    n : int
        Number of equal‑size steps, n > 0.

    Returns
    -------
    float
        Approximation of y(t1).

    Notes
    -----
    The algorithm computes the time at each step as ``t = t0 + i*h``
    instead of accumulating ``t += h``.  This avoids drift caused by
    floating‑point rounding and keeps the true step boundary
    unchanged.  The RK4 update is:

    .. math::

        k1 = h f(t, y)
        k2 = h f(t + h/2, y + k1/2)
        k3 = h f(t + h/2, y + k2/2)
        k4 = h f(t + h, y + k3)
        y_{n+1} = y_n + (k1 + 2k2 + 2k3 + k4)/6
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    h = (t1 - t0) / n
    y = y0
    for i in range(n):
        t = t0 + i * h
        k1 = h * f(t, y)
        k2 = h * f(t + h / 2.0, y + k1 / 2.0)
        k3 = h * f(t + h / 2.0, y + k2 / 2.0)
        k4 = h * f(t + h, y + k3)
        y += (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    return y
