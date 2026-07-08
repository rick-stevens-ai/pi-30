import math

def solve(f, y0, t0, t1, n):
    """
    Integrate dy/dt = f(t,y) from t0 to t1 using RK4.
    Key feature: compute time explicitly as t = t0 + step*h,
    never accumulate.
    """
    h = (t1 - t0) / n
    y = y0
    for step in range(n):
        t = t0 + step * h  # Never accumulate t += h
        k1 = f(t, y)
        k2 = f(t + h/2, y + h*k1/2)
        k3 = f(t + h/2, y + h*k2/2)
        k4 = f(t + h, y + h*k3)
        y += (h/6) * (k1 + 2*k2 + 2*k3 + k4)
    return y
