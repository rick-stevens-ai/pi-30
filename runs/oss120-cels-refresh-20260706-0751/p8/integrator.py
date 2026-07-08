"""
Integrator module providing a stable RK4 solver.

The `solve` function integrates dy/dt = f(t, y) from t0 to t1 using
`n` equal steps.  It **never accumulates the time variable**; instead
it computes the current time as `t = t0 + step * h` for each step.  This
prevents floating‑point drift that would otherwise accumulate when using
`t += h`.  The RK4 scheme yields higher accuracy and ensures convergence
as required by the tests in `converge_check.py`.
"""

from typing import Callable

def solve(f: Callable[[float, float], float], y0: float, t0: float, t1: float, n: int) -> float:
    """Integrate dy/dt = f(t, y) from `t0` to `t1` using `n` RK4 steps.

    Parameters
    ----------
    f: Callable[[float, float], float]
        The derivative function f(t, y).
    y0: float
        Initial value y(t0).
    t0: float
        Start time.
    t1: float
        End time.
    n: int
        Number of integration steps (must be > 0).

    Returns
    -------
    float
        Approximation of y(t1).
    """
    if n <= 0:
        raise ValueError("Number of steps 'n' must be positive")

    h = (t1 - t0) / n
    y = y0
    for i in range(n):
        t = t0 + i * h  # compute exact time for this step, no accumulation
        k1 = f(t, y)
        k2 = f(t + h / 2.0, y + h * k1 / 2.0)
        k3 = f(t + h / 2.0, y + h * k2 / 2.0)
        k4 = f(t + h, y + h * k3)
        y += (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return y
