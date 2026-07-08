def solve(f, y0, t0, t1, n):
    """Integrate dy/dt = f(t,y) from t0 to t1 using RK4.
    
    Args:
        f: function t, y -> dy/dt
        y0: initial value y(t0)
        t0: start time
        t1: end time
        n: number of steps
        
    Returns:
        y(t1) computed by RK4
    """
    h = (t1 - t0) / n
    y = y0
    for step in range(n):
        t = t0 + step * h
        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h/2, y + k2/2)
        k4 = h * f(t + h, y + k3)
        y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
    return y
