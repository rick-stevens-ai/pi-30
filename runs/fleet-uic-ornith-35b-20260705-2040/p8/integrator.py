"""Integrator module — provides solve(f, y0, t0, t1, n)."""


def solve(f, y0, t0, t1, n):
    """Advance y'(t) = f(t, y) via classical RK4 on a drift-free grid.

    Time is computed as *no-accumulate*:  t_step = t0 + step*h
    so floating-point drift cannot corrupt the final time value.
    """
    h = (t1 - t0) / n

    y = float(y0)
    for step in range(n):
        # Drift-free grid: never use `t += h`
        t_step  = t0 + step * h
        t_next  = t0 + (step + 1) * h

        k1 = f(t_step, y)
        k2 = f(t_step + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(t_step + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(t_next,           y +       h   * k3)

        y += (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    return y
