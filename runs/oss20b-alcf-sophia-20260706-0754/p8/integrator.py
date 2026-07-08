"""Integrator module implementing solve via RK4.

This module provides a simple ODE integration function using the classic
fourth‑order Runge–Kutta scheme.  It is intentionally minimal to keep the
exercise self‑contained.
"""

import math


def solve(f, y0, t0, t1, n):
    """Integrate dy/dt = f(t, y) from t0 to t1.

    Parameters
    ----------
    f : callable
        ODE function accepting the current time ``t`` and state ``y``.
    y0 : float
        Initial state value at ``t0``.
    t0 : float
        Start time.
    t1 : float
        End time.
    n : int
        Number of integration steps.

    Returns
    -------
    float
        Approximate state value at time ``t1``.
    """
    h = (t1 - t0) / n
    y = y0
    for step in range(1, n + 1):
        t = t0 + step * h  # compute time from step index, never accumulate
        k1 = f(t - h, y)
        k2 = f(t - h / 2, y + h * k1 / 2)
        k3 = f(t - h / 2, y + h * k2 / 2)
        k4 = f(t, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return y
