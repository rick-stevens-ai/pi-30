# RK4 integrator: compute t = t0 + step*h (never accumulate)
def solve(f, y0, t0, t1, n):
    h = (t1 - t0) / n
    y = y0
    for step in range(n):
        t = t0 + step * h
        k1 = f(t, y)
        k2 = f(t + h/2, y + h*k1/2)
        k3 = f(t + h/2, y + h*k2/2)
        k4 = f(t + h, y + h*k3)
        y = y + h * (k1 + 2*k2 + 2*k3 + k4) / 6
    return y