# RK4 integrator for ODE solving
# Uses t = t0 + step*h to avoid accumulation drift

def solve(f, y0, t0, t1, n):
    """Solve dy/dt = f(t,y) from t0 to t1 with n steps using RK4.
    
    Args:
        f: function f(t, y) returning dy/dt
        y0: initial value y(t0)
        t0: start time
        t1: end time
        n: number of steps
    
    Returns:
        y(t1): solution at end time
    """
    h = (t1 - t0) / n
    y = y0
    
    for step in range(n):
        t = t0 + step * h  # Never accumulate t += h to avoid drift
        k1 = f(t, y)
        k2 = f(t + h/2, y + h/2 * k1)
        k3 = f(t + h/2, y + h/2 * k2)
        k4 = f(t + h, y + h * k3)
        y = y + h / 6 * (k1 + 2*k2 + 2*k3 + k4)
    
    return y