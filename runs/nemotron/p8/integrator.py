def solve(f, y0, t0, t1, n):
    """
    Integrate dy/dt = f(t, y) using RK4 from t0 to t1 with n steps.
    Uses t = t0 + step * h to avoid floating-point accumulation drift.
    """
    if n <= 0:
        raise ValueError("Number of steps must be positive")
    
    h = (t1 - t0) / n
    y = y0
    
    for step in range(n):
        t = t0 + step * h
        
        k1 = f(t, y)
        k2 = f(t + h/2, y + h/2 * k1)
        k3 = f(t + h/2, y + h/2 * k2)
        k4 = f(t + h, y + h * k3)
        
        y = y + h/6 * (k1 + 2*k2 + 2*k3 + k4)
    
    return y