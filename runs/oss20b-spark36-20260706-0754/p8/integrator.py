"""
Simple RK4 ODE integrator.

This module defines a single function `solve(f, y0, t0, t1, n)` which integrates the differential equation
denoted by the callable ``f`` for one scalar variable. The integration uses the classical 4th order Runge–Kutta method. Time is computed as ``t = t0 + i*h`` inside the loop to avoid floating‑point drift that would arise from repeatedly adding ``h``.

Usage example (matches converge_check.py):

>>> f = lambda t, y: y  # dy/dt = y  -> y(t) = exp(t)
>>> y = solve(f, 1.0, 0.0, 1.0, 50000)  # should be close to e
"""

from __future__ import annotations


def solve(f, y0: float, t0: float, t1: float, n: int) -> float:
    """Integrate the ODE dy/dt = f(t, y) using RK4.

    Parameters
    ----------
    f : Callable[[float, float], float]
        Right‑hand side of the differential equation.
    y0 : float
        Initial value at ``t0``.
    t0 : float
        Initial time.
    t1 : float
        Final time.
    n : int
        Number of integration steps; must be > 0.

    Returns
    -------
    float
        Approximation to y(t1).
    """
    if n <= 0:
        raise ValueError("Number of steps 'n' must be positive")

    h = (t1 - t0) / n
    y = float(y0)

    for i in range(n):
        # Compute the time at this step, avoiding drift from repeated addition.
        t = t0 + i * h

        k1 = f(t, y)
        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(t + h, y + h * k3)

        y += (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    return y

__all__ = ["solve"]
