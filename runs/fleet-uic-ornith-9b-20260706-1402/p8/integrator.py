def solve(f, y0, t0, t1, n):
    h = (t1 - t0) / n
    for i in range(n):
        t = t0 + i * h
        k1 = f(t, y0)
        k2 = f(t + 0.5 * h, y0 + 0.5 * h * k1)
        k3 = f(t + 0.5 * h, y0 + 0.5 * h * k2)
        k4 = f(t + h, y0 + h * k3)
        y0 += (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return y0
