"""RK4 integrator: solve dy/dt = f(t, y) with t = t0 + step*h to avoid drift."""


def solve(f, y0, t0, t1, n):
    h = (t1 - t0) / n
    y = float(y0)
    for step in range(n):
        t = t0 + step * h  # never accumulate: t += h
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h / 2 * k1)
        k3 = f(t + h / 2, y + h / 2 * k2)
        k4 = f(t + h, y + h * k3)
        y += (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return y
