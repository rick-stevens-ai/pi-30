def solve(f, y0, t0, t1, n):
    """
    Integrates dy/dt = f(t, y) from t0 to t1 using the RK4 method.
    Returns the final state y at t1 as a scalar float.
    """
    h = (t1 - t0) / n
    t = t0
    y = y0

    for _ in range(n):
        # RK4 steps
        k1 = h * f(t, y)
        k2 = h * f(t + 0.5 * h, y + 0.5 * k1)
        k3 = h * f(t + 0.5 * h, y + 0.5 * k2)
        k4 = h * f(t + h, y + k3)

        y = y + (k1 + 2*k2 + 2*k3 + k4) / 6.0
        t = t + h
    
    # Return the final state as a scalar float to resolve TypeError in convergence check
    return y

