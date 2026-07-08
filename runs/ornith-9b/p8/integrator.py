def solve(f, y0, t0, t1, n):
    h = (t1 - t0) / n
    yk = y0
    for i in range(n + 1):
        t = t0 + i * h
        if i == n:
            return yk
        k1 = f(t, yk)
        k2 = f(t + h/2.0, yk + (h / 2.0) * k1)
        k3 = f(t + h/2.0, yk + (h / 2.0) * k2)
        k4 = f(t + h, yk + h * k3)
        yk += (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
